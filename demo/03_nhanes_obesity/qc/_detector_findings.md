# v3.7.0 Detector Findings — DEMO 3 (NHANES obesity<->diabetes)
Captured: 2026-06-07 (literal stdout from medsci-skills/skills/self-review/scripts)
Manuscript: manuscript/manuscript.md (FINAL, post-fix)

## 1. check_classical_style.py
```
=========================================
 Classical-Style Body Lint (§J)
=========================================
| Check | Severity | Detail |
|---|---|---|
| (none) | — | classical-style body conventions satisfied |

OK: classical-style body conventions satisfied.
```

## 2. check_cohort_arithmetic.py (STROBE exclusion cascade)
```
=========================================
 Cohort Arithmetic (Phase 2.5 / 2.5b)
=========================================
| Check | Severity | Detail |
|---|---|---|
| (none) | — | no cohort-arithmetic discrepancy detected |

OK: no cohort-arithmetic discrepancy detected.
```

## 3. check_scope_coherence.py
```
=========================================
 Scope Coherence (§D)
=========================================
| Check | Severity | Detail |
|---|---|---|
| (none) | — | conclusion scope matches the design/endpoint |

OK: conclusion scope matches the design/endpoint.
```

## 4. check_reference_adequacy.py
```
==============================================
 Reference Adequacy Gate (count + named methods)
==============================================
 Article type   : original_research -> original_research
 Cited refs     : 0  (target 25-45)
 Distribution   : Intro 0 / Methods 0 / Results 0 / Discussion 0
 Methods 0-cite : True
 Uncited methods: STROBE
 ✗ [major] methods_zero_citations: The Methods/Statistical Analysis section contains no citations; every named method, score, guideline, and diagnostic criterion needs a canonical source (found uncited: STROBE).
 ✗ [major] below_article_type_target: Cited references (0) are below the original_research target (25-45).

 Verdict: BELOW_TARGET  |  2 major, 0 minor  |  adequacy_safe=False
```

## 5. check_confounding_completeness.py (Phase 2.5e / O1)
```
=========================================
 Confounding Completeness (Phase 2.5e / O1)
=========================================
adjustment set: age, sex, race
| Covariate | Imbalance p | SMD | In adjustment set? | Verdict |
|---|---|---|---|---|
| age..mean..SD.. | 0.000999 | — | yes | ✓ |
| BMXBMI..mean..SD.. | 0.000999 | — | NO | ✗ Major |
| obesity_f.... | 0.000999 | — | NO | ✗ Major |

MAJOR candidate: 2 imbalanced covariate(s) absent from the adjustment set.
Fix: Report an extended-adjustment sensitivity model adding the unadjusted imbalanced covariates; keep the original model primary only if the extended model agrees.
```

## Interpretation

| Detector | Result | Action |
|---|---|---|
| check_classical_style | CLEAN (0) | No § symbols, no in-body AI disclosure, heading style OK |
| check_cohort_arithmetic | CLEAN (0) | Exclusion cascade 9254 = 5010 + 3685 + 394 + 165 reconciles |
| check_scope_coherence | CLEAN (0) after fix | INITIAL fired CROSS_SECTIONAL_PROGNOSTIC ('predicts incident' then 'longitudinal follow'); reworded conclusion region to association-only vocabulary -> passes |
| check_reference_adequacy | 2 Major (EXPECTED) | References intentionally [UNVERIFIED] for the methods demo; 0 cited -> methods_zero_citations + below_target. Not a content defect; would resolve via /search-lit + /verify-refs in production |
| check_confounding_completeness | 2 Major (FALSE POSITIVE by design) | Flags BMXBMI + obesity as imbalanced & unadjusted. But BMI/obesity IS the exposure; the O1 check assumes an exposure-stratified Table 1, while this Table 1 is stratified by the OUTCOME (diabetes). Exposure differing across outcome strata is the finding, not a confounding gap. age (a real confounder) is correctly in the adjustment set |
