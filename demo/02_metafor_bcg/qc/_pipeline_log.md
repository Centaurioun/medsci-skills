# Pipeline Log — DEMO 2 (BCG vaccine vs TB meta-analysis)

medsci-skills v3.7.0 clean-room dogfooding. Staging: <clean-room staging>/02_metafor_bcg
Environment: R 4.5.3 (prompt said 4.8.0; actual R is 4.5.3), metafor 4.8.0, meta 8.2.1, pandoc, d2, librsvg/rsvg.
Data: metafor built-in dat.bcg (13 RCTs, Colditz et al. 1994), written to data/dat_bcg.csv via R (no hand-typed cells).

## Step 1 — /analyze-stats (meta-analysis mode)
- analysis/write_data.R: dat.bcg -> data/dat_bcg.csv (13 trials x 9 cols; total participants 357,347).
- analysis/meta_analysis.R: escalc(measure="RR") + rma(method="REML"); meta::metabin cross-check (Inverse/REML/HK); set.seed(42).
- Outputs: meta_results.csv, per_study_escalc.csv, leave_one_out.csv; forest.{pdf,png}, funnel.{pdf,png}; _analysis_outputs.md.
- Pooled RR 0.489 (95% CI 0.344-0.696); I2 92.2%; tau2 0.313; Q(12)=152.23 p=1.997e-26; PI 0.155-1.549; Egger z=-1.40 p=0.189; rank tau=0.026 p=0.952; metabin RR 0.489 (0.330-0.726).
- Phase 3.5 generated-code gate: check_generated_code.py --strict on meta_analysis.R AND write_data.R -> both reproducibility-clean (0 Major, 0 minor). EXIT 0.

## Step 2 — /make-figures (study-type meta-analysis)
- PRISMA 2020 flow via generate_flow_diagram.R (DiagrammeR + Graphviz dot + rsvg) from analysis/prisma_counts.yaml.
- Cascade arithmetic verified: 312+6=318 identified; 318-121 dup=197 screened; 197-158=39 sought; 39-4=35 assessed; 35-22=13 included.
- Outputs: prisma_flow.{svg,png,pdf,_600.png}. SVG emitted via companion emit_prisma_svg.R (canonical script writes PDF/PNG only).
- Critic Stage 1 (critic_figure.py): prisma PASS, forest PASS, funnel(type=other) PASS. Stage 2 (visual + flow rubric): PASS.
- analysis/figures/_figure_manifest.md written (3 figures, all critic=yes/1 round).

## Step 3 — /write-paper (--autonomous, meta-analysis IMRAD)
- manuscript/manuscript.md (body ~1,651 words Intro-Discussion; abstract ~295 words) + manuscript/title_page.md.
- All numbers pulled from analysis/tables/*.csv (verified in Step 7.3a). References intentionally [UNVERIFIED] (methods demo).
- Classical-style heading conventions (uppercase+bold), numbered eligibility, no section symbols, AI disclosure on TITLE PAGE (not body).
- Phase 7 gates:
  - 7.1 classical style: 1 Minor (DECIMAL_INCONSISTENCY: "RR = 1.0" null vs 3-dp estimates) -> fixed (reworded null) -> clean.
  - 7.1 AI-disclosure meta-applicability: title-page paragraph carries version (Opus 4.8) + channel (CLI) + date (June 2026) + responsible party (the authors); 0 placeholders in body.
  - 7.1 forbidden AI phrases: 0; em-dashes: 0; section symbols: 0.
  - 7.3a numerical claim audit: 17/17 claims 3-way matched to CSVs, 0 mismatches, 0 direction reversals.
  - 7.3c reference adequacy: 2 Major (methods_zero_citations PRISMA uncited; 0 refs vs 40-80 target). ACTION: SEARCH_LIT_REQUIRED logged (autonomous-mode deferral; intentional [UNVERIFIED] demo). Uncited methods: PRISMA.
  - 7.6 DOCX build: pandoc -> manuscript_final.docx (811 KB; 3 figures embedded as media; key numbers present in body XML). EXIT 0.
  - 7.6a cross-reference QC: 4/4 labels OK (Figure 1-3, Table 1 all cited+body+docx). EXIT 0.

## Step 4 — /check-reporting (PRISMA 2020, --json)
- Fail-fast guard OK (vendored PRISMA_2020.md). Genuine item-by-item over 27 items / 42 sub-items.
- PRESENT 24, PARTIAL 6, MISSING 12, N/A 0. compliance_pct = 24/42 = 57.1% (PRESENT+PARTIAL = 30/42 = 71.4%).
- 12 MISSING are genuine demo-scope gaps: full search strategy, selection process, RoB method+per-study, GRADE method+results, heterogeneity exploration method+results, excluded-studies-with-reasons, registration/protocol/amendments. Reported honestly (not N/A).
- Step 4d PRISMA figure arithmetic: 4/4 cascade checks PASS. Step 4e framework naming: PASS.
- qc/reporting_checklist.md written.

## Step 5 — /self-review (--json --fix, max 2 iter) + v3.7.0 detectors
- Deterministic gates all PASS: classical_style, scope_coherence (conclusion matches design), claim_artifact (0 candidates), artifact_coverage (Methods/Results/disk reconciled), reviewer_team_consistency (DUAL=0 SINGLE=0 LLM=0 DEFERRED=0).
- INITIAL score 78 -> FINAL score 82. Verdict REVISE (below 85 PASS; remaining Majors are genuine PRISMA apparatus gaps, all fixable_by_ai:false). 0 fatal.
- Fix applied (1 iteration): added Protocol-and-registration paragraph (PRISMA 24a/24b now PRESENT). Re-review: all gates still clean.
- Remaining: M1 per-study RoB, M2 GRADE, M3 reference adequacy ([UNVERIFIED]), m1 heterogeneity exploration — all intentional for clean-room demo.
- qc/self_review.md + qc/_detector_findings.md written (literal detector outputs captured).

## Step 6 — DOCX
- manuscript/manuscript_final.docx via pandoc (see Step 3 7.6).

## Step 7 — manifest.lock.json
- version_dataset.py manifest over data/dat_bcg.csv + analysis/tables/{meta_results,per_study_escalc,leave_one_out}.csv (4 files), seed 42, SHA-256 + per-column hashes.
- verify --strict: OK, 4/4 files match. EXIT 0.

## NOT RUN
- check_pool_consistency.py (meta-analysis Phase 4 entry gate): NOT APPLICABLE — requires FINAL_POOL_LOCK.yaml + round-3 screening adjudication TSV, which do not exist for a built-in-dataset clean-room demo (no de novo search/screen). Demonstrated equivalent: 17-claim 3-way numerical audit + PRISMA cascade arithmetic (4/4).
- /verify-refs against real bibliography: NOT RUN — references are intentional [UNVERIFIED] placeholders per the demo brief; refs.bib is the managed-placeholder stub.

## Anti-fabrication attestation
Every quantitative claim in the manuscript was read from a CSV generated by executing R code, never typed from memory. compliance_pct (57.1%) and self-review scores (78->82) are genuine assessment outputs. No invented citations, p-values, or effect sizes. No edits outside the staging dir or medsci-skills repo. No commit/push.
