# ICMR ethical guidance and prototype status

Reviewed for submission: 12 October 2026.

## Accurate project statement

**Aarogya Saathi's design is informed by ICMR ethical guidance for biomedical research and healthcare AI. The prototype includes safeguards for optional AI consent, clinician review, scoped access and transparent simulation. A complete guideline assessment, independent validation and applicable institutional ethics review remain pending. No ICMR approval, certification or full compliance is claimed.**

## Official references

- [ICMR Ethical Guidelines for Application of Artificial Intelligence in Biomedical Research and Healthcare (2023)](https://www.icmr.gov.in/ethical-guidelines-for-application-of-artificial-intelligence-in-biomedical-research-and-healthcare): official overview describes ethical principles, governance, informed consent and ethics review across development, deployment and adoption.
- [ICMR National Ethical Guidelines for Biomedical and Health Research Involving Human Participants (2017), listed by the Bioethics Unit](https://ethics.ncdirindia.org/icmr_ethical_guidelines.aspx/Default.aspx).
- [ICMR Bioethics Unit FAQs](https://ethics.ncdirindia.org/Fre_AQ.aspx): practical context for the 2017 guidelines, including review of participant information and consent documents in English and local languages.

This note is an initial project mapping, not a clause-by-clause compliance audit or legal opinion. The official overview and FAQs were checked; the full PDFs could not be reliably fetched by the research tool during this update. Read the complete applicable guidelines with the institution before a real-patient study. Applicability and necessary review should be determined with the responsible institution and Ethics Committee, rather than assumed from a hackathon demonstration.

## Existing prototype safeguards and remaining work

| Topic | Current prototype | Before real-patient research / deployment |
|---|---|---|
| Consent and autonomy | Optional AI is consent-gated, with an opt-out. | Review participant information, purposes, external-provider processing, withdrawal and language accessibility. An app toggle alone is not a complete research consent process. |
| Human oversight and safety | Doctors review and approve prescriptions; automated check-ins route concerns to staff. | Establish clinical responsibility, escalation procedures, risk assessment and monitoring. Validate that automation does not delay appropriate care. |
| Privacy and confidentiality | Hospital and patient access scopes; fictional public demo accounts. | Review retention/deletion, access auditing, vendor handling, deployment security and all applicable data-protection duties. |
| Transparency | Simulated OTP, calls and breathing data are labelled; physical device untested. | Explain AI limitations, intended use and uncertainty to actual users. Do not present sensor estimates as diagnostic measurements. |
| Fairness and access | Several patient interface languages are available. | Native-speaker review, accessible consent and usability testing with older patients, caregivers and people without reliable smartphone access. No fairness result is claimed. |
| Evidence and accountability | Software tests and informal user feedback are documented separately. | Prospectively define evaluation measures, responsible investigators, incident handling and appropriate ethics review before recruitment. |

## Research evidence limits

The nurse feedback is second-hand informal feedback relayed by a team member. Reddit material is exploratory public secondary research with unverified identities. Neither establishes clinical effectiveness, representative need, hospital endorsement or Ethics Committee approval. No improved recovery, reduced complications or measured workload reduction is claimed.

The proposed ward pilot is a plan only. No real-patient enrolment should be implied. Physical device validation and any applicable regulatory requirements are separate from referencing ICMR ethics guidance.
