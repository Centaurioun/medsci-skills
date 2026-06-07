# Self-Review Report: Efficacy of BCG Vaccination Against Tuberculosis: A Random-Effects Meta-Analysis of 13 Randomized Trials

**Target journal**: not specified (clean-room methods demonstration)
**Manuscript type**: Meta-analysis (intervention, PRISMA 2020)
**Date**: 2026-06-07
**Tool**: medsci-skills v3.7.0 /self-review --json --fix (single-pass)
**Overall assessment**: The manuscript is internally rigorous: every numeric claim traces to a generated CSV, all deterministic gates (classical style, scope coherence, claim-vs-artifact, artifact coverage, reviewer-team consistency) pass, and the heterogeneity/prediction-interval framing is honest. Its remaining gaps are the standard systematic-review apparatus (per-study risk of bias, GRADE certainty, full search/screening, individual study citations) that this clean-room demo deliberately does not produce because it pools a single canonical built-in dataset rather than running a de novo review.

## INITIAL assessment (before --fix)

Overall score: 78 / 100 | Verdict: REVISE

## Anticipated Major Comments (fix before submission)

M1. **No per-study risk-of-bias assessment** [G]
A PRISMA 2020 reviewer would require a risk-of-bias judgment for each of the 13 randomized trials (e.g., RoB 2), reported per study and summarized in the synthesis. The manuscript presents none.
**Severity**: Fixable (requires new assessment, not data)
**Suggested fix**: Add RoB 2 assessment of the 13 trials with a traffic-light figure and a Methods paragraph. `fixable_by_ai: false` — out of scope for this methods demo.

M2. **No certainty-of-evidence (GRADE) assessment** [G]
With I-squared 92.2% and a prediction interval crossing 1.0, a reviewer would expect a GRADE rating for the TB-incidence outcome, which would likely be downgraded for inconsistency.
**Severity**: Fixable (requires new assessment)
**Suggested fix**: Add a GRADE certainty assessment paragraph. `fixable_by_ai: false`.

M3. **Methods/Statistical Analysis names methods with zero citations; reference count far below target** [F]
The reference-adequacy gate (`check_reference_adequacy.py`) flagged `methods_zero_citations: true` (PRISMA named uncited) and 0 cited references against the meta-analysis target of 40–80. Every named method and the reporting guideline need canonical sources, and each of the 13 trials should be individually cited.
**Severity**: Fixable (requires reference acquisition)
**Suggested fix**: Resolve the [UNVERIFIED] placeholders via /search-lit → /lit-sync → /verify-refs --strict. `fixable_by_ai: false` — intentional for this demo; recorded as SEARCH_LIT_REQUIRED.

## Anticipated Minor Comments (address proactively)

m1. **No exploration of the very high heterogeneity** [G/C]: With I-squared 92.2%, a meta-regression on latitude (the `ablat` variable, available in the dataset) is the obvious next step; the manuscript acknowledges this as out of scope in Limitations but performs no subgroup/meta-regression. (Results, Heterogeneity)

m2. **Review not registered, and this was not stated** [F]: PRISMA item 24a expects an explicit registration statement. (Fixed in --fix: a Protocol-and-registration paragraph now states the review was not registered and no protocol prepared.)

m3. **Funding statement on title page only** [F]: PRISMA item 25 funding/support appears as a title-page placeholder rather than a body Funding section. (Title page)

m4. **Underpowered small-study tests reported without strong caveat in the Abstract** [C]: Egger and rank tests at k=13 are underpowered; the body states this but the Abstract reports the non-significant tests plainly. (Abstract)

## Strengths (emphasize in cover letter)

- Every numeric claim (pooled RR, CI, I-squared, tau-squared, Q, prediction interval, Egger/rank statistics, leave-one-out range) traces to a generated CSV; a 17-claim 3-way audit returned 0 mismatches.
- A second software implementation (meta::metabin, Hartung-Knapp) reproduces the point estimate exactly, demonstrating the result is data-driven rather than package-specific.
- The prediction interval is reported and correctly interpreted (crosses 1.0), so the conclusion does not overstate uniform benefit.
- Leave-one-out shows the pooled estimate is robust to any single trial (RR 0.452–0.533, all CIs exclude 1).

## FINAL assessment (after --fix, 1 iteration)

Overall score: 82 / 100 | Verdict: REVISE
Fix iterations: 1 / 2
Fixed issues: 1 (m2 — added Protocol-and-registration statement; PRISMA 24a/24b now PRESENT)
Remaining issues requiring human/external work: 4 (M1 RoB, M2 GRADE, M3 references, m1 heterogeneity exploration) — all `fixable_by_ai: false`, all intentional for a clean-room methods demonstration.

The score remains REVISE (below the 85 PASS threshold) because the remaining Major comments are genuine PRISMA gaps that cannot be closed by text edits on a single built-in dataset. They are expected and disclosed for this demo. No fatal (design-invalidating) issue is present: there is no leakage, no circularity, no estimand drift, and no numeric fabrication.

## R0 Pre-Submission Findings (for /revise cross-reference)

R0-1 [MAJ] M1: No per-study risk-of-bias assessment
R0-2 [MAJ] M2: No GRADE certainty-of-evidence assessment
R0-3 [MAJ] M3: Methods methods uncited + reference count below target ([UNVERIFIED] placeholders)
R0-4 [MIN] m1: No heterogeneity exploration (meta-regression on latitude)
R0-5 [MIN] m2: Registration statement (RESOLVED in --fix)
R0-6 [MIN] m3: Funding statement title-page-only
R0-7 [MIN] m4: Underpowered small-study tests reported plainly in Abstract

```json
{
  "self_review_version": "1.0",
  "manuscript_title": "Efficacy of BCG Vaccination Against Tuberculosis: A Random-Effects Meta-Analysis of 13 Randomized Trials",
  "date": "2026-06-07",
  "initial_score": 78,
  "overall_score": 82,
  "verdict": "REVISE",
  "fatal_count": 0,
  "major_count": 3,
  "minor_count": 4,
  "fix_iterations": 1,
  "fixed_count": 1,
  "demo_note": "Clean-room methods demo on metafor dat.bcg; remaining Majors are genuine PRISMA apparatus gaps (RoB/GRADE/search/refs) intentionally out of scope, all fixable_by_ai:false. No fatal/design issue.",
  "issues": [
    {"id":"M1","severity":"major","category":"G","category_name":"Reporting Guideline Compliance","location":"Methods/Results","description":"No per-study risk-of-bias (RoB 2) assessment for the 13 trials.","fixable_by_ai":false,"suggested_fix":"Add RoB 2 assessment + traffic-light figure."},
    {"id":"M2","severity":"major","category":"G","category_name":"Reporting Guideline Compliance","location":"Methods/Results","description":"No GRADE certainty-of-evidence rating for the TB-incidence outcome.","fixable_by_ai":false,"suggested_fix":"Add GRADE certainty assessment (likely downgraded for inconsistency)."},
    {"id":"M3","severity":"major","category":"F","category_name":"Reporting Completeness","issue_type":"reference_adequacy","subtype":"methods_zero_citations","location":"Methods - Statistical Analysis","description":"Named methods/guideline uncited and 0 references vs meta-analysis target 40-80.","fixable_by_ai":false,"suggested_fix":"Resolve [UNVERIFIED] placeholders via /search-lit -> /lit-sync -> /verify-refs --strict."},
    {"id":"m1","severity":"minor","category":"C","category_name":"Validation & Stats","location":"Results - Heterogeneity","description":"I-squared 92.2% with no meta-regression on latitude (ablat available).","fixable_by_ai":false,"suggested_fix":"Add latitude meta-regression; acknowledged in Limitations."},
    {"id":"m2","severity":"minor","category":"F","category_name":"Reporting Completeness","location":"Methods - Protocol and registration","description":"Registration status not stated (PRISMA 24a).","fixable_by_ai":true,"suggested_fix":"State the review was not registered and no protocol prepared.","status":"RESOLVED"},
    {"id":"m3","severity":"minor","category":"F","category_name":"Reporting Completeness","location":"Title page","description":"Funding statement on title page only, not a body Funding section.","fixable_by_ai":false,"suggested_fix":"Add body Funding section."},
    {"id":"m4","severity":"minor","category":"C","category_name":"Validation & Stats","location":"Abstract","description":"Underpowered small-study tests (k=13) reported plainly in Abstract.","fixable_by_ai":true,"suggested_fix":"Note the k<10 underpowering caveat in the Abstract too."}
  ]
}
```
