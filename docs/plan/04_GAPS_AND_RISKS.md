# Gaps and risks – what we missed

**Written:** 10 Oct 2026 · **Sources opened:** 19 (10 readable, 9 failed or unreadable) plus search snippets, all listed at the end · **Confidence overall:** medium (high on "what is missing", medium to low on prices and on rules we could only read second-hand)

**Answers founder note 18:** "How much stuff did we miss? Plan everything, every single detail."

**How to read this file.** Each gap has an ID (G-1, G-2 …). Severity uses four levels:

| Code | Meaning |
|---|---|
| **P0** | Blocker before any real patient touches it |
| **P1** | Blocker before a paid pilot |
| **P2** | Needed at scale (3+ hospitals) |
| **P3** | Nice to have |

Effort: **S** = days, **M** = weeks, **L** = months. **₹** = costs money, passed to the costs file. Owners are roles, because the team's names are not in the repo yet: **Lead** (founder), **Tech**, **Clinical** (a doctor or physiotherapist we do not have yet), **Ops**, **Reg** (regulatory consultant), **CA** (chartered accountant), **Lawyer**.

Research status words: **CONFIRMED** (two independent sources or one primary source), **SINGLE SOURCE**, **NOT CONFIRMED**. Source grades: A = law, regulator, peer-reviewed · B = reputable organisation · C = blog, vendor, or a search snippet we did not open ("snippet only"). `#123` = a row in `docs/research/SOURCES_LEDGER.md`. **Nothing here is legal, medical or tax advice. Confirm with a clinician, a regulatory consultant, a lawyer and a CA before acting.**

Not repeated here (owned by sibling files): parts, power, enclosure (`01_HARDWARE_REVIEW.md`); app, Bluetooth, app stores (`02_MOBILE_APP_AND_BLUETOOTH.md`); customers and expansion (`05_EXPANSION_AND_CUSTOMERS.md`); itemised costs (`03_COSTS_AND_BUDGET.md`).

---

## Answer in 12 lines

1. **We missed a lot, but most of it is paperwork and people, not code.** This file lists 96 gaps. 27 of them block a first real patient.
2. **The biggest hole is clinical.** Nobody with a medical licence has reviewed anything. There is no list of who must NOT use the product, and the standard guideline says the exercise is wrong for patients who cannot be instructed or supervised (confused, sedated, very young). That describes some of our home users.
3. **No one decides the target volume.** The app lets a nurse type a goal, but there is no rule for how to pick it or change it day by day, and we found no Indian reference values for it.
4. **There is no rest or "stop if dizzy" rule.** Hospital leaflets all say stop and breathe normally if light-headed. Our plan asks for up to 10 breaths, 14 times a day, with no pain or dizziness check built.
5. **The public code repository lists our own open security holes** (no login on the nurse pages, unprotected call webhooks). Fine for fake patients. Must be fixed, or the repository made private, before a real one.
6. **The live site runs on free hosting that says "do not use for production"** and a free database that pauses after a quiet week. Paid plans in Mumbai are a must before a pilot.
7. **There is no company, no founders' agreement, no written answer on who owns the code**, and the college's and the hackathon's ownership rules have not been read. Every grant and every hospital will ask.
8. **Operations are blank:** who trains nurses, who answers the phone when a unit fails at 8 pm, how units come back from homes, who cleans and logs them, what the hospital's biomedical engineers will demand.
9. **A light quality system must start now**, not at licence time: a risk file, a complaint log, serial-number tracking and a recall plan cost almost nothing today and are painful to rebuild later.
10. **Ethics gaps:** consent that an elderly, non-reading patient truly understands; the family update can feel like being watched; separate permission to train the model on a patient's breaths; what the patient keeps when the pilot ends.
11. **Every number in the business plan is unmeasured:** reuse count, loss rate, price, share of operations with a spirometer, sensor accuracy, whether patients can use it. Section J gives the cheapest test for each; eight can be done within a month for almost no money.
12. **Three things to do this month:** find a clinical lead, sign a one-page founders' agreement, and run the bench test of the sensor through a real tube. If the bench test fails, most of the rest changes.

---

## A. Clinical and safety

**Already covered:** red-flag words → fixed "contact your nurse / call 112" message (`FEATURE_STATUS.md` §7); the AI never diagnoses (`backend/app/llm.py`); evidence for and against the exercise (`RESEARCH_REPORT.md` §2.3–2.4); ethics and insurance for a study (`05_icmr_ethics_abdm_evidence.md` B5-4 to B5-6); breath-hold time 3–5 s (ledger #44, #45).

### What is missing

| ID | Gap | Why it matters | Sev | Owner | Effort |
|---|---|---|---|---|---|
| G-1 | **No contraindication list and no screening step.** Nothing asks "should this patient do the exercise at all?" | Coaching the wrong patient is the most direct way to harm someone | P0 | Clinical | S |
| G-2 | **No rule for the target volume.** The nurse types a number; no guidance, no starting value, no daily progression, no cap | A goal set too high causes pain, strain and a false "falling behind" alert; too low and the exercise does nothing | P0 | Clinical + Tech | M |
| G-3 | **No rest rule, no dizziness or pain check.** "Pain / breathless check" is listed as not built | Fast repeated deep breaths cause light-headedness; a fall at home after surgery is a serious harm | P0 | Clinical + Tech | S |
| G-4 | **No clinical risk file.** No written list of ways the product could hurt someone, with likelihood and a control for each | Ethics committees and the regulator ask for it; it also drives design | P0 | Clinical + Reg | M |
| G-5 | **No adverse-event process.** Nobody is named to receive, record and report a harm | Required by a study protocol now and by the licence later (see G-R4) | P0 | Clinical + Lead | S |
| G-6 | **No "what happens if it fails mid-session" behaviour.** Unit dies, phone dies, voice stops at breath 6 | The patient may wait, panic, or think they did it wrong. The safe default must be: carry on with the plain spirometer | P0 | Tech | S |
| G-7 | **Nurse alert load is unmeasured.** Red/amber rules were set by the team, never agreed with a nurse (`RESEARCH_REPORT.md` 11.1 item 11) | Too many alerts get ignored, and then the real one is missed | P1 | Clinical + Tech | M |
| G-8 | **No clinical sign-off of spoken sentences.** 21 lines × 11 languages; native-speaker checks are pending in 3 languages, medical review in none | A mistranslated instruction ("breathe out" for "breathe in") is a safety defect | P0 | Clinical | M |
| G-9 | **No named clinical advisor or lead.** | Every item above needs one. Grants and ethics committees expect one | P0 | Lead | S |
| G-10 | **Oxygen users.** A patient on an oxygen mask must take it off to use the mouthpiece | Oxygen level can drop during repeated breaths (G-R3) | P1 | Clinical | S |
| G-11 | **No rule for when the coach should say "stop for today".** | Fatigue, wound pain, cough with blood: the software keeps counting to 10 | P0 | Clinical + Tech | S |
| G-12 | **False reassurance.** A green tick tells the family "all is well" when it only means "did the exercise" | A family may delay calling a doctor | P1 | Clinical | S |
| G-13 | **No hand-over from hospital target to home target** at discharge, and no end date for the episode | Reminders that never stop; goals that never change | P1 | Clinical + Tech | S |

### What the research found

**G-R1: The standard guideline lists patients for whom the exercise is not appropriate. Our plan has no equivalent.**
- Detail: The American Association for Respiratory Care guideline (2011) lists as contraindications: patients who cannot be instructed or supervised to use the device properly; patients who cannot cooperate or understand (very young children, confused or delirious patients, heavily sedated patients); patients who cannot breathe deeply because of pain, a weak diaphragm or opioid painkillers; and patients who cannot generate enough breath (vital capacity below about 10 mL per kg of body weight, or inspiratory capacity below about one-third of predicted). A teaching site adds untreated pneumothorax (collapsed lung with air in the chest). A general reference adds caution with pneumothorax and with recent chest, abdominal or eye surgery.
- Source: AARC guideline, Respiratory Care 2011;56(10):1600 – snippet only, grade C as read (the journal page refused us twice, ledger #40 and S1) · respiratorytherapyzone.com (S8, grade C, opened) · Wikipedia "Incentive spirometer" (snippet only, C).
- Status: **SINGLE SOURCE at grade C** for the exact wording. The list is consistent across what we could read. We did **not** find haemoptysis (coughing blood) or "unstable patient" on an incentive-spirometer list; those appear on lists for lung-function *testing*, which is a different procedure. **NOT CONFIRMED** for those two.
- What it means: a human with access to the journal must read the full guideline (10 minutes). Then a clinician writes our list. Until then the rule is: **a clinician decides who gets a unit; the software never decides.** Dementia and delirium are on the list, so "patients with dementia" (section B) is not an accessibility problem to solve; it is a group to exclude or to enrol only with a carer present.

**G-R2: The target is normally set by a clinician, often from a chart of predicted values by age, height and sex. No Indian chart was found.**
- Detail: A UK teaching-hospital leaflet says the physiotherapist, nurse or doctor sets the device up, and the patient moves the marker to the best volume reached and uses that as the next target. Makers print a chart ("nomogram") of predicted inspiratory capacity by age, height and sex; a US trial protocol shows one that starts at 2,000 mL for a 20-year-old man of 58 inches and falls with age. Studies of Indian adults report lung volumes below European predictions.
- Source: Cambridge University Hospitals leaflet, approved 16 Jul 2024 (S3, B) · clinical-trial protocol and Indian lung-function studies (snippets only, C).
- Status: clinician-sets-target **CONFIRMED** (S3 plus ledger #44, #45). Indian reference values for inspiratory capacity: **NOT CONFIRMED** – none found. Whether a Western chart overstates the goal for Indian patients: plausible, **NOT CONFIRMED**.
- What it means: do not ship a built-in chart. Version 1 rule to propose to the clinical lead: start from the patient's best supervised breath in hospital; the goal is that value; raise it only when the patient beats it on several sessions; the nurse can override. Collecting the first Indian reference set is a research contribution in itself.

**G-R3: Hospital leaflets agree on "stop if dizzy" and on short sets with rests. They do not agree on the dose.**
- Detail: Cambridge: three cycles of four deep breaths with a short rest between cycles, "regularly through the day"; if dizzy, take more breaks. Other NHS leaflets: stop and take a few normal breaths if dizzy or light-headed; if it recurs, do fewer breaths at a time. A teaching site: 5–10 breaths per session, about hourly while awake, rest between breaths; lists light-headedness and tingling from over-breathing, tiredness, airway spasm in asthma, and a fall in oxygen if an oxygen mask is left off too long; states "no single schedule is proven best".
- Source: S3 (B) · United Lincolnshire, Northern Care Alliance, Stockport, Lancashire leaflets (snippets only, C; one refused us, S2) · S8 (C).
- Status: "stop if dizzy, rest between breaths" **CONFIRMED**. A single correct dose: **NOT CONFIRMED** (sources differ).
- What it means: our "10 breaths, 14 times a day" is one reasonable schedule, not a standard. The care plan must let the clinician set breaths per session and sessions per day (today sessions are fixed at 14). Add: a forced pause between breaths, a "feeling dizzy?" button, and a spoken "stop and breathe normally" line. All are small changes.

**G-R4: India has a reporting scheme for harm from medical devices. Licence holders must report; hospitals and staff may.**
- Detail: The Materiovigilance Programme of India (MvPI) started in 2015. The Indian Pharmacopoeia Commission coordinates it; CDSCO is the regulator. A licence holder must tell the licensing authority about a "suspected unexpected serious adverse event" and act on it, including any recall, **within 15 days of learning of it**. Serious means death, life-threatening, permanent damage or hospital admission. There is a reporting form, a form for recalls and fixes in the field (FSCA, "field safety corrective action"), and a helpline, 1800 180 3024 (Mon–Fri, 9:00–17:30). A CDSCO circular (2024) repeated the duty.
- Source: IntechOpen chapter, 2021 (S4, B) · Lexplosion note on the CDSCO circular, 3 Jun 2024 (S11, C) · IPC's own page returned "not found" (S19).
- Status: 15-day duty for licence holders **CONFIRMED at grade B/C**; the rule number should be read in the Medical Devices Rules text (ledger has the PDF) before quoting.
- What it means: before a licence, harm in a study is reported under the study protocol to the ethics committee and the lead investigator (B5-6). After a licence, the 15-day clock applies to us. Either way we need one page: who receives a complaint, how it is graded, who reports, by when. Write it now.

**G-R5: Most alarms in hospitals do not need action, and nurses slow down as useless alarms pile up.**
- Detail: A video study in a children's hospital (36 nurses, 210 hours): 87.1% of intensive-care alarms and 99.0% of ward alarms needed no action, and nurses responded more slowly after more non-actionable alarms. A 2026 survey of nurses doing remote care after surgery reports that "digital alert fatigue is common" and linked to less proactive escalation.
- Source: Journal of Hospital Medicine 2015, PMC4456276 (S18, A) · BMC Nursing 2026 (snippet only, C; login wall, S17).
- Status: **CONFIRMED** for bedside alarms; **SINGLE SOURCE (snippet)** for remote post-surgery care.
- What it means: count alerts per nurse per shift in the pilot and set a ceiling. Ask the ward to agree thresholds before go-live. Report "share of alerts the nurse acted on" as a pilot outcome.

---

## B. People who are not the "typical" user

**Already covered:** voice-first design, big text, 11 languages, family in the loop (`RESEARCH_REPORT.md` §3); LASI figures: only 24% of women aged 60+ can read and write, 37.1% have low vision when tested, 9.6% report hearing problems and 0.7% use a hearing aid (ledger #117).

| ID | Group | What is missing | Sev | Owner | Effort |
|---|---|---|---|---|---|
| G-14 | **Hearing loss** (about 1 in 10 report it; almost none have aids) | A voice-first product fails silently for them. Need: a loud, low-pitched voice option, a volume test at set-up, lights and a large on-screen cue that carry the same meaning as the voice, vibration on the phone | P1 | Tech | M |
| G-15 | **Low vision** (over a third) | Works if voice works. Missing: a set-up the patient can do by touch (one raised button), high-contrast marks on the unit | P1 | Hardware + Tech | S |
| G-16 | **Tremor or weak hands** (common after surgery and in the elderly) | Placing the spirometer on the base and holding it steady. A shaking tube moves the disc reading. Needs a bench test with deliberate shake and a stable base | P1 | Hardware | S |
| G-17 | **Dementia, delirium, heavy sedation** | A listed contraindication (G-R1). Missing: an enrolment question, and a "carer must be present" mode | P0 | Clinical | S |
| G-18 | **Non-readers** | Covered by voice. Missing: consent they can truly give (section H), pictures on the quick-start card, no text-only error messages | P0 | Clinical + Design | S |
| G-19 | **A language we do not have** (India has 22 scheduled languages; we have 11) | No fallback is defined. Proposal: pictures and tones only, plus a family member's language for the updates; never fall back to English silently | P1 | Tech | S |
| G-20 | **Children** | Different device size, different goals, parental consent, and stricter rules on children's data under the privacy law (B4-13). A child-size spirometer exists for under-12s (snippet, C). Decision needed: **adults only for now**, stated in the instructions | P0 (decide) | Lead | S |
| G-21 | **Tracheostomy** (a breathing tube in the neck) | They do not use a mouthpiece: a one-way-valve T-piece fits the tube (snippet, C; the leaflet page was gone, S15). Our unit should still read the disc. Untested. Decision: exclude from the first pilot | P1 | Clinical | S |
| G-22 | **Facial weakness or no lip seal** (stroke, nerve disease) | Air leaks, so the disc under-reads and the coach scolds a patient who is trying. Diagnostic lung testing uses a face mask for these patients and reads about 200 mL lower (snippet, C). Decision: exclude at first; never label such breaths "too shallow" without a nurse's note | P1 | Clinical | S |
| G-23 | **Left-handed or one-handed set-up; bed-bound patients** | The unit must work from either side and on a bed tray. The spirometer must stay upright; in bed it tilts | P1 | Hardware | S |
| G-24 | **Patients with no family** | The reminder ladder ends at "family". Missing: a path that skips to the nurse, and a home with no second phone | P1 | Tech + Clinical | S |
| G-25 | **No reliable electricity** | NFHS-5 shows most states with 96–99% of people in homes with electricity (snippet, C), but that says nothing about hours of supply. Missing: battery life target in days, charge from a phone charger or power bank, a clear "charge me" signal the patient can hear. Battery life is unmeasured (`DEVICE_LIFECYCLE.md` §10) | P1 | Hardware | M |
| G-26 | **No smartphone in the home, or one shared phone** | 41% of older Indians own a smartphone (repo, F-INDIA-5). The plan relies on a phone. The hospital-lent "hub phone" is an open question in `DEVICE_LIFECYCLE.md` | P1 | Lead + Ops | M |
| G-27 | **Women as patients and as carers** | See H (equity). Phone is often the husband's or son's; updates then go to him, not to her | P1 | Clinical | S |

---

## C. Operations and service

**Already covered:** the assign → return → clean → re-issue life cycle on paper (`DEVICE_LIFECYCLE.md` §5); cleaning class for skin-contact equipment (B6-10); loss rates abroad (B6-16); none of it is built or tried.

| ID | Gap | Why it matters | Sev | Owner | Effort | ₹ |
|---|---|---|---|---|---|---|
| G-28 | **Nurse training plan:** who trains, how long, what proves a nurse is trained, retraining for new staff and night shifts | Wards rotate staff; an untrained nurse assigns a unit to the wrong patient | P0 | Ops + Clinical | M | ₹ |
| G-29 | **Quick-start card and 2-minute video** for patients (pictures first) and a separate one for nurses | Listed as "not built" in `FEATURE_STATUS.md` §3 | P0 | Design | S | ₹ (print) |
| G-30 | **Helpline:** a number, hours, languages, who answers, what they may and may not say (never clinical advice) | A patient whose unit is silent at 8 pm will call someone. If nobody, they stop | P0 | Ops | S | ₹ |
| G-31 | **Spare units and swap-outs:** how many spares per ward, who swaps, how fast | A dead unit with no spare ends that patient's programme | P1 | Ops | S | ₹ |
| G-32 | **Getting units back from homes:** who collects, when (follow-up visit? courier?), what if the patient moves or dies | The business model rests on reuse. Nobody has designed the return trip | P1 | Ops | M | ₹ |
| G-33 | **Cleaning log:** who cleaned which serial number, when, with what; a "clean / not clean" tag on the unit | Infection control will ask on day one; also needed for the risk file | P0 | Ops + Clinical | S | – |
| G-34 | **Stock control:** a list of every unit by serial number and where it is; lost, broken, retired | Without it, loss rate (the key business number) cannot be measured | P0 | Ops + Tech | S | – |
| G-35 | **Repair or replace policy:** what is repaired, by whom, what is scrapped, how scrap is disposed of | Cost per episode depends on it | P1 | Ops | S | ₹ |
| G-36 | **What biomedical engineering will demand** (see G-R6) | They can block a device at the door | P0 | Ops | M | ₹ |
| G-37 | **Service promises:** response time for a dead unit, uptime of the dashboard, who the hospital calls | Needed in the pilot agreement | P1 | Lead | S | – |
| G-38 | **A named person at the hospital** who owns the pilot day to day (not the champion doctor) | Pilots die when the champion is on leave | P0 | Lead | S | – |
| G-39 | **Consumables:** the spirometer and mouthpiece are single-patient (B6-11). Who buys them, who throws them away, how | Bio-medical waste rules apply to the hospital; cost sits somewhere | P1 | Ops | S | ₹ |
| G-40 | **Staff time is not counted.** Minutes per patient for assign, teach, clean, chase | The pitch claims to save nurse time. It may add time | P1 | Clinical | S | – |

**G-R6: Accredited hospitals keep every piece of equipment on a register with a unique number, a maintenance plan and records. Loaned and demonstration equipment is usually tested on arrival.**
- Detail: NABH (India's hospital accreditation board) publishes a biomedical equipment checklist asking for: an inventory register with a unique numbering system; the maker's operating manual; a documented preventive-maintenance plan; breakdown and repair records; operator training records; a complaint register; condemnation (retirement) records; and an annual or comprehensive maintenance contract, or in-house engineers. A Dubai regulator's checklist adds that all equipment, including loaned and demonstration units, is safety-tested and calibrated on installation and carries an asset tag.
- Source: NABH checklist "CHECK 04.16" (snippet only, C; the file refused connection, S9) · Dubai Health Authority checklist (snippet only, C; foreign, comparison only).
- Status: **SINGLE SOURCE (snippet)**. The wording of the NABH 6th-edition standard (Jan 2025) was not read.
- What it means: bring to the first meeting: a serial-number list, a one-page user manual, a maintenance and calibration schedule (even "check against the printed marks monthly"), a cleaning instruction, and an electrical-safety statement for a battery unit at 5 V. Ask the biomedical engineer for their intake form before building the pilot kit.

---

## D. Software and data (outside the app and hardware files)

**Already covered, on paper only:** login, roles, hospital separation, audit log, backups, retention table, incident runbooks, security testing, model versions and drift (`FUTURE_ARCHITECTURE.md` §2, 3, 6, 8, 9; top-10 decisions in §13). **None is built** (`FEATURE_STATUS.md` §12). Known open holes are written as failing tests in `tests/test_critical.py`.

| ID | Gap | Why it matters | Sev | Owner | Effort | ₹ |
|---|---|---|---|---|---|---|
| G-41 | **No staff login at all.** Anyone with the web address can read every patient, phone number and family link (test at line 302) | A breach on day one of a pilot | P0 | Tech | M | – |
| G-42 | **The public repository documents our own open holes** (seven `xfail` tests name the file and function), and holds the full business research | An attacker's to-do list. Fix the holes, or make the repo private before real data | P0 | Tech + Lead | S | – |
| G-43 | **Call and message webhooks partly unprotected** (Exotel has no secret; a Twilio GET path skips the check) | A stranger can "press 1" for a patient and silence a reminder ladder | P0 | Tech | S | – |
| G-44 | **Red-flag and STOP words typed in English letters for Tamil and Malayalam are not understood** | A patient types "nenju vali" (chest pain) and nothing happens | P0 | Tech + native speakers | S | – |
| G-45 | **Database failure shows raw error text**, and a red-flag message could be lost | Safety message must survive an outage | P0 | Tech | S | – |
| G-46 | **Hosting is on free plans.** Render's free tier: sleeps after 15 minutes, may restart at any time, "do not use for production". Supabase free projects pause after a quiet week (G-R7) | Missed reminders and lost alerts | P0 | Tech | S | ₹ |
| G-47 | **App server is in Singapore**, database in Mumbai | Hospitals will ask for India-only. Move before real data | P0 | Tech | S | ₹ |
| G-48 | **No backup has ever been restored.** | An untested backup is a hope, not a backup | P0 | Tech | S | ₹ |
| G-49 | **No monitoring, no on-call.** If the alert path breaks at night nobody knows. A student team cannot staff 24×7 | Decide and state the service hours honestly; give the ward a paper fallback | P0 | Tech + Lead | M | ₹ |
| G-50 | **Breach duties not operational** (G-R8): 6 hours to CERT-In, 72 hours to the Data Protection Board from May 2027, plus the hospital under contract | No contact list, no template, no named person | P0 | Lead + Lawyer | S | – |
| G-51 | **Clock rules.** CERT-In asks systems to sync time with the government time servers or a traceable source (G-R8). Units with no network guess the time (`DEVICE_LIFECYCLE.md` risk 6) | A session credited to the wrong hour raises a false "missed" alert | P1 | Tech | S | – |
| G-52 | **Time zones.** Family members abroad are allowed; quiet hours and "today" must follow each person's own zone | A 3 am call to a son in Dubai | P1 | Tech | S | – |
| G-53 | **Penetration test (VAPT).** Planned, not booked. NHA requires a report from a CERT-In-listed auditor for national health-ID integration (snippet, C) | Hospitals ask for the report | P1 | Tech | S | ₹ |
| G-54 | **Record-keeping period is undefined** (G-R9). Our retention table says "hospital's period (?)" | We must keep what the hospital must keep, and delete the rest | P1 | Lawyer + Clinical | S | – |
| G-55 | **Patient data export and deletion on request** not built | Privacy-law right from May 2027; hospitals ask sooner | P1 | Tech | M | – |
| G-56 | **Integration with hospital systems.** No plan beyond "FHIR later" (G-R10) | Nurses will not open a second screen for long | P2 | Tech | L | ₹ |
| G-57 | **Multi-hospital separation** (hospital id on every table) not built | Decision 1 in the architecture file; cheap now, costly later | P1 | Tech | S | – |
| G-58 | **Status page and a way to tell wards about an outage** | Trust | P2 | Tech | S | – |
| G-59 | **Disaster recovery never rehearsed**; targets exist on paper only | – | P1 | Tech | S | ₹ |
| G-60 | **Single-vendor dependence** (table below) | One email from a vendor can stop the service | P1 | Tech + Lead | M | ₹ |
| G-61 | **Open-source licences:** no licence file in our own public repo; no list of the libraries we ship (SBOM) | By default a public repo with no licence means "all rights reserved", which is fine for ownership but should be a choice. Device rules want the list | P1 | Tech | S | – |
| G-62 | **AI model lifecycle:** 0 real breaths; the live server can retrain itself (`/api/train`); no frozen test set; no bias check by age, sex or lung size; no change log | The regulator's software guidance asks for all of it (#123); a small woman's "good" breath may be labelled "shallow" | P0 for the pilot protocol, P1 to build | Tech + Clinical | L | – |
| G-63 | **The language model's version can change under us.** The summary writer is a vendor model; vendors retire models | Wording changes with no review. Pin the version, keep the template as the default for clinical content | P1 | Tech | S | – |
| G-64 | **Patient names are still sent to the AI vendor** (`FEATURE_STATUS.md` §12 item 4) | Personal data leaving India with no contract | P0 | Tech | S | – |
| G-65 | **Internationalisation beyond voice:** dates, numbers, right-to-left Urdu, font support, text length in buttons | Broken screens in the languages we claim | P2 | Tech | M | – |
| G-66 | **No record of who changed a care plan or silenced an alert** | Disputes after an incident | P0 | Tech | M | – |

### Vendor dependence – what happens if each one changes

| Vendor | Used for | If price rises / policy changes / it shuts | Fallback today | Missing |
|---|---|---|---|---|
| Sarvam | Indian voices, speech-to-text, AI calls | Voice falls back to recorded clips and the browser voice; AI calls stop | 341 recorded clips; keypad calls via another provider | A second voice vendor tested once; a clause on notice of price changes |
| Supabase | Database | Paid plan needed anyway. Data is plain Postgres, so it can move | Local demo database (fake data only) | A tested export and restore into another Postgres host |
| Render | Web server | No India region (#W3) so we must leave it for real data anyway | None | Choose the Mumbai host now |
| Meta / WhatsApp (through Twilio or another partner) | Family and patient messages | Template rejected, number quality drops, health-content policy tightens, per-message price changes | SMS and voice call are designed, not live | A registered SMS route; never make WhatsApp the only path for a red flag |
| Anthropic | Evening summary text | Model retired or price change | Template text (works today with no key) | Version pin; a decision that templates are the regulated default |
| Twilio / Exotel | Calls | Indian calling rules changed in 2026 (B4-17) | Not live | An Indian telephony partner and registered sender IDs |
| GitHub, jsDelivr (3D library) | Code hosting, a script on the showroom page | Outage breaks the showroom only | – | Host the script ourselves for anything patient-facing |

**G-R7: Free hosting is not fit for patients, in the vendors' own words.**
- Detail: Render: a free web service sleeps after 15 minutes without traffic, takes about a minute to wake, "might restart at any time", and "Do not use them for production applications." Supabase: free projects are paused after low activity over 7 days; the page gives both "90 days" and "1 year" as the restore window; paid projects are never paused.
- Source: render.com/docs/free (S13, B) · supabase.com/docs/guides/platform/free-project-pausing (S12, B).
- Status: **CONFIRMED** (vendors' own pages).
- What it means: paid plans before any real patient. Prices are already in `FUTURE_ARCHITECTURE.md` §11 and W1.

**G-R8: The 6-hour rule is real, and it applies to us once we are a company.**
- Detail: CERT-In's Directions of 28 Apr 2022 apply to service providers, intermediaries, data centres, body corporates and government bodies; individuals are not covered. Listed incidents, including data breaches and unauthorised access, must be reported **within 6 hours of noticing or being told**; a first report can be partial. Logs of all systems must be kept for a rolling 180 days within India. Clocks must sync with the government's time servers (NIC or NPL) or a source traceable to them; cloud customers may use the cloud's own time service. Penalty under section 70B(7) of the IT Act: up to one year in prison or a fine up to ₹1 lakh or both. A later law (Jan Vishwas Act) is reported to have raised the maximum fine to ₹1 crore.
- Source: Nishith Desai Associates analysis of the official FAQs (S14, B) · ledger #194 (the Directions, A, known from search results) · Trilegal on the Jan Vishwas Act (snippet only, C).
- Status: 6 hours, 180 days, time sync: **CONFIRMED**. No exemption for small firms was mentioned: **NOT CONFIRMED either way**. The ₹1 crore figure: **NOT CONFIRMED**.
- What it means: one page with CERT-In's reporting address, the hospital's contact and a fill-in template. A named person. From May 2027 add the Data Protection Board within 72 hours (B4-13).

**G-R9: A doctor must keep inpatient records for 3 years; many hospitals keep them far longer. Our data must follow the hospital's rule.**
- Detail: The medical council's ethics regulations (2002) require records of indoor patients to be kept for 3 years from the start of treatment, and a copy given within 72 hours of a request. Hospital-quality guidance: outpatient records 2 years; records in a legal case until the case ends; one large public hospital keeps inpatient records 10 years; children's records until adulthood. No single national rule covers all hospitals.
- Source: consortium of accredited hospitals guidance and journal summaries (snippets only, C; the PDF was unreadable, S7).
- Status: **SINGLE SOURCE (snippets)**. Read the regulation text and ask each hospital's records officer.
- What it means: the contract must say the hospital is the record keeper and gets a full export; we keep our copy only as long as the contract says. Our "90 days for message content" needs the hospital's agreement.

**G-R10: No reliable ranking of Indian hospital software vendors was found.**
- Detail: One vendor (KareXpert) claims 300+ hospitals live on its hospital and medical-record software. A 2026 survey preprint says the FHIR data standard underpins the national health-ID programme but adoption elsewhere is "uneven and largely compliance-driven". Nothing reliable was found on other private vendors or on the government's eHospital system.
- Source: NABH software listing and a preprint (snippets only, C).
- Status: **NOT CONFIRMED**. HL7 and FHIR are the two common message formats for passing data between hospital systems; FHIR is the newer one.
- What it means: do not build integration for the pilot. Offer a printed A4 summary (already built) and a file export. Ask each hospital which system it runs; that list is the real market data.

**G-R11: Every Python library we ship has a permissive licence.**
- Detail: Read from the installed packages on 10 Oct 2026: FastAPI, Anthropic SDK, Twilio SDK, pytest, pydantic – MIT; uvicorn, python-dotenv, NumPy, pandas, scikit-learn, joblib, httpx, starlette, SciPy – BSD; tzdata, python-multipart – Apache-2.0; Pillow – MIT-CMU. The showroom uses three.js 0.169.0. The firmware names the Pololu VL53L0X/VL53L1X libraries.
- Source: local package metadata in `.venv` (primary, A). three.js and the Pololu libraries were **not** checked this round.
- Status: **CONFIRMED** for the Python list. **NOT CONFIRMED** for the firmware libraries; the sensor maker's own code inside them carries its own terms.
- What it means: obligations are light: keep the copyright notices and ship a list of third-party licences. Check the two firmware libraries before making units. Generate a software bill of materials (a machine-readable list of every library and version) on each release; `requirements.txt` already pins exact versions.

---

## E. Quality and regulatory housekeeping (beyond the licence path)

**Already covered:** the licence route, fees, standards list, labelling and unique device identifier in outline (`04_legal_and_regulatory.md` B4-1 to B4-12, B4-5); the four standards named (`FUTURE_ARCHITECTURE.md` §10). **Missing: any actual document.**

A quality management system (QMS) is the set of written habits a device maker follows so that it can show how each unit was designed, built, changed and supported. It does not need software or a consultant to start. It needs a shared folder and discipline.

| ID | Item | Lightweight version to start this month | Sev | Owner | Effort | ₹ |
|---|---|---|---|---|---|---|
| G-67 | **Document control** | One folder; every document has a number, version, date, author, approver. Git already does most of this for code and docs | P1 | Lead | S | – |
| G-68 | **Design history file** (the story of every design decision) | The repo's `docs/` is 80% of it. Add: intended-use statement, user needs, requirements, tests that prove each requirement | P1 | Tech | M | – |
| G-69 | **Risk management file** (same as G-4) | A spreadsheet: hazard, cause, harm, likelihood, severity, control, check | P0 | Clinical + Reg | M | – |
| G-70 | **Complaint handling** | One form, one log, one owner, a 2-day first response; feeds G-5 | P0 | Ops | S | – |
| G-71 | **Supplier control** | A list of every supplier (sensor, board, case, cloud, voice) with what we check on arrival | P1 | Ops | S | – |
| G-72 | **Traceability by serial number** | Each unit: serial, build date, parts batch, firmware version, calibration result, every patient episode (no names on the unit) | P0 | Ops + Tech | S | – |
| G-73 | **Post-market surveillance** (watching the product in use) | Monthly review of complaints, failures, alert counts, model labels | P1 | Clinical | S | – |
| G-74 | **Recall / field fix procedure** | One page: how to find every unit of a batch, tell the hospital, pull or fix it; links to the 15-day duty (G-R4) | P1 | Lead + Reg | S | – |
| G-75 | **Usability file** | Notes and videos from every user test, tasks tried, errors seen. Start with the three interviews | P0 for the pilot | Design | M | – |
| G-76 | **Cybersecurity file** | Threat table exists (§9.1 of the architecture file). Add test evidence and the VAPT report | P1 | Tech | S | ₹ |
| G-77 | **Software bill of materials** | Auto-generate per release (G-R11) | P1 | Tech | S | – |
| G-78 | **Labelling and instructions for use**, in each language we support | The label rules are in B4-5, B6-13. Nobody has drafted the leaflet. It must carry the contraindications (G-1), cleaning, battery and disposal text | P0 for the pilot (draft), P1 final | Clinical + Design | M | ₹ (translation, print) |
| G-79 | **Shelf life and battery ageing** | Lithium cells fade with charge cycles and heat. State a service life and a battery-replacement rule; record cycles per unit. No figure measured | P1 | Hardware | M | ₹ |
| G-80 | **Packaging and transport tests** | Drop, vibration, heat in a courier van; lithium cells have their own transport test and labelling rules. Not researched here; flag to the hardware file | P1 | Hardware | M | ₹ |
| G-81 | **Calibration record per spirometer model** and a re-check interval | The reading in mL is only as good as the table. No table exists (`FEATURE_STATUS.md` §1) | P0 | Hardware + Clinical | M | – |
| G-82 | **Training records for our own team** (who is allowed to release software, who signs clinical text) | Auditors ask "who approved this and were they qualified?" | P2 | Lead | S | – |

No new web research was needed for this section; the rules are in file 04. What is new is the finding that **none of these has a first draft**, and that most cost time, not money. Prices for a certification audit and a consultant remain unknown (B4, open question 8).

---

## F. Company and people

**Already covered:** company set-up steps and DPIIT recognition (B3-15); grants and the ₹10 lakh ordering trap (B3-7 to B3-10); patent, design and trademark in outline (B4-21); "check the college's and hackathon's IP rules" (B4 open question 13). **Missing: every agreement between the people.**

| ID | Gap | Why it matters | Sev | Owner | Effort | ₹ |
|---|---|---|---|---|---|---|
| G-83 | **No founders' agreement.** Shares, roles, who decides, what happens when one leaves | The usual cause of early start-up failure; grants and incubators ask for it | P1 (sign this month) | Lead | S | ₹ (lawyer) |
| G-84 | **No vesting.** Shares earned over time, not given on day one (G-R12) | The team are students; some will take jobs. Without vesting, a founder who leaves in month 3 keeps a full share | P1 | Lead | S | – |
| G-85 | **Time commitment alongside studies** not written down; exams and placements are not on any plan | The pilot will clash with an exam month | P1 | Lead | S | – |
| G-86 | **Who owns the code today?** All commits are under one personal GitHub account; no company exists; no assignment from the other members | The company must own it before any grant or deal. Each member signs a short assignment when the company is formed | P1 | Lead + Lawyer | S | ₹ |
| G-87 | **AI-written code.** Most of the code was written with an AI coding tool (G-R13) | Ownership is likely fine but untested in Indian courts; investors ask | P2 | Lawyer | S | – |
| G-88 | **College IP policy unread** | Some colleges claim student work done with college resources; a no-objection letter is needed for NIDHI-PRAYAS (B3-7) | P1 | Lead | S | – |
| G-89 | **Hackathon IP terms unread.** We searched; the organisers' terms are not public (G-R14) | A clause could give the organiser a licence or more | P1 (ask this week) | Lead | S | – |
| G-90 | **No medical co-founder or clinical lead, no advisor agreements** (advisors usually get a small share or a fee, in writing) | Same as G-9 | P0 | Lead | M | ₹ |
| G-91 | **Bookkeeping, bank account, PAN/TAN, tax registrations** (G-R15) | Grants are paid to a bank account in the applicant's or company's name; mixing personal money is a classic mess | P1 | CA | S | ₹ |
| G-92 | **Yearly compliance calendar for a private limited company** (G-R15) | Late filing costs ₹100 a day per form (snippet); directors can be disqualified | P1 once incorporated | CA | S | ₹ |
| G-93 | **Insurance:** study insurance (via the hospital, B5-6), product liability, cyber, and ordinary cover for units in transit | No Indian price found (B4-19). The pilot cannot start without the first | P0 (study), P1 (others) | Lead | M | ₹ |
| G-94 | **Contracts for helpers:** interns, freelance designers, a 3D-print vendor: each needs an IP-assignment and confidentiality line | Otherwise they own what they made | P1 | Lawyer | S | ₹ |
| G-95 | **Non-disclosure agreements** with hospitals and manufacturers | Our public repo already discloses most of the idea, which weakens any later patent or secrecy claim (see also B4-21: public display before a design filing) | P1 | Lawyer | S | – |
| G-96 | **Private material in a public repo.** Founder note 23 says the team's private WaBI details must stay private; the repo also has an untracked `infffff/` folder | One wrong `git add` publishes it | P0 (hygiene) | Tech | S | – |

**G-R12: Four years with a one-year pause is the usual founder vesting pattern in India. It is a contract habit, not a law.**
- Detail: 25% of a founder's shares become theirs after one year (the "cliff"); the rest in monthly or quarterly steps over three more years. It only works if the agreement gives the company or the other founders the right to buy back unvested shares at cost, and they use it.
- Source: EquityList and Treelife explainers (snippets only, C).
- Status: **SINGLE SOURCE (snippets)**; common practice.
- What it means: a one-page agreement now (shares, roles, vesting, IP assignment, what happens on leaving), replaced by a proper one at incorporation.

**G-R13: Indian law names a human as the author of computer-generated work; the more human choice, the safer the claim.**
- Detail: Section 2(d)(vi) of the Copyright Act 1957 says that for a computer-generated work the author is "the person who causes the work to be created". An AI cannot be an author. Protection is strongest where a person made real creative choices; output from a short prompt alone may get no protection. Recommended practice: set ownership in agreements with staff, vendors and tool providers, and keep records of human contribution. The Registrar of Copyrights applied the same reading on 31 Aug 2026 in an order about the "DABUS" system; the government published a consultation paper on AI and copyright in Dec 2025.
- Source: S.S. Rana & Co. article, 31 Aug 2026 (S10, B) · Intepat on the Registrar's order (snippet only, C).
- Status: statute wording **CONFIRMED at B**; how courts treat AI-written *code*: **NOT CONFIRMED** (no ruling found).
- What it means: keep the Git history (it shows human direction, review and edits), keep `docs/` as the record of design choices, read the coding tool's terms on output ownership, and have each member assign their work to the company. Low risk, cheap to tidy.

**G-R14: The hackathon's ownership terms could not be found online.**
- Detail: Two searches found no terms for the Social Impact Hackathon 2026. Hackathon terms vary widely elsewhere: some leave ownership with teams, some take a licence to show the work, a few claim it.
- Source: searches only; nothing opened. General examples: snippets, C.
- Status: **NOT CONFIRMED.**
- What it means: before submitting on 11 Oct, read the form's terms and email the organisers one question: "Do teams keep all rights in their submission?" Save the reply.

**G-R15: Tax and company housekeeping thresholds (second-hand; a CA must confirm).**
- Detail: GST registration is needed above ₹40 lakh a year of turnover for goods and ₹20 lakh for services in most states (lower in some); it is compulsory at any turnover for sales of goods across state lines. Tax deducted at source: a hospital paying us may deduct 1–2% on contracts above ₹30,000 a bill or ₹1 lakh a year, and 2–10% on technical or professional fees above ₹50,000 a year, so we receive less cash than we invoice and claim it back. The Income-tax Act 2025 renumbers these sections. A private limited company files: a start-of-business declaration within 180 days (INC-20A); auditor appointment (ADT-1); accounts within 30 days of the annual meeting (AOC-4); annual return within 60 days (MGT-7A for small companies); director identity checks (date disputed between sources); an income-tax return by 31 Oct if audited.
- Source: tax and compliance explainers (snippets only, C).
- Status: **SINGLE SOURCE (snippets).** Do not rely on any figure without a CA.
- What it means: a lent unit plus a per-patient fee will likely cross state lines early, so plan for GST registration from the first paid invoice. Budget a CA retainer (price not found; ask two).

---

## G. Commercial details nobody has written down

**Already covered:** pricing options and the ₹500 per episode idea (B2-19, B3-6, B6-4 to B6-6); deposit and rental examples (B6-8, B6-9); a one-page pilot agreement is on the 90-day list but not drafted; what a hospital asks for in a data processing agreement (B4-16); late payment by government buyers and the 45-day rule for small suppliers (B2-4, B2-4a); GST on devices is 5% since 22 Sep 2025 (B6-2).

| ID | Gap | Note | Sev | Owner | Effort | ₹ |
|---|---|---|---|---|---|---|
| G-97 | **Pilot agreement** (free pilot): who owns the units and the data, who may publish, insurance, who reports harm, end date, what happens to patients after | Needed before the ethics submission | P0 | Lead + Lawyer | S | ₹ |
| G-98 | **Data processing agreement** | Says the hospital controls the data and we process it for them (our reading in `FUTURE_ARCHITECTURE.md` §3.3) | P0 | Lawyer | S | ₹ |
| G-99 | **Master service agreement and service-level agreement** for a paid customer | Uptime, support hours, liability cap, exit and data return | P1 | Lawyer | M | ₹ |
| G-100 | **Price list and quote template** | One page: per-episode fee, deposit per unit, lost-unit charge, what is included | P1 | Lead | S | – |
| G-101 | **Invoicing and collection:** how to bill per episode (monthly count from the system, signed by the ward), credit period, late fee | Private-hospital credit periods are not published (B2-3). Register as a micro enterprise (Udyam) to use the 45-day rule (B2-4a) | P1 | CA | S | – |
| G-102 | **GST on a device-plus-service bundle** (G-R16) | 5% on a device, a different rate on a software service; a bundle can be taxed as one or the other | P1 | CA | S | – |
| G-103 | **Deposits and loss charges** | Whether a hospital may take a deposit from a patient, and whether that is allowed inside a study, is an open question (B6) | P1 | Lawyer | S | – |
| G-104 | **Warranty terms** | Period, what is covered, battery excluded or not, turnaround | P1 | Ops | S | ₹ |
| G-105 | **Referral or reseller agreement** | For a distributor or a spirometer maker (B2-21). Any seller of a device needs registration (B2-10a) | P2 | Lawyer | M | ₹ |
| G-106 | **Brand name check** (G-R17) | Not done | P1 (this month) | Lead | S | ₹ |
| G-107 | **Website and sales deck** | The live demo is not a website. A hospital searches the name first | P1 | Design | M | ₹ |
| G-108 | **Case-study and logo permission** | A clause in the pilot agreement: may we name the hospital, quote results, use photos? Patient photos need their own consent | P1 | Lawyer | S | – |
| G-109 | **Advertising rules applied to our own materials** | "Prevents pneumonia" is an offence (B4-20). Nobody has reviewed the showroom, videos and deck against the never-say list | P0 for anything shown to a hospital | Lead | S | – |

**G-R16: A bundle is taxed at the rate of its main part.**
- Detail: Under section 8 of the GST law, a "composite supply" (things naturally sold together where one is the main item) is taxed at the main item's rate. A "mixed supply" (unrelated things sold for one price) is taxed at the highest rate among them.
- Source: tax explainers quoting sections 2(30), 2(90) and 8 of the CGST Act (snippets only, C).
- Status: **SINGLE SOURCE (snippets).**
- What it means: whether "a lent unit plus coaching software per patient" is a supply of goods (5%), a service at a higher rate, or a rental, changes our margin. One hour with a CA before the first quote. The right code for the base unit is still unknown (B6 open question).

**G-R17: Quick public checks found no one else using "SpiroBuddy". The trademark register still needs a person.**
- Detail (all checked 10 Oct 2026): a web search for "SpiroBuddy" / "Spiro Buddy" returned no product, company or trademark; Google Play's search for "spirobuddy" returned "No results"; none of spirobuddy.com, .in, .co.in, .app, .health has a DNS record (a sign, not proof, that they are unregistered). Similar registered or pending names abroad in the same field: SPIRO, SPIRODOC, SPIROHOME (US).
- Source: Google Play search page (S16, B) · DNS look-ups run locally · search results (snippets, C).
- Status: **NOT CONFIRMED** as free. The Indian register cannot be searched by a program (it has a CAPTCHA).
- How to check properly (30 minutes, a person): (1) India's trademark public search at ipindia.gov.in → "Trade Marks" → "Public Search": search SPIROBUDDY and "SPIRO" as a prefix in class 10 (medical apparatus), class 9 (software and apps) and class 44 (medical services). (2) A domain registrar for the five domains. (3) Apple's App Store search. (4) The company-name check on the MCA site before incorporation. (5) Instagram, LinkedIn, X handles. "Spiro" is a common, descriptive prefix in this field, so expect a narrow right. File the trademark before the name is used commercially (B4-21).

---

## H. Evidence, impact and ethics

**Already covered:** the evidence ladder (bench → volunteers → 30–50 patients → controlled study) and sample sizes (B5-20); consent rules with a literate witness, vulnerable groups, insurance, the trial register (B5-4 to B5-8); the AI guideline gap (the model has seen no real breaths) (B5-9); the honest limits of the evidence for the exercise itself (`RESEARCH_REPORT.md` §2.4); e-waste duties in outline (B4-12, B6-15).

| ID | Gap | What to write or decide | Sev | Owner | Effort |
|---|---|---|---|---|---|
| G-110 | **No monitoring-and-evaluation plan for the social-impact claim** | A one-page theory of change: unit + coach → more sessions done properly → (assumed) fewer lung problems → fewer return visits. Indicators we can measure: sessions per day, share of good breaths, days used, nurse minutes, alerts acted on. Indicators we cannot claim yet: pneumonia, readmission. Baseline: two weeks of the ward's usual practice before the units arrive. Who measures: the hospital's team, not us | P1 | Clinical + Lead | S |
| G-111 | **Equity: does it widen the gap?** | It needs a phone, a charger and a hospital that lends it. Only 41% of older Indians own a smartphone and 24% of older women can read (repo). Record phone ownership, sex, language and income band for everyone screened, and report who was left out. Offer the hub-phone or no-phone mode first to those without | P1 | Clinical | S |
| G-112 | **Consent that an elderly, non-reading patient truly understands** | Use "teach-back": the patient says in their own words what the unit does, who sees the data and how to stop. Record that it was done. The read-aloud consent exists in code; the understanding check does not | P0 | Clinical | S |
| G-113 | **The family update as surveillance or pressure** | The patient chooses who gets updates, sees exactly what they see, and can stop it in one word without telling the family. "Send a cheer" yes; "you missed three" to a son, only if the patient agreed. An elder dependent on the family may not feel free to refuse: ask them alone | P0 | Clinical + Tech | S |
| G-114 | **Training the model on a patient's breaths** | A separate yes/no, not bundled with care (designed in `FUTURE_ARCHITECTURE.md` §3.7, not built). Say what cannot be undone after training | P0 | Tech + Clinical | S |
| G-115 | **Withdrawing from a study** | One word, any language; what happens to data already collected; the unit is collected without argument | P0 | Clinical | S |
| G-116 | **After the pilot ends** | Do patients keep the unit until they finish? Does the ward keep the system? Ethics guidance expects a plan for benefit after a study (B5-4). Decide and write it into G-97 | P0 | Lead | S |
| G-117 | **Staff as subjects.** Nurses' response times are being measured | Tell them; do not let the dashboard become a tool to rank nurses | P1 | Clinical | S |
| G-118 | **Environmental footprint** | Per unit: one lithium cell, one circuit board, a plastic case; per patient: one single-use spirometer and mouthpiece (already the case without us). Reuse lowers our footprint per patient; a take-back route and a battery-disposal instruction are missing. Producer duties under the e-waste rules attach when we sell under our own brand (B6-15) | P2 | Ops | S |
| G-119 | **The evidence for the exercise itself may weaken** | Our measurable claim is adherence and technique. Keep the product useful for supervised breathing exercises in lung rehabilitation, where the evidence base is different (`RESEARCH_REPORT.md` §2.8) | P1 | Lead | – |
| G-120 | **No pre-registered question.** | State before the pilot what result would make us stop | P1 | Clinical | S |

---

## I. Risk register – top 25

Likelihood and impact: H = high, M = medium, L = low. Team judgement, not measured.

| # | Risk | Type | L | I | Early warning sign | Mitigation |
|---|---|---|---|---|---|---|
| 1 | **The laser cannot read the disc through the real tube** (curved clear plastic, closed floor, beam wider than the bore) | Technical | M | H | Jumpy or stuck readings in the first bench hour | Bench-test this week with one spirometer and one sensor; keep the camera method as plan B; do not build 10 units first |
| 2 | **No clinician joins**, so nothing clinical is signed off | Team | M | H | Three interviews done and nobody offers to help | Ask each interviewee directly; approach the college's nearest teaching hospital; offer authorship on the pilot paper |
| 3 | **A patient is harmed** (faints, falls, strains a wound, ignores symptoms because the app showed green) | Clinical | L | H | Dizziness or pain reports in volunteer tests | G-1, G-3, G-11, G-12; clinician decides enrolment; study insurance; adverse-event page |
| 4 | **A pilot needs CDSCO permission and we start without it** | Regulatory | M | H | Ethics committee asks "is the device licensed?" | Hospital-led study; written answer from a consultant or MedTech Mitra first (B5-10) |
| 5 | **Hospitals will not pay** | Commercial | H | H | "Send a proposal" with no budget holder named | Ask price in every interview; test ₹200 / ₹500 / ₹1,000; line up donor money for public hospitals (B2-12) |
| 6 | **The team graduates and disperses** | Team | H | H | Missed weekly meeting; placement season | Founders' agreement with vesting; one person full-time by a set date; a grant that pays a stipend |
| 7 | **Units do not come back from homes** | Operational | M | H | First five returns take more than two weeks | Return at the follow-up visit; deposit or sign-out; overdue list; measure in the pilot |
| 8 | **Data breach** (no login today; open holes published) | Technical | H (if launched as is) | H | Any real data entered before G-41 to G-45 are closed | Close P0 items; private repo; penetration test; breach page |
| 9 | **The spirometer maker adds a sensor itself** | Commercial | M | H | A "smart" model in a catalogue or tender | Partner early (B2-21); our value is the coach, languages and dashboard, which work with any maker's unit |
| 10 | **A phone-camera app makes the base unit unnecessary** | Commercial | M | H | A camera-only app with hospital users | Build the camera input ourselves as a low-cost tier; the dashboard is the product |
| 11 | **InSee or another funded foreign product enters India** | Commercial | L | M | An Indian distributor or CDSCO import licence | Price, Indian languages, home use, Indian spirometer models |
| 12 | **Evidence for the exercise weakens further**; a guideline drops it | Clinical | M | H | A new review or society statement | Position as "breathing-exercise coaching and adherence", usable in lung rehabilitation |
| 13 | **A key vendor changes terms** (voice, WhatsApp, hosting, AI) | Technical | H | M | Price or policy email; template rejections | Fallbacks in the vendor table; never one path for a red flag |
| 14 | **Nurses ignore the dashboard** | Operational | H | H | Alerts unacknowledged for hours in week 1 | Agree thresholds with the ward; daily list on paper or WhatsApp to the charge nurse; count alerts per shift |
| 15 | **Elderly patients cannot use it alone** | Clinical | M | H | More than 1 in 3 need help in a first test | Test with 5 older people now; carer-assisted mode; simplify to one button |
| 16 | **The model is wrong on real breaths** (trained on pretend ones) | Technical | H | M | Labels disagree with a physiotherapist on the first 50 breaths | Rules first, model in shadow; collect labelled real breaths in the volunteer stage |
| 17 | **Wrong patient's data on a re-issued unit** | Clinical | M | H | A session appears before a unit is assigned | Assignment required; quarantine unassigned readings (`DEVICE_LIFECYCLE.md` §5.5); serial-number log |
| 18 | **Infection spread by a shared unit** | Clinical | L | H | Infection-control nurse objects to the cleaning step | Unit never touches the mouth; wipe-clean case; cleaning log; their sign-off before the pilot |
| 19 | **Money runs out before evidence** | Financial | H | H | No grant submitted by month 3 | Apply to NIDHI-PRAYAS and the state idea grant now (B3-7, B3-8); keep the pilot tiny |
| 20 | **A founder dispute or unclear IP ownership blocks a grant** | Team | M | H | Disagreement over who is "CEO" or who owns the repo | G-83 to G-89 this month |
| 21 | **We say something we must not** ("prevents pneumonia", "approved") | Reputational | M | H | A slide or video with a banned phrase | One person checks every public item against the never-say list (G-109) |
| 22 | **Automated calls or messages breach telecom or WhatsApp rules** | Regulatory | M | M | Number flagged or blocked | Indian telephony partner, registered sender, consent records (B4-17) |
| 23 | **Outage during a pilot with no one on call** | Operational | H | M | First alert missed overnight | Paid hosting; a test alert every few minutes; state service hours; paper fallback on the ward |
| 24 | **Battery fault or overheating in a home** | Technical | L | H | A warm unit on charge; a swollen cell | Certified cell and charger (B4-10); protection circuit; charging instruction; hardware file owns the detail |
| 25 | **Family pressure or loss of dignity causes a patient to drop out or complain** | Reputational | M | M | A patient asks to stop "because my son scolds me" | G-113; patient controls the updates; ask the patient alone |

---

## J. Assumptions register – numbers nobody has measured

| # | Assumption in the plans | Where it is used | Cheapest test | Time |
|---|---|---|---|---|
| 1 | **The sensor reads the disc through the tube to within about 100 mL** | Everything | One sensor, one spirometer, a syringe or the printed marks; 20 readings per mark | 1 day once parts arrive |
| 2 | **Older patients can use it without help** | Product, pitch | Five people aged 60+ (relatives), simulator or prototype, watch silently, count where they get stuck | 1 week |
| 3 | **A hospital will pay about ₹500 per patient** (or ₹200, or ₹1,000) | Unit economics | Ask three prices in each of 10 interviews; ask "who signs, from which budget" | 2–3 weeks |
| 4 | **10–30% of major operations come with a spirometer** | Market size | Ask a ward to tally for two weeks; ask one distributor how many they sell a month | 2 weeks |
| 5 | **A unit is reused 10 (or 20) times** | Cost per episode | Life test: charge-discharge and 200 clean-and-wipe cycles on two units; then count in the pilot | 2 weeks bench; 3 months pilot |
| 6 | **Units come back** (loss rate assumed low) | Cost per episode | Lend five dummy units for two weeks with a sign-out sheet; count returns and days late | 3 weeks |
| 7 | **Nurses will open the dashboard and act** | Value to the hospital | Paper version first: a daily one-page list to one charge nurse for a week; ask what she did with it | 1 week |
| 8 | **Patients do more sessions with the coach than without** | The whole claim | Healthy volunteers or relatives: one week plain spirometer with a tally sheet, one week with the coach | 2 weeks |
| 9 | **Families want the update and patients accept it** | Family feature | Ask in interviews, patient and family separately | 2 weeks |
| 10 | **The breath model works on real breaths** | Coaching quality | 200 real breaths from 10 volunteers, labelled by a physiotherapist; compare | 1 week after hardware |
| 11 | **A unit costs about ₹1,500 to make** | Pricing | Order parts for 5; get one written quote for 100 boards and cases | 2–3 weeks |
| 12 | **Server and messaging cost about ₹318–505 per episode** | Pricing | Run the live system with 10 simulated patients for 14 days on paid plans; read the bills | 2 weeks |
| 13 | **Cleaning takes a nurse a minute or two** | Hospital acceptance | Time it with a stopwatch on a dummy unit, with the hospital's own wipes | 1 hour |
| 14 | **The battery lasts through a typical episode between charges** | Home use | Bench test at 14 sessions a day | 1 week after hardware |
| 15 | **Patients go home with a working phone and mobile data** | Home model | Ask 20 patients at discharge (through a nurse) | 1 week |
| 16 | **The spoken lines are understood by older listeners in each language** | Safety | One older native speaker per language listens to all 21 lines and repeats back the meaning | 1 week |
| 17 | **Voice reminders and calls change behaviour** | Reminder ladder | Count sessions in the hour after each kind of nudge in the pilot | Pilot |
| 18 | **A free pilot needs only an ethics committee** | Timeline | One written question to MedTech Mitra or a consultant | 2–4 weeks |
| 19 | **The base fits every common Indian spirometer** | Market | Buy three brands; measure | 1 week |
| 20 | **Hospitals will lend equipment to go home** | Model B | Ask the nursing head and the biomedical engineer in interviews | 2 weeks |

---

## The 15 biggest gaps, ranked

| # | Gap | Why it matters | Stage it blocks | Owner | Effort |
|---|---|---|---|---|---|
| 1 | No clinical lead or advisor (G-9, G-90) | Nothing clinical can be signed off | Any real patient | Lead | S to find, ongoing |
| 2 | No contraindication list or screening (G-1, G-17) | Coaching the wrong patient | Any real patient | Clinical | S |
| 3 | Sensor never tested on a real tube (J-1) | The product may not work as designed | Everything | Hardware | S |
| 4 | No target-volume rule (G-2) | Wrong goals, false alerts, strain | Any real patient | Clinical + Tech | M |
| 5 | No rest, dizziness, pain or "stop" behaviour (G-3, G-11) | Fainting and falls | Any real patient | Clinical + Tech | S |
| 6 | No login; open security holes published (G-41 to G-45) | Breach on day one | Any real patient | Tech | M |
| 7 | Free hosting, server outside India, no restore test, no monitoring (G-46 to G-49) | Lost alerts, lost data | Any real patient | Tech | S–M |
| 8 | No risk file, complaint log, adverse-event page, serial tracking (G-4, G-5, G-70, G-72) | Ethics committee, regulator, and basic safety | Any real patient | Clinical + Ops | M |
| 9 | Pilot permission question unanswered (risk 4; B5-10) | Could make the pilot unlawful | Any real patient | Reg | S (one question) |
| 10 | No founders' agreement, vesting or IP assignment; college and hackathon terms unread (G-83 to G-89) | Team break-up, blocked grants | Paid pilot (do now) | Lead | S |
| 11 | Operations undefined: training, helpline, returns, cleaning log, biomedical intake (G-28 to G-36) | The pilot fails in week one for dull reasons | Any real patient | Ops | M |
| 12 | Consent understanding, family-update control, model-training consent, after-pilot plan (G-112 to G-116) | Ethics approval and patient dignity | Any real patient | Clinical | S |
| 13 | Model has 0 real breaths, self-retrains on the live server, no bias check (G-62) | Wrong labels; regulator's AI questions | Paid pilot | Tech + Clinical | L |
| 14 | Instructions for use, labels, quick-start card and video in each language, clinically signed (G-8, G-29, G-78) | A device with no leaflet cannot go home | Any real patient | Clinical + Design | M |
| 15 | No contracts, price list, GST position or brand check (G-97 to G-106) | Cannot take money | Paid pilot | Lead + Lawyer + CA | M |

---

## "Do before any real patient" checklist

**People and permission**
- [ ] A named clinician agrees in writing to be clinical lead or lead investigator.
- [ ] Written answer on whether the pilot needs CDSCO permission.
- [ ] Ethics committee approval; study insurance in place through the host hospital.
- [ ] Pilot agreement and data processing agreement signed.

**Clinical**
- [ ] Contraindication list and enrolment form signed by the clinician; "adults only" stated.
- [ ] Target-volume rule and the allowed range for breaths per session and sessions per day.
- [ ] Rest between breaths, "feeling dizzy?" and "stop for today" behaviour built and tested.
- [ ] Every spoken line checked by a native speaker and signed by the clinician, per language used.
- [ ] Risk file, complaint form, adverse-event page with names and phone numbers.
- [ ] Alert thresholds agreed with the ward; a paper fallback for outages.
- [ ] Failure behaviour: if anything stops, the patient hears or sees "carry on with your spirometer".

**Consent and dignity**
- [ ] Consent with a teach-back check and a literate witness; separate yes/no for model training and for family updates.
- [ ] Withdrawal in one word; a written plan for what patients and the ward keep after the pilot.

**Device**
- [ ] Bench accuracy measured against the printed marks; calibration table per spirometer model.
- [ ] Serial number, asset tag, cleaning instruction and "clean" tag on every unit; stock list.
- [ ] Biomedical engineering and infection control have seen the unit and said yes.
- [ ] Battery and charger checks (hardware file).

**Software and data**
- [ ] Staff login, roles and an audit record; hospital id on every table.
- [ ] All seven known open holes closed (`tests/test_critical.py` `xfail` list); repository private or scrubbed.
- [ ] Paid hosting in Mumbai for both server and database; one backup restored as a test.
- [ ] A check that raises a test alert every few minutes and tells someone when it fails.
- [ ] No patient names sent to any AI vendor; live retraining switched off; model and rules version stamped on each breath.
- [ ] Breach page: who reports to CERT-In within 6 hours, and to the hospital.
- [ ] Red-flag and STOP words in English letters for every language used.

**Operations**
- [ ] Nurse training done and recorded; quick-start card and video; helpline number, hours and languages.
- [ ] Spare units on the ward; a return route; a named pilot coordinator at the hospital.

---

## "Decide this month" list for the founders

1. **Who is in, for how long, and for what share?** Sign a one-page founders' agreement with vesting.
2. **Who is the clinical lead?** Name three people to ask this week.
3. **Is the repository public or private** from now on? (Founder note 23 and G-42 both say: private, or scrub it.)
4. **Adults only, and which patients are excluded** from the first pilot (children, tracheostomy, facial weakness, dementia without a carer)?
5. **Which state and which first hospital?** (Still open in the founder notes.)
6. **Lend or sell for the pilot?** (File 06 recommends lend. Confirm.)
7. **What do we promise about hours?** Daytime service with a paper fallback, or more?
8. **Is the template or the AI the default writer** of anything a patient or family reads?
9. **The name:** run the trademark and domain checks, then keep "SpiroBuddy" or change it before any printing.
10. **Which one person goes full-time first, and from what money?**
11. **What result would make us stop or change direction?** (Write it before the bench test.)
12. **Ask the college and the hackathon organisers the ownership question** and file the answers.

---

## "Hand to the costs file" list

Sourced prices are given where one was found. Everything else is "get a quote".

| Item | From | Price found | Source and grade |
|---|---|---|---|
| Penetration test (VAPT) of the web app | G-53 | about ₹40,000–₹3,50,000 depending on scope | vendor blogs, snippets only, C |
| Paid hosting (server in Mumbai) and paid database with point-in-time recovery | G-46 to G-48 | database plan US$25 a month; recovery add-on from US$100 a month | `FUTURE_ARCHITECTURE.md` W1 (search results) |
| Monitoring and alerting tools | G-49 | not found | – |
| Regulatory consultant (one question, then a retainer) | risk 4 | not found | B4 open question 8 |
| Lawyer: founders' agreement, pilot agreement, data processing agreement, later master and service-level agreements, NDAs, intern contracts | G-83, G-94, G-97 to G-99 | not found | – |
| Chartered accountant: set-up, bookkeeping, GST, yearly filings | G-91, G-92, G-102 | not found; late filing ₹100 a day per form | snippet, C |
| Company incorporation and stamp duty | G-91 | see B3-15 | file 03 |
| Trademark filing (3 classes), domains | G-106 | see B4-21 for the trademark fee; domains not priced | file 04 |
| Study insurance; product liability; cyber; transit cover | G-93 | not found (no Indian insurer publishes one) | B4-19 |
| Clinical lead or advisor (fee or share) | G-90 | not found | – |
| Translation and clinical review of instructions and voice lines, per language | G-8, G-78 | not found | – |
| Printing: quick-start cards, leaflets, labels, asset tags, "clean" tags | G-29, G-33, G-78 | not found | – |
| Training video production | G-29 | team time | – |
| Helpline: a number and someone's time | G-30 | not found | – |
| Spare units (suggest 20% extra) and replacement batteries | G-31, G-79 | unit cost in B6-1 | file 06 |
| Returns: courier or staff travel; cleaning wipes | G-32, G-33 | not found | – |
| Hub phones if the hospital will not lend one | G-26 | see `DEVICE_LIFECYCLE.md` | – |
| Three brands of spirometer for fit tests; bench-test kit | J-1, J-19 | spirometers about ₹200–₹1,000 each | `RESEARCH_REPORT.md` §4.1 |
| Packaging, drop and transport tests; battery transport compliance | G-80 | not found | hardware file |
| Quality-system certification audit, later | E | not found | B4 open question 8 |
| Ethics committee fee; trial registration (free) | checklist | fee not found; registration free | B5-8 |
| Website | G-107 | not found | – |
| Tax deducted at source by paying hospitals (cash-flow effect, 1–10%) | G-R15 | thresholds ₹30,000 / ₹1 lakh / ₹50,000 | snippets, C |
| Time of the team (the largest cost; unpaid today) | all | – | – |

---

## What we could not find (and who can answer)

- The full text of the AARC guideline's contraindication and hazard sections (journal pages refused us). **A person with a browser, 10 minutes.**
- Indian reference values for inspiratory capacity. **A chest physician or respiratory physiologist.**
- Coughing blood and "unstable patient" as listed reasons not to do this exercise. **The clinical lead.**
- The NABH standard's exact words on loaned equipment and home-returned devices. **A hospital quality manager.**
- Which hospital software each target hospital runs. **Ask in interviews.**
- The hackathon's ownership terms and the college's IP policy. **The organisers; the college.**
- Whether CERT-In's rules exempt very small firms; the current maximum fine. **A lawyer.**
- Prices: consultant, lawyer, CA, insurance, certification audit, translation. **Quotes.**
- Hours of electricity supply in patients' homes; phone and data access at discharge. **Twenty patients, through a nurse.**

---

## Sources opened this round

"Opened" means we fetched the page. Nine of nineteen gave nothing readable; they are listed so nobody tries them again the same way.

| # | URL | Title | Publisher | Grade | Used in |
|---|---|---|---|---|---|
| S1 | https://journals.sagepub.com/doi/10.4187/respcare.01471 | Incentive Spirometry: 2011 (AARC guideline) | Respiratory Care / SAGE | – | Refused (HTTP 403). Search snippet used in G-R1, grade C |
| S2 | https://www.northerncarealliance.nhs.uk/patient-information/patient-leaflets/physiotherapy-incentive-spirometer-3-ball | Physiotherapy – Incentive Spirometer (3 ball) | Northern Care Alliance NHS | – | Refused (HTTP 403). Snippet used in G-R3, grade C |
| S3 | https://www.cuh.nhs.uk/patient-information/incentive-spirometer/ | Incentive spirometer (approved 16 Jul 2024) | Cambridge University Hospitals NHS | B | G-R2, G-R3 |
| S4 | https://www.intechopen.com/chapters/76231 | Medical device adverse event reporting in India (2021) | IntechOpen (peer-reviewed chapter) | B | G-R4 |
| S5 | https://www.utoledo.edu/hhs/respiratorycare/pdfs/Incentive_Spirometry.pdf | (page not found) | University of Toledo | – | Nothing |
| S6 | https://mskcc.org/pdf/cancer-care/patient-education/how-use-your-incentive-spirometer | How To Use Your Incentive Spirometer | Memorial Sloan Kettering | – | PDF text unreadable; headings only; nothing used |
| S7 | https://caho.in/files/Medical records Retention and Destruction G6 CMBT.pdf | Medical records retention and destruction | CAHO | – | PDF text unreadable. Snippet used in G-R9, grade C |
| S8 | https://www.respiratorytherapyzone.com/incentive-spirometry/ | Incentive Spirometry: A Guide for Clinical Practice (2026) | Respiratory Therapy Zone | C | G-R1, G-R3 |
| S9 | https://testing.nabh.co/wp-content/uploads/2025/07/E.-E-Mitra_CHECK-04.16_Biomedical-Equipment-Management-Checklist.pdf | Biomedical Equipment Management Checklist | NABH | – | Connection refused. Snippet used in G-R6, grade C |
| S10 | https://ssrana.in/articles/who-owns-what-the-machine-makes-authorship-and-ownership-of-ai-generated-works-under-indian-law/ | Who Owns What the Machine Makes? (31 Aug 2026) | S.S. Rana & Co. (law firm) | B | G-R13 |
| S11 | https://lexplosion.in/medical-device-license-holders-mandated-to-report-all-suspected-unexpected-serious-adverse-events-to-the-materiovigilance-programme-of-india-mvpi-for-timely-risk-identification-and-regulatory-compli/ | Note on the CDSCO circular on reporting to MvPI (3 Jun 2024) | Lexplosion | C | G-R4 |
| S12 | https://supabase.com/docs/guides/platform/free-project-pausing | Project pausing | Supabase | B | G-R7 |
| S13 | https://render.com/docs/free | Deploy for free | Render | B | G-R7 |
| S14 | https://nishithdesai.com/research-and-articles/hotline/technology-law-analysis/cert-in-releases-faqs-explaining-the-direction-on-cybersecurity-6139 | CERT-In releases FAQs explaining the Direction on cybersecurity | Nishith Desai Associates | B | G-R8 |
| S15 | https://saintlukeskc.org/node/34749 | Using an incentive spirometer with your tracheostomy tube | Saint Luke's Health System | – | Page gone (HTTP 404). Snippet used in G-21, grade C |
| S16 | https://play.google.com/store/search?q=spirobuddy&c=apps | Google Play search for "spirobuddy" (10 Oct 2026) | Google | B | G-R17 |
| S17 | https://link.springer.com/article/10.1186/s12912-026-04486-2 | Digital alert fatigue in nurse-led remote postoperative care (2026) | BMC Nursing / Springer | – | Login redirect. Snippet used in G-R5, grade C |
| S18 | https://pmc.ncbi.nlm.nih.gov/articles/PMC4456276 | Association between exposure to nonactionable alarms and response time (2015) | Journal of Hospital Medicine, via PMC | A | G-R5 |
| S19 | https://www.ipc.gov.in/mandates/pvpi/materiovigilance-programme-of-india-mvpi.html | (page not found) | Indian Pharmacopoeia Commission | – | Nothing |

**Search snippets used but not opened (all grade C, "snippet only"):** United Lincolnshire, Stockport and Lancashire NHS leaflets (G-R3) · Wikipedia "Incentive spirometer" (G-R1) · a US clinical-trial protocol with a target-volume chart, and Indian lung-function studies (G-R2) · Dubai Health Authority equipment checklist (G-R6) · KareXpert's NABH listing and a 2026 preprint on FHIR in India (G-R10) · vendor blogs on penetration-test prices: tcsa.in, cybersigmacs.com, securiumsolutions.com (costs list) · tax and compliance explainers: tallysolutions.com, bankbazaar.com, equitylist.co, incorpx.io, taxguru.in, knowyourgst.com (G-R15, G-R16) · EquityList and Treelife on founder vesting (G-R12) · Intepat on the Registrar's DABUS order (G-R13) · Trilegal on the Jan Vishwas Act (G-R8) · Down To Earth on NFHS-5 electricity (G-25) · MSF catalogue, child-size spirometer (G-20) · Thorax study on face masks for lung testing (G-22) · trademark listings for SPIRO, SPIRODOC, SPIROHOME (G-R17).

**Local checks (no web page):** installed Python package licences (G-R11); DNS look-ups for five domain names (G-R17); `tests/test_critical.py` `xfail` reasons; `git remote` and the repository's file list.

**Ledger rows cited without re-opening:** #40, #44, #45, #117, #123, #194, #205, and the W-series in `FUTURE_ARCHITECTURE.md`.
