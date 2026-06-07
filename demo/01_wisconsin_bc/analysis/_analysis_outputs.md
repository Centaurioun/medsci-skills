# Analysis Outputs
Generated: 2026-06-07
Study type: Diagnostic accuracy (DTA / STARD), index tests vs histopathology reference

## Dataset
- Wisconsin Breast Cancer (sklearn.datasets.load_breast_cancer), N=569, malignant=212, benign=357, 30 FNA features.
- Stratified 70/30 train/test split, seed=42. Test n=171.

## Tables
- `tables/table1_features_by_class.csv` -- Key features by reference-standard class (mean (SD), SMD, P)
- `tables/diagnostic_accuracy.csv` -- Sens/Spec/PPV/NPV/Acc (Wilson CIs) + AUC (DeLong CI) + Brier + Youden threshold
- `tables/auc_comparison_delong.csv` -- Pairwise DeLong AUC comparison
- `tables/predictions.csv` -- Per-sample test-set predicted probabilities + truth

## Figures
- `figures/roc_curve.pdf` / `.png` -- ROC curves (3 models, DeLong AUC in legend)
- `figures/confusion_matrices.pdf` / `.png` -- Confusion matrices at threshold 0.5

## Key results (test set, n=171)
- Logistic Regression: AUC 0.998 (0.994-1.0), Sens 0.938, Spec 0.991, Brier 0.019
- Random Forest: AUC 0.996 (0.991-1.0), Sens 0.922, Spec 1.0, Brier 0.029
- SVM (RBF): AUC 0.997 (0.992-1.0), Sens 0.922, Spec 1.0, Brier 0.02
