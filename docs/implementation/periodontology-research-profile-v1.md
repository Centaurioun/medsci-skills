# Periodontology Research Profile v1 — Implementation Handoff

**Date:** 2026-08-20  
**Repository:** `Centaurioun/medsci-skills`  
**Branch:** `feature/periodontology-research-profile-v1`  
**Base:** `main@1cad5503690d2caeb1328ae928e840a2e2d7b8cb`  
**Wave:** `Wave 2 — Periodontology Domain Enrichment`  
**Mode:** implementation-first  
**Testing / verification:** not authorized / not run  
**Merge to main:** not authorized / not performed

## Objective

Add bounded periodontal/peri-implant research-domain expertise to the existing MedSci skill family without creating a second statistics engine, general study-design owner, evidence authority, writer, or standalone Dentistry provider.

## Implemented surfaces

### C1 — Capability ownership

**Status:** `IMPLEMENTED — UNTESTED`

Modified:

- `capabilities.yml`

Added:

- `periodontology_domain_expertise`
- owner: `periodontology-research`
- overlaps: existing `design-study`, `analyze-stats`, `make-figures`, `write-paper`, `self-review`, `check-reporting`

The ownership rule explicitly preserves those existing procedural owners.

### C2 — Typed Layer-D skill contract

**Status:** `IMPLEMENTED — UNTESTED`

Created:

- `skills/periodontology-research/skill.yml`

Contract:

```text
schema_version: 2
name: periodontology-research
layer: D
owner_domain: periodontology_domain_expertise
maturity: experimental
```

The contract produces bounded domain decision notes/annotations and does not own canonical analysis/manuscript writes.

Safety boundaries explicitly state that the domain skill:

- does not authorize citations or verify source claims;
- does not compute statistics;
- does not replace generic study-design, figure, writing, review, or reporting owners;
- does not infer unavailable clinical facts;
- remains advisory Layer-D behavior.

### C3 — Reusable domain profile

**Status:** `IMPLEMENTED — UNTESTED`

Created:

- `skills/periodontology-research/references/periodontology-domain-profile.md`
- `skills/periodontology-research/SKILL.md`

Coverage includes:

- periodontal health / gingivitis / periodontitis construct separation;
- staging/grading preservation when relevant without freezing one guideline edition as timeless truth;
- peri-implant health / mucositis / peri-implantitis separation;
- PD/PPD, CAL, BOP, plaque/gingival measurement interpretation;
- patient -> tooth/implant -> site -> visit hierarchy;
- full-mouth vs sampled-site interpretation;
- repeated/longitudinal measurement cues;
- changing denominator risks from missing/extracted/unavailable teeth/sites;
- clinical vs statistical significance distinction;
- periodontal treatment-response framing;
- smoking, baseline severity, prior periodontal care, oral-hygiene, systemic/medication, and site-selection cues;
- oral-systemic causal-overreach guardrails;
- terminology and claim-force consistency across manuscript sections;
- explicit handoffs to existing MedSci owners;
- `CANNOT_DETERMINE` / missing-input behavior instead of guessing.

### C4 — MedSci orchestration exposure

**Status:** `IMPLEMENTED — UNTESTED`

Modified:

- `skills/orchestrate/SKILL.md`

Added:

- `periodontology-research` to the Available Skills table;
- direct-routing examples for periodontal constructs, patient-tooth-site hierarchy, peri-implant terminology, and oral-systemic periodontal framing;
- explicit multi-step rule: run the domain pass for domain constraints, then route methodological/statistical/figure/reporting/writing/review work to the existing owner.

No second orchestrator was added.

## C5 — Generated catalog/docs exposure

**Status:** `PARTIAL — LIMITATION RECORDED`

The MedSci repository treats catalog/docs surfaces as generated artifacts, including `metadata/skills_catalog.json` and generated per-skill documentation.

The current ChatGPT/GitHub-only environment can edit repository files but cannot obtain a local `medsci-skills` checkout and execute the repository generators. A normal shell clone attempt is unavailable because the local shell environment cannot resolve GitHub.

To avoid inventing or hand-maintaining a second catalog representation, generated catalog/docs were **not** manually fabricated.

Required later materialization in a generator-capable environment:

```text
run the repository's existing skill catalog/docs generators
-> include periodontology-research in their derived outputs
-> persist only the generator-produced changes
```

This limitation is local to generated exposure; it did not block the source skill/profile/orchestration implementation.

## C6 — Academic Research snapshot consumption

**Status:** `NOT STARTED — OUTSIDE CURRENT WAVE SOURCE SCOPE`

No changes were made to:

- `Centaurioun/academic-research-plugin` MedSci source pin;
- `generated/medsci-snapshot/`;
- Academic `MEDSCI_PROCEDURES` inventory;
- Academic public routing for `periodontology-research`.

The planning contract treats downstream Academic snapshot consumption as a separately authorized step after a MedSci source revision is accepted/selected. The generated Academic snapshot must not be hand-edited.

## Commits

Material implementation commits in this branch include:

- `7de33983dbae3e64bb3feab176f22123234bbfa1` — add Periodontology capability owner;
- `a23307953c59652f91b5ac24d492f70f07b2398d` — add Layer-D skill contract;
- `5e4210597e968bc0912ea90b88170671743a6b6b` — add reusable domain profile;
- `f17993343890953400ff3d077cb2a62caf0221ed` — add skill instructions;
- `6265d9b9a850a620075fe9e5aa6e28633f1c9407` — correct frontmatter metadata typo;
- `b724b804700c7a9a35829ed3222c4eafb356e083` — expose bounded orchestration routing.

## Explicitly not performed

- unit/integration/contract tests;
- skill-contract validator execution;
- catalog/docs generator execution;
- manual QA;
- maturity promotion beyond `experimental`;
- Academic Research snapshot regeneration;
- Academic provider/routing integration;
- merge/release;
- Wave 3 Humanities implementation.

## Wave 2 source conclusion

```text
C1 capability owner          IMPLEMENTED — UNTESTED
C2 typed Layer-D contract    IMPLEMENTED — UNTESTED
C3 profile + skill           IMPLEMENTED — UNTESTED
C4 orchestrate exposure      IMPLEMENTED — UNTESTED
C5 generated catalog/docs    PARTIAL — LIMITATION RECORDED
C6 Academic snapshot         OUT OF CURRENT SOURCE SCOPE

WAVE 2 SOURCE IMPLEMENTATION:
  COMPLETE_WITH_RECORDED_GENERATOR_LIMITATION
```

Stop here for Wave 2 source implementation. Do not automatically start validation, snapshot integration, merge/release, or Wave 3.
