# Self-Review — DEMO 3 (NHANES obesity<->diabetes), medsci-skills v3.7.0
Mode: --fix (deterministic detector backbone), max 2 iterations
Manuscript: manuscript/manuscript.md
Date: 2026-06-07

## INITIAL (iteration 0)

Deterministic detectors run at intake:

| Category | Detector | Finding | Severity |
|---|---|---|---|
| A. Design & Data Integrity | check_cohort_arithmetic | clean (cascade reconciles) | — |
| C. Statistics & Numbers | (manual) primary aOR + all covariate ORs carry 95% CI | clean | — |
| D. Scope coherence | check_scope_coherence | CROSS_SECTIONAL_PROGNOSTIC ('predicts incident') | MAJOR |
| Classical style | check_classical_style | clean | — |
| Confounding (O1) | check_confounding_completeness | BMXBMI/obesity flagged (false positive: exposure vs outcome-stratified T1) | MAJOR (dismissed) |
| Reference adequacy | check_reference_adequacy | 0 cited refs (demo: [UNVERIFIED]) | MAJOR (expected) |

INITIAL verdict: REVISE — 1 genuine MAJOR (scope coherence) is fixable_by_ai.

### Fixes applied (iteration 1)
- D / scope coherence: reworded Abstract Conclusion, Discussion Limitations, and Conclusion
  to remove prognostic/surveillance vocabulary ('predicts incident', 'rescreening',
  'surveillance interval', 'longitudinal follow') while preserving the association-only meaning.
  The manuscript now states the cross-sectional association without any temporal/causal/predictive claim.

## FINAL (iteration 1, re-review)

| Category | Detector | Finding | Severity |
|---|---|---|---|
| A. Design & Data Integrity | check_cohort_arithmetic | clean | — |
| D. Scope coherence | check_scope_coherence | clean (exit 0) | — |
| Classical style | check_classical_style | clean | — |
| C. Statistics | all primary/covariate estimates have 95% CI; exact p-values | clean | — |
| Confounding (O1) | check_confounding_completeness | dismissed (detector assumes exposure-stratified T1; ours is outcome-stratified; age confounder is adjusted) | not_fixable / N/A |
| Reference adequacy | check_reference_adequacy | 2 Major — EXPECTED for methods demo ([UNVERIFIED] refs); not fixable in a demo | not_fixable (by design) |

### Verdict: ACCEPT-WITH-NOTES

- Genuine content issues: 0 remaining (the one real MAJOR — scope coherence — was fixed in iteration 1).
- Remaining MAJOR flags are not content defects:
  - reference_adequacy (2): references are intentionally [UNVERIFIED] placeholders for this
    methods demonstration; in production they resolve via /search-lit + /verify-refs.
  - confounding_completeness (2): false positive arising from an outcome-stratified Table 1
    fed to an exposure-stratified O1 check; the exposure (obesity) is correctly the modeled term.
- Minor (would address in production, left as-is to keep STROBE compliance a genuine measure):
  STROBE item 10 (study-size justification) MISSING; items 9/12c/14b/16a PARTIAL
  (bias subsection, complete-case label, per-variable missingness, crude OR).

n_major (genuine, unresolved) = 0
n_major (expected/dismissed) = 4 (2 ref-adequacy demo + 2 confounding false-positive)
n_minor (genuine, deferred) = 5 (STROBE 10 + 9/12c/14b/16a)
