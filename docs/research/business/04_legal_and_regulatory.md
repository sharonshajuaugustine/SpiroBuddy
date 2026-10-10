# Legal and regulatory map: prototype → paid hospital pilot → sale in India

**Written:** 10 Oct 2026 · **Sources opened:** 20 (15 useful, 5 blocked or empty) · **Confidence overall:** medium (high on the Medical Devices Rules text and fees; low on 2026 amendments, radio approval, insurance prices)

> **This is a map with sources, not legal advice.** Every "our reading" below is the team's reading of a rule. Confirm with a regulatory consultant, a lawyer and a chartered accountant before acting. Rules change: each one carries its date.

Short forms used: **CDSCO** = India's central drug and medical-device regulator. **MDR 2017** = Medical Devices Rules 2017, the law for devices. **SLA** = State Licensing Authority (the state drug controller). **CLA** = Central Licensing Authority (CDSCO itself). **Notified Body** = a private audit firm registered with CDSCO to inspect factories. **QMS** = quality management system, the written way a maker controls design and production. **EC** = ethics committee. **DPDP** = Digital Personal Data Protection Act 2023.

---

## Answer in 10 lines

1. **The unit needs a manufacturing licence, not just a free registration.** Free registration is only for Class A devices that are non-sterile *and non-measuring*. CDSCO's own FAQ says a device "measures" if it shows a body quantity in units. Ours shows millilitres. (B4-1, B4-2)
2. **The licence is cheap; the paperwork is not.** Official fee: ₹5,000 per site + ₹500 per device for Class A (measuring) or Class B, from the state authority. Class A: decision in 45 days, audit afterwards. Class B: audit first; the rule's clock adds up to about 140 days. (B4-3)
3. **A ₹500 test licence (Form MD-12 → MD-13) is the legal way to build prototypes for evaluation.** Decision within 30 days, valid 3 years. CDSCO's FAQ says prototypes for validation testing use this route. (B4-4)
4. **A patient study with an unlicensed prototype is the hard part.** The "ethics committee only" exemption in the rule applies to an academic study on a **licensed** device. Otherwise the rule asks for CDSCO permission (MD-22 → MD-23), fee ₹1,00,000, decision within 90 days. (B4-6)
5. **The quickest lawful first study is therefore a hospital-led academic study**, approved by that hospital's registered ethics committee, where the prototype only *watches* an exercise the nurse already prescribed. Whether that needs CDSCO permission for an unlicensed add-on is the single most important question to put to a consultant. (B4-6, B4-7)
6. **No medical device is on the BIS compulsory-registration list**, but the lithium cell and any mains charger are. Buy BIS-registered cells and a BIS-registered USB adaptor; don't make your own. (B4-10)
7. **The radio (Bluetooth/Wi-Fi) needs WPC approval.** A pre-approved ESP32 module helps, but the approval certificate is per model; whether our finished product needs its own is not confirmed. (B4-11)
8. **Data law is mid-switch.** DPDP consent-manager rules start 13 Nov 2026; the main duties start 13 May 2027. Until then the older IT Act health-data rules (2011) still apply. The Data Protection Board had no members as of Aug 2026. (B4-13, B4-14)
9. **The Telemedicine Guidelines say AI platforms may not counsel patients or prescribe; they may only assist a doctor.** So the coach must stay on "how to do the exercise", and every clinical decision stays with the nurse or doctor. (B4-15)
10. **Never say "prevents pneumonia" in any advert.** Pneumonia is item 42 in the Schedule of the Drugs and Magic Remedies Act 1954; advertising an "article" as preventing it is a criminal offence. (B4-20)

---

## Findings

### 1. CDSCO path

### B4-1: A device that shows a body measurement in units is a "measuring" device, so the free Class A registration route is closed to us
- Detail: CDSCO FAQ (Doc No. CDSCO/FAQ/MD/01/2024), Q72: a device is measuring if it is "intended by the manufacturer to measure quantitatively a physiological or anatomical parameter… and the result of the measurement is displayed in legal units". Q69–71: Class A non-sterile non-measuring devices are exempt from the licensing chapters; they only register online, get a system-generated number, and pay **no fee**. SpiroBuddy shows inhaled volume in mL.
- Source: CDSCO FAQ on Medical Devices 2024 – https://www.cdsco.gov.in/opencms/export/sites/CDSCO_WEB/Pdf-documents/MDfAq24.pdf – grade A. Also ledger #150 (item 496, plain incentive spirometer = Class A non-measuring).
- Status: CONFIRMED (primary source; class itself is still the team's reading, ledger #183)
- What it means for SpiroBuddy: Plan for a licence (Form MD-5), whether CDSCO calls us Class A-measuring or Class B. A version that showed *no* numbers (only "good breath / try again") might argue non-measuring; that is a design choice to discuss with a consultant, not a loophole to assume.

### B4-2: An accessory sold on its own is licensed like a device; software inside it takes the same class
- Detail: MDR 2017, First Schedule Part I: "Accessories are classified in their own right separately from the device with which they are used"; "Software, which drives a device or influences the use of a device, falls automatically in the same class." FAQ Q60: an accessory is a device "intended specifically by its manufacturer to be used together with a particular medical device (parent) to enable or assist" it. FAQ Q63: for an accessory "marketed individually", follow the Medical Devices Grouping Guideline and "submit requisite documents of the main device(s)". FAQ Q67–68: stand-alone software that meets the device definition is regulated; FAQ Q54: no labelling exemption for software.
- Source: MDR 2017 consolidated text (IIT Madras copy) – https://www.iitm.ac.in/sites/default/files/Others/medicaldevicesrules2017.pdf – grade A; CDSCO FAQ 2024 (above) – grade A.
- Status: CONFIRMED
- What it means for SpiroBuddy: Our application will need documents about the parent spirometer (e.g. Romsons Breazer). Ask the spirometer maker early, or pick a parent whose maker will cooperate. The coaching app and firmware are part of the device, not a separate "wellness app".

### B4-3: Manufacturing licence, Class A (measuring) or Class B: official fee ₹5,000 + ₹500, state authority, 45 days (A) or about 140 days (B)
- Detail (MDR 2017 rule 20 and Second Schedule):
  - Apply on the Ministry's online portal in **Form MD-3** to the **State Licensing Authority**, with the Fourth Schedule Part II documents and an undertaking that the Fifth Schedule QMS is followed. Licence comes in **Form MD-5**.
  - **Fee:** ₹5,000 for one site + ₹500 for each distinct device. Retention fee: same amounts (rule 29).
  - **Class A (measuring):** SLA decides within **45 days**. No audit before grant; a Notified Body audits within **120 days after** grant.
  - **Class B:** Notified Body audit within **90 days** of application; its report within **30 days**; SLA decision within **20 days** of the report. The QMS must be verified by audit **before** grant.
  - The SLA assigns the Notified Body; the maker cannot choose (FAQ Q83). The Notified Body's own audit charge is **not** in the fee table: not found.
  - Class C/D for comparison: Form MD-7 → MD-9, to CDSCO centrally, ₹50,000 + ₹1,000.
  - **Loan licence (MD-4 → MD-6):** lets a company make its device at another licence-holder's factory (FAQ Q82).
- Source: MDR 2017 (IITM copy, above) – A; CDSCO fee table – https://www.cdscomdonline.gov.in/NewMedDev/resources/app_srv/NMD/global/helpfiles/FeePaidDetails.pdf – A; CDSCO FAQ 2024 – A.
- Status: CONFIRMED for fees and rule timelines. **NOT CONFIRMED:** a June 2026 draft (G.S.R. 515(E)) reportedly cuts the Class B audit window from 90 to 30 days; search snippets only (C), and we could not confirm it is final.
- What it means for SpiroBuddy: A **loan licence with an existing licensed Indian device maker** is the realistic route for a student team: no factory of our own. Government fees are under ₹10,000; the real cost is the QMS, the technical file and testing (no official price found).

### B4-4: Test licence for prototypes: Form MD-12 → MD-13, ₹500 per device, 30 days, valid 3 years
- Detail: MDR 2017 rule 31: a "small quantity" of any class may be made "for the purpose of clinical investigations, test, evaluation, examination, demonstration or training". Apply in Form MD-12 to the **Central** Licensing Authority; decision within 30 days; licence valid 3 years; keep a record of quantities made. Rule 32: devices may be used only for those purposes, at the place named in the licence. FAQ Q59: prototypes for "techno-commercial feasibility testing, verification & validation testing" → "may obtain Test licence in Form MD-13". FAQ Q47: one licence can list several test sites. Documents: device description and intended use, equipment list, qualified staff list.
- Source: MDR 2017 (IITM copy) – A; fee table – A; FAQ 2024 – A.
- Status: CONFIRMED
- What it means for SpiroBuddy: Before any unit leaves the team's bench for a lab or a hospital, hold an MD-13. It needs a legal entity and an address. A hackathon demo on team members with fake patients is not "sale or distribution"; our reading is that it needs nothing, but a consultant should confirm.

### B4-5: QMS, portal, labelling and UDI
- Detail:
  - **QMS:** the Fifth Schedule of MDR 2017 is the legal requirement (rule 3(zn)). It is modelled on ISO 13485; an ISO 13485 certificate is what Notified Bodies and hospital buyers expect, but the *rule* names the Fifth Schedule. (ISO 13485 link: team knowledge + ledger #202, grade B.)
  - **Portal:** applications go through the Ministry's online medical-devices portal (cdscomdonline.gov.in, where the fee table is hosted). The newer National Single Window System was not checked.
  - **Standards (rule 7):** BIS standard if one exists; if not, ISO/IEC; if not, the maker's validated standard. FAQ Q25 repeats this.
  - **Labelling (rule 44):** name of device; details to identify it and its use; maker's name and factory address; net quantity; month and year of manufacture (expiry not needed for "medical equipment or instruments"); batch/lot number; storage conditions; warnings; "Manufacturing Licence Number"; symbols from BIS/ISO allowed. "Physician's Sample – Not to be sold" on free samples.
  - **UDI (rule 46):** text says "With effect from 1st day of January, 2022" every approved device "shall bear unique device identification" (a GS1-style product code plus batch/serial; for software, the version). Search results say the Ministry deferred this "till further orders" in Dec 2021 and no new date was found.
  - **Legal Metrology:** a 2025 amendment to the Packaged Commodities Rules reportedly lets the MDR 2017 govern label font and placement for devices; MRP and consumer-care declarations still apply. Snippets only.
- Source: MDR 2017 (IITM copy) – A; fee table host – A; UDI deferral and Legal Metrology 2025 – search snippets only – C.
- Status: CONFIRMED for rule text; UDI current date and Legal Metrology 2025 detail NOT CONFIRMED.
- What it means for SpiroBuddy: Put a serial number and firmware version on every unit from the first prototype; it costs nothing and matches UDI when it arrives.

### B4-6: When a patient study needs CDSCO permission, and when an ethics committee is enough – the exact words
- Detail (MDR 2017 Chapter VII):
  - Rule 51(1): permission to run a clinical investigation of an **investigational medical device** is sought from the CLA in **Form MD-22**; granted in **Form MD-23** (rule 52); reject-or-grant within **90 days**.
  - Fee: **₹1,00,000** for a pilot, ₹1,00,000 for a pivotal study. "No fee shall be payable by any institute, organisation, hospital run or funded by the Central Government or the State Government."
  - "Pilot clinical investigation means clinical investigation to be carried out for the first time in human participants."
  - **Rule 51(3):** "No permission for conduct of **academic clinical study on licenced medical device** shall be required, where (a) the Ethics Committee approves such a study; and (b) the data generated during the study shall not be used to furnish to the Central Licensing Authority to manufacture or to import for marketing any investigational medical device in the country."
  - Rule 3(a): "academic clinical study" = "a clinical study conducted for academic purpose on a medical device for the approved or a new intended use, new material of construction, new improved design or new population".
  - Rule 3(x): an "investigational medical device" is one that (i) has no **predicate device** (a similar device already approved in India), or (ii) is licensed but claims a new use, population, material or major design change, "and is being assessed for safety or performance or effectiveness in a clinical investigation".
  - Rule 63: a device with no predicate needs CLA permission (Form MD-26, ₹50,000) after its clinical investigation; "in respect of investigational medical device of Class A, data on clinical investigation may not be required" unless the CLA says so.
  - Class A non-sterile non-measuring devices are exempt from Chapter VII altogether (FAQ Q69), which is why the plain spirometer itself is easy.
  - Rule 55: the sponsor must give medical management and compensation for study-related injury.
- Source: MDR 2017 (IITM copy) – A; fee table – A.
- Status: CONFIRMED (text). How it applies to us is **our reading, not a ruling**.
- What it means for SpiroBuddy: The EC-only exemption is written for a **licensed** device. An unlicensed prototype does not clearly fit. Three lawful shapes for a first study, to put to a consultant: (a) a hospital-run academic study where the hospital's EC decides, and the data is never used for our licence (grey: device unlicensed); (b) a government hospital as sponsor, MD-22 with **no fee**; (c) get the MD-5 licence first, then run an academic study under rule 51(3). Whether an Indian predicate exists for a spirometer-tracking add-on is unknown.

### B4-7: Any study on people also needs a registered ethics committee and should be listed on the trial registry
- Detail: Since 19 Sep 2019 (New Drugs and Clinical Trials Rules 2019, Chapter IV), every EC reviewing biomedical and health research must be registered with the Department of Health Research on the NAITIK portal; provisional registration up to 2 years, final for 5 years. ECs follow ICMR's National Ethical Guidelines. MDR rule 50 routes device studies to the EC set up under the Drugs and Cosmetics Rules.
- Source: MDR 2017 rule 50 (IITM copy) – A; DHR registry and ICMR Bioethics pages – search snippets only – C (government pages, not opened).
- Status: CONFIRMED for rule 50; SINGLE SOURCE (snippet) for DHR detail.
- What it means for SpiroBuddy: Pick a pilot hospital that already has a DHR-registered EC. A college EC that is not registered cannot approve a patient study. CTRI (trial registry) listing: not checked this round.

### B4-8: Is coaching-only software a medical device? CDSCO's 2026 guidance (already in the ledger) says alerts and disease mentions take it out of "wellness"
- Detail: Document name and date: **"Guidance Document on Medical Device Software", CDSCO/MD/GD/MDSW/01/2026, reported 21 Jul 2026** (ledger #135 primary, #123 law-firm summary). It replaces "SaMD/SiMD" with "medical device software"; it is guidance "for public awareness", not law. Nothing new was opened this round. The 2024 FAQ (Q68) adds only: wellness software that meets the device definition is regulated.
- Source: ledger #135 (A), #123 (B); CDSCO FAQ 2024 – A.
- Status: CONFIRMED (from earlier rounds)
- What it means for SpiroBuddy: The software drives a measuring unit, so it takes the unit's class (B4-2). A phone-only coach with no sensor and no disease words would be the only "wellness" candidate.

### 2. Standards and test labs

### B4-9: Standards the unit would be tested against; none is named in Indian law for this product, but rule 7 makes ISO/IEC the default
| Standard | Covers, in one line | Position in India |
|---|---|---|
| IEC 60601-1 | Basic electrical and mechanical safety of medical electrical equipment | Applies through rule 7 where no BIS standard exists; a Notified Body will expect a test report |
| IEC 60601-1-2 | Electromagnetic compatibility (does not disturb, is not disturbed by, other equipment) | Same |
| IEC 60601-1-11 | Extra rules for devices used at home (untrained users, drops, moisture) | Expected, because we claim home use |
| IEC 62304 | How medical software is planned, built, tested and changed | Expected for the firmware and app |
| ISO 14971 | Risk management file: list hazards, reduce them, show what is left | Expected; the Fifth Schedule asks for risk management |
| IEC 62366-1 | Usability: proving ordinary users can use it safely | Expected, important for elderly users |
| IEC 60825-1 | Laser safety classes | The sensor chip is declared Class 1 (eye-safe) by its maker (ledger #118). The finished product should keep the maker's cover-glass and power limits to stay Class 1 |
| ISO 10993 | Biological safety of materials that touch the patient | Needed only for patient-contact parts. A base the spirometer stands on is touched by hands only (intact skin, short contact). Our reading: a materials statement, not full testing; confirm with the test lab |
- Detail: The one-line descriptions are standard catalogue knowledge, not opened this round (ledger #202 lists four of them). "Expected" means expected by a Notified Body or hospital buyer, not written into a notified order for this product. No BIS standard for an incentive-spirometer add-on was found.
- **Labs:** IIT Kanpur's EMI/EMC and Electrical Safety facility says it won NABL accreditation (India's lab accreditation body) in 2024 for full-compliance testing, lists IEC 60601-1 and IEC 60601-1-2, and says it serves startups "at an affordable price"; fees are on a separate page not opened. Bharat Test House, Conformity Testing Labs and TÜV SÜD India also advertise 60601 testing (vendor claims, snippets only, C).
- Source: MDR 2017 rule 7 – A; IIT Kanpur EMC lab – https://www.iitk.ac.in/emc/about-us – B; ledger #118, #202.
- Status: SINGLE SOURCE for the lab; standards list CONFIRMED only as "commonly expected"
- What it means for SpiroBuddy: Budget a pre-compliance test at an academic lab before any hospital pilot; hospitals' biomedical engineers will ask for an electrical-safety report. No test price was found.

### 3. Electronics and radio

### B4-10: BIS compulsory registration: no medical device is listed, but lithium cells and power adaptors are
- Detail: BIS's Scheme-II (Registration) page lists, under the Electronics & IT Goods (Requirement of Compulsory Registration) Order 2021: sealed secondary cells/batteries for portable use (**IS 16046**), power adaptors for IT equipment (IS 13252 Part 1), power banks, smart watches, wireless headphones, Bluetooth speakers. **No medical device appears.** A Feb 2026 MeitY order reportedly adds rated-capacity checks under IS 16047 Part 3 (snippet only). Whether a cell *embedded* in an unlisted product needs its own registration: sources conflict; a 2018 customs notice says embedded batteries and adaptors need it (snippet only).
- Source: BIS, Products under Compulsory Registration (Scheme II) – https://www.bis.gov.in/product-certification/products-under-compulsory-certification/scheme-ii-registration-scheme – A.
- Status: CONFIRMED (list); embedded-cell question NOT CONFIRMED
- What it means for SpiroBuddy: Use a cell and a USB adaptor that already carry a BIS registration number (R-number) and keep the supplier's certificate. Simplest of all: ship no adaptor and no battery in version 1 (USB-powered from a registered adaptor). Air transport of lithium cells follows UN 38.3 testing by the cell maker: not researched this round.

### B4-11: Radio approval (WPC ETA): pre-approved modules exist; whether the finished product needs its own approval is not confirmed
- Detail: The WPC Wing (Department of Telecommunications) issues an **Equipment Type Approval through self-declaration** under O.M. No. ETA-WPC/Policy/2018-19 dated 26 Feb 2019, on the Saral Sanchar portal. We read a real certificate: ETA-SD-20200704087, 23 Aug 2020, for the Espressif **ESP32-PICO-V3-ZERO** Wi-Fi/Bluetooth module, 2402–2480 MHz, licence-exempt under Gazette notification G.S.R. 45(E) of 28 Jan 2005. Its terms: valid only for the stated parameters; "not valid in case any change". A consultancy guide (snippet, C) says a module approval "does not automatically resolve" compliance for the product that contains it; the finished product is assessed in its own configuration. The DoT memo itself returned HTTP 403.
- Source: WPC ETA certificate hosted by Espressif – https://www.espressif.com/sites/default/files/ETA-SD-20200704087%20ESP32-PICO-V3-ZERO%20WPC.pdf – A (government certificate); Freyr guide – snippet only – C.
- Status: SINGLE SOURCE; the end-product question is NOT CONFIRMED
- What it means for SpiroBuddy: Choose the exact ESP32 module variant that already has an ETA and use its stock antenna unchanged. Then ask a WPC consultant whether an India-made product with that module needs its own self-declared ETA. No fee was found in an official source.

### B4-12: E-waste and battery waste: registration with the pollution board is triggered by selling under our own brand
- Detail:
  - **Battery Waste Management Rules 2022** (CPCB FAQ): covers "all types of batteries regardless of chemistry". "Producer" includes anyone who sells batteries "including in equipment, under its own brand". But the FAQ answers directly for makers of "medical equipment… using battery as a component": "If a company is using battery provided by other battery manufacturer/producer, then it will **not** have any EPR obligations." Importing cells ourselves would make us a Producer (register on the CPCB portal, Form 1(A)/1(B)).
  - **E-Waste (Management) Rules 2022** (G.S.R. 823(E), 22 Jul 2022; in force 1 Apr 2023): Schedule I includes a medical-devices category ("except implanted and infected products"); producers register on the CPCB portal and meet recycling targets by buying certificates. Whether our product type is on the list, and any small-producer relief: snippets only.
- Source: Maharashtra Pollution Control Board, FAQs for BWMR 2022 – https://mpcb.gov.in/sites/default/files/inline-files/FAQs_for_BWMR_2022.pdf – A; e-waste – search snippets only – C.
- Status: CONFIRMED (battery); NOT CONFIRMED (e-waste detail)
- What it means for SpiroBuddy: Buy Indian-supplied, branded cells (no import) → no battery registration. Check the e-waste Schedule I list before the first sale; not needed for a pilot where units stay our property and come back.

### 4. Data and digital-health law

### B4-13: DPDP timetable as of Oct 2026: Board on paper since Nov 2025, consent managers from 13 Nov 2026, main duties from 13 May 2027
- Detail: DPDP Rules 2025 notified 13 Nov 2025 (ledger #122). Phase 1 (then): the Data Protection Board provisions and rules 17–21. Phase 2 (**13 Nov 2026**; some sources say 14 Nov): rule 4, **consent managers** (a registered go-between that lets a person give and withdraw consents in one place). Phase 3 (**13 May 2027**): notice, consent, security safeguards, breach intimation, rights, retention, children's data, significant data fiduciary duties. LiveLaw, 1 Aug 2026: the Board "has no appointed Chairperson and no appointed Members"; applications were invited on 6 May and 6 Jun 2026.
- Already in the report (not redone): 72-hour breach report, one-year logs, no special health-data category, transfers abroad allowed unless a country is blacklisted (ledger #122, #196).
- Children: verifiable parental consent is required for under-18s (DPDP Act s.9, ledger #196). Significant data fiduciary (a large or sensitive processor named by the Government): extra audits and a data protection officer; no list was found.
- Source: LiveLaw, "India's Data Protection Board: Established in Law, Absent in Fact" – https://www.livelaw.in/articles/india-data-protection-board-established-law-543751 – B; phase dates – search snippets from law-firm notes (JSA PDF returned 403) – C; ledger #122, #196 – A.
- Status: CONFIRMED (dates agree across ledger #122 and two secondary sources); Board status SINGLE SOURCE, two months old
- What it means for SpiroBuddy: We are not a consent manager and need not register as one. Exclude under-18 patients from the pilot to avoid parental-consent machinery. Build to the May 2027 standard now; hospitals already ask for it.

### B4-14: Until May 2027 the older IT Act health-data rules still bind; DISHA never became law
- Detail: A law-firm note (KSK) says section 44(2) of the DPDP Act, which removes IT Act section 43A (the base of the 2011 "SPDI Rules" that treat medical records as sensitive and ask for written consent), sits in the 18-month tranche, i.e. May 2027. Until then SPDI "continues to operate". DISHA (Digital Information Security in Healthcare Act) was a March 2018 draft; a 2023 journal paper still calls it "proposed"; no enactment found. CERT-In Directions of 28 Apr 2022 (6-hour incident report, 180-day logs in India) remain (ledger #194).
- Source: search snippets only (KSK; Indian Journal of Medical Ethics 2023) – C; ledger #194 – A.
- Status: NOT CONFIRMED from primary text (section 44 commencement notification not opened)
- What it means for SpiroBuddy: For a pilot before May 2027, collect **written or recorded** consent that names health data (meets both regimes), and publish a privacy policy. Do not cite DISHA.

### B4-15: Telemedicine Practice Guidelines 2020: AI platforms may assist a doctor but may not counsel or prescribe
- Detail: Notified 25 Mar 2020; they govern **registered medical practitioners** giving consultations, and platforms that host them. An International Bar Association summary: AI/ML platforms "are not permitted for consultations or the prescribing of medicines"; they may "assist the registered medical practitioner". Another summary (snippet): only a doctor can counsel; "the final prescription or counseling has to be directly delivered by the doctor". Text tools such as WhatsApp are listed as allowed channels for doctors. The guidelines also cover health-worker-to-doctor consultations.
- Source: IBA, "India's new telemedicine guidelines" – https://www.ibanet.org/article/15234243-b534-45f6-b303-4919cfe9a2dc – B. Primary PDF still unread (ledger #214–217 failed).
- Status: SINGLE SOURCE (secondary)
- What it means for SpiroBuddy: Our reading: a tool that coaches an exercise a nurse already prescribed, and connects the patient to a nurse, is not itself a "teleconsultation". But the AI must never give medical advice, and if a **doctor** uses our call link to consult, the guidelines apply to that doctor. Keep the fixed "contact your nurse / call 112" reply for any symptom.

### B4-16: What a hospital will ask for in a data processing agreement (DPA)
- Detail (team synthesis from DPDP Rules #122, CERT-In #194, Meta terms #210–212; not a published hospital template): hospital = data fiduciary (decides why data is used), SpiroBuddy = processor; purpose limited to the pilot; list of data items; India storage location and named sub-processors (cloud host, Meta, voice and AI vendors); encryption and role-based access; access logs kept 1 year; breach notice to the hospital "without delay" so it can meet 72 hours (and CERT-In's 6 hours); help with patient requests (access, correction, erasure, withdrawal); deletion or return at pilot end; audit right; no secondary use, no training of AI on patient data without consent; staff confidentiality; liability cap and indemnity.
- Source: ledger #122, #194, #210–212.
- Status: NOT CONFIRMED as a hospital's actual template (none found)
- What it means for SpiroBuddy: Draft our own two-page DPA and bring it to the hospital; it speeds the IT review.

### 5. Messaging and calls (new only)

### B4-17: TRAI's 2026 call rules were notified on 18 Sep 2026; the Gazette date is still not found; no rule requires telling the listener "this is an AI"
- Detail: Secondary reports number it Regulation 05 of 2026, notified 18 Sep 2026; most provisions start 30 days after Gazette publication (so about 18 Oct 2026 **if** published the same day: an inference, not a fact). The duty found is to **pre-declare** automated (A2P) calling and caller IDs to the telecom operator, not to announce AI on the call. Separately, the IT (Intermediary Guidelines) Amendment Rules, G.S.R. 120(E) of 10 Feb 2026, in force 20 Feb 2026, require **labelling of synthetically generated audio/visual content** by platforms; whether a one-to-one phone call is covered is not stated in any source found. ASCI (the advertising self-regulator) issued AI-content labelling guidelines for adverts on 29 Sep 2026, effective three months later.
- Source: search snippets only (telecom press; Hogan Lovells/Freshfields notes; exchange4media) – C; ledger #106, #139 – A.
- Status: NOT CONFIRMED (Gazette date; AI-call disclosure)
- What it means for SpiroBuddy: Open every automated call with "This is an automated voice assistant from <hospital>". It is cheap, honest, and covers any reading of the 2026 rules. SMS DLT fee remains unconfirmed (no new source).

### 6. Liability and contracts

### B4-18: Consumer Protection Act 2019 makes the maker liable for defects, wrong instructions and broken promises; misuse and ignored warnings are defences
- Detail: Chapter VI (sections 82–87), in force 20 Jul 2020. A "product manufacturer" includes anyone who makes, assembles, designs or puts its own mark on a product. Liable for manufacturing or design defect, departure from specification, **failure to give adequate instructions or warnings**, and breach of an **express warranty even without negligence** (s.84). A "product service provider" is liable for deficient service or missing warnings (s.85). Section 87 defences include misuse and an obvious risk the user should have known. The Central Consumer Protection Authority can order recalls and fine up to ₹10 lakh (₹50 lakh for repeats) for misleading adverts. Clinical negligence stays with the treating professional and hospital under ordinary negligence law; a tool that coaches while "the nurse decides" still carries product liability for wrong readings or wrong instructions.
- Source: IBA / Nishith Desai, "The changing face of product liability regime in India and its impact on the med-tech sector" (c. mid-2020) – https://www.ibanet.org/article/B20060BD-6365-425E-A9D9-6FFDFC477F62 – B; section details and penalties – search snippets – C.
- Status: CONFIRMED (two secondary sources agree; statute not opened)
- What it means for SpiroBuddy: The protection is in the **intended-use statement and instructions**, not in a disclaimer. Write: "An exercise coach and adherence tracker for a spirometer your nurse prescribed. Not for diagnosis or monitoring of any disease. Volumes are estimates. If you feel breathless, chest pain or fever, stop and contact your nurse or call 112." Never promise an outcome (that is an express warranty).

### B4-19: Insurance exists but no Indian insurer publishes a medtech price
- Detail: Clinical-trial liability policies are sold in India (SBI General publishes a wording; New India Assurance, ICICI Lombard named in press). Product-liability and professional-indemnity cover for device makers is sold through brokers. The only published price found: an SME cyber policy, ₹1 crore cover for about ₹50,000 a year (2023 press release, not a medtech quote).
- Source: search snippets only – C.
- Status: NOT CONFIRMED
- What it means for SpiroBuddy: Get one broker quote for (a) clinical-trial/no-fault cover for the pilot and (b) product liability + cyber. An EC will usually ask for (a).

**Key clauses of a hospital pilot agreement (team synthesis, not from a published template):** purpose and duration; who is sponsor and who is investigator; EC approval as a condition; device stays our property and is on loan; intended use and limits; nurse retains all clinical decisions; training and support; adverse-event reporting both ways; insurance and compensation (MDR rule 55 if it is a clinical investigation); data roles (attach the DPA); IP (each side keeps its own; results and publications agreed); price or no-charge statement; confidentiality; termination and device return; governing law.

### 7. Advertising and claims

### B4-20: "Prevents pneumonia" in an advert is a criminal offence, not just a regulatory risk
- Detail: Drugs and Magic Remedies (Objectionable Advertisements) Act 1954. Section 2(b)(iii): "drug" includes "any article, other than food, intended to affect or influence in any way the structure or any organic function of the body". Section 3(d): no advertisement may suggest a drug is for "the diagnosis, cure, mitigation, treatment or prevention of any disease… specified in the Schedule". Schedule item **42: Pneumonia**. Section 7: first conviction up to 6 months' prison or fine or both; later, up to 1 year. "Advertisement" includes labels, circulars and spoken announcements. Whether a breathing-exercise coach is an "article intended to affect an organic function" is our cautious reading.
- Also: the Uniform Code for Marketing Practices in Medical Devices 2024 (Department of Pharmaceuticals, 6 Sep 2024): efficacy claims must rest on current evidence and the instructions for use; product claims must match the licence; no promotion before approval; "safe" not to be used unqualified (KPMG summary; last two points from snippets).
- ASCI Code: health claims need evidence in proportion; "cure" and absolute claims are regularly struck down (snippets, C).
- Source: Act text (Tripura High Court copy) – https://thc.nic.in/Central%20Governmental%20Acts/Drugs%20and%20Magic%20Remedies%20(Objectionable%20Advertisement)%20Act,%201954.pdf – A; KPMG, UCMPMD 2024 summary – https://assets.kpmg.com/content/dam/kpmg/in/pdf/2024/10/uniform-code-for-marketing-practices-in-medical-devices.pdf – B.
- Status: CONFIRMED (Act text); application to us is our reading
- What it means for SpiroBuddy: **May say:** "helps patients do the breathing exercise their nurse prescribed", "shows the care team who is falling behind", "a prototype". **May not say:** prevents/treats/detects pneumonia or any disease; "safe"; "clinically proven"; "CDSCO approved"; anything before a licence that reads as an offer to sell a medical device.

### 8. Intellectual property

### B4-21: Patent: the sensing idea is prior art; only a narrow, specific claim could survive. Design and trademark are cheap and worth doing
- Detail:
  - **Prior art already in the ledger:** Tidal/InSee US patent US10610129B1 (#86) and its PCT WO2022204480A1 (status "ceased", #132) on portable monitoring of incentive spirometry; the Michigan clip-on paper, Burns et al. 2023 (#50), which already tracked the piston and classified breaths; hobby voice-coach projects (#119). Published work anywhere in the world defeats novelty in India. Whether Tidal filed in India is still unchecked (the Indian patent search needs a human; report §11.1 item 2).
  - Our reading: a broad claim ("sensor reads a spirometer and coaches") is not patentable. A narrow claim on something truly new (e.g. the under-base mounting for Indian spirometers, or the calibration method) might be; needs a patent agent's search.
  - **Fees (search snippets of practitioner fee tables, C; confirm on ipindia.gov.in):** patent e-filing for a startup or individual ₹1,600 (others ₹8,000); request for examination ₹4,000; expedited examination (rule 24C, Form 18A, open to startups) ₹8,000 (others ₹60,000). Design registration ₹1,000 per design per class for startups/individuals (others ₹4,000). Trademark ₹4,500 per class e-filed for individuals/startups/small enterprises (others ₹9,000).
  - **SIPP scheme** (government pays the patent facilitator's professional fee for recognised startups): reported valid until 31 Mar 2026; extension not confirmed.
  - **Trademark search:** IP India's free public search (tmrsearch.ipindia.gov.in) → choose "Wordmark", type SPIROBUDDY, and check class **10** (medical apparatus), class **9** (software, sensors) and class **44** (medical services). Also try "phonetic" search for sound-alikes (SPIRO BUDDY, SPYROBUDDY). The site needs a human at a browser; not done this round.
  - **Who owns it:** the National Innovation and Startup Policy 2019 (Ministry of Education) is reported to say: IP is **jointly owned** by inventors and institute when institute facilities or funds are "used substantially" or the work is part of the curriculum; inventors own it fully when no institute resources are used; institute/incubator equity typically 2–9.5%. College summaries only (C); the one PDF opened had no clause text. Individual institutes differ (one found gives the institute ownership with a 70:30 revenue split to inventors).
- Source: ledger #50, #86, #132, #119; IP fees and NISP – search snippets – C; Delhi University NISP note (opened, nothing useful) – https://www.slc.du.ac.in/uploads/research/innovation-council/2019-20/National_Innovation_and_Start-up_Policy.pdf.
- Status: NOT CONFIRMED (fees and NISP from snippets); prior art CONFIRMED from ledger
- What it means for SpiroBuddy: **The team must read two documents before the pitch answer "we own it":** their own college's IP policy and the hackathon's terms and conditions. File the trademark first (cheapest, fastest), a design registration once the enclosure is final and before it is shown publicly in final form, and treat a patent as optional.

---

## 10. Compliance checklist (order · owner · cost · time)

Costs are official fees where a source gives one. "n/f" = no sourced figure found. Professional fees are not included.

### Stage 1 – before any real patient touches it
| # | Step | Owner | Official cost | Time by rule |
|---|---|---|---|---|
| 1 | Read college IP policy and hackathon terms; write a one-page founders' IP assignment | Team lead | ₹0 | 1 week |
| 2 | Register a legal entity (needed for every licence below) | Team lead + CA | n/f (agent 3's file may cover) | n/f |
| 3 | One paid hour with a CDSCO regulatory consultant: class (A-measuring or B), predicate, and whether the first study needs MD-22 | Team lead | n/f | 1–2 weeks |
| 4 | Fix the intended-use statement, warnings and "never diagnoses" wording; freeze banned claims (B4-18, B4-20) | Product owner | ₹0 | days |
| 5 | Start the risk file (ISO 14971) and a simple design history; serial + firmware version on each unit | Hardware lead | ₹0 | ongoing |
| 6 | **Test licence** MD-12 → MD-13 for prototype units | Entity | **₹500 per device** | **30 days**; valid 3 years |
| 7 | Bench safety check: BIS-registered cell and adaptor, pre-approved radio module, basic electrical-safety pre-test at a NABL lab | Hardware lead | n/f | n/f |
| 8 | Hospital partner with a **DHR-registered ethics committee**; protocol, patient information sheet and consent form in the patient's language; EC approval | Clinical lead (hospital investigator) | EC fee n/f | EC cycle n/f |
| 9 | If the consultant says it is a clinical investigation: MD-22 → MD-23 | Sponsor | **₹1,00,000** (nil for government-run or -funded hospitals) | **90 days** |
| 10 | Data: India-hosted database, DPA with the hospital, written consent naming health data, breach plan, adults only | Software lead | ₹0 | 2 weeks |
| 11 | Insurance quote for the study (trial/no-fault + product liability) | Team lead | n/f | n/f |

### Stage 2 – before a paid pilot (money changes hands = "sale")
| # | Step | Owner | Official cost | Time by rule |
|---|---|---|---|---|
| 12 | QMS to the Fifth Schedule (ISO 13485 style) | Quality owner | n/f | months |
| 13 | Manufacturing partner with an existing licence → **loan licence** (MD-4 → MD-6), or own licence MD-3 → MD-5 | Entity | **₹5,000 site + ₹500 device** | Class A: **45 days**, audit within 120 days after. Class B: audit ≤ 90 days + report ≤ 30 + decision ≤ 20 |
| 14 | Test reports: IEC 60601-1, 60601-1-2, 60601-1-11; software file (IEC 62304); usability (IEC 62366-1) | Hardware + software leads | n/f | n/f |
| 15 | Label to rule 44, with licence number; instructions for use in local languages | Product owner | ₹0 | – |
| 16 | WPC radio approval position confirmed; ETA if needed | Hardware lead | n/f | n/f |
| 17 | Pilot agreement + DPA signed; WhatsApp on the hospital's verified number; calls through a registered Indian telephony partner with A2P declared | Team lead | – | – |
| 18 | Trademark filed (classes 10, 9, 44) | Team lead | ₹4,500 per class (snippet, C) | – |

### Stage 3 – before selling at scale
| # | Step | Owner | Official cost | Time |
|---|---|---|---|---|
| 19 | Notified Body audits passed; licence retention fee every 5 years | Quality owner | ₹5,000 + ₹500 | – |
| 20 | E-waste producer registration (CPCB) if listed; battery registration only if we import or brand cells | Operations | n/f | – |
| 21 | Legal Metrology declarations (MRP, consumer care) on the pack | Operations | n/f | – |
| 22 | UDI when the Government fixes a date | Quality owner | n/f | – |
| 23 | DPDP full compliance by **13 May 2027**; annual security audit by a CERT-In-empanelled auditor (ledger #205) | Software lead | n/f | – |
| 24 | Post-market complaint and adverse-event system; UCMPMD marketing-code self-declaration | Quality owner | ₹0 | yearly |
| 25 | Design registration; patent only if a narrow novel claim is found | Team lead | ₹1,000 / ₹1,600 (snippets, C) | – |

---

## What to say in the 5-minute pitch (5 bullets max, each with its source)
- "We have read the law: our unit shows a measurement, so it needs a state manufacturing licence, not just a free registration. The official fee is ₹5,000 plus ₹500." (CDSCO FAQ 2024 Q72; MDR 2017 Second Schedule)
- "Prototypes for evaluation are made under a ₹500 test licence, decided in 30 days." (MDR 2017 rule 31; CDSCO fee table)
- "Our first study will be hospital-led, approved by a registered ethics committee, and we will confirm with CDSCO whether it also needs central permission." (MDR 2017 rule 51)
- "The AI never counsels or diagnoses: India's telemedicine guidelines reserve that for doctors, and our design already sends every symptom to the nurse." (IBA summary of TPG 2020)
- "We build to the data law that takes full effect on 13 May 2027: itemised consent, India storage, 72-hour breach reporting." (ledger #122; LiveLaw 1 Aug 2026)

## What NOT to say (claims that would be wrong or unproven)
- "It only needs registration / it's Class A so no licence": wrong for a measuring device.
- "An ethics committee approval is all we need for a patient study": the exemption is written for licensed devices.
- "Prevents pneumonia" or any disease claim: Schedule item 42 of the 1954 Act; also raises the device class.
- "Our ESP32 module is certified, so the product is certified": the certificate is per model; not confirmed for the finished product.
- "We are DPDP compliant / certified": the main duties are not yet in force and no certificate exists.
- "We have a patent / it is patentable": prior art exists (#50, #86, #132); no search done in India.
- "The team owns all the IP": not until the college policy and hackathon terms are read.
- "Licensing takes 45 days": that is only the Class A decision clock, after a complete file; Class B is longer and the technical file takes months.
- Any rupee figure for testing, consultants, Notified Body audits or insurance: none was found in an official source.

## First 90 days: concrete next steps (who does what, rough cost in ₹ where a source gives one)
1. **Week 1 – Team lead:** read the college IP policy and hackathon terms; sign a founders' IP assignment. ₹0.
2. **Week 1 – Team lead:** run the free IP India trademark search for SPIROBUDDY in classes 10, 9, 44. ₹0.
3. **Weeks 1–3 – Team lead:** one consultation with a CDSCO regulatory consultant with three written questions: class; predicate; does a hospital-led observational study of an unlicensed add-on need MD-22? Cost n/f.
4. **Weeks 2–4 – Product owner:** freeze intended use, warnings, claims list; add "automated voice assistant" line to calls. ₹0.
5. **Weeks 2–6 – Team lead + CA:** register the entity; apply for DPIIT startup recognition (unlocks fee rebates; see agent 3's file).
6. **Weeks 4–8 – Entity:** file Form MD-12 for the test licence. **₹500 per device**; decision within 30 days.
7. **Weeks 4–10 – Hardware lead:** build 3–5 units with a pre-approved radio module and BIS-registered cell/adaptor; pre-compliance electrical test at a NABL lab (e.g. ask IIT Kanpur's facility for its charge sheet). Cost n/f.
8. **Weeks 4–12 – Clinical lead:** sign a memorandum with one hospital that has a DHR-registered EC; submit protocol, consent form, DPA. If it is a government hospital, an MD-22 would carry no fee.
9. **Weeks 6–12 – Team lead:** file the trademark (₹4,500 per class, snippet-sourced) and get one insurance broker quote.
10. **Week 12 – Quality owner:** shortlist two licensed Indian device makers for a loan-licence talk.

## Open questions (what you could not find, and who could answer it)
1. Does a hospital-led observational study of an **unlicensed** add-on need MD-22/MD-23, or is EC approval enough? → CDSCO Medical Devices Division or a regulatory consultant.
2. Class A-measuring or Class B, and is there an Indian **predicate**? → same.
3. Is the June 2026 draft (G.S.R. 515(E)) on Class B audit timelines final? What exactly did G.S.R. 743(E)/744(E) of Aug 2026 change? → Gazette of India; consultant.
4. Current UDI start date. → CDSCO.
5. Does an India-made product with an ETA-holding ESP32 module need its own WPC ETA, and the fee? → WPC Regional Licensing Office or a WPC agent. (DoT memo returned 403.)
6. Does an embedded BIS-registered cell in an unlisted product need anything more? → BIS-recognised lab.
7. Is our product type in E-Waste Rules Schedule I; any small-producer relief? → CPCB portal helpdesk.
8. Notified Body audit charges; 60601 test charges; consultant fees; insurance premiums. → quotes.
9. Primary text of the Telemedicine Practice Guidelines 2020 (still unread). → download by hand.
10. DPDP section 44 commencement notification (SPDI repeal date) and Board appointments after Aug 2026. → MeitY site; a privacy lawyer.
11. TRAI 2026 regulation Gazette date; whether a one-to-one AI call falls under the Feb 2026 synthetic-content labelling rules. → telecom lawyer.
12. Did Tidal file a patent in India; is SPIROBUDDY free as a trademark? → manual IP India searches; patent agent.
13. The team's college IP policy and the hackathon's IP terms. → the team.
14. Official IP India fee schedule and SIPP scheme status after 31 Mar 2026. → ipindia.gov.in.

## Sources opened this round
| # | URL | title | publisher | grade | used in |
|---|---|---|---|---|---|
| 1 | https://www.iitm.ac.in/sites/default/files/Others/medicaldevicesrules2017.pdf | Medical Devices Rules 2017, consolidated (211 pp; a different copy from ledger #183), rules 3, 7, 20, 31–32, 44, 46, 50–55, 63, First and Second Schedules | CDSCO/MoHFW text hosted by IIT Madras | A | B4-2 to B4-7, B4-9 |
| 2 | https://www.cdscomdonline.gov.in/NewMedDev/resources/app_srv/NMD/global/helpfiles/FeePaidDetails.pdf | Fee payable for licence, permission and registration certificate (Second Schedule table) | CDSCO online portal | A | B4-3, B4-4, B4-6 |
| 3 | https://www.cdsco.gov.in/opencms/export/sites/CDSCO_WEB/Pdf-documents/MDfAq24.pdf | Frequently Asked Questions on Medical Devices, Doc No. CDSCO/FAQ/MD/01/2024 | CDSCO | A | B4-1 to B4-5 |
| 4 | https://www.indialaw.in/blog/regulatory/medical-devices-amendment-rules-2026/ | Draft Medical Devices (Amendment) Rules 2026, G.S.R. 270(E), 10 Apr 2026 (test fees, sterilisation label) | IndiaLaw LLP | B | context: draft does not touch rule 20 |
| 5 | https://www.pureglobal.com/news/india-gsr-744e-eu-rule-63-class-a-qms-2026 | G.S.R. 744(E), 14 Aug 2026: EU added to rule 63; QMS self-certification for Class A non-measuring | Pure Global (consultancy) | C | context; Open question 3 |
| 6 | https://www.ibanet.org/article/15234243-b534-45f6-b303-4919cfe9a2dc | India's new telemedicine guidelines | International Bar Association | B | B4-15 |
| 7 | https://www.livelaw.in/articles/india-data-protection-board-established-law-543751 | India's Data Protection Board: Established in Law, Absent in Fact (1 Aug 2026) | LiveLaw | B | B4-13 |
| 8 | https://mpcb.gov.in/sites/default/files/inline-files/FAQs_for_BWMR_2022.pdf | FAQs under Battery Waste Management Rules 2022 | Maharashtra Pollution Control Board (CPCB FAQ) | A | B4-12 |
| 9 | https://www.espressif.com/sites/default/files/ETA-SD-20200704087%20ESP32-PICO-V3-ZERO%20WPC.pdf | WPC ETA through self-declaration, ETA-SD-20200704087, 23 Aug 2020 | DoT WPC Wing (hosted by Espressif) | A | B4-11 |
| 10 | https://assets.kpmg.com/content/dam/kpmg/in/pdf/2024/10/uniform-code-for-marketing-practices-in-medical-devices.pdf | Uniform Code for Marketing Practices in Medical Devices 2024 (summary, Oct 2024) | KPMG India | B | B4-20 |
| 11 | https://thc.nic.in/Central%20Governmental%20Acts/Drugs%20and%20Magic%20Remedies%20(Objectionable%20Advertisement)%20Act,%201954.pdf | Drugs and Magic Remedies (Objectionable Advertisements) Act 1954, full text | Tripura High Court (statute copy) | A | B4-20 |
| 12 | https://www.iitk.ac.in/emc/about-us | EMI/EMC and Electrical Safety facility, about us | IIT Kanpur | B | B4-9 |
| 13 | https://www.ibanet.org/article/B20060BD-6365-425E-A9D9-6FFDFC477F62 | The changing face of product liability regime in India and its impact on the med-tech sector (c. 2020) | IBA / Nishith Desai Associates | B | B4-18 |
| 14 | https://www.bis.gov.in/product-certification/products-under-compulsory-certification/scheme-ii-registration-scheme | Products under Compulsory Registration (Scheme II) | Bureau of Indian Standards | A | B4-10 |
| 15 | https://www.slc.du.ac.in/uploads/research/innovation-council/2019-20/National_Innovation_and_Start-up_Policy.pdf | NISP 2019 session note | Delhi University college | – | nothing useful (no clause text) |
| 16 | https://www.jsalaw.com/wp-content/uploads/2025/11/JSA-Prism-InfoTech-November-2025-DPDP-Rules.Final_.pdf | JSA Prism: DPDP Rules (Nov 2025) | JSA (law firm) | – | nothing useful (HTTP 403) |
| 17 | https://tnpcb.gov.in/pdf_2024/EPREWaste6225.pdf | EPR e-waste note | Tamil Nadu Pollution Control Board | – | nothing useful (error page) |
| 18 | https://dot.gov.in/sites/default/files/Regarding%20ETA%20for%20Wireless%20equipment_0.pdf | DoT memo on ETA for wireless equipment | Department of Telecommunications | – | nothing useful (HTTP 403) |
| 19 | https://www.squirepattonboggs.com/-/media/files/insights/publications/2020/11/product-liability-under-the-consumer-protection-act-2019/product-liability-under-the-consumer-protection-act-2019.pdf | Product liability under the CPA 2019 | Squire Patton Boggs | – | nothing useful (empty download) |
| 20 | https://www.indiacode.nic.in/indiacode/bitstream/123456789/1412/1/A1954-21.pdf | Drugs and Magic Remedies Act (India Code copy) | India Code | – | nothing useful (download failed; read via #11) |
| 21 | Search snippets only, NOT opened: DHR/NAITIK and ICMR Bioethics pages (EC registration); law-firm and press notes on DPDP phases, SPDI repeal, DISHA; TRAI Third Amendment press coverage; IT Rules G.S.R. 120(E) Feb 2026 notes; ASCI AI-labelling guidelines 29 Sep 2026; Freyr WPC guide; Nemko/Corpseed BIS notes; e-waste and Legal Metrology 2025 summaries; IP fee tables (Intepat, SS Rana); NISP college pages; insurance broker pages; G.S.R. 515(E) draft summaries; UDI deferral reports | various | various | C | B4-3, B4-5, B4-7, B4-10 to B4-14, B4-17 to B4-21 |
