<!-- Domain probe module — shared, vendored BYTE-IDENTICAL by /peer-review and /self-review.
     Severity words below (MAJOR / MINOR / major / minor) denote finding severity, NOT a journal
     recommendation. Each consuming skill maps findings to its own output:
       - peer-review: Major / Minor comments + Confidential Comments to the Editor; a design-level
         flaw (missing consent, identifiable patient data, or causal overclaim) is placed as Major #1.
       - self-review: Anticipated Major / Minor Comments (Fatal / Fixable) mapped to category letters.
     Do NOT edit one copy only — run `python3 scripts/check_domain_probe_sync.py --sync`. -->

# Case-report probes (CR1–CR6)

A checklist for **case reports and small single-patient clinical narratives**. These probes
complement (do not replace) the generic Phase 2 issue checklist and the CARE items. They target the
places reviewers most often challenge case reports: why the case is publishable, whether the patient
is protected, whether the story is chronologically complete, and whether the Discussion stays inside
the evidence level of n=1.

**CR1 — Novelty / teaching-value justification**:
- Does the manuscript state why this case is worth publishing: rare presentation, diagnostic trap,
  management complication, unusual imaging/pathology correlation, unexpected response, or a practical
  bedside lesson?
- Is the claim anchored to a transparent literature boundary or epidemiologic context? "Rare" without
  a search boundary, comparator cases, or a clinically actionable lesson is a MAJOR priority concern,
  because the paper's contribution is the case's teaching value.

**CR2 — Consent, patient protection, and image de-identification**:
- Is written informed consent documented, or is a waiver/IRB basis stated when appropriate? Are
  patient images, dates, locations, institution names, initials, faces, scan metadata, and unusual
  demographic details removed or justified?
- Missing consent language or identifiable images/data is a MAJOR ethical/reporting issue. If the
  manuscript includes potentially identifying details, treat it as a finding even when the prose says
  "de-identified."

**CR3 — Causal attribution discipline**:
- Does the Discussion distinguish temporal association from causation? A single case can suggest a
  hypothesis or illustrate a plausible adverse event; it cannot establish incidence, efficacy,
  safety, risk, or mechanism.
- Escalate when Title/Abstract/Conclusion claims that an intervention "caused", "prevented",
  "proved", "was effective", or "should change practice" without stronger evidence. The fix is to
  reframe as "was temporally associated with", "is consistent with", "highlights", or "should prompt
  consideration."

**CR4 — Similar-case comparison and literature absence handling**:
- Does the manuscript compare the case with the nearest prior cases, including similarities and
  differences in presentation, diagnosis, intervention, and outcome? If five or more similar cases
  are found, a compact comparison table is usually clearer than prose.
- "First case", "only case", or "no prior reports" requires a documented search boundary. Without
  it, ask the authors to soften the claim or state the search strategy; do not let an unverified
  priority claim carry the Abstract.

**CR5 — CARE narrative completeness**:
- Can the reader reconstruct Patient Information -> Clinical Findings -> Timeline -> Diagnostic
  Assessment -> Therapeutic Intervention -> Follow-up and Outcomes? Is the timeline figure/table
  present when the course is multi-step, and does it include the final follow-up interval?
- Missing timeline, follow-up duration, diagnostic reasoning, or outcome assessment is usually a
  Fixable Major for a case report because the narrative is the evidence.

**CR6 — Generalizability and teaching-point framing**:
- Does the conclusion state a narrow learning point rather than a population-level recommendation?
  Strong case reports teach clinicians what to consider, monitor, or report; they do not infer
  prevalence, comparative effectiveness, or standard-of-care changes.
- Check the Abstract and final paragraph together. A cautious Discussion cannot rescue an
  overgeneralized Abstract conclusion.

**Output template (CR2 / CR3 example)**:
> "The case is clinically interesting, but the submission does not yet provide enough information for
> publication as a case report. First, the consent/anonymization statement should be made explicit,
> including whether the accompanying images have been stripped of identifiers. Second, the Discussion
> currently treats the temporal improvement after treatment as evidence that the intervention was
> effective. Because this is a single case, I would suggest reframing the conclusion as a hypothesis-
> generating observation and narrowing the teaching point to when clinicians should consider this
> diagnosis or management option."

**Discipline — leads vs findings (applies to CR1–CR6)**:
- A missing element is a **lead until the whole manuscript, figures, legends, and ethics statements are
  checked**. Do not allege absent consent or absent follow-up if it appears in a title page, figure
  legend, supplement, or patient-perspective section.
- Anchor every comment to what the flaw changes: patient protection (CR2), evidentiary overreach
  (CR3/CR6), contribution/priority (CR1/CR4), or narrative completeness (CR5). Avoid asking for
  broad extra literature unless it directly supports the case's teaching value.
