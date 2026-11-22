# Fork/upstream v6.4.0 sync — preservation rules

Date: 2026-11-22. GitHub source changes are IMPLEMENTED — UNTESTED. Merge and tests remain Codex tasks.

## Authoritative repository facts

- Upstream: Aperivue/medsci-skills, main commit 424c9ac5e8b1bb3761461124aeff87fc8cb748f7 when checked.
- Old fork: Centaurioun/medsci-skills, main commit e9a15b50c029de637065684b94e2cd0cead8b506, source version 5.24.0.
- GitHub cross-fork compare: **fork/main 34 ahead, 274 behind** upstream/main; merge base 8481d69314e5464677e6be8237d276709f58906b. User had seen 72 ahead in a GitHub UI view; resolve which refs are being compared if counts differ.
- Official published v6.4.0 tag: 56273a0dcea1d2a62696bee9f49346defd4e9812. Upstream/main is six commits ahead of the tag at this checkpoint.
- Prepared fork feature: feature/2026-11-22-medsci-v6.4.0-port, based directly on the official tag, staged as 6.4.1-rc.0 (UNRELEASED).

## Original fork-specific components already ported

Both full research specialist skills, their typed manifests and their reference profiles:
- skills/periodontology-research/{SKILL.md,skill.yml,references/periodontology-domain-profile.md}
- skills/psychometrics-pro/{SKILL.md,skill.yml,references/psychometrics-pro-domain-profile.md}

Their original domain decision research records were also brought to docs/implementation. Both SKILL.md frontmatters are adapted for v6 metadata and a governed Academic Research write boundary. They are integrated into capabilities.yml, skills/orchestrate/SKILL.md, the v6 category-map generator, and the medsci-data entry in .claude-plugin/marketplace.json.

Original research helper additions under existing skills:
- skills/meta-analysis/scripts/import_screening_records.py
- skills/meta-analysis/scripts/screening_batch_ledger.py
- skills/revise/scripts/revision_ledger.py
- skills/revise/scripts/revision_anchor_map.py
- skills/lit-sync/references/deep_reading_note_profile.md
- skills/lit-sync/scripts/render_deep_reading_note.py
- skills/self-review/scripts/report_code_lineage.py
- skills/present-paper/references/slide_evidence_manifest.md
- skills/present-paper/scripts/audit_slide_evidence.py

The v6 SKILL.md and skill.yml references for these additions are also present. Old fork plugin.json and .codex-plugin/plugin.json have been ported and marked with fork prerelease version. Do not automatically publish them using the upstream npm namespace.

## Explicit conflict-resolution ownership

1. **Core upstream MedSci skill implementations, installer, official QUADAS-3, v6 model aliases and reporting files:** use current upstream v6 source plus explicitly ported fork patches, NOT old v5 source.
2. **Fork-only periodontology and psychometrics specialists:** keep the new v6-port versions. Do not replace them with their old-frontmatter v5 copies, and do not duplicate the skill folders.
3. **Original fork helper files and their links:** keep the v6 port's additive scripts and integration while incorporating any newer upstream/main edits to surrounding skill instructions.
4. **Routing, capabilities, category map and marketplace:** preserve upstream v6 structure plus both custom domains. Avoid copying old v5 versions wholesale.
5. **Generated metadata, distribution_file hashes, skills_catalog, docs/skills, counts:** regenerate using upstream v6 generators; never manually splice stale generated data.
6. **Version and attribution:** upstream v6 scripts/gen_distribution_manifest.py uses CITATION.cff as version SSOT. Currently CITATION.cff documents the published upstream 6.4.0 but the fork package/manifest are staged at 6.4.1-rc.0. This is a KNOWN prerelease consistency issue that Codex must address deliberately before the generated manifest or release gates can be claimed valid. Do not invent a release date, DOI or npm publishing ownership.
7. **Historical fork docs and plugin declarations:** preserve the source in a traceable form, but adapt to v6 and current schemas where necessary. Old release badges/README snapshots are not authoritative proof of a fork release.

## Codex integration plan

Use a clean authenticated local clone; add upstream remote; fetch all refs. Preserve fork/main current full commit in a timestamped backup branch before any merge. Create a staging branch from the v6-port feature branch and merge upstream/main to bring the post-tag six commits. Create a separate integration branch starting from old fork/main and merge the staging branch. This retains the fork's old 34 unique commits in Git history while bringing in v6 source and the fork-only specialist source. Resolve merge conflicts per the rules above rather than using a global ours/theirs choice. Regenerate official v6 indexes, run Codex-only testing, and open a PR targeting fork/main. Do not force push or reset main. Do not merge into main unless user explicitly approves.

After source is selected and committed, use Academic Research's existing MedSci exact-SHA snapshot builder in a separately authorized local Codex environment. No user manuscripts, Zotero records, clinical datasets or canonical Forge documents may be changed for testing.

Controlling Codex instructions are maintained in Centaurioun/academic-research-plugin, docs/research/2026-11-22-skill-ecosystem/CODEX-FORK-MAIN-UPSTREAM-SYNC.md.
