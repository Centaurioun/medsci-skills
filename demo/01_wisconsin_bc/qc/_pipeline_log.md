# Pipeline Build Log — DEMO 1 (Wisconsin Breast Cancer)
medsci-skills v3.7.0 · clean-room regeneration · 2026-06-07
Staging: <clean-room staging>/01_wisconsin_bc/

Dataset: Wisconsin Diagnostic Breast Cancer (sklearn.datasets.load_breast_cancer)
N = 569 FNA samples (212 malignant / 357 benign), 30 cytomorphometric features.
Reference standard = histopathology `diagnosis` (malignant/benign).
Stratified 70/30 split, seed 42 → train n=398, test n=171 (64 malignant / 107 benign).
Reporting target: STARD 2015.

---

## Step 0 (pre-existing) — /analyze-stats
- Status: COMPLETE (upstream; passed v3.7.0 generated-code gate)
- Key outputs: analysis/analyze.py (gate-clean), analysis/tables/*.csv, analysis/figures/{roc_curve,confusion_matrices}.{pdf,png}
- All quantitative claims below trace to analysis/tables/*.csv (read at build time, never retyped from memory).

## Step 1 — /make-figures (study-type: diagnostic-accuracy)
- Status: PASS
- Added: figures/stard_flow.{svg,png,pdf} + figures/stard_flow_600.png (STARD 2015 participant flow)
- Tool: canonical R pipeline scripts/generate_flow_diagram.R (DiagrammeR + Graphviz + rsvg); SVG vector source emitted via DiagrammeRsvg::export_svg.
- Config: figures/stard_flow.yaml (cell counts = Logistic Regression row of diagnostic_accuracy.csv).
- Arithmetic verified: TP+FP=61, FN+TN=110, TP+FN=64 (malignant), FP+TN=107 (benign), total=171;
  Sens=60/64=0.938, Spec=106/107=0.991 reproduce the CSV exactly.
- ROC (Figure 2) + confusion matrices (Figure 3) pre-existing from /analyze-stats; retained at analysis/figures/.
- Manifest: analysis/figures/_figure_manifest.md (3 figure entries) — non-empty, HALT gate satisfied.

## Step 2 — /write-paper (--autonomous, IMRAD, diagnostic-accuracy)
- Status: PASS (with one expected deferred WARN on reference count)
- Output: manuscript/manuscript.md (body Intro→Discussion ~1,091 words; full file ~1,703 words incl. abstract+legends)
           manuscript/title_page.md (AI-disclosure on title page, not in body)
- Index tests = 3 ML classifiers (logistic regression, random forest, SVM-RBF); reference standard = histopathology.
- All numbers pulled from analysis/tables/*.csv.

### Phase 7 gate results
- Step 7.1 classical-style lint (check_classical_style.py --strict): PASS (exit 0, 0 findings).
  → qc/classical_style.json. No §, no in-body AI disclosure, em-dash count 0, no decimal inconsistency.
- Step 7.1 AI-pattern scan (forbidden-phrase grep over the write-paper list): CLEAN (0 forbidden phrases).
- Step 7.3c reference-adequacy gate (check_reference_adequacy.py, article-type ai_validation): adequacy_safe=true.
  → qc/reference_adequacy.json. 0 major, 1 minor.
  - methods_zero_citations: false; uncited_named_methods: [] (Brier, DeLong, STARD, calibration all cited).
  - reference_count_verdict: BELOW_TARGET (14 cited vs 25-45 target).
  - Action: WARN (deferred). This is EXPECTED — references are intentional [UNVERIFIED] placeholders
    (methods demo, not clinical submission). Per Step 7.3c autonomous mode, BELOW_TARGET with no Methods
    named-method gap is a logged WARN, not a block. SEARCH_LIT_REQUIRED is NOT triggered (named-method
    tier clean). No references were fabricated to hit the target.

## Step 3 — /check-reporting (STARD 2015, --json)
- Status: PASS (assessment complete)
- Checklist source: vendored check-reporting/references/checklists/STARD.md (30 items; check_checklist_exists.py OK).
- STARD-AI NOT used (classical ML on tabular benchmark, not an LLM-as-outcome study); MI-CLEAR-LLM not paired.
- Framework-naming audit (check_framework_naming.py, Step 4e): CLEAN.
- Genuine item-by-item assessment → qc/reporting_checklist.md (Parts A-D) + qc/_stard_assessment.json.
- compliance_pct = PRESENT / applicable = 14 / 23 = 60.9%.
  - PRESENT 14, PARTIAL 8, MISSING 1 (item 26 registration), N/A 7 (10b/11/14/17/20/22/23).
  - N/A items are intrinsic to a public computational benchmark (no patients/procedures/timing/readers).
  - Percentage derived from the actual assessment, NOT invented.

## Step 4 — /self-review (--fix, max 2 iterations)
- Status: PASS after 1 fix iteration (limit 2, not exhausted)
- Output: qc/self_review.md + qc/_detector_findings.md (literal detector captures).
- Scores: initial 82 (REVISE) → final 88 (PASS). Major 1→0, Minor 1→1.
- Deterministic detectors (v3.7.0):
  - check_classical_style.py: CLEAN (0 findings).
  - check_cohort_arithmetic.py: CLEAN (split + 2×2 cell sums consistent).
  - check_reference_adequacy.py: 0 major / 1 minor (BELOW_TARGET 14<25-45; deliberate placeholder, fixable_by_ai:false).
  - check_scope_coherence.py: CLEAN (no CROSS_SECTIONAL_PROGNOSTIC / SURROGATE_CARE_DIRECTIVE).
  - check_artifact_coverage.py: 1 MAJOR (DISK_UNREPORTED: predictions.csv) → FIXED → CLEAN on re-run.
- Fix applied: Data Availability sentence releasing predictions.csv (per-sample probabilities) for independent recompute.
- Final deterministic state: 0 Major, 1 Minor (reference count, by design).

## Step 5 — Build manuscript_final.docx (pandoc)
- Status: PASS
- Tool: pandoc 3.9.0.2 (markdown → docx); title_page.md + \newpage + manuscript.md combined.
- Output: manuscript/manuscript_final.docx (17 KB).
- Verified docx body XML contains key numbers (0.998, 0.554, n = 171, TP = 60, Brier).

## Step 6 — Reproducibility lock (version_dataset.py, seed 42)
- Status: PASS
- manifest build: 5 files (data/*.csv + analysis/tables/*.csv), --seed 42, --base . → manifest.lock.json
  (content SHA-256 + per-column hashes + row/col counts per file).
- verify --strict: "OK: 5 file(s) match the manifest." exit 0.
- manifest.lock.json own SHA-256: 9b9001c15f37b23ae4b870f98777e07cb6489af57aca04ce72b15710541b1fc1
- data/wisconsin_breast_cancer.csv sha256: a33e4b101199ada24b7f416758a3b761a5978a1983191a58b89264c428a26726 (569×32)

## Step 7 — Pipeline log
- This file. All 7 steps logged; every quantitative claim traced to analysis/tables/*.csv.

---

## Anti-fabrication attestation
- Every number in manuscript.md was read from a CSV under analysis/tables/ at build time
  (diagnostic_accuracy.csv, auc_comparison_delong.csv, table1_features_by_class.csv, predictions.csv),
  never retyped from memory. STARD 2×2 cells recompute to the CSV Sens/Spec exactly.
- compliance_pct (60.9%) and self-review scores (82→88) are the genuine output of the actual
  item-by-item / detector assessments; no target was invented.
- References are intentional [UNVERIFIED] placeholders (methods demo) — none fabricated.
- No step returned "NOT RUN": all 7 steps executed.
