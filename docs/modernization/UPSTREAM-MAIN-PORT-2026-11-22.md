# MedSci Fork — Current Upstream-Main Source Port, 2026-11-22

**Implementation:** source changes committed on Centaurioun/medsci-skills feature/2026-11-22-medsci-upstream-main-port.

**State:** IMPLEMENTED — UNTESTED; no local Git sync merge, generated-index regeneration, PR, release, installation or live service deployment executed.

## Why this branch supersedes two earlier upgrade candidates

- Old Centaurioun fork main was pinned to MedSci 5.24.0 at e9a15b50c029de637065684b94e2cd0cead8b506.
- Earlier feature/2026-11-22-skill-capability-upgrades was based on that old fork and staged a historical 5.25.0-rc.0. It is preserved but should not be used as the final source upgrade.
- Later feature/2026-11-22-medsci-v6.4.0-port began at the official upstream v6.4.0 tag 56273a0dcea1d2a62696bee9f49346defd4e9812. It ported original helper modules, custom specialists, plugin metadata and source routing but was six upstream commits behind.
- **THIS BRANCH** feature/2026-11-22-medsci-upstream-main-port was created directly at upstream Aperivue/medsci-skills main commit 424c9ac5e8b1bb3761461124aeff87fc8cb748f7 as observed on 2026-11-22, six commits after v6.4.0. It is the current authoritative fork-side integration candidate.
- Upstream may advance again; compare with the live origin/main refs at execution rather than assuming this source is forever newest.

## Actual original code and source configuration now present

Two fork-only scientific specialists migrated from old fork main with their entire
source-defined typed skills, source references and research handoff documents:
- skills/periodontology-research/SKILL.md, skill.yml, references/periodontology-domain-profile.md
- skills/psychometrics-pro/SKILL.md, skill.yml, references/psychometrics-pro-domain-profile.md

Their SKILL.md headers use the current v6 Agent Skills description + metadata layout;
their original detailed domain methodology, scope and evidence boundaries remain.

Nine original additive helper files/profiles ported into existing source owners:
- meta-analysis: scripts/import_screening_records.py, scripts/screening_batch_ledger.py;
- revise: scripts/revision_ledger.py, scripts/revision_anchor_map.py;
- lit-sync: references/deep_reading_note_profile.md, scripts/render_deep_reading_note.py;
- self-review: scripts/report_code_lineage.py;
- present-paper: references/slide_evidence_manifest.md, scripts/audit_slide_evidence.py.

Related SKILL.md procedures for meta-analysis, search-lit, revise, lit-sync, self-review
and present-paper refer to these optional helpers. Related typed skill.yml
deterministic_scripts entries list them without creating redundant new top-level skills.

The cross-batch ledger on this new branch now uses an indexed identity lookup and
explicit named human adjudication (including source locator) of disagreements
between independent reviewer screening decisions. It still never modifies a
research project directly, makes inclusion judgments, or treats records/reports/
studies as automatically equivalent.

Fork-specific integration files preserved or modernized:
- capabilities.yml has specialist owner domains;
- skills/orchestrate/SKILL.md routes to both optional domain specialists;
- scripts/gen_skills_catalog_json.py maps both custom owner domains to a category;
- .claude-plugin/marketplace.json includes both under medsci-data;
- plugin.json and .codex-plugin/plugin.json retain the fork-specific plugin surfaces;
- original docs/implementation/ records for the two specialist skill projects are preserved.

Upstream core v6 procedures, official QUADAS-3 v1.2 guidance, 8 compatibility
alias folders, the current upstream six post-v6.4.0 commits, and existing MedSci
scientific gate families are inherited rather than overwritten with v5 files.

Expected source layout after adding specialists is **56 typed skills plus 8
redirect-only aliases**, subject to the actual Codex generator/schema confirmation.

## Pre-release version and citation provenance

Fork source staged version: 6.4.1-rc.0, intentionally UNPUBLISHED.

- package.json says 6.4.1-rc.0.
- CITATION.cff says 6.4.1-rc.0, points to the Centaurioun fork, retains credit to
  upstream authors and their original paper, and does NOT invent a fork DOI or
  released date. No public fork release or upstream-owned npm package publication
  has taken place.
- plugin.json and .codex-plugin/plugin.json say 6.4.1-rc.0.
- metadata/distribution_manifest.json and metadata/distribution_files.json are
  auto-generated artifacts and remain stale from upstream v6.4.0. DO NOT hand
  patch their generated values. Codex will run scripts/gen_distribution_manifest.py
  after the source merge, using CITATION.cff as its version SSOT, then appropriate
  catalog/count/skill documentation generators.

The upstream Aperivue v6.4.0 publication date, original work, license and DOI
must remain historically attributable, not relabelled as a newly published fork release.

## Git merge/history and Codex boundary

GitHub confirmed the old fork/main and upstream/main have diverged (observed
34 ahead, 274 behind at the main/main comparison). The user's GitHub view of
72 ahead refers to the older feature/2026-11-22-skill-capability-upgrades
branch, not fork/main; no contradiction.

No merge into fork/main was performed; all historic fork commits remain intact.
A trusted local Codex environment should:

1. Fetch latest upstream/main and the current source feature branch; if upstream
   has moved since the base commit above, resolve only the additional delta on
   a new staging branch without losing custom source.
2. Create and push a backup branch at the exact old fork main commit.
3. Create an integration branch FROM old fork main, then merge the prepared
   current-upstream-main source feature/staging branch into it with a real
   two-parent merge. This preserves the old fork's Git history, custom specialists
   and upstream version upgrades without force-pushing main.
4. Resolve collisions file by file, keeping v6 core content and these original
   fork additions, not copying v5-generated catalogs or obsolete v5 QUADAS-3
   guides over the latest upstream.
5. Execute user-delegated tests, repair any observed problems, run native
   generators, record actual provenance/SHAs, and push a proposed fork main PR.
   Do not merge or publish without explicit user authorization.
6. Use the approved final exact source commit to regenerate Academic Research's
   complete MedSci snapshot with its source closure builder on an Academic
   feature branch; live runtime deployment is a separate action.

**Controlling Codex handoff:**
Centaurioun/academic-research-plugin, branch
feature/2026-11-22-skill-capability-upgrades,
docs/research/2026-11-22-skill-ecosystem/CODEX-UPSTREAM-MAIN-FINAL-HANDOFF.md.

## Dispositions

Source port, typed specialists, routing, original helper modules, citation
prerelease metadata and Academic workflow profiles: IMPLEMENTED — UNTESTED.

Cross-fork merge with preserved history, generated distribution data, local
fixture/gate tests, exact Academic snapshot, source PR, main merge, release,
runtime deployment: NOT PERFORMED; assigned to the later Codex phase under
the user's explicit separation of responsibilities.
