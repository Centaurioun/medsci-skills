## Abstract

**Background:** Obesity and type 2 diabetes frequently co-occur, but nationally
representative estimates of their association require analysis that respects the complex
sampling design of population health surveys. We examined the cross-sectional association
between obesity and self-reported diabetes in U.S. adults using the National Health and
Nutrition Examination Survey (NHANES) 2017-2018 cycle.

**Methods:** We analyzed adults aged 20 years or older with a measured body mass index (BMI),
a valid self-reported diabetes status, and a positive examination weight. Obesity was defined
as BMI of 30 kg/m^2 or higher. The outcome was self-reported physician-diagnosed diabetes.
Survey-weighted logistic regression (examination weights, with stratification and clustering)
estimated the adjusted odds ratio (aOR) for obesity, controlling for age, sex, and
race/ethnicity. A glycohemoglobin-based outcome (HbA1c of 6.5% or higher) was used in a
sensitivity analysis.

**Results:** Of 9,254 NHANES 2017-2018 participants, 5,010 met eligibility criteria. The
weighted prevalence of diabetes was 11.7% (95% confidence interval [CI], 10.6-12.8) and of
obesity 42.3% (95% CI, 38.9-45.7). The weighted prevalence of diabetes was 7.6% among
non-obese adults and 17.3% among adults with obesity. In the survey-weighted model, obesity
was associated with diabetes (aOR 3.03; 95% CI, 2.29-4.02; p < 0.001) after adjustment for
age, sex, and race/ethnicity. The HbA1c-based sensitivity analysis was concordant (aOR 2.95;
95% CI, 2.18-3.98).

**Conclusion:** In this nationally representative cross-sectional sample, obesity was
strongly associated with diabetes after demographic adjustment. Because exposure and outcome
were measured at the same examination, these findings describe a cross-sectional association
and do not support any causal or temporal conclusion.

**Keywords:** obesity; diabetes mellitus; NHANES; complex survey; cross-sectional study;
body mass index

## **INTRODUCTION**

Obesity is among the most prevalent modifiable conditions in U.S. adults and is consistently
linked to metabolic disease, including type 2 diabetes [UNVERIFIED]. Understanding the
population-level association between obesity and diabetes is relevant for surveillance and
for framing the scale of metabolic risk in the general adult population.

National health surveys are well suited to this question because they sample the
non-institutionalized population using a stratified, multistage probability design and carry
sampling weights that permit nationally representative estimates [UNVERIFIED]. Each sampled
adult represents a known number of people in the target population, and adults are not sampled
independently but in clusters nested within design strata. Analyses that ignore the survey
weights, stratification, and clustering therefore yield biased point estimates and
underestimated standard errors, so the design must be carried into both the descriptive and
the regression steps [UNVERIFIED]. A weighted prevalence and a survey-weighted odds ratio,
estimated with design-based variance, are the quantities that generalize to the U.S. adult
population rather than to the sampled individuals alone.

The National Health and Nutrition Examination Survey (NHANES) measures height and weight
directly in a mobile examination center, allowing obesity to be defined from a measured body
mass index (BMI) rather than from self-report. Using the 2017-2018 NHANES cycle, we
quantified the weighted prevalence of obesity and diabetes in U.S. adults and estimated the
demographically adjusted association between obesity and self-reported diabetes. We treat the
result as an association, consistent with the cross-sectional design.

## **METHODS**

### Study design and data source

This was a cross-sectional analysis of the NHANES 2017-2018 cycle, a nationally
representative survey of the civilian, non-institutionalized U.S. population conducted with a
stratified, multistage probability sampling design. NHANES is a publicly available,
de-identified data resource; no additional ethical approval was required for this secondary
analysis. Reporting follows the STROBE recommendations for cross-sectional studies.

### Study population

Eligible participants were adults who met all of the following criteria: (1) age 20 years or
older; (2) a non-missing measured BMI; (3) a valid self-reported diabetes status (a response
of "yes" or "no"); and (4) a positive mobile examination center (MEC) examination weight.
Participants with a borderline, refused, or unknown diabetes status, with a missing BMI, or
younger than 20 years were excluded.

### Variables

The exposure was obesity, defined as a measured BMI of 30 kg/m^2 or higher (versus less than
30 kg/m^2). The primary outcome was self-reported physician-diagnosed diabetes. Covariates
were age (continuous, years), sex (male or female), and race/ethnicity (Mexican American,
other Hispanic, non-Hispanic White, non-Hispanic Black, non-Hispanic Asian, and
other/multiracial, with non-Hispanic White as the reference). For a sensitivity definition of
diabetes, we used glycohemoglobin (HbA1c) of 6.5% or higher among participants with an
available HbA1c measurement.

### Statistical analysis

All analyses incorporated the NHANES complex survey design: the MEC examination weight as the
sampling weight, the design stratum as the stratification variable, and the masked variance
pseudo-primary sampling unit as the cluster, with nesting of clusters within strata. Variance
was estimated by Taylor-series linearization, yielding 15 design degrees of freedom for the
single two-year cycle, which was used as supplied without multi-cycle re-weighting.

Weighted prevalences of obesity and diabetes were estimated with 95% confidence intervals
(CIs). A weighted Table 1 described participant characteristics by diabetes status. A
survey-weighted logistic regression model estimated the adjusted odds ratio (aOR) for obesity
with respect to diabetes, adjusting for age, sex, and race/ethnicity. The sensitivity
analysis repeated the model with the HbA1c-based outcome among participants with an available
HbA1c value. A two-sided p value below 0.05 was considered statistically significant.
Analyses were performed in R using the survey package.

The authors used a large language model (Claude Opus 4.8, Anthropic, accessed via the
programmatic API in June 2026) to assist with drafting and consistency checking of the
manuscript text; all statistical results were generated by executed analysis code, and all
text was reviewed and approved by the authors, who take responsibility for the work.

## **RESULTS**

### Participants

Of 9,254 NHANES 2017-2018 participants, 3,685 were excluded for being younger than 20 years,
394 for a missing measured BMI, and 165 for a borderline, refused, or unknown diabetes
status; no eligible participant had a non-positive examination weight. The final analytic
sample comprised 5,010 adults, of whom 2,090 (41.7%) were classified as obese on unweighted
counts and 2,920 as non-obese (Figure 1).

### Weighted prevalence

The weighted prevalence of diabetes was 11.7% (95% CI, 10.6-12.8), and the weighted
prevalence of obesity was 42.3% (95% CI, 38.9-45.7). Adults with diabetes were older than
adults without diabetes (weighted mean age 61.6 versus 46.2 years) and had a higher mean BMI
(33.3 versus 29.3 kg/m^2) (Table 1). The weighted prevalence of diabetes was 7.6% among
non-obese adults and 17.3% among adults with obesity.

### Association between obesity and diabetes

In the survey-weighted logistic regression model, obesity was associated with self-reported
diabetes (aOR 3.03; 95% CI, 2.29-4.02; p < 0.001) after adjustment for age, sex, and
race/ethnicity (Table 2, Figure 2). Older age was also associated with diabetes (aOR 1.07 per
year; 95% CI, 1.06-1.08; p < 0.001), and female sex was associated with lower odds (aOR 0.66;
95% CI, 0.47-0.92; p = 0.046). Relative to non-Hispanic White adults, higher odds were
observed for non-Hispanic Asian (aOR 2.39; 95% CI, 1.53-3.75), other/multiracial (aOR 1.95;
95% CI, 1.37-2.77), and Mexican American (aOR 1.68; 95% CI, 1.17-2.41) adults.

### Sensitivity analysis

Among the 4,779 participants with an available HbA1c measurement, the weighted prevalence of
an HbA1c of 6.5% or higher was 9.8% (95% CI, 8.8-10.8). Using this laboratory-based outcome,
the adjusted association with obesity was concordant with the primary analysis (aOR 2.95; 95%
CI, 2.18-3.98).

## **DISCUSSION**

In a nationally representative cross-sectional sample of U.S. adults, obesity was associated
with roughly three-fold higher odds of self-reported diabetes after adjustment for age, sex,
and race/ethnicity. The association was consistent when diabetes was defined from measured
glycohemoglobin rather than self-report, which argues against the result being an artifact of
self-report alone. The weighted prevalences of obesity (42.3%) and diabetes (11.7%) are
consistent with the high population burden of metabolic disease in U.S. adults [UNVERIFIED].

These findings illustrate the practical importance of carrying the complex survey design into
the analysis. The point estimates were weighted to the U.S. adult population, and the
confidence intervals reflect the stratified, clustered sampling through Taylor-series
linearization rather than treating the sample as a simple random draw [UNVERIFIED]. The
single two-year cycle was used with its supplied examination weight, which is appropriate
when only one cycle is analyzed and avoids the re-weighting that combining adjacent cycles
would require [UNVERIFIED]. The demographic covariates behaved as expected, with age strongly
associated with diabetes, underscoring that the obesity association is not explained by the
age structure of the obese group.

The magnitude of the obesity association is consistent with the observed contrast in weighted
prevalence: diabetes was reported by 7.6% of non-obese adults and 17.3% of adults with
obesity, a gradient that persisted after adjustment. The pattern across race/ethnicity
groups, with higher adjusted odds among several minority groups relative to non-Hispanic
White adults, is also broadly in keeping with documented disparities in metabolic disease
[UNVERIFIED]; we report these covariate estimates descriptively and do not interpret them as
the study's primary question. The concordance between the self-report and HbA1c-based outcomes
strengthens confidence that the obesity-diabetes association is not an artifact of how the
outcome was ascertained, although the two definitions are not interchangeable and identify
overlapping but distinct groups.

Several limitations apply. First, and most importantly, the design is cross-sectional:
obesity and diabetes were ascertained at the same examination, so the analysis describes an
association and cannot establish temporal order or causation. We therefore frame the result as
an association only and draw no inference about disease onset over time, which a single-visit
design cannot address. Second, the
primary outcome relied on self-reported physician diagnosis, which can misclassify
undiagnosed diabetes; the concordant HbA1c-based sensitivity analysis partly mitigates but
does not eliminate this concern. Third, obesity was defined by a single BMI threshold, which
does not capture body-fat distribution. Fourth, residual confounding by unmeasured factors
(diet, physical activity, socioeconomic position) is likely and was not addressed.

## **CONCLUSION**

In U.S. adults sampled by NHANES 2017-2018, obesity was strongly and independently associated
with diabetes in a survey-weighted analysis. Given the cross-sectional design, this is an
association rather than evidence of causation, and data collected at more than one time point
would be needed to address questions of temporality and disease onset.

## Tables

**Table 1.** Weighted characteristics of NHANES 2017-2018 adults by diabetes status. See
`analysis/tables/table1.csv`.

**Table 2.** Survey-weighted logistic regression for self-reported diabetes (adjusted odds
ratios, 95% CI). See `analysis/tables/regression_or.csv`.

## Figure Legends

**Figure 1.** Flow of NHANES 2017-2018 participants through eligibility criteria to the
analytic sample (n = 5,010). Dashed boxes indicate exclusions.

**Figure 2.** Adjusted odds ratios (95% CI) for self-reported diabetes from the
survey-weighted logistic regression model (weights, stratification, and clustering applied).
The obesity term is highlighted; the dashed line marks the null (odds ratio = 1).

## Data Availability

The data are publicly available from the U.S. Centers for Disease Control and Prevention
NHANES program (2017-2018 cycle). The derived analytic dataset and analysis code that
reproduce all results are available with this report.

## References

References in this methods-demonstration manuscript are intentionally left as [UNVERIFIED]
placeholders. In a production run they would be resolved through /search-lit and /verify-refs
against PubMed and CrossRef and rendered by a reference manager.
