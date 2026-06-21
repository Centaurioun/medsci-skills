# Skill `references/` load model + routing-asset gate

A maintainer note that records two decisions for the v4.6.0 cleanup: (1) the
`references/` load model that gates the `write-paper` Phase-7 extraction pilot,
and (2) why the routing-asset gate scans the `${CLAUDE_SKILL_DIR}/`-prefixed form
and **not** bare `references/...` paths.

## 1. Load model — extraction reduces per-invocation context

In the Agent Skills model, a skill's `SKILL.md` **body** is loaded into context
when the skill is invoked, while files under `references/` are read **on demand**
— only when the `SKILL.md` instructs the agent to read them. The repo's own
convention confirms this: reference files are introduced as
`${CLAUDE_SKILL_DIR}/references/<file>` with "read it before X" phrasing
(e.g. `skills/revise/SKILL.md`, `skills/humanize/SKILL.md`), i.e. they are not
assumed already-present, they are fetched when needed.

Consequence for the token diet:

- The always-on routing cost (a skill's frontmatter `description`) is **unchanged**
  by extraction.
- The per-invocation cost (the loaded `SKILL.md` body) **shrinks** when large,
  conditionally-needed prose moves into `references/` that is read only when that
  phase actually runs.

So moving `write-paper` Phase 7 (~460 lines, only relevant during the final
polish pass) into `references/` reduces what a `write-paper` invocation must carry
up front. **Conclusion: the extraction pilot (A1) is worth doing.** The pilot
should still measure the realized delta on `write-paper` before extending the
pattern to other skills (A2/A3, deferred to v5.1).

## 2. Routing-asset gate scans `${CLAUDE_SKILL_DIR}/...`, not bare `references/...`

The extraction creates a new pointer from `SKILL.md` to an extracted
`references/...` file. To catch a mistyped/dangling pointer,
`scripts/validate_routing_assets.py` already validates every
`${CLAUDE_SKILL_DIR}/<path>` asset reference (scan A) plus the `check-reporting`
checklist bullets (scan B).

A bare `references/<path>` existence scan was considered and **rejected** — an
empirical scan of the live repo found 13 bare `references/...` mentions, **none of
which are bundled-asset bugs**, in two categories a path-existence check cannot
distinguish:

- **Cross-skill references** — the path names *another* skill's `references/` dir,
  not the current skill's: `humanize` → `revise`'s `r2r_voice.md`; `revise` →
  `humanize`'s `ai_patterns.md`; `analyze-stats` → `make-figures`'
  `exemplar_plots/*.md`; `calc-sample-size` → `analyze-stats`' `templates/`;
  `write-paper` → `manage-refs`' `check_xref_symptoms.md`.
- **Runtime project artifacts** — files the skill writes/reads in the *user's*
  project workspace, not bundled in the repo: `references/library.bib`
  (`search-lit` output), `references/zotero_collection.json` (`lit-sync` writes it
  "in the project workspace"), `references/verified_references.tsv` (`verify-refs`
  output).

A bare-path existence gate would red CI on all 13 — exactly the false-positive
risk the plan flagged. **Decision:** rely on the unambiguous
`${CLAUDE_SKILL_DIR}/references/<file>` form (scan A) and require extraction
pointers to use that prefix — which is already the repo convention. The only gap
was that this gate had **no regression test**; PR-1 adds one
(`tests/test_routing_assets.sh`).

### Implication for the A1 extraction

Write the Phase-7 pointers as
`${CLAUDE_SKILL_DIR}/references/phase7_integrity_audits.md` and
`${CLAUDE_SKILL_DIR}/references/phase7_docx_build.md` so scan A validates them. A
dangling pointer then fails `validate_routing_assets.py --strict` (covered by the
new test).
