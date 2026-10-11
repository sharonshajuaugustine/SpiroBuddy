# 09 – Domain sweep: every business area checked once more

**Written:** 11 Oct 2026 · **Method:** read the summaries, ranked lists and checklists of `docs/plan/00`–`08`, `BUSINESS_BRIEF.md`, `07_competitors_and_alternatives.md`, `HANDOFF.md`, `FEATURE_STATUS.md` (headings) and `FUTURE_ARCHITECTURE.md` (skimmed). I also checked a few things in the code and the repo. Then I walked 32 domains one by one. For each domain: what is already covered (by ID), then only the **new** items.

**How to read the item tables**
- **ID:** DS-n (DS = domain sweep). Older IDs are cited, never repeated: **G-n / G-R n** (04 gaps), **BS-n** (08 blind spots), **C/O/D/P-n** (07 cross-check), **B7-n** (competitors), **L-n** (06 legal), **E-n** (05 expansion), **M-n** (02 app), **H-n** (01 hardware), **B1–B6-n** (business research files), **J-n** (04 assumptions).
- **Sev:** High / Med / Low.
- **When:** **Sub** = before the hackathon submission (Mon 12 Oct 2026, 11:00 AM IST) · **Pilot** = before any real patient · **Sale** = before the first paid sale · **Scale** = 3+ hospitals.
- **Basis:** a repo file, a search snippet (grade C, page not opened), or **"our reasoning"** (nobody has checked it).
- Owner roles as in 04: Lead, Tech, Clinical, Ops, Reg, CA, Lawyer, Design, Hardware.
- Nothing here is medical, legal, tax or investment advice.

---

## Answer in 12 lines

1. **The earlier files are thorough.** Of 32 domains, 12 are now fully covered. I found **64 new items**. Most are smaller than the gaps in 04 and 08.
2. **Biggest thing for tomorrow: the code ZIP.** If someone zips the project folder, the ZIP will contain `.env` (5 filled-in values, possibly live keys), `infffff/` (organisers' screenshots with real names) and `.venv`. Build the ZIP from git only (DS-60).
3. **The public demo may be able to send real messages or spend money.** With no login, anyone could press demo buttons that call WhatsApp, phone or AI services if keys are set. Check that before judges arrive. Then switch on two-step login and spending caps on every account (DS-29, DS-28).
4. **The demo video can leak or get blocked.** Watch for real names or numbers on screen, music the team has no rights to, and a file over 100 MB (DS-62, DS-35).
5. **AI vendors: nobody has read Anthropic's or Sarvam's terms on health data** (whether they keep it, train on it, or where it is processed). The code also sends age, sex and type of surgery, not only names (DS-24, extends G-64).
6. **Voice red-flags may fail for the people who need them most.** Speech-to-text has not been tested on elderly, breathless or hoarse voices (after a breathing tube). A button or keypad path must always exist (DS-25).
7. **The outcome a hospital would pay for (fewer lung complications) needs roughly 1,350 patients per group to prove** (our arithmetic). A start-up cannot run that study. So agree up front which smaller results the hospital will accept: nurse minutes, adherence, a report it can show its accreditation inspectors (DS-6).
8. **Free pilots rarely turn into paid ones unless the terms are agreed first.** Put the success test and the price after the pilot into the pilot agreement (DS-43).
9. **Lending units burns cash.** Every new hospital needs about ₹3–5 lakh up front: units bought now, and hospital payments 2–6 months later (our arithmetic). Hospital deposits, invoice discounting through TReDS (a government-backed platform where a bank pays the invoice early) and grants are the levers (DS-37, DS-39).
10. **Supply risks nobody named:** the laser sensor has one maker. The spirometer maker can change its plastic mould without telling us, which would break our fit and calibration. Cheap parts on hobby sites can be fakes (DS-15, DS-16, DS-17).
11. **Weakest areas still:** exit paths, international, environment, and channel partners. All are thin but low priority. Clinical, legal, security and regulatory are well covered.
12. **Cheapest wins:** a git-only ZIP, a 10-minute check of the video, a spending cap on each API key, and one paragraph in the pilot agreement on "what happens after". Each is under an hour and none needs hardware.

---

## 1. Clinical and patient safety

**Covered by:** G-1 to G-13, G-17, G-20 to G-22, G-R1 to G-R5, BS-1, BS-4, BS-5, BS-12, risk 3, risk 24, L-17, M-37 #24 (safety button with no unit and no internet).

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-1 | **Painkiller timing.** Physiotherapists often time deep-breathing practice to the window when pain relief works. Our schedule ignores it | Breaths done in pain are shallow. The coach scolds the patient and the nurse gets a false "poor technique" | Med | Pilot | Ask the clinical lead (G-9) whether to add "best done 30–60 min after your pain tablet" to the plan. Let the nurse shift the schedule | Clinical | Our reasoning |
| DS-2 | **Over-use: no upper limit.** A keen patient, a pushy son (G-113) or a game-like streak can drive extra sessions | Dizziness and tiredness from too many deep breaths. G-3 covers rest *within* a session, not a daily cap | Med | Pilot | Clinician sets a maximum number of sessions per hour and per day. Above it, the coach says "well done, rest now" | Clinical + Tech | Our reasoning |
| DS-3 | **Hazards from our own unit in a home:** a charging cable across the floor at night, and small parts (USB plug cover, silicone feet) that a grandchild can swallow | A fall after surgery is serious. Choking is a known small-part hazard. Battery risk is covered (risk 24); these are not | Med | Pilot | Add both to the risk file (G-4) and the leaflet (G-78): "charge away from the walkway"; tethered plug; glued-in feet | Hardware + Clinical | Our reasoning |
| DS-4 | **"Call 112" only.** In many states, older people know **108** as the ambulance number | In a panic, the familiar number gets dialled. A wrong or unknown number wastes minutes | Low | Pilot | Show "112 or 108 (ambulance)" if the clinical lead agrees. Check the pilot state's practice | Clinical | Our reasoning |
| DS-5 | **Home care of the spirometer itself** (washing and drying the mouthpiece, storing it away from dust) is not in any script | If the coach says anything about cleaning, it is clinical content and needs sign-off (G-8). If it says nothing, the plastic goes mouldy over two weeks | Low | Pilot | One signed-off clip and one picture on the quick-start card (G-29), copied from the maker's leaflet | Clinical | Our reasoning |

## 2. Clinical evidence and study design

**Covered by:** B5-20 and the four-step evidence plan in `05_icmr_ethics_abdm_evidence.md` (it already includes a control arm with a "silent sensor" and about 36–45 patients per group for adherence), G-110, G-119, G-120, J-8, B7-18 to B7-21, E-6, BS-25, C9 to C11.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-6 | **The result a hospital would pay for cannot be proven at our size.** Cutting lung complications from 10% to 7% needs about 1,350 patients per group (80% power, our arithmetic from the 10.4% rate in `CHECKPOINT_1.md`) | Adherence alone may not open a budget. Without an agreed "buying result", a good pilot still ends with "interesting, no money" | High | Pilot | Before the pilot, ask the hospital: "Which three numbers would make you pay?" Write them into the protocol as secondary outcomes, for example nurse minutes per patient, return visits within 30 days, and the accreditation (NABH) education record (E-4) | Lead + Clinical | Our arithmetic and reasoning |
| DS-7 | **Spill-over between groups in a controlled study.** Once nurses see SpiroBuddy, they teach everyone better. Patients in nearby beds talk to each other | Spill-over hides the real effect, so a true benefit can look like none | Med | Before the controlled study (step 4) | Ask a statistician to compare a "ward-by-ward" or "before-and-after, staggered by ward" design (cluster or stepped-wedge) against bed-by-bed randomisation | Clinical + statistician | Our reasoning |
| DS-8 | **Hospital data we will need is not in any agreement:** length of stay, readmissions and cost per patient sit in the hospital's billing and records systems | Without written access, the money case (E-6) cannot be measured even if it is true | Med | Pilot | One clause in the pilot agreement (G-97) and the protocol listing these fields, taken in anonymised form by the hospital's own staff | Lead + Lawyer | Our reasoning |
| DS-9 | **Conflict of interest.** The founders own the product and would analyse its trial | Journals and ethics committees ask for this to be declared. Reviewers discount a study the maker analysed | Med | Pilot | Declare the interest in the protocol. Let the hospital's investigator or statistician hold and analyse the data. Agree authorship rules (who is named on papers) in writing | Clinical + Lead | Our reasoning (standard journal practice) |

## 3. UX for elderly and low-literacy users

**Covered by:** G-14 to G-19, G-23, G-29, G-75, G-112, M-28, L-19, BS-8, E-16 (dialects), `FUTURE_ARCHITECTURE.md` §5.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-10 | **The carer, not the patient, will often run the phone and the unit.** In many Indian homes a daughter or daughter-in-law handles the phone. G-17 has a "carer present" mode only for confused patients | If set-up and training target only the patient, the person actually pressing buttons was never taught | Med | Pilot | Make "teach the carer too" a default step at enrolment. Write a carer version of the quick-start card. Ask about this in the interviews | Design + Clinical | Our reasoning; 41% smartphone ownership among older Indians (repo, G-26) |
| DS-11 | **Teach before the operation, not on discharge day.** On discharge day a patient gets ten instructions and remembers few | Low recall leads to wrong use at home. Pre-surgery teaching also feeds the pre-surgery practice path (E-8) | Med | Pilot | Propose enrolment at the pre-surgery clinic visit in the pilot design. Ask the physiotherapist in the interview | Clinical | Our reasoning |
| DS-12 | **Numbers on the patient's screen** (mL, %, "1,250") | Many older users struggle with numbers. It also touches the device-class question (D6) | Low | Pilot | Patient screens show a filling picture and "good / try again". Numbers appear only on nurse screens | Design | Our reasoning; D6 |

## 4. Nurse workflow and alarm fatigue

**Covered by:** G-7, G-R5, G-28, G-38, G-40, G-66, G-117, BS-11 to BS-16, BS-18, risk 14, J-7.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-13 | **No fixed action for each alert, and no "closed because…" reason.** "Seen" is not the same as "dealt with" | Alerts pile up in a grey zone. Nobody can tell the hospital how fast alerts are acted on, which is a selling point and a safety measure | Med | Pilot | Each alert type gets 2–3 named actions (called patient / told doctor / not needed) and one tap to close with a reason. Report median time to action per shift | Tech + Clinical | Our reasoning |
| DS-14 | **The nurse may not speak the patient's language.** A Malayali nurse in a Delhi ward cannot check what the Hindi coach told Ravi | The nurse cannot verify or correct the coaching, and red-flag replies get misread | Low | Pilot | The dashboard shows the English (or nurse's language) version of each spoken line and each patient reply | Tech | Our reasoning |

## 5. Product, hardware, manufacturing and supply chain

**Covered by:** H-1, H-6 to H-10, B3-1 to B3-5 (production steps, board, 3D printing, moulds; tooling, minimum orders and working capital for stock at 10,000 units), G-31, G-35, G-71, G-72, G-79 to G-81, G-104, L-22 (local content), L-24 (import paperwork), J-11, J-19, C1, C5, C6.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-15 | **The laser sensor has a single maker** (ST makes the whole VL53 family). The better chip (VL53L4CD) is not stocked in India (H-1) | An end-of-life notice or a chip shortage (as in 2021–22) stops production. There is no drop-in replacement | Med now, High at Sale | Sale | Buy the pilot's whole sensor need in one order, plus 20%. Keep the sensor on its own plug-in board (H-10 rule). Bench-test one non-ST distance sensor as a backup | Hardware | Our reasoning; H-1, H-10 |
| DS-16 | **The spirometer maker can change its mould without telling us.** A new base shape, tube or piston colour breaks our fit and the calibration table (H-8) | Units in the field start reading wrong, with no error shown | High | Pilot | Buy the pilot's spirometers from one batch and record the batch. Ask Romsons (E-19) for advance notice of changes. Have the seating check (H-6) flag any unusual resting distance | Hardware + Lead | Our reasoning |
| DS-17 | **Fake or cloned parts** on hobby marketplaces: copied sensor boards, lithium cells with less capacity than the label says | Wrong readings, short battery life, fire risk. BIS registration (L-4) needs an invoice trail anyway | Med | Pilot | Buy only from authorised distributors. Keep invoices with batch numbers in the supplier list (G-71). Test the capacity of 3 cells per batch | Hardware + Ops | Our reasoning |
| DS-18 | **Import cost and delay.** The real cost of an imported part = list price + freight + customs duty + 18% import GST + broker fee. Radio modules with no Indian approval (ETA) can be held at customs (L-24) | Plan 03 prices are Indian shop prices. Any imported part (VL53L4CD, nRF modules) costs more and takes weeks longer | Med | Pilot | Ask one Indian distributor for a delivered price and delivery time on the two imported parts before Stage B | Hardware | Our reasoning; L-24 |
| DS-19 | **No test bench (jig) at the end of assembly, and no check before a unit goes to the next patient.** H-8 needs a per-unit offset. G-72 needs a recorded result. Nothing describes the fixture or the pass/fail test | Hand-testing 20 units differently each time spoils the traceability and calibration records. A worn unit is re-issued unnoticed | Med | Pilot | One 3D-printed fixture with a fixed target at two heights, plus a script that writes pass/fail to the unit's serial record. Re-issue test: battery health, window clean, rest distance in range | Hardware + Tech | Our reasoning; H-8, G-72 |
| DS-20 | **Humidity and corrosion.** Coastal and monsoon homes (Kerala, the first target state, B1-13) have damp air for months. IP22 (H-6) covers dripping water, not damp | Corroded contacts, a fogged sensor window, a swollen cell | Med | Pilot | Coat the circuit board with a protective coating (conformal coat). Leave 2 units in a sealed box with a wet cloth for 2 weeks and re-test | Hardware | Our reasoning |
| DS-21 | **Contract manufacturer and the licence.** A manufacturing licence covers a site and its people. MDR expects named technical staff with set qualifications. If a contract maker builds the units, its site and quality system become part of our file (loan licence, Gate 2 #24) | Choosing a maker without a medical-device quality system (ISO 13485) means redoing it at licence time | Med | Sale | Shortlist 3 electronics manufacturers with ISO 13485. Ask each for set-up cost, minimum order and whether they host loan licences. Ask the regulatory consultant about the staff qualification rule | Hardware + Reg | Our reading (staff rule not checked this round) |

## 6. Firmware and over-the-air (OTA) updates

**Covered by:** H-2, H-10, M-35 (signed images, staged roll-out, roll-back, minimum safe version), M-37 #4 (firmware signing key), #22, #23, `FUTURE_ARCHITECTURE.md` §4, G-72.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-22 | **The secure-update design is written for the ESP32** (Secure Boot v2, eFuse, `FUTURE_ARCHITECTURE.md` §4). The battery unit moves to the nRF52840 (H-2, D8), which uses a different boot loader (for example MCUboot) and key storage | The pilot firmware could ship with no working secure boot because the plan describes the wrong chip | Med | Pilot | Rewrite §4's OTA row for the nRF52840. Decide who holds the signing key and where the backup lives, offline, with two keepers | Tech | Repo (C5, `FUTURE_ARCHITECTURE.md` §4) |

## 7. Software reliability

**Covered by:** G-45 to G-49, G-58, G-59, BS-32, risk 23, M-31, `FUTURE_ARCHITECTURE.md` §7–8.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-23 | **No automatic test gate before deploy.** Render redeploys on every push to `main` (HANDOFF). There is no `.github/workflows` folder. HANDOFF lists one failing test | A broken commit goes straight to the live link judges use. Later, it goes to patients | Med (Sub: freeze per BS-32) | Pilot | Add one GitHub Action that runs `pytest` on every push, and set Render to deploy only after it passes | Tech | Repo (no `.github/`), `HANDOFF.md` |

## 8. AI and machine learning

**Covered by:** G-62, G-63, G-64, G-114, BS-2, BS-28, BS-30, risk 16, L-18, B5-9, E-17, `FUTURE_ARCHITECTURE.md` §6 (registry, drift, shadow mode, LLM guardrails, no free text in prompts). The call-script code already has an output filter (`_BAD`) and a template fallback (`backend/app/comms/script.py`).

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-24 | **Vendor terms on health data are unread.** Nobody has checked whether Anthropic and Sarvam keep inputs, use them for training, where they process them, or whether they sign a data processing agreement. Also, `script.py` sends **age, sex and type of surgery** with the first name. G-64 names only the name | Health data leaving India under unknown terms. A hospital's data agreement (G-98) will ask exactly this | High | Pilot | Read both vendors' commercial and privacy terms (one hour). Ask Sarvam in writing. Send placeholders instead of age, sex and surgery. Prefer the template for anything patient-facing (D13) | Tech + Lawyer | Repo code; our reasoning |
| DS-25 | **Speech-to-text on our real users is untested:** elderly speakers, missing teeth, breathless or hoarse after a breathing tube, regional accents | A spoken "chest pain" is missed. The red-flag check (G-44) only works on text the speech service got right | High | Pilot | Record 10 older relatives saying the red-flag words in 2 languages, while tired. Measure the hit rate. Keep a "press 9 / big red button" path that needs no speech | Tech + Clinical | Our reasoning |
| DS-26 | **No clinical definition of a "good breath".** How slow? How long a hold (3 s or 5 s)? What volume compared with the target? The model's labels rest on team rules (`rules.py`), not on a signed standard | Every label, every alert and every "accuracy" figure rests on it. Two physiotherapists may disagree | Med–High | Pilot (before collecting real labels) | The clinical lead writes a one-page labelling guide. Two raters label the same 50 breaths. Measure how often they agree | Clinical + Tech | Repo (`rules.py`, `FUTURE_ARCHITECTURE.md` §6.4); our reasoning |
| DS-27 | **Who owns a model trained on hospital A's patients?** Hospital A may claim it, or forbid its use at hospital B | Without a clause, the main thing that is hard to copy (E-18: a labelled set of real breaths) may not legally be ours | Med | Pilot | One clause in the pilot and data agreements (G-97, G-98): anonymised features and trained models belong to the company; raw data stays the hospital's | Lawyer | Our reasoning; E-17, E-18 |

## 9. Cybersecurity

**Covered by:** G-41 to G-43, G-53, G-76, G-96, BS-14, BS-35, M-35, M-37 #4, `FUTURE_ARCHITECTURE.md` §9 and §4 (device signing).

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-28 | **Account hygiene:** two-step login on GitHub, Render, Supabase, Anthropic and Sarvam; new keys after the hackathon (keys have been pasted into many sessions); a monthly spending cap on each paid key | A leaked key = someone else's bill, or our account banned. BS-31 adds a second admin, but not these | Med | Sub (caps), then after judging (rotation) | 15 minutes per service: turn on two-step login, set a spending cap. Rotate the keys after results | Lead + Tech | Our reasoning |
| DS-29 | **The public demo can trigger real side effects.** No login, and demo buttons drive the reminder ladder, WhatsApp, calls and AI summaries. If keys are set on Render, any visitor can send messages to the demo numbers or burn credit | Spam to a real phone, a bill, a WhatsApp number flagged as spam (risk 22) | Med | Sub | Confirm on Render which keys are set. For the judging period, keep live sending off (`DEMO_*` numbers unset) or add a simple rate limit | Tech | `.env` has 5 filled values; HANDOFF says no keys on Render as of 10 Oct (may have changed) |
| DS-30 | **Social engineering by phone.** "I'm his son, tell me how he's doing." Callers to the helpline (G-30) or the ward (BS-11) are not identity-checked | Health data disclosed to the wrong person. A scammer collects details for BS-7 fraud | Med | Pilot | Helpline script: share nothing; offer a call-back to the number on file only | Ops | Our reasoning |

## 10. Data governance and ABDM/ABHA

**Covered by:** G-50, G-54, G-55, G-98, G-R8, G-R9, B4-13, B4-14, B4-16, B5-17, B5-18, L-7, BS-33, `FUTURE_ARCHITECTURE.md` §3.3 to §3.8. (ABDM = India's national digital health system; ABHA = the patient's national health ID.)

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-31 | **WhatsApp copies cannot be deleted.** Family messages sit on Meta's servers and on relatives' phones for good. A deletion request (G-55) cannot reach them | Every word in a family message is permanent. BS-14 covers nurses' phones, not families' | Med | Pilot | Keep family messages to "sessions done today" and a cheer: no surgery type, no scores, no red flags | Tech + Clinical | Our reasoning |
| DS-32 | **The team's own handling of data:** laptops, CSV exports, screenshots for slides, test copies of the database | Most small-company leaks come from a founder's laptop or a shared drive, not a hack | Med | Pilot | One-page rule: who on the team may see real data, no exports to personal drives, disk encryption on, no screenshots with patient details | Lead + Tech | Our reasoning |

## 11. Interoperability (hospital systems, HL7/FHIR)

**Covered by:** G-56, G-R10, BS-16, `FUTURE_ARCHITECTURE.md` §3.8 (FHIR export, ABDM milestones M1–M3, CSV/PDF first). HL7 and FHIR are the common formats for passing data between hospital systems.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-33 | **Store the hospital's own patient number (UHID / MRN) from day one** | Without it, our records cannot later be matched to the hospital's system. Matching by name and phone produces wrong matches | Low–Med | Pilot | Add one field to the patient record. Make it required at enrolment | Tech | Our reasoning |

## 12. Regulatory (CDSCO, BIS, WPC, export)

**Covered by:** L-1 to L-6, L-24, L-25, B4-1 to B4-12 (including laser and electrical-safety standards in B4-9), B5-10, B5-11, C4 to C9, G-67 to G-82, the Gate 0–4 checklists in 06, BS-17, BS-21, E-15 (export).

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-34 | **Nobody watches for rule changes.** 2026 alone brought new software guidance, call rules (B4-17), a draft accessibility regime (L-19) and the DPDP timetable | A rule changes and we learn it from a hospital | Low | Pilot | One named person checks the CDSCO, MeitY and TRAI notice pages on the first Monday of each month and logs anything relevant | Reg (Lead until hired) | Our reasoning |

(DS-21 covers the manufacturing-licence staff question.)

## 13. Legal and IP

**Covered by:** G-61, G-83 to G-89, G-94, G-95, G-106, L-10 to L-13, L-16, L-17, B4-18, B4-20, B4-21, C16, D9.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-35 | **Rights in the demo material:** background music in the videos, images, fonts, 3D assets, and the generated voice clips (does Sarvam's licence allow commercial reuse of its output?) | A public video with unlicensed music can be muted or taken down. Commercial use of voice output depends on the vendor's terms | Med | Sub (music), Pilot (voices) | Use no music, or a track with a clear free licence. Note each asset's source (`3D_SOURCES.md` already does this for dimensions). Read Sarvam's output terms | Design + Lead | Our reasoning |

## 14. Company formation and governance

**Covered by:** G-83 to G-92, L-14, L-23, B3-15, D2.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-36 | **A written list of every share promise made so far,** including casual ones ("you'll get some equity") to helpers, mentors or a doctor | Spoken promises become disputes at the first investment, or block it | Low–Med | Before incorporation | One shared private note: who was promised what, when, and on what condition. Settle each one in the founders' agreement (G-83) | Lead | Our reasoning |

## 15. Finance

**Covered by:** G-91, G-92, G-101, G-102, L-15 (GST rates, bundle rule, TDS), L-26, B2-4, B2-4a and L-22 (45-day rule and the buyer's tax deduction), B3-6, B6-2, C12, O6, risk 19, D11.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-37 | **Cash tied up in lent units.** A 50-unit hospital means about ₹1.35–1.5 lakh of units bought up front (₹2,700–2,950 each with GST, Plan 03). Hospital payments arrive 60–180 days after each month. With spares and set-up, each new hospital needs roughly **₹3–5 lakh** before it pays back (our arithmetic) | Growth eats cash: the faster we sign hospitals, the sooner we run out. Plan 03 shows monthly profit, not timing | High | Sale | Add a cash-timing sheet to Plan 03. Levers: a unit deposit or set-up fee from the hospital, hospital-owned units (D7), TReDS (DS-39), and grants tied to units | Lead + CA | Our arithmetic from Plan 03 |
| DS-38 | **GST input credit can pile up.** Parts are bought at 18% GST. If the device is sold at 5% (B6-2), more tax goes in than comes out. The extra can be claimed back, but slowly ("inverted duty" refund). A per-episode service at 18% does not have this problem | Cash stuck with the tax office. It changes which model (sell or lend) is cheaper in practice | Med | Sale | Ask the CA, together with the bundle question (G-102) | CA | General GST knowledge; not confirmed |
| DS-39 | **TReDS for large hospital chains.** Companies with turnover over ₹250 crore must register on TReDS (MSME Ministry order S.O. 4845(E), 7 Nov 2024, deadline 31 Mar 2025). TReDS is a government-backed online platform where a bank pays a small supplier's approved invoice early, for a small discount | Turns a 90–180 day wait from a big private chain into cash within days. It needs Udyam (MSME) registration, already advised (L-22) | Med | Sale | When the first big-chain customer appears, ask its finance team whether it pays through TReDS | CA | Search snippets (grade C); later changes not checked |
| DS-40 | **What counts as one billable "episode"?** A unit assigned but never used? A patient readmitted on day 3 (BS-10)? Two short assignments? | The ward and our invoice will disagree. Disputes delay payment further | Med | Sale | One-line definition in the price list (G-100), for example "a unit assigned for 3 or more days with 1 or more recorded session", with the system's monthly report as the shared count | Lead | Our reasoning |
| DS-41 | **Grants pay late and in instalments.** Many schemes pay in tranches (instalments) after milestones or receipts | Spending runs months ahead of grant money. Founders end up paying out of their own pockets (G-91) | Med | Pilot | Read each scheme's payment terms (B3-7 to B3-10). Plan cash so the first tranche covers the first milestone | Lead + CA | Our reasoning |

## 16. Pricing and packaging

**Covered by:** D7, Plan 03 §2 to §3, B6-4 to B6-9, B6-19, G-100, G-103, BS-22, BS-23, J-3, O10, B1-14 (home physiotherapy price as an anchor).

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-42 | **A family-paid add-on,** for example an extra 2–4 weeks of home coaching or more frequent family updates, often paid by children who live in another city or abroad | A second source of money that does not wait for a hospital budget. It must never be sold as clinical benefit (L-13) and must not pressure the patient (G-113) | Low | Scale | Add one question to the family interview: "Would you pay ₹X to continue after two weeks?" | Lead | Our reasoning |

## 17. Sales process and procurement

**Covered by:** B1-2 to B1-4, B2-1 to B2-10a, B2-24, E-3, L-21, L-22, BS-21 to BS-24.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-43 | **No plan for turning the free pilot into a paid one.** Free pilots often end in "thanks, we'll think about it" | Months of work with no revenue. G-97 lists what the pilot agreement covers, but not what happens after it | High | Pilot | Add to the pilot agreement: agreed success measures (DS-6), the price after the pilot, a decision date, and a named budget holder (J-3) | Lead | Our reasoning |
| DS-44 | **Hospital supplier forms.** A purchase department asks for PAN, GST number, MSME certificate, a cancelled cheque, ISO and licence copies, an insurance certificate and references | The order waits weeks for paperwork | Low–Med | Sale | Keep one folder ready from incorporation onward | Ops | Our reasoning |
| DS-45 | **The government buying portal (GeM) may have no product category that fits us.** GeM is the online marketplace where government hospitals buy | A bid may need a custom category or an open tender instead | Low | Scale | Search GeM for "incentive spirometer" and "remote patient monitoring" once there is a licence (B2-5) | Lead | Our reasoning |

## 18. Channel partners and distributors

**Covered by:** E-14, B2-17, B2-21, B2-23, G-105, BS-21.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-46 | **Exclusive deals, and distributors who cannot run lending.** A distributor or Romsons may ask for state-wide exclusive rights. Most distributors sell boxes; they do not train nurses, collect units or clean them | Locked out of a state by a weak partner, or a model (lending) the channel cannot carry out | Low | Scale | Rule: no exclusive rights without yearly sales targets and an exit clause. Use distributors for hospital-owned units only | Lead + Lawyer | Our reasoning |

## 19. Marketing, brand, content and credibility with doctors

**Covered by:** G-106 to G-109, BS-17, BS-19, BS-20, BS-34, B2-22 (IACTSCON 2027 poster, ISACON, IAP), B2-23, L-13, L-21 (no gifts or fees to doctors), P7, E-17 (co-authored papers).

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-47 | **A one-page evidence note for clinicians,** separate from the pitch deck: what is known about the exercise (B7-18 to B7-21), what we measure, what we do not claim, with references | Doctors distrust start-up decks. An honest one-pager builds trust and keeps everyone saying the same allowed things | Low–Med | Pilot | Draft it from B7-22, CHECKPOINT_1's "honest limit" and the never-say list. Have the clinical lead check it | Lead + Clinical | Our reasoning |

## 20. Partnerships

**Covered by:** E-10 (TB programme, Ni-kshay Mitra), E-14, E-19, B2-12, B2-18, B2-21, BS-24, L-26 (CSR routes).

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-48 | **Nursing and physiotherapy colleges as partners.** Students could train patients, staff a helpline or run follow-up calls, and do supervised research projects using the pilot | Cheap, credible labour for the pilot's hardest jobs (G-28, G-30). Faculty can serve as investigators (B5-14) | Low–Med | Pilot | Ask the physiotherapy college linked to the first hospital during the interviews | Lead | Our reasoning |

## 21. Customer success and training

**Covered by:** G-28, G-29, G-37, G-38, BS-13, E-17 item 1 (monthly report to the hospital).

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-49 | **One "super-user" nurse per shift,** plus a monthly 30-minute review with the ward using the same 5 numbers each time | Ward staff rotate. A single coordinator (G-38) cannot cover nights. A fixed review rhythm keeps the champion engaged and finds trouble early | Low–Med | Pilot | Put both in the pilot plan. Define the 5 numbers (sessions done, alerts, time to action, units out, returns) | Ops | Our reasoning |

## 22. Support and logistics

**Covered by:** G-30 to G-35, G-80 (transport, lithium shipping rules), BS-6, BS-9, BS-11, M-37 #8, risk 7, B6-16. **No new items.**

## 23. Impact measurement and SDG reporting

**Covered by:** G-110, G-111, B5 headline metric (share of due sessions completed), SDG 3 and target 3.8 in `CHECKPOINT_1.md`.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-50 | **Use the same impact definitions in the deck, grant forms and CSR reports.** Today the pitch, the brief and the evidence plan use slightly different words. CSR funders expect project reports matched to their spending categories | Different numbers in different places look careless, or worse | Low–Med | Sub (deck), Scale (CSR) | Fix one sentence and use it everywhere: "Share of due hourly sessions completed, from about X today (unknown) to a target set with the ward" | Lead | Repo (B5, CHECKPOINT_1); our reasoning |

## 24. Environment (e-waste, single-use plastics)

**Covered by:** G-39, G-118, L-5, B4-12, B6-15, H-6 (materials).

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-51 | **Do not claim an environmental benefit.** Our unit adds electronics and a battery. The single-use spirometer is thrown away either way | A "green" claim that does not hold up is a credibility risk with judges and buyers | Low | Sub | Add "eco-friendly / reduces waste" to the never-say list (P7) | Lead | Our reasoning |

## 25. Accessibility

**Covered by:** L-19, M-28, G-14 to G-16, G-23, Gate 3 #35 (IS 17802 conformance).

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-52 | **The nurse dashboard's red / amber / green.** About 1 in 12 men cannot tell red from green easily (general knowledge). M-28's "never by colour alone" rule is written for the patient app only | A colour-blind nurse misreads which patient is urgent | Low | Pilot | Check that every status on the dashboard also has a word or an icon | Design | Our reasoning |

## 26. Ethics and equity

**Covered by:** G-111 (who is left out), G-24, G-26, G-27, G-112 to G-117, BS-2, B5-5, L-20, E-16 (dialects).

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-53 | **Giving back to the hospitals and patients whose data trained the model.** ICMR's AI guidance stresses fairness and benefit (B5-9). If their breaths build our company's main asset (E-18), they should benefit | An ethics committee may ask. Hospitals will ask in the data negotiation (DS-27) | Low | Pilot | Offer pilot sites free or discounted use and co-authorship. State this in the consent form | Lead + Clinical | Our reasoning |

## 27. Team, hiring, advisers, culture, founder health

**Covered by:** G-82 to G-85, G-90, G-94, BS-29, BS-31, risk 2, risk 6, L-23, B3-12.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-54 | **No skills map and no "first hire" decision.** Missing skills: embedded firmware for the battery unit, quality and regulatory, clinical, hospital sales | Grants and incubators ask "who builds what?" A wrong first hire wastes the first grant | Med | Pilot | One table: skill → who has it now → gap → hire, adviser or partner. Most likely first gaps: clinical lead (G-9) and an embedded/quality person | Lead | Our reasoning |
| DS-55 | **Founder health and cover.** Hackathon all-nighters, exams (G-85), one person holding everything (BS-31) | Burnout is a common reason student start-ups stop. Nobody covers anyone's role | Low–Med | Sub onward | Agree a rest rule after submission, and a written "who covers whom" for each role | Lead | Our reasoning |

## 28. Fundraising

**Covered by:** B3-7 to B3-14, B3-16, L-26, C12, D11, risk 19, BS-24.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-56 | **No grant calendar.** "Current grant call dates" is an open question in the brief. BIRAC BIG runs about twice a year (B3-9). NIDHI-PRAYAS goes through host incubators with their own intakes | A missed window can mean 6 months' delay | Med | Pilot | One page listing scheme, next deadline (confirmed on the official page), what it needs, owner. Review monthly | Lead | Repo (BUSINESS_BRIEF open questions); our reasoning |
| DS-57 | **Limits on giving away shares.** Incubators often take a small stake for small money (B3-12). Several small deals early can leave founders with too little to attract later investors | Dilution (each new shareholder shrinks the founders' slice) is hard to undo | Low–Med | Pilot | Before signing any equity deal: write down the total share the founders keep, and ask a start-up lawyer (L-26). Prefer grants first, which already is the plan | Lead | Our reasoning |

## 29. International expansion

**Covered by:** E-15 (Bangladesh first, after an Indian licence), L-24 (free-sale certificate, export approvals), B7-1 (InSee in the US). DS-42 adds family members abroad as possible payers. **No other new items.**

## 30. Exit paths

**Covered by:** nothing specific.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-58 | **Likely buyers of the company one day,** and what they would check first. Possible buyers: spirometer makers (Romsons, B2-21), pharma companies with digital programmes (Cipla, Lupin: B7-14, B7-15), monitoring companies (Dozee-type, B1-17), home-care and rehab chains (E-14). A buyer checks clean ownership of the code and designs (G-86), the licence, the quality system and the rights to the data and models (DS-27) | Not urgent. But each of these is cheap to keep clean now and costly to fix later. Investors also ask "who buys you?" | Low | Scale (keep clean from now) | Keep a one-line answer for investors. Treat G-86 and DS-27 as part of being "ready to be bought" | Lead | Our reasoning |

## 31. Reputation and crisis communication

**Covered by:** BS-7, BS-10, BS-34 (press note, spokesperson), G-50 (breach reporting), G-74 (recall), G-109.

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-59 | **One crisis playbook covering four cases:** a patient dies or is harmed while using the device, a data breach, a viral complaint on social media, a faulty batch. Key rule: **the hospital speaks to its patients first**, and we do not comment on a patient | In the first hours, silence or a wrong word does more damage than the event. Today the pieces sit in three files with no single order of steps | Med | Pilot | One page: who is told in the first hour, the first day and the first week; holding lines; who speaks; logs kept (BS-33) | Lead + Lawyer | Our reasoning |

## 32. Hackathon-specific

**Covered by:** BS-17, BS-25, BS-28 to BS-32, P1 to P10, C14, C18, the 11 BEFORE-SUBMISSION fixes in 07, 00 #25 to #28, O10, `DEMO_VIDEO_SHOTLIST.md`, `INTERVIEW_GUIDE.md`, `CHECKPOINT_1.md` (SDG, TRL 3–4).

**New:**

| ID | What | Why it matters | Sev | When | Cheapest next step | Owner | Basis |
|---|---|---|---|---|---|---|---|
| DS-60 | **The code ZIP could leak secrets and real names.** The project folder holds `.env` (5 filled-in values), `infffff/` (organisers' screenshots with real names, HANDOFF) and `.venv`. Git ignores them; a "right-click → compress" does not | Live keys handed to organisers and judges. Real people's names published | High | Sub | Build the ZIP from git only: `git archive -o SpiroBuddy.zip HEAD`. Open the ZIP and check there is no `.env`, `infffff` or `.venv`. Check it is under 100 MB | Tech | Repo (`.gitignore`, `.env` present) |
| DS-61 | **No self-score against what the organisers asked for.** They require: Problem, Who is affected, Solution, Technology/AI, Impact, Scalability, plus 3 or more interviews, an SDG mapping, one measurable impact metric and an honest readiness level (HANDOFF) | Judges score against their own list. A missing heading costs points regardless of quality | Med | Sub | A 10-line checklist: each required item → the slide number. Fill gaps before uploading | Lead | `HANDOFF.md` |
| DS-62 | **Demo video checks:** real names, phone numbers or account details visible on screen (browser bookmarks, notifications, the Render or Supabase dashboard, WhatsApp chats); file over 100 MB; audio too quiet; Hindi or regional clips without English subtitles | A privacy slip in a public video. An upload that fails at 10:55 am | Med–High | Sub | Turn on Do Not Disturb, use a clean browser profile, watch the final file once start to finish, check its size, add English subtitles to non-English lines | Lead | Our reasoning; `00_FOUNDER_NOTES.md` #25, #27 |
| DS-63 | **The live pitch can fail on the day:** Zoom drops, the screen share shows notifications, the free server is slow to wake (G-46), the presenter loses connection | Five minutes is short. A frozen demo wastes all of it | Med | Sub | Keep the video on the presenter's computer to play instead of the live demo. A second person ready to take over. Open the site 2 minutes before. Practise once with a timer | Lead | Our reasoning; BS-31, BS-32 |
| DS-64 | **Interviews must be real, consented and quoted honestly.** Zero were done as of 10 Oct (00 #28). Under time pressure, there is a temptation to round up or invent | Made-up user research is the fastest way to lose trust if a judge asks a follow-up question | Med | Sub | Report the true number. Ask each person's permission to quote them; use first names or roles only. If fewer than 3 were done, say so and state when the rest are booked | Lead | `00_FOUNDER_NOTES.md` #28 |

---

## Top 20 new items, ranked

Ranked by how bad × how soon. Items due before submission are pulled up.

| # | ID | Item | Sev | When | Cheapest fix |
|---|---|---|---|---|---|
| 1 | DS-60 | Code ZIP leaks `.env` keys and real names | High | **Sub** | `git archive`, then open and check the ZIP |
| 2 | DS-62 | Demo video shows private details, is over 100 MB, or has no subtitles | Med–High | **Sub** | Clean browser profile, Do Not Disturb, watch it once, check the size |
| 3 | DS-29 | Public demo can send real messages or spend credit | Med | **Sub** | Check Render keys; keep live sending off while judging |
| 4 | DS-28 | No two-step login or spending caps; keys need changing | Med | **Sub** | 15 minutes per service |
| 5 | DS-35 | Music, images or voice clips in the demo with unclear rights | Med | **Sub** | No music, or a clearly licensed track |
| 6 | DS-64 | Interviews: honest count, consent to quote | Med | **Sub** | Report the true number; ask permission |
| 7 | DS-61 | Deck not checked against the organisers' required items | Med | **Sub** | 10-line checklist → slide numbers |
| 8 | DS-63 | Live pitch failure (Zoom, notifications, slow server) | Med | **Sub** | Local video file, backup presenter, one timed run |
| 9 | DS-24 | Anthropic and Sarvam health-data terms unread; age, sex and surgery sent to the AI | High | Pilot | Read terms; send placeholders; template by default |
| 10 | DS-25 | Spoken red flags untested on elderly or hoarse voices | High | Pilot | 10-person recording test; a button path that needs no speech |
| 11 | DS-6 | The result a hospital pays for needs about 1,350 patients per group; agree smaller "buying" results | High | Pilot | Ask "which 3 numbers would make you pay?" |
| 12 | DS-43 | No path from free pilot to paid | High | Pilot | Success test, price and decision date in the pilot agreement |
| 13 | DS-16 | Spirometer mould changes break fit and calibration without warning | High | Pilot | One batch; seating check; ask Romsons for change notice |
| 14 | DS-37 | Each new hospital ties up about ₹3–5 lakh in lent units | High | Sale | Cash-timing sheet; deposits; hospital-owned units |
| 15 | DS-26 | No clinical definition of a "good breath" to label against | Med–High | Pilot | One-page labelling guide; two raters on 50 breaths |
| 16 | DS-15 | Single-maker laser sensor | Med → High | Sale | Buy all pilot sensors at once; test a backup sensor |
| 17 | DS-10 | The carer, not the patient, runs the phone | Med | Pilot | Teach the carer at enrolment; carer quick-start card |
| 18 | DS-11 | Teaching on discharge day is poorly remembered | Med | Pilot | Enrol at the pre-surgery visit |
| 19 | DS-13 | Alerts have no set action and no closing reason | Med | Pilot | 2–3 actions per alert; tap to close; time to action |
| 20 | DS-2 | No daily cap on sessions (over-use, family pressure) | Med | Pilot | Clinician sets maximums; coach says "rest now" |

Just outside the top 20: DS-23 (no automatic test gate before deploy), DS-27 (who owns the model), DS-59 (crisis playbook), DS-17 (fake parts), DS-20 (humidity), DS-31 (WhatsApp copies cannot be deleted).

---

## Domains now fully covered vs still thin

**Fully covered (nothing new, or only small additions):** clinical and patient safety · clinical evidence design (except the "buying result", DS-6) · UX for elderly users · regulatory · legal and IP · company formation · data governance and ABDM · cybersecurity (DS-28 to DS-30 are hygiene) · support and logistics · accessibility · ethics and equity · international (headline level, rightly deferred).

**Covered, with real new items:** nurse workflow (DS-13) · AI/ML (DS-24 to DS-27) · manufacturing and supply chain (DS-15 to DS-21) · finance (DS-37 to DS-41) · sales (DS-43) · hackathon (DS-60 to DS-64).

**Still thin (low priority today, but nobody has gone deep):**
- **Exit paths:** only DS-58. Fine for now.
- **Channel partners:** E-14 lists them, but no terms model beyond DS-46.
- **Environment:** rules are known (L-5), but there is no take-back route design or measured footprint (G-118 open).
- **Firmware/OTA:** designed on paper for the wrong chip (DS-22). Nothing built.
- **Marketing and brand:** the rules (what not to say) are strong; there is no positive content plan, website or channel (G-107 open).
- **Customer success:** pieces exist (G-28, G-38, DS-49), but no onboarding playbook for hospital number two.
- **Pricing:** the numbers are deep, but there is no packaging (tiers) beyond D7. Price testing waits on interviews (J-3).

---

## Web searches and URLs

- **No web page was opened.** Nothing in `docs/research/SOURCES_LEDGER.md` was touched.
- **One web search** (results summaries only, grade C), to check TReDS for DS-39: "TReDS mandatory companies turnover 250 crore MSME notification 2024". Results used:
  - https://singhania.in/blog/mandatory-treds-registration-for-companies-above-250-crore-turnover
  - https://www.vjmglobal.com/blog/companies-with-turnover-more-than-inr-250-crores-have-to-get-registered-on-treds-by-31st-march-2025
  - https://www.outlookbusiness.com/industry/firms-with-rs-250-crore-turnover-rush-to-register-on-treds-as-march-31-deadline-nears
  - https://m1xchange.com/newsletters/digital-connect-q3-24/M1-Newsletter-Q3-2024.pdf
- Repo checks run for this file: `.gitignore`, presence of `.env` (variable names counted, values not read), no `.github/` folder, `backend/app/comms/script.py` (what is sent to the AI and the output filter), keyword searches across `docs/`.
