# 11 – Home recovery companion: should SpiroBuddy grow into a full "recovery kit"?

**Written:** Sun 11 Oct 2026 by the research agent, for the post-hackathon roadmap and the "future roadmap" part of the pitch video. **Nothing in this file is built.** Every new feature here is **Planned** unless it says otherwise.

**How to read this file**
- `[R n]` = a source opened for this file (numbered list at the end; all added to `docs/research/SOURCES_LEDGER.md` as rows 340 onward). `[#n]` = an older ledger row, not re-opened unless stated.
- `file:line` = an existing repo file this builds on. Read those for detail; it is not repeated here.
- **(snippet)** = seen only in a search result, page not opened, grade C. **(est.)** = our own estimate, with its basis given.
- Confidence tags: **CONFIRMED** (primary source or two independent sources) · **SINGLE SOURCE** · **ESTIMATE** · **NOT FOUND**.
- Price anchor: the founder meant **₹2,000** (rupees) as a starting assumption, not a fixed price. The ₹1.5 lakh band is covered in one line only (section 3.4).
- This is not legal or medical advice. Where a rule is involved, "our reading" is marked; confirm with a regulatory consultant or lawyer.

---

## Answer in 12 lines

1. **The need is real.** About half of older Indians take 5 or more medicines [R19]. Families already pay ₹1,000–3,500 a day for a home nurse [R2]. Hospitals under Ayushman Bharat must give free medicines and follow-up for 15 days after surgery, and pay for any readmission themselves [R20].
2. **Apollo already sells this idea** as a 2-week "Home Discharge" package after heart surgery, including help with medicines [R15]. So the idea is proven to sell. It is not new.
3. **The government now gives away the "records + booking + reminders" part free.** Aarogya Setu 2.0 (launched 29 Jun 2026) does health records, OCR of reports, appointment booking, reminders and wearable sync [R6].
4. **So do not compete on records or reminders.** Plug into ABDM (India's national health-records network) and keep our edge: proof the exercise was done, a nurse who sees who is slipping, and the family in the loop.
5. **Reading a prescription photo is not safe on its own.** The best Indian study got about 82% right on simulated handwriting; GPT-4o and Gemini scored under 8% before training [R1]. The authors say it must not be deployed.
6. **Safe design:** the AI only drafts the medicine schedule. A nurse or pharmacist confirms every line before any reminder goes out. The app never changes a dose and never advises.
7. **Regulation:** our reading of CDSCO's 2026 software guidance is that storing records, scheduling and plain messages are *not* medical-device software [R16]. Anything that interprets or recommends is. Keep the medicine module "relay what the doctor wrote" only.
8. **₹2,000 covers a 30-day core kit at scale, but not everything.** Core kit cost at scale is about ₹870 (est.); it fails if we also supply the spirometer, a hub phone, and extra devices. Options in section 3.4.
9. **Elderly users:** voice calls and the family on WhatsApp beat app notifications. Only 41% of older Indians own a smartphone (F-INDIA-5). Self-reported "I took it" taps overstate adherence: 99DOTS was only 69% accurate against urine tests [R17].
10. **Easy hardware:** pre-paired kits, QR onboarding and a lent "hub" phone are the realistic path. A SIM inside our own unit needs a company to register as an M2M provider, which took one firm about 6 months [R10].
11. **Three-ball spirometers:** readable in principle (light sensors or the phone camera), but a ball only says "flow reached a level", not volume. Good enough to count sessions, not to measure lungs.
12. **Biggest risk is scope creep.** Lead with the spirometer insight; show the recovery kit as the roadmap, not the product.

---

## A. Demand and price: will families or hospitals pay?

### A-1: Medicines after discharge are a real problem, but Indian post-surgery data are thin
- **Older Indians take many medicines.** A 2021 meta-analysis of 27 Indian studies: polypharmacy (5–9 medicines) 49%, 10 or more medicines 31%, potentially inappropriate medicines 28% [R19]. A 2024 six-city study found 33.7% on five or more daily (snippet).
- **Post-surgery adherence in India: no good figure found.** A 2023–24 AIIMS Deoghar study (111 patients, mostly bypass) reported 82% "high adherence" by self-report (snippet). A 2017 *Indian Heart Journal* paper on 265 bypass patients found 26% non-adherent, but its authors appear to be from Pakistan (snippet; check before citing). An Indian heart-attack registry (716 patients, 2025) found only 42.7% with good adherence (snippet).
- **Why people come back to hospital after heart surgery:** a 53-study meta-analysis found 12.9% readmitted within 30 days, mostly for infection, irregular heartbeat, heart failure, lung complications and fluid around the lung [R4]. Medicines were not named as a cause. So "missed medicines cause readmissions" is **not** a claim we can make.
- **Verdict:** the medicine burden is well documented; the post-surgery adherence gap in India is not. **CONFIRMED** (polypharmacy, readmission causes) / **NOT FOUND** (Indian post-surgery adherence figure).

### A-2: What Indian families pay today for help after discharge
| Service | Price seen | Source |
|---|---|---|
| Home nurse, per day | ₹1,000–3,500 (Chennai, Jun 2026) | [R2], vendor blog, C |
| 12-hour nurse shift, per month | ₹22,000–40,000 (Delhi, Chennai) | snippet of Samarth blog (page refused, 403), C |
| Physiotherapy, per session | ₹500–1,500 | [R2], C |
| Residential recovery facility, per month | ₹40,000–1,20,000 | [R2], C |
| Medicines, per month in early recovery | ₹5,000–15,000 | [R2], C |
| Dozee contactless monitor rental | ₹3,999 for 30 days, ₹2,999 for 15 days (undated) | snippet of BioSpectrum, C |
| Portea ICU-at-home (2018 claim) | ₹6,500–12,000 a day | snippet of MediaNama, C |
| Bluetooth pulse oximeter (bought) | ₹3,124 (BPL iOxy) | [R22], C |
| Bluetooth BP monitor (bought) | about ₹2,200–2,500 (Omron, price trackers) | snippet, C; ₹1,850–2,330 for Omron in `03_COSTS_AND_BUDGET.md:237` |
| Average out-of-pocket per hospital stay (NSS 2025) | ₹34,064 overall; ₹50,508 private; ₹6,631 public | [R23], B |

- **Verdict:** a ₹2,000 kit is about the price of **one day of a home nurse** or **one Bluetooth BP monitor**, and about 4–6% of an average private hospital bill. That makes ₹2,000 *credible* for families who pay privately. **ESTIMATE** (comparison is ours; prices are mostly grade C).

### A-3: Is anyone already selling a "recovery package"? Yes – the closest analogue is Apollo
- **Apollo Hospitals, Hyderabad, Oct 2023:** "Home Discharges" for every cardiac surgery patient. A 2-week programme with doctors, nurses, physiotherapists and a care coordinator, tied to the surgeon's discharge advice. It lists "assistance with medication adherence", wound care, parameter monitoring and 24-hour coordinator support. Apollo said 300–500 patients had used it and that it would become standard care [R15]. A trade article later reported over 900 enrolments and 3 readmissions per 100 (snippet, unverified, no comparison group). **Price not published.**
- **Manipal + ConnectedLife (2022):** wearables after high-risk surgery with medicine and physio reminders (ledger #130, not re-opened).
- **Verdict:** a hospital-run home recovery package with medicine support **already exists and is sold** in India. Our kit would be a cheaper, tech-led version that a hospital without Apollo's home-care arm could offer. **SINGLE SOURCE** (Apollo press coverage).

### A-4: Who pays?
| Payer | Why they might | Evidence |
|---|---|---|
| **Hospital, inside the surgery package** | Under PM-JAY (Ayushman Bharat), the surgical package covers 15 days after discharge: consultation, medicines, diagnostics. The hospital must hand over the medicines and do follow-up free; readmission for complications is paid from the original package [R20]. So a slow or failed recovery costs the hospital, not the patient | [R20], A (state health agency FAQ applying national rules) |
| **Family, out of pocket** | They already pay for nurses and devices (A-2) | A-2 |
| **Insurer** | IRDAI has allowed "home treatment" as an add-on since 2021, but it needs a doctor's daily-monitored line of treatment; Covid-era home claims were often refused (snippets) | snippets, C; `05_EXPANSION_AND_CUSTOMERS.md` E-14 row "Insurers" |
| **Willingness to pay for remote monitoring, general** | A 2022 review of 11 studies in 7 countries: 19–70% willing to pay; older people less willing (snippet; page refused). A US survey: under half would pay more than US$5 a month (snippet) | C |
- **Verdict:** the hospital is the strongest payer for the first 15 days (PM-JAY makes it their cost). The family is the payer for "premium" extras. Insurers: not yet. **CONFIRMED** (PM-JAY rule) / **ESTIMATE** (who will actually pay us).

**Section A verdict:** Demand is real and a market already pays for home recovery, mostly through nurses. ₹2,000 is a believable family price. No Indian study shows that a reminder kit reduces readmissions after surgery. **ESTIMATE.**

---

## B. Prescription photo → reminders

### B-1: How good is AI at reading Indian prescriptions?
- **MIRAGE (Oct 2024, preprint):** 1,133 Indian doctors wrote simulated prescriptions; 513,407 used for training, 15,000 for testing. A fine-tuned open model got about **82%** of medicine name + dose pairs right. Without training, **GPT-4o scored 7.6, Gemini 1.5 Pro 5.5, LLaVA 2.0 (F1, out of 100)**. Rare medicines were read worse. The authors say the accuracy is "in no way deployable" [R1].
- **Printed vs handwritten:** a Vietnamese app (Google Vision + GPT-3.5) got 90.2% of fields right on printed prescriptions and **25.7% on handwritten** ones, on only 11 handwritten samples (snippet).
- **Indian prescriptions are hard even for people:** a Delhi children's clinic study found abbreviations in 53.6% of 343 prescriptions; 80.8% of 105 Kerala pharmacists said poor handwriting or unclear symbols cause problems (snippets). Frequency codes like OD (once a day), BD (twice), TDS (three times), HS (at bedtime) and SOS (only if needed) are common; no study measuring errors on these specific codes was found.
- **Brand names:** India uses many brand names for one generic. A national medicine code list was named as a gap by a 2026 FHIR study (medication terminology) [R21]. Samsung licenses Tata 1mg's drug data for this reason [R18].
- **Verdict:** printed, computer-generated discharge prescriptions are probably readable with checks; handwritten ones are not safe to automate. **SINGLE SOURCE** (MIRAGE) + snippets.

### B-2: Who already does this?
| Product | Records | Reads prescription photo | Medicine reminders | Notes |
|---|---|---|---|---|
| **Aarogya Setu 2.0** (Govt, Jun 2026) | Yes (ABDM PHR) | "Smart Reports" with OCR of documents | "Personalised reminders" | Also UHI appointment booking, insurance wallet, wearable sync, free [R6] |
| **Eka Care** | Yes, ABDM-approved | "Medical Records Analyser" makes a dashboard from records | Clinic-side WhatsApp reminders | Claims 20 million+ ABHA created, 140 million+ records [R5] |
| **Samsung Health (India)** | Yes, with Eka Care (snippet) | No (type the name) | Yes: gentle to strong alerts, refill alerts, interaction info from Tata 1mg data (Oct 2024) [R18] | Samsung phones only |
| **Tata 1mg, PharmEasy, Apollo 24/7** | Some | Upload prescription to *order medicine* | Not confirmed | Not checked this round |
| **Medisafe, MyTherapy** | No | No photo reading found | Yes | Global apps |
| **DRiefcase** | Yes; first ABDM-approved PHR app (Jan 2022, snippet) | Not checked | Not checked | – |
- **Do reminder apps work?** The largest trial (MedISAFE-BP, 411 adults, 12 weeks) found a small rise in self-reported adherence and **no blood-pressure benefit** [R3]. The authors suggest linking the app to clinical care, which is what a nurse dashboard does.
- **Verdict:** reminders and records are a crowded, free commodity. Reading a photo is offered by few, and nobody we found pairs it with a human check. **CONFIRMED** (crowded) / **SINGLE SOURCE** (each product's features).

### B-3: The safe design (summary; full box in section 4)
1. Patient or family photographs the **printed discharge summary** (handwritten slips: the nurse types them in).
2. The AI drafts a table: medicine, strength, how often, how long, with the photo crop beside each line.
3. A named nurse or pharmacist confirms or corrects each line. **No reminder goes out before this.**
4. Reminders say only what the doctor wrote ("Time for Tab. X, 1 tablet, as your doctor wrote"). No advice, no dose change, no "you can skip".
5. Missed doses: tell the family and nurse; never tell the patient to "double up".
6. Any change to the prescription comes only from the doctor, re-confirmed by the nurse.

### B-4: Is a medicine-reminder app a medical device in India?
- **CDSCO's 2026 software guidance, re-read for this question** [R16] (ledger #135): software that only does "transfer, storage, archive data, convert, format, communication, simple search" is **not** medical-device software. Hospital information systems for "scheduling patient appointments/visits" and storing patient information are not either. **But** if such a system adds "real-time patient monitoring" or "quantification of physiological parameters for clinical decision-making", it "may be considered as a medical device". Wellness software must make no reference to diseases.
- **Our reading:** a reminder that relays a human-confirmed schedule, plus records and booking, sits in the "not a device" list. AI that *interprets* a prescription and generates the schedule with no human check moves towards a device function. Our base unit is already a measuring device (`docs/research/business/04_legal_and_regulatory.md:30`, B4-1), and software that drives it takes its class (`04_legal_and_regulatory.md:36`, B4-2). **Keep the medicine module a separate software function** from the spirometer software, so its status is decided on its own.
- **Telemedicine Practice Guidelines 2020:** AI may assist a doctor but may not counsel or prescribe (`docs/plan/06_LEGAL_DEEP_DIVE.md:150`, L-8). So the app must never answer "can I stop this tablet?". The same guidance makes the doctor responsible for any prescription sent through a platform.
- **E-pharmacy:** selling medicines is out of scope; no rule was checked this round. Do not add ordering.
- **Verdict:** our reading is that a human-confirmed reminder and records module is **not** a medical device, but an automated "photo → schedule" feature may be. Ask CDSCO through MedTech Mitra (`docs/research/business/05_icmr_ethics_abdm_evidence.md:115`, B5-11). **SINGLE SOURCE** (primary guidance; application is our reading).

**Section B verdict:** build "photo → AI draft → human confirms → reminders", printed prescriptions only at first, with no advice. Do not market "AI reads your prescription". **SINGLE SOURCE / ESTIMATE.**

---

## C. Hospital link and records (ABDM)

### C-1: ABDM in 2026 is big and already does what the founder described
- **Scale (PIB backgrounder, 6 Jul 2026):** over **104 crore health records** linked to over **93 crore ABHA accounts** [R6]. A news report of a Lok Sabha reply gives 95.99 crore ABHA by 31 Jul 2026 (snippet). **Scan & Share** (scan a QR at the hospital desk to register) issued over **23.21 crore** tokens by 18 Jun 2026; an IIHMR study found waiting time fell from about an hour to 2–5 minutes [R6].
- **UHI** (Unified Health Interface, the open booking network) has five live services, including doctor consultation [R6]. So "book a follow-up through the app" can use UHI rather than a custom link per hospital.
- **Incentives paid (DHIS) to 18 Jun 2026:** hospitals ₹107+ crore, labs and pharmacies ₹2.95 crore, digital solution companies ₹26+ crore [R6]. Do not put these in our business case (`05_icmr_ethics_abdm_evidence.md:157`, B5-18).
- **Aarogya Setu 2.0** is now the government's own PHR app with OCR, reminders, UHI booking and wearable sync [R6]. This is the biggest surprise of this round.
- **Verdict:** **CONFIRMED** (primary PIB document).

### C-2: What it takes for SpiroBuddy to join ABDM
- Already researched: milestones M1 (ABHA), M2 (share records as a provider, "HIP"), M3 (read records, "HIU"); vendor-reported 4–9 months; security audit ("Safe-to-Host", WASA) before production keys (`05_icmr_ethics_abdm_evidence.md:151`, B5-17; `docs/FUTURE_ARCHITECTURE.md:165`, §3.8).
- **New this round:** the ABDM developer forum says PHR (patient-app) integration has its own sandbox section ("Building PHR App"), separate from M1–M3 for web systems; every PHR app works with one consent manager (snippets; abdm.gov.in and the forum refused connections). India's FHIR profiles have no lung-function profile (`FUTURE_ARCHITECTURE.md:165`).
- **Cheapest path (our reading):** do **not** build our own PHR app. (1) Send our episode summary into the hospital's already-certified system, or become a small HIP for "SpiroBuddy episode reports" only. (2) Let patients view records in Aarogya Setu or Eka Care. (3) Use UHI for booking later.
- **Verdict:** **SINGLE SOURCE** (vendor and forum snippets for steps and time).

### C-3: Hospital systems (HIS) in practice
- A 2025 mixed-methods study (eGov Foundation with WHO SEARO; 22 survey replies, 10 interviews; preprint) found FHIR use in India is "uneven and largely compliance-driven"; people confuse ABDM compliance with FHIR conformance; medicine terminology and validation tools are weak [R21]. No HIS market-share figure was found.
- **Verdict:** expect CSV/PDF exports and ABDM links, not live FHIR APIs, in most private hospitals. **SINGLE SOURCE** (preprint).

### C-4: Storing health data – the law
- Already covered: DPDP Act main duties start **13 May 2027**; until then the IT Act "SPDI" rules apply; breach reports in 72 hours (Board) and 6 hours (CERT-In); transfers abroad allowed unless a country is blacklisted (`06_LEGAL_DEEP_DIVE.md:117`, L-7; `FUTURE_ARCHITECTURE.md:143`, §3.5 India data residency; `:154`, §3.7 consent records).
- **New for the recovery kit:** prescriptions and discharge summaries are richer health data than breath counts. Three changes: (1) store images in India (Mumbai) and delete the photo once the nurse confirms the schedule, unless the patient asks to keep it; (2) a separate consent purpose for "records storage" and for "family sees my medicines"; (3) if we sell direct to families, **we** become the data fiduciary, not the hospital (`06_LEGAL_DEEP_DIVE.md:117`, "Who is who").
- **Verdict:** **CONFIRMED** (from existing files).

**Section C verdict:** do not build a records app. Link to ABDM, let the government and Eka-type apps hold records, and keep our data narrow. **CONFIRMED / ESTIMATE.**

---

## D. Elderly-friendly design: what makes older Indian patients actually use reminders

- **Phones:** only 41% of older Indians own a smartphone; 13% use the internet (HelpAge 2025, `docs/research/KNOWLEDGE_BASE.md:166`, F-INDIA-5). 29% of over-60s find it hard to make a call (LASI, `KNOWLEDGE_BASE.md:1048`, F-INDLOC-7). Most live with their children and most older women cannot read (`KNOWLEDGE_BASE.md:536`, F-INDLOC-3).
- **Voice calls reach people only with retries:** Kilkari: 50% answer the first call, 76% by the third (`KNOWLEDGE_BASE.md:1042`, F-INDLOC-6). No peer-reviewed Indian study of IVR for older adults was found (`KNOWLEDGE_BASE.md:1000`, F-INDLOC-5). This round's search again found Indian SMS and WhatsApp trials for blood pressure and diabetes, but no IVR result for the elderly (snippets).
- **"I took it" is not proof:** in India's TB programme, patient phone-call reports of doses were only **69% accurate** against surprise urine tests (sensitivity 70%, specificity 61%; 597 patients). About 4 in 10 non-adherent patients were missed [R17]. So a "press 1 if you took it" log overstates adherence. Label it "reported", never "taken".
- **Reminder apps alone give small effects** (MedISAFE-BP, [R3]). Linking to a nurse is what the authors recommend.
- **What to build (our design, from the evidence above and `docs/FEATURE_PLAN.md:138`, Part D):**
  1. Default channel for the patient: a **voice call** in their language at dose time, pre-recorded clip, "Press 1 if done". No app needed.
  2. Default channel for the family: WhatsApp utility message (₹0.115 each, `KNOWLEDGE_BASE.md:61`, F-COMMS-2) with "missed" alerts only, not every dose.
  3. The family member can act as **proxy** (confirms doses for the patient), but only with the patient's own consent (`06_LEGAL_DEEP_DIVE.md:337`, L-20).
  4. One medicine per call; never read out more than 3 at once.
  5. Morning calls first (best pickup in Kilkari, `KNOWLEDGE_BASE.md:1109`, F-INDLOC-9); retry up to 3 times, then tell the family.
- **Verdict:** voice for the patient, WhatsApp for the family, and a nurse who sees the misses. **CONFIRMED** (phone ownership, call pickup, self-report inaccuracy) / **NOT FOUND** (Indian IVR trial in older adults).

---

## E. Easy-connect hardware and a "universal" spirometer reader

### E-1: Pairing with no fiddly steps
- Already designed: QR sticker → Android "companion device" box → press the unit's button → bonded; a visible "Pair again" path (`docs/plan/02_MOBILE_APP_AND_BLUETOOTH.md:99`, M-5; `:108`, M-6). The unit itself beeps reminders, so a phone that kills background apps does not break care (`02_MOBILE_APP_AND_BLUETOOTH.md:403`, M-33).
- **Best practice abroad:** Current Health (US/UK) ships kits "pre-configured" with a tablet that has its own cellular radio, so patients without home internet can use it [R13]. The company was sold back to its founder by Best Buy in June 2025 after Best Buy Health losses (snippets; pages refused). Lesson: kits work, but the hardware-heavy model is expensive.
- **Our rule for the kit (est.):** the nurse pairs everything **before discharge** on the ward (about 5 minutes, `docs/research/business/06_sell_vs_share.md:237`). The patient never sees a pairing screen.
- **Verdict:** **CONFIRMED** (Android method, from 02) / **SINGLE SOURCE** (Current Health).

### E-2: A home hub that talks to other devices
- **Standard Bluetooth health profiles exist** and are adopted by the Bluetooth SIG: Blood Pressure, Glucose, Weight Scale, Pulse Oximeter, Health Thermometer, Continuous Glucose Monitoring [R12]. A hub that speaks these can read many brands without custom code. **Caveat (eng.):** many cheap Indian devices use their own app protocol instead; check each model before promising support.
- **Three hub options:**
  | Option | Cost (est.) | Pros | Cons |
  |---|---|---|---|
  | Patient's or family's own Android phone | ₹0 | No extra device | Only ~41% of elders own one; family phone may leave the house |
  | **Lent hub phone + data SIM** | ₹5,400–6,000 per phone (`03_COSTS_AND_BUDGET.md:77`, C) + about ₹300 a month SIM (est., consumer plan) | Works now, no telecom licence | Phone can be lost; needs charging |
  | **Cellular module inside our own base** | LTE Cat-1 module ₹980 ex-GST; NB-IoT module ₹525 ex-GST (Evelta, Mumbai stock) [R11]; M2M data "as low as ₹30 a month" [R10] | Always connected, no phone at all | Company must register as an M2M service provider (SARAL portal, operator onboarding): took one firm **about 6 months** [R10]; DoT/TEC rules (`06_LEGAL_DEEP_DIVE.md:78`, L-3); more power, bigger battery |
- **Verdict:** pilot and year 1: lent hub phone. Cellular base: only after a company exists and M2M registration is done. **SINGLE SOURCE** (module prices, M2M process) / **ESTIMATE** (totals).

### E-3: One reader for both spirometer types?
- **The problem (already known):** the laser reads only the volume (piston) type; Indian wards probably stock the cheap three-ball type (`docs/private/10_FINAL_VERDICT.md:66`; `05_EXPANSION_AND_CUSTOMERS.md:429`, E-12; `01_HARDWARE_REVIEW.md:428`, H-7).
- **What a three-ball reading gives clinically:** each ball rises at a set inspiratory **flow**. The Teleflex Triflo II spans about 600–1,200 cc per second, with a stated accuracy of ±400 cc/s (snippets; manual not opened, ledger #339). How long the balls stay up × the flow level gives a **rough** volume (our arithmetic: 900 cc/s for 3 s ≈ 2.7 L), but with ±400 cc/s error this is **not** a lung measurement.
- **Is it enough for adherence?** Yes, for counting: "a session happened, N breaths, balls reached level 1/2/3, held for about T seconds". That is the metric the pilot needs ("share of due sessions completed", `05_icmr_ethics_abdm_evidence.md:175`). It is weaker for technique.
- **Ways to read it (none built):**
  | Method | Evidence | Fit for elderly | Verdict |
  |---|---|---|---|
  | Light sensors (one per tube) on a clip-on side bracket | Michigan ISTracker reads a flow "bobbin" at 100% (`07_competitors_and_alternatives.md:70`, B7-3); an abandoned US patent used light gates on three tubes (B7-7) | Good: nothing to aim | **Best hardware path** |
  | Phone camera on a stand | One simulated tablet study for volume type; nothing for three-ball (`07_competitors_and_alternatives.md:120`, B7-11) | Poor: needs a steady phone and light | A two-week student experiment |
  | Microphone | Lab only (B7-10) | Good | Watch only |
  | Manual tap or "press 1 after your session" call | No sensing; self-report is inaccurate ([R17]) | Best | Fallback only; label "reported" |
- This matches the verdict's "breath from any source" layer (`10_FINAL_VERDICT.md:69`): accept a breath from our base, a light-gate bracket, the camera or a tap, each tagged with how it was measured.
- **Verdict:** a three-ball light-gate bracket is feasible and is the most valuable hardware extension. **CONFIRMED** (feasibility, two sources) / **NOT FOUND** (anyone shipping one).

---

## F. Competitors and analogues for a "complete recovery companion"

| Player | What it does | Where | Threat / partner |
|---|---|---|---|
| **Aarogya Setu 2.0** | Free PHR, OCR reports, reminders, UHI booking, wearables [R6] | India, government | Takes the records/reminders space. Partner via ABDM |
| **Apollo Home Discharges** | 2-week nurse-led recovery after heart surgery, incl. medicine support [R15] | Hyderabad | Proves demand; competitor in Apollo hospitals; model to copy elsewhere |
| **Eka Care** | ABDM PHR, records analyser, clinic WhatsApp reminders [R5] | India | Records partner |
| **Samsung Health** | Medicine reminders with Tata 1mg data [R18] | India, Samsung phones | Free reminders for some users |
| **Lupin LYFE** | CDSCO-licensed remote cardiac rehab software (`07_competitors_and_alternatives.md:145`, B7-15) | India | Partner: our base as a data source |
| **Manipal + ConnectedLife** | Wearables + reminders after surgery (ledger #130) | India | Shows hospitals buy it |
| **Dozee** | Contactless bed monitor; home rental (snippet) | India | Different sensor; possible partner |
| **Medisafe, MyTherapy** | Reminder apps; small effects in trials [R3] | Global | Commodity |
| **Biofourmis + CopilotIQ** | Merged Oct 2024 into an "AI-driven in-home care" platform incl. post-acute care [R14] | US | Shows consolidation |
| **Current Health** | Pre-configured cellular kits; sold back to founder 2025 (snippets) | US/UK | Shows hardware-heavy kits are hard to make pay |
| **Hello Heart** | Employer-paid heart app with BP cuff; last big round $70M in 2022 (snippet) | US | Different payer (employer) |

- **What stays hard to copy for SpiroBuddy:** (1) an **objective** count of the breathing exercise surgeons already prescribe, which no reminder app has; (2) working with the cheap spirometer the ward already has (once the three-ball bracket exists); (3) voice-first coaching in Indian languages with the family loop; (4) the nurse view of "who is slipping". Records and medicine reminders are **not** hard to copy.
- **Verdict:** the "complete companion" space is crowded and partly free. Our moat is the exercise measurement plus the nurse loop. **CONFIRMED** (crowding) / **ESTIMATE** (moat).

---

## G. Risks

| Risk | How bad | What to do |
|---|---|---|
| **Scope creep** dilutes the sharp spirometer insight; the verdict's strength is "one sharp insight" (`10_FINAL_VERDICT.md:13`) | High | Pitch the spirometer now, the recovery kit as roadmap. Build medicines only after the spirometer pilot gives its one number |
| **Liability for a missed or wrong reminder** | High | Human confirms every line; contract says the hospital owns clinical decisions and we own software defects (`06_LEGAL_DEEP_DIVE.md:294`, L-17); ICMR's AI guideline says responsibility must be allocated *before* deployment [R7 §1.5]; Consumer Protection Act covers wrong instructions (`04_legal_and_regulatory.md:179`, B4-18) |
| **Regulatory class jump** (AI that reads prescriptions or advises = device software) | Medium–High | Keep medicines as a separate, non-interpreting module; ask CDSCO in writing [R16] |
| **Data breach** of prescriptions and discharge summaries | High | India storage, delete photos after confirmation, role-based access, 72-hour/6-hour breach plan (`FUTURE_ARCHITECTURE.md:154`) |
| **"Adherence" overstated** by self-reports | Medium | Label "reported" vs "measured"; [R17] |
| **Free government app** makes paid records worthless | High for records | Don't sell records; sell measurement + nurse time |
| **Hardware cost** of a multi-device kit kills the ₹2,000 price | High | Lend and recover devices; software-only tier (3.4) |
- **Verdict:** manageable if medicines stay "relay + human check" and the kit stays on the roadmap. **ESTIMATE.**

---

## H. ICMR and research-ethics compliance for the new features

**What already exists (don't repeat):** ICMR is not a regulator and has not seen SpiroBuddy (`05_icmr_ethics_abdm_evidence.md:6`). ICMR 2017 risk levels and review routes (`:42`, B5-3), consent mapping incl. impartial witness and e-consent (`:48`, B5-4), vulnerable groups (`:64`, B5-5), compensation, with the institution as sponsor in student research (`:70`, B5-6), EC registration (`:76`, B5-7), CTRI (`:82`, B5-8), the AI guideline from secondary sources (`:88`, B5-9), the CDSCO MD-22 question (`:109`, B5-10; answered as "plan for permission" in `06_LEGAL_DEEP_DIVE.md:22`, L-1), the evidence plan (`05_icmr…:175`), and consent and capacity (`06_LEGAL_DEEP_DIVE.md:337`, L-20).

**New this round:** the **ICMR 2023 AI guideline PDF was read in full** (it failed in the earlier round) [R7]; ICMR 2017 was re-opened for **section 11 (datasets) and sections 5.5/5.7** [R8]; CDSCO's NDCT Rules FAQ was read for the drug-trial overlap [R9].

### H-1: Rule by rule, for the new features
| # | Rule (source) | What it requires | Feature it hits | Do / Don't |
|---|---|---|---|---|
| 1 | **ICMR AI 2023, §1.1 Autonomy** [R7] | Humans keep "complete control"; patients must be told about AI and can refuse it without coercion; where AI and clinician differ, the patient is given both options | Coaching AI, prescription reader, AI summaries | **Do:** offer a "nurse only, no AI" option with the same care. **Don't:** make AI use a condition of getting the kit |
| 2 | **ICMR AI 2023, §1.5 Accountability** [R7] | AI for health "should always be appropriately supervised" (Human In The Loop); legal responsibility defined before use; regular internal and external audits, with reports **made publicly available** | Prescription reader, coaching, dashboard alerts | **Do:** a named nurse/pharmacist signs off each parsed prescription; publish a short audit summary yearly. **Don't:** let any parsed schedule go live unreviewed |
| 3 | **ICMR AI 2023, §1.4 Data privacy (vii, viii)** [R7] | Extra consent for sharing data if not taken before; repurposing "data surplus" without consent is unethical | Records storage, family WhatsApp, model training | **Do:** separate consent ticks for care, family sharing, records storage and AI training. **Don't:** keep prescription photos "in case they are useful later" |
| 4 | **ICMR AI 2023, §4.2 (vi)** [R7] | "IEC approval is required for the use of retrospective data for developing and validating the AI technology" | Training/testing the prescription reader on real prescriptions | **Don't:** collect real prescriptions to train or test the model without ethics approval. **Do:** test on synthetic or published datasets (e.g. MIRAGE's public 100-record subset [R1]) until then |
| 5 | **ICMR AI 2023, §1.10 Validity, §2.2** [R7] | "Rigorous clinical and field validation before application on patients"; prospective validation preferred | Prescription reader, breath model | **Don't:** call either "validated". **Do:** measure the reader's error rate against the nurse's corrections in the pilot |
| 6 | **ICMR AI 2023, Table 2 checklist (17 items)** [R7] | An EC will ask for: objectives, technology, funding/conflicts, team credentials, participants, recruitment, risks, treatment of research injury, benefits, evidence, validation, accountability (named persons), monitoring, data handling, consent type, right to be forgotten, human moderation | Any study of the kit | **Do:** write a 2-page answer to all 17 before approaching an EC (extends the 10-item list in `05_icmr…:175`) |
| 7 | **ICMR AI 2023, §4.2 (ii)–(iii)** [R7] | Check understanding by "teach-back"; explain which parts are human and which are technology | Consent for the kit | **Do:** end the consent call with "tell me in your words what the app does and what the nurse does" |
| 8 | **ICMR 2017 §11.7.1–11.7.2 Datasets** [R8] | Repositories built for care but later used for research or **commercialisation** need EC review; data mining needs EC approval; ensure privacy, accuracy, security and liability when data is outsourced or sold | Records store, nurse dashboard data, any analytics | **Don't:** analyse or publish dashboard data, or sell/share it, without EC approval. **Do:** treat routine care data and research data as two separate purposes |
| 9 | **ICMR 2017 §11.7.4, Box 11.6** [R8] | For cloud and networked databases: physical security, passwords, role-based access, encryption in transit | Records, WhatsApp integrations | **Do:** role-based access (nurse sees her ward only), encryption, access logs |
| 10 | **ICMR 2017 §5.5 e-consent** [R8] | E-consent allowed (text, audio, video, interactive) but process, signatures and privacy must be EC-approved first; don't use electronic methods if the participant is uncomfortable with them | Voice consent in the app | **Do:** keep a paper/thumb-print path with an impartial witness (B5-4) |
| 11 | **ICMR 2017 §5.7 waiver** [R8] | Waiver of consent only for less than minimal risk and with EC approval | Retrospective chart review of readmissions | **Don't:** assume a waiver; ask the EC |
| 12 | **NDCT Rules 2019 (CDSCO FAQ Q9–12)** [R9] | A "clinical trial" is a study of a **new or investigational drug**. An "academic clinical trial" of an approved drug at a new dose/route/indication needs no CDSCO permission if the EC approves, results aren't used for approval or promotion; ICMR guidelines incl. compensation still apply | Medication reminders | **Our reading:** reminders for medicines already prescribed at the prescribed dose are **not** a drug trial. **Don't:** ever change, test or compare doses or drugs. That would pull the study under NDCT |
| 13 | **MDR 2017 clinical investigation (MD-22)** | Already analysed: plan for CDSCO permission for the base unit (`06_LEGAL_DEEP_DIVE.md:22`, L-1) | Spirometer pilot; any hub or three-ball bracket | **Do:** ask MedTech Mitra; a new bracket is a new device design |
| 14 | **Telemedicine guidelines 2020** | AI may not counsel or prescribe (`06_LEGAL_DEEP_DIVE.md:150`, L-8). An Indian ethics journal says the guidelines only partly cover ethics [R24] | Nurse calls, AI calls | **Do:** fixed red-flag text; doctor consults follow the guidelines |
| 15 | **ICMR guidance on mHealth / remote monitoring / telemedicine research** | **Not found.** A search found no ICMR document specific to mHealth apps or remote monitoring; the AI guideline and ICMR 2017 are what an EC will apply (snippets) | All | NOT FOUND – ask the EC secretary |

### H-2: ICMR compliance checklist before any pilot (one page)

**Hackathon demo with fake patients: none of the steps below apply.** No real person, no real data, no research. Keep saying "fake patients only" and never upload a real prescription to the demo. (The only rule that applies today: don't use a real person's prescription photo even "to test the OCR" – that is real health data and, if used to develop the AI, needs EC approval [R7 §4.2 (vi)].)

**Before a real pilot (all apply):**
1. **Decide what is care and what is research.** Routine reminders in a paid service are care. Measuring whether they work, publishing, or training AI on the data is research and needs an EC [R8 §11.7].
2. **Find a faculty principal investigator** at the hospital and check its EC is registered with DHR (`05_icmr…:76`, B5-7).
3. **Ask CDSCO via MedTech Mitra** in writing: (a) base unit class and whether the pilot needs MD-22; (b) whether the medicine module is medical-device software (`05_icmr…:115`).
4. **Write the 17-item AI checklist** answer [R7 Table 2] plus the protocol, information sheet and consent form in each language.
5. **Consent with separate ticks:** care, family sharing, records storage, AI use (with a "no AI" option), research use of data, AI training. Witness and thumb-print path for people who cannot read (B5-4).
6. **Teach-back** at the end of consent [R7 §4.2 (ii)].
7. **Human-in-the-loop written into the protocol:** a named nurse/pharmacist confirms every parsed prescription; who is accountable for what, in writing [R7 §1.5].
8. **No dose or drug changes in the study, ever** (keeps it outside NDCT [R9]).
9. **Data plan:** India storage, role-based access, encryption, photo deletion after confirmation, breach plan [R8 Box 11.6; L-7].
10. **Compensation/insurance** for research injury from the host institution (B5-6; [R9] Q12 says ICMR compensation rules apply even to academic drug trials).
11. **EC approval → CTRI registration (free) → first patient** (`05_icmr…:82`, B5-8).
12. **Serious adverse events** to the EC within 24 hours (B5-6); keep an incident log for every missed or wrong reminder.
13. **Publish** a short yearly audit of AI performance and errors [R7 §1.5].
14. **Never say** "ICMR approved", "ethics approved" or "validated" (`05_icmr…:196`).

- **Verdict:** nothing in ICMR blocks the recovery kit, but the prescription reader adds three duties the spirometer pilot did not have: EC approval before using real prescriptions to build the AI, a human sign-off on every parsed prescription, and published audits. **CONFIRMED** (primary ICMR and CDSCO texts read) / our application is a reading, not a ruling.

---

## 3. Proposed product shape

### 3.1 Tiers
| Tier | Who pays | What's in it | Status |
|---|---|---|---|
| **1. Hospital spirometer tier** (today's plan) | Hospital, about ₹1,000 per episode (est., `03_COSTS_AND_BUDGET.md:26`) or ₹200 software on hospital-owned units | Clip-on base, voice coach, nurse dashboard, family WhatsApp | Software Live/Simulated; device not built |
| **2. Software-only recovery tier** | Family or hospital, monthly | Medicine reminders (voice call + family WhatsApp), human-confirmed schedule, follow-up date reminders, "breath from any source" with manual log | Planned |
| **3. Premium home recovery kit** | Family top-up, or hospital as a premium discharge option | Tier 1 + tier 2 + lent hub phone and optional lent BLE devices (pulse oximeter, BP) + scheduled nurse check-in calls | Planned |

### 3.2 Feature list with status
| Feature | Status |
|---|---|
| Voice breathing coach, nurse dashboard, family WhatsApp preview, red-flag fixed message | **Live** (demo, fake patients) |
| Clip-on base readings | **Simulated** |
| AI daily summary (template fallback live) | **In development** |
| WhatsApp and phone calls (real sending) | **In development** (sandbox/preview) |
| Prescription photo → AI draft → human confirms | **Planned** |
| Medicine reminders by voice call and family WhatsApp | **Planned** |
| "Reported" vs "measured" adherence labels | **Planned** |
| ABDM link (send episode report; view in Aarogya Setu/Eka) | **Planned** |
| Follow-up booking via UHI or hospital link | **Planned** |
| Lent hub phone, pre-paired before discharge | **Planned** |
| BLE pulse oximeter / BP / weight via standard profiles | **Planned** |
| Three-ball light-gate bracket | **Planned** (research item) |
| Phone-camera breath reading | **Planned** (experiment) |
| Cellular (SIM) base | **Planned**, after company + M2M registration |

### 3.3 Staged roadmap
| Stage | What we do | Must be true to move on |
|---|---|---|
| **0–3 months** | Spirometer bench test; 5–10 interviews incl. "would you pay ₹2,000 for a 30-day kit?" and "who confirms prescriptions on your ward?"; MedTech Mitra questions incl. the medicine module; build the human-confirm screen on **synthetic** prescriptions only | Bench test passes; at least 3 of 10 families or nurses say yes to a priced kit; written CDSCO answer requested |
| **3–12 months** | Spirometer pilot (as `05_EXPANSION_AND_CUSTOMERS.md:581`, E-20); add medicine reminders for pilot patients with nurse-confirmed schedules (no AI parsing until EC approves); prototype three-ball light-gate bracket; ABDM: send episode PDF into the hospital's system | Pilot number (share of due sessions done); zero unconfirmed schedules sent; nurse time per patient measured |
| **12–24 months** | Premium kit with lent hub phones and BLE devices; AI prescription drafting (printed only) under EC approval; ABDM HIP integration; paid hospital or family pilots at ₹2,000-band prices; decide on the cellular base | Paying customers renew; reader error rate measured; licence path clear |

### 3.4 Does ₹2,000 cover the kit? (all numbers are **ESTIMATES**)
**Assumption:** a 30-day "recovery plan" after a big operation, family uses their own phone unless stated, the clip-on base is **lent and returned**, ₹96 = US$1.

| Cost line (₹ per 30-day episode) | At scale | Pilot size | Basis |
|---|---|---|---|
| Clip-on base, lent (share + 5% loss + cleaning) | 395 | 395 | `03_COSTS_AND_BUDGET.md:192-194` (₹2,500 unit ÷ 10 patients + loss + cleaning) |
| Server, messages, voice, summaries (1 patient-month) | 85–110 | ≈ 450 | `FUTURE_ARCHITECTURE.md:360` §11 |
| Medicine reminders: 3 doses a day by pre-recorded call | ≈ 70 | ≈ 70 | 90 calls × about ₹0.76 line cost (Plivo, `KNOWLEDGE_BASE.md:500`) (est.) |
| Family WhatsApp alerts (misses only, ~30) | ≈ 4 | ≈ 4 | ₹0.115 each (F-COMMS-2) |
| AI calls on misses (~4) | ≈ 32 | ≈ 32 | ≈ ₹8 per AI call (`KNOWLEDGE_BASE.md:500`) |
| Prescription draft by AI | ≈ 5 | ≈ 5 | Our guess for one image call; **quote needed** |
| Human confirmation of the prescription (≈10 min) | 30–60 | 30–60 | Nurse at ₹22,000–40,000 a month (snippet) ≈ ₹90–170 an hour, ×1.5–2 overheads (est.) |
| Nurse check-in calls and alert triage (≈50 min) | 100–300 | 100–300 | Same basis (est.) |
| Onboarding and support (≈15 min) | 25–75 | 25–75 | `03_COSTS_AND_BUDGET.md:200` method (est.) |
| **Core kit total** | **≈ 750–1,050** | **≈ 1,110–1,390** | |
| + Volume spirometer, if we supply it (patient keeps) | +146 to +1,067 | same | `03_COSTS_AND_BUDGET.md:205` |
| + Lent hub phone + SIM (no-smartphone homes) | +≈ 870–950 | same | ₹5,400–6,000 phone ÷ 10 uses + 5% loss + ₹300 SIM (est.) |
| + Lent BLE pulse oximeter | +≈ 470 | same | ₹3,124 [R22] ÷ 10 + 5% loss (est.) |
| + Lent BLE BP monitor | +≈ 360 | same | ₹2,400 ÷ 10 + 5% loss (est.) |
| GST if sold as a service (18%) | ₹2,000 leaves ≈ ₹1,695 | | `03_COSTS_AND_BUDGET.md:217` |

**What this says:**
- **₹2,000 covers the core kit at scale** (about ₹750–1,050 against ₹1,695 after GST), with room for some nurse time.
- **It does not cover the pilot-size version plus a spirometer plus a hub phone** (≈ ₹1,110 + ₹1,067 + ₹910 ≈ ₹3,100).
- **It cannot cover a multi-device kit** (oximeter + BP + hub) unless devices are lent and recovered many times.
- **Nurse time is the swing cost.** At 50 minutes it fits; at 2 hours a month it does not.

**Three price options around ₹2,000 (each an ESTIMATE):**
| Option | Price | Basis | Covers |
|---|---|---|---|
| **A. One-time ₹2,000 "30-day recovery plan"** | ₹2,000 once; base returned; family's own phone | Core cost ≈ ₹750–1,050 at scale | Core kit. Add ₹1,000 refundable deposit for the base |
| **B. ₹1,499 first month + ₹299 a month after** | Software-only months after month 1 | Software-only cost ≈ ₹200–400 a month (server + reminders + 15 min nurse) (est.) | Long medicine schedules (heart patients often stay on medicines for months) |
| **C. Hospital-bundled ₹1,000 + family top-up ₹999** | Hospital pays its usual ₹1,000 per episode (`03_COSTS_AND_BUDGET.md:26`); family adds ₹999 for "premium": hub phone, oximeter, extra nurse calls | PM-JAY makes the first 15 days the hospital's cost [R20] | Full premium kit at about ₹2,000 total from two payers |
| Software-only tier (no hardware) | ₹199–299 a month | Same as B | Families with their own devices |

- **Compared with today:** ₹2,000 is about one day of a home nurse (₹1,000–3,500 [R2]) and half of Dozee's 30-day rental (₹3,999, snippet).
- **The ₹1.5 lakh band, in one line:** that is residential recovery facility pricing (₹40,000–1,20,000 a month [R2]) and needs on-site nurses; not a SpiroBuddy product.

---

## 4. Safe medication design (box)

> **Rules that never change**
> 1. **The AI never diagnoses, never advises and never changes a dose, a drug, a time or a duration.** It only drafts what the doctor wrote.
> 2. **A human confirms every parsed prescription** – a named nurse, pharmacist or (for family-run plans) the doctor's clinic – line by line, with the photo crop beside each line, **before any reminder is sent**. Handwritten prescriptions are typed by the nurse, not read by the AI.
> 3. **Anything uncertain is blank, not guessed.** "SOS" (only when needed) medicines are never scheduled as reminders.
> 4. **Reminders repeat the doctor's words** and say who confirmed them. No "you may skip", no "take two now".
> 5. **Missed doses go to the family and nurse**, never "double up" advice to the patient.
> 6. **Red-flag words** (chest pain, breathless, bleeding, fainting, allergy, rash, "took too many", and the same in each language) → the fixed message: **"Please contact your nurse now. In an emergency call 112."** No AI text.
> 7. **Questions about medicines** ("can I stop this?") → "Please ask your doctor or nurse" plus a call-back button. No AI answer (Telemedicine Guidelines, L-8).
> 8. **Adherence shown as "reported"** unless a sensor measured it ([R17]).
> 9. **Every AI step is logged**; the nurse can see and undo it; errors are counted and published yearly [R7 §1.5].
> 10. **No real prescriptions are used to train or test the AI** without ethics approval [R7 §4.2 (vi)].

---

## 5. What to say in the pitch roadmap (5 lines max)

1. "Today SpiroBuddy proves one thing: whether the breathing exercise was actually done."
2. "Next, we plan a home recovery kit: medicine reminders by voice call, with a nurse confirming every prescription first." (Planned)
3. "It will link to India's ABDM records rather than build another records app." (Planned)
4. "We plan a reader for the cheap three-ball spirometer that most wards use." (Planned)
5. "Families already pay about ₹1,000–3,500 a day for a home nurse; we are testing whether ₹2,000 for a 30-day kit is a price they accept." (estimate; to be tested)

## What NOT to claim
- "AI reads your prescription" or "accurate prescription reading" – no accuracy measured; best published model is not deployable [R1].
- "Reduces readmissions" or "improves medication adherence" – no evidence for our kit; the largest reminder-app trial found no clinical benefit [R3].
- "ABDM-integrated", "ABHA-enabled", "PHR app" – none done.
- "Works with any spirometer" or "reads three-ball spirometers" – Planned only.
- "Connects to any device" – only standard-profile devices, and nothing built.
- "Doses taken" – say "doses reported".
- "Complete recovery system" in the present tense.
- "Not a medical device" for the kit – not decided (B4-1, [R16]).
- "First in India" – Apollo already sells a home recovery package [R15].
- "ICMR approved / ethics approved / validated".
- Any ₹ price as fixed – all prices are estimates to be tested.

---

## 6. Open questions
1. Will a family pay ₹2,000, and will a hospital co-pay? (interviews; one hospital purchase head)
2. Who confirms prescriptions on a typical ward today, and how long does it take? (nurse interview)
3. Does CDSCO treat a human-confirmed reminder module as medical-device software? (MedTech Mitra)
4. What does Apollo charge for its 2-week Home Discharge package? (call Apollo HomeCare; not published)
5. Current Indian price of a WhatsApp-capable hub phone and a 30-day data SIM. (quote)
6. M2M registration fee and time for a startup, and LTE-M/NB-IoT coverage in target cities. (operator enterprise desk)
7. Which Bluetooth oximeters and BP monitors sold in India use the standard SIG profiles? (buy and test 3 models)
8. Can a light-gate bracket read Indian three-ball models (Romsons SH 6082 and others)? (bench test)
9. Accuracy of AI on **printed** Indian discharge summaries. (synthetic test set first)
10. The official ABDM PHR/HIP onboarding steps and time. (abdm.gov.in and the forum refused connections this round; ask NHA integration support)
11. A real Indian figure for medicine non-adherence after heart or lung surgery. (PubMed/IJTCVS search)
12. Whether the EC at the pilot hospital treats medicine reminders as part of the spirometer study or a separate one.

---

## 7. Sources opened for this file (all added to `SOURCES_LEDGER.md`, rows 340 onward)

| # | URL | Title | Publisher | Grade | Used in |
|---|---|---|---|---|---|
| R1 | https://arxiv.org/html/2410.09729v2 | MIRAGE: multimodal identification of annotations in Indian general prescriptions (v2) | arXiv preprint | B | B-1, H-1 |
| R2 | https://www.antaraseniorcare.com/blogs/cost-of-post-operative-care-chennai | Cost of post-operative care, Chennai (24 Jun 2026) | Antara Senior Care (vendor blog) | C | A-2, 3.4 |
| R3 | https://jamanetwork.com/journals/jamainternalmedicine/article-abstract/2678454 | Morawski et al. 2018, MedISAFE-BP trial | JAMA Internal Medicine | A | B-2, D, G |
| R4 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8194115 | Shawon et al. 2021, 30-day readmission after CABG meta-analysis | J Cardiothorac Surg via PMC | A | A-1 |
| R5 | https://www.eka.care/ | Eka Care home page | Eka Care | B | B-2, F |
| R6 | https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/jul/doc202676912801.pdf | ABDM backgrounder, 6 Jul 2026 (Aarogya Setu 2.0, Scan & Share, UHI, DHIS) | PIB, Govt of India | A | Answer, B-2, C-1, F |
| R7 | https://www.icmr.gov.in/icmrobject/custom_data/pdf/Ethical-guidelines/Ethical_Guidelines_AI_Healthcare_2023.pdf | Ethical Guidelines for Application of AI in Biomedical Research and Healthcare, 2023 (full text read) | ICMR | A | H, G, 4 |
| R8 | https://ethics.ncdirindia.org/asset/pdf/ICMR_National_Ethical_Guidelines.pdf | ICMR National Ethical Guidelines 2017 – re-opened for §5.5, §5.7, §11 (ledger #310) | ICMR | A | H |
| R9 | https://cdsco.gov.in/opencms/export/sites/CDSCO_WEB/Pdf-documents/New-Drugs/FAQs/faqonndandctRules24set25.pdf | FAQs on New Drugs and Clinical Trials | CDSCO | A | H |
| R10 | https://circuitdigest.com/articles/how-can-you-get-and-use-an-m2m-iot-sim-card-in-india | How to get an M2M IoT SIM in India (25 May 2026) | CircuitDigest | B | E-2 |
| R11 | https://evelta.com/quectel | Quectel modules (EC200U, BC66) prices | Evelta (retailer) | C | E-2 |
| R12 | https://docs.nordicsemi.com/r/bundle/sds_s113/page/sds/s1xx/ble_protocol_stack/profile_service_support.html | SoftDevice S113: adopted profile and service support | Nordic Semiconductor | B | E-2 |
| R13 | http://www.forrester.com/blogs/supporting-healthcare-with-connected-devices-current-health/ | Supporting healthcare with connected devices: Current Health (28 Oct 2020) | Forrester blog | B | E-1, F |
| R14 | https://www.homecaremag.com/news/copilotiq-biofourmis-merge | CopilotIQ and Biofourmis merge (29 Oct 2024) | HomeCare magazine | B | F |
| R15 | https://www.indianpharmapost.com/news/lite/apollo-launches-hyderabads-first-homecare-recovery-program-14753 | Apollo launches Hyderabad's first homecare recovery program (6 Oct 2023), via Jina Reader | Indian Pharma Post | B | A-3, F |
| R16 | https://www.cdsco.gov.in/opencms/export/sites/CDSCO_WEB/Pdf-documents/Guidance-document-on-Medical-Device-Software-under-MDR-2017.pdf | CDSCO Guidance on Medical Device Software 2026 – re-opened for "not MDSW" list (ledger #135) | CDSCO | A | B-4, G |
| R17 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7713673 | Thomas et al. 2020, accuracy of 99DOTS vs urine isoniazid | Clin Infect Dis via PMC | A | D, E-3, 4 |
| R18 | https://news.samsung.com/in/samsung-announces-new-medications-tracking-feature-for-samsung-health-in-india | Samsung Health Medications feature in India (24 Oct 2024), via Jina Reader | Samsung Newsroom India | B | B-1, B-2, F |
| R19 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8173298/ | Bhagavathula et al. 2021, polypharmacy in older Indians, meta-analysis | Frontiers in Pharmacology via PMC | A | A-1 |
| R20 | https://sha.uk.gov.in/ScannedDocs/WebSite/Uploads/CLAIM_ADJ/Claims%20Adjudication%20FAQs.pdf | PM-JAY claims adjudication FAQs (15-day post-hospitalisation rule) | State Health Agency, Uttarakhand | A | A-4, 3.4 |
| R21 | https://www.preprints.org/manuscript/202606.1791/v1 | HL7 FHIR implementation in India, mixed-methods assessment (preprint, 2026), via Jina Reader | eGov Foundation / WHO SEARO, preprint | B | B-1, C-3 |
| R22 | https://pharmeasy.in/health-care/products/bpl-medical-technologies-ioxy-bluetooth-finger-tip-pulse-oximeter-4396078 | BPL iOxy Bluetooth pulse oximeter listing | PharmEasy (retailer) | C | A-2, 3.4 |
| R23 | https://www.orfonline.org/research/india-s-2025-national-health-survey-update-higher-access-persistent-financial-risk | India's 2025 national health survey update (13 May 2026) | Observer Research Foundation | B | A-2 |
| R24 | https://ijme.in/articles/telemedicine-and-ethics-opportunities-in-india/ | Telemedicine and ethics: opportunities in India (abstract only, 2021) | Indian Journal of Medical Ethics | A | H-1 |

**Opened but failed or empty (logged in the ledger as "nothing useful"):** link.springer.com (login redirect; same paper read as R4), care.samarth.community (403), news.samsung.com PHR article (timeout), dashboard.abdm.gov.in (title only), currenthealth.com (404), mdmaxx.com Stel Life hub (403), healthexec.com (403), histalk2.com (redirect), bwhealthcareworld.com (403, also via Jina), fiercehealthcare.com (403), businesswire.com CopilotIQ (403 via Jina), two apollohospitals.com pages (403), abdm.gov.in:8081 HIP/HIU guidelines (refused), devforum.abdm.gov.in (refused), jmir.org 2021 review (empty), jmir.org 2022 WTP review (empty), doaj.org WTP record (403).

**Search snippets only (grade C, not opened):** Dozee rental prices (BioSpectrum); Portea 2018 critical-care price (MediaNama); Samarth nurse shift prices; Current Health sale (HIStalk, HealthExec); Hello Heart funding; Lok Sabha ABHA figure (Kashmir Life); Scan & Share 2024 PIB figures; Triflo II flow range and ±400 cc/s; Omron Bluetooth BP price trackers; IRDAI home-treatment add-on (2021 news); Apollo 900 enrolments and 3/100 readmission (BW Healthcare); DRiefcase first ABDM PHR app (BioSpectrum, Jan 2022); Indian prescription abbreviation and pharmacist surveys; Vietnamese OCR study; AIIMS Deoghar, IHJ 2017 and ACS-registry adherence studies; JMIR 2022 willingness-to-pay review; PwC remote-monitoring survey; ABDM developer forum PHR answer; Indian SMS/WhatsApp BP trials (SMS4BP, Punjab).

**Older ledger rows cited, not re-opened:** #130, #135 (re-opened, see R16), #310 (re-opened, see R8), #339.
