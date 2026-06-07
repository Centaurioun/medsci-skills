# Analysis Outputs
Generated: 2026-06-07
Study type: Survey-weighted cross-sectional association (NHANES 2017-2018 complex survey)
Data source: CDC NHANES 2017-2018 public XPT files (clean-room; no fabricated values)

## Design
- Weights: WTMEC2YR (MEC exam 2-year weight, single cycle, used as-is)
- Strata: SDMVSTRA ; Cluster/PSU: SDMVPSU (nest = TRUE)
- Tool: R 4.5.3, survey + tableone (Taylor linearization SEs)
- Design df = 15 (15 strata x 2 PSU)

## Population & exclusion cascade
- `tables/exclusion_cascade.csv` -- STROBE exclusion steps
- Total DEMO_J participants: 9254 -> adults >=20 (5569) -> measured BMI (5175)
  -> valid self-report diabetes status DIQ010 in {1,2} (5010) -> positive MEC weight (5010 FINAL)
- Analytic N = 5010

## Tables
- `tables/table1.csv` -- Weighted Table 1 by diabetes status (self-report)
- `tables/regression_or.csv` -- Primary adjusted OR table (estimate, ci_lower, ci_upper, p)
- `tables/regression_or_hba1c_sensitivity.csv` -- Sensitivity model (outcome = HbA1c>=6.5)
- `tables/key_scalars.csv` -- Headline numbers for the manuscript
- `tables/exclusion_cascade.csv` -- STROBE flow counts

## Key results (traced to key_scalars.csv)
- Weighted diabetes prevalence (self-report): 11.7% (95% CI 10.6-12.8)
- Weighted obesity prevalence (BMI>=30): 42.3% (95% CI 38.9-45.7)
- PRIMARY adjusted OR obesity->diabetes: 3.03 (95% CI 2.29-4.02), p < 0.001
  (model: diabetes ~ obesity + age + sex + race)
- Sensitivity (HbA1c>=6.5, n=4779): aOR 2.95 (95% CI 2.18-3.98), p < 0.001
- Weighted HbA1c>=6.5 prevalence: 9.8% (95% CI 8.8-10.8)

## Scripts
- `00_prepare_data.py` -- read XPT, merge on SEQN, exclusion cascade, write data/nhanes_analytic.csv
- `01_survey_analysis.R` -- survey design, weighted Table 1, primary + sensitivity wlogistic regression

## Figures (downstream /make-figures)
- `figures/strobe_flow.{svg,png}` -- STROBE participant flow
- `figures/forest_or.{pdf,png}` -- forest plot of adjusted ORs
