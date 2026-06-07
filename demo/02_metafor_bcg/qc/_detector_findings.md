# v3.7.0 Detector Findings — DEMO 2 (BCG meta-analysis)

Captured: 2026-06-07. medsci-skills v3.7.0. All commands run against the staging package.

## 1. check_classical_style.py (self-review §J / write-paper Step 7.1)

```
$ python3 $MEDSCI_SKILLS_ROOT/skills/self-review/scripts/check_classical_style.py manuscript/manuscript.md
=========================================
 Classical-Style Body Lint (§J)
=========================================
| Check | Severity | Detail |
|---|---|---|
| (none) | — | classical-style body conventions satisfied |

OK: classical-style body conventions satisfied.
exit: 0
```

## 2. check_pool_consistency.py (meta-analysis Phase 4 entry gate)

```
$ python3 $MEDSCI_SKILLS_ROOT/skills/meta-analysis/scripts/check_pool_consistency.py --help
usage: check_pool_consistency.py [-h] --lock LOCK
                                 --adjudication-tsv ADJUDICATION_TSV
                                 [--decision-col DECISION_COL]
                                 [--uid-col UID_COL]
                                 [--include-labels INCLUDE_LABELS] [--out OUT]
                                 [--quiet]

Phase 4 entry gate: asserts UID-set equality between the frozen
FINAL_POOL_LOCK.yaml and the round-3 adjudication TSV.

options:
  -h, --help            show this help message and exit
  --lock LOCK
  --adjudication-tsv ADJUDICATION_TSV
  --decision-col DECISION_COL
  --uid-col UID_COL
  --include-labels INCLUDE_LABELS
                        Comma-separated decision labels counted as included.
  --out OUT
  --quiet
```

NOT APPLICABLE to this clean-room demo: check_pool_consistency.py asserts UID-set equality
between a frozen FINAL_POOL_LOCK.yaml and a round-3 screening adjudication TSV. Those PRISMA
screening artifacts do not exist here because DEMO 2 pools the metafor built-in dat.bcg corpus
(13 fixed trials) rather than running a de novo search-and-screen. Marked NOT RUN (no
FINAL_POOL_LOCK.yaml / adjudication TSV); the demonstrated equivalent is the deterministic
17-claim 3-way numerical audit (Step 7.3a, 0 mismatches) plus the PRISMA Figure cascade
arithmetic (4/4 checks reconcile: 318->197->39->35->13).

## 3. check_reference_adequacy.py (self-review Phase 2.5c-2 / write-paper Step 7.3c)

```
$ python3 $MEDSCI_SKILLS_ROOT/skills/self-review/scripts/check_reference_adequacy.py --manuscript manuscript/manuscript.md --bib manuscript/_src/refs.bib --article-type meta-analysis
==============================================
 Reference Adequacy Gate (count + named methods)
==============================================
 Article type   : meta-analysis -> meta_analysis
 Cited refs     : 0  (target 40-80)
 Distribution   : Intro 0 / Methods 0 / Results 0 / Discussion 0
 Methods 0-cite : True
 Uncited methods: PRISMA
 ✗ [major] methods_zero_citations: The Methods/Statistical Analysis section contains no citations; every named method, score, guideline, and diagnostic criterion needs a canonical source (found uncited: PRISMA).
 ✗ [major] below_article_type_target: Cited references (0) are below the meta_analysis target (40-80).

 Verdict: BELOW_TARGET  |  2 major, 0 minor  |  adequacy_safe=False
exit: 0
```

## 4. check_generated_code.py (analyze-stats Phase 3.5) — bonus v3.7.0 detector

```
$ python3 $MEDSCI_SKILLS_ROOT/skills/analyze-stats/scripts/check_generated_code.py analysis/meta_analysis.R --strict
=========================================
 Generated-Code Quality (Phase 3.5)
=========================================
| File:Line | Check | Severity | Detail |
|---|---|---|---|
| (none) | — | — | scripts are reproducibility-clean |

OK: 1 file(s) reproducibility-clean (0 minor flag(s)).
exit: 0
```
