#!/usr/bin/env python3
"""Compare source-to-slide evidence declarations with readable PPTX slide text.

A bounded, read-only OpenXML inspection aid. It verifies ONLY whether supplied
display snippets occur in native slide XML text. It NEVER verifies that a number
is correct relative to the scientific source, whether an image depicts the
original paper, visual layout, embedded chart data, or clinical conclusions.

Usage:
  python3 audit_slide_evidence.py --manifest slide_evidence.json --pptx talk.pptx

Manifest v1: {"schema_version":1,"elements":[{"slide_id":"S08",
  "element_id":"primary-outcome","source_identity":"verified zotero item/DOI",
  "source_locator":"Table 2","claim_or_visual_type":"NUMERIC_RESULT",
  "display_mode":"NATIVE_TABLE","expected_display_text":"95% CI",
  "source_review_state":"SOURCE_VERIFIED"}]}

No writes, code execution, image OCR, data retrieval or PDF conversion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

MAX_MANIFEST = 3_000_000
MAX_PPTX = 120_000_000
MAX_SLIDES = 300
MAX_ITEMS = 2000
MAX_SLIDE_XML = 3_000_000
SID_RX = re.compile(r"^S0*([1-9][0-9]{0,2})$")
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
PRES_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
DRAW_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
RASTER_MODES = {"SOURCE_IMAGE", "RENDERED_CHART", "REDRAWN_SCHEMATIC"}
NATIVE_MODES = {"NATIVE_TEXT", "NATIVE_TABLE", "VECTOR_EQUATION"}
SOURCE_STATES = {"SOURCE_VERIFIED", "PROVISIONAL", "UNASSESSED", "BLOCKED_SOURCE_ACCESS"}


def duplicate_guard(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def bounded_zip_member(archive, path):
    member = archive.getinfo(path)
    if member.file_size > MAX_SLIDE_XML:
        raise ValueError("PPTX XML member too large: " + path)
    return archive.read(path)


def slide_paths(archive):
    """Resolve presentation order, not zip filename numbering."""
    presentation = ET.fromstring(bounded_zip_member(archive, "ppt/presentation.xml"))
    relationships = ET.fromstring(bounded_zip_member(archive, "ppt/_rels/presentation.xml.rels"))
    ids = {}
    for rel in relationships.findall("{" + PKG_REL_NS + "}Relationship"):
        if rel.get("TargetMode") == "External":
            continue
        ids[rel.get("Id")] = rel.get("Target")
    paths = []
    slide_list = presentation.find("{" + PRES_NS + "}sldIdLst")
    if slide_list is None:
        return paths
    for element in slide_list.findall("{" + PRES_NS + "}sldId"):
        relation = element.get("{" + REL_NS + "}id")
        target = ids.get(relation)
        if not target:
            raise ValueError("PPTX slide relationship missing")
        if target.startswith("/"):
            path = posixpath.normpath(target.lstrip("/"))
        else:
            path = posixpath.normpath(posixpath.join("ppt", target))
        if not path.startswith("ppt/slides/") or not path.endswith(".xml"):
            raise ValueError("Unexpected internal slide relationship")
        paths.append(path)
    if len(paths) > MAX_SLIDES:
        raise ValueError("Too many slides")
    return paths


def slide_text(archive, path):
    root = ET.fromstring(bounded_zip_member(archive, path))
    chunks = [t.text or "" for t in root.iter("{" + DRAW_NS + "}t")]
    return " ".join(" ".join(chunks).split())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--pptx", type=Path, required=True)
    args = parser.parse_args()
    try:
        if not args.manifest.is_file() or args.manifest.stat().st_size > MAX_MANIFEST:
            raise ValueError("Missing or oversized evidence manifest")
        if not args.pptx.is_file() or args.pptx.stat().st_size > MAX_PPTX:
            raise ValueError("Missing or oversized presentation")
        raw = args.manifest.read_bytes()
        manifest = json.loads(raw, object_pairs_hook=duplicate_guard)
        if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
            raise ValueError("Expected schema_version=1 evidence manifest")
        elements = manifest.get("elements")
        if not isinstance(elements, list) or len(elements) > MAX_ITEMS:
            raise ValueError("Expected bounded elements array")
        findings = []
        with zipfile.ZipFile(args.pptx) as archive:
            paths = slide_paths(archive)
            cache = {}
            keys = set()
            for item in elements:
                if not isinstance(item, dict):
                    raise ValueError("Evidence element must be an object")
                slide_id, element_id = item.get("slide_id"), item.get("element_id")
                if not isinstance(slide_id, str) or not isinstance(element_id, str) or not element_id:
                    raise ValueError("Missing slide_id/element_id")
                match = SID_RX.fullmatch(slide_id)
                if not match:
                    raise ValueError("Slide identifiers must follow S01, S02, ...")
                number = int(match.group(1))
                marker = (number, element_id)
                if marker in keys:
                    raise ValueError("Duplicate slide element identity")
                keys.add(marker)
                mode = item.get("display_mode")
                if mode not in NATIVE_MODES | RASTER_MODES:
                    raise ValueError("Unknown display_mode")
                review_state = item.get("source_review_state", "UNASSESSED")
                if review_state not in SOURCE_STATES:
                    raise ValueError("Unknown source_review_state")
                source_identity = item.get("source_identity", "")
                source_locator = item.get("source_locator", "")
                expected = item.get("expected_display_text", "")
                if not all(isinstance(v, str) for v in (source_identity, source_locator, expected)):
                    raise ValueError("Source and expected text must be strings")
                if number > len(paths):
                    state = "SLIDE_NOT_FOUND"
                elif mode in RASTER_MODES:
                    state = "RASTER_OR_IMAGE_CONTENT_NOT_TEXT_VERIFIED"
                elif not expected.strip():
                    state = "EXPECTED_DISPLAY_TEXT_NOT_DECLARED"
                else:
                    if number not in cache:
                        cache[number] = slide_text(archive, paths[number - 1])
                    state = ("NATIVE_TEXT_PRESENT_SOURCE_NOT_RECHECKED"
                             if " ".join(expected.split()) in cache[number]
                             else "NATIVE_TEXT_MISSING_OR_SPLIT")
                findings.append({
                    "slide_id": slide_id, "element_id": element_id,
                    "display_mode": mode, "source_review_state": review_state,
                    "source_locator_present": bool(source_locator.strip()),
                    "source_identity_present": bool(source_identity.strip()),
                    "display_check": state,
                    "scientific_fidelity_verified": False,
                })
        report = {
            "schema_version": 1, "disposition": "READ_ONLY_NO_SCIENTIFIC_VERIFICATION",
            "manifest_sha256": hashlib.sha256(raw).hexdigest(),
            "pptx_sha256": hashlib.sha256(args.pptx.read_bytes()).hexdigest(),
            "slide_count": len(paths),
            "findings": findings,
            "limitations": [
                "Text found in slide XML does not establish numerical or citation correctness",
                "Image, chart data and visual layout were not inspected",
                "The source_review_state field is supplied, not independently certified",
                "Neither a canonical write nor a scientific review was performed",
            ],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, ET.ParseError, zipfile.BadZipFile) as exc:
        print("SLIDE_EVIDENCE_AUDIT_ERROR: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
