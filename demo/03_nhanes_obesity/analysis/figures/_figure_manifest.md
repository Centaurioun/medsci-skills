# Figure Manifest
Generated: 2026-06-07
Study type: observational / cross-sectional (STROBE), survey-weighted
Source: analysis/tables/*.csv (no fabricated values)

## Figure 1 — STROBE participant flow
- `strobe_flow.svg` / `strobe_flow.png` / `strobe_flow_600.png` / `strobe_flow.pdf`
- Built with make-figures `generate_flow_diagram.R --type strobe` (PDF/PNG) + DiagrammeRsvg (SVG)
- Counts traced to `analysis/tables/exclusion_cascade.csv`:
  9,254 -> 5,569 (age>=20) -> 5,175 (BMI) -> 5,010 (valid DM status) -> 5,010 analytic
  (obese n=2,090 / non-obese n=2,920)

## Figure 2 — Forest plot of adjusted odds ratios
- `forest_or.pdf` (vector) / `forest_or.png` (300 DPI)
- Built with `02_make_forest.py`, reading `analysis/tables/regression_or.csv`
- Primary term highlighted: Obesity (BMI>=30) aOR 3.03 (95% CI 2.29-4.02), p<0.001
- Reference: log-scale OR axis, null at 1.0; covariates age, sex, race shown

## Captions (draft)
- **Figure 1.** Flow of NHANES 2017-2018 participants through eligibility criteria to the
  analytic sample (cross-sectional, survey-weighted). Dashed boxes show exclusions.
- **Figure 2.** Adjusted odds ratios (95% CI) for self-reported diabetes from a
  survey-weighted logistic regression (n = 5,010; weights WTMEC2YR, strata SDMVSTRA,
  PSU SDMVPSU). Obesity (BMI >= 30) shown in red. The dashed line marks the null (OR = 1).
