## Reporting Guideline Compliance Report

Manuscript: Efficacy of BCG Vaccination Against Tuberculosis: A Random-Effects Meta-Analysis of 13 Randomized Trials
Guideline: PRISMA 2020 (27 items / 42 sub-items)
Date: 2026-06-07
Assessed by: Claude (automated pre-screening, medsci-skills v3.7.0 /check-reporting)

> Note: This is a clean-room methods demonstration of the medsci-skills pipeline.
> The 13 included randomized trials and all event counts are genuine; the upstream
> PRISMA record counts are illustrative, and references are [UNVERIFIED] placeholders.
> PRISMA items that depend on a real de novo systematic-review workflow (full search
> strategy, dual-reviewer screening, per-study risk of bias, GRADE certainty,
> registration) are therefore genuinely MISSING. This is expected for the demo and
> reported honestly rather than marked N/A.

### Summary

| Status | Count | Percentage |
|--------|-------|------------|
| PRESENT | 24 | 57.1% |
| PARTIAL | 6 | 14.3% |
| MISSING | 12 | 28.6% |
| N/A | 0 | 0% |
| **Total** | **42** | **100%** |

Overall compliance (PRESENT / applicable): 24/42 = 57.1%
(PRESENT + PARTIAL / applicable = 30/42 = 71.4%)

### Detailed Checklist

| # | Section | Item | Status | Location | Notes |
|---|---------|------|--------|----------|-------|
| 1 | Title | Identify as systematic review/meta-analysis | PRESENT | Title | "A Random-Effects Meta-Analysis of 13 Randomized Trials" |
| 2 | Abstract | Structured summary | PRESENT | Abstract | Background/Methods/Results/Conclusion; registration not applicable (demo) |
| 3 | Introduction | Rationale | PRESENT | Introduction P1-P2 | TB burden, variable BCG efficacy, latitude/mycobacteria covariates |
| 4 | Introduction | Objectives (PICO) | PRESENT | Introduction P3 | Pooled relative effect + heterogeneity characterization |
| 5 | Methods | Eligibility criteria | PRESENT | Methods (Eligibility) | Numbered (1)-(3) inclusion criteria |
| 6 | Methods | Information sources | PARTIAL | Methods (Study design) | Canonical dataset cited; illustrative upstream sources; no search dates |
| 7 | Methods | Search strategy (full) | MISSING | - | No full search strategy (methods demo; not de novo search) |
| 8 | Methods | Selection process | MISSING | - | No reviewer count/independence (illustrative cascade only) |
| 9 | Methods | Data collection process | PARTIAL | Methods (Statistical analysis) | 2x2 cell extraction described; reviewer count not stated |
| 10a | Methods | Data items (outcomes) | PRESENT | Methods (Outcome) | Incident TB defined as the outcome |
| 10b | Methods | Data items (other variables) | PARTIAL | Methods | Cell counts + latitude available; covariate handling not detailed |
| 11 | Methods | Risk of bias assessment method | MISSING | - | No RoB tool described for the trials |
| 12 | Methods | Effect measures | PRESENT | Methods (Outcome and effect measure) | Risk ratio (RR), RR<1 = protective |
| 13a | Methods | Synthesis: eligibility per synthesis | PRESENT | Methods (Statistical analysis) | Single synthesis (13 trials, one outcome) |
| 13b | Methods | Synthesis: data preparation | PRESENT | Methods | Log RR + variance from 4 cell counts |
| 13c | Methods | Synthesis: tabulation/display | PRESENT | Methods + Figure Legends | Forest plot + per-trial table |
| 13d | Methods | Synthesis: model + heterogeneity + software | PRESENT | Methods (Statistical analysis) | Random-effects REML; I2/tau2/Q; metafor + meta packages named |
| 13e | Methods | Methods to explore heterogeneity causes | MISSING | - | No subgroup/meta-regression (noted out of scope) |
| 13f | Methods | Sensitivity analyses | PRESENT | Methods (Statistical analysis) | Leave-one-out described |
| 14 | Methods | Reporting bias assessment method | PARTIAL | Methods (Statistical analysis) | Egger + rank test described; not framed as missing-results synthesis |
| 15 | Methods | Certainty assessment (GRADE) | MISSING | - | No GRADE/certainty framework |
| 16a | Results | Study selection (flow diagram) | PRESENT | Results + Figure 1 | PRISMA flow; cascade arithmetic verified (318->197->39->35->13) |
| 16b | Results | Excluded studies cited with reasons | MISSING | - | Excluded studies not individually cited (illustrative cascade) |
| 17 | Results | Study characteristics, each cited | PARTIAL | Results + Table 1 | Per-trial counts in Table 1; trials not individually cited ([UNVERIFIED] refs) |
| 18 | Results | Risk of bias per study | MISSING | - | No per-study RoB presented |
| 19 | Results | Results of individual studies (summary stats + effect + precision) | PRESENT | Table 1 + Figure 2 | Per-trial cell counts, RR, 95% CI in Table 1 and forest plot |
| 20a | Results | Synthesis: characteristics + RoB of contributing studies | PARTIAL | Results (Pooled effect) | Characteristics summarized; RoB absent |
| 20b | Results | Synthesis: summary estimate + precision + heterogeneity + direction | PRESENT | Results (Pooled effect, Heterogeneity) | RR 0.489 (0.344-0.696); I2 92.2%; tau2 0.313; Q=152.23; protective |
| 20c | Results | Investigations of heterogeneity causes | MISSING | - | No subgroup/meta-regression performed |
| 20d | Results | Sensitivity analyses results | PRESENT | Results (Sensitivity) | Leave-one-out RR 0.452-0.533, all CIs exclude 1 |
| 21 | Results | Reporting biases assessment results | PRESENT | Results (Small-study effects) + Figure 3 | Egger z=-1.40 p=0.189; rank tau=0.026 p=0.952; funnel plot |
| 22 | Results | Certainty of evidence results | MISSING | - | No GRADE results |
| 23a | Discussion | General interpretation in context | PRESENT | Discussion P1-P2 | Average-protective + heterogeneity-dominant interpretation |
| 23b | Discussion | Limitations of the evidence | PRESENT | Discussion (Limitations) | Heterogeneity unexplained; multi-decade trials; strain/dose/ascertainment |
| 23c | Discussion | Limitations of review processes | PRESENT | Discussion (Limitations) | Methods-demo single dataset; illustrative selection; no moderator analysis |
| 23d | Discussion | Implications for practice/policy/research | PRESENT | Discussion (Clinical implications + summary) | Local-estimation message; moderator analysis future work |
| 24a | Other | Registration (name + number, or not registered) | MISSING | - | Not registered; not explicitly stated as unregistered in body |
| 24b | Other | Protocol access | MISSING | - | No protocol prepared/cited |
| 24c | Other | Amendments | MISSING | - | No registration/protocol to amend; not explicitly stated |
| 25 | Other | Support/funding | PARTIAL | Title page | Funding [UNVERIFIED] placeholder on title page; not in body |
| 26 | Other | Competing interests | PRESENT | Title page | COI declared (placeholder: none for demo) on title page |
| 27 | Other | Availability of data, code, materials | PRESENT | Title page (Data availability) | dat.bcg + analysis scripts/tables/figures available; open dataset |

### Action Items (Priority Order)

1. [MISSING] Item 7/8: Full search strategy + selection process. Production review needs the full database search string and dual-reviewer screening. Not applicable to this clean-room demo (no de novo search); flagged honestly.
2. [MISSING] Item 11/18: Risk of bias (method + per study). Add RoB 2 assessment of the 13 randomized trials.
3. [MISSING] Item 15/22: GRADE certainty of evidence for the TB-incidence outcome.
4. [MISSING] Item 13e/20c: Heterogeneity exploration. With I2=92.2%, meta-regression on latitude (ablat) is the natural addition; out of scope for demo.
5. [MISSING] Item 24a/24b/24c: Registration/protocol. State explicitly that the review was not registered and no protocol prepared.
6. [PARTIAL] Item 17: Cite each included study. Resolve [UNVERIFIED] reference placeholders so each of the 13 trials is individually cited.
7. [PARTIAL] Item 25: Support/funding. Move funding statement from title-page placeholder into a body Funding section.

### Section Boundary Check

- Results: factual findings only; no interpretation, no prior-literature comparison, no unquantified evaluative adjectives. PASS.
- Discussion: no new data beyond Results; interpretation matches evidence level (prediction interval crossing null acknowledged). PASS.

### Step 4d: PRISMA Figure 1 Arithmetic & Cross-Reference Audit

- check1 records screened = identified - duplicates: PRESENT (318 - 121 = 197)
- check2 sought = screened - excluded: PRESENT (197 - 158 = 39)
- check3 assessed = sought - not retrieved: PRESENT (39 - 4 = 35)
- check4 included = assessed - excluded: PRESENT (35 - 22 = 13)
- Body<->figure cross-reference: "13 randomized trials (357,347 participants)" agrees across Results, Table 1 source, Figure 1. PRESENT.
- Manifest cross-ref: _figure_manifest.md flow-diagram row Critic=yes, path agrees. PRESENT.

### Step 4e: Reporting-Framework Naming Audit

- PRISMA 2020 named cleanly; no base/extension mismatch, no +AI/-AI hyphen confusion, no self-coined item labels, no vague "recent guidance". PASS (qc/framework_naming.json).

```json
{
  "check_reporting_version": "1.0",
  "manuscript_title": "Efficacy of BCG Vaccination Against Tuberculosis: A Random-Effects Meta-Analysis of 13 Randomized Trials",
  "guideline": "PRISMA 2020",
  "guideline_version": "2020",
  "date": "2026-06-07",
  "total_items": 42,
  "present": 24,
  "partial": 6,
  "missing": 12,
  "na": 0,
  "compliance_pct": 57.1,
  "compliance_present_or_partial_pct": 71.4,
  "prisma_figure_arithmetic": "PASS (4/4 cascade checks)",
  "framework_naming": "PASS",
  "demo_note": "Clean-room methods demo; full-search/RoB/GRADE/registration items genuinely MISSING (not de novo review); references [UNVERIFIED]."
}
```

---

### Post-self-review update (after /self-review --fix)

The /self-review --fix pass (Step 5) inserted a "Protocol and registration" paragraph into
Methods, explicitly stating the review was not registered and no protocol was prepared. This
moves PRISMA items 24a (Registration) and 24b (Protocol access) from MISSING to PRESENT.

Updated tally: PRESENT 26, PARTIAL 6, MISSING 10, N/A 0.
Updated compliance: 26/42 = 61.9% (PRESENT); 32/42 = 76.2% (PRESENT+PARTIAL).

The body table above reflects the as-assessed state at check-reporting run time (57.1%);
this note records the post-fix state for accuracy. Item 24c (amendments) remains MISSING-but-
N/A in spirit (no registration to amend); it is left MISSING since the body does not say so.
