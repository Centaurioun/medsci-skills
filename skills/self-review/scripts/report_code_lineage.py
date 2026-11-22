#!/usr/bin/env python3
"""Proposal-only paper -> analysis code/output lineage inventory.

Input is a reviewer-authored manifest with claims and paths. The tool reads
only filenames and SHA-256 for files *inside* --project-root; it never runs
analysis code, reads datasets into output, exports patient records, validates
statistical results, modifies files or claims the paper is reproduced.

Emits JSON to stdout for MedSci review and optional governed persistence.
No canonical manuscript or Zotero file is written.

Usage:
    python3 report_code_lineage.py --project-root . --manifest qc/lineage_input.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

MAX_MANIFEST = 1_000_000
MAX_CLAIMS = 500
MAX_FILES = 25
MAX_HASH_FILE = 200_000_000
VALID_ID = re.compile(r"^[A-Za-z][A-Za-z0-9._:-]{0,95}$")


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON field {key}")
        result[key] = value
    return result


def source_ref(project_root: Path, value: str) -> dict:
    if not isinstance(value, str) or not value.strip():
        return {"path": None, "status": "UNSPECIFIED"}
    candidate = (project_root / value).resolve()
    if not candidate.is_relative_to(project_root):
        return {"path": value, "status": "OUTSIDE_PROJECT_REJECTED"}
    if not candidate.is_file():
        return {"path": value, "status": "NOT_FOUND"}
    try:
        size = candidate.stat().st_size
        if size > MAX_HASH_FILE:
            return {"path": value, "status": "TOO_LARGE_FOR_HASH", "bytes": size}
        digest = hashlib.sha256()
        with candidate.open("rb") as inp:
            for block in iter(lambda: inp.read(64 * 1024), b""):
                digest.update(block)
        return {
            "path": value, "status": "FILE_PRESENT_NOT_EXECUTED",
            "sha256": digest.hexdigest(), "bytes": size,
        }
    except OSError as exc:
        return {"path": value, "status": "NOT_READABLE", "error_type": type(exc).__name__}


def list_of_paths(item: dict, name: str) -> list[str]:
    value = item.get(name, [])
    if not isinstance(value, list) or len(value) > MAX_FILES or any(not isinstance(x, str) for x in value):
        raise ValueError(f"{name} must contain 0-{MAX_FILES} paths")
    return value


def prepare(manifest: dict, project_root: Path) -> dict:
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise ValueError("Expected manifest schema_version=1")
    claims = manifest.get("claims")
    if not isinstance(claims, list) or len(claims) > MAX_CLAIMS:
        raise ValueError("Expected bounded claims array")
    seen = set()
    findings = []
    for raw in claims:
        if not isinstance(raw, dict):
            raise ValueError("Every claim must be an object")
        cid = raw.get("claim_id")
        if not isinstance(cid, str) or not VALID_ID.fullmatch(cid) or cid in seen:
            raise ValueError(f"Missing, duplicate or malformed claim_id {cid!r}")
        seen.add(cid)
        scripts = [source_ref(project_root, x) for x in list_of_paths(raw, "scripts")]
        inputs = [source_ref(project_root, x) for x in list_of_paths(raw, "input_files")]
        outputs = [source_ref(project_root, x) for x in list_of_paths(raw, "output_files")]
        if not raw.get("manuscript_locator"):
            verdict = "UNMAPPED_MANUSCRIPT_LOCATION"
        elif not scripts or not outputs:
            verdict = "INCOMPLETE_LINEAGE"
        elif any(x["status"] not in {"FILE_PRESENT_NOT_EXECUTED"} for x in scripts + outputs):
            verdict = "MISSING_OR_UNREADABLE_ARTIFACT"
        else:
            verdict = "FILES_PRESENT_RESULT_NOT_VERIFIED"
        findings.append({
            "claim_id": cid,
            "manuscript_locator": raw.get("manuscript_locator"),
            "claim_text": raw.get("claim_text"),
            "scripts": scripts, "input_files": inputs,
            "output_files": outputs, "mapping_state": verdict,
            "does_not_establish": [
                "Analysis execution or successful reproduction",
                "Numerical agreement between outputs and manuscript",
                "Scientific validity of the claimed result",
            ],
        })
    return {
        "schema_version": 1,
        "disposition": "READ_ONLY_PROVENANCE_REPORT",
        "overall_state": "NOT_VALIDATED",
        "files_checked": sum(len(x[k]) for x in findings for k in ("scripts", "input_files", "output_files")),
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--project-root", required=True, type=Path)
    args = parser.parse_args()
    try:
        root = args.project_root.resolve()
        if not root.is_dir() or not args.manifest.is_file() or args.manifest.stat().st_size > MAX_MANIFEST:
            raise ValueError("Missing project root or missing/oversized manifest")
        payload = json.loads(args.manifest.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
        report = prepare(payload, root)
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (ValueError, OSError, UnicodeError) as exc:
        print(f"PAPER_CODE_LINEAGE_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
