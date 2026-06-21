# Maintainers

MedSci Skills is a physician-built toolkit. Its value comes from real
manuscript-writing, submission, reviewer-feedback, and revision experience, so the
roles below deliberately separate **clinical/research authority** (which stays with
the founder) from **technical maintenance** (which can be shared).

## Roles

### Founder / Clinical Lead

Final authority on everything that touches clinical or research validity:

- the project's clinical/research **scope** (what the toolkit does and does not do);
- inclusion of an **official** skill, detector, probe, or reporting checklist;
- any **medical / research claim** in the docs or skill content;
- interpretation of **benchmark / evaluation** results;
- the final **release** approval.

External contributors do **not** add unsupported medical claims independently;
those changes require Clinical Lead review.

### Technical Maintainer (role, may be shared in future)

Maintains the engineering surface, but not the clinical validity of content:

- PR hygiene and review structure; CI; issue triage;
- documentation consistency, changelog, release-note drafting;
- version synchronization (`package.json` / `CITATION.cff` / release tag / catalog
  counts) and packaging/release automation;
- non-medical documentation cleanup.

### Clinical Reviewers (optional, future)

Domain experts who review specific skills, detectors, or reporting content. An
optional role to grow review capacity without expanding merge rights.

### Community Contributors

Anyone opening issues, examples, or pull requests. Contributions follow
[`CONTRIBUTING.md`](CONTRIBUTING.md); they must not introduce unsupported medical
claims, PHI, or private manuscript content.

## Decision rule

If a change affects **clinical/research scope, an official-skill decision, a
medical/research claim, or a benchmark interpretation**, it needs Clinical Lead
sign-off. Everything else (CI, docs, packaging, refactors, test coverage) is
ordinary technical maintenance.

## Permission ramp for a future part-time technical maintainer

To onboard help safely, merge rights expand with demonstrated trust — not all at
once. The detailed ramp lives in
[`docs/maintainer_workflow.md`](docs/maintainer_workflow.md); in brief: triage →
docs-only merges → non-medical merges, with the founder retaining final release
approval throughout.

## Current

- **Founder / Clinical Lead:** Yoojin Nam, MD ([ORCID 0000-0001-8565-1360](https://orcid.org/0000-0001-8565-1360)).
- **Technical Maintainer:** the founder, currently; the role is documented so it
  can be shared.
