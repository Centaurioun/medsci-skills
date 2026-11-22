# QUADAS-3 (2026) — DTA Risk-of-Bias and Applicability Routing Guide

> **Navigation and recording aid; NOT the complete official QUADAS-3 instrument.**
> Do not reconstruct, infer, paraphrase into substitute questions, or auto-score the
> official signalling questions from this abbreviated guide. Obtain the current
> official form (University of Bristol; version 1.2 as listed on 2026-11-22)
> and the explanation-and-elaboration document before starting an assessment.

## Sources and scope

- Official tool and latest document: https://www.bristol.ac.uk/population-health-sciences/projects/quadas/quadas-3/quadas-3-tool/
- Whiting PF, Tomlinson E, Rutjes AWS, et al. QUADAS-3: A revised tool for the quality assessment of diagnostic test accuracy studies. *Ann Intern Med*. 2026;179(4):548–555. doi:10.7326/ANNALS-25-02104.
- Davenport CF, Rutjes AWS, Mallett S, et al. QUADAS-3 explanation and elaboration. *Ann Intern Med*. 2026;179:e2504943. doi:10.7326/ANNALS-25-04943.
- Use for risk-of-bias and applicability judgements **within a systematic review of primary diagnostic test accuracy evidence** (diagnosis, screening, staging).
- This is **not** a reporting guideline. Use PRISMA-DTA for the systematic-review report and STARD/STARD-AI for primary-study reporting, when applicable.
- QUADAS-2 remains available for pre-specified historical protocols, comparisons or otherwise justified legacy assessments. Do not silently mix QUADAS-2 and QUADAS-3 results or assume QUADAS-C is validated as a direct add-on to QUADAS-3. Document any tool change as a protocol decision.

## Six-phase workflow and assessment granularity

| Phase | Unit | Required working record |
|---|---|---|
| 1. Synthesis questions | Review / synthesis question | PIRD question ID, population, index test, target condition, intended clinical role, threshold/setting |
| 2. Ideal test accuracy trial | Per synthesis question | Prespecified ideal comparison, participants, target condition, test procedures, plausible bias mechanisms |
| 3. Flow diagram | Each study | How participants, tests, target condition assessment, and missing/uninterpretable results flow |
| 4. Accuracy estimates to assess | Each study | **Estimate ID** for each threshold, subgroup, condition and metric set; source figure/table/page |
| 5. Domain judgements | **Each selected accuracy estimate** | Source evidence, official signalling-question answers, four domain judgements + applicability for first three, rationale, assessed by/adjudication |
| 6. Overall judgement | **Each selected accuracy estimate** | Explicit overall risk-of-bias and applicability judgements, supporting reasons, unresolved information |

Phase 5 risk-of-bias domains (names from official tool):
1. **Participants**
2. **Index test**
3. **Target condition**
4. **Analysis**

Applicability is separately considered for the first three domains in relation to the review synthesis question and ideal test accuracy trial. The assessment is **estimate-level, not one judgement per publication**. Do not collapse multiple test thresholds or different study populations into one undifferentiated study-level rating.

## Suggested output record (original local interoperability schema)

Each output row should contain at minimum:

```text
review_id, synthesis_question_id, ideal_trial_ref, study_id, accuracy_estimate_id,
index_test, target_condition, threshold_or_subgroup, source_attachment_or_doi,
source_locator, participant_flow_ref, assessor_id, domain, official_form_version,
official_signalling_answers_ref, risk_of_bias_judgement, applicability_judgement,
evidence_excerpt_or_locator, rationale, uncertainty, adjudication_status,
overall_risk_of_bias, overall_applicability, assessment_date
```

The row schema is a **local proposal**, not an official QUADAS-3 machine-readable form.
Use the exact official judgement categories and signalling-question text **from the current
form**. If the original form, full text or necessary estimate-level information is absent,
record **UNASSESSED / INSUFFICIENT_SOURCE** rather than a fabricated answer.
Where no estimate-level result is available, do not claim to have completed QUADAS-3.

### Human authority and data fidelity

The reviewer team makes/approves individual judgements. AI may organise excerpts and
surface missing details, but does not replace the official instrument or independent
reviewer adjudication. Preserve source locations, disagreements, and revision history.
Any canonical saved project artifact must use the existing governed writer; this
guide has no authority to write to Zotero or a manuscript file.

## Copyright/provenance

This guide is newly written navigation text based on public methodological descriptions.
It **does not reproduce** the official form's copyrighted signalling-question list.
Do not distribute the official QUADAS-3 form as a bundled file without explicit
license/permissions clearance. Cite the primary publication and use the official source.
