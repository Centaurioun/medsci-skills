# Skill gap register

A living, scored ledger of **skill weaknesses the loop targets**. This supersedes the old
fixed "priority order" — each iteration consults this register (PLAYBOOK Step 0), works the
highest-scoring **open** gap, and feeds newly discovered gaps back in (Step B). The point is to
find the weaknesses across the *whole* suite — including ones we did not know about — by
reading strong papers and noticing what our skills do not yet cover or check.

## Scoring

`score = impact × frequency × deficit` (each 1–5; higher = work it sooner).

- **impact** — how much a real manuscript benefits when this gap is filled.
- **frequency** — how often the relevant study type / task actually shows up.
- **deficit** — how missing it is now (5 = absent, 1 = minor polish).

**status:** `open` · `in-progress` · `shipped (#PR)` · `saturated` (lane's gaps are filled —
stop adding marginal items there).

## How gaps enter the register

1. **Paper-driven (Step B).** While analyzing a strong paper/review, note not only what *it*
   does well but **what a strong paper in this area needs that our skills do not cover or
   check** — a missing exemplar, table-type, figure anatomy, probe, checklist item, or
   template. Add it as a row.
2. **Cross-skill audit (every ~4 iterations).** Pick one skill the loop has not touched
   recently and scan its `references/` against the common cases in its domain (what table
   types / figure types / probes / templates a practitioner expects). Record what is absent.
   Rotate the audited skill so coverage spreads beyond the obvious (figures, review skills).
3. **User-flagged.** Areas the user calls out (e.g., figures).

## Open gaps (work highest score first)

| id | skill | gap | impact | freq | deficit | score | status |
|----|-------|-----|:------:|:----:|:-------:|:-----:|--------|
| G1 | make-figures | `exemplar_plots/km_curve.md` — KM survival-curve anatomy (number-at-risk, censoring marks, CI band, no extrapolation past follow-up); pairs the survival table-type | 4 | 5 | 5 | 100 | shipped (this PR) |
| G2 | analyze-stats | `table-types/agreement.md` — reliability table (ICC / weighted κ / Bland–Altman LoA) — supported by `agreement_analysis.py` but no table-type template | 4 | 4 | 5 | 80 | shipped (this PR) |
| G3 | make-figures | `exemplar_plots/roc_pr.md` — ROC / precision-recall anatomy (CI band, operating point, AUPRC under imbalance) | 4 | 5 | 5 | 100 | shipped (this PR) |
| G4 | make-figures | `exemplar_plots/calibration_plot.md` — calibration anatomy (bins/loess, slope/intercept, distribution rug) | 4 | 4 | 5 | 80 | shipped (this PR) |
| G5 | peer-review + self-review | `domain-probes/` RCT / intervention-trial probe (CONSORT: randomisation, allocation concealment, blinding, ITT, selective-outcome) — no trial probe despite trials being common | 5 | 4 | 5 | 100 | shipped (this PR) |
| G6 | make-figures | `exemplar_plots/bland_altman.md` + `confusion_matrix.md` | 3 | 3 | 5 | 45 | open |
| G7 | write-paper | `exemplar_introduction.md` + `exemplar_abstract.md` (the two sections without exemplars; section_guides exist) | 3 | 5 | 3 | 45 | intro shipped; abstract open |
| G8 | check-reporting | `checklists/METRICS.md` — radiomics methodological-quality tool (named in the critical-item floor but no checklist) | 3 | 3 | 4 | 36 | open |
| G9 | calc-sample-size | `references/justification_examples.md` — reviewer-safe sample-size justification prose per design (found via cross-skill audit; SKILL.md promised "IRB-ready justification text" but no exemplar library) | 4 | 4 | 4 | 64 | shipped (this PR) |
| G10 | present-paper | `scripts/inject_speaker_notes.py` run-level markdown parser — general speaker notes rendered `**bold**` literally (the failure mode pptx-speaker-notes.md warns against); the parser existed only in inject_pronunciation_notes.py. Found while triaging the unmerged `present-paper-md-notes-glossary` branch (whose verify_refs/academic-aio parts were already superseded by main) | 3 | 4 | 4 | 48 | shipped (rescue PR) |
| G11 | manage-refs | `scripts/render_pandoc.sh` had no pre-render reference audit — a direct render call could ship fabricated/mismatched citations (the master pre_submission_gate audits, but direct calls bypass it). Found while triaging the unmerged present-paper-md-notes-glossary branch | 4 | 3 | 4 | 48 | shipped (cleanup PR) |
| G12 | make-figures | `exemplar_plots/decision_curve.md` — net-benefit decision-curve (DCA) anatomy (treat-all/treat-none reference lines, threshold-probability range, model curve, operating-point); the clinical-utility counterpart to ROC/calibration. Cross-cutting: unblocks prognostic + TRIPOD+AI + clinical-impact. Found while reverse-engineering adjacent clinical-research areas (prognostic external validation) | 4 | 4 | 5 | 80 | in-progress (this PR) |
| G13 | check-reporting | `checklists/TRIPOD_LLM.md` — TRIPOD-LLM reporting guideline for studies using large language models (base TRIPOD + LLM extension). Step 4e already routes the name but no checklist is vendored — a `MISSING_CHECKLIST_CONTRACT_VIOLATION` waiting to happen. Found while reverse-engineering the LLM-study reporting area | 5 | 3 | 5 | 75 | in-progress (this PR) |
| G14 | analyze-stats | `table-types/incremental_value.md` — "beyond baseline" added-value table standard (ΔAUC + DeLong CI, NRI, IDI, net-benefit); no table-type covers incremental-value claims, which AI-vs-baseline and prognostic papers routinely make. Pre-builds the clinical-impact NRI/IDI need | 4 | 3 | 5 | 60 | in-progress (this PR) |
| G15 | peer-review + self-review | `domain-probes/survival_prognostic.md` TRIPOD+AI subsection — model/dataset-flow (train/tune/internal-test/external-test), subgroup/fairness performance, calibration paired with decision-curve. The survival/prognostic probe (S1–S8) checks survival design but not the AI-prediction-model reporting flow that TRIPOD+AI governs | 4 | 4 | 4 | 64 | in-progress (this PR) |

## Lane status

- **make-figures** (figure exemplars): forest shipped (#130); km/roc/calibration/bland-altman/
  confusion/visual-abstract open — **the suite's weakest area, keep returning here.**
- **write-paper exemplars**: methods/results/discussion trio shipped; intro/abstract open.
- **review domain-probes**: 6 modules; RCT/trial + survey/qualitative/economic still open.

## Shipped (audit trail)

| id | shipped | skill | note |
|----|---------|-------|------|
| — | #128–#130 | peer-review/self-review/write-paper/analyze-stats/make-figures/check-reporting | optimistic-validation seam, exemplar trio, survival table, forest exemplar, critical-item floor, selective-outcome exemplar |
