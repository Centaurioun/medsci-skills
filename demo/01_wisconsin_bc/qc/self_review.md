# Pre-Submission Self-Review — DEMO 1 (Wisconsin Breast Cancer)
medsci-skills v3.7.0 · /self-review --fix (max 2 iterations) · 2026-06-07
Manuscript: manuscript/manuscript.md · Type: original / diagnostic-accuracy · Target reporting: STARD 2015

## Scores

| | overall_score | verdict | Major | Minor |
|---|---|---|---|---|
| **Initial (iteration 0)** | 82 | REVISE | 1 | 1 |
| **Final (iteration 1, after --fix)** | 88 | PASS | 0 | 1 |

Verdict thresholds (skill contract): PASS = score ≥ 85 with no fatal issue; otherwise REVISE.
The final state has no fatal issue; the single remaining Minor is a deliberate, unfixable-by-AI
condition (reference count below target because references are intentional [UNVERIFIED]
placeholders in a methods demo). Iteration limit (2) not exhausted — PASS reached after 1 fix pass.

## What the --fix loop did

- **Iteration 0** found one Major (deterministic): `DISK_UNREPORTED` — `predictions.csv`
  (per-sample test-set predicted probabilities) was on disk and in the analysis manifest but
  not mentioned anywhere in the manuscript (`check_artifact_coverage.py`, Phase 2.5f). This is
  `fixable_by_ai: true`.
- **Fix:** added a sentence to Data Availability releasing `predictions.csv` so every accuracy
  estimate, CI, and DeLong comparison is independently recomputable.
- **Iteration 1 re-review:** artifact coverage reconciled (Major resolved); all other
  detectors unchanged. No fatal issue remains → PASS.

## Systematic category check (A–K)

| Cat | Category | Verdict | Note |
|-----|----------|---------|------|
| A | Study design & data integrity | OK | Held-out test set, leakage prevented (train-only standardization), seed fixed. Cohort-arithmetic detector CLEAN. |
| B | Reference standard & ground truth | OK | Histopathology reference standard stated; timing N/A (same archived sample); no human readers (blinding N/A). |
| C | Validation & statistical reporting | OK | **Calibration [CRITICAL]: PRESENT** — Brier score reported for all 3 index tests (LR 0.019, RF 0.029, SVM 0.020). AUC with DeLong CIs + Wilson CIs for proportions + paired DeLong comparison. |
| D | Clinical framing & importance | OK | Scope-coherence detector CLEAN; no surrogate-care-directive, no cross-sectional-prognostic overreach. Applicability explicitly bounded. |
| E | Reproducibility | OK | Code + seed + reproducibility lock; per-sample predictions released (after fix). |
| F | Reporting completeness | MINOR | Reference count below article-type target (deliberate — [UNVERIFIED] placeholders). STARD compliance 60.9% (14/23 applicable) per /check-reporting; the gaps are clinical-cohort descriptors a public benchmark cannot supply. |
| G | Reporting-guideline compliance | OK | /check-reporting (STARD 2015) run; framework-naming audit clean; STARD flow diagram present. |
| H | Circularity | OK | Label (histopathology) is independent of the FNA-derived features; no label-feature overlap. |
| I | Protocol heterogeneity | N/A | Single curated benchmark; no multi-site acquisition. |
| J | Classical style | OK | check_classical_style.py CLEAN (no §, no in-body AI disclosure, em-dash 0, decimals consistent). |
| K | Reviewer-team consistency | N/A | No human reviewers/extraction; computational analysis. |

## Anticipated Major Comments (fix before submission)

None remaining after the fix pass. (Iteration 0 had one: the unreported `predictions.csv`,
now resolved.)

## Anticipated Minor Comments (address proactively)

1. **[F] Reference count below target (deliberate).** 14 cited references vs the 25–45
   article-type target, and all are `[UNVERIFIED]` placeholders. For a real submission, resolve
   via /search-lit (paper mode) → /lit-sync → /verify-refs --strict. Not fixable by AI and not
   fabricated. This is the expected condition of a methods demonstration.

## Readiness verdict

Ready as a **methods/reproducibility demonstration**. NOT ready as a clinical submission, by
design: the references are unverified placeholders and the dataset is a curated single-source
benchmark with non-transportable predictive values. Every reported number traces to a committed
analysis table; all deterministic v3.7.0 detectors are clean except the deliberate reference-count
minor.

## Phase 3c JSON

```json
{
  "overall_score_initial": 82,
  "overall_score_final": 88,
  "verdict_initial": "REVISE",
  "verdict_final": "PASS",
  "fix_iterations_used": 1,
  "fix_iteration_limit": 2,
  "major_initial": 1,
  "minor_initial": 1,
  "major_final": 0,
  "minor_final": 1,
  "fatal_final": 0,
  "resolved": [
    {"id":"M1","detector":"check_artifact_coverage.py","subtype":"DISK_UNREPORTED",
     "was":"predictions.csv on disk/manifest but unreported","fix":"Data Availability mention","fixable_by_ai":true}
  ],
  "remaining": [
    {"id":"m1","category":"F","detector":"check_reference_adequacy.py","subtype":"below_article_type_target",
     "description":"14 cited refs < 25-45 target; all [UNVERIFIED] placeholders (methods demo)","fixable_by_ai":false}
  ],
  "detectors_clean": ["check_classical_style.py","check_cohort_arithmetic.py","check_scope_coherence.py","check_artifact_coverage.py"],
  "note": "Scores reflect a genuine category + deterministic assessment; calibration present (Brier), traceable numbers, paired DeLong test. No target score invented."
}
```
