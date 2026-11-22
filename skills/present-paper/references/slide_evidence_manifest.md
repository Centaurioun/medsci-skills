# Source-to-Slide Evidence Manifest — Optional Academic Presentation Contract

**Owner:** `present-paper`; accompanying scientific figure owner: `make-figures`.

This is an original, lightweight **source-fidelity** artifact for a clinical or research talk. It does not replace the existing speaker-notes engine, template architecture, Q&A, figure creation pipeline or the authorised document writer.

## When to create it

Use when the deck includes numerical primary findings, diagnostic performance, patient groups, statistical comparisons, clinical images, citations, reused tables or multiple source articles. A decorative keynote without scholarly claims need not carry this manifest.

## One row per material slide assertion, chart, table or sourced image

| Field | Required meaning |
|---|---|
| `slide_id` / `element_id` | Stable slide+element identifiers |
| `claim_or_visual_type` | `ASSERTION`, `NUMERIC_RESULT`, `TABLE`, `CHART`, `SOURCE_FIGURE`, `REDRAWN_SCHEMATIC` |
| `source_identity` | Zotero itemKey/attachmentKey where verified, or bounded DOI/PMID/authoritative user-supplied file |
| `source_locator` | Figure, page, table, supplementary item, or precise provided data cell |
| `retrieval_depth` | Exact evidence depth and source-access limit; never present an abstract snippet as full-text inspection |
| `reported_value` / `unit` | Exact numerical figure, denominator, units and comparison group if relevant |
| `uncertainty` | CI/SD/IQR/p-value or explicit `NOT_REPORTED` |
| `display_mode` | `NATIVE_TEXT`, `NATIVE_TABLE`, `VECTOR_EQUATION`, `SOURCE_IMAGE`, `RENDERED_CHART` |
| `editability` | `EDITABLE`, `NOT_EDITABLE`, `PARTIALLY_EDITABLE`, with reason |
| `review_state` | `SOURCE_VERIFIED`, `PROVISIONAL`, `UNASSESSED`, `BLOCKED_SOURCE_ACCESS` |
| `caption_attribution` | Source citation and whether `ORIGINAL`/`ADAPTED`/`REDRAWN` |
| `limitations` | Any uncertainty or visual degradation that must be shown to presenter |

## Principles

1. **Academic fidelity is more important than visually appealing images.** Do not render a clinical table, significance test, numerical label or mathematical equation as generated imagery when it can be preserved as verified editable text/table/vector.
2. **Do not promise universal editability.** Current `present-paper` can export editable slide text and uses raster plots/diagrams in some templates. Label an embedded plot `RENDERED_CHART` and `NOT_EDITABLE` unless a true native editable chart is actually produced.
3. **Original paper figures are evidence, not decorative material.** Keep the identifier, original legend/caption relationship, copyright/permission context and precise locator. A crop must not alter interpretation or hide important axes.
4. **Never fabricate missing data or annotate a figure by inference.** Flag `UNASSESSED` and keep the value out of the public claim until sourced.
5. **Preserve source fidelity in speaker notes.** Any statistic spoken aloud must align with the value shown and the source manifest.
6. **For educational conceptual diagrams**, an original redrawing is allowed when clearly labelled and does not imitate a measured patient result. Do not confuse a schematic with a real diagnostic image.
7. **No new writer.** This manifest is a proposed scientific-content contract; actual canonical deck/project persistence follows the host's authorised write path.

## Example (synthetic; no real study evidence claimed)

```json
{
  "slide_id": "S08",
  "element_id": "primary-outcome-ci",
  "claim_or_visual_type": "NUMERIC_RESULT",
  "source_identity": "ZOTERO_ITEM_KEY_IF_VERIFIED",
  "source_locator": "Table 2",
  "retrieval_depth": "full_text_inspected",
  "reported_value": "SOURCE_REQUIRED",
  "unit": "NOT_REPORTED",
  "uncertainty": "NOT_REPORTED",
  "display_mode": "NATIVE_TABLE",
  "editability": "EDITABLE",
  "review_state": "UNASSESSED",
  "caption_attribution": "SOURCE_PENDING",
  "limitations": "Do not populate synthetic numbers; consult exact source"
}
```

## Related prior art (not imported)

Academic PPTX Skill's action headlines and semantic slide types, and the `scholar-slides` fidelity-first source→slide philosophy motivated this optional contract. It is compatible with current MedSci `present-paper` and `make-figures` without importing new agents, image renderers or dependencies.
