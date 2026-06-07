# Diagnostic accuracy of three machine-learning classifiers for distinguishing malignant from benign breast masses on fine-needle aspirate cytomorphometry

## Abstract

**Background:** Fine-needle aspiration (FNA) of a breast mass yields quantitative nuclear and cell-shape measurements that can be used to discriminate malignant from benign lesions. Whether routine machine-learning classifiers reach diagnostic accuracy comparable to one another on these features, and whether any single classifier is preferable, is the question addressed here.

**Objective:** To estimate and compare the diagnostic accuracy of three machine-learning classifiers using histopathology as the reference standard, and to report this analysis as a reproducible demonstration of the medsci-skills v3.7.0 pipeline.

**Methods:** We used the Wisconsin Diagnostic Breast Cancer dataset (569 FNA samples; 212 malignant, 357 benign), in which 30 cytomorphometric features were computed per sample. The reference standard was the histopathologic diagnosis (malignant or benign). Samples were partitioned into training (n = 398) and test (n = 171) sets by a stratified 70/30 split (seed 42). Three index tests were fitted on the training set: logistic regression, random forest, and a support-vector machine with a radial-basis-function kernel. Discrimination was summarized by the area under the receiver-operating-characteristic curve (AUC) with DeLong 95% confidence intervals; sensitivity and specificity at a 0.5 probability threshold were reported with Wilson intervals; calibration was summarized by the Brier score. Pairwise AUC differences were tested with the DeLong method.

**Results:** On the test set (64 malignant, 107 benign), logistic regression reached an AUC of 0.998 (95% CI 0.994–1.000), with sensitivity 0.938 (95% CI 0.850–0.975) and specificity 0.991 (95% CI 0.949–0.998) at the 0.5 threshold, and a Brier score of 0.019. The random forest reached an AUC of 0.996 (95% CI 0.991–1.000) and the support-vector machine an AUC of 0.997 (95% CI 0.992–1.000). All three pairwise DeLong comparisons were non-significant (p = 0.554, 0.640, and 0.800).

**Conclusion:** All three classifiers discriminated malignant from benign FNA samples with very high and statistically indistinguishable accuracy on this benchmark; logistic regression offered the best probability calibration. The result should be read as a methods demonstration rather than clinical validation, because the dataset is a curated single-source benchmark and the references in this manuscript are unverified placeholders.

## INTRODUCTION

Fine-needle aspiration (FNA) is a low-cost, minimally invasive sampling method for a palpable or imaged breast mass [1]. Digitized FNA images can be reduced to quantitative descriptors of nuclear size, texture, and cell-shape variability, and these descriptors separate malignant from benign lesions with substantial accuracy [2]. Translating such measurements into a reproducible classifier is a recurring task in diagnostic machine learning, and several model families are routinely applied without a clear consensus on which is preferable [3].

Reporting of diagnostic-accuracy studies is governed by the STARD 2015 statement, which asks for an explicit reference standard, a participant flow diagram, and accuracy estimates accompanied by confidence intervals [4]. Comparative claims between competing index tests further require a test for the difference in discrimination rather than a side-by-side display of point estimates [5]. Many published comparisons report only AUC point estimates and omit the paired statistical test, leaving the reader unable to judge whether an apparent ranking is real.

This study has two aims. The first is substantive: to estimate the diagnostic accuracy of three machine-learning classifiers for malignant-versus-benign FNA discrimination against a histopathology reference standard, and to test whether the classifiers differ. The second is methodological: the analysis serves as a clean-room demonstration of the medsci-skills v3.7.0 reproducible-reporting pipeline, in which every quantitative claim is traced to a committed analysis artifact and the manuscript is checked against deterministic style, reporting, and reference-adequacy gates.

## METHODS

### Dataset and reference standard

We used the Wisconsin Diagnostic Breast Cancer dataset as distributed with scikit-learn [6], comprising 569 FNA samples. Thirty cytomorphometric features (the mean, standard error, and worst value of ten nuclear measurements) were computed per sample. The reference standard for each sample was the histopathologic diagnosis, coded as malignant or benign; 212 samples were malignant and 357 were benign. No patient-level identifiers were present in the dataset.

### Index tests

Three index tests were evaluated: a logistic-regression classifier [7], a random-forest classifier with 400 trees [8], and a support-vector machine with a radial-basis-function kernel [9]. Continuous features were standardized to zero mean and unit variance using parameters estimated on the training set only, and the same transformation was applied to the test set to prevent information leakage. Each index test output a probability of malignancy.

### Statistical analysis

Samples were partitioned into a training set (n = 398) and a test set (n = 171) by a stratified 70/30 split with a fixed random seed (42); the test set preserved the malignant/benign proportion of the full dataset (64 malignant, 107 benign). All accuracy estimates were computed on the held-out test set.

Discrimination was summarized by the area under the receiver-operating-characteristic curve (AUC), with 95% confidence intervals from the DeLong method [5]. At a fixed probability threshold of 0.5, sensitivity, specificity, positive predictive value, negative predictive value, and accuracy were computed, and binomial proportions were given Wilson 95% confidence intervals [10]. Probability calibration was summarized by the Brier score [11]. The Youden index was used to report an alternative operating threshold for each index test. Pairwise differences in AUC between index tests were tested with the DeLong method for correlated curves [5]; a two-sided p value below 0.05 was treated as evidence of a difference. Reporting followed the STARD 2015 statement [4]. Analyses used Python (scikit-learn [6] and SciPy [12]) with the random seed fixed at 42 for reproducibility.

## RESULTS

### Sample characteristics

The 30 cytomorphometric features separated the two reference-standard classes strongly. Mean nuclear-concave-points was 0.09 (SD 0.03) in malignant versus 0.03 (SD 0.02) in benign samples (standardized mean difference 2.33), and mean perimeter was 115.37 (SD 21.85) versus 78.08 (SD 11.81; standardized mean difference 2.12); both differences were significant (p = 3.13 × 10⁻⁷¹ and p = 1.02 × 10⁻⁶⁶, respectively). Mean fractal dimension did not differ between classes (standardized mean difference −0.03; p = 0.767). Participant flow is shown in Figure 1.

### Diagnostic accuracy

On the test set (n = 171), logistic regression reached an AUC of 0.998 (95% CI 0.994–1.000). At the 0.5 probability threshold it correctly classified 60 of 64 malignant and 106 of 107 benign samples, giving a sensitivity of 0.938 (95% CI 0.850–0.975), a specificity of 0.991 (95% CI 0.949–0.998), a positive predictive value of 0.984, a negative predictive value of 0.964, and an accuracy of 0.971. Its Brier score was 0.019, the lowest of the three index tests.

The random forest reached an AUC of 0.996 (95% CI 0.991–1.000), with sensitivity 0.922 (95% CI 0.830–0.966), specificity 1.000 (95% CI 0.965–1.000), and a Brier score of 0.029. The support-vector machine reached an AUC of 0.997 (95% CI 0.992–1.000), with sensitivity 0.922 (95% CI 0.830–0.966), specificity 1.000 (95% CI 0.965–1.000), and a Brier score of 0.020. The receiver-operating-characteristic curves are shown in Figure 2 and the confusion matrices at the 0.5 threshold in Figure 3.

### Pairwise comparison of discrimination

The three index tests were statistically indistinguishable in discrimination. Pairwise DeLong tests gave p = 0.554 for logistic regression versus random forest, p = 0.800 for logistic regression versus the support-vector machine, and p = 0.640 for random forest versus the support-vector machine. No pairwise difference approached significance.

## DISCUSSION

Three routine machine-learning classifiers discriminated malignant from benign breast FNA samples with very high accuracy on this benchmark, and the differences among them were not statistically significant. Logistic regression, the simplest model, matched the two more flexible models on discrimination and gave the best probability calibration (Brier score 0.019). For a feature set this separable, model complexity bought no measurable gain in discrimination, which argues for preferring the model that is easiest to calibrate and interpret.

These findings agree with the broader observation that, on well-separated tabular feature sets, regularized linear models are often competitive with ensemble and kernel methods [3]. The practical implication is that a comparative diagnostic study should report a paired test of discrimination, as the STARD framework and the DeLong method jointly recommend [4,5]; had we reported only the AUC point estimates, logistic regression's 0.998 would appear to outrank the random forest's 0.996, yet that ordering is within sampling noise (p = 0.554).

This study has clear limitations. The dataset is a curated, single-source benchmark with a high malignant prevalence relative to a screening population, so the reported predictive values are not transportable to clinical practice. There was no external validation cohort and no assessment across image-acquisition sites or operators. The 0.5 probability threshold is conventional rather than clinically optimized, although Youden-based thresholds are reported alongside it for each index test. Finally, the references in this manuscript are unverified placeholders: the analysis is a reproducibility demonstration of the medsci-skills v3.7.0 pipeline, not a clinical validation, and the manuscript should not be cited as evidence for clinical deployment.

Within those limits, the analysis demonstrates a fully traceable diagnostic-accuracy workflow: a STARD-compliant participant flow, AUC estimates with DeLong intervals, threshold metrics with Wilson intervals, a calibration score, and a paired test of discrimination, with every reported number tracing to a committed analysis table.

In summary, logistic regression, random forest, and a radial-basis-function support-vector machine all distinguished malignant from benign breast FNA samples with statistically indistinguishable, very high accuracy on the Wisconsin benchmark; logistic regression is the most attractive of the three because it matches the others on discrimination while offering the best calibration and the simplest model.

## Data Availability

The dataset is the Wisconsin Diagnostic Breast Cancer dataset distributed publicly with scikit-learn (`sklearn.datasets.load_breast_cancer`). All analysis code, derived tables, figures, and a reproducibility lock file accompany this demonstration. The complete per-sample test-set predicted probabilities for all three index tests are released alongside the reference-standard labels (`predictions.csv`), so that every accuracy estimate, confidence interval, and DeLong comparison reported here can be recomputed independently.

## Figure Legends

**Figure 1.** STARD 2015 participant flow diagram. The 569 FNA samples were partitioned by a stratified 70/30 split (seed 42) into a training set (n = 398) and a test set (n = 171). The histopathology reference standard was applied to all test samples (64 malignant, 107 benign). The 2×2 cell counts shown are for the logistic-regression index test at a 0.5 probability threshold (TP = 60, FP = 1, FN = 4, TN = 106).

**Figure 2.** Receiver-operating-characteristic curves for the three index tests on the test set, with DeLong AUC and 95% confidence interval in the legend.

**Figure 3.** Confusion matrices for the three index tests at a 0.5 probability threshold (test set, n = 171).

## References

> Note: the references below are UNVERIFIED placeholders. This manuscript is a
> reproducibility demonstration of the medsci-skills v3.7.0 pipeline, not a clinical
> submission. In a real submission these markers would be resolved through
> /search-lit → /lit-sync → /verify-refs and would not be hand-typed.

1. [UNVERIFIED] Reference on fine-needle aspiration of breast masses.
2. [UNVERIFIED] Reference on quantitative cytomorphometry for breast lesion classification.
3. [UNVERIFIED] Reference on comparative performance of linear versus ensemble/kernel classifiers on tabular data.
4. [UNVERIFIED] Bossuyt PM, et al. STARD 2015 statement for reporting diagnostic accuracy studies.
5. [UNVERIFIED] DeLong ER, et al. Comparing the areas under two or more correlated ROC curves.
6. [UNVERIFIED] Pedregosa F, et al. scikit-learn: machine learning in Python.
7. [UNVERIFIED] Reference on logistic regression for classification.
8. [UNVERIFIED] Breiman L. Random forests.
9. [UNVERIFIED] Cortes C, Vapnik V. Support-vector networks.
10. [UNVERIFIED] Wilson EB. Probable inference, the law of succession, and statistical inference.
11. [UNVERIFIED] Brier GW. Verification of forecasts expressed in terms of probability.
12. [UNVERIFIED] Virtanen P, et al. SciPy 1.0: fundamental algorithms for scientific computing in Python.
