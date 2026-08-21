# Periodontology Research Domain Profile

This reference supplies **domain constraints** for `/periodontology-research`.
It is not a statistics manual, evidence authority, reporting checklist, or
manuscript-writing procedure. Use it to keep periodontal and peri-implant
constructs, measurement levels, clinical interpretation, and handoffs coherent.

## 1. Scope and terminology

### Periodontal constructs

Treat the following as distinct constructs unless the study's cited definition
explicitly establishes a different relationship:

- periodontal health;
- gingival inflammation / gingivitis;
- periodontitis;
- periodontal disease severity/extent;
- periodontal treatment status and treatment response.

Do not silently convert one construct into another. In particular:

- gingivitis is not a synonym for periodontitis;
- a periodontal index value is not itself a complete disease diagnosis unless
  the study's operational definition makes it so;
- disease presence, severity, extent, progression/risk, and treatment response
  are different claims and may require different variables and estimands.

When staging, grading, case definitions, thresholds, or classification-system
labels matter, preserve the exact system used by the study and verify its current
source. Do not freeze one guideline edition or threshold as timeless domain
truth inside this profile.

### Peri-implant constructs

Keep peri-implant health, peri-implant mucositis, and peri-implantitis distinct
from each other and from tooth-based periodontal constructs. Do not transfer a
tooth-level definition, measurement convention, or treatment-response claim to
an implant without explicit justification.

### Common periodontal measurements

Use measurement names precisely and preserve the study's operational definition.
Typical concepts include:

- probing pocket/probing depth (PPD/PD);
- clinical attachment level/loss (CAL);
- bleeding on probing (BOP/BoP);
- plaque indices and plaque presence;
- gingival indices / gingival inflammation measures;
- recession and other site-level measurements when collected;
- tooth loss / missing teeth when relevant to the research question.

These variables are not interchangeable. A change in one does not automatically
imply equivalent change in another, and a surrogate periodontal measure should
not be promoted to a patient-centered benefit without supporting evidence.

### Treatment and follow-up terminology

Separate:

```text
baseline disease state
-> treatment exposure / treatment phase
-> post-treatment assessment
-> longer-term maintenance / follow-up
```

State the actual intervention and timing. Do not infer treatment completion,
adherence, maintenance, or sustained benefit from an isolated post-treatment
measurement.

### Oral-systemic framing

Periodontal and systemic variables may be associated through multiple pathways,
shared determinants, treatment effects, selection, and measurement processes.
Do not treat an observed oral-systemic association as evidence that periodontal
disease caused a systemic outcome or that periodontal treatment caused systemic
improvement unless the design and evidence support that claim.

---

## 2. Hierarchy and analysis-unit traps

Periodontal datasets commonly contain nested and repeated measurements:

```text
patient
  -> tooth / implant
      -> site
          -> repeated visit / timepoint
```

The domain review must identify which level each variable belongs to and which
level the scientific claim targets.

### Required questions

For every material outcome/exposure, ask:

1. Is it defined at patient, tooth/implant, site, or visit level?
2. Was it measured once or repeatedly?
3. Was a site-level variable summarized to tooth or patient level? How?
4. Does the denominator change across visits because teeth/sites are missing,
   extracted, restored, or otherwise unavailable?
5. Does the manuscript make a patient-level claim from a lower-level descriptive
   result without a model/estimand that supports that generalization?
6. Are multiple sites/teeth from the same patient being treated as independent?

### Domain boundary

`/periodontology-research` identifies the hierarchy and the risk. It does **not**
choose or compute the statistical model. Hand clustering, repeated-measures,
multilevel, denominator, estimand, and inference questions to `/analyze-stats`.

---

## 3. Measurement and longitudinal interpretation

### Baseline and follow-up

Preserve the study's actual time origin and visit schedule. Distinguish:

- cross-sectional between-group differences;
- within-patient change;
- between-group difference in change;
- short-term treatment response;
- longer-term maintenance or recurrence.

Do not describe a single follow-up difference as a longitudinal treatment effect
without the design/analysis needed to support that interpretation.

### Full-mouth versus sampled measurements

Record whether outcomes were based on:

- full-mouth assessment;
- selected teeth;
- selected sites;
- index teeth;
- a study-specific sampling protocol.

A sampled-site estimate should not silently become a full-mouth claim. If the
sampling frame changes over time, flag the interpretation risk.

### Changing denominators

Common causes include:

- tooth extraction or loss;
- absent/missing teeth at baseline;
- site-level non-recording;
- implant/tooth replacement;
- visit-specific measurement availability.

Report whether percentages and means use a stable or changing denominator.
Changing denominators can alter apparent improvement even when the underlying
clinical process is unchanged.

### Repeated measures and non-independence

Repeated visits, multiple teeth, and multiple sites create dependence cues.
Domain review should surface them before interpretation. `/analyze-stats` owns
formal handling of covariance, multilevel structure, repeated measures, and
uncertainty.

### Clinical versus statistical significance

A statistically detectable difference is not automatically clinically
important. Conversely, a clinically relevant change may be estimated imprecisely.
Keep effect magnitude, uncertainty, baseline severity, measurement scale, and
clinical meaning visible rather than equating `p < 0.05` with clinical benefit.

### Treatment response

Before describing improvement, ask:

- which metric changed;
- from what baseline;
- at which level (site/tooth/patient);
- over what interval;
- whether the same denominator/population was followed;
- whether the comparison is within-group or between-group;
- whether concomitant care or behavior could contribute.

---

## 4. Design and confounding cues

The domain profile flags periodontal-specific concerns; `/design-study` owns the
general methodological adjudication.

### Common cues to inspect

#### Smoking and tobacco exposure

Smoking/tobacco exposure may materially affect periodontal status, treatment
response, and systemic outcomes. Check whether it is part of eligibility,
descriptive balance, adjustment, stratification, or an acknowledged limitation
when relevant.

#### Baseline disease severity

Baseline severity can influence both achievable change and apparent treatment
response. Flag major imbalance, restricted severity ranges, or interpretations
that ignore baseline status. Regression-to-the-mean is a methodological concern
to hand to `/design-study` and `/analyze-stats` when applicable.

#### Prior periodontal treatment and maintenance

Prior therapy, recent debridement, maintenance attendance, antibiotic exposure,
and relevant adjunctive treatment can change the meaning of baseline and
follow-up measurements. Do not infer treatment-naive status when it is not given.

#### Oral-hygiene behavior

Oral-hygiene instruction, adherence, plaque control, professional care, and
behavioral changes may be part of the intervention or a co-intervention. Keep
that distinction visible.

#### Systemic conditions and medications

Relevant systemic disease and medications may affect inflammation, healing,
bleeding, periodontal status, or study eligibility. The domain skill should flag
plausible relevance but must not invent undocumented diagnoses, medication use,
or causal effects.

#### Site and severity selection

Check whether the study selects:

- worst sites;
- diseased teeth only;
- specific tooth types;
- index teeth;
- implants with disease;
- patients above a severity threshold.

Selection can change the target population and the meaning of subsequent
improvement. Do not generalize beyond the sampled structure without justification.

#### Oral-systemic causal overreach

For observational oral-systemic studies, distinguish:

```text
association
!= temporal ordering
!= mediation
!= causal effect
!= treatment benefit
```

Ask `/design-study` to adjudicate confounding, temporality, selection, collider,
mediation, or causal-identification questions. Ask `/analyze-stats` to adjudicate
the corresponding estimand/model.

---

## 5. Writing and interpretation constraints

Flag the following before text is handed to `/write-paper`, `/self-review`, or
`/peer-review`:

### Level-of-analysis promotion

Do not write a patient-level conclusion when the supporting result is only a
site- or tooth-level descriptive finding unless the analysis supports the
patient-level estimand.

### Surrogate promotion

Do not translate improvement in plaque, BOP, PD/PPD, CAL, or another periodontal
measure directly into improved quality of life, reduced systemic events, or
other patient-centered outcomes unless those outcomes were measured and the
evidence supports the connection.

### Causal promotion

Avoid causal verbs for uncontrolled or non-causal observational associations.
Match claim force to design and analysis.

### Terminology drift

Use the same construct names and operational meanings across:

```text
Abstract
Methods
Results
Tables/Figures
Discussion
Conclusion
```

If the Methods defines one disease/measurement construct and the Discussion uses
a broader label, flag the drift.

### Periodontal versus peri-implant conflation

Do not merge tooth-based and implant-based disease, measurements, or treatment
response into one construct unless the study explicitly defines and justifies a
combined estimand.

### Absence of evidence

Do not infer periodontal health, disease absence, treatment success, or lack of
progression from an unmeasured or unavailable variable. Missing clinical facts
remain missing.

---

## 6. Domain decision-note contract

A useful `/periodontology-research` output should be compact and inspectable:

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

Do not add a result simply to fill every heading. Mark a section `not material`
when appropriate.

---

## 7. Handoff matrix

| Domain issue identified | Existing owner / next skill |
|---|---|
| Study design, validity, confounding, causal framing | `/design-study` |
| Statistical estimand, clustering, repeated measures, model, CI/test | `/analyze-stats` |
| Figure choice or scientific visualization | `/make-figures` |
| Reporting guideline/checklist completeness | `/check-reporting` |
| Manuscript drafting | `/write-paper` |
| Own-manuscript critical review | `/self-review` |
| External manuscript review | `/peer-review` |
| Literature discovery | `/search-lit` |
| Existing-reference audit | `/verify-refs` |

For multi-step requests, `/orchestrate` may call `/periodontology-research` to
surface domain constraints and then route the actual procedural work to the
owner above.

---

## 8. Evidence and authority boundaries

Periodontology expertise does not make a statement citable and does not verify a
source. When a claim depends on a classification definition, guideline,
measurement threshold, prevalence, treatment effect, or other external evidence,
use the relevant literature/reference workflow and preserve source provenance.

When this skill is consumed through **Academic Research**:

```text
candidate discovery -> ZotSeek
source/evidence verification -> Zotero Local
scientific procedure -> existing MedSci owner
write routing -> Academic Write Coordinator
persistence -> Manuscript Forge Production
```

The domain profile cannot widen any of those authorities.

---

## 9. Uncertainty behavior

Return `CANNOT_DETERMINE` or an explicit missing-input note rather than guessing
when a material interpretation depends on unavailable information such as:

- the case definition/classification system;
- measurement level or sampling protocol;
- denominator at a visit;
- treatment exposure/adherence;
- timing of measurements;
- prior periodontal care;
- smoking/systemic/medication status;
- statistical estimand/model;
- source support for a domain-specific claim.

Domain expertise should narrow ambiguity, not conceal it.
