# Companion: reuse generate_flow_diagram.R's DOT builder to also emit an SVG
# (the canonical script writes PDF/PNG only; the demo manifest requests .svg).
suppressPackageStartupMessages({
  library(DiagrammeR); library(DiagrammeRsvg); library(rsvg); library(yaml)
})
# Source the canonical functions WITHOUT triggering main() (interactive guard).
src <- readLines("${MEDSCI_SKILLS_ROOT}/skills/make-figures/scripts/generate_flow_diagram.R")
src <- src[!grepl("^if \\(!interactive\\(\\)\\) main\\(\\)", src)]
eval(parse(text = paste(src, collapse = "\n")))

cfg <- yaml::read_yaml("analysis/prisma_counts.yaml")
dot <- build_dot(cfg)
svg <- export_svg(grViz(dot))
writeLines(svg, "analysis/figures/prisma_flow.svg")
# Also re-emit a clean PNG from the same SVG for SSOT consistency
rsvg_png(charToRaw(svg), "analysis/figures/prisma_flow.png", width = 2400)
cat("Wrote analysis/figures/prisma_flow.svg + prisma_flow.png\n")
