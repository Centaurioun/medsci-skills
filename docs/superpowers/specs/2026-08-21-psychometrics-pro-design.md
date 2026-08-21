# Psychometrics / PRO Specialist Design

**Date:** 2026-08-21  
**Repository:** `Centaurioun/medsci-skills`  
**Branch:** `feature/psychometrics-pro-v1`  
**Canonical base:** `main@af9c61831504dcd87955e533ef5cac9e888253b7`  
**Status:** APPROVED FOR IMPLEMENTATION

## Goal

Add a narrow MedSci specialist for psychometrics and patient-reported outcome measurement that owns measurement-science reasoning without replacing MedSci's existing statistics, study-design, evidence, reporting, writing, figure, or persistence owners.

## Why this is a real ownership gap

The current MedSci catalog contains general statistical support for survey/Likert data, reliability/agreement, ICC/kappa, and related computations through `analyze-stats`, but no dedicated specialist was identified whose primary responsibility is construct/instrument interpretation, measurement-property reasoning, PROM/PRO suitability, meaningful-change interpretation, or psychometric evidence ceilings.

Therefore Queue 8 is not primarily a new calculation engine. It is a thin methodology/domain layer that determines what measurement question is being asked, what evidence is required to support the psychometric claim, and which existing MedSci owner should perform the procedural work.

## Canonical representation

Create:

```text
skills/psychometrics-pro/
  SKILL.md
  skill.yml
  references/psychometrics-pro-domain-profile.md
```

The specialist is a MedSci Layer-D decision-note capability analogous in architectural role to other thin domain/methodology layers. It does not create a new MCP provider, daemon, port, persistence system, or standalone Academic Research authority.

## Owned responsibilities

`psychometrics-pro` owns only bounded measurement-science reasoning:

- construct definition and construct/score interpretation;
- instrument or scale interpretation;
- PROM/PRO suitability for a stated population and use;
- measurement-property reasoning;
- content validity;
- structural validity;
- construct validity / hypothesis-testing logic;
- criterion-validity interpretation when a defensible criterion exists;
- cross-cultural validity and measurement-invariance reasoning;
- internal-consistency interpretation;
- reliability and test-retest interpretation;
- measurement error;
- responsiveness;
- interpretability and floor/ceiling effects;
- score direction and scoring-rule implications;
- change-score interpretation;
- MID/MCID and meaningful-change reasoning;
- SEM/MDC interpretation;
- translation/cross-cultural-adaptation methodology;
- reflective/formative measurement concerns when materially relevant;
- single-item versus multi-item measurement concerns;
- ordinal item/scale interpretation;
- missing-item/scoring-rule implications;
- bounded handoff decisions to existing MedSci owners.

## Non-responsibilities and preserved owners

The new specialist must not absorb existing authorities:

```text
statistical computation / models     -> analyze-stats
general study design                  -> design-study
sample-size computation               -> calc-sample-size
literature discovery                  -> search-lit / Academic ZotSeek
source/reference verification         -> verify-refs / Academic Zotero Local
reporting compliance                  -> check-reporting
scientific figures                    -> make-figures
manuscript drafting                   -> write-paper
manuscript critique                   -> self-review / peer-review
persistence                           -> existing Academic writer / Forge path
```

The specialist may identify that a particular analysis, design feature, source, or reporting check is needed, but it does not execute or usurp that owner's responsibility.

## Core methodological guardrails

The profile must explicitly preserve these distinctions:

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

Internal-consistency claims must not be interpreted independently of the scale's dimensional/structural assumptions when those assumptions are material.

General claim-force rule:

```text
PSYCHOMETRIC CLAIM FORCE
<=
AVAILABLE MEASUREMENT-PROPERTY EVIDENCE
+ METHOD APPROPRIATENESS
+ VERIFIED STANDARD/SOURCE SUPPORT WHEN STANDARD-DEPENDENT
```

## Evidence ceiling and current standards

Do not freeze specific contemporary guideline thresholds, quality ratings, or cutoffs into the skill as timeless truth.

When a psychometric decision depends materially on a current external standard, guideline, rating rule, instrument manual, validation definition, licensing condition, or measurement-property threshold, the specialist must flag the need for source-backed verification rather than asserting a remembered rule as authority.

When consumed through Academic Research, preserve:

```text
candidate discovery -> ZotSeek
source/evidence verification -> Zotero Local
scientific methodology -> MedSci
write routing -> Academic Write Coordinator
persistence -> Manuscript Forge Production
```

## Activation boundary

Activate for material psychometric or PRO measurement questions, such as:

- evaluating psychometric properties of a questionnaire/PROM;
- deciding whether a study supports construct validity;
- reliability/responsiveness interpretation;
- MCID/MID versus measurement-error questions;
- planning validation or cross-cultural adaptation;
- determining whether longitudinal score change can be meaningfully interpreted;
- instrument suitability for a stated population/use.

Do not activate merely because a questionnaire or scale is present.

Examples that should normally stay with other owners:

```text
"Compare mean OHIP-14 scores across three groups." -> analyze-stats
"Plot questionnaire scores over four visits." -> make-figures
"Find papers using OHIP-14." -> search-lit / discovery
```

## Mixed-task orchestration

For a request such as "Plan a validation study for this Turkish PROM and tell me what analyses are required":

```text
psychometrics-pro
  -> construct + measurement-property plan
  -> design-study for study architecture
  -> analyze-stats for actual statistical procedures/computation
```

`psychometrics-pro` determines which measurement questions must be answered and how the resulting statistics may be interpreted. It does not become a second statistics engine.

## Output contract

Return a compact inspectable decision-note artifact using this structure when material:

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

Do not fabricate content merely to fill every heading; mark non-material sections succinctly.

## V1 exclusions

Do not implement in Queue 8:

- generic survey platform;
- questionnaire registry/database;
- automatic questionnaire licensing or copyright adjudication;
- automatic questionnaire translation engine;
- full COSMIN systematic-review engine;
- dedicated Rasch/IRT provider;
- psychometric meta-analysis platform;
- regulatory PRO submission workflow;
- full patient-centered outcomes platform;
- new Academic Research provider/daemon/port;
- new persistence authority.

Rasch/IRT or other advanced measurement models may be recognized as possible downstream methods, but the initial specialist does not create a separate execution engine for them.

## Source-side completion criteria

The MedSci source portion is complete when:

1. `psychometrics-pro` exists exactly once as a valid MedSci skill;
2. `SKILL.md`, `skill.yml`, and the domain profile are mutually consistent;
3. the specialist owns measurement-science reasoning but not statistical computation;
4. standard-dependent claims require source verification rather than frozen remembered thresholds;
5. activation examples distinguish psychometric intent from ordinary questionnaire statistics/discovery/figure work;
6. mixed tasks specify explicit handoffs to existing owners;
7. no new provider, persistence authority, or broad PRO platform is created;
8. bounded source validation identifies no material schema/content defect.

After canonical MedSci merge, Academic Research integration is a separate second half of Queue 8: refresh the exact MedSci snapshot, expose `psychometrics-pro`, and add narrow ordinary-language reachability without creating a new request class unless implementation proves one genuinely necessary.
