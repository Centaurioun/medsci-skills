<!-- AUTO-GENERATED from skills/periodontology-research/SKILL.md by scripts/gen_skill_docs.py. Do not edit by hand. -->

# periodontology-research

> Use when periodontal or peri-implant terminology, case definitions, patient-tooth-site measurement hierarchy, treatment interpretation, or oral-systemic claims materially affect a research task.

**Invoke:** `/periodontology-research`

## When to use

`periodontology-research` activates on requests such as: periodontology research, periodontitis, gingivitis, peri-implant, clinical attachment level, probing depth, bleeding on probing, oral-systemic, periodontal measurements.

## Quality Card

**Purpose** — Supply bounded periodontal and peri-implant domain interpretation constraints, terminology checks, measurement/hierarchy warnings, and handoffs to existing MedSci procedure owners.

**Safety boundaries**

- Domain expertise does not authorize citations or verify source claims.
- Does not compute statistics or replace /analyze-stats.
- Does not replace generic study-design, writing, figure, review, or reporting owners.
- Does not infer unavailable clinical facts or convert missing information into certainty.
- Advisory Layer-D output only: writes decision notes, not canonical analysis or manuscript artifacts.

**Known limitations**

- Experimental domain profile; current guideline-specific thresholds and case definitions still require authoritative source verification.
- Clinical plausibility review supports but does not replace researcher or clinician judgement.
- No standalone demo or dedicated automated behavioral check is shipped with the initial profile.

**Evidence** — `not_yet_demonstrated`

## Bundled resources

**References** (`skills/periodontology-research/references/`):

- `periodontology-domain-profile.md`

## Source

Canonical definition: [`skills/periodontology-research/SKILL.md`](../../skills/periodontology-research/SKILL.md)

---

*Part of [MedSci Skills](../../README.md) — Claude Code skills for the medical research lifecycle. This page is generated from the skill's `SKILL.md`; edit that file and re-run `scripts/gen_skill_docs.py`.*
