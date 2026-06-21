# Security & Scope Boundary

MedSci Skills is open-source tooling for clinical-manuscript preparation. This page
covers how to report a vulnerability and — because this is medical-domain software —
the safety boundary and the data-hygiene rules for public issues.

## Reporting a vulnerability

If you find a security issue (for example, a script that could execute untrusted
input, a dependency vulnerability, or a path that could exfiltrate local data),
please report it privately rather than opening a public issue:

- Use GitHub's **"Report a vulnerability"** (Security → Advisories) on the
  repository, or
- contact the maintainer listed in [`CITATION.cff`](CITATION.cff).

Please include reproduction steps and the affected version. We will acknowledge the
report and work on a fix; please allow reasonable time before public disclosure.

## Medical scope boundary

MedSci Skills supports **manuscript preparation and research workflow**. It is
**not** a clinical tool. Specifically, it:

- does **not** provide patient-specific medical advice;
- does **not** make diagnoses or recommend treatment;
- does **not** replace authors, statisticians, reviewers, IRBs, or journal
  requirements;
- **requires human-expert verification** of every output — it can produce
  incomplete or incorrect results if used without review.

The deterministic detectors are designed to **reduce common manuscript-preparation
errors** before review; they do not guarantee correctness and are not a substitute
for expert judgment.

## Data hygiene — keep PHI and private content out of public issues

This is a public repository. When filing issues, PRs, or examples, do **not**
include:

- protected health information (PHI) or any patient-level data;
- unredacted local file paths, private emails, or institution-only context;
- unpublished manuscript content, private manuscript IDs, or project codes;
- confidential reviewer comments (unless fully anonymized and you have the right to
  share them).

Use synthetic or public datasets in examples. The repository's validators include a
PII/precedent scan, but the first line of defense is not pasting sensitive content
in the first place. If you need to share a failing case that involves sensitive
data, reduce it to a synthetic minimal reproduction.
