---
name: periodontology-research
description: >
  Experimental Layer-D periodontology domain skill. Applies periodontal, peri-implant, dental,
  and oral-systemic research constraints to terminology, measurement hierarchy, study interpretation,
  and handoff decisions without replacing MedSci's existing design, statistics, evidence, figure,
  writing, review, or reporting owners.
triggers: periodontology research, periodontal study, periodontitis research, gingivitis research, peri-implant research, periodontal measurements, probing depth, clinical attachment, bleeding on probing, patient tooth site hierarchy, oral-systemic periodontal framing
tools: Read, Write, Edit, Grep, Glob
model: inherit
---

# Periodontology Research Skill

## Purpose

Use this skill to apply **periodontal and peri-implant domain constraints** to a
research task before or alongside the existing MedSci procedural owners.

It is a thin domain layer, not a second research engine.

```text
periodontal / peri-implant domain question
        ↓
periodontology-research
        ↓
domain decision notes
        ↓
existing owner: design-study / analyze-stats / make-figures /
                check-reporting / write-paper / self-review / peer-review
```

The detailed reusable profile is:

`references/periodontology-domain-profile.md`

---

## When This Skill Activates

Use `/periodontology-research` when domain knowledge materially changes one or
more of the following:

- periodontal or peri-implant terminology;
- case/construct interpretation;
- measurement meaning;
- patient → tooth/implant → site → visit hierarchy;
- full-mouth versus sampled-site interpretation;
- changing denominators across visits;
- treatment-response framing;
- oral-systemic interpretation;
- periodontal-specific design/confounding cues;
- manuscript consistency across Methods, Results, figures/tables, Discussion,
  and Conclusion.

Typical prompts include:

```text
Review the periodontal constructs in this study.
Check whether these site-level results support the patient-level conclusion.
Audit the periodontal measurement and denominator logic.
Review the peri-implant terminology in this manuscript.
Check the oral-systemic periodontal framing for overreach.
Apply a periodontal domain check before the statistical analysis.
```

---

## When NOT to Use

Do not activate merely because a medical study mentions oral health or dentistry.
Do not use this skill as a substitute for:

- literature discovery → `/search-lit`;
- reference/source audit → `/verify-refs`;
- generic design/validity adjudication → `/design-study`;
- statistical computation/model choice → `/analyze-stats`;
- scientific figure generation → `/make-figures`;
- reporting-guideline audit → `/check-reporting`;
- manuscript drafting → `/write-paper`;
- own-manuscript review → `/self-review`;
- external peer review → `/peer-review`.

If the right procedural owner is already obvious and no periodontal domain
interpretation is needed, call that owner directly.

---

## Authority Boundary

This skill owns only:

```text
periodontal/peri-implant terminology fidelity
+ domain construct distinctions
+ measurement/hierarchy interpretation
+ domain-specific plausibility and inference warnings
+ domain-specific handoff decisions
```

It does **not** own:

```text
statistical inference
study-design authority
source/evidence verification
citation authorization
figure generation
reporting completeness
manuscript authorship
canonical persistence
```

Domain expertise cannot turn an unverified statement into evidence.

---

## Required Inputs

Use the smallest available context sufficient for the domain question. Useful
inputs may include:

- study question or aims;
- protocol or Methods excerpt;
- variable definitions / codebook;
- visit schedule and treatment description;
- outcome definitions;
- analysis/result summary;
- table or figure;
- Discussion/Conclusion excerpt;
- manuscript section requiring domain consistency review.

Do not require a fixed project layout when a bounded excerpt is enough.

When a material domain fact is missing, record the missing input rather than
infer it.

---

## Operating Workflow

### Step 1 — Identify domain-sensitive constructs

List only the periodontal/peri-implant constructs that matter to the task.
Examples may include:

- health / gingivitis / periodontitis;
- staging or grading labels when actually used;
- peri-implant health / mucositis / peri-implantitis;
- probing depth;
- clinical attachment level/loss;
- bleeding on probing;
- plaque/gingival measures;
- tooth loss or missing teeth;
- treatment phase and follow-up;
- oral-systemic variables.

Preserve the study's own operational definition. If a current guideline,
threshold, or classification definition is required, flag it for source-backed
verification rather than treating this skill's memory as authority.

### Step 2 — Map the measurement hierarchy

Reconstruct the relevant structure:

```text
patient
  -> tooth / implant
      -> site
          -> visit / timepoint
```

For each important variable, identify its level and whether it is repeated.
Flag:

- site/tooth observations treated as independent patients;
- patient-level conclusions from lower-level descriptive data;
- unrecorded aggregation rules;
- unstable denominators caused by missing/extracted teeth or unavailable sites;
- full-mouth claims based on a sampled protocol without justification.

Do not choose the statistical correction yourself. Send model/estimand questions
to `/analyze-stats`.

### Step 3 — Check measurement and longitudinal meaning

Inspect whether the interpretation distinguishes:

- baseline state;
- treatment exposure;
- post-treatment response;
- longer follow-up/maintenance;
- within-patient change;
- between-group difference;
- between-group difference in change.

Keep statistical significance separate from clinical importance.

### Step 4 — Surface domain-specific design/confounding cues

When relevant, identify issues such as:

- smoking/tobacco exposure;
- baseline periodontal severity;
- prior periodontal treatment/maintenance;
- oral-hygiene behavior or co-intervention;
- systemic conditions/medications;
- site/tooth/disease-severity selection;
- changing denominators;
- oral-systemic causal overreach.

This is a cueing layer. `/design-study` owns the general validity/confounding
adjudication and `/analyze-stats` owns the formal statistical treatment.

### Step 5 — Check interpretation and terminology consistency

Flag:

- gingivitis/periodontitis conflation;
- periodontal/peri-implant conflation;
- disease presence/severity/progression/response conflation;
- site-level findings promoted to patient-level claims;
- surrogate periodontal measures promoted to patient-centered benefit without
  evidence;
- causal language unsupported by the design;
- terminology drift between Methods, Results, tables/figures, Discussion, and
  Conclusion.

### Step 6 — Hand off to the existing owner

Use the handoff matrix rather than solving an adjacent procedure inside this
skill.

| Need | Route |
|---|---|
| design, validity, confounding, causal framing | `/design-study` |
| estimand, clustering, repeated measures, model, CI/test | `/analyze-stats` |
| scientific visualization | `/make-figures` |
| reporting guideline/checklist | `/check-reporting` |
| manuscript drafting | `/write-paper` |
| own-manuscript critical review | `/self-review` |
| external manuscript review | `/peer-review` |
| literature discovery | `/search-lit` |
| existing-reference audit | `/verify-refs` |

For multi-step tasks, return the domain notes first so `/orchestrate` can pass
them to the procedural owner.

---

## Standard Output

Return bounded decision notes:

```text
## Periodontology Domain Notes

Context / task:
- ...

Relevant constructs:
- ...

Terminology / definition issues:
- ...

Measurement level and denominator:
- patient / tooth / implant / site / visit
- ...

Longitudinal / treatment interpretation:
- ...

Domain-specific design or confounding cues:
- ...

Clinical interpretation constraints:
- ...

Required handoff:
- owner skill: ...
- question for owner: ...

Uncertainty / missing inputs:
- ...
```

Use `not material` for irrelevant headings. Do not invent findings merely to
populate the template.

---

## Evidence Discipline

When a domain statement depends on external evidence — for example a case
definition, classification rule, measurement threshold, prevalence estimate,
treatment effect, prognosis, or oral-systemic association — treat the statement
as evidence-dependent.

This skill may identify what needs verification; it does not authorize the
claim or citation.

When consumed through Academic Research, preserve the existing authority chain:

```text
ZotSeek              -> discovery candidates
Zotero Local         -> source identity and bounded evidence
MedSci owner skill   -> scientific procedure
Academic Write Coordinator -> write routing
Manuscript Forge Production -> persistence
```

Do not widen those boundaries.

---

## Anti-Hallucination

- Never invent periodontal or peri-implant diagnoses, staging/grading assignments,
  case definitions, thresholds, treatment history, patient/tooth/site counts, or
  source claims that were not supplied or verified.
- Never convert domain plausibility into evidence. A clinically plausible statement
  remains unverified until the relevant source/evidence owner establishes support.
- If a guideline version, classification rule, threshold, or case definition is
  required but not verified, mark it `NEEDS_SOURCE_VERIFICATION` rather than
  supplying a remembered value as authoritative.
- If the patient → tooth/implant → site → visit hierarchy, denominator, treatment
  exposure, or measurement protocol is materially missing, return
  `CANNOT_DETERMINE` or a missing-input note instead of filling the gap.
- Do not infer statistical results, causal effects, clinical significance, or
  treatment benefit from domain terminology alone; hand those questions to the
  existing procedural owner.

---

## Uncertainty and Failure Behavior

Return an explicit uncertainty or `CANNOT_DETERMINE` when interpretation depends
on missing material information, including:

- classification/case definition;
- measurement protocol;
- site/tooth/patient denominator;
- visit timing;
- treatment exposure/adherence;
- prior periodontal therapy;
- smoking/systemic/medication status;
- statistical model/estimand;
- source support for a domain claim.

Do not convert missing data into a reassuring default.

---

## Side Effects

Layer-D behavior only:

- decision notes/annotations are allowed;
- direct canonical manuscript/analysis rewrites are not owned here;
- no references are generated from memory;
- no source verification is claimed;
- no statistical computation is claimed.

---

## Maturity

`experimental`

This initial profile is intentionally experimental. It should accumulate real
use before any later promotion to a stronger maturity claim.
