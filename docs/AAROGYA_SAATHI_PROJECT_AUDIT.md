# Aarogya Saathi / SpiroBuddy — product and implementation audit

**Implementation update:** this is the assessment before the subsequent fixes. See [CODEX_IMPLEMENTATION_HANDOFF.md](CODEX_IMPLEMENTATION_HANDOFF.md) for the new registration, OTP, notes, reviewed notepad, medicine alerts, patient AI consent, corrected deck and current verification/deployment status.

**Audit date:** 12 October 2026 (IST)
**Live site:** https://spirobuddy.onrender.com/
**Basis:** the founder's request in this chat, `CLAUDE.md`, project plans and source, and direct inspection of the deployed website.
**Purpose:** explain what exists, what does not, what feels disconnected, and what to build next. This audit does not change application code or deploy anything.

## 1. Overall verdict

There is a useful foundation here, but it is **not yet the complete hospital management platform you described**. It is currently a SpiroBuddy breathing-care prototype with staff authentication, a patient phone web app, a breathing triage dashboard, simulated communications, a strong device visualization, and a structured digital prescription module.

The five connected workspaces — hospital, department, doctor, nurse and patient — do not exist as five completed experiences. The department account is especially important: it is the missing operational link between patient registration, beds, doctors, nurses and device updates.

The main problem is not that everything Claude built is meaningless. Much of it is reusable. The problem is that the product changed direction repeatedly while old documents, old screens, new foundations and unfinished plans accumulated. A visitor sees a polished breathing story, while you expect a connected hospital platform. Those are different levels of scope.

Three conclusions should guide the next work:

1. Preserve the breathing engine, permissions, prescription data model and useful patient UI patterns.
2. Build one complete journey through all five roles before adding more peripheral features.
3. Bring the deployed site, feature labels and project instructions into agreement. Local implementation is not the same thing as deployed functionality.

## 2. What I understand your intended product to be

For this report, **Aarogya Saathi** is the overall platform and **SpiroBuddy** is its incentive-spirometer module. Earlier files spell the platform name “Arogya Sathi”; this report uses your latest spelling without renaming the application.

The intended journey is:

1. A hospital has its own organization, departments, staff and branding.
2. Staff register a patient under the hospital's own registration number, with their name, contact details and relevant clinical information.
3. The patient is assigned to a department, doctor and, where appropriate, a room or bed.
4. The doctor records a consultation and writes a prescription. Your latest request adds a notepad-style input that AI converts into structured prescription fields.
5. A doctor reviews that conversion before it becomes the patient's medication plan.
6. The patient enters their hospital registration number and verifies an OTP delivered to the phone number already recorded by the hospital.
7. The patient's phone shows the confirmed medicines, their prescribed schedule, relevant records and help options.
8. If assigned a spirometer, the patient can use the SpiroBuddy module from the same app.
9. The attachment measures the moving piston/disc in a volumetric incentive spirometer. Calibrated readings drive coaching and exercise records.
10. Usage and relevant exceptions become visible to the responsible department and assigned nurse. The hospital receives an appropriate overview.

“Five pages” should mean **five role workspaces**, each with a few purposeful screens. Trying to place registration, prescriptions, bed management and every history on five giant pages would recreate the current clutter.

This scope does not presently include billing, insurance, laboratory operations, theatre management or every other hospital module. Your own project instructions explicitly exclude payments from hospital and patient workflows. The immediate goal should be a coherent patient-care platform with a credible path to broader hospital management.

## 3. How the evidence was evaluated

I read `CLAUDE.md` first, then `START_PROMPT.md`, `docs/HANDOFF.md`, `docs/PROGRESS.md`, `docs/REQUIREMENTS.md`, `docs/ARCHITECTURE.md`, `docs/rebuild/STATE.md`, the OTP brief, the whole-platform plan and relevant implementation files.

Code discovery began with the codebase knowledge graph. Its initial index lacked newer auth, branding and prescription files, so I refreshed the index before relying on it. I inspected specific symbols and callers, then read the relevant files where the graph was insufficient.

The live review covered the landing page, staff login, doctor sign-in, dashboard, Ravi's chart, prescription workspace, patient app, medicines page, patient-login URL, units screen, Impact, Trust, Vision, Architecture and 3D showroom. I inspected rendered text and selected screenshots. I did not submit prescriptions, send messages, reset the shared demo, change branding or edit live patient records.

The status terms below are deliberately more precise than a single “built” label:

| Audit term | Meaning |
|---|---|
| Observed live | The deployed page visibly showed the capability during this audit. |
| Implemented locally | Relevant source exists in this checkout; this alone does not prove it works on Render. |
| Partial foundation | Some storage, helper, API or UI work exists, but the user journey is incomplete. |
| Simulated / mock | The experience uses generated data, simulated delivery or browser-only state. |
| Missing from inspected implementation | No completed route/workspace was found in the relevant current code. A design document is not implementation. |
| Not verified | Needs an execution, device, provider or scenario not completed in this audit. |

**Limits:** this is a product and implementation audit, not a clinical, legal, penetration-test or physical-device validation. Medical statistics and legal statements copied into public pages were reviewed for presentation and consistency, not independently revalidated. Existing historical test counts are not treated as new test results.

## 4. The instructions disagree with one another

### 4.1 The original prompt describes a smaller product

`START_PROMPT.md` and older `REQUIREMENTS.md` focus on a nurse/doctor breathing website, simulator, showroom and videos. They explicitly set aside the patient app. Later work built that app anyway, and the founder's platform plan expanded the scope much further.

It would be unfair to call the original breathing dashboard a failed complete hospital system: it was initially designed for a much narrower problem. It is fair to say that the expanded platform has not yet been delivered.

### 4.2 OTP has replaced PIN in the intended design, but not the code

The latest founder decision at the top of `CLAUDE.md` requires registration number + OTP. The older sections still recommend registration number + PIN and describe SMS OTP as later work.

`docs/rebuild/REGNO_OTP_BRIEF.md` explicitly supersedes the PIN brief. It specifies simulated OTP delivery first, with real SMS later. However, current `routes_me.py`, `patient_login.py` and `web/js/patient-login.js` implement **PIN login**, not OTP request and verification. There is no current `patient_otp.py` module or OTP test file in the inspected directories.

The PIN is reusable until replaced; it has lockout protections, but it is not the intended single-use, expiring desk code either. Calling it a one-time desk code today would be incorrect.

### 4.3 Your notepad + AI request changes an earlier prescription decision

An earlier founder decision in `CLAUDE.md` deliberately prioritizes structured doctor typing and says AI photo reading is not the headline. The deployed prescription form follows that decision.

Your latest request asks for **free-text notepad input → AI extraction → patient prescription**. That supersedes the older product preference, but does not make the existing form useless. It should become the manual fallback and the review interface for extracted lines.

Photo/PDF extraction and free-text notepad extraction are separate capabilities. A helper that can read a prescription image does not prove that the new notepad flow exists.

### 4.4 Handoff and build-state records are stale

`HANDOFF.md` contains claims such as “no login needed” and “patient app set aside” alongside later accounts of authentication and a patient app. `STATE.md` also includes old “not redeployed” language and rows that do not fully reflect newer local files. The feature registry still marks PIN login as being built while its source already exists.

**Recommended correction:** maintain one short, authoritative current-scope document with the latest decisions and one deployment record with commit, migration state, verification date and known gaps. Keep older plans as history, clearly marked superseded.

## 5. Feature matrix against the five workspaces

| Requirement | What exists | Verdict / gap |
|---|---|---|
| Hospital organization and data separation | Hospital IDs, scoped staff permissions and isolation tests | Useful foundation; not a full hospital workspace. |
| Hospital-wide patient list | Admin permission can see hospital patients; shared dashboard exists | Breathing-oriented list, not a complete inpatient/outpatient registry. |
| Admission / discharge counts | Discharge fields and recovery-oriented records | No completed admission/checkout lifecycle or operational dashboard found. |
| Occupied / free beds | Ward and bed text on sample patient chart | No working bed inventory, allocation, transfer or availability board. |
| Hospital branding | Local branding backend, page, logo validation and patient integration | Implemented locally; live pages observed still show old identities. |
| Department login | Staff department field and platform plan | Department role/workspace missing. A string field is not department authorization. |
| Department registration | Specified in platform plan | No completed registration page or `POST /api/patients` in inspected current routes. |
| Department device updates | Breathing sessions and staff triage | No department-specific routing, inbox or summary. |
| Department roster / assignments | Planned in platform document | Missing duty roster, room assignment and task workflow. |
| Doctor login | Live demo sign-in and scoped patients | Exists. |
| Doctor consultation record | Patient breathing chart, AI summaries, settings | Not a general encounter note or consultation workflow. |
| Doctor enters patient details | Existing seeded details; narrow update endpoint | No complete registration/demographic/condition editor. |
| Hospital registration number | Local MRN generation, edit and PIN login helpers | Local foundation; live patient-login page returned 404. |
| Structured digital prescribing | Live form and local prescription/dose service | Exists; patient sample currently has no prescription. |
| Free-text notepad + AI conversion | Image/PDF extraction helper exists | Requested free-text flow missing. |
| Doctor review of AI extraction | Plans, permissions and helper work | No connected review-and-approve UI for this requested flow. |
| Doctor's day / appointments | Schema/plans and registry entries | Completed scheduling journey missing. |
| Nurse login and patient scope | Auth and access grants | Backend foundation; live workspace remains shared triage screen. |
| Nurse phone duty/tasks/rooms | Platform plan | Missing. |
| Nurse breathing alerts | Live alerts inbox, chart, fixed rules | Strongest staff-facing working module. |
| Patient phone web app | Live app, large buttons, languages, breathing gauge | Exists as a web app, not a verified store app. |
| Patient MRN + phone OTP | OTP brief only; local PIN flow | Required OTP flow missing. |
| Patient sees prescription and schedule | Medicines and pharmacy interfaces; dose APIs | Implemented; audited live sample is empty. |
| “I took it” tracking | Local dose-report routes and UI | Implemented as reported adherence, correctly not sensor evidence. |
| Spoken due/missed medicine reminders | Registry says In development | Complete proactive reminder loop missing. |
| Reminder when app closed | Registry says Planned | No verified push/store notification journey. |
| Patient prescription PDF | Pharmacy card and staff chart print exist | No dedicated verified prescription PDF flow found. Chart print is a different artifact. |
| Documents / reports | Schema, storage helpers and plans | No completed patient document-vault journey. |
| Assigned-device-only Breathing tab | Patient app has breathing as its main screen | Required modular home/tabs missing. |
| Real optical measurement | Firmware, calibration/detection code, 3D concept | No physical build or bench evidence established. |
| Bluetooth patient phone connection | Planned | Current firmware is USB serial. |
| Unit inventory shared across staff/phones | Browser-local mock units | Not a server-backed device fleet. |
| Family updates | Family page and communication simulators | Useful supplementary module; real delivery not established here. |

## 6. What the live website actually showed

### 6.1 Landing page

The story is easy to understand as a hospital-to-home breathing product. The two pillars — exercise records and prescriptions on the phone — are related and worth keeping.

However, the live headline was “After surgery, the hospital stays connected to the patient at home,” while the current local instructions prescribe “Every breath, coached and counted.” The live site still refers to Demo General Hospital, whereas current local instructions use Dawnlight General Hospital.

There are no clear entry points for all five roles. “Hospital login” leads to a generic staff login, and the patient link opens a sample directly.

The phrase “shows that the breathing exercise was really done” is stronger than what a simulator demonstrates. Even a future piston reading should be described in terms of recorded movement and exercise evidence, with explicit provenance, rather than guaranteed correctness or patient identity.

### 6.2 Staff login

The login page has working-looking fields and one-click fictional admin, doctor and nurse accounts. I signed in through “Try as Doctor” and reached the dashboard.

The page links to doctor signup and nurse key redemption. Current local web files do not contain `signup.html` or `redeem.html`, and the registry marks those journeys In development. These are exposed entry points without a completed local destination; the live destinations were not separately clicked during this audit.

The page does not offer department login. It does not make the difference between a hospital administrator and a department coordinator clear.

### 6.3 Doctor dashboard

Doctor sign-in opened a **breathing triage dashboard**, with four visible patients in this doctor's scope. That is useful evidence of a scoped patient list; it is not evidence of a complete hospital list.

The dashboard showed ten open alerts, nine red and one amber. At the time of observation, no sessions were due yet today, while the status explanation drew on yesterday's missed sessions. The dashboard does explain the before-8-am rule, but the mix is still difficult to interpret at a glance.

The header says “Demo City Hospital,” differing from the login and public site. The alert inbox “I am” selector defaulted to **Sister Anjali**, despite signing in as the doctor. The chart's calling identity also said Sister Anjali. This undermines confidence in who owns the work.

There was no visible doctor day list, register-patient action, consultation entry, department summary or bed board.

### 6.4 Ravi's staff chart

The chart displayed age, sex, operation, postoperative day, ward/bed, language and family. It had hourly exercise slots, seven-day volume history, breath quality, recent sessions, AI summary, WhatsApp actions, voice preferences, care circle, escalation history and settings.

These are relevant to breathing follow-up. Together, they create an extremely long page. Consultation context and prescribing are visually secondary, while messages and simulated escalation logs occupy substantial space.

The “Medicines” link opens the prescription workspace. The local general patient update endpoint accepts target volume, hold target, language and family phone; it does **not** implement the comprehensive name/age/condition/registration editor described in your request.

### 6.5 Prescription workspace

The deployed form asks for medicine name, strength, form, amount/unit, morning/afternoon/night or a frequency code, food timing, duration, SOS status and instructions. This is a sensible structured prescription editor.

“Send to the patient's phone” means saving and issuing the prescription into the shared system. It is not proof of an SMS, WhatsApp delivery or push notification.

There is no notepad-style prescription input or AI conversion button. The source explicitly says this route has no AI or photo upload.

Ravi's current medicines showed **“No current prescription.”** The patient's medicines screen also showed no medicine yet. This is a concrete demo-data gap, not proof that the prescribing backend is broken. I did not issue a prescription into the shared live database as part of this read-only audit.

### 6.6 Patient phone app

The patient page is visually coherent: a compact column, large exercise button, piston gauge, coaching text, four language choices, exercise checklist, medicines link and unwell button. This is worth preserving.

It is still a **SpiroBuddy-first screen**. A patient whose main need is medicine or follow-up must look past the breathing module. There is no implemented Today / Medicines / Breathing / Help navigation with Breathing conditional on a server-backed assignment.

The app is a mobile web app. Store publication and real native Bluetooth operation have not been demonstrated.

Navigating to the known local patient-login path on Render returned **404: Not Found**. Therefore the new registration-number login page is not available on the inspected deployment, regardless of its local source.

### 6.7 Units page

The page honestly explains that it is a mock-up and its list lives only in the current browser. It illustrates handover, return, cleaning and reuse well.

That storage choice cannot support the real workflow. A nurse handing out a device on one phone does not thereby assign it on the patient's separate phone or the department's computer. The sample battery and last-seen fields are mock values, not telemetry.

Keep this page as a design reference, then connect a real fleet/assignment model on the server.

### 6.8 Public Impact, Trust, Vision and Architecture

These pages show considerable effort to distinguish assumptions, targets and demo results. That is a strength.

But they read partly like internal research documents. References such as “PITCH_FACTS #…,” “plan 11,” “R19” and “B1-13” do not help an ordinary visitor locate an external source. They should become readable titles and links, with internal reference IDs kept in the repository.

There are specific contradictions:

- Vision says QR checking is still in development, while Medicines labels it Live.
- Trust says all ten medication rules live in code, but missed-dose nurse escalation is still In development in the registry.
- Trust discusses sample-prescription uploads as though the upload screens are available, while the current prescription routes implement structured typing only.
- Architecture labels Anthropic and Sarvam voice Live, while the observed staff chart says browser voice is being used because no Sarvam key is available. A working fallback does not demonstrate that an external provider is running.
- Architecture describes visits and papers within the patient app, although those completed patient journeys are not present.
- Vision retains the narrower recovery-product and tier story rather than clearly presenting the latest five-role platform.

A status badge cannot repair a sentence that already implies an unfinished workflow works today.

### 6.9 3D showroom

The showroom is a strong concept demonstration. It rendered the volumetric spirometer, underside attachment, illustrative phone, laser annotation, camera views, breath controls and guided-tour controls. I exercised the Good control and inspected the model visually.

It communicates the mounting idea better than paragraphs alone. It also correctly says the beam is drawn for illustration and identifies the model as a concept.

It is not a connected patient digital twin. Its movement and readings come from the model, and its phone screen is illustrative. Do not interpret the model's geometric distance as evidence that the physical sensor can reliably read through the actual spirometer base.

## 7. What Claude built well

### 7.1 A useful software seam between device and app

Firmware emits distance readings over serial; the browser can convert readings through calibration, detect breath phases and produce features; the backend records sessions and classifies breaths. The simulator lets development continue before hardware exists.

This separation is a sound foundation for replacing simulated input with measured input later.

### 7.2 A practical nurse breathing view

The triage list, explanations, history and fixed-rule alert inbox answer a real question: who needs attention after discharge? These are better than a dashboard containing only attractive charts.

### 7.3 Structured digital prescriptions

The prescribing service separates prescriptions, items and dose events. Doctor saving is treated as sign-off. There is support for current, replaced and stopped prescriptions, and SOS lines are excluded from ordinary scheduled events.

The patient report is recorded as **reported**, rather than claiming medicine ingestion was measured. Keep that distinction.

### 7.4 Authentication and hospital scoping foundations

The project has staff sessions, role permissions, scoped patient access, hashed credentials/tokens, audit infrastructure and tests addressing isolation. These are important building blocks for the larger product.

However, these foundations do not by themselves complete department permissions, database row security or every clinical workflow.

### 7.5 Patient presentation and fallback work

Large controls, localized text, voice support and a simple breathing gauge are appropriate design choices for a phone experience. The app tries to remain demonstrable without paid providers or hardware.

### 7.6 Honest physical-device status

The current instructions clearly say the unit is not built or bench-tested. The firmware and showroom are supporting artifacts, not presented as a completed physical trial. Preserve that honesty.

## 8. What is incomplete or does not connect

### 8.1 There is no normal way to begin with a new patient

The strongest screens start from seeded Ravi. The intended platform starts from registration. Without enrollment, the story cannot connect an actual new hospital number to a doctor, prescription and patient login.

**Needed:** create/find patient, enter MRN and phone, assign department/doctor, record the relevant status and then continue to prescribing or device assignment.

### 8.2 Departments are labels rather than operational entities

The current authorization roles are admin, doctor, nurse and patient. Department is a staff field, not a completed account and access boundary.

**Needed:** an explicit department entity, membership and coordinator permissions; scoped registration, bed board, nurse assignments and device follow-up.

### 8.3 The hospital view does not have hospital operations

Recovery patients and breathing slots cannot generate a reliable bed occupancy count. Text saying “Ward 3B · Bed 11” cannot tell you whether that bed is now occupied, reserved, under cleaning or available.

**Needed:** beds and admission/transfer/discharge events, with one authoritative current allocation and history.

### 8.4 Doctor work and breathing exercise sessions are different things

`sessions` currently means breathing sessions. It should not become a table that also vaguely stores doctor consultations.

**Needed:** separate encounter/consultation records with author, patient, date, status, notes and linked prescription. Clarify whether “record the session” means clinical notes, audio recording or transcription; no verified doctor audio workflow exists today.

### 8.5 An AI helper exists without the requested user journey

`ai_gemini.extract_prescription` is an image/PDF drafting helper. Graph caller tracing found no connected application caller for that extraction function. Current medication routes do not use it.

**Needed:** free-text extraction endpoint, review state, structured edit screen and explicit doctor approval. Do not silently convert generated text into a live medication schedule.

### 8.6 Prescription schedule display is not a complete reminder system

The dose service can produce events and show statuses. The registry still calls the proactive voice card and missed-dose nurse alert In development, and push/offline reporting Planned.

**Needed:** a due-event processor, deduplicated reminder/alert events, acknowledgment, consent-aware delivery and clear behavior when the app is closed or disconnected.

### 8.7 Browser-local units break the cross-phone story

Local storage is fine for a clearly marked mock, but cannot be the source of truth for equipment loaned by a department.

**Needed:** device ID, assignment owner, assignment dates, readiness/calibration state and telemetry stored on the server. Pairing must resolve against that assignment.

### 8.8 The current screens do not reliably tell you who you are

A doctor sees a nurse identity selector and a different hospital name. The legacy dashboard shell is not the role-aware hospital shell present in `ui.js`, which only activates for `/hospital/` pages. Those planned pages are absent from the current web directory.

**Needed:** one visible authenticated identity and hospital/department context on each staff screen. Assigning an alert should use the logged-in actor; changing its owner should be a separate, permission-checked action.

### 8.9 Peripheral depth arrived before the core journey

Family cheers, IVR ladders, research pages, tour controls and long communication logs can all be useful. They feel disconnected when patient registration, department work and medicine reminders are unfinished.

Do not delete them blindly. Move them behind appropriate tabs and prioritize the core care journey before expanding them.

## 9. Technical findings that matter to the product

### 9.1 Session completion is too permissive in the inspected source

`POST /api/sessions` checks patient visibility and the shape of the breaths list. `service.record_session` then creates a session and marks the hourly slot done even if the cleaned breaths list is empty. There is no ten-breath completion requirement in that function.

This is a **source-confirmed validation gap**, not a live exploit tested in this audit. A client can also submit a recognized label, numeric score and a source string; the service accepts those values rather than always deriving trustworthy classification/provenance itself.

**Why it matters:** the key promise is evidence of exercise. A completed slot must have explicit completion criteria and cannot rely solely on an arbitrary client assertion.

**Fix:** distinguish partial/completed sessions, validate minimum accepted breaths and timestamp rules, derive score/label as appropriate, and record trusted input provenance. A simulator may complete a simulated exercise, but it must remain identifiable as simulated.

### 9.2 Patient app input provenance is currently weak

The current `app.html` posts `source: 'app'` for its saved session. This does not distinguish simulator input from USB measurement. The service only accepts `demo`, `device` or `app`, and a client can choose those strings.

**Fix:** carry input type and device/assignment identity through the measurement path. For a physical device, add pairing/session verification appropriate to the chosen architecture. Do not equate a source field supplied by a browser with authenticated device evidence.

### 9.3 Offline demo fallback is not offline patient care

`api.js` can switch to a browser mock when the health check fails. The service worker deliberately does not cache API responses. The mock state contains fictional patients and mock interactions.

This supports a resilient demonstration, but does not establish access to the authenticated patient's last real prescription or an offline queue for adherence reports. The registry's “Last data when offline” wording needs closer validation.

**Fix:** show offline and sample-mode states distinctly. If offline care is supported later, cache only the explicitly approved patient data, scope it to the session, clear it on logout and queue writes with deduplication.

### 9.4 Registration numbers must be resolved inside a hospital

The current PIN login searches MRN candidates across patients and then checks PINs. MRNs are intended to be unique per hospital, not universally unique. This becomes particularly problematic for OTP request: the user provides the number before there is a second factor to select the right record.

**Fix:** resolve the hospital from a hospital-specific link/QR, a hospital code or an explicit selection. Login identity should be `(hospital, registration number)`. Never choose arbitrarily between patients with the same MRN at different hospitals.

### 9.5 PIN work is valuable but should not be relabeled as OTP

Argon2 hashing, attempt limits and staff MRN editing are useful reusable code. They do not supply challenge expiry, resend limits, phone delivery or single use.

**Fix:** build the OTP adapter and challenge lifecycle specified in the brief. Separately add expiration and consumption to the desk-code fallback if it is meant to be one-time.

### 9.6 Multi-step prescribing deserves failure and concurrency checks

Prescription creation writes a draft, item rows and current status, cleans up some failures, then updates replaced prescriptions and refreshes doses. That is useful defensive work, but the sequence is not evidence of a single atomic transaction across all supported stores.

**Fix:** verify failure between each major step, simultaneous replacement and repeated submission. Avoid duplicate current versions or a visible prescription with an inconsistent schedule. Add an idempotency key and transactional behavior where the storage layer supports it.

### 9.7 Database foundations do not equal implemented features

Appointment tables, document tables, permission names and contract sections are useful preparation. They must not be counted as working bookings, a document vault or a department account until routes, permissions, screens and end-to-end tests exist together.

## 10. Recommended shape of the five workspaces

| Workspace | Main question answered | Primary screens / actions |
|---|---|---|
| Hospital | What is happening across this hospital? | Patient registry, department totals, admissions/discharges, bed availability, staff and branding. |
| Department | Who is here and what needs coordinating? | Register patient, admissions/bed board, doctor and nurse assignments, department alerts, device follow-up. |
| Doctor | Who am I seeing and what care have I prescribed? | My day, patient record, encounter notes, notepad/extraction review, prescriptions and follow-up. |
| Nurse | What do I need to do on this shift? | Assigned patients/rooms, tasks, prioritized alerts, handover; device setup under More. |
| Patient | What should I do now, and how do I get help? | Today, Medicines, Breathing when assigned, Help; records/follow-up when implemented. |

The patient home should lead with the next relevant confirmed task. It should not require every patient to enter a breathing screen to find their medicines. Keep the current large Start button within the Breathing module.

The staff chart should use clear tabs: Overview, Consultation, Medicines, Breathing, Records and Timeline. Put communication logs behind a History section. A nurse's routine work should not require scrolling past a configuration editor and the full escalation trace.

## 11. Proposed underlying records

Reuse existing entities where appropriate, but add the missing operational model deliberately:

- **Hospital:** name, branding, settings and enabled modules.
- **Department:** hospital, name, coordinator/membership and active status.
- **Staff membership:** hospital/department, role and assignment scope.
- **Patient:** internal ID, hospital MRN, contact, language and demographic fields.
- **Encounter/admission:** patient, department, doctor, status, times and clinical note references.
- **Bed / allocation:** room/ward, bed state, active encounter and transfer history.
- **Prescription / items / dose events:** reuse the existing design, link it to the relevant encounter and approval.
- **Device / assignment / breathing session:** device, patient/encounter, assigned team, provenance and measurement status.
- **Task / alert:** patient, department, responsible staff, reason, priority and resolution.
- **Authentication challenge:** hospital/patient, hashed code, expiry, consumed state and attempt limits.
- **Consent / audit:** retain purpose and actor history, and apply it consistently.

Every department-scoped record must also remain hospital-scoped. Preserve the internal patient ID for relationships and MRN as the hospital-facing identifier. Do not join records by patient name.

## 12. How the AI prescription flow should work

The desired flow can be added without discarding the current form:

1. Doctor opens the correct patient and consultation.
2. Doctor types the prescription in a notepad, with optional clinical notes kept distinguishable from medication instructions.
3. AI extracts draft medication fields. It copies what is explicitly written; missing strength, duration or timing remains unclear.
4. Review screen shows original text alongside extracted structured lines.
5. Doctor edits and confirms the lines and explicit schedule.
6. Doctor approves the prescription; only then is it published to the patient and used to create dose events.
7. Original input, approved version and reviewer identity remain traceable through references and appropriate storage rules.

If AI is unavailable, the doctor uses the existing structured editor. Do not call template output a successful AI interpretation. Do not allow ambiguous free text to create active medicine reminders.

Acceptance should include incomplete text, mixed-language instructions, contradictory frequency, SOS medication, edits after extraction, rejected drafts and repeated saves. No draft should appear as an active prescription on the patient's phone.

## 13. What the physical SpiroBuddy module still needs

The concept matches your description: a sensor below a volumetric spirometer reads the moving disc/piston. The inspected firmware uses VL53L1X or VL53L0X and emits USB serial readings at roughly 30 Hz. Bluetooth is not implemented by that sketch.

To move from concept to measured exercise evidence:

1. Verify the actual spirometer's underside and optical path. A rendered transparent model does not answer whether the real base blocks or distorts the reading.
2. Build a fixed mounting prototype that does not obstruct normal use.
3. Calibrate known printed volume positions against measured distance.
4. Measure repeatability, sensor failures, ambient-light effects and mount movement.
5. Validate slow/fast movement and hold detection against independently observed traces.
6. Preserve measurement validity, connection loss, timestamp and calibration version in stored records.
7. Establish the patient-phone transport and device assignment flow.
8. Show those records on the assigned department and nurse views.

These are engineering validation steps, not evidence of a clinical benefit. The synthetic model's reported accuracy must remain explicitly synthetic until evaluated on appropriate measured data.

## 14. Prioritized work plan

### Priority 0 — make the current story reliable

- Publish an authoritative current-scope and deployment-status file; resolve OTP/PIN and notepad/structured-input contradictions.
- Confirm the intended deploy commit and compare it with local code. Deploying was not part of this audit.
- Fix identity display: one hospital name and the authenticated staff name/role everywhere.
- Remove or clearly mark entry links to unfinished screens.
- Prepare a stable sample with an issued prescription so Medicines and pharmacy checking have something to show.
- Correct public claims about reminders, uploads, provider usage and QR readiness.
- Fix the session-completion and provenance gaps before presenting recorded sessions as trustworthy exercise evidence.

### Priority 1 — complete one patient-care journey

- Department entity and coordinator account.
- Registration page with hospital MRN, phone and doctor/department assignment.
- Patient OTP request/verify with simulated delivery clearly marked; real delivery added when configured.
- Doctor encounter record and structured prescription, followed by the notepad/extraction review extension.
- Patient Today and Medicines screens, with confirmed schedule and report action.
- Missed-dose alert assigned to the correct team.
- Server-backed device assignment and conditional Breathing module.
- Patient simulated exercise appearing on the department and assigned nurse views.

### Priority 2 — complete hospital operations around that journey

- Admission, transfer and discharge events.
- Bed inventory and conflict-safe allocations.
- Hospital overview derived from real department/admission data.
- Nurse shift, room assignments, task completion and handover.
- Doctor day list and appointment request/confirmation.

### Priority 3 — extend once the core works

- Prescription PDF and records vault.
- Real OTP/message adapters and delivery status.
- Closed-app reminders, offline adherence queue and recovery behavior.
- Physical sensor integration and measured-input validation.
- Native/store apps and Bluetooth.
- Imports/exports, hospital onboarding and further device modules.

Avoid promising delivery dates from this list without sizing the tasks and deciding which flows must be production-grade. Earlier estimates in the repository are planning assumptions, not verified schedules.

## 15. Acceptance checks for the next build

| Scenario | Passing behavior |
|---|---|
| Register a new patient | Saved under the provided MRN in the correct hospital; doctor/department assignments visible without a seed reset. |
| Reuse an MRN | Duplicate within one hospital is rejected; the same MRN in another hospital resolves correctly through hospital context. |
| Patient has no phone | Staff can continue care; patient login explains the appropriate pending/recovery path. |
| Request OTP | Challenge expires, works once, has resend/try limits and does not expose a code outside permitted simulation mode. |
| Wrong hospital or patient | Staff and patients cannot access another scope's records; UI and APIs both enforce it. |
| Doctor consultation | Encounter is saved with author/time and linked to the patient's record. |
| AI drafts a prescription | Draft remains invisible to patient schedules until doctor approval; uncertain fields require review. |
| Doctor issues prescription | Patient sees the approved version and exact confirmed schedule; retries do not create duplicates. |
| Patient reports a dose | “Reported” updates on the appropriate staff view; repeat taps do not duplicate reporting. |
| Dose becomes overdue | One meaningful alert after the configured grace interval; correct department/assignee; no dosing advice. |
| Device assignment | A handover on the nurse's phone is visible on the patient's separate phone and department computer. |
| Partial or empty breathing session | Does not count as a completed exercise slot. |
| Simulated breathing session | Completion is recorded and visibly remains simulated. |
| Real device session | Calibration and provenance are recorded; invalid/disconnected readings do not silently count. |
| Bed allocation | Two simultaneous assignments cannot occupy the same bed; transfer/discharge releases or changes it consistently. |
| Offline / provider failure | UI explains what is unavailable; mock data cannot masquerade as the patient's current records. |
| Phone use | Complete key tasks at a narrow viewport with readable text, keyboard access and no horizontal scrolling. |

## 16. Verification performed and outstanding

**Performed:** direct deployed-page review, doctor demo sign-in, chart/prescription inspection, patient app and medicine empty-state inspection, patient-login 404 check, device inventory design inspection, public-page consistency review, 3D model rendering/control inspection, source and graph review.

**Not performed:** live prescription creation, sample reset, real communications, admin/nurse full operational click-through, real OTP delivery, physical hardware validation, Android/iOS installation, external source revalidation or a fresh full test-suite run.

A focused local test run was attempted for authentication, isolation, PIN login, medicines, branding, public pages and platform features. The first attempt failed because the test fixture could not create a child directory in the environment's default temporary folder. A retry used a workspace temporary directory, but produced no result output during the audit and was interrupted. **No fresh test pass is claimed.** The temporary retry folder was removed afterward. This limits execution confidence in local-only features; the live observations and source findings above remain separately identified.

## 17. Evidence map for developers

| Finding | Main evidence |
|---|---|
| Intended five roles | `docs/plan/13_AROGYA_SATHI_PLATFORM.md` §§1–3; latest founder request. |
| Latest OTP requirement | `CLAUDE.md` founder decisions; `docs/rebuild/REGNO_OTP_BRIEF.md`. |
| Actual local PIN implementation | `backend/app/routes_me.py`, `backend/app/patient_login.py`, `web/patient-login.html`, `web/js/patient-login.js`. |
| Department role absent | `backend/app/authz.py` role/action matrix; current routes; platform plan calls it a new piece. |
| Enrollment absent / narrow edits | `backend/app/main.py` patient route definitions and `update_patient`. |
| Structured prescribing | `backend/app/routes_meds.py`, `backend/app/meds/service.py`, `web/prescribe.html`, medication JS. |
| AI helper not integrated | `backend/app/ai_gemini.py:extract_prescription`; graph caller trace; current medication routes. |
| Dose events vs reminders | `meds/service.py:refresh_doses`, `routes_meds.py:me_today`; `features.py` dose keys. |
| Session completion/provenance | `main.py:post_session`, `service.py:record_session`; session save in `web/app.html`. |
| Browser-only unit assignments | `web/js/units-mock.js`; Units page note; `PROGRESS.md` mock-unit entry. |
| Old vs role-aware shell | `web/js/ui.js:isHospitalPage`, hospital nav and legacy header handling. |
| Offline mock distinction | `web/js/api.js`, `web/sw.js`, feature registry. |
| Physical transport/design | `firmware/spirobuddy_serial/spirobuddy_serial.ino`, `docs/HARDWARE.md`, `docs/3D_SOURCES.md`, showroom. |
| Deployment discrepancy | Live landing/chart identities and patient-login 404 compared with current local files. |
| Stale project state | `START_PROMPT.md`, `HANDOFF.md`, `REQUIREMENTS.md`, `STATE.md` compared with current source. |

## 18. Final assessment

Keep the existing work, but stop treating the roadmap, the local checkout and the deployed demo as interchangeable.

The next convincing demonstration is one newly registered patient moving through department registration, doctor consultation and approved prescription, patient OTP access, patient action, and a meaningful update on the responsible nurse and department screens. Add hospital occupancy from real admission records, and show SpiroBuddy as an assigned module inside that platform.

That would make Aarogya Saathi feel like one connected product. Today, it feels like several promising pieces around a breathing-care demo.
