# Figure Manifest
Generated: 2026-06-07
Study type: diagnostic-accuracy (STARD 2015)

| Figure | Path | Type | Tool | Critic | Rounds | Description |
|--------|------|------|------|--------|--------|-------------|
| Figure 1 | figures/stard_flow.svg | flow-diagram | R (DiagrammeR/Graphviz) | yes | 1 | STARD 2015 participant flow: 569 FNA samples → stratified 70/30 split (seed 42) → test set n=171, with histopathology reference 2×2 cells (TP=60, FP=1, FN=4, TN=106; Logistic Regression at threshold 0.5) |
| Figure 2 | analysis/figures/roc_curve.pdf | roc-curve | matplotlib | yes | 1 | ROC curves for the three index tests (Logistic Regression, Random Forest, SVM-RBF) with DeLong AUC + 95% CI in legend |
| Figure 3 | analysis/figures/confusion_matrices.pdf | confusion-matrix | matplotlib | yes | 1 | Confusion matrices for the three index tests at threshold 0.5 (test set n=171) |

## Critic notes
- Figure 1 (STARD flow): rendered via the canonical R pipeline
  (`generate_flow_diagram.R`, DiagrammeR + Graphviz dot + rsvg). Monochrome
  black-outline / white-fill in Arial. All cell counts trace to
  `analysis/tables/diagnostic_accuracy.csv` (Logistic Regression row).
  Arithmetic verified: TP+FP=61, FN+TN=110, TP+FN=64 (malignant), FP+TN=107
  (benign), total=171; Sens=60/64=0.938, Spec=106/107=0.991 — both reproduce
  the CSV exactly. SVG (vector source) + PNG (300 dpi) + 600 dpi PNG emitted.
- Figures 2–3: produced by the upstream `/analyze-stats` stage (gate-clean);
  retained at their original `analysis/figures/` paths. No re-render needed.

## Source-of-truth note
Every quantitative element in these figures is read from a CSV under
`analysis/tables/`; no number is hand-typed into a figure.
