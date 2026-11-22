# Queue 8 — Psychometrics / PRO Source Validation

**Date:** 2026-08-21  
**Repository:** `Centaurioun/medsci-skills`  
**Branch:** `feature/psychometrics-pro-v1`  
**Canonical base:** `main@af9c61831504dcd87955e533ef5cac9e888253b7`

## Scope

This is the bounded source-side validation for the new `psychometrics-pro` MedSci specialist. It does not claim live Academic Research reachability; Academic snapshot/exposure/routing is the second half of Queue 8 and starts only after this source capability is canonicalized.

## Implemented source files

```text
skills/psychometrics-pro/SKILL.md
skills/psychometrics-pro/skill.yml
skills/psychometrics-pro/references/psychometrics-pro-domain-profile.md
```

Planning records:

```text
docs/superpowers/specs/2026-08-21-psychometrics-pro-design.md
docs/superpowers/plans/2026-08-21-psychometrics-pro.md
```

## Repository boundary check

Comparison against canonical base showed the branch ahead by 6 commits and behind by 0 before this evidence commit. Product/source scope was limited to the new Psychometrics/PRO capability plus its spec/plan; no existing MedSci skill was modified.

## Contract checks

Confirmed from the committed source:

```text
name: psychometrics-pro
schema_version: 2
layer: D
owner_domain: psychometrics_pro_measurement_science
maturity: experimental
```

`SKILL.md`, `skill.yml`, and `references/psychometrics-pro-domain-profile.md` are present and mutually aligned around a thin measurement-science decision-note role.

The initial front-matter indentation typo in `SKILL.md` was corrected during implementation before validation. The final front matter contains the top-level `tools:` field in the expected position.

## Existing downstream-owner resolution

Every downstream owner named by the new skill was resolved to an existing MedSci skill on the canonical source base:

```text
orchestrate
design-study
calc-sample-size
analyze-stats
search-lit
verify-refs
make-figures
check-reporting
write-paper
self-review
peer-review
```

No invented downstream skill slug remains.

## Authority-boundary checks

The new specialist owns:

```text
construct/instrument interpretation
measurement-property reasoning
PROM/PRO distinctions
score and meaningful-change interpretation constraints
cross-cultural/adaptation methodology cues
psychometric evidence ceilings
measurement-science handoff decisions
```

It explicitly does NOT own:

```text
statistical computation or model fitting
sample-size computation
generic study-design authority
source/evidence verification
citation authorization
figure generation
reporting completeness
manuscript authorship
canonical persistence
```

Existing ownership remains:

```text
statistics -> analyze-stats
general design -> design-study
sample-size computation -> calc-sample-size
discovery -> search-lit
reference/source audit -> verify-refs
figures -> make-figures
reporting -> check-reporting
writing -> write-paper
own-manuscript review -> self-review
external review -> peer-review
```

`check-reporting` already includes COSMIN among its reporting/checklist surfaces. The new specialist therefore does not implement a duplicate COSMIN reporting engine; it only supplies measurement-science reasoning and flags standard-dependent claims for authoritative source verification.

## Psychometric guardrail checks

The source contract explicitly preserves:

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

It also preserves the claim ceiling:

```text
PSYCHOMETRIC CLAIM FORCE
<= AVAILABLE MEASUREMENT-PROPERTY EVIDENCE
 + METHOD APPROPRIATENESS
 + VERIFIED STANDARD/SOURCE SUPPORT WHEN STANDARD-DEPENDENT
```

No contemporary numerical guideline cutoff or instrument-specific threshold was frozen into the specialist as timeless authority.

## Activation-boundary checks

The source contract distinguishes psychometric intent from ordinary questionnaire use:

```text
"Evaluate the psychometric properties of this questionnaire."
-> psychometrics-pro

"Compare mean OHIP-14 scores across three treatment groups."
-> analyze-stats

"Plot OHIP-14 scores over four visits."
-> make-figures

"Find papers using OHIP-14."
-> search-lit / discovery
```

Academic Research runtime reachability for those examples is NOT claimed by this source-side validation and remains the second-half Queue 8 task.

## Mixed-task handoff check

The source contract handles validation-study requests by composing owners rather than replacing them:

```text
psychometrics-pro
-> measurement questions / construct / intended use / claim ceiling
-> design-study
-> calc-sample-size when needed
-> analyze-stats for actual statistical procedures
```

## V1 exclusions preserved

Not added:

- generic survey platform;
- questionnaire registry/database;
- automatic licensing/copyright adjudication;
- automatic questionnaire translation engine;
- full COSMIN systematic-review engine;
- dedicated Rasch/IRT provider;
- psychometric meta-analysis platform;
- regulatory PRO submission workflow;
- full patient-centered outcomes platform;
- new MCP provider/daemon/port;
- new persistence authority.

## Limitation

This validation is repository-static and source-contract scoped. It does not demonstrate Academic Research exposure, ordinary-language selection, generated-snapshot provenance, or live host invocation. Those are intentionally deferred until the exact canonical MedSci source SHA is available after merge.

## Recommendation

`READY_FOR_CANONICAL_MERGE`
