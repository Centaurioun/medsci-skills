#!/usr/bin/env python3
"""Format a source-indexed one-paper reading note in Turkish or English.

Consumes researcher-curated evidence JSON, never retrieves a paper, validates
a quoted passage, adds a Zotero item or persists a note. The orchestrator must
verify source identity, content depth and citation authority separately.
Outputs a proposal JSON to stdout with note text and missing-anchor flags.

python3 render_deep_reading_note.py --input sourced_paper.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

MAX_INPUT = 3_000_000
MAX_CLAIMS = 400
MAX_ASSETS = 100
DEPTHS = {"metadata_only", "abstract", "bounded_passages", "full_text_inspected"}
RELATIONS = {"DIRECTLY_REPORTED", "AUTHOR_INFERENCE", "READER_INTERPRETATION", "UNASSESSED"}
TITLES = {
    "tr": ["Bibliyografik kimlik", "Araştırma sorusu ve katkı", "Tasarım ve yöntemler",
           "Bulgular ve nicel kanıt", "Şekiller ve tablolar", "Eleştirel değerlendirme",
           "Araştırmayla ilişkisi", "Açık sorular", "Kanıt ve atıf izlenebilirliği"],
    "en": ["Bibliographic identity", "Research question and contribution", "Design and methods",
           "Results and quantitative evidence", "Figures and tables", "Critical appraisal",
           "Relevance to research", "Open questions", "Evidence and citation provenance"],
}
SECTIONS = ["question", "methods", "results", "critical", "relevance", "unknown"]
IDENTITY = ["title", "year", "doi", "pmid", "zotero_item_key", "zotero_attachment_key"]
ID_RX = re.compile(r"^[A-Za-z][A-Za-z0-9._:-]{0,95}$")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON property " + key)
        result[key] = value
    return result


def txt(value):
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError("Expected explicit string content")
    return value.strip().replace("\r", " ")


def shown(value, language):
    return txt(value) or ("[KAYNAK SAĞLANMADI]" if language == "tr" else "[SOURCE NOT PROVIDED]")


def section(lines, title, content):
    lines.extend(["## " + title, "", content, ""])


def render(data, digest):
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Expected schema_version 1")
    language = data.get("language", "tr")
    if language not in TITLES:
        raise ValueError("Only tr and en output formats are supported")
    titles = TITLES[language]
    paper = data.get("paper")
    if not isinstance(paper, dict) or not txt(paper.get("title")):
        raise ValueError("paper.title is required")
    depth = data.get("retrieval_depth", "metadata_only")
    if depth not in DEPTHS:
        raise ValueError("Unknown retrieval depth")
    text_sections = data.get("sections", {})
    claims = data.get("claims", [])
    assets = data.get("assets", [])
    if not isinstance(text_sections, dict) or not isinstance(claims, list) or not isinstance(assets, list):
        raise ValueError("Invalid sections/claims/assets type")
    if len(claims) > MAX_CLAIMS or len(assets) > MAX_ASSETS:
        raise ValueError("Too many evidence entries")
    warnings = []
    if depth != "full_text_inspected":
        warnings.append("FULL_TEXT_NOT_ESTABLISHED")
    lines = ["# " + txt(paper["title"]), "", "## " + titles[0], ""]
    for field in IDENTITY:
        lines.append("- " + field + ": " + shown(paper.get(field), language))
    lines.extend(["- retrieval_depth (declared, not verified by formatter): " + depth,
                  "- source_input_sha256: " + digest, ""])
    sections_map = {"question": 1, "methods": 2, "results": 3,
                    "critical": 5, "relevance": 6, "unknown": 7}
    for name in SECTIONS[:3]:
        section(lines, titles[sections_map[name]], shown(text_sections.get(name), language))
    lines.extend(["## " + titles[4], ""])
    ids = set()
    for asset in assets:
        if not isinstance(asset, dict):
            raise ValueError("Asset must be an object")
        identifier = txt(asset.get("id"))
        if not identifier or identifier in ids:
            raise ValueError("Asset id missing or duplicated")
        ids.add(identifier)
        locator = txt(asset.get("source_locator"))
        if not locator:
            warnings.append("ASSET_MISSING_SOURCE_LOCATOR:" + identifier)
        lines.extend(["### " + identifier, "",
                      "- source_locator: " + shown(locator, language),
                      "- original_caption: " + shown(asset.get("caption"), language),
                      "- interpretation: " + shown(asset.get("what_it_supports"), language),
                      "- visual_access: " + shown(asset.get("visual_access"), language), ""])
    if not assets:
        lines.extend(["[NO ASSETS SUPPLIED]", ""])
    for name in SECTIONS[3:]:
        section(lines, titles[sections_map[name]], shown(text_sections.get(name), language))
    lines.extend(["## " + titles[8], ""])
    ids.clear()
    for claim in claims:
        if not isinstance(claim, dict):
            raise ValueError("Claim must be an object")
        identifier = txt(claim.get("claim_id"))
        if not ID_RX.fullmatch(identifier) or identifier in ids:
            raise ValueError("Claim ID missing, duplicated or malformed")
        ids.add(identifier)
        relation = claim.get("source_relation", "UNASSESSED")
        if relation not in RELATIONS:
            raise ValueError("Unknown claim relation")
        locator = txt(claim.get("source_locator"))
        if not locator:
            warnings.append("CLAIM_MISSING_SOURCE_LOCATOR:" + identifier)
        lines.extend(["### " + identifier, "",
                      "- claim: " + shown(claim.get("claim_text"), language),
                      "- source_relation (supplied): " + relation,
                      "- source_locator: " + shown(locator, language),
                      "- evidence_excerpt: " + shown(claim.get("evidence_excerpt"), language),
                      "- uncertainty: " + shown(claim.get("uncertainty"), language), ""])
    if not claims:
        lines.extend(["[NO EVIDENCE CLAIMS SUPPLIED]", ""])
    note = "\n".join(lines)
    return {"schema_version": 1, "disposition": "PROPOSAL_ONLY_NOT_PERSISTED",
            "retrieval_depth": depth, "source_input_sha256": digest,
            "note_sha256": hashlib.sha256(note.encode("utf-8")).hexdigest(),
            "note_markdown": note, "grounding_warnings": warnings,
            "not_verified_by_this_script": [
                "Paper identity and exact passages", "Source locator truth",
                "Statistics and scientific interpretation", "Fulltext actually accessed",
                "Any canonical write or Zotero operation"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    try:
        if not args.input.is_file() or args.input.stat().st_size > MAX_INPUT:
            raise ValueError("Missing or oversized input")
        data = args.input.read_bytes()
        result = render(json.loads(data, object_pairs_hook=unique_object),
                        hashlib.sha256(data).hexdigest())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, UnicodeError) as exc:
        print("DEEP_READING_NOTE_ERROR: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
