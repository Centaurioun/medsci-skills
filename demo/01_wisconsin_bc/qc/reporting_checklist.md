# STARD 2015 Reporting Compliance — DEMO 1 (Wisconsin Breast Cancer)

Guideline: **STARD 2015** (Standards for Reporting of Diagnostic Accuracy Studies)
Checklist source: check-reporting/references/checklists/STARD.md (vendored, 30 items)
Manuscript assessed: manuscript/manuscript.md + manuscript/title_page.md
Date: 2026-06-07 · medsci-skills v3.7.0

Note: STARD 2015 (not STARD-AI) is used per the task's stated reporting target. The study
evaluates classical ML classifiers on a tabular benchmark; it does not evaluate an LLM as the
diagnostic outcome, so MI-CLEAR-LLM is not paired. Framework-naming audit (Step 4e): clean.

## Part A: Summary

| Status | Count | % of 30 |
|--------|-------|---------|
| PRESENT | 14 | 46.7% |
| PARTIAL | 8 | 26.7% |
| MISSING | 1 | 3.3% |
| N/A | 7 | 23.3% |

**Applicable items (excl. N/A): 23**
**Overall compliance: PRESENT / applicable = 14 / 23 = 60.9%**

The 7 N/A items reflect that the dataset is a curated public computational benchmark with no
patients, procedures, recruitment timeline, or human readers (items 10b, 11, 14, 17, 20, 22, 23).
The single MISSING item is trial/protocol registration (item 26), expected for a benchmark
re-analysis. The PARTIAL items are mostly clinical-cohort descriptors (eligibility, sampling,
demographics, severity, sample-size justification) that a curated benchmark cannot fully supply.

## Part B: Item-by-item assessment

| # | Section | Item | Status | Location | Notes |
|---|---------|------|--------|----------|-------|
| 1 | Title/Abstract | Title identifies a diagnostic-accuracy study | PRESENT | Title | Title names "diagnostic accuracy" of classifiers; AUC/Sens/Spec are the measures. |
| 2 | Title/Abstract | Structured abstract | PRESENT | Abstract | Design, participants, index tests, reference standard, N, accuracy with 95% CIs, conclusion. |
| 3 | Introduction | Scientific/clinical background + intended use | PRESENT | Introduction p1 | FNA cytomorphometry background and discriminative intended use. |
| 4 | Introduction | Objectives/hypotheses | PRESENT | Introduction p3 | Two explicit aims (accuracy estimation + classifier comparison). |
| 5 | Methods | Study design (prospective/retrospective) | PARTIAL | Methods (Statistical analysis) | Held-out test design stated; prospective/retrospective label not given (benchmark has no collection timing). |
| 6 | Methods | Eligibility criteria, settings, locations | PARTIAL | Methods (Dataset) | Source/feature set described; clinical inclusion/exclusion and setting do not apply to a curated benchmark. |
| 7 | Methods | Sampling (consecutive/random/convenience) | PARTIAL | Methods (Statistical analysis) | Stratified random train/test split stated; original source-series sampling not characterized. |
| 8a | Methods | Index test in replicable detail | PRESENT | Methods (Index tests) | 3 classifiers fully specified (family, 400 trees, RBF kernel, train-only standardization, seed 42). |
| 8b | Methods | Reference standard in replicable detail | PRESENT | Methods (Dataset) + Abstract | Histopathologic diagnosis (malignant/benign). |
| 9 | Methods | Rationale for reference standard | PARTIAL | Methods (Dataset) | Histopathology used as gold standard; rationale implicit, no alternatives weighed. |
| 10a | Methods | Index cut-off pre-specification | PRESENT | Methods (Statistical analysis) | 0.5 threshold pre-specified; Youden reported as labeled alternative. |
| 10b | Methods | Reference cut-off pre-specification | N/A | -- | Binary histopathologic label; no cut-off applies. |
| 11 | Methods | Blinding | N/A | -- | No human readers; deterministic classifier on held-out features; leakage prevented by train/test split. |
| 12 | Methods | Methods for estimating/comparing accuracy | PRESENT | Methods (Statistical analysis) | AUC + DeLong CIs, Wilson CIs, Brier, pairwise DeLong comparison. |
| 13 | Methods | Sample size determination | PARTIAL | Methods (Statistical analysis) | Test n=171 stated; no formal power/precision justification. |
| 14 | Results | Dates and setting of recruitment | N/A | -- | Public benchmark; recruitment dates/setting unavailable. |
| 15 | Results | Demographics of participants | PARTIAL | Results (Sample characteristics) | Class-level feature means/SDs/SMDs given; age/sex absent from benchmark. |
| 16 | Results | Participant numbers + flow diagram | PRESENT | Results + Figure 1 | 569 to 398/171; malignant/benign counts; STARD flow diagram. |
| 17 | Results | Time interval index-vs-reference | N/A | -- | Both computed/recorded on the same archived sample; no interval. |
| 18 | Results | Distribution of disease severity | PARTIAL | Results (Sample characteristics) | Class distribution via SMDs; severity spectrum/alternative diagnoses not characterized. |
| 19 | Results | Cross-tabulation index x reference | PRESENT | Results + Figures 1, 3 | TP/FP/FN/TN reported (LR) + confusion matrices for all 3. |
| 20 | Results | Adverse events | N/A | -- | Computational re-analysis; no procedures, no adverse events. |
| 21 | Results | Accuracy estimates with precision | PRESENT | Results | AUC (DeLong CI) + Sens/Spec/PPV/NPV/Acc (Wilson CI) per index test. |
| 22 | Results | Handling of indeterminate results | N/A | -- | No indeterminate results; no missing labels/features. |
| 23 | Results | Subgroup/variability analyses | N/A | -- | None performed; none claimed. |
| 24 | Discussion | Study limitations | PRESENT | Discussion p3 | Single-source benchmark, high prevalence, no external validation, conventional threshold, methods-demo caveat. |
| 25 | Discussion | Clinical applicability | PRESENT | Discussion p2-3 | Intended interpretive role stated and clinical applicability explicitly bounded. |
| 26 | Other | Registration | MISSING | -- | No registration; benchmark re-analysis unregistered (registration increasingly expected). |
| 27 | Other | Protocol accessibility | PARTIAL | Data Availability | Full code + reproducibility lock accompany the demo; no separately citable protocol. |
| 28 | Other | Funding | PRESENT | Title page (Funding) | "None (methods demonstration)". |

## Part C: Action items (MISSING / PARTIAL)

- [MISSING] Item 26 (Registration): add a registration number or state explicitly that the
  benchmark re-analysis was not prospectively registered. (Out of scope for this methods demo.)
- [PARTIAL] Items 5, 6, 7, 9, 13, 15, 18, 27: clinical-cohort descriptors a curated public
  benchmark cannot fully supply. For a real diagnostic study they would be filled from the source
  cohort metadata and a power/precision calculation. Left PARTIAL deliberately, not fabricated.

## Part D: JSON summary

```json
{
  "guideline": "STARD 2015",
  "manuscript": "manuscript/manuscript.md",
  "total_items": 30,
  "counts": { "PRESENT": 14, "PARTIAL": 8, "MISSING": 1, "NA": 7 },
  "applicable_items": 23,
  "present_items": 14,
  "compliance_pct": 60.9,
  "compliance_formula": "PRESENT / applicable = 14 / 23 = 60.9%",
  "framework_naming_audit": "clean",
  "registration_timing": { "registered": false, "note": "benchmark re-analysis; not registered" },
  "missing_items": [26],
  "partial_items": [5, 6, 7, 9, 13, 15, 18, 27],
  "na_items": [ "10b", 11, 14, 17, 20, 22, 23 ],
  "note": "compliance_pct from a genuine item-by-item assessment; N/A excluded from denominator. No target number invented."
}
```
