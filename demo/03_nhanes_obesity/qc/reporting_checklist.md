# STROBE Reporting Checklist - DEMO 3 (NHANES obesity<->diabetes)

- Guideline: STROBE 2007 (cross-sectional)
- Checklist source: medsci-skills/skills/check-reporting/references/checklists/STROBE.md (contract verified by check_checklist_exists.py)
- Manuscript: manuscript/manuscript.md
- Assessed: 2026-06-07 (genuine item-by-item assessment, not a target)

## Compliance

- Applicable items: 30 (4 NOT_APPLICABLE excluded: 6b, 12b, 14c, 16c)
- PRESENT: 25 | PARTIAL: 4 | MISSING: 1
- compliance_pct = present / applicable = 25/30 = 83.3%
- (Half-credit for PARTIAL would give 27/30 = 90.0%; the strict figure 83.3% is reported.)

## Item-by-item

| # | Section | Status | Note |
|---|---------|--------|------|
| 1a | Title/Abstract | PRESENT | Title and abstract both state 'cross-sectional' and 'survey-weighted'. |
| 1b | Abstract | PRESENT | Structured abstract: background, methods, results, conclusion with key numbers. |
| 2 | Introduction | PRESENT | Background on obesity-diabetes link and rationale for survey-design analysis. |
| 3 | Introduction | PRESENT | Objective stated: quantify weighted prevalence and demographically adjusted association; association framing. |
| 4 | Methods | PRESENT | Cross-sectional design of NHANES 2017-2018 stated early in Methods. |
| 5 | Methods | PRESENT | Setting (U.S. non-institutionalized population) and cycle dates (2017-2018) given. |
| 6a | Methods | PRESENT | Cross-sectional eligibility criteria given as a numbered list; source = NHANES. |
| 6b | Methods | NOT_APPLICABLE | Matching item for cohort/case-control; no matching in this cross-sectional study. |
| 7 | Methods | PRESENT | Exposure (obesity BMI>=30), outcome (self-report diabetes), covariates (age, sex, race), and sensitivity definition (HbA1c>=6.5) defined. |
| 8 | Methods | PRESENT | Measured BMI from MEC, DIQ010 self-report, LBXGH lab measurement named as data sources. |
| 9 | Methods | PARTIAL | Some bias handling implicit (HbA1c sensitivity for outcome misclassification, design-based variance); no dedicated 'efforts to address bias' subsection. |
| 10 | Methods | MISSING | No explicit study-size justification; sample is the available NHANES cycle (fixed n). Not addressed as a formal sample-size rationale. |
| 11 | Methods | PRESENT | Age handled continuously; BMI dichotomized at 30 with the boundary stated; race as categorical with referent. |
| 12a | Methods | PRESENT | Survey-weighted logistic regression with confounder adjustment described. |
| 12b | Methods | NOT_APPLICABLE | No subgroup or interaction analyses were performed in this demonstration. |
| 12c | Methods | PARTIAL | Missing data handled by complete-case eligibility (missing BMI / invalid status excluded; counts reported), but the complete-case strategy is not labeled as such in Methods prose. |
| 12d | Methods | PRESENT | Cross-sectional sampling strategy explicitly carried into analysis: weights, strata, PSU, Taylor linearization, design df=15. |
| 12e | Methods | PRESENT | HbA1c-based sensitivity analysis described. |
| 13a | Results | PRESENT | Numbers at each eligibility stage reported (9254 -> ... -> 5010). |
| 13b | Results | PRESENT | Reasons for exclusion at each stage given (age, missing BMI, invalid DM status). |
| 13c | Results | PRESENT | STROBE flow diagram provided (Figure 1). |
| 14a | Results | PRESENT | Weighted Table 1 of characteristics by diabetes status; key contrasts in text. |
| 14b | Results | PARTIAL | Missing-data counts reported for the exclusion-defining variables (BMI, DM status) in the flow; per-variable missingness in the analytic set not tabulated separately. |
| 14c | Results | NOT_APPLICABLE | Follow-up time item is cohort-specific; cross-sectional study has no follow-up. |
| 15 | Results | PRESENT | Cross-sectional: weighted diabetes prevalence overall and within obesity strata reported (7.6% / 17.3%). |
| 16a | Results | PARTIAL | Confounder-adjusted ORs with 95% CIs reported and confounders named; crude/unadjusted OR not reported as a separate estimate (only descriptive weighted prevalences by obesity). |
| 16b | Results | PRESENT | Category boundary for the dichotomized BMI variable (>=30) stated. |
| 16c | Results | NOT_APPLICABLE | Relative-to-absolute over time requires a time period; not meaningful for a cross-sectional prevalence-odds analysis. |
| 17 | Results | PRESENT | Sensitivity analysis (HbA1c outcome) reported in Results. |
| 18 | Discussion | PRESENT | Key results summarized with reference to the objective (association, ~3-fold odds). |
| 19 | Discussion | PRESENT | Limitations enumerated with direction of bias (cross-sectional, self-report misclassification, single BMI threshold, residual confounding). |
| 20 | Discussion | PRESENT | Cautious interpretation: association-only, no causal/prognostic claim. |
| 21 | Discussion | PRESENT | Generalizability addressed via weighting to the U.S. adult population. |
| 22 | Other | PRESENT | Funding stated (None; methods demonstration) on title page. |

## Auto-fixable gaps (would address in production)
- Item 10 (MISSING): note the study used the entire eligible NHANES 2017-2018 cycle (no a-priori sample-size calc; precision via CIs).
- Item 12c / 14b (PARTIAL): explicit "complete-case analysis" label + per-variable missingness line.
- Item 16a (PARTIAL): add crude (unadjusted) survey-weighted OR alongside the adjusted OR.
- Item 9 (PARTIAL): short bias-handling sentence.

Left as-is in the demo to keep the compliance figure a genuine assessment output.
