# Source-Grounded Single-Paper Deep Reading — Optional MedSci Profile

**Purpose:** Create a reusable, evidence-bound reading note for exactly one selected paper, without creating a second library or canonical file writer. This is an analysis/output profile, not a Zotero synchronization routine, and it does not imply the paper was independently reproduced.

## Trigger and scope

Use this profile when the user asks for **deep reading / critical appraisal / detailed paper notes** from one accessible article, Zotero item, authorized PDF or sufficiently supplied full text. Do not substitute the `review-paper` skill (which drafts a review article) for single-paper reading.

The current `lit-sync` bibliography/Obsidian notes remain available for separately authorized standalone workflows. **When composed under Academic Research, do not invoke `zotero_add_by_doi`, Zotero library writes, Obsidian vault writes, or other direct persistence as a side effect of this profile.** Zotero Local identity and bounded passages are read-only evidence; accepted canonical output is persisted only via Academic Write Coordinator → Manuscript Forge Production upon a separately authorized request.

## Inputs and source state

- `paper_identity`: DOI / PMID / title / year, resolving conflicts rather than guessing.
- `zotero_item_key`, `zotero_attachment_key`, or an explicit non-Zotero source identity.
- `retrieval_depth`: metadata_only | abstract | bounded_passages | full_text_inspected.
- `source_locators`: page/section/table/figure identifiers, with direct supporting quotation or faithful paraphrase and provenance.
- `reading_language`: `tr` or `en`, following the user's preference (additional languages may be requested, never inferred).
- Optional `research_question`, `research_direction`, `note_version`, pre-existing note to compare.
- Optional extracted figure/table image **only** when an authorized source image and accurate locator are available; otherwise use text-only placeholders without invented visuals.

A title/abstract search result, a bibliography entry, or a ZotSeek candidate alone cannot qualify as a complete deep read. Show **LIMITED_TO_ABSTRACT** or **SOURCE_INSUFFICIENT** instead of claiming full-text inspection.

## Paper-type routing

- Clinical intervention: design, comparator, allocation, interventions, outcomes, effect estimates, confidence intervals, limitations.
- Observational/epidemiology: sampling, exposure and outcome definitions, confounding, clustering, missingness, estimand and causal-claim ceiling.
- Diagnostic accuracy / imaging: patient flow, index test/reference/target condition, independent unit, accuracy estimates by threshold; do not infer QUADAS-3 verdicts without the official tool.
- Systematic/scoping review: question, search/screening, study vs report/record distinctions, evidence synthesis, risk-of-bias/certainty limitations.
- Psychometric/PRO: construct, sample, language/cultural validity, scoring, reliability/measurement properties, change interpretation; do not turn a score change into a validated individual clinical change without evidence.
- Method/theory: formal assumptions, implementation steps, mathematical claims, observed performance and stated limitations.

## Recommended note sections (TR/EN equivalent labels)

1. **Bibliographic identity / Bibliyografik kimlik** — item IDs, year, verified source path and depth.
2. **Question and contribution / Araştırma sorusu ve katkı** — what this article actually tests.
3. **Design and methods / Tasarım ve yöntemler** — setting, sample, variables, contrasts, estimands, analytical unit.
4. **Results and quantitative evidence / Bulgular ve nicel kanıt** — grounded values, denominator, CI, page/table locator.
5. **Figures and tables / Şekil ve tablolar** — one record per figure/table: source label, original caption/location, what it actually supports, unresolved image access.
6. **Critical appraisal / Eleştirel değerlendirme** — limitations, alternative explanations, confounding/bias signals; distinguish observation from reviewer inference.
7. **Connection to research direction / Araştırma ile bağlantısı** — applicability and differences, without inventing transferability.
8. **Open questions / Açık sorular** — missing evidence, contradictory statements and next study questions.
9. **Citation/evidence provenance / Atıf ve kanıt izlenebilirliği** — claim IDs and qualifying bounded evidence, not a fabricated reference list.

## Evidence and status contract

Each material claim should have a source relation tag (`DIRECTLY_REPORTED`, `AUTHOR_INFERENCE`, `READER_INTERPRETATION`, `UNASSESSED`) and locator when available. Notes must not elevate a claim based only on abstract-level material. Missing exact page or figure access should be labelled; no image, number, DOI or quote is invented.

Stages: `SOURCE_IDENTIFIED` → `SOURCE_DEPTH_ASSESSED` → `NOTE_DRAFT_READY` → `CLAIM_GROUNDING_PARTIAL|CLAIM_GROUNDING_COMPLETE` → `PROPOSAL_RETURNED` → `AUTHORIZED_WRITE_PENDING` (optional, external). Only the **actual AWC/Forge receipt** may establish persisted state. Naturalization may improve fluency but cannot change the source's meaning, missingness, or certainty.

## Optional proposal formatter

The local `scripts/render_deep_reading_note.py` formats researcher-curated schema_version=1 JSON into TR/EN Markdown in a stdout JSON proposal. Its digest binds the output to those input bytes, **not** to the authoritative PDF or a Zotero verification receipt. Source checks, scientific interpretation and figure/table evidence must be established separately before the formatter runs. No file, vault or Zotero write is made by this helper. It is useful even when only bounded passages are available, as long as the evidence-depth limitation remains explicit.

## External inspiration, not imported code

This profile independently adapts the *requirements* identified in DeepPaperNote (source-manifest, figure-plan, note-proof) and DailyPaper paper-reader, not their Obsidian database, scripts, language limitation (`en`/`zh-CN`) or persistence route. It is a locally authored profile: `tr`/`en` are first-class outputs.
