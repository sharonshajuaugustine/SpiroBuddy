# Version 4 wording rulebook

Checked 12 Oct 2026 against the repo (code equals deployed checkpoint 6755f77). Where the audit and a judge disagree, the repo decides.

Short names: **KB** = docs/research/KNOWLEDGE_BASE.md · **PF** = docs/research/PITCH_FACTS.md · **F** = backend/app/features.py · **H** = docs/CODEX_IMPLEMENTATION_HANDOFF.md · **NF** = docs/INFORMAL_NURSE_FEEDBACK.md · **DECK** = .build/pitch/with-spirobuddy/submission/content.txt

---

## 1. APPROVED WORDING

**1. India operations.** "India's public records show about forty-nine lakh major operations a year."
Evidence: KB:149-152 (4.9 million, 2019 data, an undercount).

**2. Lung-complication rate.** "In a large international study, about one in ten adults having surgery had a lung complication."
Evidence: KB:74-77, PF:6. Never drop "international". The audit's "under general anaesthesia" is not in our fact base; do not add it.

**3. Chennai study.** "In one small Chennai hospital study, only six percent of patients used their spirometer properly the day after surgery. With teaching, seventy-two percent did by day three. That was in hospital; we found no Indian data on practice at home."
Evidence: KB:971-975, PF:11. Say "percent", never a head-count. The study used a ball-type device.

**4. Mixed evidence.** "Evidence that this exercise alone prevents lung complications is mixed, so we measure follow-through first and claim no health benefit."
Evidence: KB:84-87, KB:263-272, PF:50, DECK:49-50.

**5. Informal nurse feedback.** Exact sentence (NF:42), spoken by the team member whose mother it is:
"Feedback from a nurse in my family highlighted confusing discharge instructions, forgotten medicine schedules, uncertainty about breathing exercises and limited time for repeated coaching. Patients may also skip exercises when they hurt. Our prototype responds with a readable care plan and check-ins that ask why help is needed, then bring concerns to the nurse."
If the other teammate speaks: "a nurse in a team member's family". Short cut: "Informal feedback from one nurse in my family: patients may skip breathing exercises when they hurt, forget medicine schedules and find discharge papers confusing."
Evidence: NF:7, NF:11-16, NF:42.

**6. InSee and record apps.** "Health-record apps such as Aarogya Setu 2.0 and Eka Care hold records and reminders. InSee, a US breath tracker, is FDA-cleared for hospital use only. We join the doctor's plan, dose reports and breathing coaching on one hospital record."
Evidence: docs/plan/11_HOME_RECOVERY_COMPANION.md:19, 86-87; KB:127-132; KB:288-291; PF:32.

**7. App language.** "The screen's labels, times and food words are in Hindi here. English, Tamil and Malayalam are the other screen languages. What the doctor typed is shown as typed, not translated."
Evidence: F:226-227; web/js/meds-core.js:12, 47-48; H:28, H:51; docs/CODEX_DISCHARGE_HANDOFF.md:85. The care-instructions page (s6) is English only.

**8. Device.** "SpiroBuddy is our optional breathing module, designed to clip onto an ordinary piston-type incentive spirometer. In our design, a laser distance sensor would read how high the piston rises, and a small controller would send it by USB cable to the web app in Chrome or Edge on a laptop. The firmware and the 3D design exist; no unit has been built or tested. Bluetooth to the phone is planned."
"Calibration against each model's printed marks would estimate the volume. It coaches practice; it is not a lung test."
Shot s7a: "This is where the unit would connect. No unit exists yet, so a simulator stands in."
Evidence: F:212-217; firmware/spirobuddy_serial/spirobuddy_serial.ino:4-5; web/js/sources.js:3, 72-75; web/js/breath.js:2, 29; KB:592, 848-851.

**9. Pilot targets.** "In a proposed one-ward pilot, twenty patients over fourteen days, we would measure activation: patients viewing their plan within forty-eight hours, illustrative target eighty percent of enrolled patients. And day-seven return: illustrative target sixty percent of activated patients. These are targets, not results."
Evidence: DECK:239-256.

**10. Price and who pays.** "The hospital is the buyer, at a proposed, unvalidated thousand rupees per follow-up episode. We have no paying customers, and we do not charge patients."
Evidence: DECK:218-220; PF:46; CLAUDE.md. Do not speak ₹2,500: the deck calls it a selling price (DECK:233-235), the research a parts cost (PF:46).

**11. Hospital records, patient module, hospital branding.** "Every record carries its hospital, and the app checks it on each request. The breathing module is switched on per patient. Each hospital sets its own app name, logo and accent colour; safety messages and status labels stay fixed."
Shot s10: "The admin previews a new accent colour, then undoes it. Nothing is saved."
Evidence: F:84-87 (scoping Live in the app layer; database rules Planned); backend/app/routes_patients.py:66-70, 77; H:22; F:126-128 (branding Live); backend/app/branding.py:4-10, 34; web/branding.html:72, 115-119. The accent colours only the name strip. New modules are the expansion plan (DECK:205).

**12. Roadmap.** "Next, as targets and not commitments: ward usability checks and device bench tests in ninety days, and a reviewed patient pilot by six months."
Evidence: DECK:281-290.

**13. What production still needs.** "Before real use we still need database transactions, shared rate limits across servers, and real SMS." Optional: "and database-level rules per hospital."
Evidence: H:142, H:144, H:146; DECK:214; F:86-87; F:124-125. The site already runs on Supabase (H:92; backend/app/store.py:4-5; DECK:159).

**14. Regulator (CDSCO).** Supported by our own research, with a hedge: "Because nurse alerts probably make this medical-device software, we would ask the regulator, CDSCO, for a ruling before any real patient use."
Evidence: KB:825-834 (alerting software is not wellness); KB:353; KB:358; KB:1080-1090 ("CDSCO decides"); PF:52. Keep "probably". Never state a device class as fact.

**15. Login code.** "Kamala logs in with her hospital number and a one-time code. The code is real: single-use, and it expires in ten minutes. Only its delivery is simulated; it shows on screen instead of an SMS."
Evidence: F:122-125; H:26; web/patient-login.html:4.

**16. Prescription draft.** "She types the prescription and prepares a draft. No AI is used here; it is a manual-format draft. Anything the draft cannot fill, like food timing, is marked 'Needs review', and she must choose before she can send it."
Evidence: backend/app/meds/notepad.py:27-47, 53; web/js/meds-prescribe.js:106, 313, 317; F:148-151. The manual format has no food field: "Before breakfast" lands in the note box, so line 2's food field also needs a choice. Never say "only one field".

**17. Pharmacy screen.** "She can show this screen at the pharmacy counter. The QR lets the chemist check it against the hospital's copy."
Evidence: F:142-147; web/js/meds-patient.js:238-239 (the screen says "Not for dispensing").

**18. Beds and overview.** "The hospital admin admits her to a bed, and the overview counts come from those recorded bed operations."
Evidence: F:102-107. Say "admin", not "department" (department login is Planned).

**19. Care document.** "The doctor publishes the instructions she wrote. Kamala taps 'I have read this version'. That records reading, not consent."
Evidence: H:49-51; H:146.

**20. Visit.** "Kamala asks for a visit and picks a time. The doctor confirms it on My day, and her phone shows Confirmed."
Evidence: F:135-136; F:184-189 (in-app only; nothing is sent).

**21. Breathing session.** "The coach gives feedback on each simulated breath. This short session is saved as partial; a complete one needs ten valid breaths."
Evidence: F:204-209; backend/app/service.py:270-271, 285; H:31; web/app.html:373. Labels come from a model trained on simulated breaths, or fixed rules (backend/app/models_ml.py:1).

**22. Scripted simulated call.** "Next, a simulated check-in call in Hindi. No real phone call is placed. The assistant's lines are fixed, scripted text, and the presenter taps preset sample answers. Kamala's consent for automated calls is recorded on her chart."
"The sample answer reports mild pain near the stitches, and asks for a callback."
Evidence: backend/app/comms/sarvam.py:113-146, 149-157; web/js/phone-sim.js:31; backend/app/routes_comms.py:406-409; F:292-293; H:96; H:134.

**23. Nurse alert.** "Fixed keyword rules, not AI, raise the nurse alert. Sister Anjali reads what was reported, assigns it to herself and acknowledges it."
Evidence: sarvam.py:176-186, 195, 286-306, 347-356; F:98-99; F:286-287.

**24. "Runs live" scope and what is simulated.** "Every product screen you saw was recorded on our public site, with fictional patients. Simulated: the login-code delivery, the breaths and the call. Not built: the device. No AI wrote anything you saw."
If WhatsApp bubbles show in s9a, add "and the WhatsApp messages" (F:290-291).
Evidence: H:5; H:150; F:122-123; F:204-213; F:282-283; F:292-293.

**25. Optional AI line.** "AI drafting is in development. It is optional, needs the patient's consent and a doctor's review, and never diagnoses." (F:150-151; F:250-251; H:24-25.)

**26. ICMR ethics guidance.** "Our design is informed by ICMR ethics guidance, not approved by ICMR." Pair it with "Before real use we still need ethics committee review". Say I-C-M-R as four letters; do not speak the years.
On screen: the live Trust page's ICMR 2017 rows Privacy (Live) and Ethics committee review (Planned), the ICMR AI-in-health 2023 table (Human oversight, Accountability, Audit: In development; Transparency: Live) and "Not reviewed or approved by ICMR, an ethics committee or CDSCO." Card: "Ethics committee review · Full ICMR assessment pending · Planned".
Evidence: docs/ICMR_ETHICS_CONTEXT.md (approved statement: "informed by ... No ICMR approval, certification or full compliance is claimed"); web/data/trust.json (rule_groups 1-2; checklist steps 4 and 11); live /trust.html sections 1, 4, 5; deck slide 15 ("ICMR ethical guidance informs the design ... Full assessment and applicable ethics review remain pending"). Never show the "Vulnerable participants" row: it says the patient screens take no typing, and the video shows typing.

---

## 2. NEVER SAY

| Phrase | Why |
|---|---|
| "at home… only six in a hundred"; "At home, nobody teaches" | In-hospital study (KB:975); unsupported absolute. |
| "one in ten Indian patients" | Mostly European hospitals (KB:77). |
| "prevents lung complications", "faster recovery", "fewer readmissions", "saves nurse time" | Not measured; evidence mixed (KB:84-87, 269; NF:48). |
| "we interviewed nurses", "our research", "a study", "nurses told us" | One nurse, second-hand, informal (NF:7, 46). |
| "InSee works / is used in US hospitals" | Only FDA clearance is documented (KB:127-132). |
| "no one else does this", "first", "our laser sensing is new" | Record apps and InSee exist (KB:291; CLAUDE.md). |
| "in the patient's language" with no limit; "the prescription / care plan is translated" | Interface words only (F:226-227; H:51). |
| "the sensor reads… sends… calibration estimates" (present tense) | No unit built or tested (F:212-213). |
| "connects to her phone by USB" | Laptop Chrome or Edge only (sources.js:75); Bluetooth Planned (F:214-215). |
| "works with any spirometer" | Piston type only (F:216-217). |
| "measures lung function", "the device measured this breath", "accurate" | Not a lung test; breaths simulated (F:204-205). |
| "session complete", "exercise done" | Saved as partial (service.py:271). |
| "eighty percent of patients" as a result, or without "of enrolled / of activated" | Illustrative targets (DECK:242-256). |
| "patients never pay", "free for patients" | We cannot promise what a hospital bills. |
| "modules switch on per hospital" | Breathing is per patient (routes_patients.py:66, 77). |
| "the whole app takes the hospital's colours", "this hospital's logo" | Name strip only; no logo shown, nothing saved in s10 (branding.html:72). |
| "needs a shared database", "production-ready" | Already on Supabase (H:92); readiness not claimed (H:144). |
| "CDSCO-approved", "no licence needed", "it is Class A/B" | No ruling exists (PF:52, PF:58). |
| "ICMR-approved / certified / endorsed / validated", "ICMR-compliant", "complies with ICMR", "follows all ICMR guidelines" | Guidance informs the design; no assessment or approval exists (docs/ICMR_ETHICS_CONTEXT.md). |
| "ethics approval obtained", "ethics-cleared", "an ethics committee reviewed it", "study / pilot done" | Ethics committee review is Planned (trust.json; /trust.html section 5). |
| "the ICMR checklist is done", "full ICMR assessment" | The 17-item ICMR AI checklist is a Planned pilot step (trust.json checklist step 4). |
| "the patient screens take no typing" | Kamala types her hospital number and code in s5a (the Trust page row is wrong on this). |
| "the code is simulated", "an SMS was sent" | Real code, simulated delivery (H:26). |
| "the AI drafted this prescription" | Manual-format draft (notepad.py:53). |
| "tap I took it", "she took her medicine" | No dose is tapped in v4; a tap means reported (F:172-173). |
| "the chemist dispenses from this screen", "used at pharmacies" | "Not for dispensing"; not tried with a real pharmacy (F:144). |
| "AI call", "the AI asks", "a real call", "Sarvam called her" | Fixed text in a simulator (sarvam.py:113-157; H:96). |
| "her own words", "Kamala says" | Preset answers tapped by the presenter (sarvam.py:149). |
| "the AI alerts the nurse" | Keyword rules (sarvam.py:176-186). |
| "everything you saw runs live", "fully working" | Slides and the render are not software; notepad and line review are In development (F:150-151, 158-159). |
| "used by", "pilot done", "users", "partner hospital", "customers" | None exist (H:11; DECK:220). |
| "every patient's phone", "works without a smartphone" | No-phone base Planned (F:218-219; KB:166). |

---

## 3. ON-SCREEN TEXT RULES

**Problem statistic cards (number · line · source line).** Each appears only when its number is spoken.
1. **49 lakh** · "major operations a year in India's public records" · Source: "Int J Surg 2024 · 2019 data · an undercount" (KB:149-152)
2. **1 in 10** · "adults having surgery had a lung complication" · Source: "LAS VEGAS study, Eur J Anaesthesiol 2017 · 9,864 patients, 146 hospitals, 29 countries, mostly Europe" (KB:74-77)
3. **6% → 72%** · "used their spirometer properly on day 1 after surgery; 72% by day 3 with teaching (in hospital)" · Source: "Small Chennai study, 60 inpatients · J Pharm Bioallied Sci 2024 · No Indian home-use data found" (KB:971-975)

**Nurse feedback label (exact, NF:36):** "One nurse's informal feedback, relayed by a team member; additional themes confirmed by phone according to the team member, 12 October 2026."

**Device image tag:** "3D concept render · not built", on every frame showing the render, including the cover. Never "Device concept (simulated)" alone.

**Call scene labels**
- Role bar: "Doctor · call simulator" (not "Patient").
- Phone tag: "Kamala's phone (simulated) · no real call".
- Assistant subtitles: "Automated assistant (simulator, scripted · Hindi):"
- Reply subtitles: "Kamala (preset sample answer):"
- Translate the greeting faithfully: "this is SpiroBuddy's automated care assistant, calling from the hospital" (backend/app/comms/common.py:276).
- Nurse inbox caption: "Raised by fixed rules, not AI".

**Other captions**
- Login: "Real code · simulated delivery (no SMS)".
- Prescription: "Manual-format draft · no AI"; zoom on "Needs review" for 2 seconds.
- Medicines: "Hindi screen labels · medicine names as the doctor typed them".
- Breathing: "Simulated breaths · saved as partial (complete = 10 valid breaths)".
- Branding: "Preview only · not saved".
- One "Sample patient" line per scene; do not repeat "demo" (CLAUDE.md).
- Chapter chips use the organisers' exact criterion names (for example "MVP / Prototype", "Solution Quality").

**Cover tagline:** "Connecting hospital care to the patient's phone." (not "every patient's phone"). Name as in the deck: "Aarogya Saathi, with the SpiroBuddy breathing coach".

**End-card status line:** "Live · Simulated · In development · Planned: every feature on our status list carries one of these labels." Second line: "Fictional patients only · Device not built · spirobuddy.onrender.com" (F:19-21; F:212-213).
