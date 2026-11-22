#!/usr/bin/env python3
"""Normalize bibliographic screening exports into a proposal-only record manifest.

Accepted local files: RIS, PubMed MEDLINE/NBIB, Web of Science plain text,
and CSV/TSV. Does not access the network or modify files. Writes normalized
JSON (default) or CSV *to stdout only*. Under Academic Research, persist
accepted data exclusively through the governed writer.

Records != reports != studies. Records are assigned stable, per-run IDs.
Strong-identifier disagreements are flagged, never silently deduplicated.
All input sources and raw record indices remain attached to merged rows.
This tool does not perform study eligibility screening or assign inclusion.

Usage:
    python3 import_screening_records.py export.ris export.nbib > proposed_records.json
    python3 import_screening_records.py export.csv --format csv > proposed_records.csv

Does not execute or test any external provider.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

MAX_BYTES = 20_000_000
MAX_RECORDS = 100_000
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\]\);,]+", re.I)
PMID_RE = re.compile(r"^[0-9]{3,12}$")
HEADER_MAP = {
    "title": ("title", "ti", "article title", "publication title", "document title"),
    "doi": ("doi", "digital object identifier"),
    "pmid": ("pmid", "pubmed id", "pubmedid", "pmid/id"),
    "year": ("year", "publication year", "py", "date", "published", "publication date"),
    "author": ("authors", "author", "au", "first author", "author(s)"),
    "journal": ("journal", "journal title", "source", "publication name"),
}


def norm_title(value: str) -> str:
    stripped = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"\w+", stripped))


def doi(value: str) -> str:
    candidate = value.strip().lower()
    candidate = re.sub(r"^(https?://(?:dx\.)?doi\.org/|doi:\s*)", "", candidate)
    match = DOI_RE.search(candidate)
    return match.group(0).rstrip(".,") if match else ""


def pmid(value: str) -> str:
    v = value.strip()
    return v if PMID_RE.fullmatch(v) else ""


def year(value: str) -> str:
    match = re.search(r"\b(?:19|20)\d{2}\b", str(value))
    return match.group(0) if match else ""


def item(title="", doi_value="", pmid_value="", year_value="", author="", journal="", record_type=""):
    return {
        "title": " ".join(str(title).split()),
        "doi": doi(str(doi_value)),
        "pmid": pmid(str(pmid_value)),
        "year": year(str(year_value)),
        "author": " ".join(str(author).split()),
        "journal": " ".join(str(journal).split()),
        "record_type": str(record_type or "").strip(),
    }


def tag_blocks(lines: list[str], kind: str):
    """Read sequential RIS / Web of Science records with continuation lines."""
    rows, current, last_key = [], defaultdict(list), None
    for line in lines:
        if kind == "ris":
            match = re.match(r"^([A-Z0-9]{2})  - (.*)$", line)
            terminator = line.startswith("ER  -")
            continuation = line.startswith("      ") and last_key
        else:
            match = re.match(r"^([A-Z0-9]{2}) (.*)$", line)
            terminator = line.strip() == "ER"
            continuation = line.startswith("   ") and last_key
        if terminator:
            if current:
                rows.append(dict(current))
            current, last_key = defaultdict(list), None
            continue
        if match:
            last_key = match.group(1)
            current[last_key].append(match.group(2).strip())
        elif continuation:
            current[last_key][-1] += " " + line.strip()
    if current:
        rows.append(dict(current))
    return rows


def first(row: dict[str, list[str]], *keys: str) -> str:
    for key in keys:
        vals = row.get(key)
        if vals:
            return vals[0]
    return ""


def parse_ris(lines: list[str]):
    return [
        item(first(x, "TI", "T1", "CT", "BT"),
             first(x, "DO", "M3"),
             first(x, "AN", "PM"),
             first(x, "PY", "Y1", "DA"),
             first(x, "AU", "A1"),
             first(x, "JO", "JF", "T2"),
             first(x, "TY"))
        for x in tag_blocks(lines, "ris")
    ]


def parse_wos(lines: list[str]):
    return [
        item(first(x, "TI"), first(x, "DI"), "", first(x, "PY"),
             first(x, "AU"), first(x, "SO"), first(x, "PT"))
        for x in tag_blocks(lines, "wos")
    ]


def parse_nbib(lines: list[str]):
    records, record, last_key = [], defaultdict(list), None
    for line in lines + [""]:
        if not line.strip():
            if record:
                records.append(dict(record))
            record, last_key = defaultdict(list), None
            continue
        match = re.match(r"^([A-Z0-9]{2,5})\s*-\s(.*)$", line)
        if match:
            last_key = match.group(1)
            record[last_key].append(match.group(2).strip())
        elif line.startswith(" ") and last_key and record[last_key]:
            record[last_key][-1] += " " + line.strip()
    output = []
    for r in records:
        aid = next((v for v in r.get("AID", []) if "[doi]" in v.lower()), "")
        output.append(item(first(r, "TI", "TT"), first(r, "LID") or aid,
                           first(r, "PMID"), first(r, "DP", "DEP", "EDAT"),
                           first(r, "FAU", "AU"), first(r, "JT", "TA"), "MEDLINE"))
    return output


def parse_table(content: str, sep: str):
    rows = csv.DictReader(io.StringIO(content), delimiter=sep)
    if not rows.fieldnames:
        raise ValueError("Input table is missing a header")
    normalized = {str(h).strip().lower(): h for h in rows.fieldnames if h is not None}

    def field(r: dict, key: str) -> str:
        for candidate in HEADER_MAP[key]:
            original = normalized.get(candidate)
            if original is not None:
                return str(r.get(original) or "").strip()
        return ""

    return [
        item(field(r, "title"), field(r, "doi"), field(r, "pmid"),
             field(r, "year"), field(r, "author"), field(r, "journal"), "TABLE")
        for r in rows
    ]


def parse_file(path: Path):
    if not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise ValueError(f"File missing/oversized: {path}")
    content = path.read_text(encoding="utf-8-sig", errors="replace")
    lines = content.splitlines()
    ext = path.suffix.lower()
    if ext == ".ris":
        # Exports from PubMed can sometimes have .ris extension.
        if any(re.match(r"^PMID\s*-\s", ln) for ln in lines[:30]):
            return parse_nbib(lines), "nbib"
        return parse_ris(lines), "ris"
    if ext == ".nbib":
        return parse_nbib(lines), "nbib"
    if ext in {".csv", ".tsv"}:
        return parse_table(content, "\t" if ext == ".tsv" else ","), ext.lstrip(".")
    if ext == ".txt":
        if any(ln.startswith("FN ") or ln.startswith("VR ") for ln in lines[:6]):
            return parse_wos(lines), "wos"
        if any(re.match(r"^PMID\s*-\s", ln) for ln in lines[:30]):
            return parse_nbib(lines), "nbib"
        if any(ln.startswith("TY  -") for ln in lines[:30]):
            return parse_ris(lines), "ris"
    raise ValueError(f"Unrecognized export format: {path}; expected RIS/NBIB/WoS/CSV/TSV")


def conflicting(a: dict, b: dict) -> bool:
    return (bool(a["doi"] and b["doi"] and a["doi"] != b["doi"])
            or bool(a["pmid"] and b["pmid"] and a["pmid"] != b["pmid"]))


def potential_match(a: dict, b: dict) -> tuple[bool, str]:
    if a["doi"] and b["doi"] and a["doi"] == b["doi"]:
        return True, "same_doi"
    if a["pmid"] and b["pmid"] and a["pmid"] == b["pmid"]:
        return True, "same_pmid"
    if a["title"] and b["title"] and norm_title(a["title"]) == norm_title(b["title"]):
        if a["year"] and b["year"] and a["year"] == b["year"]:
            if not (a["doi"] or a["pmid"] or b["doi"] or b["pmid"]):
                return True, "same_title_year_no_ids"
            return False, "title_year_only_manual_review"
    return False, ""


def import_records(paths: list[Path]) -> dict:
    seen = []
    for path in sorted(paths, key=lambda p: str(p)):
        rows, fmt = parse_file(path)
        if len(seen) + len(rows) > MAX_RECORDS:
            raise ValueError("Too many records")
        source_digest = hashlib.sha256(path.read_bytes()).hexdigest()
        for n, row in enumerate(rows, 1):
            if not row["title"] and not row["doi"] and not row["pmid"]:
                continue
            row["origin"] = [{
                "file": str(path), "sha256": source_digest,
                "format": fmt, "source_record_number": n,
            }]
            seen.append(row)

    unique, conflicts, possible = [], [], []
    for candidate in seen:
        merged = False
        for existing in unique:
            matched, why = potential_match(existing, candidate)
            if not matched and not why:
                continue
            if conflicting(existing, candidate):
                conflicts.append({
                    "code": "IDENTIFIER_CONFLICT_NOT_MERGED",
                    "left_origins": existing["origin"], "right_origins": candidate["origin"],
                })
                continue
            if not matched:
                possible.append({
                    "code": "TITLE_YEAR_POTENTIAL_DUPLICATE",
                    "left_origins": existing["origin"], "right_origins": candidate["origin"],
                })
                continue
            existing["origin"].extend(candidate["origin"])
            for key in ("title", "doi", "pmid", "year", "author", "journal", "record_type"):
                if not existing[key] and candidate[key]:
                    existing[key] = candidate[key]
            merged = True
            break
        if not merged:
            unique.append(candidate)
    for n, record in enumerate(unique, 1):
        record["record_id"] = f"R{n:06d}"
        record["screening_decision"] = "NOT_SCREENED"
        record["study_id"] = None
        record["report_id"] = None
    return {
        "schema_version": 1, "disposition": "PROPOSAL_ONLY_NOT_PERSISTED",
        "unit": "bibliographic_record_not_study",
        "totals": {
            "raw_records": len(seen), "unique_records": len(unique),
            "duplicates_merged": len(seen) - len(unique),
            "identifier_conflict_pairs": len(conflicts),
            "possible_duplicate_pairs": len(possible),
        },
        "records": unique,
        "identifier_conflicts": conflicts,
        "possible_duplicates": possible,
        "limitations": [
            "Only exact identifiers or identifier-free exact title/year are auto-deduplicated.",
            "Manual adjudication is required for ambiguous and conflicting bibliographic identity.",
            "A record is not automatically a report or independent study.",
            "No eligibility or inclusion decision was generated.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    args = parser.parse_args()
    try:
        payload = import_records(args.inputs)
        if args.format == "json":
            json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
            print()
        else:
            fields = ["record_id", "title", "doi", "pmid", "year", "author",
                      "journal", "record_type", "screening_decision",
                      "study_id", "report_id", "source_manifest"]
            writer = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            for row in payload["records"]:
                output = {**row, "source_manifest": json.dumps(row["origin"], ensure_ascii=False)}
                writer.writerow(output)
        return 0
    except (OSError, ValueError, UnicodeError, csv.Error) as exc:
        print(f"SCREENING_IMPORT_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
