#!/usr/bin/env python3
"""Proposal-only cross-batch systematic-review screening record ledger.

Connects import_screening_records.py manifest batches without treating search
records as independent reports/studies. Retains a stable SRnnnnnn record ID,
source origins, an append-only reviewer decision history and ambiguity flags.
No file writes or network activity: returns proposed JSON on stdout.

Examples:
  python3 screening_batch_ledger.py ingest --batch batch-01.json
  python3 screening_batch_ledger.py ingest --batch batch-02.json --ledger ledger.json \
    --expected-ledger-sha256 <sha256>
  python3 screening_batch_ledger.py decide --ledger ledger.json --record-id SR000001 \
    --stage title_abstract --reviewer R1 --decision include
  python3 screening_batch_ledger.py summary --ledger ledger.json

Output is a proposal. Only the separately authorized Academic Write
Coordinator -> Manuscript Forge may persist accepted canonical records;
source_sha256 is for caller-controlled compare-and-swap, not proof of a write.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

MAX_INPUT_BYTES = 25_000_000
MAX_RECORDS = 100_000
MAX_EVENTS = 100
ID_RX = re.compile(r"^SR[0-9]{6}$")
REVIEWER_RX = re.compile(r"^[A-Za-z0-9._:@-]{1,80}$")
STAGES = {"title_abstract", "full_text"}
DECISIONS = {"include", "exclude", "unclear", "awaiting_fulltext"}
METADATA_KEYS = ("title", "doi", "pmid", "year", "author", "journal", "record_type")


def reject(message: str) -> None:
    raise ValueError(message)


def unique_properties(pairs: list[tuple[str, object]]) -> dict:
    obj = {}
    for key, value in pairs:
        if key in obj:
            reject(f"Repeated JSON property {key}")
        obj[key] = value
    return obj


def read_json(path: Path) -> tuple[dict, str]:
    if not path.is_file():
        reject(f"File missing: {path}")
    if path.stat().st_size > MAX_INPUT_BYTES:
        reject(f"File too large: {path}")
    data = path.read_bytes()
    obj = json.loads(data, object_pairs_hook=unique_properties)
    if not isinstance(obj, dict):
        reject("Expected a JSON object")
    return obj, hashlib.sha256(data).hexdigest()


def title_key(value: str) -> str:
    return " ".join(re.findall(r"\w+", unicodedata.normalize("NFKC", value).casefold()))


def metadata(rec: dict) -> dict:
    data = {k: rec.get(k, "") for k in METADATA_KEYS}
    if any(not isinstance(v, str) for v in data.values()):
        reject("Bibliographic identity fields must be strings")
    return data


def normalized_origin(value: object) -> list[dict]:
    if not isinstance(value, list):
        reject("origin must be a list")
    result = []
    for item in value:
        if not isinstance(item, dict):
            reject("origin elements must be objects")
        for field in ("file", "sha256", "format", "source_record_number"):
            if field not in item:
                reject(f"Missing origin field: {field}")
        result.append({field: item[field] for field in
                       ("file", "sha256", "format", "source_record_number")})
    return result


def empty_ledger() -> dict:
    return {"schema_version": 1, "next_record_number": 1,
            "records": [], "source_batches": [], "review_required": []}


def validate_ledger(obj: dict) -> None:
    if obj.get("schema_version") != 1 or not isinstance(obj.get("records"), list):
        reject("Expected screening-batch-ledger schema_version=1")
    if len(obj["records"]) > MAX_RECORDS:
        reject("Record count exceeds safety limit")
    if not isinstance(obj.get("next_record_number"), int) or obj["next_record_number"] < 1:
        reject("Invalid next_record_number")
    if not isinstance(obj.get("source_batches"), list) or not isinstance(obj.get("review_required"), list):
        reject("Missing ledger provenance/ambiguity arrays")
    seen = set()
    for rec in obj["records"]:
        if not isinstance(rec, dict) or not isinstance(rec.get("record_id"), str):
            reject("Invalid record")
        rid = rec["record_id"]
        if not ID_RX.fullmatch(rid) or rid in seen:
            reject(f"Malformed/duplicate record ID: {rid}")
        seen.add(rid)
        metadata(rec)
        normalized_origin(rec.get("origin", []))
        decisions = rec.get("review_events")
        if not isinstance(decisions, list) or len(decisions) > MAX_EVENTS:
            reject(f"Invalid review event list for {rid}")


class IdentityIndex:
    """Indexed bibliographic identity lookup, rebuilt once per incoming batch.

    Index values are record offsets, not stored cross-run record IDs. Record IDs
    are always the ledger's durable SRnnnnnn values.
    """

    def __init__(self, records: list[dict]):
        self.by_doi = defaultdict(set)
        self.by_pmid = defaultdict(set)
        self.by_title_year = defaultdict(set)
        for offset, record in enumerate(records):
            self.register(offset, record)

    def register(self, offset: int, record: dict) -> None:
        if record["doi"]:
            self.by_doi[record["doi"]].add(offset)
        if record["pmid"]:
            self.by_pmid[record["pmid"]].add(offset)
        if record["title"] and record["year"]:
            self.by_title_year[(title_key(record["title"]), record["year"])].add(offset)

    def find(self, candidate: dict, records: list[dict]) -> tuple[list[int], list[int]]:
        offsets = set()
        if candidate["doi"]:
            offsets.update(self.by_doi.get(candidate["doi"], ()))
        if candidate["pmid"]:
            offsets.update(self.by_pmid.get(candidate["pmid"], ()))
        if candidate["title"] and candidate["year"]:
            offsets.update(self.by_title_year.get((title_key(candidate["title"]), candidate["year"]), ()))
        matches, advisory = [], []
        for offset in sorted(offsets):
            old = records[offset]
            strong = ((candidate["doi"] and old["doi"] and candidate["doi"] == old["doi"])
                      or (candidate["pmid"] and old["pmid"] and candidate["pmid"] == old["pmid"]))
            same_title_year = (
                candidate["title"] and old["title"] and candidate["year"] and old["year"]
                and candidate["year"] == old["year"]
                and title_key(candidate["title"]) == title_key(old["title"])
            )
            if strong or (same_title_year and not any(
                    (candidate["doi"], candidate["pmid"], old["doi"], old["pmid"]))):
                matches.append(offset)
                # Conflicting titles attached to one identifier need a human
                # check; a matching DOI alone is not evidence that a title
                # transcription or record mapping is scientifically correct.
                if strong and candidate["title"] and old["title"] and (
                    title_key(candidate["title"]) != title_key(old["title"])
                ):
                    advisory.append(offset)
            elif same_title_year:
                advisory.append(offset)
        return matches, advisory


def identifier_conflict(a: dict, b: dict) -> bool:
    return bool((a["doi"] and b["doi"] and a["doi"] != b["doi"])
                or (a["pmid"] and b["pmid"] and a["pmid"] != b["pmid"]))


def add_flag(ledger: dict, code: str, record_ids: list[str],
             import_id: str, note: str) -> None:
    ledger["review_required"].append({
        "code": code, "record_ids": record_ids,
        "source_import_id": import_id, "note": note,
        "status": "HUMAN_ADJUDICATION_REQUIRED",
    })


def incorporate(ledger: dict, batch: dict, import_sha: str) -> dict:
    validate_ledger(ledger)
    if batch.get("schema_version") != 1 or batch.get("unit") != "bibliographic_record_not_study":
        reject("Expected v1 bibliographic-record import manifest")
    records = batch.get("records")
    if not isinstance(records, list) or len(records) > MAX_RECORDS:
        reject("Expected bounded imported records")
    if any(src.get("sha256") == import_sha for src in ledger["source_batches"]):
        reject("This exact import manifest was already accepted; no duplicate batch ingestion")
    stats = {"new": 0, "merged": 0, "ambiguous": 0}
    identity_index = IdentityIndex(ledger["records"])
    for row in records:
        if not isinstance(row, dict):
            reject("Import record must be an object")
        candidate = metadata(row)
        origins = normalized_origin(row.get("origin", []))
        if not candidate["title"] and not candidate["doi"] and not candidate["pmid"]:
            reject("Imported records require title or persistent identifier")
        matches, advisory = identity_index.find(candidate, ledger["records"])
        compatible = [i for i in matches if not identifier_conflict(ledger["records"][i], candidate)]
        collision = [i for i in matches if identifier_conflict(ledger["records"][i], candidate)]
        needs_review = bool(collision or advisory or len(compatible) > 1)
        if len(compatible) == 1 and not needs_review:
            old = ledger["records"][compatible[0]]
            old_origins = {json.dumps(o, sort_keys=True) for o in old["origin"]}
            for origin in origins:
                if json.dumps(origin, sort_keys=True) not in old_origins:
                    old["origin"].append(origin)
                    old_origins.add(json.dumps(origin, sort_keys=True))
            for k in METADATA_KEYS:
                if not old[k]:
                    old[k] = candidate[k]
            identity_index.register(compatible[0], old)
            stats["merged"] += 1
            continue

        number = ledger["next_record_number"]
        if number > 999999:
            reject("Stable record ID capacity exhausted")
        stable_id = f"SR{number:06d}"
        ledger["next_record_number"] += 1
        ledger["records"].append({
            "record_id": stable_id, **candidate, "origin": origins,
            "report_id": None, "study_id": None,
            "identity_state": "PENDING_ADJUDICATION" if needs_review else "IDENTIFIED",
            "review_events": [],
        })
        identity_index.register(len(ledger["records"]) - 1, ledger["records"][-1])
        stats["new"] += 1
        if needs_review:
            stats["ambiguous"] += 1
            add_flag(ledger, "POSSIBLE_IDENTITY_OVERLAP",
                     [ledger["records"][i]["record_id"] for i in sorted(set(matches + advisory))] + [stable_id],
                     import_sha, "Strong identifier disagreement, title-year overlap, or multiple matches; do not combine automatically")
    ledger["source_batches"].append({
        "sha256": import_sha, "raw_record_count": batch.get("totals", {}).get("raw_records"),
        "incoming_unique_records": len(records), **stats,
        "import_flags": {
            "identifier_conflicts": batch.get("identifier_conflicts", []),
            "possible_duplicates": batch.get("possible_duplicates", []),
        },
    })
    validate_ledger(ledger)
    return stats


def record_review(ledger: dict, args: argparse.Namespace) -> None:
    validate_ledger(ledger)
    rec = next((r for r in ledger["records"] if r["record_id"] == args.record_id), None)
    if rec is None:
        reject(f"Unknown stable record ID {args.record_id}")
    if not REVIEWER_RX.fullmatch(args.reviewer):
        reject("Reviewer ID must be a bounded identifier")
    if args.decision == "awaiting_fulltext" and args.stage != "full_text":
        reject("awaiting_fulltext is only valid at the full-text stage")
    if args.decision == "exclude" and not args.reason.strip():
        reject("Exclusion decisions require an exact reason")
    if rec.get("identity_state") != "IDENTIFIED":
        reject("Cannot screen unresolved identity until human adjudication is recorded")
    events = rec["review_events"]
    if len(events) >= MAX_EVENTS:
        reject("Too many review events on one record")
    events.append({
        "stage": args.stage, "reviewer": args.reviewer, "role": args.role,
        "decision": args.decision, "reason": args.reason,
        "source_locator": args.locator,
        "supersedes_event_number": next((i + 1 for i in reversed(range(len(events)))
            if events[i]["stage"] == args.stage and events[i]["reviewer"] == args.reviewer), None),
    })


def resolve_identity(ledger: dict, args: argparse.Namespace) -> dict:
    """Record the human's identity decision without silently merging records."""
    rec = next((x for x in ledger["records"] if x["record_id"] == args.record_id), None)
    if rec is None or rec.get("identity_state") != "PENDING_ADJUDICATION":
        reject("Only an existing pending identity can be adjudicated")
    if not args.decided_by.strip() or not args.reason.strip():
        reject("Identity resolution requires a named adjudicator and a reason")
    if args.decision == "distinct":
        if args.canonical_record_id:
            reject("distinct cannot specify a canonical duplicate ID")
        rec["identity_state"] = "IDENTIFIED"
    else:
        canonical = next((x for x in ledger["records"] if x["record_id"] == args.canonical_record_id), None)
        if canonical is None or canonical is rec or canonical.get("identity_state") != "IDENTIFIED":
            reject("duplicate must reference an existing identified canonical record")
        if rec["review_events"]:
            reject("Cannot suppress a potentially screened record as duplicate; adjudicate its review events separately")
        rec["identity_state"] = "DUPLICATE_REFERENCE"
        rec["canonical_record_id"] = canonical["record_id"]
    rec.setdefault("identity_decision_events", []).append({
        "decision": args.decision, "decided_by": args.decided_by,
        "reason": args.reason, "linked_to": rec.get("canonical_record_id"),
    })
    for flag in ledger["review_required"]:
        if args.record_id in flag.get("record_ids", []) and all(
            x.get("identity_state") != "PENDING_ADJUDICATION"
            for x in ledger["records"] if x["record_id"] in flag.get("record_ids", [])
        ):
            flag["status"] = "RESOLVED_MANUALLY"
    return {"action": "human_identity_resolution", "record_id": rec["record_id"],
            "identity_state": rec["identity_state"]}


def link_report(ledger: dict, args: argparse.Namespace) -> dict:
    """Keep record, report and study IDs separate; require human evidence."""
    rec = next((x for x in ledger["records"] if x["record_id"] == args.record_id), None)
    if rec is None or rec.get("identity_state") != "IDENTIFIED":
        reject("Only a human-confirmed identified record may be linked to a report/study")
    if not (args.report_id and args.study_id and args.decided_by and args.evidence_locator):
        reject("Report/study links require both identifiers, adjudicator and source evidence locator")
    if (rec.get("report_id") not in (None, args.report_id)
            or rec.get("study_id") not in (None, args.study_id)):
        reject("Existing report/study link conflicts: an explicit separate correction is required")
    rec["report_id"] = args.report_id
    rec["study_id"] = args.study_id
    rec.setdefault("mapping_events", []).append({
        "report_id": args.report_id, "study_id": args.study_id,
        "decided_by": args.decided_by, "source_evidence_locator": args.evidence_locator,
    })
    return {"action": "human_report_study_mapping", "record_id": rec["record_id"]}


def summarize(ledger: dict) -> dict:
    validate_ledger(ledger)
    totals = {"records": len(ledger["records"]), "pending_identity": 0,
              "unscreened": 0, "title_abstract_conflicts": 0, "full_text_conflicts": 0,
              "full_text_not_available": 0}
    conflict_ids = []
    for row in ledger["records"]:
        if row.get("identity_state") == "PENDING_ADJUDICATION":
            totals["pending_identity"] += 1
        if not row["review_events"]:
            totals["unscreened"] += 1
        for stage in STAGES:
            latest = {}
            for ev in row["review_events"]:
                if ev["stage"] == stage and ev["role"] == "reviewer":
                    latest[ev["reviewer"]] = ev["decision"]
            if len(set(latest.values())) > 1:
                totals[stage + "_conflicts"] += 1
                conflict_ids.append(row["record_id"])
            if stage == "full_text" and "awaiting_fulltext" in latest.values():
                totals["full_text_not_available"] += 1
    return {"counts": totals, "conflict_record_ids": sorted(set(conflict_ids)),
            "human_identity_flags": sum(1 for x in ledger["review_required"] if x.get("status") != "RESOLVED_MANUALLY"),
            "human_linked_records": sum(1 for x in ledger["records"] if x.get("report_id") is not None)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    imp = sub.add_parser("ingest", help="Propose ingestion of a normalized import batch")
    imp.add_argument("--batch", type=Path, required=True)
    imp.add_argument("--ledger", type=Path)
    imp.add_argument("--expected-ledger-sha256")
    dec = sub.add_parser("decide", help="Propose append-only human screening decision")
    dec.add_argument("--ledger", type=Path, required=True)
    dec.add_argument("--record-id", required=True)
    dec.add_argument("--stage", choices=sorted(STAGES), required=True)
    dec.add_argument("--reviewer", required=True)
    dec.add_argument("--role", choices=["reviewer", "adjudicator"], default="reviewer")
    dec.add_argument("--decision", choices=sorted(DECISIONS), required=True)
    dec.add_argument("--reason", default="")
    dec.add_argument("--locator", default="")
    dec.add_argument("--expected-ledger-sha256")
    resolver = sub.add_parser("resolve-identity", help="Human identity adjudication without silent merging")
    resolver.add_argument("--ledger", type=Path, required=True)
    resolver.add_argument("--record-id", required=True)
    resolver.add_argument("--decision", choices=["distinct", "duplicate"], required=True)
    resolver.add_argument("--canonical-record-id", default="")
    resolver.add_argument("--decided-by", required=True)
    resolver.add_argument("--reason", required=True)
    resolver.add_argument("--expected-ledger-sha256")
    mapper = sub.add_parser("link-report", help="Explicit human record-to-report/study link")
    mapper.add_argument("--ledger", type=Path, required=True)
    mapper.add_argument("--record-id", required=True)
    mapper.add_argument("--report-id", required=True)
    mapper.add_argument("--study-id", required=True)
    mapper.add_argument("--decided-by", required=True)
    mapper.add_argument("--evidence-locator", required=True)
    mapper.add_argument("--expected-ledger-sha256")
    summary = sub.add_parser("summary", help="Read-only cross-batch/dual-review status")
    summary.add_argument("--ledger", type=Path, required=True)
    args = parser.parse_args()
    try:
        previous_sha = None
        if args.command == "ingest" and not args.ledger:
            if args.expected_ledger_sha256:
                reject("Cannot use expected ledger SHA without --ledger")
            ledger = empty_ledger()
        else:
            ledger, previous_sha = read_json(args.ledger)
            validate_ledger(ledger)
            expected = getattr(args, "expected_ledger_sha256", None)
            if expected and previous_sha != expected.lower():
                reject("SOURCE_LEDGER_SHA256_MISMATCH; refusing stale proposal")
        if args.command == "ingest":
            batch, sha = read_json(args.batch)
            details = incorporate(ledger, batch, sha)
        elif args.command == "decide":
            record_review(ledger, args)
            details = {"action": "append_review_event", "record_id": args.record_id}
        elif args.command == "resolve-identity":
            details = resolve_identity(ledger, args)
        elif args.command == "link-report":
            details = link_report(ledger, args)
        else:
            details = summarize(ledger)
        result = {
            "schema_version": 1,
            "disposition": "READ_ONLY_SUMMARY" if args.command == "summary" else "PROPOSAL_ONLY_NOT_PERSISTED",
            "previous_ledger_sha256": previous_sha,
            "details": details,
        }
        if args.command != "summary":
            result["ledger"] = ledger
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"SCREENING_LEDGER_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
