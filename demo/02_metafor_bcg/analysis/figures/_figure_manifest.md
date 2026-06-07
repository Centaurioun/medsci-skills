# Figure Manifest
Generated: 2026-06-07
Study type: meta-analysis (PRISMA 2020)

| Figure | Path | Type | Tool | Critic | Rounds | Description |
|--------|------|------|------|--------|--------|-------------|
| Figure 1 | analysis/figures/prisma_flow.svg | flow-diagram | DiagrammeR (Graphviz dot + rsvg) | yes | 1 | PRISMA 2020 flow diagram; records cascade 318 → 197 screened → 39 sought → 35 assessed → 13 randomized trials included (357,347 participants) |
| Figure 2 | analysis/figures/forest.pdf | forest-plot | metafor (R) | yes | 1 | Random-effects (REML) forest plot of risk ratio of TB, BCG-vaccinated vs control, across 13 trials; pooled RR 0.49 [0.34, 0.70] |
| Figure 3 | analysis/figures/funnel.pdf | funnel-plot | metafor (R) | yes | 1 | Funnel plot of log risk ratio vs standard error for small-study/publication-bias assessment (Egger p = 0.189) |

## Outputs per figure
- prisma_flow: `.svg` (vector), `.png` (300 dpi, 2400 px), `.pdf` (vector), `_600.png` (600 dpi line-art)
- forest: `.pdf` (vector), `.png` (300 dpi)
- funnel: `.pdf` (vector), `.png` (300 dpi)

## Critic notes
- All three figures PASS critic Stage 1 (`critic_figure.py`): DPI ≥ 300, width spec met,
  no out-of-palette dominance, OCR text legible. Reports: `qc/{prisma_flow,forest,funnel}.critique.json`.
- Stage 2 (qualitative, flow-diagram rubric): PRISMA structure faithful, monochrome Arial,
  cascade arithmetic internally consistent (312+6−121=197; 197−158=39; 39−4=35; 35−22=13),
  exclusion side-boxes dashed without arrowheads, included box highlighted. PASS.
- Forest plot: per-study RR/CI match `analysis/tables/per_study_escalc.csv`; pooled diamond
  matches `analysis/tables/meta_results.csv` (RR 0.4894 [0.3441, 0.6962]). The inline 2×2 cell
  counts crowd the author labels slightly at this width — cosmetic only; the effect estimates,
  CIs, and pooled diamond are unambiguous. Accepted as `critic_pass: yes`.

## Data-integrity note (clean-room methods demo)
The 13 INCLUDED trials and all per-study counts derive from metafor's built-in `dat.bcg`
(Colditz et al. 1994), written to `data/dat_bcg.csv` and read by the analysis scripts.
The PRISMA *upstream* record counts (databases/duplicates/screening/exclusions) are ILLUSTRATIVE
for a methods demonstration of the medsci-skills pipeline — they are not the yield of a real
literature search. This is stated in the manuscript Methods and the figure caption.
