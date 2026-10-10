# ICMR, research ethics, ABDM and the evidence plan
**Written:** 10 Oct 2026 · **Sources opened:** 15 (plus 2 that failed to open) · **Confidence overall:** medium (high on ICMR 2017 ethics rules and CTRI, which were read in the primary text; medium on the AI guideline, whose PDF was too large to open; low on ABDM exit steps, which rest on vendor and forum sources)

Short forms used: **ICMR** = Indian Council of Medical Research (the Government's medical research body). **CDSCO** = India's medical-device and drug regulator. **EC / IEC** = (institutional) ethics committee, the hospital panel that must approve any study on people. **CTRI** = Clinical Trials Registry – India. **ABDM** = Ayushman Bharat Digital Mission, the national digital health records programme. **NHA** = National Health Authority, which runs ABDM. **DHR** = Department of Health Research.

## Answer in 10 lines
1. **There is no connection between SpiroBuddy and ICMR today.** ICMR has not seen, funded, reviewed or endorsed it. Say so plainly.
2. **ICMR does not approve apps or devices.** CDSCO licenses devices. ICMR writes the ethics rules, runs the trial registry, funds research and runs help desks for innovators.
3. **The real touchpoints are five:** (a) ICMR's 2017 ethics guidelines, which every hospital ethics committee applies; (b) ICMR's 2023 AI ethics guidelines; (c) CTRI, run by an ICMR institute; (d) MedTech Mitra, Patent Mitra and the device mission (help, not approval); (e) ICMR grants and the INTENT trial network (not open to students directly).
4. **Before the first real patient, the team needs one thing above all: approval from a registered ethics committee.** A researcher cannot decide for themselves that a study is "low risk"; the committee decides (ICMR 2017, section 4.8.3).
5. **Our consent design already matches much of ICMR 2017** (own language, read aloud, easy withdrawal). **Gaps:** no impartial literate witness for patients who cannot read, no participant information sheet, no compensation or insurance plan, no ethics-committee sign-off of the electronic consent method.
6. **CTRI registration is free, must be done before the first patient, and review takes about 10 working days.** It is mandatory only for regulatory trials, but journals and many ethics committees demand it. Register every patient study anyway.
7. **Whether a patient pilot of our unlicensed measuring unit needs CDSCO permission is NOT CONFIRMED.** Device "clinical investigations" need CDSCO permission (Forms MD-22/MD-23). Ask CDSCO through MedTech Mitra before the pilot.
8. **No Indian professional-society guideline recommending incentive spirometry was found.** The only Indian government document found that names the spirometer is the draft TB pulmonary-rehab guidance (ledger #176). The US guideline (ledger #42) says not to rely on it alone.
9. **ABDM is not needed for a pilot.** It matters later, when a hospital wants our sessions inside the patient's record. Passing the test environment is reported by vendors to take months, not weeks.
10. **Never say "ICMR approved", "ABDM compliant" or "clinically validated".** Say "designed to follow ICMR's ethics guidelines; not yet reviewed by any ethics committee".

## Findings

### B5-1: ICMR is a research body, not a regulator; it does not approve apps or devices
- Detail: ICMR's own innovator portal describes its role as "handholding" for clinical evaluation, regulatory facilitation and adoption, done *in partnership with* CDSCO. Device licensing sits with CDSCO under the Medical Devices Rules 2017 (ledger #183). ICMR's 2017 guideline itself says CTRI registration "was made mandatory by CDSCO", which shows who the regulator is.
- Source: MedTech Mitra "About" – https://medtechmitra.icmr.org.in/about – grade A (government page); ICMR National Ethical Guidelines 2017, section 3.7 – https://ethics.ncdirindia.org/asset/pdf/ICMR_National_Ethical_Guidelines.pdf – grade A; ledger #183.
- Status: CONFIRMED
- What it means for SpiroBuddy: there is no such thing as "ICMR approval" for us to seek or claim. The honest line is "we follow ICMR's ethics guidelines".

### B5-2: The complete list of ICMR touchpoints, and where there is NO connection
| Touchpoint | What it is | Connection to SpiroBuddy today |
|---|---|---|
| National Ethical Guidelines 2017 | The rulebook every Indian ethics committee applies | None yet. Applies the day we study real people. |
| AI ethics guidelines 2023 | Principles for AI in health | None yet. We can map our design to them (B5-9). |
| CTRI | Public trial registry, run by ICMR's National Institute of Medical Statistics | None. No study registered. |
| MedTech Mitra | Help desk with CDSCO for innovators | None. Not applied. |
| Patent Mitra | Patent-filing help | None. Not applied; eligibility for us unclear (B5-13). |
| Device mission (MDMS) | Schemes and centres for device makers | None. |
| Extramural grants | Research money | None. Students cannot be lead investigators (B5-14). |
| INTENT | ICMR's network of trial hospitals | None. |
| ICMR approval / certification of apps | Does not exist | Not applicable. |
- Source: as cited in B5-1, B5-3 to B5-15.
- Status: CONFIRMED (that the touchpoints exist); the "none" column is the team's own position (BRIEF: no real users, no company).
- What it means for SpiroBuddy: in the pitch, "connection with ICMR" means "the rules we will follow and the doors we will knock on", not a relationship.

### B5-3: ICMR 2017 – the ethics committee, not the researcher, decides the risk level and the type of review
- Detail: *National Ethical Guidelines for Biomedical and Health Research Involving Human Participants*, ICMR, October 2017. Table 2.1 sets four risk levels: less than minimal, minimal (harm no greater than daily life or routine tests such as history-taking and physical examination), minor increase over minimal, and more than minimal. Section 4.8 sets three review routes: exemption (less than minimal risk, no identifiers), expedited (no more than minimal risk) and full committee. Section 4.8.3: "A researcher cannot decide that her/his proposal falls in the exempted, expedited or full review category". Section 7.7 covers device studies and uses the same A–D classes as CDSCO.
- Source: ICMR 2017 guideline (text extracted and read) – https://ethics.ncdirindia.org/asset/pdf/ICMR_National_Ethical_Guidelines.pdf – grade A.
- Status: CONFIRMED (primary text)
- What it means for SpiroBuddy: our reading is that a coaching study with a non-invasive unit could be argued as minimal risk, but post-surgery and older patients, identifiable health data and phone calls make full review likely. Do not write "exempt" anywhere. Ask the committee.

### B5-4: ICMR 2017 consent rules, mapped to what SpiroBuddy has
| ICMR 2017 requirement (section) | What SpiroBuddy has (report 7.5) | Gap |
|---|---|---|
| Written informed consent before any study step (2.2.1, 5.1.4) | Spoken yes plus date, stored | No signed or thumb-print form. Verbal-only consent is allowed only "in exceptional circumstances" with EC approval (5.3.8). |
| Information in a language the person understands, simple and culturally sensitive (5.2.1) | Consent read aloud in the patient's language, itemised data list | Wording not yet checked by native speakers (report 11.1 item 5). |
| Two-part document: participant information sheet + consent form, both approved by the EC (2.2.1, 5.2.2) | A consent script for the service | No research information sheet (purpose, risks, right to refuse, who to call, compensation). |
| If the participant cannot read: an **impartial literate witness**, not a relative and not on the study team, present throughout, who signs (5.3.6, 5.4.3) | Read-aloud consent | No witness step. A son or daughter does not qualify. |
| Audio or video recording may document consent; all three people in frame for verbal consent (5.3.8); AV recording required only for certain CDSCO-notified trials (2.2.2) | None | Decide with the EC. Recording needs its own consent. |
| Electronic consent allowed (text, audio, video, interactive sites) but the process, signature method, privacy and security "must be reviewed and approved by the EC a priori" (5.5) | In-app, voice-led consent | Not reviewed by any EC. |
| Free to ask questions, take time, talk to family; no pressure (5.3.4, 5.3.5) | One-word STOP; weekly "keep reminders?" renewal | Good. Add "refusing does not affect your care". |
| Re-consent when things change (2.2.3, section 5) | Weekly renewal for calls | Stronger than required for calls; define re-consent for protocol changes. |
| Privacy: code or anonymise, limit access, no identifying publication (2.3) | Minimal data to the AI; fake patients only | Need a written data plan for real data (where stored, who sees it, how long). |
- Source: ICMR 2017 guideline, sections cited – same URL – grade A.
- Status: CONFIRMED (primary text). The right-hand columns are the team's own assessment.
- What it means for SpiroBuddy: the voice-first consent is a real strength for people who cannot read, but for *research* it must sit beside a witness and a signed or thumb-printed form.

### B5-5: Vulnerable groups – "elderly" is not a named group, but many of our patients will count as vulnerable
- Detail: Section 6 defines vulnerable persons as those "relatively or absolutely incapable" of protecting their own interests, and lists among others the economically and socially disadvantaged, the cognitively impaired, the terminally ill, and people in dependent relationships. The word "elderly" appears only once (6.7.7, tribal groups). Research with vulnerable groups goes to full committee review.
- Source: ICMR 2017 guideline, section 6 – same URL – grade A.
- Status: CONFIRMED (primary text)
- What it means for SpiroBuddy: age alone is not the test. Low literacy, poverty, post-surgery pain and dependence on the ward nurse are. Recruitment must not be done by the patient's own treating nurse alone.

### B5-6: Compensation and insurance – in a student study the host institution becomes the "sponsor"
- Detail: Section 2.6: participants harmed by the research are entitled to compensation; medical care is free if harm is research-related; serious adverse events go to the EC within 24 hours, with a relatedness report within 14 days. Section 2.6.4: "In investigator initiated research/student research, the investigator/institution where the research is conducted becomes the sponsor" and must provide compensation or insurance cover. The EC checklist asks for an insurance policy "if applicable".
- Source: ICMR 2017 guideline, sections 2.6, 4 – same URL – grade A.
- Status: CONFIRMED (primary text)
- What it means for SpiroBuddy: the hospital will ask "who pays if something goes wrong?". No sourced premium was found; get a quote. A company or institution must stand behind the study; a student team on its own cannot.

### B5-7: Ethics committees must be registered with the Department of Health Research (and with CDSCO for regulated trials)
- Detail: The New Drugs and Clinical Trials Rules 2019, Chapter IV, require any committee reviewing biomedical and health research to register with the authority designated by the Government, which is DHR, through the "Naitik" portal; the registry is called NECRBHR. Provisional registration lasts 2 years, final 5 years. Committees that review clinical trials must *also* register with CDSCO (SUGAM portal), valid 5 years.
- Source: "Registration of ethics committees" article – https://pmc.ncbi.nlm.nih.gov/articles/PMC10718093 – grade A (peer-reviewed). DHR's own page returned HTTP 403 (not read); search snippet of it agrees (C).
- Status: CONFIRMED (one peer-reviewed source plus snippet of the primary page)
- What it means for SpiroBuddy: before approaching a hospital, ask one question: "Is your ethics committee registered with DHR (NECRBHR), and with CDSCO?" If not, its approval may not be accepted by CTRI, journals or CDSCO.

### B5-8: CTRI – free, prospective only, about 10 working days; mandatory only for regulatory trials
- Detail: CTRI is "managed by the ICMR-National Institute of Medical Statistics, New Delhi". Registration of regulatory trials is mandatory. Since **1 April 2018** only prospective registration is accepted (before the first participant). **No fee.** CTRI reviews a submission within **10 working days**; total time depends on the registrant's replies. Ethics-committee approval must be uploaded; regulator approval "where applicable". CTRI registers all study types, including observational ones. ICMR 2017 section 3.7: registration "is voluntary for other biomedical and health research"; section 3.7.1 says device, educational, behavioural and observational studies "may be registered prospectively".
- Source: CTRI FAQ – https://ctri.nic.in/Clinicaltrials/faq.php – grade A; ICMR 2017 guideline section 3.7 – grade A.
- Status: CONFIRMED (two primary sources)
- What it means for SpiroBuddy: a feasibility study of a coaching device is not legally forced to register unless it is a regulatory trial, but it costs nothing and unregistered studies are hard to publish. Register the usability study, the pilot and the controlled study. Order: EC approval first, then CTRI, then first patient.

### B5-9: ICMR's 2023 AI ethics guideline – principle by principle
*Ethical Guidelines for Application of Artificial Intelligence in Biomedical Research and Healthcare*, ICMR (DHR-ICMR AI Cell), 2023, 76 pages, ISBN 978-93-5811-343-3. Sections: ethical principles; guiding principles for stakeholders; ethics review process; governance; informed consent. **The official PDF could not be opened (over the 10 MB tool limit). The ten principle names below come from several secondary reports that agree; the "requires" column is from those reports and one peer-reviewed review. Check exact wording in the PDF before quoting.**

| Principle | What it requires (as reported) | What SpiroBuddy has | Gap |
|---|---|---|---|
| Autonomy | Human oversight of the AI ("human in the loop"); a person can override it; patients consent and may refuse AI | Fixed rules, not the AI, decide alerts; a nurse reviews the dashboard; every message says it is automated; one-word STOP | No way yet for a patient to choose "nurse only, no AI coach" while staying in the programme |
| Safety and risk minimisation | Prevent misuse; secure systems; ethics committee weighs benefit against risk | Red-flag words skip the AI and give a fixed "contact your nurse / call 112" message; the AI never diagnoses | No formal risk file (ISO 14971); no security test; no EC review |
| Trustworthiness | Reliable, explainable, transparent tools | Breath judgement is rule-based and explainable; template fallback when the AI fails | No published description of the model or its limits |
| Data privacy | Privacy protected at every stage; anonymise | Only first name and the day's numbers go to the AI; fake patients only | Patient data is stored in India (Mumbai) but the web server that serves the pages is outside India today (report 7.3); no written data plan for real data |
| Accountability and liability | Regular internal and external audits; clear responsibility for faults | Message log exists | No audit plan; no legal entity to hold liability |
| Optimisation of data quality | Training data large enough and representative of Indian patients | Breath model tested only on synthetic breaths (95.8%) | **Largest gap.** No real breath data at all |
| Accessibility, equity and inclusiveness | Bridge the digital divide; native-language interfaces | 11 languages, voice-first, phone calls for people without smartphones | Not tested with older listeners; wording unchecked in three languages |
| Collaboration | Work across disciplines and stakeholders | Plans call for a nurse or physiotherapist to agree alert rules | No clinician has done so yet (report 11.1 item 11) |
| Non-discrimination and fairness | No bias in data or results; a way to raise concerns | Same rules for every patient | No check that accuracy holds across age, sex, lung size, device model; no complaints route |
| Validity | Clinical and field validation before use; testing at each new site | None | No validation on real people. Hence never say "clinically validated" |

The guideline also asks ethics committees reviewing AI studies to look at data source, quality, anonymisation, selection bias, participant protection and compensation, and to include members with AI and legal knowledge.
- Source: ICMR guideline landing page – https://www.icmr.gov.in/ethical-guidelines-for-application-of-artificial-intelligence-in-biomedical-research-and-healthcare – grade A (sections, year, ISBN only); Zenodo record – https://zenodo.org/record/8262489 – grade A (same); "AI in neurology … an Indian perspective" – https://pmc.ncbi.nlm.nih.gov/articles/PMC12000087/ – grade A (human in the loop, accountability, validation, native language, consent, right to be forgotten); Down To Earth news report – https://www.downtoearth.org.in/news/health/icmr-releases-guidelines-for-artificial-intelligence-use-in-the-health-sector-88338 – grade B (names 9 of the 10 principles); search snippets of other reports – grade C.
- Status: SINGLE SOURCE for each description (secondary); the existence, year and section list are CONFIRMED. Whether the guideline is legally binding: NOT CONFIRMED (described everywhere as "ethical guidelines"; no source called it law).
- What it means for SpiroBuddy: we can honestly say the design follows several principles (human oversight, native language, minimal data). We cannot claim validity or data quality.

### B5-10: Does a patient pilot need CDSCO permission? Not confirmed – ask before starting
- Detail: Under the Medical Devices Rules 2017, a clinical investigation of an investigational device needs permission from CDSCO (apply in Form MD-22, permission in MD-23), with ethics approval and consent forms per the Seventh Schedule. A CDSCO flowchart reportedly says clinical investigation is "not mandatory" for Class A devices. The academic-study exemption found in searches applies to **drugs**; no equivalent for devices was found. We expect our unit to be Class B (report 7.1).
- Source: search snippets of CDSCO's MD-22 checklist and consultancy pages – grade C (snippet only, not opened); ledger #183 for the Rules themselves (not re-opened).
- Status: NOT CONFIRMED
- What it means for SpiroBuddy: our reading is that a hospital pilot of an unlicensed Class B measuring unit on patients may count as a clinical investigation needing CDSCO permission; a bench test and a healthy-volunteer usability test of the *software and fit* are less likely to. Confirm with CDSCO (through MedTech Mitra) or a regulatory consultant before acting.

### B5-11: MedTech Mitra – a free question desk run by ICMR with CDSCO, for innovators and startups
- Detail: "Handholding MedTech Innovators For Clinical Evaluation". Led by ICMR with CDSCO, under NITI Aayog's guidance; coordinated by ICMR's Division of Development Research. Gives guidance on regulatory requirements, testing and validation, production, clinical evaluation and technology assessment. Partners include Atal Innovation Mission, the INTENT network, Kalam Institute of Health Technology and HTAIn. To apply: fill in the product and its stage online and "request guidance"; an ICMR–CDSCO team then discusses it one to one. The page names "innovators or startups" and gives no formal eligibility list, fee or deadline.
- Source: MedTech Mitra "About" – https://medtechmitra.icmr.org.in/about – grade A. Search snippet of the ICMR page: aimed at "leads ready for clinical validation" – grade C.
- Status: SINGLE SOURCE (primary). Launch date and whether an unregistered student team may apply: NOT CONFIRMED.
- What it means for SpiroBuddy: this is the one ICMR door worth knocking on first. Use it to ask the two open questions: our device class, and whether the pilot needs CDSCO permission.

### B5-12: INTENT – ICMR's clinical trial network of about 75 sites, which covers devices
- Detail: Indian Clinical Trial and Education Network, run by ICMR's Clinical Studies & Trials Unit. 75 sites for Phase II/III and 4 for Phase I, including public and private medical colleges. Scope includes medical devices and diagnostics. The FAQ does not say who may bring a study, how to apply or what it costs. Contact: intent@hq.icmr.org.in.
- Source: INTENT FAQ – https://intent.icmr.org.in/faq.html – grade A.
- Status: SINGLE SOURCE (primary)
- What it means for SpiroBuddy: relevant for the controlled study (step 4), not the first pilot. Reach it through MedTech Mitra, which lists INTENT as a partner.

### B5-13: Patent Mitra exists; students are not named as eligible
- Detail: "Medical Innovations Patent Mitra", an ICMR platform for patent filing, prosecution, maintenance and technology transfer. Eligible: ICMR institutes, ICMR-funded extramural grantees, medical colleges and institutes, **DPIIT-registered start-ups**, and institute-led biomedical innovators. Launch date (8 March 2025) and "zero-cost" come from search snippets of ICMR's newsletter, not opened.
- Source: Patent Mitra "About" – https://patentmitra.icmr.org.in/about/ – grade A; newsletter snippet – grade C.
- Status: SINGLE SOURCE (eligibility); cost and launch date NOT CONFIRMED (snippet only)
- What it means for SpiroBuddy: usable only after the team registers a startup with DPIIT, or files through a medical college partner. Prior-art search is still an open task (report 11.1 item 2).

### B5-14: ICMR research grants – the lead investigator must be a regular employee; the 2026 calls have closed
- Detail: The ICMR Small ("Anveshan") Extramural Grant call for 2026 closed **16 March 2026**; the Intermediate call closed 20 March 2026; both were released 19 December 2025. Eligibility, from search snippets of the call documents: scientists with "regular employment" in a medical college, research institute, university or recognised lab; a co-investigator from the same institution; apply online at epms.icmr.org.in. Students are not named; our reading is that they cannot be principal investigator. Budget for the small grant: "up to ₹2 crore" in an older call (snippet); 2026 figure not confirmed.
- Source: ICMR call page – https://www.icmr.gov.in/post/call-for-investigator-initiated-research-proposals-for-icmr-small-extramural-grants-icmr-anveshan-extramural-grants-2026-last-date-march-16-2026-5-00-pm-ist – grade A (name and date only); call-document snippets – grade C.
- Status: CONFIRMED (dates); SINGLE SOURCE / snippet (eligibility and amounts)
- What it means for SpiroBuddy: a faculty member at a medical college must lead any ICMR grant, with the team as collaborators. If the pattern repeats, the next call opens around December 2026 (team inference, not announced).

### B5-15: ICMR's device mission (MDMS) targets products past proof of concept
- Detail: Medical Device and Diagnostics Mission Secretariat, at ICMR headquarters, supports device R&D through to market. Programmes named: CLiMB (biodesign programmes with medical and engineering institutes), mPRiDE (support for products nearing commercialisation), mPRAGATI, CiBiOD, and ICMR-DHR Centres of Excellence. The page gives no eligibility or application details. A search snippet says Centres of Excellence were set up at six IITs (Bombay, Guwahati, Hyderabad, Kanpur, Kharagpur, Madras).
- Source: MDMS introduction – https://mdms.icmr.org.in/about-us/introduction.html – grade A; IIT list snippet – grade C.
- Status: SINGLE SOURCE
- What it means for SpiroBuddy: later-stage. A biodesign programme (CLiMB) at a nearby institute could be a home for the hardware build; check the "Call for Proposals" page.

### B5-16: No Indian professional-society guideline recommending incentive spirometry was found
- Detail: Searches for the Indian Chest Society, National College of Chest Physicians, Indian Association of Cardiovascular-Thoracic Surgeons, Indian Society of Anaesthesiologists and Indian Association of Physiotherapists found no recommendation on incentive spirometry. The 2019 joint ICS–NCCP guideline is about *diagnostic* spirometry, a different thing. The only Indian government document found that names the spirometer is the **draft** RBIPMT pulmonary-rehabilitation guidance for people affected by TB, July 2024 (ledger #176). The US guideline (AARC 2011, ledger #42) suggests a volume-type device but says not to use it alone.
- Source: search results only (snippets) – grade C; ledger #176 (A), #42 (A).
- Status: NOT CONFIRMED (absence of evidence after one round of searching; society websites were not opened)
- What it means for SpiroBuddy: do not say "recommended by Indian guidelines". Say "widely prescribed after surgery in India; named in the Government's draft TB rehab guidance".

### B5-17: ABDM – what joining means, and why a pilot does not need it
- Detail: Joining means building against NHA's test environment ("sandbox") in milestones: **M1** create and verify the patient's ABHA health ID; **M2** act as a Health Information Provider (share records, with the patient's consent, as FHIR bundles – FHIR is the standard record format); **M3** act as a Health Information User (read records held elsewhere). A consent manager app sits between patient and both sides. A May 2023 Government release (snippet) counted 53 apps at M2 and 45 at M3, including private ones. Reported exit steps: functional testing, a security audit by a CERT-In empanelled firm ("Safe-to-Host" certificate), a demo to NHA, then production keys. A vendor says NHA wants **at least two milestones** to exit and that this is not in any published circular. Vendor time estimates: 4–9 months. The Indian FHIR profile set has no lung-function or device profile (ledger #199).
- Source: vendor blog – https://nirmitee.io/blog/does-your-platform-need-abdm-certification-non-hims-guide/ – grade C; forum and PIB snippets – grade C; ledger #199 (A), #200 (A/C). The official sandbox site (https://sandbox.abdm.gov.in/) returned only a page title.
- Status: NOT CONFIRMED from a primary NHA source (milestone meanings agree across several sources; exit steps and times are vendor claims)
- What it means for SpiroBuddy: our reading is that a pilot run under the hospital's own ethics approval needs no ABDM link. A hospital is likely to ask instead: where is the data stored, who can see it, and can we export it. Offer a PDF or CSV export now and "ABDM-ready design" later. The cheapest later route is to plug into the hospital's already-certified records system rather than certify ourselves.

### B5-18: NHA's Health Data Management Policy and the Digital Health Incentive Scheme
- Detail: The Health Data Management Policy was approved on 14 December 2020; it sets minimum privacy standards for ABDM participants, is read alongside the law, and treats health data as sensitive personal data; a revised draft followed in April 2022. The incentive scheme pays hospitals and "digital solution companies" per record linked to ABDM (reported as ₹20 per record above 100 a month, capped at ₹4 crore; an older deck gave different figures). Whether it runs past June 2025: not confirmed.
- Source: search snippets only – grade C; ledger #200 for the scheme's guidelines (A, not re-opened).
- Status: NOT CONFIRMED (snippets; figures changed over time)
- What it means for SpiroBuddy: do not put incentive money in the business case. Do not quote the ₹ figures in the pitch.

### B5-19: Other national programmes – no documented route for third-party tools was found
- Detail: eSanjeevani (the Government telemedicine service) was itself integrated with ABDM in June 2022; that is a platform link, not an open interface for outside apps. Nothing was found describing a developer route into Nikshay (the TB programme's system), Ayushman Arogya Mandirs (primary health centres), the National Programme for Health Care of the Elderly, or any state post-discharge follow-up programme.
- Source: search snippets only – grade C.
- Status: NOT CONFIRMED (absence after one search)
- What it means for SpiroBuddy: the only documented door into national systems is ABDM. For TB, the realistic route is a pilot with a state TB cell or an NTEP-linked institute, not an API.

### B5-20: Sample-size logic for pilots – about 30 is typical, 12 per group is the usual floor
- Detail: Julious (2005) recommends 12 per group for a pilot with no prior data. An audit of UK pilot trials found a median of 30 per arm. A 2023 review of 761 UK pilot and feasibility studies found a median target of 30 (middle half: 20–50), and 57% missed their target. Reporting standards say pilot size should be justified by feasibility aims, not by power.
- Source: search snippets of the papers (PMC10662929; Julious 2005; Billingham 2013) – grade C as read (peer-reviewed, not opened). Global, not Indian.
- Status: SINGLE SOURCE (snippet)
- What it means for SpiroBuddy: "30–50 patients" for the feasibility pilot is in line with normal practice. Plan for under-recruitment.

## The evidence plan, in order (sized for a student team)
Headline metric throughout: **share of due hourly sessions completed** (sessions done ÷ sessions due in waking hours). Times are team estimates. All sample-size arithmetic below is a **team assumption** to be redone by a statistician.

| Step | Question it answers | Design | Primary outcome | Size and logic | Approvals | Time |
|---|---|---|---|---|---|---|
| 1. Bench accuracy | Does the sensor read the disc height, and volume, correctly? | No people. Compare sensor readings with the printed volume marks, then with a calibration syringe (a syringe that pushes a known volume of air), on several spirometers | Mean error in mL and limits of agreement | e.g. 5 units × 6 volumes × 10 repeats (team assumption) | None (no human participants) | 2–4 weeks after hardware exists |
| 2. Usability, healthy volunteers | Can people set it up and follow the voice coach? Does the breath judgement match an observer? | 15–20 adults including older adults, 2–3 languages; observed tasks; observer vs software on each breath | Task completion; agreement of software with observer | 12 is the usual floor (B5-20); 15–20 gives room for language groups | **Ethics committee** (these are human participants; likely expedited – the EC decides). CTRI: optional, register anyway. CDSCO: our reading is no; confirm | 1–2 months incl. EC |
| 3. Feasibility pilot, one hospital | Will post-surgery patients use it, and can the ward run it? | Single arm, 30–50 patients after chest or abdominal surgery, in hospital and for 1–2 weeks at home | Share of due sessions completed, with a confidence interval; also recruitment and drop-out rates, nurse time, harms | With 40 patients and a between-patient spread of 25 points (assumed), the mean is known to about ±8 points (1.96 × 25 ÷ √40) | **Full ethics committee review** (registered with DHR); **CTRI before first patient** (free, ~10 working days); insurance or compensation plan; **CDSCO: not confirmed – ask first (B5-10)** | 4–6 months |
| 4. Controlled study | Does it raise adherence versus usual care? (Not: does it prevent pneumonia) | Randomised, two arms: usual spirometer teaching vs the same plus SpiroBuddy; 1–3 hospitals | Difference in share of due sessions completed; in the control arm this needs a silent sensor or it cannot be measured | To detect a 20-point difference with a 30-point spread, 80% power: about 36 per arm, ~45 with drop-outs (assumed). Anchor: reminders gave 58% vs 28% of waking hours (ledger #2) | Full EC at each site; CTRI; CDSCO permission likely; ideally via INTENT (B5-12) and an ICMR grant led by a faculty investigator (B5-14) | 9–15 months |

**Who can host.** Not found: any published list of hospitals that host student or startup pilots. What the sources do show: INTENT's 75 sites include public and private medical colleges; ICMR-DHR Centres of Excellence sit at six IITs (snippet); MedTech Mitra partners with Kalam Institute of Health Technology. Team assumption: the most realistic host is a teaching hospital linked to the team's own university, with a physiotherapy or surgery faculty member as principal investigator.

**How to approach an ethics committee.** First find a faculty principal investigator at the hospital; committees accept applications from their own staff. Then prepare: (1) protocol; (2) participant information sheet and consent form in English and each local language, with the witness line; (3) the electronic and voice consent method, described for approval; (4) investigator CVs and research-ethics training certificates; (5) device description, safety notes and the statement that it coaches and never diagnoses; (6) data plan (storage in India, access, retention, withdrawal); (7) insurance or compensation statement from the host institution; (8) case record forms and the adverse-event reporting plan (24 hours / 14 days); (9) budget and funding source; (10) AI description: what the model does, what data it saw, how a human overrides it. Items 1, 2, 4, 7 and 8 come from ICMR 2017; item 10 from the 2023 AI guideline.

## What to say in the 5-minute pitch (5 bullets max, each with its source)
- "ICMR does not approve apps. It sets the ethics rules. We have designed our consent to those rules: in the patient's language, read aloud, and one word to stop." (ICMR 2017, sections 5.2–5.5)
- "No real patient has used this yet. Our first real study will go to a registered hospital ethics committee and will be registered on CTRI before the first patient. Registration is free." (CTRI FAQ; ICMR 2017 section 3.7)
- "The AI never decides alerts and never diagnoses; fixed rules and a nurse do. That is the 'human in the loop' ICMR's 2023 AI guideline asks for." (ICMR 2023 guideline, as reported; PMC12000087)
- "Our evidence plan has four steps: bench test, healthy volunteers, a 30–50 patient pilot, then a controlled study. We measure one thing: the share of due hourly sessions completed." (this document; ledger #2 for the anchor)
- "Our first call after the hackathon is MedTech Mitra, the ICMR–CDSCO help desk for innovators." (MedTech Mitra About page)

## What NOT to say (claims that would be wrong or unproven)
- **"ICMR approved / certified / endorsed / recognised."** No such approval exists and ICMR has not seen the product.
- **"ICMR compliant"** as a flat claim. Say "designed to follow ICMR's ethics guidelines; not yet reviewed by an ethics committee".
- **"Ethics approved"** or "IEC cleared". No committee has reviewed anything.
- **"Clinically validated", "clinically proven", "tested on patients".** Tested on synthetic breaths only.
- **"ABDM compliant", "ABDM integrated", "ABHA enabled".** No sandbox work has been done. "Designed so records can later be exported in the ABDM format" is the most that is true.
- **"CTRI registered"**, **"CDSCO approved"**, **"exempt from ethics review"**, **"low risk, so no approval needed"**.
- **"Recommended by Indian guidelines"** for incentive spirometry. None was found.
- **"Supported by MedTech Mitra / Patent Mitra / INTENT."** We have not applied.
- Any ₹ figure for ABDM incentives.

## First 90 days: concrete next steps (who does what, rough cost in ₹ where a source gives one)
1. **Week 1 – team lead:** submit a guidance request on MedTech Mitra asking (a) our device class and (b) whether a hospital pilot needs CDSCO permission. Cost: no fee stated on the portal.
2. **Weeks 1–3 – team lead:** find a faculty principal investigator (physiotherapy, surgery or anaesthesia) at a teaching hospital. Ask whether its ethics committee is registered with DHR and CDSCO.
3. **Weeks 2–4 – hardware lead:** build two units and run the bench test (step 1). No approval needed. Parts cost: see report 4.6.
4. **Weeks 2–6 – all:** write the protocol, information sheet and consent form for step 2; get Hindi, Tamil and Malayalam wording checked by native speakers; add the impartial-witness step and a thumb-print or signature form.
5. **Weeks 4–8 – software lead:** write the one-page AI description and the data plan; move any real-data hosting to India before any real person is enrolled (report 7.3).
6. **Weeks 6–10 – investigator:** submit to the ethics committee; ask the host institution for its compensation or insurance arrangement. No sourced premium found; get a quote.
7. **After EC approval:** register on CTRI. **Cost: ₹0** (CTRI FAQ). Allow 10 working days plus replies.
8. **Weeks 10–13:** run the healthy-volunteer usability study.
9. **By December 2026 – investigator:** watch ICMR's call-for-proposals page for the next small-grant call (the last one opened 19 Dec 2025). **Founders:** if registering a startup, add DPIIT recognition so Patent Mitra becomes available.

## Open questions (what you could not find, and who could answer it)
- Exact wording and numbering of the ten principles in ICMR's 2023 AI guideline, and its legal status. *Who:* anyone who downloads the PDF from icmr.gov.in in a browser.
- Whether a hospital pilot of our unlicensed unit is a "clinical investigation" needing CDSCO permission; whether any academic exemption exists for devices. *Who:* CDSCO via MedTech Mitra; a regulatory consultant.
- Whether an unregistered student team may apply to MedTech Mitra; its launch date; any fee. *Who:* the portal's contact desk.
- Whether students may be co-investigators on ICMR grants; the 2026 small-grant budget ceiling. *Who:* the 2026 call PDF; ICMR's extramural desk.
- Any Indian society guideline on incentive spirometry (society websites not opened). *Who:* a chest physician or cardiothoracic physiotherapist.
- The official NHA sandbox exit steps, the "two milestones" rule, real time and cost; whether the incentive scheme is still running. *Who:* NHA integration support; a hospital IT head.
- Whether ABDM participation is voluntary for a tool like ours (assumed, not sourced this round). *Who:* NHA.
- The cost of clinical-trial insurance for a 40-patient device pilot. *Who:* an insurer or the host hospital's research office.
- Which hospitals near the team host student pilots, and their ethics-committee fees and meeting dates. *Who:* the team's own university research office.
- Any documented third-party route into Nikshay, Ayushman Arogya Mandirs or elderly-care programmes. *Who:* a state TB officer or state health mission.
- Whether ICMR has revised the 2017 ethics guideline since. *Who:* ICMR Bioethics Unit website.

## Sources opened this round
| # | URL | title | publisher | grade | used in |
|---|---|---|---|---|---|
| 1 | https://ctri.nic.in/Clinicaltrials/faq.php | CTRI Frequently Asked Questions | ICMR-National Institute of Medical Statistics | A | B5-8 |
| 2 | https://medtechmitra.icmr.org.in/about | MedTech Mitra – About | ICMR / CDSCO | A | B5-1, B5-11 |
| 3 | https://www.icmr.gov.in/ethical-guidelines-for-application-of-artificial-intelligence-in-biomedical-research-and-healthcare | AI ethics guideline 2023 – landing page (sections, ISBN only) | ICMR | A | B5-9 |
| 4 | https://ethics.ncdirindia.org/asset/pdf/ICMR_National_Ethical_Guidelines.pdf | National Ethical Guidelines for Biomedical and Health Research Involving Human Participants, Oct 2017 (text extracted and read) | ICMR (Bioethics Unit, NCDIR) | A | B5-1, B5-3 to B5-6, B5-8 |
| 5 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12000087/ | Artificial intelligence in neurology, ethics, recent guideline, and law – an Indian perspective | peer-reviewed, via PMC | A | B5-9 |
| 6 | https://www.icmr.gov.in/post/call-for-investigator-initiated-research-proposals-for-icmr-small-extramural-grants-icmr-anveshan-extramural-grants-2026-last-date-march-16-2026-5-00-pm-ist | ICMR Small (Anveshan) Extramural Grants 2026 – call page (name and date only) | ICMR | A | B5-14 |
| 7 | https://zenodo.org/record/8262489 | Ethical Guidelines for Application of AI in Biomedical Research and Healthcare, India, 2023 (record page only) | ICMR via Zenodo | A | B5-9 |
| 8 | https://indiaai.gov.in/news/icmr-releases-ethical-guidelines-for-ai-in-biomedical-research-and-healthcare | ICMR releases ethical guidelines for AI (page truncated, nothing read) | IndiaAI (government) | B | none |
| 9 | https://sandbox.abdm.gov.in/ | ABDM Sandbox (page title only, nothing read) | NHA | A | B5-17 (noted as unreadable) |
| 10 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10718093 | Registration of ethics committees with DHR and CDSCO | peer-reviewed, via PMC | A | B5-7 |
| 11 | https://www.downtoearth.org.in/news/health/icmr-releases-guidelines-for-artificial-intelligence-use-in-the-health-sector-88338 | ICMR releases guidelines for AI use in the health sector (2023) | Down To Earth | B | B5-9 |
| 12 | https://intent.icmr.org.in/faq.html | INTENT FAQ | ICMR | A | B5-12 |
| 13 | https://patentmitra.icmr.org.in/about/ | Medical Innovations Patent Mitra – About | ICMR | A | B5-13 |
| 14 | https://mdms.icmr.org.in/about-us/introduction.html | About MDMS | ICMR | A | B5-15 |
| 15 | https://nirmitee.io/blog/does-your-platform-need-abdm-certification-non-hims-guide/ | Does your platform need ABDM certification? | Nirmitee (vendor blog) | C | B5-17 |

**Tried and failed (not read):** https://www.icmr.gov.in/icmrobject/custom_data/pdf/Ethical-guidelines/Ethical_Guidelines_AI_Healthcare_2023.pdf (over the 10 MB tool limit); https://dhr.gov.in/national-ethics-committee-registry-biomedical-and-health-research-necrbhr (HTTP 403).

**Search snippets only, not opened (grade C as read):** CDSCO MD-22 checklist and consultancy pages on device clinical investigations; ICMR 2023–2026 grant call PDFs; Patent Mitra newsletter; ICMR press note on IIT Centres of Excellence; PIB May 2023 release on ABDM integrations; ABDM developer-forum threads on sandbox exit; reports on the Health Data Management Policy (Dec 2020) and the Digital Health Incentive Scheme; Julious 2005, Billingham 2013 and the 2023 ISRCTN pilot-size review (PMC10662929); ICS–NCCP spirometry guideline 2019; other news summaries of the ICMR AI guideline.

**Ledger sources cited, not re-opened:** #2, #42, #176, #183, #199, #200.
