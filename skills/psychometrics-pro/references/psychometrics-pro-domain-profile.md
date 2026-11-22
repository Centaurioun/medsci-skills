# Psychometrics / PRO Domain Profile

This reference supplies **measurement-science constraints** for
`/psychometrics-pro`. It is not a statistics manual, evidence authority,
translation engine, questionnaire database, or manuscript-writing procedure.
Use it to keep constructs, instruments, measurement properties, score meaning,
claim force, and handoffs coherent.

## 1. Construct, instrument, population, and intended use

Always separate these concepts before interpreting psychometric evidence:

```text
construct / outcome concept
instrument / PROM
item / subscale / total score
target population
language / cultural version
intended use
measurement property
```

A **PRO** is a patient-reported outcome concept or endpoint family. A **PROM** is
an instrument used to measure a PRO. Neither term is itself evidence that the
instrument is reliable, valid, responsive, interpretable, or suitable for a
specific use.

Do not assume that evidence from one population, language, setting, disease
severity, age group, administration mode, or intended use transfers unchanged to
another.

### Activation boundary

A questionnaire, scale, Likert item, quality-of-life score, or PRO variable does
not automatically make a task psychometric.

Examples:

```text
Evaluate whether this validation study supports construct validity.
-> psychometrics-pro

Compare mean questionnaire scores across three groups.
-> analyze-stats

Plot questionnaire scores over four visits.
-> make-figures

Find papers using this questionnaire.
-> search-lit / discovery
```

Use the specialist only when the measurement meaning or measurement-property
claim is material.

---

## 2. Measurement-property map

Apply only the properties needed for the actual intended claim. Do not turn every
instrument question into a checklist of every possible property.

### Content validity

Ask whether the instrument's content adequately represents the intended
construct for the target population and use. Do not infer adequate content from
internal-consistency coefficients, factor analysis, or correlations alone.

When content-validity judgement depends on a current framework, development
record, qualitative evidence, expert/patient involvement, or instrument manual,
flag those sources for verification rather than inventing details.

### Structural validity

Structural validity concerns whether the observed score structure is compatible
with the dimensional structure required by the instrument's interpretation.

Do not treat a high internal-consistency coefficient as proof of dimensional
structure. If factor-analytic or other structural analysis is needed, hand the
actual computation/model choice to `/analyze-stats`.

### Internal consistency

Interpret internal consistency in relation to the intended score and relevant
structural assumptions. Avoid statements such as:

```text
Cronbach alpha is high, therefore the scale is valid.
```

Reliability-type coefficients quantify a specific property under specific data
and assumptions; they do not establish the entire validity argument.

### Reliability / test-retest

Reliability addresses consistency or reproducibility under the relevant repeated
measurement design. Clarify:

- what is repeated;
- over what interval;
- whether the construct is expected to remain stable;
- which score/level is evaluated;
- whether the statistic addresses relative ranking, absolute agreement, or a
  different reliability question.

Hand actual ICC/kappa/agreement/statistical computation to `/analyze-stats`.

### Measurement error

Keep measurement error distinct from reliability and from meaningful change.
When SEM, MDC, limits of agreement, or related quantities are needed, identify
the interpretation question and delegate computation to `/analyze-stats`.

A change smaller than an error-related threshold may be difficult to distinguish
from measurement noise, but exact rules or thresholds must follow the actual
method and verified source/manual when standard-dependent.

### Construct validity / hypothesis testing

Construct-validity claims require hypotheses or other evidence that connects
observed relationships/differences to the intended construct interpretation.

Do not convert an arbitrary significant correlation into a universal validity
claim. Clarify:

- why the comparator/relationship is theoretically relevant;
- expected direction and, when justified, magnitude/order;
- whether competing explanations remain;
- whether the evidence addresses the intended population and score use.

### Criterion validity

Do not assume every comparator is a gold standard. Criterion-validity language
requires a defensible external criterion for the target construct/use. If the
criterion itself is imperfect or conceptually different, use more cautious
construct-validity framing unless a verified standard justifies otherwise.

### Cross-cultural validity / measurement invariance

Translation or use in another language/culture does not establish measurement
equivalence.

Separate:

```text
linguistic translation
conceptual equivalence
cultural adaptation
structural comparability
measurement invariance / differential functioning
psychometric validation in the target population
```

If invariance or differential item functioning must be tested, `/analyze-stats`
owns the computation/model; this specialist owns the interpretation boundary.

### Responsiveness

Responsiveness concerns the instrument's ability to detect change in the
construct as intended. Do not infer responsiveness merely because a pre-post test
is statistically significant.

Distinguish:

```text
observed change
statistically detectable change
responsiveness evidence
measurement error
meaningful / important change
```

The design must make the change interpretation credible. Hand generic design
questions to `/design-study` and statistical computation to `/analyze-stats`.

### Interpretability

Interpretability concerns the meaning assigned to scores and changes. It is not
itself equivalent to validity or reliability.

Material issues may include:

- score direction;
- plausible score range;
- subscale versus total-score meaning;
- reference values or category labels when verified;
- distributional context;
- floor/ceiling effects;
- individual versus group-level interpretation;
- change-score interpretation.

### Floor and ceiling effects

Large concentrations near scale limits can constrain detectable worsening or
improvement and may change the interpretation of longitudinal results. Do not
use a remembered universal percentage cutoff as timeless authority; verify any
standard-dependent rule.

### MID / MCID and meaningful change

Keep terminology and derivation explicit. Do not treat all important-difference
estimates as interchangeable.

At minimum distinguish:

```text
MID/MCID or other meaningful-change estimate
!= measurement error
!= SEM
!= MDC
```

The interpretation depends on how the estimate was derived, the population,
anchor/distributional method if relevant, the intended level of use, and source
support.

### SEM / MDC

SEM and MDC are error/reliability-related concepts and do not automatically tell
us what patients consider important. Conversely, an MCID/MID estimate does not
show that observed individual change exceeds measurement error. Preserve both
questions when they are material.

---

## 3. Score and instrument architecture

### Score direction and scoring rules

Never assume whether a higher score means better or worse health/function. Use
the instrument's verified scoring rule when interpretation depends on direction,
reverse-coded items, weighting, subscale composition, transformation, or missing
items.

### Missing items

Do not invent a prorating/imputation rule. If instrument-specific missing-item
rules affect score validity or comparability, require the verified instrument
manual or study protocol.

### Ordinal item/scale interpretation

Likert-type items are ordinal observations. A summed/derived scale may be treated
differently under a justified analysis plan, but this specialist does not decide
that merely from item labels. Hand modeling and inferential choices to
`/analyze-stats`.

### Single-item versus multi-item measurement

Do not transfer internal-consistency logic to a single-item measure. Ask what
property and use are actually being evaluated.

### Reflective versus formative concerns

Use this distinction only when it materially affects interpretation or model
choice. Do not force every instrument into a measurement-model debate. When it
matters, flag that coefficient/factor interpretations may depend on the assumed
relationship between construct and indicators.

---

## 4. Translation and cross-cultural adaptation

This specialist owns **methodology cues**, not automatic translation.

Preserve:

```text
literal translation != conceptual equivalence
language translation != cultural validation
translated PROM != psychometrically validated PROM
same instrument name != measurement equivalence across groups
```

Material review questions may include:

- Was the intended construct preserved?
- Was the target population involved where appropriate?
- Were ambiguous/culturally specific items addressed?
- Is the translated scoring structure the same and verified?
- Is cross-group comparability being claimed?
- Is measurement-invariance or differential-functioning evidence needed?

Do not invent a mandated adaptation sequence or required number/type of
translators from memory. Verify current framework-specific requirements if the
claim depends on them.

---

## 5. Core psychometric guardrails

Always preserve these distinctions:

```text
reliability != validity
high Cronbach alpha != instrument validity
high ICC != instrument validity
statistically significant change != responsiveness established
responsiveness != clinically meaningful change
MCID/MID != MDC
correlation with another scale != automatic criterion validity
translation != cross-cultural validation
translated PROM != validated PROM
PRO != PROM != psychometric measurement property
```

Internal consistency is not a substitute for content or structural validity.
A validity argument is not established by collecting unrelated favorable
statistics and labeling the bundle "validated."

General claim-force rule:

```text
PSYCHOMETRIC CLAIM FORCE
<= AVAILABLE MEASUREMENT-PROPERTY EVIDENCE
 + METHOD APPROPRIATENESS
 + VERIFIED STANDARD/SOURCE SUPPORT WHEN STANDARD-DEPENDENT
```

If evidence only addresses one property, limit the claim to that property.

---

## 6. Standard, manual, and source dependence

Do not hard-code contemporary guideline editions, quality-rating systems,
thresholds, or instrument-specific manuals into timeless domain truth.

Source-backed verification is required when material decisions depend on:

- a current psychometric standard/framework;
- a rating rule or quality criterion;
- a numerical threshold;
- an instrument's scoring/manual rule;
- an instrument-specific MID/MCID;
- licensing/copyright/permission conditions;
- a formal adaptation or validation requirement.

The specialist may say **which kind of source is required**. It must not claim
that model memory itself verified the current rule.

When consumed through Academic Research:

```text
candidate discovery -> ZotSeek
source/evidence verification -> Zotero Local
scientific procedure -> MedSci
write routing -> Academic Write Coordinator
persistence -> Manuscript Forge Production
```

---

## 7. Mixed-task handoff model

A common validation task may need several owners.

Example:

```text
Plan a validation study for this Turkish PROM and tell me which analyses are required.
```

Recommended composition:

```text
psychometrics-pro
  -> construct, intended use, measurement properties, hypotheses,
     meaningful-change/interpretation targets, claim ceiling

design-study
  -> validation-study architecture, comparator, sampling/validity issues

calc-sample-size
  -> sample-size computation when required

analyze-stats
  -> factor/reliability/agreement/invariance/responsiveness or other
     statistical procedure actually selected
```

The new specialist does not compute the analyses. Its job is to make sure the
analysis answers the right measurement question and that the resulting claim is
not stronger than the evidence.

---

## 8. Handoff matrix

| Measurement-science issue | Existing owner / next skill |
|---|---|
| Statistical model, reliability/ICC/agreement calculation, factor/invariance/responsiveness analysis | `/analyze-stats` |
| General validation-study architecture, bias, comparator, design validity | `/design-study` |
| Sample-size computation | `/calc-sample-size` |
| Literature discovery | `/search-lit` |
| Current source/manual/reference verification | `/verify-refs` |
| Scientific visualization | `/make-figures` |
| Reporting guideline/checklist completeness | `/check-reporting` |
| Manuscript drafting | `/write-paper` |
| Own-manuscript critical review | `/self-review` |
| External manuscript review | `/peer-review` |

For multi-step requests, `/orchestrate` may call `/psychometrics-pro` to establish
the measurement-science constraints before handing procedural work to the owners
above.

---

## 9. Decision-note contract

A useful `/psychometrics-pro` output is compact and inspectable:

```text
## Psychometrics / PRO Assessment

Construct:
Instrument:
Population:
Intended use:

Measurement properties implicated:
- ...

Evidence currently available:
- ...

Evidence missing:
- ...

Psychometric interpretation:
- ...

Unsupported/promoted claims:
- ...

Standard/source verification needed:
- ...

Required handoffs:
- owner: ...
  question: ...

Claim ceiling:
- ...

Status:
- READY | PARTIAL | CANNOT_DETERMINE_FROM_CURRENT_EVIDENCE
```

Do not fill headings mechanically. Mark non-material sections succinctly.

---

## 10. V1 exclusions

Queue 8 does not create:

- a generic survey platform;
- a questionnaire registry/database;
- automatic questionnaire licensing/copyright adjudication;
- automatic questionnaire translation;
- a full COSMIN systematic-review engine;
- a dedicated Rasch/IRT provider;
- psychometric meta-analysis infrastructure;
- a regulatory PRO submission workflow;
- a full patient-centered outcomes platform;
- a new Academic Research provider, daemon, port, or persistence authority.

Advanced methods may be recognized as downstream needs; recognition does not
create a new execution owner.

---

## 11. Uncertainty behavior

Return `CANNOT_DETERMINE_FROM_CURRENT_EVIDENCE` or explicit missing-input notes
rather than guessing when a material interpretation depends on unavailable:

- construct definition;
- instrument/version/language;
- target population;
- intended use;
- scoring/manual rule;
- dimensional structure;
- study design/timepoints;
- comparator/hypothesis definition;
- measurement-property results;
- current standard/guideline source;
- statistical analysis needed to evaluate the property.

Measurement-science expertise should reduce ambiguity without disguising missing
evidence.
