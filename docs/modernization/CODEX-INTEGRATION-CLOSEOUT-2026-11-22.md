# Codex Integration Closeout — 2026-11-22

## Exact source and history

- Old fork `main`: `e9a15b50c029de637065684b94e2cd0cead8b506` (MedSci 5.24.0).
- Backup branch pushed to `Centaurioun/medsci-skills`: `backup/fork-main-before-v6-sync-20261122T000000Z` at that exact SHA.
- Official upstream `Aperivue/medsci-skills:main`: `424c9ac5e8b1bb3761461124aeff87fc8cb748f7` (confirmed current at closeout).
- Prepared fork source `feature/2026-11-22-medsci-upstream-main-port`: `436eae575888dff9c5d3e15928c901e90af6e152`.
- Prepared source already contains current upstream/main as an ancestor; no separate staging merge was needed.
- Integration branch: `integration/fork-main-current-upstream-20261122T184331Z`.
- Merge commit: `07eae794b74d803a240bb568901aa749b85e34e1`; first parent is old fork main and second parent is the prepared source SHA. This commit is the two-parent source integration.
- PR #4: https://github.com/Centaurioun/medsci-skills/pull/4 — OPEN, non-draft, base `main`, head `integration/fork-main-current-upstream-20261122T184331Z` at `07eae794b74d803a240bb568901aa749b85e34e1` when inspected.
- No main branch was changed or force-pushed.

## Conflict resolutions

Fourteen conflicts were resolved individually. Current v6 source was retained for README.md, README.zh-CN.md, docs/skills/README.md, paper.md, skills/orchestrate/SKILL.md, both specialist SKILL.md files, plugin.json, .codex-plugin/plugin.json and .claude-plugin/marketplace.json. The generator source was retained for `scripts/gen_skills_catalog_json.py`. Generated catalog/count/distribution artifacts were regenerated with the repository tools after source integration; no generated hashes were hand-written. This preserves v6 core and fork-specific routes without copying v5 core content.

## Fork-specific material and version

- `periodontology-research` and `psychometrics-pro` typed skill content, profiles and routing are present; both validate as v2 skills.
- All nine original helper files and source integrations are present: two meta-analysis helpers, two revision helpers, two lit-sync files, one self-review helper and two presentation files.
- Source and generated metadata consistently report `6.4.1-rc.0`, an unpublished prerelease. No fork DOI/date was invented.
- A prerelease-compatible semver pattern was added to the distribution generator and version consistency checker because the previous v6 regex rejected the required rc version.
- Catalogs report 56 typed skills and 8 redirect-only aliases; distribution manifest inventories 1,492 files.

## Verification performed

Passed: capability registry strict validation; all 56 typed v2 contracts and 8 aliases; frontmatter schema (64 blocks); catalog count consistency; version consistency; generated catalog, distribution manifest, skill docs and marketplace checks; npm package audit; marketplace (9 checks); skill catalog (10 checks); skill discovery (7 checks); screening reconciliation; response claims (112 checks); lit-sync polling (4 checks); PRISMA 5-way synthetic gate (43 checks; GNU sed used to avoid macOS sed incompatibility); presentation deck-reading test; Python syntax compilation of all nine helper modules.

Additional temporary synthetic fixtures passed for duplicate DOI import, proposal-only revision ledger and anchor mapping, contained lineage inventory, abstract-depth deep-reading warning, two-record batch ledger ingestion, and native PPTX text presence. These are local synthetic checks only; they do not establish live host behavior, scientific correctness, or user approval.

## Not performed

No PR merge, release/tag, npm publication, Academic Runtime restart/deploy, Zotero write, or canonical manuscript write. The Academic snapshot is handled in the Academic feature branch handoff. PR status is recorded in this report after it is opened.
