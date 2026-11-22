#!/usr/bin/env python3
"""Proposal-only reviewer-issue ledger transformer (stdlib only).

This utility never saves a file or edits a manuscript. It reads an optional
JSON issue ledger and emits a JSON proposal to stdout. Under Academic Research,
only Academic Write Coordinator -> Manuscript Forge may persist accepted output.
A transition labelled APPLIED_CONFIRMED requires an external write receipt;
a CLOSED transition additionally requires a human/source-verified location.

Examples:
  python3 revision_ledger.py init
  python3 revision_ledger.py add --input ledger.json --id R1-1 --round R1 \
      --comment "Clarify the primary outcome" --severity major
  python3 revision_ledger.py set --input ledger.json --id R1-1 \
      --status PATCH_PROPOSED --reason "Draft replacement ready"
  python3 revision_ledger.py report --input ledger.json

This is not a substitute for manuscript comparison, author approval, or a
canonical writer. No tests or runtime validation are implied by the source.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

MAX_INPUT = 2_000_000
MAX_ISSUES = 2500
IDENTIFIER = re.compile(r"^[A-Za-z][A-Za-z0-9._:-]{0,79}$")
STATES = {
    "OPEN": {"TRIAGED", "WITHDRAWN_REASONED"},
    "TRIAGED": {"EVIDENCE_REQUIRED", "AUTHOR_DECISION_REQUIRED", "PATCH_PROPOSED", "WITHDRAWN_REASONED"},
    "EVIDENCE_REQUIRED": {"TRIAGED", "PATCH_PROPOSED", "WITHDRAWN_REASONED"},
    "AUTHOR_DECISION_REQUIRED": {"PATCH_PROPOSED", "WITHDRAWN_REASONED"},
    "PATCH_PROPOSED": {"APPROVED", "AUTHOR_DECISION_REQUIRED", "WITHDRAWN_REASONED"},
    "APPROVED": {"APPLIED_CONFIRMED", "PATCH_PROPOSED"},
    "APPLIED_CONFIRMED": {"CLOSED", "PATCH_PROPOSED"},
    "CLOSED": set(),
    "WITHDRAWN_REASONED": set(),
}
SEVERITIES = {"major", "minor", "editorial", "unclassified"}


def fail(message: str) -> None:
    raise ValueError(message)


def no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            fail(f"Duplicate JSON property: {key}")
        result[key] = value
    return result


def load(path: str) -> tuple[dict, str]:
    candidate = Path(path)
    if not candidate.is_file() or candidate.stat().st_size > MAX_INPUT:
        fail("Ledger is absent, not a regular file, or too large")
    data = candidate.read_bytes()
    ledger = json.loads(data, object_pairs_hook=no_duplicate_keys)
    validate(ledger)
    return ledger, hashlib.sha256(data).hexdigest()


def validate(ledger: object) -> None:
    if not isinstance(ledger, dict) or ledger.get("schema_version") != 1:
        fail("Expected revision-ledger schema_version=1")
    issues = ledger.get("issues")
    if not isinstance(issues, list) or len(issues) > MAX_ISSUES:
        fail("Ledger issues must be a bounded array")
    ids = set()
    for issue in issues:
        if not isinstance(issue, dict) or not isinstance(issue.get("id"), str):
            fail("Each issue must have a string ID")
        iid = issue["id"]
        if not IDENTIFIER.fullmatch(iid) or iid in ids:
            fail(f"Invalid or duplicated issue ID {iid!r}")
        ids.add(iid)
        if issue.get("status") not in STATES:
            fail(f"Invalid status for {iid}")
        if issue.get("severity") not in SEVERITIES:
            fail(f"Invalid severity for {iid}")


def envelope(ledger: dict, source_sha: str | None, changed: bool) -> dict:
    return {
        "schema_version": 1,
        "disposition": "PROPOSAL_ONLY_NOT_PERSISTED",
        "source_sha256": source_sha,
        "changed": changed,
        "ledger": ledger,
    }


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    add = sub.add_parser("add")
    add.add_argument("--input", required=True)
    add.add_argument("--id", required=True)
    add.add_argument("--round", required=True)
    add.add_argument("--reviewer", default="unspecified")
    add.add_argument("--severity", choices=sorted(SEVERITIES), default="unclassified")
    add.add_argument("--comment", required=True)
    add.add_argument("--source-anchor", default="")
    add.add_argument("--proposed-action", default="")
    update = sub.add_parser("set")
    update.add_argument("--input", required=True)
    update.add_argument("--id", required=True)
    update.add_argument("--status", required=True, choices=sorted(STATES))
    update.add_argument("--reason", required=True)
    update.add_argument("--decision-by", default="")
    update.add_argument("--write-receipt", default="")
    update.add_argument("--verified-locator", default="")
    update.add_argument("--evidence", default="")
    report = sub.add_parser("report")
    report.add_argument("--input", required=True)
    return parser


def main() -> int:
    parser = make_parser()
    args = parser.parse_args()
    try:
        if args.command == "init":
            result = envelope({"schema_version": 1, "issues": []}, None, True)
        else:
            ledger, sha = load(args.input)
            if args.command == "report":
                counts = {state: 0 for state in STATES}
                for issue in ledger["issues"]:
                    counts[issue["status"]] += 1
                result = {
                    "disposition": "READ_ONLY_SUMMARY",
                    "source_sha256": sha,
                    "counts": counts,
                    "unresolved_ids": [
                        issue["id"] for issue in ledger["issues"]
                        if issue["status"] not in {"CLOSED", "WITHDRAWN_REASONED"}
                    ],
                }
            elif args.command == "add":
                if not IDENTIFIER.fullmatch(args.id) or not IDENTIFIER.fullmatch(args.round):
                    fail("Invalid issue ID or revision round")
                if any(i["id"] == args.id for i in ledger["issues"]):
                    fail(f"Issue {args.id} already exists")
                if len(ledger["issues"]) >= MAX_ISSUES:
                    fail("Issue limit exceeded")
                if not args.comment.strip():
                    fail("Reviewer comment is required")
                ledger["issues"].append({
                    "id": args.id, "round": args.round, "reviewer": args.reviewer,
                    "severity": args.severity, "comment": args.comment,
                    "source_anchor": args.source_anchor,
                    "proposed_action": args.proposed_action,
                    "status": "OPEN", "evidence": "",
                    "write_receipt": "", "verified_locator": "",
                    "history": [{"status": "OPEN", "reason": "Reviewer comment intake"}],
                })
                result = envelope(ledger, sha, True)
            else:
                issue = next((x for x in ledger["issues"] if x["id"] == args.id), None)
                if issue is None:
                    fail(f"Unknown issue ID {args.id}")
                current, target = issue["status"], args.status
                if target not in STATES[current]:
                    fail(f"Invalid state transition: {current} -> {target}")
                if not args.reason.strip():
                    fail("A transition reason is required")
                if target == "APPROVED" and not args.decision_by.strip():
                    fail("APPROVED requires identified author decision")
                if target == "APPLIED_CONFIRMED" and not args.write_receipt.strip():
                    fail("APPLIED_CONFIRMED requires canonical write receipt")
                if target == "CLOSED" and not (args.verified_locator.strip() or issue.get("verified_locator")):
                    fail("CLOSED requires verified revised-manuscript locator")
                if target == "WITHDRAWN_REASONED" and not args.decision_by.strip():
                    fail("WITHDRAWN_REASONED requires accountable decision")
                issue["status"] = target
                if args.evidence:
                    issue["evidence"] = args.evidence
                if args.write_receipt:
                    issue["write_receipt"] = args.write_receipt
                if args.verified_locator:
                    issue["verified_locator"] = args.verified_locator
                issue.setdefault("history", []).append({
                    "from": current, "status": target, "reason": args.reason,
                    "decision_by": args.decision_by,
                })
                result = envelope(ledger, sha, True)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"REVISION_LEDGER_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
