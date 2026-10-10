# Legal deep dive (second pass): closing the open items and covering what the first pass missed

**Written:** 10 Oct 2026 · **Sources newly opened:** 23 (17 read, 6 blocked or empty) · **Confidence overall:** medium. High where we read the rule itself (Medical Devices Rules, Bharatiya Nyaya Sanhita, E-waste amendment, accessibility rules, procurement order, WPC FAQ). Low where we had only search snippets or general knowledge (company law deadlines, tax rates, fees, case law).

> **This is a map of the law with sources. It is NOT legal advice.** Every "our reading" is the team's reading of a rule. Rules change. Before acting on any item, confirm with the adviser named at the end of that area.

**How to read this file**
- It does not repeat the first pass. First-pass findings are cited by their ID (B4-6, B5-4, B6-15 and so on) from `docs/research/business/`.
- **Status words:** CONFIRMED = we read the primary text, or two independent sources agree. SINGLE SOURCE = one secondary source. NOT CONFIRMED = snippets only, or general knowledge we did not check this round.
- **"General knowledge"** means the researcher knows the rule from training but did not open a source this round. Treat every such line as a question for the adviser, not as a fact.
- **Grades:** A = Act, Rule, regulator text · B = law firm, major outlet, official company page · C = blog, vendor, or a search snippet not opened.
- Short forms: **CDSCO** (India's medical-device regulator) · **MDR 2017** (Medical Devices Rules 2017) · **CLA** (Central Licensing Authority, i.e. CDSCO) · **EC** (ethics committee) · **DPDP** (Digital Personal Data Protection Act 2023) · **WPC** (the radio-spectrum wing of the telecom department) · **ETA** (Equipment Type Approval, the radio approval) · **BIS** (Bureau of Indian Standards) · **CPCB** (Central Pollution Control Board) · **GST** (Goods and Services Tax) · **RMP** (registered medical practitioner, i.e. a doctor on the medical register).

**Two corrections to the first pass**
1. The E-Waste (Management) Rules 2022 are **G.S.R. 801(E) dated 2 Nov 2022** (in force 1 Apr 2023). B4-12 gave "G.S.R. 823(E), 22 Jul 2022". Source: the amendment notification G.S.R. 61(E) of 30 Jan 2023, which names the principal rules (L-5).
2. B4-11 said the radio approval for the finished product was "not confirmed". The WPC's own FAQ answers it: **no separate approval for an India-made product that uses an already-approved module unchanged** (L-2).

---

# PART A – Closing the open items

## L-1: Does a first patient study with an unlicensed prototype need CDSCO permission? (closes B4-6, B5-10)

**The question.** Is ethics-committee approval enough, or must we also get CDSCO permission (apply in Form MD-22, receive Form MD-23)?

**What the rule says (operative words, MDR 2017 as amended to 14 Oct 2022).**
| Rule | Operative words (short quotes) |
|---|---|
| 49 | No one may run "any clinical investigation in respect of investigational medical device" in people except "in accordance with the permission granted by the Central Licensing Authority". |
| 3(l) | A clinical investigation is "the systematic study of an investigational medical device in or on human participants" to assess "safety, performance or effectiveness". |
| 3(x) | An investigational medical device is one "(i) which does not have its predicate device" **or** (ii) one that is already licensed and "claims for new intended use or new population or new material or major design change". |
| 3(zm) | A predicate device is "first time and first of its kind, approved for manufacture for sale or for import" by the CLA, with similar use, material and design. |
| 51(3) | "No permission for conduct of academic clinical study on licensed medical device shall be required" if the EC approves and the data is not used for a licence. |
| 51(2) proviso | "no fee shall be payable by any institute, organisation, hospital run or funded by" the Central or a State Government. |
| 31(1), 32(a) | A test licence covers small quantities "for the purpose of clinical investigations, test, evaluation, examination, demonstration or training", used "exclusively" for that, "at the place specified in the licence". |
| 53(i), (iii) | After permission: start only after EC approval; register on the Clinical Trial Registry "before enrolling the first participant". |
| 55 | Medical care and compensation fall on "the sponsor permitted under rule 52". |
| 63, 2nd proviso | For "investigational medical device of Class A, data on clinical investigation may not be required" for the licence, unless the CLA asks. |

**Our reading, in both directions.**

*Reading A – permission IS needed (the cautious reading, and the one we advise planning for).*
1. No device of our kind (a sensor base that tracks an incentive spirometer) is known to be approved in India. So it likely has **no predicate**. That puts it in limb (i) of rule 3(x): an investigational medical device.
2. Any planned, written-protocol study in patients that checks whether it works ("performance or effectiveness") is then a **clinical investigation**. Rule 49 requires permission. "Human participants" is not limited to patients, so using healthy volunteers does not avoid it.
3. The EC-only exemption in rule 51(3) is written for a **licensed** device. Ours is not.
4. A first-in-human study is a "pilot clinical investigation". Fee ₹1,00,000 (B4-6), **nil if a government-run or government-funded hospital is the sponsor**. Decision within 90 days (rule 52).

*Reading B – ethics committee only.*
1. If a predicate **does** exist, our unlicensed prototype falls in **neither** limb of rule 3(x). It is then not an "investigational medical device", so a study of it is not a Chapter VII "clinical investigation". (The licence route would be "substantial equivalence" to the predicate, rule 51(5).)
2. If the study does not assess the **device** at all – for example it only asks patients and nurses whether the screens are understandable, with the device's readings never used for care – it may be health research under the ICMR guidelines (B5-3) and not a device investigation. This is thin: "does the coach improve adherence?" is an effectiveness question.
3. Work that is clearly **not** a study on patients – bench accuracy tests, demonstrations to staff, staff training – is covered by the test licence wording itself ("test, evaluation, examination, demonstration or training").

**A third route the first pass under-weighted.** Rule 63 says clinical data "may not be required" to license a **Class A** investigational device. If CDSCO accepts Class A (measuring), the order could be: bench evidence → licence (Form MD-5 or a loan licence, B4-3) → **then** an academic study under rule 51(3) with EC approval only. That turns the hardest question into an ordinary one. If CDSCO says Class B, this route is not available on the text.

**What stays true under every reading.**
- The units must be lawfully made: a test licence (Form MD-13, ₹500 per device, B4-4), and used only at the place named in it.
- A registered EC must approve (B4-7, B5-7). Informed consent in the patient's language (B5-4).
- The MDR does not make an insurance policy compulsory: the Seventh Schedule asks for an insurance certificate "if any". **Compensation** for study injury is compulsory for a permitted sponsor (rule 55). ECs usually ask for cover anyway (B5-6).

- **Primary source:** Medical Devices Rules 2017, CDSCO consolidated copy "as amended vide GSR 777(E) dt. 14-10-2022" (source 1) – grade A.
- **Status:** CONFIRMED for the text. How it applies to us: **our reading, not a ruling**. We found **no CDSCO FAQ or guidance** on academic studies of unlicensed devices (searched; the only CDSCO checklist found is pre-2018, source 4).
- **Remaining doubt:** (a) whether a predicate exists; (b) Class A-measuring or Class B; (c) amendments after Oct 2022 (the 2026 changes in B4-3 were not read in primary form); (d) how CDSCO treats a hospital-led observational study in practice.
- **Confidence:** high on wording; **medium-low** on the outcome. Plan and budget for Reading A; ask in writing before the pilot.
- **Who to ask:** a CDSCO regulatory consultant, and CDSCO itself through MedTech Mitra (B5-11). Ask for the answer in writing.

## L-2: Radio approval (WPC ETA) – the finished product question is answered (closes B4-11)

- **What we found.** The WPC FAQ on ETA through self-declaration says: a product working in licence-exempt bands needs an ETA; but when the product is **made in India** and the approved radio module is "fitted in it without any modification/alteration; then no separate ETA is required for such finished product." Products **made outside India** need an ETA for each product before import. A search summary of the DoT clarification to its 26 Feb 2019 memo says the same: where the radio module is separate, the ETA applies only to the module.
- **Fee and time:** ₹10,000 for each product with one or more built-in radio modules, paid on the BharatKosh portal. The ETA has **no expiry** and no renewal. A radio test report from an accredited lab is needed. Once an ETA exists for a model, other people may use it to import that model without paying again. No processing time is stated; self-declaration certificates are generated on the Saral Sanchar portal.
- **Who holds it:** the applicant who files (manufacturer or importer). For an India-made unit with an approved module, the module's ETA is the one that counts.
- **Licence-exempt band (2.4 GHz):** this is what makes the self-declaration route available. It does not remove the need for an ETA on the module.
- **Source:** DoT/WPC "ETA FAQ" (copy hosted on Scribd, read through a text reader; the BSNL and DoT hosts were unreachable) – grade B for the host, A for the content; DoT clarification – search summary only – C. Ledger #295 (a real ETA certificate).
- **Status:** CONFIRMED for the India-made rule (FAQ text plus matching summary of the DoT clarification). Fee: SINGLE SOURCE (FAQ, undated, about 2019).
- **Remaining doubt:** the FAQ is old. New rules under the Telecommunications Act 2023 were not checked. Changing the antenna or transmit power counts as a modification.
- **What to do:** use an ESP32 module variant that has an ETA, with its stock antenna and firmware power limits; keep a copy of the certificate in the technical file. If the finished unit is ever **imported assembled**, it needs its own ETA.
- **Who to ask:** a WPC/telecom compliance agent (one email with the module's ETA number).

## L-3: If a 4G module and SIM are added later – M2M registration and TEC certification

- **Rule.** DoT guidelines of 8 Feb 2022, "Registration Process of M2M Service Providers (M2MSP) & WPAN/WLAN Connectivity Provider for M2M Services". They cover (a) anyone providing machine-to-machine services over a telecom operator's SIMs, **including companies that use such services inside their own products**, and (b) anyone using Bluetooth or Wi-Fi "for providing M2M connectivity for commercial purposes" in unlicensed spectrum. Captive, non-commercial use is also mentioned. Duties: follow the SIM know-your-customer rules, take connectivity only from licensed operators, protect privacy, and use only devices that meet TEC (Telecommunication Engineering Centre) standards where certification is mandatory. Earlier DoT instructions (2018) created M2M-only SIMs with restricted features and a 13-digit number series.
- **Applies when:** scale, and only if we ship a SIM. Whether a Bluetooth unit that talks only to the patient's own phone makes us a "WPAN connectivity provider" is **not clear** from the summary; our reading is that it does not (we provide a device, not connectivity), but the wording is wide.
- **MTCTE** (Mandatory Testing and Certification of Telecom Equipment, run by TEC): which module categories are covered today, fee and time: **not found**.
- **Source:** Khaitan & Co note, 11 Feb 2022 (source 8) – B; Bar & Bench commentary – snippet – C.
- **Status:** SINGLE SOURCE (secondary). Registration fee, MTCTE scope: NOT CONFIRMED.
- **What to do:** stay Bluetooth-to-phone for the pilot. Before any SIM version: buy a module already MTCTE-certified, take M2M SIMs from an operator or a registered M2M provider, and check registration.
- **Who to ask:** telecom compliance agent; the SIM provider's enterprise desk.

## L-4: BIS (closes B4-10 as far as public sources allow)

- **Listed parts:** lithium cells IS 16046 (Part 2) and battery packs IS 16046 (Part 1); power adaptors IS 13252 (Part 1) (B4-10, ledger #300). A MeitY direction of 3 Feb 2026 tightens rated-capacity checks on registered cells (snippet, C).
- **Finished unit:** not on the compulsory registration list (B4-10). No "wireless" entry was found that would catch a sensor base.
- **Embedded cell:** the only statement found is a 2015 industry note: cells and adaptors need their **own** registration even when they arrive inside a registered host product. Old, grade C.
- **Medical electrical standards:** BIS notified five medical-device standards in Aug 2026, including parts of IS 13450 (the Indian version of IEC 60601), with older editions allowed until 3 Feb 2027. This sets the standards; it does **not** by itself make a BIS mark compulsory. A Quality Control Order (an order that makes a BIS standard compulsory) exists or is proposed for medical gloves and was drafted for a few items (glucose meters, clinical thermometers and others); **none found for our product type**. Under MDR rule 7 a BIS standard, where one exists, is the standard a device is judged against (B4-5), so IS 13450 matters through the CDSCO licence, not through BIS.
- **Source:** search snippets (consultancy pages, a 2015 Kiwa update) – C; ledger #300 – A.
- **Status:** NOT CONFIRMED beyond B4-10. Tried: BIS services pages (search only).
- **What to do:** buy cells and adaptors that show a BIS registration number (R-number); keep supplier certificates. Version 1 with no battery and no adaptor in the box avoids the question.
- **Who to ask:** a BIS-recognised test lab.

## L-5: E-waste and battery waste (closes B4-12, extends B6-15)

- **E-waste: a micro enterprise is outside the rules.** CPCB's FAQ lists what the E-Waste (Management) Rules 2022 do not apply to; it includes a "Micro enterprise as defined in" the MSME Development Act 2006. So while the company is a registered micro enterprise (Udyam registration, L-23), the producer duties do not apply. They return when it outgrows "micro".
- **Is our product listed?** Schedule I has a medical-devices group (codes MDW1 to MDW10; "with the exception of all implanted and infected products"). Summaries list radiotherapy, cardiology, dialysis, pulmonary ventilators, nuclear medicine, lab diagnostics, analysers, imaging, and a general "other devices for diagnosis, treatment or monitoring" style entry. The exact wording of that last entry was **not read**. The January 2023 amendment (G.S.R. 61(E), read in full) only adds a lead exemption for medical devices.
- **Producer** = anyone who makes and offers to sell listed equipment "under its own brand", sells under its brand equipment made by others, or offers imported equipment for sale (B6-15, CPCB FAQ). Registration is on the CPCB portal. **Fee: not found in an official source.**
- **Batteries:** unchanged from B4-12. Using cells bought from an Indian battery producer creates no battery duty for us; importing cells does.
- **Source:** CPCB "FAQ E-waste" 23 Jan 2024 (ACMA-hosted copy, source 6) – A; G.S.R. 61(E) (source 3) – A; Schedule I list – snippets – C.
- **Status:** CONFIRMED (micro-enterprise exclusion; producer definition; rule number). NOT CONFIRMED (the exact Schedule I entry; fees; whether lending without selling makes us a producer).
- **Who to ask:** CPCB e-waste portal helpdesk; an environmental compliance consultant at the first sale.

## L-6: Legal Metrology (closes part of B4-5 and B6-13)

- **Pack declarations.** B6-13 (ledger #328) stands: since 2025 the MDR label rule governs device labels; whether maximum retail price and consumer-care lines are still needed on a retail box is not confirmed. Nothing new found.
- **Is a unit that shows millilitres a "measuring instrument" needing model approval?** Model approval applies to weights and measures **specified** in the Legal Metrology (General) Rules 2011. The medical items found in those rules are clinical thermometers and blood-pressure instruments (sphygmomanometers; a new Part for manual ones was notified 7 Jan 2026, snippet). **No entry for spirometers or breathing-volume devices was found.** Our reading: no model approval is needed, because the instrument type is not specified. An absence in search results is not proof.
- **Source:** search snippets (TaxGuru, Simpliance, a state copy of the Approval of Models Rules) – C.
- **Status:** NOT CONFIRMED.
- **Who to ask:** regulatory consultant (one line: "is a volume-indicating spirometer accessory a specified measuring instrument?").

## L-7: Data law in October 2026 – what is in force (closes B4-13, B4-14)

**Commencement (notification G.S.R. 843(E), 13 Nov 2025).**
| Date | What starts | In force today? |
|---|---|---|
| 13 Nov 2025 | Definitions, the Data Protection Board chapter, rule-making and related sections; section 44(1) and (3) | Yes |
| 13 Nov 2026 | Consent-manager registration (section 6(9), section 27(1)(d)) | No (5 weeks away) |
| 13 May 2027 | Everything that matters to us: notice, consent, security, breach reporting, patient rights, children, significant data fiduciaries, penalties, and **section 44(2)** | No |

- **Section 44(2)** is the clause that removes section 43A of the IT Act and with it the 2011 "SPDI" rules (the older rules that treat health records as sensitive and ask for written consent). It is in the last tranche. **So section 43A and the SPDI Rules still apply until 13 May 2027.** One source says 12 May; the gazette arithmetic gives 13 May.
- **Source:** search summaries quoting the notification (MYND DPDP wiki, Acuity Law, Taxmann) – B/C; the wiki itself returned HTTP 503 when opened. Ledger #122 (Rules), #196 (Act), #293 (Board has no members, Aug 2026).
- **Status:** CONFIRMED (three secondary sources agree and match ledger #122). Gazette PDF itself not read.

**What the Act and Rules will require from 13 May 2027** (from the Act and Rules in the ledger, #196 and #122; section numbers are general knowledge, to be checked by the lawyer).
| Topic | Rule in plain words |
|---|---|
| Notice | Before or with the consent request: an itemised list of the data, the purpose, how to withdraw consent, how to use one's rights, how to complain to the Board (section 5; Rule 3). |
| Language | The person must be offered the notice in English or any language in the Eighth Schedule of the Constitution (22 languages). **There is no special rule for people who cannot read.** A spoken notice plus a recorded "yes", with a witness, is our design answer (B5-4), not a rule in the DPDP text. |
| Consent | Free, specific, informed, unambiguous, by a clear affirmative action; as easy to withdraw as to give (section 6). |
| Who is who | The **data fiduciary** decides why and how data is used: in a pilot, the hospital. The **data processor** works on its behalf: us. The fiduciary stays responsible for the processor and must have a contract (section 8). If we sell direct to patients, **we** are the fiduciary. |
| Breach | Tell affected people and the Board without delay; detailed report to the Board within 72 hours (Rule 7, B4-13). |
| Children and guardians | Under 18: verifiable parental consent, no tracking or targeted advertising. A person with a disability who has a lawful guardian: the guardian's verifiable consent (section 9; Rules 10–11). |
| Significant data fiduciary | Named by the Government on volume and sensitivity of data and risk. **No numeric threshold in the Act.** Extra duties: India-based data protection officer, independent audit, impact assessment (section 10; Rule 13). No list found (B4-13). |
| Transfer abroad | Allowed unless the Government restricts a country by notification (section 16); Rule 15 adds conditions about foreign-state access. Matters for our US-hosted server and AI vendors. |
| Penalties (Schedule) | Up to ₹250 crore for failing reasonable security; up to ₹200 crore for not reporting a breach or for breaching children's rules; up to ₹50 crore for other breaches. No jail. No direct compensation to the person. |
- **Status:** NOT CONFIRMED this round (taken from ledger documents and general knowledge; not re-opened).

**Other data rules in force today.**
- **CERT-In Directions, 28 Apr 2022** (ledger #194): report listed cyber incidents within 6 hours; keep logs 180 days inside India; sync clocks to the government time servers. In force. They apply to "service providers, intermediaries, data centres, body corporate".
- **DISHA** (a 2018 health-data bill): never enacted (B4-14). Do not cite it.
- **ABDM Health Data Management Policy:** binds only those who join the ABDM network, by agreement (B5-17, B5-18). Not needed for a pilot.
- **Who to ask:** a privacy/healthcare lawyer for the hospital data agreement; the hospital's IT head for their template.

## L-8: Telemedicine Practice Guidelines 2020 – primary text still unread, but two independent summaries agree (closes B4-15 in part)

- **Legal form.** Issued 25 Mar 2020 by the Board of Governors of the Medical Council, added as **Appendix 5** to the Indian Medical Council (Professional Conduct, Etiquette and Ethics) Regulations 2002. So they bind **doctors**, through their professional-conduct code.
- **Who is covered.** Registered medical practitioners. Five situations: patient to doctor, caregiver to doctor, **health worker to doctor**, doctor to doctor, emergencies. A health worker (a nurse, allied health professional, mid-level provider or auxiliary nurse midwife) may **facilitate** a consultation, take history, convey findings, and explain or reinforce the doctor's advice.
- **What they exclude.** Specifications for hardware or software, data-management systems, remote surgery, and consultations outside India.
- **AI.** Platforms based on AI or machine learning may not counsel patients or prescribe; they may assist a doctor, and the final counselling or prescription must come from the doctor (two summaries agree; B4-15 had one). A platform that breaks the rules can be blacklisted, after which no doctor may use it.
- **Consent.** Implied if the patient starts the consultation; **explicit** (message, email, audio or video) if a health worker, caregiver or doctor starts it.
- **Our reading for each feature.**
  | Feature | Inside the guidelines? |
  |---|---|
  | Automated coaching messages about an exercise the nurse prescribed | No: not a consultation with a doctor. But an AI that answers a symptom question would be "counselling". Keep the fixed nurse/112 reply. |
  | AI phone call that reminds and encourages | Same as above. Open with "this is an automated assistant" (B4-17). |
  | A nurse's follow-up call | Not a doctor consultation. The guidelines do not regulate nurses acting alone. **No rule from the Indian Nursing Council or the allied-health commission on tele-practice was found** (searched; nothing surfaced). |
  | A doctor uses our link to speak to the patient | Yes: the doctor must follow the guidelines (identify both sides, consent, records, prescribing limits). |
- **Status of the 2002 Regulations:** general knowledge, not checked: the National Medical Commission's 2023 conduct regulations were put on hold shortly after they were notified, so the 2002 text is understood to remain in force. Ask the lawyer.
- **Source:** Khaitan & Co note, 31 Mar 2020 (source 2) – B; MediaNama summary, Mar 2020 (source 15) – B. The official PDF hosts in the ledger (#214–217) are blocked; MediaNama hosts a copy that we did not open.
- **Status:** CONFIRMED at secondary level (two independent summaries). Nursing and physiotherapy councils: NOT CONFIRMED (nothing found).
- **Who to ask:** healthcare lawyer; the pilot hospital's medical superintendent.

## L-9: TRAI and DoT call rules – nothing new beyond the ledger

- The first pass and the research report already hold the primary texts: the Third Amendment regulations of 18 Sep 2026 (ledger #106), TRAI's press release (#139), the 140/160/1600 number series note (#70), DLT header and template registration (#108), and provider summaries (#71, #110). We did not re-open them.
- **Still not found:** the Gazette publication date of the 2026 amendment (which fixes the start date), and any rule that requires saying "this is an AI" on a one-to-one call (B4-17).
- **AI voice labelling:** the IT (Intermediary Guidelines) Amendment Rules, G.S.R. 120(E), notified 10 Feb 2026, in force 20 Feb 2026, require **intermediaries** (platforms that host other people's content) to label "synthetically generated information" and keep provenance data. Summaries describe the target as deepfake-style content that appears authentic. A reminder call in a clearly synthetic voice from the hospital's own number is, on our reading, not what the rule targets, and we are not an intermediary. Snippets only.
- **Status:** NOT CONFIRMED (no new primary source).
- **What to do:** keep the practice in B4-17: say it is an automated assistant, call only with recorded consent, use a registered Indian telephony provider with the right number series.
- **Who to ask:** the telephony provider's compliance desk; a telecom lawyer before scale.

## L-10: Patents (extends B4-21)

- **The tests** (Patents Act 1970; wording is general knowledge, not opened this round): an invention must be a new product or process with an inventive step and industrial use (section 2(1)(j)). Not patentable: "a mathematical or business method or a computer programme per se or algorithms" (section 3(k)); and any process for the "diagnostic, therapeutic or other treatment of human beings" (section 3(i)).
- **What that means for us.** The coaching logic and breath-scoring software are caught by 3(k) unless claimed with the hardware as a technical system. "A method of coaching a patient's breathing" risks 3(i). Only a **device** claim (mount, optics, calibration hardware) is a candidate.
- **Prior art already in the ledger:** #86 (Tidal US patent), #132 (Tidal PCT, ceased), #50 (Michigan clip-on paper, 2023), #119 (hobby voice coaches), #131 (Indian patent search, partial).
- **Our own disclosure is now prior art too.** The code repository is public and the site is live. Indian law has only narrow grace periods. Anything already shown cannot be patented by anyone, including us. Anything **new** (a mount, a calibration jig) must be filed **before** it is shown.
- **Provisional versus complete.** A provisional specification fixes the date cheaply; the complete specification must follow within 12 months or the application is treated as abandoned (general knowledge: section 9).
- **Fees (e-filing; secondary fee tables agree; the official First Schedule page was not reachable):** filing ₹1,600 for a natural person, startup, small entity or educational institution (₹8,000 for others); request for examination ₹4,000 (₹20,000); expedited examination ₹8,000 (₹60,000); extra pages over 30 ₹160 each, extra claims over 10 ₹320 each. Educational institutions got the reduced rate in 2021. Rule 7 of the Patents Rules (official page, snippet) confirms fees sit in the First Schedule and that paper filing costs 10% more.
- **Status:** SINGLE SOURCE for fees (several practitioner tables, grade C, consistent with B4-21). Statute wording NOT CONFIRMED this round.
- **Who to ask:** a registered patent agent, for a paid novelty search before any filing.

## L-11: Design, trademark, copyright, and AI-assisted code

- **Design registration** (Designs Act 2000; general knowledge): protects the look of the enclosure; must be new and **not published before filing**. File before the final enclosure appears in a video or pitch. Fee ₹1,000 per class for individuals and startups (B4-21, snippet).
- **Trademark:** classes 10 (medical apparatus), 9 (software, sensors), 44 (medical services); add 42 if software is sold as a service. ₹4,500 per class for individuals, startups and small enterprises; ₹9,000 for others (B4-21, snippet). The free search for "SPIROBUDDY" is still to be done by a person.
- **Copyright in code** (Copyright Act 1957; general knowledge): software is a literary work. The author owns it first, unless written in the course of employment. **A contractor, intern or student volunteer owns what they write unless they assign it in writing.** An assignment that states no period is treated as lasting five years, and one that states no territory as covering India only (section 19): the assignment must say "perpetual, worldwide".
- **AI-assisted code.** There is no statute on AI authorship. Section 2(d)(vi) names, for a computer-generated work, the person who causes it to be created. Reports say the Registrar of Copyrights, in an order of 31 Aug 2026 on the "DABUS" application, refused to record an AI as author but treated the human who caused the work as the author, and limited the finding to that case. A government committee's working paper of Dec 2025 on generative AI is advisory. Our reading: code written by team members with AI help is owned like any other code the team writes; keep humans making the design decisions and keep the commit history.
- **Source:** search snippets (Intepat, SS Rana, World Trademark Review) – C. The order itself was not opened.
- **Status:** NOT CONFIRMED.
- **Who to ask:** IP attorney.

## L-12: Who owns student work? Three published university policies, and hackathon terms (closes part of B4-21)

| Institution | The rule in its policy | Revenue share |
|---|---|---|
| IIT Kanpur | Institute owns IP created by students "with the significant use of funds or facilities" it administers. Students keep copyright in their thesis. | not read |
| Anna University (2023 policy) | University owns IP created by students "who make use of the resources" of the University. Created without its resources and outside normal duties: the creator owns it, and revenue is shared 75:25 (creator : University). | On University-owned IP, 60% to creators, 40% to the University |
| IIT Palakkad | Institute is "the owner of all intellectual properties" created by creators (students included) unless a prior agreement says otherwise. | not read |
| IIT Bombay (student-magazine summary, grade C) | Institute owns when "significant" resources are used; library and network use do not count. | about 70% to inventors on the first tranche |

- **The usual rule:** the institute owns, or co-owns, when its money, labs or coursework were used; the student owns work done with their own time and tools. Policies differ on what "use of resources" means, and one (Palakkad) starts from institute ownership.
- **Hackathons:** published terms from other events (OpenAI, Samsung Next, Liquid AI: foreign, snippets, C) usually leave ownership with participants and take a licence to publicise the entry. One (a Singapore university) takes joint ownership. **This hackathon's own terms have not been read.**
- **Source:** IIT Kanpur IPR policy (source 10) – B; Anna University IP Policy (source 9) – B; IIT Palakkad IPR Policy (source 11) – B; others snippets – C.
- **Status:** CONFIRMED for the three policies read. The team's own college: unknown (Founder notes, section F).
- **Who to ask:** the college's innovation cell (ask for the policy in writing); the hackathon organisers (ask for the terms); then the IP attorney.

## L-13: Advertising and claims (extends B4-20)

- **Drugs and Magic Remedies Act 1954:** B4-20 stands (Schedule item 42, pneumonia). Other lung-related Schedule entries such as pleurisy and tuberculosis are listed from memory; the Schedule (ledger #297) was not re-opened, so numbers are not given. Relevant if we ever market to post-tuberculosis rehabilitation.
- **CCPA Guidelines for Prevention of Misleading Advertisements, 2022** (general knowledge): an advert must be truthful, must not exaggerate, claims said to rest on research must name the source, disclaimers must not contradict the claim, and endorsers must do due diligence. Penalties as in B4-18.
- **Dark patterns** (CCPA guidelines, Nov 2023; general knowledge): thirteen listed practices are treated as unfair, including false urgency, "confirm shaming", forced action, subscription traps and nagging. Relevant to reminder design: a reminder must never shame or pressure a patient. This matches our "patient side simple and kind" rule.
- **ASCI** (self-regulator): health claims need proportionate evidence; AI-content labelling guidelines of 29 Sep 2026 (B4-17, snippet).
- **Device claims:** label rule 44 (B4-5); marketing code (L-22); no promotion before a licence.
- **App stores** add their own claim rules (L-26).
- **Status:** NOT CONFIRMED this round (no new primary source).
- **Who to ask:** healthcare lawyer, with the actual pitch deck and web copy.

---

# PART B – Areas the first pass did not cover

Most of Part B is **general knowledge plus search snippets**. It is a list of the right questions and the usual answers, to be confirmed by the adviser named. Where we read a primary text, it says so.

## L-14: Setting up the company

- **Which form.**
  | Form | Minimum people | Good for | Limits |
  |---|---|---|---|
  | Private limited company | 2 shareholders, 2 directors | Investors, grants that need a company, share options | Most compliance |
  | Limited liability partnership (LLP) | 2 partners, one resident in India | Low cost, few filings | Cannot issue shares or share options; investors rarely invest |
  | One Person Company | 1 member (an Indian citizen) and a nominee | A solo founder | A minor cannot be member or nominee; must convert to take investors |
  Section 80-IAC (the startup tax holiday) is open only to a private limited company or an LLP (snippet). Most schemes in B3-8 to B3-10 ask for a company. **Usual choice for a team that wants grants and investors: private limited.**
- **Resident director:** at least one director who stayed in India 182 days or more in the year (section 149(3), Companies Act 2013; sources differ on calendar year versus financial year).
- **Founders who are students or under 18.** Being a student is no bar. A person under 18 cannot make a binding contract (Indian Contract Act, section 11), cannot realistically be a director, and can hold shares only through a guardian. **Every founder who signs must be 18 or older.**
- **Steps (Ministry of Corporate Affairs portal):** digital signatures → name reservation and incorporation in the single "SPICe+" form with electronic memorandum and articles → PAN, TAN, bank account and optional GST, provident fund and state insurance registrations come with the linked form. Government fee and stamp duty depend on the state and share capital. **No official fee figure was found** (B3-15 also found none).
- **First-year calendar (general knowledge; a company secretary must confirm dates and penalties).**
  | When | What |
  |---|---|
  | Within 30 days | First board meeting; appoint the first auditor |
  | Within 180 days | Declaration that share money has been received (Form INC-20A) |
  | Each year | At least 2 board meetings for a small company or startup (4 otherwise); annual general meeting; accounts (AOC-4) and annual return (MGT-7 or 7A) filed after it; auditor form (ADT-1) |
  | By 30 June | Return of deposits and loans (DPT-3) |
  | By 30 September | Director identity check (DIR-3 KYC) |
  | Tax | Income-tax return; tax-deduction (TDS) returns each quarter; GST returns if registered |
  Missing filings brings daily late fees, deactivation of director numbers and, in the end, strike-off. Amounts: not confirmed.
- **DPIIT recognition:** B3-15 (ledger #274). Benefits to check with the CA: section 80-IAC (100% of profit for 3 years in a row out of the first 10; company formed before 1 Apr 2030; turnover up to ₹100 crore; needs a separate inter-ministerial certificate: snippets); **"angel tax" (section 56(2)(viib)) no longer applies from assessment year 2025-26** (snippets, several agree); self-certification under labour laws for the first years (the Startup India page did not load; which laws apply after the labour codes is unclear, L-24).
- **Founders' agreement (practice, not a statute):** roles, shareholding, **vesting** (shares earned over time, commonly 4 years with a 1-year "cliff"), what happens when a founder leaves, decision rules, and **assignment of all IP to the company** by every founder and contractor, in writing, perpetual and worldwide (L-11).
- **ESOP** (employee share options): available only in a company; a pool is created by shareholder resolution; one-year minimum vesting; founders can receive options only in a DPIIT-recognised startup. General knowledge.
- **When it bites:** before the test licence (B4-4 needs a legal entity), before any contract, grant to a company, or bank account.
- **Status:** NOT CONFIRMED (general knowledge and snippets).
- **Who to ask:** company secretary or chartered accountant.

## L-15: Tax

- **Income-tax numbering warning.** A new Income-tax Act (2025) is understood to apply from 1 Apr 2026 and renumbers sections. The section numbers in this file (80-IAC, 56(2)(viib), 43B(h), 194C and so on) are from the 1961 Act. The CA must map them. General knowledge.
- **GST registration** (snippets): compulsory above ₹40 lakh a year for goods sold **within one state** and ₹20 lakh for services (lower in a few special-category states). **Selling goods to another state requires registration from the first rupee.** A hospital customer will usually want a GST invoice anyway.
- **Rates:** 5% on medical devices under headings 9018/9019 since 22 Sep 2025 (B6-2, ledger #335). Software as a service: 18% (snippets). **Bundle rule** (CGST Act, section 8): a naturally bundled "composite supply" takes the rate of its main element; a "mixed supply" sold for one price takes the highest rate. So device-with-built-in-software sold as one product points to the device rate; a per-patient software or rental fee points to 18%. Our classification (B6-2) is still open; an **advance ruling** can settle it.
- **Place of supply:** for goods, where delivery ends; for services to a registered hospital, the hospital's state. Decides state versus inter-state tax. General knowledge.
- **E-invoicing:** compulsory above ₹5 crore annual turnover (snippets). Not relevant early.
- **Tax deducted by customers (TDS):** hospitals deduct a small percentage from payments for contracts and for technical or professional services, and government bodies also deduct GST-TDS on larger contracts. The company claims it back in its return. Rates: ask the CA.
- **Grants:** whether a grant is taxed as income depends on its purpose and terms; a pure grant with nothing supplied in return is generally outside GST. Ask the CA before accepting; keep the sanction letter.
- **Status:** NOT CONFIRMED except the 5% rate (B6-2).
- **Who to ask:** chartered accountant.

## L-16: Contracts the team will sign

**The law behind them (general knowledge).** Indian Contract Act 1872: who can contract (section 11), unlawful terms (23), restraint of trade (27), damages (73), agreed damages are capped at reasonable compensation (74), indemnity (124), **bailment** (148–171: someone holding another's goods must take the care of an ordinary prudent person, is not liable for loss if they did, and is liable if they do not return goods on time). Specific Relief Act 1963: courts can order performance. Arbitration and Conciliation Act 1996: a written arbitration clause, with a named seat. Liability caps are generally enforceable between businesses, but not for fraud or wilful misconduct, not against consumers' statutory rights, and not for duties a statute places on us.

| Contract | Clauses that matter most | Stage |
|---|---|---|
| Non-disclosure agreement | What is confidential, term, **no licence to the idea**, return of materials | Before any hospital or manufacturer talk |
| Founders' agreement and IP assignments | L-14 | Now |
| Hospital pilot agreement | Purpose; prototype status; **nurse keeps every clinical decision**; EC approval as a condition; who is sponsor; units on loan; data roles; adverse events; publication; no charge or price; exit (list in B4-19) | Before any real patient |
| Clinical study agreement | Sponsor and investigator duties, compensation (MDR rule 55 if permitted), insurance, records for 7 years (rule 57), registry listing | If L-1 Reading A |
| Data processing agreement | B4-16 list; add sub-processors abroad (L-7) and CERT-In timing | Before any real patient |
| Loan (bailment) of units | Units stay ours; hospital's duty of care; who pays for loss or damage (state it: the default law excuses a careful holder); cleaning between patients (B6-10); return date | Pilot |
| Service and service-level agreement | Uptime promise, support hours, what happens when the internet or AI is down (our offline fallback), credits, liability cap | Paid pilot |
| Manufacturer / supplier agreement | Specification, quality system, who holds the licence (loan licence, B4-3), IP in tooling, recalls, traceability, component certificates (BIS, ETA) | Before sale |
| Distributor agreement | Territory, MD-42 registration (B2-10a), price rules, marketing-code compliance (L-22), complaint reporting | Sale |
| App terms of use and privacy policy | Intended use and warnings (B4-18), not for emergencies, data notice (L-7), account deletion (L-26) | Before any real user |
| Consent forms | B5-4; L-21 | Before any real patient |

- **Electronic contracts and signatures:** valid under the IT Act (section 10A); Aadhaar eSign is a recognised electronic signature; a few document types are excluded. **Stamp duty** is a state tax on agreements; an unstamped agreement cannot be used as evidence until duty and penalty are paid. General knowledge.
- **Status:** NOT CONFIRMED (team synthesis on general knowledge).
- **Who to ask:** healthcare lawyer (pilot, data, consent); company secretary (stamping).

## L-17: Liability when something goes wrong

- **Product liability:** B4-18 stands. Added from summaries of the Consumer Protection Act 2019: "product manufacturer" includes whoever puts **their own mark** on a product made by someone else, so a contract manufacturer does not move liability away from us; "product seller" includes someone who **leases** a product, so lending does not take us outside the chapter. Section 87 lists defences (misuse, alteration, and failure to warn where the product was to be used under expert supervision and the warnings were given to that expert). Section 87's text was not read (the official copy failed to download).
- **Medical negligence (general knowledge):** the Supreme Court in *Jacob Mathew v State of Punjab* (2005) applied the test that a professional is not negligent if they followed a practice accepted by a responsible body of their profession, and required gross negligence for a criminal case. Hospitals answer for their staff. A tool does not shift the nurse's duty. Contracts usually split it: hospital answers for clinical decisions, maker answers for device and software defects, each indemnifies the other.
- **Criminal law (read in the official text):** Bharatiya Nyaya Sanhita 2023, section 106(1): causing death by a rash or negligent act: up to **five years** and fine; the lower two-year limit applies only to "a registered medical practitioner while performing medical procedure". Section 125: a rash or negligent act that endangers life: up to three months or ₹2,500; six months or ₹5,000 if hurt is caused; three years or ₹10,000 if grievous hurt is caused. These apply to **individuals**, including engineers and founders.
- **Licence-holder duties (read in MDR 2017):** tell the licensing authority of any "suspected unexpected serious adverse event" and action taken, including recall, "within fifteen days" (rule 26(ii)); get prior approval for major changes (rule 26(iii), Sixth Schedule), which will include major software changes; keep manufacturing and sales records; **recall** a device believed unsafe and inform the authority (rule 89). In a permitted clinical investigation, serious adverse events go to CDSCO within 14 days (rule 53(v)).
- **Materiovigilance Programme of India** (the national device adverse-event reporting scheme, coordinated by the Indian Pharmacopoeia Commission): general knowledge; whether recent orders make reporting through it compulsory for licence holders was not found (search failed on rate limits).
- **Insurance:** B4-19 stands (no prices). Types to ask a broker about: clinical-trial/no-fault cover, product liability, professional indemnity, cyber. Not compulsory under the MDR text (L-1); compensation is.
- **Source:** BNS 2023, Ministry of Home Affairs copy (source 14) – A; MDR 2017 (source 1) – A; CPA – snippets (Cyril Amarchand, others) – C.
- **Status:** CONFIRMED (BNS; MDR rules 26, 53, 89). NOT CONFIRMED (CPA section 87 wording; case law; materiovigilance).
- **Who to ask:** healthcare lawyer; insurance broker.

## L-18: AI-specific rules as of October 2026 – what is law, what is guidance

| Item | Type | What it means for us |
|---|---|---|
| MDR 2017 + software classification (B4-2) | **Binding law** | The coach software takes the device's class. |
| Telemedicine guidelines, AI clause (L-8) | **Binding on doctors** | AI may not counsel or prescribe. |
| DPDP Act and Rules (L-7) | **Binding law**, main parts from 13 May 2027 | Consent, purpose limits, no hidden reuse of patient data to train models. |
| Consumer Protection Act (B4-18) | **Binding law** | Wrong instructions or broken promises by the AI are our liability. |
| IT (Intermediary Guidelines) Amendment Rules, G.S.R. 120(E), in force 20 Feb 2026 | **Binding law, on intermediaries** | Labelling of synthetic audio/video on platforms. Our reading: not aimed at us (L-9). Snippets. |
| India AI Governance Guidelines, MeitY, 5 Nov 2025 | **Guidance, non-binding** | Seven principles; says existing laws already apply to AI. Snippets. |
| MeitY advisories of March 2024 on AI models | **Advisory**, aimed at platforms | General knowledge; status not checked. |
| ICMR Ethical Guidelines for AI in healthcare, 2023 (B5-9) | **Guidance**; an EC will apply it | Human oversight, safety, consent, accountability. |
| CDSCO Guidance on Medical Device Software, 2026 (ledger #135) | **Guidance** | How CDSCO reads the rules for software. Its position on self-learning algorithms was not re-read. |
| A dedicated AI Act or "Digital India Act" | **None found** | – |

- **"Human in the loop" in practice** (our reading across the above): (1) a named nurse or doctor makes every clinical decision; (2) the AI's wording on symptoms is fixed text, not generated; (3) every AI message is logged and reviewable; (4) the model is not changed in the field without a controlled release (a major change needs the licensing authority's approval once licensed, L-17); (5) the patient is told it is automated and can reach a human.
- **Status:** NOT CONFIRMED for the 2025–26 items (snippets).
- **Who to ask:** healthcare lawyer; regulatory consultant for the software-change question.

## L-19: Accessibility law

- **Rule (read in the gazette copy).** Rights of Persons with Disabilities (Amendment) Rules 2023, notified May 2023, amend Rule 15: "Websites, apps, information and communication technology based public facilities and services", everyday electronic goods and consumer products must comply with **IS 17802 (Part 1) 2021 and (Part 2) 2022**, the Indian accessibility standard for ICT (closely based on the international web accessibility guidelines).
- **Who:** the 2016 Act's accessibility duties reach private establishments and service providers (general knowledge: sections 40–46), with fines for breach.
- **Courts (snippets):** *Rajive Raturi v Union of India*, 8 Nov 2024: the Supreme Court told the Government to turn accessibility guidance into mandatory rules. *Pragya Prasun v Union of India*, 30 Apr 2025 (2025 INSC 599): digital access is part of the right to life; about 20 directions on accessible digital services.
- **Draft:** RPwD (Amendment) Rules 2026, published 20 Jul 2026, would create a mandatory conformance regime for ICT products "for public or consumer use", including foreign suppliers. Comments closed 19 Aug 2026. **Final status not found.**
- **What an app for elderly and low-vision users should meet:** IS 17802 (text contrast, resizable text, screen-reader labels, no time limits that cannot be extended, captions or text for audio, large touch targets). This is also good design for our users; a hospital or government buyer may ask for a conformance statement.
- **Maintenance and Welfare of Parents and Senior Citizens Act 2007:** about maintenance payments and care duties. **Not relevant** to family WhatsApp updates.
- **Source:** RPwD (Amendment) Rules 2023, gazette copy (source 7) – A; cases and draft – snippets (SCC Online, IndiaLaw) – C.
- **Status:** CONFIRMED (Rule 15 and the standard). NOT CONFIRMED (penalties, case details, 2026 draft status).
- **Who to ask:** healthcare lawyer; an accessibility auditor before a government sale.

## L-20: Consent and capacity

- **Research consent:** B5-4 and B5-5 (ICMR 2017). A person who cannot read: the form is read out, a thumb impression or recorded verbal consent is taken, and an **impartial literate witness** signs (ICMR, snippet).
- **Reduced capacity.** The Mental Healthcare Act 2017 (general knowledge) presumes every adult has capacity; a person has it if they can understand the information, appreciate the consequences, and communicate a choice; diagnosis or age alone proves nothing; a person can name a "nominated representative". It governs mental-health treatment, but ECs use the same test. For research, a legally acceptable representative may consent for a person who lacks capacity, and the person's own agreement is still sought (B5-5). **Simplest pilot rule: enrol only adults who can consent for themselves.**
- **Family consenting for a patient:** there is no general right for a relative to consent for a capable adult. The **patient** must agree before family receive updates; the product already does this.
- **Recording calls** (general knowledge): no statute fixes a one-party or all-party consent rule for private recordings; interception is a government power; recordings are widely admitted as evidence; but a recording of a patient is personal (health) data, so notice and consent are needed under the SPDI rules now and DPDP later. **Announce the recording and take a recorded "yes".**
- **Children:** under 18 needs verifiable parental consent under DPDP and assent plus parental consent in research. Exclude in the pilot (B4-13).
- **Status:** NOT CONFIRMED (general knowledge; one search failed on rate limits).
- **Who to ask:** the hospital's ethics committee secretary; healthcare lawyer.

## L-21: Hospital-side rules that will be passed on to us

- **Clinical Establishments Act 2010 and state equivalents:** register and set minimum standards for hospitals. They bind the hospital, not us; they are why a hospital asks for records, staff qualifications and infection-control proof. General knowledge.
- **NABH** (hospital accreditation) standards include information management (confidentiality, access control, retention) and facility/equipment management (inventory, safety testing, maintenance, training before use). Expect a biomedical engineer to ask for an electrical-safety report (B4-9), a user manual, a cleaning instruction (B6-10) and a maintenance plan. General knowledge; edition and clause numbers not checked.
- **No payments to doctors for referrals (read in part).** Indian Medical Council Regulations 2002: clause 6.4 bars a doctor from giving or receiving any commission for referring patients (snippet of the text). Clause 6.8, added 10 Dec 2009 (read): a doctor shall not receive "any gift", travel, hospitality, or cash "for individual purpose in individual capacity" from the pharmaceutical "and allied health sector industry"; research funding is allowed only **through approved institutions**, transparently and with ethics clearance; a doctor shall not publicly endorse an industry product (6.8.1(h), snippet).
- **Uniform Code for Marketing Practices in Medical Devices 2024** (Department of Pharmaceuticals, 6 Sep 2024; B4-20; summaries): no gifts or money to healthcare professionals or their families; evaluation samples only to qualified people, recorded, and marked "Evaluation Sample – Not for Sale"; reported cap on samples at 2% of domestic sales; yearly disclosure of samples and conference spending; **no promotion before approval**. A 2025 revision is reported. Summaries describe it as a code enforced through industry associations, with a yearly self-declaration.
- **Anti-bribery:** Prevention of Corruption Act 1988 as amended in 2018 (snippets): offering an undue advantage to a public servant is an offence (section 8, up to seven years); a **company** is liable when anyone acting for it does so (section 9); directors can be personally liable (section 10). Doctors and staff in government hospitals are public servants.
- **So, with free units:** lend them to the **hospital** under a written agreement, not to a doctor; pay any study costs to the **institution**; no fees, travel or gifts to individual doctors; "advisory board" payments need a lawyer first.
- **Source:** MCI amendment notification 10 Dec 2009 (source 12) – A; others snippets – C; ledger #296.
- **Status:** CONFIRMED (clause 6.8). NOT CONFIRMED (the rest).
- **Who to ask:** healthcare lawyer.

## L-22: Selling to government

- **Covered already:** tenders, GeM, startup relaxations and the 45-day payment rule (B2-1 to B2-8).
- **Local content (read in the order).** Public Procurement (Preference to Make in India) Order 2017, revised 19 Jul 2024: a "Class-I local supplier" offers goods with local content of **50% or more**; Class-II is above 20% and below 50% (snippet for the 20% figure); below that is a non-local supplier, generally shut out. The bidder declares its local-content percentage itself. Imported sensor and radio modules count against us; Indian assembly, enclosure, firmware and software count for us. We have not calculated our percentage.
- **MSME (Udyam) registration:** free and online; makes the company a micro enterprise. Effects: payment protection (MSMED Act section 15: within the agreed period, never more than 45 days, 15 days if nothing is agreed; section 16: compound interest at three times the bank rate; the buyer loses its tax deduction until it pays), tender fee and deposit waivers (B2-6), **and the e-waste exclusion (L-5)**.
- **Source:** PPP-MII Order revision 19 Jul 2024, copy on the DoT site (source 16) – A; MSMED sections – snippets (TaxGuru and others) – C; B2-4a.
- **Status:** CONFIRMED (Class-I definition). SINGLE SOURCE/snippets for the rest.
- **Who to ask:** chartered accountant (Udyam, local-content certificate).

## L-23: People

- **Labour codes:** the four codes took effect 21 Nov 2025; central rules were notified 8 May 2026; several states' rules were still pending in mid-2026 (snippets). Old Act names in older guidance no longer match.
- **Thresholds (general knowledge; confirm under the codes and state rules):** provident fund at 20 workers; employees' state insurance at 10; state Shops and Establishments registration from the first employee in most states; gratuity at 10.
- **POSH Act 2013** (sexual-harassment law): an Internal Committee is compulsory at **10 or more workers**; below that, complaints go to the district Local Committee. The Act protects interns and volunteers. Adopt a one-page policy from day one.
- **Interns and student workers:** a written letter (stipend, hours, confidentiality, **IP assignment**). Unpaid "volunteers" who write code own that code unless they assign it (L-11).
- **Contractor versus employee:** decided by real control and integration, not by the label. Mislabelling creates back-dues.
- **Non-compete:** section 27 of the Contract Act makes a restraint on someone's trade void; courts refuse to enforce non-competes **after** someone leaves. Confidentiality and reasonable non-solicitation clauses, and restraints **during** the engagement, are enforced. So protect the business with IP assignment and confidentiality, not a non-compete.
- **Status:** NOT CONFIRMED.
- **Who to ask:** company secretary / labour consultant.

## L-24: Imports and exports (headline only)

- **Importing parts:** an Importer-Exporter Code from the trade directorate is needed to import commercially. Customs duty depends on the tariff heading a customs broker assigns; **we give no duty rate** (none found in an official source). At import: BIS registration for cells and adaptors (L-4); for radio modules, the existing ETA plus a signed undertaking that the module works only in licence-exempt bands and is free of import licensing (WPC FAQ, L-2). Buying parts from Indian distributors avoids all of this for a pilot.
- **Exporting the device:** each country has its own approval (CE mark, US FDA). CDSCO can issue a free-sale certificate for export on request (MDR rule 91, read).
- **Exporting health data:** L-7 (transfers abroad).
- **Status:** CONFIRMED (rule 91; WPC import undertaking). Rest NOT CONFIRMED.
- **Who to ask:** customs broker; regulatory consultant.

## L-25: App-store and platform terms

- **Google Play (read on Google's policy page):** every app completes a Health apps declaration. An app that is a regulated medical device must be declared as one and must give proof of approval or clearance from the relevant authority when asked. Other health apps must carry a disclaimer in the store description that the app is not a medical device and does not diagnose, treat, cure or prevent any condition. A public privacy-policy web page is required. If users can create an account, they must be able to delete it and its data from inside the app and from a web link (snippet).
  - **The trap:** our unit is a medical device under Indian law (B4-1, B4-2), so the companion app is a medical-device app. Before a licence we cannot show approval; and the "not a medical device" disclaimer would be untrue once we are licensed. Publish through **closed testing** for the pilot, or as a hospital-distributed web app, until the licence exists.
- **Apple (snippets, not read on Apple's site):** guideline 1.4.1: medical apps get closer review, must disclose data and method behind accuracy claims, and should link to regulatory clearance; guideline 5.1.3: health data may not be used for advertising or data mining and must not be stored in iCloud.
- **WhatsApp:** ledger #207 (business messaging policy), #213 (opt-in), #209 (template categories), #210–212 (data location). Unchanged: opt-in before the first message, utility templates only, no health advice by template.
- **Fees:** not researched here (see the costs file).
- **Source:** Google Play Console Help, Health content and services policy (source 13) – B.
- **Status:** CONFIRMED (Google, primary). NOT CONFIRMED (Apple).
- **Who to ask:** healthcare lawyer for the store listing wording; nobody else needed.

## L-26: Money and fundraising law

- **Grants to individuals versus a company:** some grants go to individuals or student teams (B3-7, B3-8); most later ones need a company (B3-9, B3-10). A grant paid to a person is that person's to account for; agree in writing that anything bought with it, and the IP, moves to the company on incorporation.
- **Convertible notes** (a loan that turns into shares later): a DPIIT-recognised startup may take one of **₹25 lakh or more in a single tranche**, to convert or be repaid within 10 years (snippets; a shorter limit is reported for foreign investors). Below ₹25 lakh, use shares or compulsorily convertible preference shares (CCPS, the usual investor instrument).
- **Foreign investment:** 100% foreign direct investment in medical-device manufacturing is allowed without prior approval (policy of 2015; current consolidated policy not checked). Investors from countries sharing a land border with India need Government approval (general knowledge). Every foreign rupee needs a valuation and a central-bank filing.
- **Crowdfunding:** a private company may not invite the public to buy shares; a private placement is limited to a set number of named people (general knowledge). **Equity crowdfunding is not a lawful route.** Donation-style crowdfunding for individuals or charities is different and brings tax questions.
- **CSR money:** companies may count as CSR spending a contribution to **incubators funded by the Central or a State Government** or their agencies (Schedule VII item (ix), as amended by G.S.R. 776(E) of 11 Oct 2019: snippets). A for-profit startup cannot simply receive CSR as a donation. Two lawful shapes: (1) CSR goes to a government-funded incubator, which supports us; (2) a company's CSR project buys or funds units **for a hospital or non-profit**, as in Dozee's MillionICU (B2-12). We are then a supplier, not a recipient.
- **Status:** NOT CONFIRMED (snippets and general knowledge).
- **Who to ask:** chartered accountant; a startup lawyer at the first cheque.

---

# PART C – Deliverables

## Answer in 15 lines

1. **First patient study:** on the text of the rules, an unlicensed prototype with no approved Indian equivalent needs CDSCO permission (Form MD-22) as well as an ethics committee. The ethics-committee-only exemption is for licensed devices. Plan for permission; ask CDSCO in writing. (L-1)
2. **A cheaper order may exist:** if CDSCO accepts Class A (measuring), clinical data "may not be required" for the licence. Licence first on bench evidence, then an academic study with ethics approval only. (L-1)
3. **A government hospital as sponsor pays no CDSCO fee** for the study permission. (L-1)
4. **Radio approval is solved for an India-made unit:** an approved module used unchanged needs no separate approval. An imported finished unit would (₹10,000). (L-2)
5. **A registered micro enterprise is outside the E-waste Rules.** Register on Udyam; it also gives payment protection. (L-5, L-22)
6. **Data law today is the 2011 SPDI rules plus CERT-In's 6-hour rule.** The DPDP duties start 13 May 2027. In a pilot the hospital is the data fiduciary and we are its processor. (L-7)
7. **Telemedicine guidelines bind doctors, not nurses or software.** AI may not counsel or prescribe. No nursing-council tele-practice rule was found. (L-8)
8. **Patent:** software and treatment methods are excluded; our own public repo is prior art; only a new hardware detail, filed before it is shown, is a candidate. (L-10)
9. **Student IP:** three university policies read all give the institute ownership when its resources are used. Read your college's policy and the hackathon terms before saying "we own it". (L-12)
10. **Every contributor must assign IP to the company in writing**, perpetual and worldwide, or the default law limits it to five years and India. (L-11)
11. **All signing founders must be 18 or older.** Private limited company is the usual form for grants and investors. (L-14)
12. **Never pay or gift individual doctors.** Lend units to the hospital, pay study costs to the institution. Government doctors are public servants. (L-21)
13. **Negligent harm is a personal criminal risk** for whoever built or deployed the tool: up to five years if a death results. The doctors' lower limit does not cover us. (L-17)
14. **App stores:** Google wants proof of approval for a medical-device app, or a "not a medical device" disclaimer that would be untrue for us. Use closed testing until licensed. (L-25)
15. **Accessibility is law:** apps must meet IS 17802. A stricter regime was drafted in July 2026. (L-19)

## Master legal checklist (in order, with stage gates)

"n/f" = no official figure found. Status is for 10 Oct 2026.

### Gate 0 – before building a prototype
| # | Item | Law or rule | Who does it | Official fee | Time | Source | Status |
|---|---|---|---|---|---|---|---|
| 1 | Read the college IP policy; get it in writing | Institute policy | Team lead | ₹0 | 1 week | L-12 | Not started |
| 2 | Read the hackathon terms on IP | Organiser terms | Team lead | ₹0 | 1 day | L-12 | Not started |
| 3 | Confirm every founder is 18+; sign a founders' agreement with IP assignment | Contract Act s.11; Copyright Act s.19 | Founders | ₹0 (stamp duty n/f) | 1 week | L-11, L-14 | Not started |
| 4 | Written IP assignment from every contributor so far | Copyright Act s.19 | Team lead | ₹0 | 1 week | L-11 | Not started |
| 5 | Decide what must stay unpublished (new hardware details) before any filing | Patents Act; Designs Act | Hardware lead | ₹0 | now | L-10, L-11 | Not started |
| 6 | Trademark search for SPIROBUDDY (classes 9, 10, 42, 44) | Trade Marks Act | Team lead | ₹0 | 1 hour | B4-21 | Not started |
| 7 | Freeze intended use, warnings and banned claims | CPA 2019; DMR Act 1954 | Product owner | ₹0 | days | B4-18, B4-20 | Not started |
| 8 | Keep only fake patients in the demo system | SPDI Rules; project rule | Software lead | ₹0 | – | L-7 | Done (project rule) |
| 9 | Pick a radio module with an existing ETA; BIS-registered cell/adaptor or none | WPC FAQ; BIS order | Hardware lead | ₹0 | – | L-2, L-4 | Not started |

### Gate 1 – before any real patient
| # | Item | Law or rule | Who | Official fee | Time | Source | Status |
|---|---|---|---|---|---|---|---|
| 10 | Incorporate (private limited) | Companies Act 2013 | Team lead + CS/CA | n/f | n/f | L-14 | Not started |
| 11 | DPIIT recognition; Udyam (micro) registration | Startup India; MSMED Act | Company | ₹0 | n/f | B3-15, L-22 | Not started |
| 12 | Written question to CDSCO / consultant: class, predicate, MD-22 or not | MDR rules 3, 49, 51, 63 | Team lead | n/f | 1–2 weeks | L-1 | Not started |
| 13 | Test licence for prototypes | MDR rule 31 (MD-12 → MD-13) | Company | ₹500 per device | 30 days | B4-4 | Not started |
| 14 | Bench safety and accuracy tests | MDR rule 7; IEC 60601 | Hardware lead | n/f | n/f | B4-9 | Not started |
| 15 | Hospital with a registered ethics committee; protocol; consent forms | MDR rule 50; ICMR 2017 | Hospital investigator | n/f | n/f | B4-7, B5-4 | Not started |
| 16 | If required: CDSCO permission | MDR rule 51 (MD-22 → MD-23) | Sponsor | ₹1,00,000; nil for government-run or -funded hospital | 90 days | L-1 | Not applicable yet |
| 17 | Trial registry listing (compulsory if item 16 applies) | MDR rule 53(iii) | Sponsor | ₹0 | about 10 working days | B5-8 | Not applicable yet |
| 18 | Pilot agreement, unit-loan terms, data processing agreement | Contract Act; SPDI Rules; DPDP s.8 | Company + hospital | n/f | 2–4 weeks | L-16, B4-16 | Not started |
| 19 | Real data on an India-hosted system; breach plan with CERT-In 6-hour step; logs 180 days | CERT-In Directions 2022 | Software lead | ₹0 | 2 weeks | L-7 | Not started |
| 20 | Consent script with spoken version, witness line, call-recording notice | ICMR 2017; SPDI | Product owner | ₹0 | 1 week | L-20 | Not started |
| 21 | Compensation arrangement / insurance quote for the study | MDR rule 55; EC practice | Company | n/f | n/f | L-17 | Not started |
| 22 | No payments or gifts to individual clinicians; written rule | IMC Regs 6.4, 6.8; PC Act | Founders | ₹0 | now | L-21 | Not started |
| 23 | App distributed by closed testing or web, not a public store listing | Google Play policy | Software lead | n/f | – | L-25 | Not started |

### Gate 2 – before a paid pilot
| # | Item | Law or rule | Who | Official fee | Time | Source | Status |
|---|---|---|---|---|---|---|---|
| 24 | Manufacturing or loan licence | MDR rule 20 (MD-5 / MD-6) | Company | ₹5,000 + ₹500 | 45 days (A) / about 140 (B) | B4-3 | Not applicable yet |
| 25 | Quality system and technical file | MDR Fifth Schedule | Quality owner | n/f | months | B4-5 | Not started |
| 26 | GST registration; rate decision (device 5% / service 18%) | CGST Act ss.8, 22, 24 | CA | ₹0 | n/f | L-15 | Not applicable yet |
| 27 | Service agreement with uptime and liability cap | Contract Act | Company | n/f | – | L-16 | Not applicable yet |
| 28 | Trademark filed | Trade Marks Act | Team lead | ₹4,500 per class (snippet) | – | B4-21 | Not started |
| 29 | POSH policy; labour registrations as headcount grows | POSH Act; labour codes | Company | n/f | – | L-23 | Not applicable yet |

### Gate 3 – before selling
| # | Item | Law or rule | Who | Official fee | Time | Source | Status |
|---|---|---|---|---|---|---|---|
| 30 | Label and instructions with licence number | MDR rule 44 | Product owner | ₹0 | – | B4-5 | Not applicable yet |
| 31 | Adverse-event, complaint and recall procedure | MDR rules 26, 89 | Quality owner | ₹0 | – | L-17 | Not applicable yet |
| 32 | Marketing-code self-declaration; claims review | UCMPMD 2024; CCPA 2022 | Company | ₹0 | yearly | L-13, L-21 | Not applicable yet |
| 33 | Seller/distributor registrations | MDR (Form MD-42) | Distributor | n/f | – | B2-10a | Not applicable yet |
| 34 | Store listing as a declared medical-device app with proof | Google / Apple terms | Software lead | n/f | – | L-25 | Not applicable yet |
| 35 | Accessibility conformance (IS 17802) | RPwD Rule 15 | Software lead | n/f | – | L-19 | Not started |
| 36 | Design registration before the final enclosure is shown | Designs Act | Team lead | ₹1,000 (snippet) | – | L-11 | Not applicable yet |

### Gate 4 – at scale
| # | Item | Law or rule | Who | Official fee | Time | Source | Status |
|---|---|---|---|---|---|---|---|
| 37 | Full DPDP compliance | DPDP Act and Rules | Company | n/f | by 13 May 2027 | L-7 | Not started |
| 38 | E-waste producer registration once no longer a micro enterprise | E-Waste Rules 2022 | Operations | n/f | – | L-5 | Not applicable yet |
| 39 | Battery registration only if importing cells | Battery Waste Rules 2022 | Operations | n/f | – | B4-12 | Not applicable yet |
| 40 | M2M registration and certified module if a SIM version ships | DoT guidelines 2022 | Hardware lead | n/f | – | L-3 | Not applicable yet |
| 41 | Local-content declaration for government tenders | PPP-MII Order (2024) | Company | ₹0 | – | L-22 | Not applicable yet |
| 42 | Security audit by an empanelled auditor; insurance programme | CERT-In; contracts | Company | n/f | yearly | B4 step 23, L-17 | Not applicable yet |

## Red lines – do not do these now

1. **Do not test on real patients without a registered ethics committee's approval** – and, until CDSCO or a consultant says otherwise in writing, without the CDSCO permission in L-1.
2. **Do not put real patient data into the current demo system.** It is hosted outside India, has no login, no consent record and no breach plan. Fake patients only.
3. **Do not say or print "prevents pneumonia"**, or name any disease, or say "safe", "clinically proven" or "CDSCO approved". (B4-20)
4. **Do not hand a prototype to a hospital or patient "to try"** without a test licence and a written loan agreement. Outside the licensed place and purpose it is an unlicensed device.
5. **Do not pay, gift, or fund travel for any doctor or nurse** for referrals, endorsements or "advice". For government staff this is a corruption offence.
6. **Do not send promotional WhatsApp messages, or any message without opt-in.** Utility templates to consenting patients only. (ledger #207, #213)
7. **Do not let the AI answer a symptom or medical question.** Fixed "contact your nurse / call 112" text only.
8. **Do not publish new hardware details** (mount, calibration method, enclosure design) before deciding on patent and design filings.
9. **Do not list the app publicly with "not a medical device"**, and do not list it as a medical device without a licence.
10. **Do not sign anything through a founder who is under 18**, and do not accept work from anyone without a written IP assignment.
11. **Do not take money from the public for shares** (equity crowdfunding) or CSR money as a "donation to the startup".
12. **Do not record calls silently.** Announce and get a recorded "yes".

## Decide this month (founders)

1. Company form and who the directors are (all 18+, one resident in India).
2. Which state: it fixes the first hospital, state grants, stamp duty and the state licensing authority.
3. Who owns what: founder shares, vesting, and the IP assignment.
4. The first-study route: (a) government hospital as sponsor with CDSCO permission and no fee; (b) licence first, study after; (c) usability-only work that is not a device study.
5. Display numbers (millilitres) or only "good breath / try again"? It may change the class (B4-1).
6. Sell, lend, or software-only for the pilot (B6-19): it changes who is the data fiduciary, the GST rate and who holds the units.
7. Bluetooth-only, with no SIM, for version 1 (avoids L-3).
8. Battery in the box or USB-powered (avoids L-4 and battery rules).
9. Keep the repo public or make it private from now on (L-10).
10. Budget for four paid first hours with advisers (below).

## Questions for the first paid hour with each adviser

### Regulatory consultant (CDSCO)
1. Is our unit Class A (measuring) or Class B? Would showing no numbers change it?
2. Is there a predicate device approved in India? How do we search and prove it?
3. For a hospital-led study of the unlicensed prototype, does CDSCO require Form MD-22? Can you get that in writing?
4. If Class A, will CDSCO license it without clinical investigation data (rule 63, second proviso)?
5. Can a college team hold a test licence (MD-13), and can the pilot hospital be named as a place of use?
6. Loan licence: which licensed makers would host us, and what parent-spirometer documents are needed (B4-2)?
7. What changed in the 2026 amendments (G.S.R. 270(E), 515(E), 743/744(E)) for our class?
8. Is a volume-indicating accessory a specified instrument under Legal Metrology? What must the retail box carry?
9. Which test reports will the Notified Body expect, and from which labs, at what cost?
10. How are software updates treated after licence: which are "major changes" needing prior approval?

### Company secretary / chartered accountant
1. Private limited or LLP for our grant and investor plans? Total government cost in our state?
2. First-year compliance calendar with dates, forms and late fees.
3. Can a full-time student be a director? Any college permission needed?
4. DPIIT recognition and Udyam: order, timing, and which benefits apply now (80-IAC, labour self-certification after the codes).
5. GST: when must we register; is our product 5% or 18%; should we seek an advance ruling?
6. How should a grant received by an individual be moved to the company and taxed?
7. What TDS will hospitals deduct from our invoices, under the 2025 Income-tax Act numbering?
8. Founder vesting and an ESOP pool: how to set up at incorporation.
9. Convertible note versus CCPS for a first ₹10–50 lakh cheque.
10. Can CSR-funded hospital purchases of our units be structured cleanly?

### IP attorney / patent agent
1. Given the prior art (ledger #50, #86, #132) and our public repo, is anything still patentable? Cost of a novelty search?
2. Does any grace period cover what we have already shown?
3. Did Tidal Medical file in India?
4. Provisional now, or wait for a hardware detail worth claiming?
5. Does our college's policy give it ownership or a share? What release do we need?
6. Do the hackathon terms give the organisers any rights?
7. Is SPIROBUDDY registrable in classes 9, 10, 42, 44? Any conflicting marks?
8. When to file the design, given our video and pitch dates?
9. Review our contributor IP assignment (perpetual, worldwide, moral-rights waiver).
10. Any ownership risk in AI-assisted code, and what records should we keep?

### Healthcare lawyer
1. Review the pilot agreement, unit-loan terms and data processing agreement.
2. Until May 2027, what exactly must the consent say under the SPDI Rules, and how do we document consent from a patient who cannot read?
3. Are we a processor or a joint fiduciary if our app shows the family updates?
4. Our AI vendors and server are abroad: what must the notice and contract say?
5. Does any nursing or physiotherapy council rule restrict nurse follow-up by phone or WhatsApp?
6. Is the 2002 medical ethics code (with the telemedicine appendix) the one in force? Does an AI reminder call fall under it?
7. Liability split and caps with the hospital; what can we not exclude?
8. What may we lawfully give a hospital or clinician (units, training, study costs) under the 2002 Regulations, the marketing code and the corruption law?
9. Review our claims list, web copy and store listing.
10. Personal criminal exposure of founders for negligent harm, and how insurance and process reduce it.

## What to say, and not say, about legal status in a 5-minute pitch

**Say**
- "We have mapped the law. Our unit shows a measurement, so it needs a state manufacturing licence. Official fee ₹5,000 plus ₹500." (B4-1, B4-3)
- "Prototypes are made under a ₹500 test licence. Our first patient study will be hospital-led with a registered ethics committee, and we will take CDSCO's written view on central permission before enrolling anyone." (B4-4, L-1)
- "The AI never diagnoses or counsels. Indian rules reserve that for doctors, and our design sends every symptom to the nurse." (L-8)
- "Today the demo uses only fake patients. We build to the data law that takes full effect on 13 May 2027." (L-7)
- "The radio module we will use is already approved in India; an India-made unit using it unchanged needs no separate radio approval." (L-2)

**Do not say**
- "We only need an ethics committee" / "no CDSCO permission is needed." Not established. (L-1)
- "It is a wellness product" or "Class A, registration only." (B4-1)
- "DPDP compliant", "HIPAA compliant", "certified", "approved".
- "Patent pending", "patentable", or "we own all the IP." (L-10, L-12)
- "Prevents pneumonia", "reduces complications", "clinically proven". (B4-20)
- "Doctors recommend it" or any named clinician's endorsement. (L-21)
- Any rupee figure for consultants, testing, audits or insurance: none is sourced.

## Still not confirmed (and what we tried)

| # | Open item | What we tried |
|---|---|---|
| 1 | CDSCO's own view on academic studies of unlicensed devices | Searched for FAQ/guidance; found only a pre-2018 checklist. Needs a written query. |
| 2 | Whether a predicate exists; Class A-measuring or B | Not answerable from public sources. |
| 3 | MDR amendments after Oct 2022 in primary form | The CDSCO copy read is amended to 14 Oct 2022. |
| 4 | DoT's own ETA clarification PDF and current fee | dot.gov.in returned 403/404; BSNL host unreachable; read a Scribd copy of the FAQ. |
| 5 | MTCTE scope for LTE modules; M2M registration fee | Search returned nothing specific. |
| 6 | Exact e-waste Schedule I medical entries; registration fee; lending = producer? | Main rules PDF not opened; CPCB FAQ read. |
| 7 | Legal Metrology: spirometer not a specified instrument; retail-box declarations | Snippets only. |
| 8 | Gazette text of the DPDP commencement notification | Wiki quoting it returned 503; three secondary sources agree. |
| 9 | Telemedicine guidelines primary PDF | Four hosts in the ledger blocked; two summaries read. A MediaNama-hosted copy exists, unopened. |
| 10 | Nursing/physiotherapy council tele-practice rules | Nothing surfaced. |
| 11 | TRAI 2026 amendment Gazette date; AI-voice disclosure on calls | No new source. |
| 12 | Official IP India fee schedule; SIPP scheme after Mar 2026 | Official schedule page not reachable; practitioner tables agree. |
| 13 | Consumer Protection Act sections 2(36), 87 wording | Official copy failed to download. |
| 14 | Materiovigilance reporting duty; case-law details; Mental Healthcare Act wording; call-recording ruling | Searches hit rate limits; general knowledge only. |
| 15 | Company-law deadlines, penalties, incorporation fees; labour thresholds under the codes; all tax rates except 5% GST | Snippets and general knowledge. |
| 16 | UCMPMD 2024 primary text and its 2025 revision | Summaries only. |
| 17 | RPwD draft rules of July 2026: final or not | One law-firm note; status unknown. |
| 18 | Apple's guideline text; store fees | Snippets only. |
| 19 | The team's college IP policy; this hackathon's terms | With the team. |

## Sources opened this round

| # | URL | Title | Publisher | Grade | Used in |
|---|---|---|---|---|---|
| 1 | https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2022/m_device/mdr,%202017%20(1).pdf | Medical Devices Rules 2017, consolidated, as amended to G.S.R. 777(E) 14 Oct 2022 (248 pp; a third copy, different URL from ledger #183 and #287); rules 3, 26, 31–33, 49–58, 63, 89–91, Seventh Schedule | CDSCO | A | L-1, L-17, L-24 |
| 2 | https://www.khaitanco.com/sites/default/files/2021-08/Ergo_31032020.pdf | Telemedicine Practice Guidelines (update, 31 Mar 2020) | Khaitan & Co | B | L-8 |
| 3 | https://tnpcb.gov.in/owems/pdf/regulations/Ewaste%20Rules2022_Amendment%20Jan23.pdf | E-Waste (Management) Amendment Rules 2023, G.S.R. 61(E), 30 Jan 2023 | MoEFCC gazette, Tamil Nadu PCB copy | A | L-5, correction 1 |
| 4 | https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadImmunization/Prescreening_Medical_Devices_Clinical_Trial.pdf | Checklist for applications for new medical devices / clinical trials (pre-2018, Form 44 era) | CDSCO | A (outdated) | L-1 (context only) |
| 5 | https://www.scribd.com/document/425353387/ETA-FAQ (read via r.jina.ai) | ETA FAQ (WPC self-declaration): fee, modules, India-made products, validity | DoT/WPC text on a third-party host | B | L-2, L-24 |
| 6 | https://www.acma.in/uploads/docmanager/FAQ_E-waste_23012024.pdf | FAQ on E-Waste (Management) Rules 2022, 23 Jan 2024 | CPCB text, hosted by ACMA | A | L-5 |
| 7 | https://www.voiceofsap.org/wp-content/uploads/2023/05/RPWD-Amendment-Rules-2023-ICT-Products-and-Services.pdf | Rights of Persons with Disabilities (Amendment) Rules 2023 (gazette copy) | DEPwD gazette, NGO-hosted copy | A | L-19 |
| 8 | https://khaitanco.com/sites/default/files/2022-02/Ergo_11022022_1.pdf | DoT issues guidelines for regulating M2M service providers (11 Feb 2022) | Khaitan & Co | B | L-3 |
| 9 | https://annauniv.edu/ipr/files/downloadable/ANNA%20UNIVERSITY%20IP%20POLICY.pdf | Anna University IP Policy (2023) | Anna University | B | L-12 |
| 10 | https://www.iitk.ac.in/ipr/data/IPR-Policy.pdf | IPR Policy | IIT Kanpur | B | L-12 |
| 11 | https://iitpkd.ac.in/sites/default/files/2021-05/IITPalakkadIPRPolicy.pdf | IIT Palakkad IPR Policy | IIT Palakkad | B | L-12 |
| 12 | https://bpni.org/News/Ethics-Regulations-MCI.pdf | Indian Medical Council (Professional Conduct, Etiquette and Ethics) (Amendment) Regulations 2009, clause 6.8 | Medical Council of India notification, NGO-hosted copy | A | L-21 |
| 13 | https://support.google.com/googleplay/android-developer/answer/16679511?hl=en | Health content and services policy | Google Play Console Help | B | L-25 |
| 14 | https://www.mha.gov.in/sites/default/files/250883_english_01042024.pdf | Bharatiya Nyaya Sanhita 2023, sections 106, 125 | Ministry of Home Affairs | A | L-17 |
| 15 | https://www.medianama.com/2020/03/223-summary-india-telemedicine-guidelines/ (read via r.jina.ai) | Summary: India's Telemedicine Guidelines 2020 | MediaNama | B | L-8 |
| 16 | https://www.dot.gov.in/static/uploads/2026/05/2dcea4c9d16dac8330428634a661b440.pdf | Public Procurement (Preference to Make in India) Order 2017, revision of 19 Jul 2024 | DPIIT order, DoT-hosted copy | A | L-22 |
| 17 | https://www.startupindia.gov.in/content/sih/en/startupgov/self-certification.html | Self-certification (labour laws) | Startup India | A | nothing extracted (script-rendered page) |
| 18 | https://web.iitd.ac.in/~elangovan/ethics/doc/india-medical-devices-rules-2017.pdf | MDR 2017 copy | IIT Delhi | – | nothing useful (404); read via #1 |
| 19 | https://dot.gov.in/sites/default/files/Clarification%20to%20OM%20dated%2026th%20February%2C%202019%20on%20ETA_0.pdf | Clarification to OM of 26 Feb 2019 on ETA | DoT | – | nothing useful (403 / 404) |
| 20 | https://dot.gov.in/sites/default/files/Instructions%20for%20grant%20of%20Equipment%20Type%20Approval%20%28ETA%29%20through%20Self-Declaration%20on%20SARAL%20SANCHAR%20Portal_0.pdf | Instructions for ETA through self-declaration | DoT | – | nothing useful (blocked page) |
| 21 | https://flash.bsnl.co.in/circular/licenses_issued/ETA_FAQ.pdf | ETA FAQ | BSNL host | – | nothing useful (host not found); read via #5 |
| 22 | https://dpdp.myndsolution.com/wiki/notifications/gsr-843e-2025-commencement/ | G.S.R. 843(E) commencement notification (wiki copy) | MYND | – | nothing useful (503); search summary used in L-7 |
| 23 | https://consumeraffairs.nic.in/sites/default/files/CP%20Act%202019.pdf | Consumer Protection Act 2019 | Department of Consumer Affairs | – | nothing useful (no file returned) |
| 24 | Search snippets only, NOT opened: Freyr WPC guide; Bar & Bench on M2M guidelines; Corpseed/Agile Regulatory/Kiwa on BIS; Lakshmikumaran, Corpseed, compliance pages on E-waste Schedule I; TaxGuru/Simpliance on Legal Metrology amendments; Acuity Law, Taxmann, MYND wiki on DPDP commencement; Lexplosion, Mondaq, SS Rana on IT Rules Feb 2026 and India AI Governance Guidelines; Intepat, SS Rana, BananaIP fee tables and ipindia.gov.in rule 7; SCC Online, IndiaLaw on RPwD rules and cases; AZB, Lexplosion, BioVoice on UCMPMD; Medical Dialogues, LiveLaw, Luther on IMC clause 6.4 and the Prevention of Corruption Act; Cyril Amarchand on product liability; ipleaders, DLA Piper, KPMG on labour codes; TaxGuru and others on GST, MSMED s.15–16, s.43B(h), angel tax, 80-IAC; Treelife/Mondaq on convertible notes; Tribune/Down To Earth on FDI; Invest India/Nishith Desai on CSR Schedule VII; Intepat/World Trademark Review on the DABUS copyright order; IIT Bombay "Insight" on IP policy; hackathon terms of OpenAI, Samsung Next, Liquid AI, NUS; Apple guideline summaries; indiabioscience on ICMR consent witness | various | C | L-2 to L-26 as marked |

---
*Not legal advice. Prepared from public sources on 10 Oct 2026 for planning. Confirm each item with the named adviser before acting.*
