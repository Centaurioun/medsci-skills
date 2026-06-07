# v3.7.0 Deterministic Detector Findings — DEMO 1 (literal captures)
medsci-skills v3.7.0 · self-review Phase 2.5 detectors · 2026-06-07
Run against: manuscript/manuscript.md (+ analysis/ for coverage)

These are the verbatim stdout of each deterministic, stdlib-only detector.

---

## ITERATION 0 (pre-fix)

### DETECTOR: check_classical_style.py  (§J classical-style body lint)
```
=========================================
 Classical-Style Body Lint (§J)
=========================================
| Check | Severity | Detail |
|---|---|---|
| (none) | — | classical-style body conventions satisfied |

OK: classical-style body conventions satisfied.
```
EXIT=0 · 0 major, 0 minor · CLEAN

### DETECTOR: check_cohort_arithmetic.py  (Phase 2.5 / 2.5b)
```
=========================================
 Cohort Arithmetic (Phase 2.5 / 2.5b)
=========================================
| Check | Severity | Detail |
|---|---|---|
| (none) | — | no cohort-arithmetic discrepancy detected |

OK: no cohort-arithmetic discrepancy detected.
```
EXIT=0 · 0 major, 0 minor · CLEAN
(Note: applicable because the STARD flow embeds a cascade/partition. The 569→398/171
split and the 2×2 cell sums are internally consistent; no RATE_BACKCALC / CASCADE_SUM /
PARTITION_OVERLAP discrepancy.)

### DETECTOR: check_reference_adequacy.py  (Phase 2.5c-2; article-type ai_validation)
```
==============================================
 Reference Adequacy Gate (count + named methods)
==============================================
 Article type   : ai_validation -> ai_validation
 Cited refs     : 14  (target 25-45)
 Distribution   : Intro 5 / Methods 9 / Results 2 / Discussion 3
 Methods 0-cite : False
 △ [minor] below_article_type_target: Cited references (14) are below the ai_validation target (25-45).

 Verdict: BELOW_TARGET  |  0 major, 1 minor  |  adequacy_safe=True
```
EXIT=0 · 0 major, 1 minor
- FIRED (minor): below_article_type_target (14 < 25-45). EXPECTED — references are
  intentional [UNVERIFIED] placeholders (methods demo). fixable_by_ai:false; not fabricated.
- CLEAN: methods_zero_citations=false; uncited_named_methods=[] (Brier, DeLong, STARD,
  calibration all carry citation markers).

### DETECTOR: check_scope_coherence.py  (§D endpoint↔conclusion)
```
=========================================
 Scope Coherence (§D)
=========================================
| Check | Severity | Detail |
|---|---|---|
| (none) | — | conclusion scope matches the design/endpoint |

OK: conclusion scope matches the design/endpoint.
```
EXIT=0 · 0 major, 0 minor · CLEAN
(No CROSS_SECTIONAL_PROGNOSTIC / SURROGATE_CARE_DIRECTIVE. The Discussion explicitly
bounds clinical applicability and makes no care directive.)

### DETECTOR: check_artifact_coverage.py  (Phase 2.5f Methods↔Results↔disk)
```
=========================================
 Artifact Coverage (Phase 2.5f)
=========================================
manifest: analysis/_analysis_outputs.md
| Direction | Severity | Detail |
|---|---|---|
| DISK_UNREPORTED | Major | manifest output 'tables/predictions.csv' is not mentioned anywhere in the manuscript |

MAJOR candidate: 1 coverage gap(s).
```
EXIT=0 · 1 major, 0 minor
- FIRED (major): DISK_UNREPORTED — tables/predictions.csv (per-sample predicted
  probabilities) on disk + in manifest but not mentioned in the manuscript.
  fixable_by_ai:true → ADDRESSED in --fix iteration 1 (added Data Availability mention).

---

## ITERATION 1 (post-fix re-review)

Fix applied: added a Data Availability sentence releasing `predictions.csv`
(per-sample test-set predicted probabilities) so every accuracy estimate/CI/DeLong
comparison is independently recomputable. This closes the DISK_UNREPORTED Major.

### DETECTOR: check_artifact_coverage.py  (re-run)
```
=========================================
 Artifact Coverage (Phase 2.5f)
=========================================
manifest: analysis/_analysis_outputs.md
| Direction | Severity | Detail |
|---|---|---|
| (none) | — | Methods↔Results↔disk all reconciled |

OK: Methods/Results/disk reconciled.
```
EXIT=0 · 0 major, 0 minor · RESOLVED (was 1 major)

### DETECTOR: check_classical_style.py --strict  (re-run)
```
| (none) | — | classical-style body conventions satisfied |
OK: classical-style body conventions satisfied.
```
EXIT=0 · CLEAN

### DETECTOR: check_reference_adequacy.py  (re-run)
```
 Cited refs     : 14  (target 25-45)
 △ [minor] below_article_type_target: Cited references (14) are below the ai_validation target (25-45).
 Verdict: BELOW_TARGET  |  0 major, 1 minor  |  adequacy_safe=True
```
EXIT=0 · 0 major, 1 minor (unchanged; unfixable-by-AI; deliberate placeholder condition)

---

## Detector roll-up

| Detector | Iter 0 | Iter 1 (final) |
|----------|--------|----------------|
| check_classical_style.py | CLEAN | CLEAN |
| check_cohort_arithmetic.py | CLEAN | CLEAN (not re-run; manuscript flow unchanged) |
| check_reference_adequacy.py | 1 minor (ref count) | 1 minor (ref count) — deliberate |
| check_scope_coherence.py | CLEAN | CLEAN (not re-run; conclusions unchanged) |
| check_artifact_coverage.py | 1 MAJOR (predictions.csv) | CLEAN (resolved) |

Final deterministic state: 0 Major, 1 Minor (reference count, by design — [UNVERIFIED]
placeholders in a methods demo; never fabricated to hit a target).
