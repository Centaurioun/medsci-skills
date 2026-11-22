# Psychometrics / PRO Specialist Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a narrow MedSci `psychometrics-pro` specialist that owns measurement-science interpretation and handoff decisions without duplicating statistics, study-design, evidence, writing, or persistence owners.

**Architecture:** Implement one Layer-D MedSci skill with a concise `SKILL.md`, schema-aligned `skill.yml`, and a reusable domain profile. The source skill returns advisory decision notes and routes computation/design/evidence work to existing MedSci owners. Academic Research exposure is explicitly deferred until this source capability is canonicalized.

**Tech Stack:** Markdown, YAML, existing MedSci skill schema and repository validation conventions.

**Spec:** `docs/superpowers/specs/2026-08-21-psychometrics-pro-design.md`

## Global Constraints

- Source base: `Centaurioun/medsci-skills@af9c61831504dcd87955e533ef5cac9e888253b7`.
- New canonical skill ID: `psychometrics-pro`.
- No new provider, daemon, port, persistence authority, questionnaire database, translation engine, or broad PRO platform.
- `psychometrics-pro` owns measurement-science reasoning, not statistical computation.
- Preserve `analyze-stats`, `design-study`, `calc-sample-size`, `search-lit`, `verify-refs`, `check-reporting`, `make-figures`, `write-paper`, `self-review`, and `peer-review` ownership.
- Current standard-dependent thresholds/rules require source-backed verification; do not freeze remembered cutoffs into the skill.
- Implementation first; run only bounded source validation after the substantive files exist.

---

### Task 1: Create the MedSci skill contract

**Files:**
- Create: `skills/psychometrics-pro/SKILL.md`
- Create: `skills/psychometrics-pro/skill.yml`

**Interfaces:**
- Consumes: existing MedSci Layer-D conventions and downstream owner slugs.
- Produces: `psychometrics-pro` advisory decision notes and explicit handoffs.

- [ ] **Step 1: Create `SKILL.md` with bounded activation and authority**

The file must include:

```text
Purpose
When to use
When NOT to use
Authority boundary
Required inputs
Operating workflow
Core psychometric guardrails
Standard/source verification rule
Output contract
Handoff matrix
Uncertainty behavior
V1 exclusions
```

The core guardrails must explicitly preserve:

```text
reliability != validity
high Cronbach alpha != instrument validity
high ICC != instrument validity
significant change != responsiveness established
responsiveness != meaningful change
MCID/MID != MDC
translation != cross-cultural validation
PRO != PROM != measurement property
```

- [ ] **Step 2: Create schema-version-2 `skill.yml`**

Use:

```yaml
schema_version: 2
name: psychometrics-pro
layer: D
owner_domain: psychometrics_pro_measurement_science
maturity: experimental
```

The YAML must state that outputs are advisory decision notes, side effects are limited to decision-note writing, and forbidden actions include replacing statistical computation or writing canonical analysis/manuscript artifacts.

Downstream consumers must include at least:

```text
orchestrate
design-study
calc-sample-size
analyze-stats
search-lit
verify-refs
check-reporting
make-figures
write-paper
self-review
peer-review
```

- [ ] **Step 3: Commit the skill contract**

```bash
git add skills/psychometrics-pro/SKILL.md skills/psychometrics-pro/skill.yml
git commit -m "feat: add psychometrics PRO specialist contract"
```

---

### Task 2: Create the measurement-science domain profile

**Files:**
- Create: `skills/psychometrics-pro/references/psychometrics-pro-domain-profile.md`

**Interfaces:**
- Consumes: construct/instrument/population/use context from the caller.
- Produces: reusable methodology constraints consumed by `SKILL.md` and downstream MedSci owners.

- [ ] **Step 1: Define construct, instrument, and intended-use distinctions**

The profile must distinguish:

```text
construct
instrument/PROM
score/subscale
target population
intended use
PRO concept
measurement property
```

It must state that mentioning a questionnaire alone does not activate psychometric review.

- [ ] **Step 2: Define the V1 measurement-property map**

Cover, without hard-coded contemporary thresholds:

```text
content validity
structural validity
internal consistency
reliability/test-retest
measurement error
construct validity/hypothesis testing
criterion validity
cross-cultural validity/measurement invariance
responsiveness
interpretability
floor/ceiling effects
score direction/scoring rules
change scores
MID/MCID
SEM/MDC
translation/cross-cultural adaptation
reflective/formative concerns when material
single-item vs multi-item concerns
ordinal score interpretation
missing-item/scoring implications
```

- [ ] **Step 3: Define claim-force and standard-verification rules**

Include the invariant:

```text
PSYCHOMETRIC CLAIM FORCE
<= AVAILABLE MEASUREMENT-PROPERTY EVIDENCE
 + METHOD APPROPRIATENESS
 + VERIFIED STANDARD/SOURCE SUPPORT WHEN STANDARD-DEPENDENT
```

Specify that current guideline/standard thresholds, rating rules, manuals, licensing conditions, or instrument-specific scoring rules require authoritative source verification when material.

- [ ] **Step 4: Define handoffs**

Map:

```text
statistical procedure/computation -> analyze-stats
general design/validity -> design-study
sample-size computation -> calc-sample-size
literature discovery -> search-lit
reference/source audit -> verify-refs
figures -> make-figures
reporting -> check-reporting
manuscript drafting -> write-paper
own-manuscript critique -> self-review
external review -> peer-review
```

- [ ] **Step 5: Commit the profile**

```bash
git add skills/psychometrics-pro/references/psychometrics-pro-domain-profile.md
git commit -m "feat: add psychometrics PRO domain profile"
```

---

### Task 3: Perform bounded source validation and record evidence

**Files:**
- Create: `docs/implementation/queue8-psychometrics-pro-source-validation.md`

**Interfaces:**
- Consumes: the three newly implemented skill files.
- Produces: source-side Queue 8 merge recommendation.

- [ ] **Step 1: Check repository-static contract consistency**

Confirm:

```text
skills/psychometrics-pro/SKILL.md exists
skills/psychometrics-pro/skill.yml exists
skills/psychometrics-pro/references/psychometrics-pro-domain-profile.md exists
skill ID is psychometrics-pro exactly once in this new capability
schema_version is 2
layer is D
maturity is experimental
all named downstream skill slugs exist in the repository
```

- [ ] **Step 2: Check authority boundaries**

Confirm the files do not claim ownership of:

```text
statistical computation
source verification
citation authorization
canonical manuscript writing
persistence
```

and do explicitly defer these to existing owners.

- [ ] **Step 3: Check activation examples**

Verify the source contract distinguishes:

```text
"Evaluate the psychometric properties of this questionnaire."
-> psychometrics-pro

"Compare mean OHIP-14 scores across three groups."
-> analyze-stats

"Plot OHIP-14 scores over four visits."
-> make-figures

"Find papers using OHIP-14."
-> search-lit / discovery
```

This is a source-contract check only; Academic runtime routing is deferred to the second half of Queue 8.

- [ ] **Step 4: Record limitations**

Record that this source-side validation does not claim live Academic Research reachability. That will be implemented after canonical MedSci merge using the exact resulting source SHA.

- [ ] **Step 5: Write final recommendation**

Use exactly one:

```text
READY_FOR_CANONICAL_MERGE
NOT_READY_MATERIAL_DEFECT
```

- [ ] **Step 6: Commit the validation record**

```bash
git add docs/implementation/queue8-psychometrics-pro-source-validation.md
git commit -m "docs: validate psychometrics PRO source capability"
```

---

### Task 4: Canonicalize source before Academic integration

**Files:**
- No new product files required.

**Interfaces:**
- Consumes: source-side validation result.
- Produces: exact canonical MedSci source SHA for the Academic Research snapshot refresh.

- [ ] **Step 1: Create a pull request to `main` from `feature/psychometrics-pro-v1`**

The PR description must preserve the authority boundary and state that Academic Research exposure is not part of the MedSci source PR.

- [ ] **Step 2: Merge only if the bounded source recommendation is `READY_FOR_CANONICAL_MERGE`**

Use an exact-head guard and normal merge.

- [ ] **Step 3: Record the resulting canonical merge SHA**

That SHA becomes the only allowed source for the second half of Queue 8 in `Centaurioun/academic-research-plugin`.

---

## Plan self-review

- Spec coverage: all approved Queue 8 source-side requirements are assigned to Tasks 1-4.
- Placeholder scan: no implementation placeholders remain.
- Ownership consistency: measurement-science reasoning belongs to `psychometrics-pro`; computation/design/evidence/writing/persistence remain with their current owners.
- Scope: Academic snapshot/exposure/routing is intentionally excluded until the MedSci source is canonical and therefore cannot accidentally pin an unmerged source branch.
