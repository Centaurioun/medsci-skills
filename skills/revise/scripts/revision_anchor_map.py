#!/usr/bin/env python3
"""Read-only mapping of reviewer issue anchors to a revised plaintext manuscript.

Reads a revision_ledger.py JSON ledger and a Markdown/LaTeX/plaintext manuscript,
searches for unique exact or whitespace-normalized snippets, and reports
candidate current line ranges. Does not rewrite the ledger, migrate issue
status, confirm writer receipts or validate reviewer-scientific adequacy.

If manuscript content is .docx, export a *clean reviewed text rendition*
through the governed document workflow first. This script will not silently
flatten track-changes XML or claim visible Word layout line numbers.

  python3 revision_anchor_map.py --ledger ledger.json \
      --manuscript revision/R2/main_revised.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

MAX_MANUSCRIPT = 15_000_000
MAX_LEDGER = 2_000_000
MAX_ANCHOR = 6000
MAX_MATCHES = 8
ALLOWED_EXT = {".md", ".markdown", ".txt", ".qmd", ".tex"}


def read_text(path: Path, limit: int) -> tuple[str, str]:
    if not path.is_file() or path.stat().st_size > limit:
        raise ValueError(f"Missing or oversized source: {path}")
    content = path.read_bytes()
    return content.decode("utf-8-sig"), hashlib.sha256(content).hexdigest()


def span_to_lines(text: str, start: int, end: int) -> dict:
    startline = text.count("\n", 0, start) + 1
    endline = text.count("\n", 0, max(start, end - 1)) + 1
    return {"start_line": startline, "end_line": endline,
            "location": f"L{startline}-L{endline}"}


def compact_with_map(text: str) -> tuple[str, list[int]]:
    chars, offsets = [], []
    was_space = False
    for pos, ch in enumerate(text):
        if ch.isspace():
            if not was_space:
                chars.append(" ")
                offsets.append(pos)
            was_space = True
        else:
            chars.append(ch)
            offsets.append(pos)
            was_space = False
    return "".join(chars), offsets


def locate(source: str, anchor: str) -> dict:
    if not isinstance(anchor, str) or not anchor.strip():
        return {"state": "NO_SOURCE_ANCHOR", "candidates": []}
    if len(anchor) > MAX_ANCHOR:
        return {"state": "ANCHOR_TOO_LONG", "candidates": []}
    matches = []
    start = 0
    while len(matches) <= MAX_MATCHES:
        pos = source.find(anchor, start)
        if pos < 0:
            break
        matches.append(span_to_lines(source, pos, pos + len(anchor)))
        start = pos + 1
    if len(matches) == 1:
        return {"state": "UNIQUE_EXACT_ANCHOR_CANDIDATE",
                "candidates": matches, "requires_human_confirmation": True}
    if len(matches) > 1:
        return {"state": "AMBIGUOUS_EXACT_ANCHOR",
                "candidates": matches[:MAX_MATCHES], "requires_human_confirmation": True}
    compact, offsets = compact_with_map(source)
    query = " ".join(anchor.split())
    matches = []
    start = 0
    while len(matches) <= MAX_MATCHES:
        pos = compact.find(query, start)
        if pos < 0:
            break
        original_start, original_end = offsets[pos], offsets[pos + len(query) - 1] + 1
        matches.append(span_to_lines(source, original_start, original_end))
        start = pos + 1
    if len(matches) == 1:
        return {"state": "UNIQUE_WHITESPACE_NORMALIZED_CANDIDATE",
                "candidates": matches, "requires_human_confirmation": True}
    if matches:
        return {"state": "AMBIGUOUS_WHITESPACE_ANCHOR",
                "candidates": matches[:MAX_MATCHES], "requires_human_confirmation": True}
    return {"state": "ANCHOR_NOT_FOUND", "candidates": [],
            "requires_human_confirmation": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", required=True, type=Path)
    parser.add_argument("--manuscript", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.manuscript.suffix.lower() not in ALLOWED_EXT:
            raise ValueError("Requires a .md/.qmd/.tex/.txt plaintext manuscript; no implicit DOCX flattening")
        raw_ledger, ledger_sha = read_text(args.ledger, MAX_LEDGER)
        manuscript, ms_sha = read_text(args.manuscript, MAX_MANUSCRIPT)
        ledger = json.loads(raw_ledger)
        if not isinstance(ledger, dict) or ledger.get("schema_version") != 1 or not isinstance(ledger.get("issues"), list):
            raise ValueError("Expected reviewer revision ledger with schema_version=1 and issues")
        results = []
        for issue in ledger["issues"][:2500]:
            if not isinstance(issue, dict):
                raise ValueError("Malformed issue record")
            result = locate(manuscript, issue.get("source_anchor", ""))
            results.append({"id": issue.get("id"), "previous_verified_locator": issue.get("verified_locator"),
                            **result})
        output = {
            "schema_version": 1, "disposition": "READ_ONLY_CANDIDATES_NOT_APPLIED",
            "ledger_sha256": ledger_sha, "manuscript_sha256": ms_sha,
            "line_numbers": "current_plaintext_file_only_not_word_page_lines",
            "results": results,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"REVISION_ANCHOR_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
