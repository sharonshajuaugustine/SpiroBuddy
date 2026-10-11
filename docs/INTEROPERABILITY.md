# Interoperability: fitting beside the hospital's own software, and moving data in and out

**Written:** Sun 11 Oct 2026 · **Answers:** the founder's ask of 11 Oct (hospitals may already have software for their patients, so data must move in and out easily) · **Confidence:** medium for the design (it reuses tables and rules already in the repo), **low** for every effort figure (nothing here is built, and no hospital system has been tried).

**How to read this file**
- **FA** = `docs/FUTURE_ARCHITECTURE.md`. **B4-x, B5-x** = findings in `docs/research/business/04_legal_and_regulatory.md` and `05_icmr_ethics_abdm_evidence.md`. **plan 11** = `docs/plan/11_HOME_RECOVERY_COMPANION.md`. **Contract L** = `docs/ARCHITECTURE.md` §21 (the exact web addresses and fields).
- Every number is a fact (with its file), or is labelled **estimate**, **assumption** or **target**. "Ours" = this file's own guess, with no outside source. A developer-day = one developer working for one day.
- Status words: **Live**, **Simulated**, **In development**, **Planned**. **Nothing in this file is Live today.** No real hospital system has been connected. The hospital and the patients in the demo are fictional.
- Terms: **HIS / EMR** (the hospital's own patient-record system). **CSV** (a plain spreadsheet file, one row per patient). **FHIR R4** (the international standard format for health records, version 4).

> ## 1. Answer in 10 lines
> 1. **SpiroBuddy sits beside the hospital's existing software. It does not replace it.** The hospital keeps its system. SpiroBuddy adds the part the patient uses at home.
> 2. **In from the hospital:** who the patient is, the operation, the discharge date and the doctor in charge. Later: prescriptions and visits.
> 3. **Out to the hospital:** the breathing summary, medicine doses as *reported* by the patient, alerts and what was done about them, visit outcomes, documents, the consent record and the audit trail.
> 4. **Four levels of connection.** Level 0: a spreadsheet in, files out, no IT work. Level 1: standard FHIR files. Level 2: a live feed. Level 3: India's national health network (ABDM).
> 5. **Status today:** no code yet. Levels 0 and 1 are **In development** (specified as Contract L, builder X3). Levels 2 and 3 are **Planned**.
> 6. **Moving a hospital in takes one day (target, not rehearsed).** The import always starts as a dry run (a trial that shows what would happen and saves nothing). Nothing is created until a hospital admin confirms.
> 7. **One safety rule never bends:** an imported prescription is only a draft. No reminder exists until a named doctor or permitted nurse approves it.
> 8. **Moving a hospital out:** a full export on request (CSV + FHIR + documents), then deletion under the retention rules. No lock-in.
> 9. **Effort (estimates):** Level 0 about 4 developer-days, Level 1 about 5–10, Level 2 about 10–20 for the first hospital system, Level 3 1–3 months plus certification steps.
> 10. **Why this order:** repo research says most private hospitals in India can give spreadsheets and PDFs, not live FHIR links (plan 11 §C-3, single source). We start where the hospital already is.

## 2. The picture

```text
  HOSPITAL (keeps its own system)            SPIROBUDDY (sits beside it)                 HOME
+-------------------------------+        +--------------------------------+        +------------------+
| HIS / EMR                     |   IN   | Import, always a dry run first |        | Patient app      |
| the hospital's own            | =====> | Hospital pages: admin, doctor, | <====> | Family page      |
| patient-record system         |        | nurse                          |        | Clip-on unit on  |
|                               |   OUT  | Data store + audit trail       |        | the spirometer   |
| stays the main record         | <===== | Export: CSV, FHIR, documents   |        |                  |
+-------------------------------+        +--------------------------------+        +------------------+
  IN  = patient list, operation, discharge date, doctor; later prescriptions (as drafts) and visits
  OUT = breathing summary, reported doses, alerts and actions, visit outcomes, documents, consent, audit
```

The left arrow is a **file** at Levels 0 and 1 (In development) and becomes a **live link** at Levels 2 and 3 (Planned). The right side is the product itself; its feature statuses are in `docs/FEATURE_STATUS.md`.

## 3. What moves each way

**IN – from the hospital to SpiroBuddy**

| Data | Lands in (table.column, `supabase/schema_v2.sql`) | Level 0 (file) | Levels 1–2 (standard) |
|---|---|---|---|
| Name, age, sex | `patients.name`, `.age`, `.sex` | CSV | FHIR `Patient` |
| Hospital record number (MRN) | `patients.mrn` | CSV `mrn` | `Patient.identifier` |
| Phone, language | `patients.phone`, `.language` | CSV | `Patient.telecom`, `.communication` |
| Operation and its date | `patients.surgery`, `.surgery_date` | CSV `surgery_type`, `surgery_date` | `Procedure` (import Planned) |
| Discharge date | `patients.discharge_date` | CSV | discharge message (Level 2) |
| Doctor in charge | `patients.primary_doctor_id` | CSV `primary_doctor_email`, matched to a doctor's account | `Patient.generalPractitioner` |
| Prescriptions | `prescriptions`, `prescription_items` – **as a draft only** | not in the CSV: the doctor types it or uploads a photo (Contract H) | `MedicationRequest` in, as a draft (Planned) |
| Appointments | `appointments` | not in the CSV: booked in SpiroBuddy (Contract I) | `Appointment` in (Planned) |

**OUT – from SpiroBuddy to the hospital**

| Data | Comes from | Level 0 (file) | Level 1 (FHIR R4) |
|---|---|---|---|
| Breathing summary: sessions done, best volume, breaths, score | `sessions` | `sessions.csv` + printable discharge plan | `Observation` |
| Care plan: volume target, hold time | `patients.target_ml`, `.hold_target_s` | `patients.csv` | `CarePlan` |
| Approved medicine lines | `prescriptions`, `prescription_items` | CSV | `MedicationRequest` |
| Medicine doses **as reported by the patient** (never "taken") | `dose_events` | `dose_events.csv` | `MedicationStatement` |
| Alerts and what was done | `alerts` (kind, severity, status, acted_by) | `alerts.csv` | CSV only for now; FHIR form is an open question |
| Visit outcomes (attended, no-show) | `appointments.status` | CSV | `Appointment` |
| Documents | `documents` + the files | list + files | `DocumentReference` |
| Consent record | `consents` | CSV | `Consent` |
| Audit trail (who saw or changed what) | `audit_events` | `audit_events.csv` | `AuditEvent` |
| Unit used | `devices` | `devices.csv` | `Device` |

We say "reported" because SpiroBuddy records that the patient tapped "I took it". It cannot know the medicine was swallowed. A dose with no report is exported as "no report", not as "not taken".

## 4. Four levels of connection

**Checked on 11 Oct 2026:** a search of `backend/` and `web/` finds no code that builds a FHIR file and no import or export route. (The feature list being written in `backend/app/features.py` names a `fhir.export` entry, but there is no route behind it yet.) The only CSV code today writes breath-training samples for the breath model (`backend/app/service.py`). So every level below is still to be built.

| Level | What it is | Status | What the hospital's IT team must do | Effort for us |
|---|---|---|---|---|
| **0 – no IT work** | A spreadsheet (CSV) of the discharge list goes in. A printable discharge plan and CSV files come out. | **In development** (specified as Contract L, builder X3) | Nothing. A ward clerk or admin fills our 10-column template and uploads it. | About **4 developer-days** (**estimate**, ours: import with dry run 2, CSV export 1, printable plan 1; reuses the patients table, the permission checks and the audit writer of `docs/REBUILD_PLAN.md` §3.3 and §3.5) |
| **1 – standard files** | FHIR R4 bundles (a bundle = one file holding many records) out per patient and per hospital. FHIR `Patient` records in. | **In development** (specified as Contract L, builder X3) | Load our files into their system, or produce `Patient` files from it, if their system can. | About **5 developer-days** for a basic bundle (**estimate**, ours); **10** for the version shaped to India's FHIR profiles (**estimate**, FA §3.8: "2 weeks") |
| **2 – live feed** | The hospital system tells SpiroBuddy when a patient is discharged: an HL7 v2 "ADT" message (an older admit-discharge-transfer message format; FA §3.8 expects it to be more common than FHIR in Indian hospital systems, unconfirmed), or a FHIR subscription or webhook (their system calls our web address). A doctor opens the SpiroBuddy chart from inside the hospital system with a SMART on FHIR launch (a standard way for one health app to open inside another, already signed in). | **Planned** | Open a secure link from their system to ours, switch on the discharge message, register SpiroBuddy as a launchable app, give test messages. Their software vendor is usually needed. | About **10–20 developer-days** for the first hospital system (**estimate**, ours: listener, field map for that system, test rig with made-up messages, launch page; no vendor quote). Each further system: **not yet costed** |
| **3 – national rails** | ABDM (Ayushman Bharat Digital Mission, India's national health-records network) with the patient's ABHA number (the national health ID), through a consent manager (an app in which the patient approves each sharing). | **Planned** | Little, if their own system is already on ABDM (our reading, plan 11 §C-2). | **1–3 months** including certification (**estimate**, FA §3.8). Vendors report 4–9 months (B5-17, not confirmed). Security-audit fee: **not yet costed** |

**Level 3, exactly as the repo research has it** (B5-17; FA §3.8; plan 11 §C-2):
1. Build against the National Health Authority's test environment (the "sandbox"), in milestones. **M1:** create and verify the patient's ABHA. **M2:** act as a health information provider – share records, with the patient's consent, as FHIR bundles. **M3:** act as a health information user – read records held elsewhere. (FA §3.8 words M2 as "link care contexts" and M3 as "consent-based sharing". The two files differ slightly.)
2. Reported exit steps: functional testing, a security audit by a CERT-In empanelled firm (a "Safe-to-Host" certificate), a demo to the authority, then production keys. One vendor says at least two milestones are needed.
3. **Not confirmed from a primary government source.** The milestone meanings agree across sources; the exit steps and times are vendor claims (B5-17).
4. India's FHIR profile set has no lung-function profile and no device profile (FA §3.8; B5-17). The breathing data would travel as a general observation.
5. Our reading (B5-17): a pilot under the hospital's own ethics approval needs no ABDM link. The cheapest later route is to send our episode summary into the hospital's own records system that is already on ABDM, or to become a small provider of "SpiroBuddy episode reports" only (plan 11 §C-2). We do not build a health-records app.

## 5. Field map (SpiroBuddy → FHIR R4)

Rule: we never invent a standard code. Where the table says "local code", it means **local code for now; standard code is an open question**. The web address that names our local codes is **founder to fill** once the product's domain is fixed.

| SpiroBuddy table and column | FHIR R4 resource and element | Codes |
|---|---|---|
| `hospitals.name`, `.city`, `.address`, `.phone` | `Organization.name`, `.address`, `.telecom` | none needed |
| `staff.name`, `.reg_no_display`, `.specialty` (doctor) | `Practitioner.name`, `.identifier`; specialty as text | local code |
| `patients.mrn` | `Patient.identifier.value` (the hospital names the identifier system) | – |
| `patients.name` | `Patient.name.text` | – |
| `patients.age` | We hold age, not date of birth. `Patient.birthDate` is filled only if the hospital sent one. | how to carry age alone: open question |
| `patients.sex` | `Patient.gender` | standard FHIR list: male, female, other, unknown |
| `patients.phone`, `.city` | `Patient.telecom` (phone), `Patient.address.city` | – |
| `patients.language` | `Patient.communication.language` | standard language tags (en, hi, ta …) |
| `patients.primary_doctor_id` | `Patient.generalPractitioner` → `Practitioner` | – |
| `patients.surgery`, `.surgery_date` | `Procedure.code.text`, `Procedure.performedDateTime`, status completed | text only; local code |
| `patients.discharge_date`, `.ward` | `Encounter.period.end`, `Encounter.location` (text); class = inpatient | builder to confirm the class code from the R4 list |
| `patients.target_ml`, `.hold_target_s`, session hours | `CarePlan` (status active, intent plan); targets as `Goal.target.detailQuantity` in mL and seconds | standard units (mL, s); activity = local code |
| `sessions.started_at`, `.breaths_count`, `.best_ml`, `.avg_score`, `.source` | one `Observation` per breathing session: `effectiveDateTime`; `component` values for best volume (mL), breaths, score | **local code** (no lung-function profile in India's set, FA §3.8) |
| `prescriptions` (status `approved`) + `prescription_items` (status `confirmed` or `edited`) | `MedicationRequest`: `medicationCodeableConcept.text` = `drug_name` exactly as written; `dosageInstruction.text`; `timing.repeat.timeOfDay` = `times`; `asNeededBoolean`; `authoredOn` = `prescribed_on`; `requester.display` = `prescriber_on_paper`; `recorder` = the staff member who approved (`reviewed_by`) | medicine: text only; **local code** (a national medicine code list is a known gap, plan 11) |
| `dose_events` (status `reported_taken`): `reported_at`, `reported_by_role`, `item_id` | `MedicationStatement`: `effectiveDateTime` and `dateAsserted` = `reported_at`; `informationSource` = the patient (or the staff member who reported for them); `basedOn` → the `MedicationRequest` | status `completed` proposed; builder to confirm |
| `appointments.start_at`, `.end_at`, `.doctor_id`, `.kind`, `.reason_text`, `.status` | `Appointment.start`, `.end`, `.participant`, `.description`; status: requested → proposed, confirmed → booked, attended → fulfilled, no_show → noshow, cancelled or declined → cancelled | standard FHIR status list; `kind` = local code |
| `documents.kind`, `.title`, `.doc_date`, `.mime`, `.size`, `.created_at` | `DocumentReference.type.text`, `.description`, `.content.attachment` (`contentType`, `size`, `creation`), `.date` | document type: **local code** |
| `consents.items`, `.method`, `.language`, `.created_at`, `.withdrawn_at`, `.version` | `Consent.dateTime`, `.patient`; status active, or inactive once withdrawn; our six items in `provision` as text | scope and category: builder to pick from the R4 lists; items = **local code** |
| `audit_events.at`, `.actor_type`, `.actor_id`, `.actor_role`, `.action`, `.resource_type`, `.resource_id` | `AuditEvent.recorded`, `.agent`, `.entity`; `source.observer` = SpiroBuddy | action name (for example `patient.view`) = **local code**; the tamper-check hashes stay in the CSV |
| `devices.serial`, `.model`, `.firmware`, `.state`, `.assigned_patient_id` | base R4 `Device.serialNumber`, `.modelNumber`, `.version`, `.status`, `.patient` (no device profile in India's set, FA §3.8) | device type: **local code** |
| `alerts` | no FHIR form chosen yet – CSV only | open question |

Left out of the FHIR files: single breaths (summaries only, FA §3.8; the CSV export does hold them), draft or rejected prescriptions, and deleted documents. Left out of every export: passwords, sign-in tokens, and the text sent to or from AI services.

## 6. Moving a hospital IN (one day – **target**, not rehearsed with any hospital)

Before the day: a signed data-processing agreement (section 9) and one hospital admin account.

| Step | Who | What happens | Contract |
|---|---|---|---|
| 1 | Hospital admin | Fills in the hospital profile: wards, departments, languages. | F |
| 2 | Doctors | Sign up with the hospital's join code; the admin approves them. This comes first because the patient list names each doctor by email. | E, F |
| 3 | Ward clerk or IT | Downloads our 10-column template and fills it from the hospital system's discharge list. | L |
| 4 | Hospital admin | Uploads the file. **The first upload is always a dry run:** it shows how many patients would be created, how many updated, and every problem row with its reason. Nothing is saved. | L |
| 5 | Clerk + admin | Fix the file and repeat step 4 until the list is clean. | L |
| 6 | Hospital admin | Confirms. Only now are patients created. No message goes to any patient or family yet. | L |
| 7 | Nurse, per patient | Records consent, sets the breathing plan, hands over the app link and the unit. | G, K |
| 8 | Doctor or permitted nurse | Types the prescription, or checks each line of an uploaded one, and approves it. Reminders exist only after this step. | H |
| 9 | Staff | Book the follow-up visits. | I |
| 10 | Hospital admin | Checks the patient count against the discharge list and sees the import in the audit log. | F |

**Rules that are fixed**
- **Dry run first.** Dry run is the default; saving needs an explicit second action by a hospital admin.
- **Duplicates** are matched on **hospital + record number** only, never on name. A match updates the patient instead of making a second one. The same record number twice in one file is a problem row.
- **Re-uploading is safe:** the same file a second time changes nothing.
- **An imported prescription is never approved by the import.** It waits as a draft for a named human (Contract H: no dose event exists before approval). This version of the import does not create prescriptions at all.
- **No consent, no messages.** An imported patient has no consent record, so nothing is sent until a nurse records consent.

## 7. Moving a hospital OUT (no lock-in)

| Step | What happens | Status |
|---|---|---|
| 1 | The hospital admin asks for a full export. | – |
| 2 | The export, in both formats: one ZIP with every table as CSV and the document files, and one ZIP with a FHIR bundle per patient. A README in each lists the row count of every file, so the hospital can check nothing is missing. | In development (Contract L) |
| 3 | The hospital confirms it has the data. Programmes are ended, staff sign-ins and nurse keys are revoked, units come back (Contracts E, G, K). | In development (those contracts) |
| 4 | Deletion under the retention rules below, with a written note of what was deleted and when. | Planned (no deletion tool yet) |

**Retention rules (FA §3.3; all are targets until a contract is signed)**

| Data | Kept for | Then |
|---|---|---|
| Breathing data, sessions, alerts, care-plan changes | The episode plus the hospital's own record-keeping period, set in the contract | Hard delete, or hand over to the hospital |
| Audit events | At least 1 year | Archived |
| Server logs | 180 days, in India | Deleted |
| Message and call content | 90 days (**estimate**, our policy) | Only the outcome is kept |
| Backups | 30 days rolling | Expire – so a deletion is complete only once old backups have expired; the privacy notice must say so |

The hospital decides, not us: for clinical data the hospital is the data fiduciary (the party that decides why data is used) and SpiroBuddy is its processor (our reading of the law, FA §3.3; to be confirmed with a lawyer).

## 8. Moving SpiroBuddy itself between hosts

- **Two interchangeable stores behind one interface.** `backend/app/store.py` has `SqliteStore` (a single file, used by the demo) and `SupabaseStore` (a hosted Postgres database). Both follow the same `Store` interface, and `make_store()` picks one from a single setting (`DATA_BACKEND`). The rest of the code does not know which one it is talking to.
- **Database changes are additive only.** `supabase/schema_v2.sql` only adds tables and columns ("if not exists"), so it is safe to run again on a new host. FA §3.1 sets the rule for later: add first, switch, remove in a later release.
- **So the service can move** from today's free hosting to an incubator server or a cloud region in India. The 7 steps and the expected downtime are in `docs/SCALING_AND_COST.md` section 7 (7f).
- **One honest limit:** a server with plain Postgres and no Supabase needs a third store class behind the same interface. Planned, not built; about 2 developer-days (**estimate**, ours: the two existing classes are about 110–150 lines each). FA §3.1 also plans to keep SQLite for the offline demo only after the pilot.
- A hospital's own data moves separately, by sections 6 and 7 – it does not depend on where SpiroBuddy is hosted.

## 9. Safety, privacy and consent on every transfer

| Guard | What it means | Where it is set |
|---|---|---|
| Encryption in transit | Every upload and download goes over https; **target** TLS 1.2 or newer. The patient list is uploaded straight to the admin page – never sent by email or chat. | FA §3.6 |
| Admin-only | Only a hospital admin can import or export a whole hospital, and only their own hospital. A doctor or nurse can export one patient, and only a patient they are allowed to see. | Contract L; `docs/REBUILD_PLAN.md` §3.3 |
| Audit entry each time | Every dry run, import and export writes who, when and how many rows – never the file itself. | Contract L; `docs/REBUILD_PLAN.md` §3.5 |
| Consent items | The patient's six items (care reminders, family sharing, records storage, AI use, research use, AI training) travel with the record, with dates and any withdrawal. Data goes back only to the hospital that treats the patient. Sharing with anyone else is Planned and would need the patient's consent each time. | Contract K; FA §3.7 |
| Only the fields needed | The import takes 10 columns. Exports follow the field map in section 5 and leave out passwords, tokens and AI text. | Contract L |
| Data-processing agreement | A two-page agreement with the hospital: the hospital decides the purpose and we process; the list of data items; storage in India and the named outside services; access logs kept 1 year; prompt breach notice; deletion or return at the end; no other use. **None is signed yet – we have no hospital partner yet.** | B4-16 (team synthesis, not a hospital's own template) |
| India storage before real patients | The database moves to an India region before the first real patient. Until then, fictional data only. | FA §3.5 |

## 10. Is it feasible?

**Yes for Levels 0 and 1:** they use only our own tables and a published standard, and need nothing from any vendor. **Level 2 is feasible one hospital system at a time.** **Level 3 is feasible but long,** and a pilot does not need it (our reading, B5-17).

| Order | Level | Build when | Effort (**estimates**, section 4) | Stage (`docs/SCALING_AND_COST.md`) |
|---|---|---|---|---|
| 1 | 0 – spreadsheet in, files out | Now (builder X3) | about 4 developer-days | 1 Pilot (1 hospital) |
| 2 | 1 – FHIR files | Now for the basic bundle (X3); the India-profile version before 10 hospitals | about 5–10 developer-days | 1 Pilot → 2 Multi-hospital (10 hospitals) |
| 3 | 2 – live feed | Only when a paying hospital asks (FA §3.8) | about 10–20 developer-days for the first system; then not yet costed | 2 Multi-hospital (10 hospitals) → 3 Multi-hospital (~100 hospitals) |
| 4 | 3 – ABDM | When the first hospital asks; needed for government programmes (FA §3.8) | 1–3 months plus certification steps | 3 Multi-hospital (~100 hospitals) → 4 National |

| Risk | Why it matters | What we do |
|---|---|---|
| Every hospital system is different | No market-share figure for hospital systems in India was found (plan 11 §C-3). One connector will not fit all. | Start with a spreadsheet any system or clerk can produce. One field map per system at Level 2. Never promise it works with every system. |
| Vendor cooperation | The hospital's software vendor may refuse a live link, be slow, or charge. Cost: not yet costed. | Levels 0 and 1 need no vendor. Level 2 only on a paying hospital's request, with the hospital asking its vendor. |
| No real test data | We hold fictional patients only – no real discharge list, no real hospital message. | Made-up files in tests. The first real file runs as a dry run with the hospital's IT watching. Ask the hospital for a sample with identities removed. |
| Wrong match | A record number typed two ways could create a duplicate. | Match on hospital + record number only; the dry run lists every row that would update. |
| Missing standard codes | No lung-function profile in India's FHIR set (FA §3.8); a national medicine code list is a known gap (plan 11). | Send text plus local codes. Keep it as an open question for the first hospital's IT team. |
| ABDM steps unconfirmed | The exit steps and times come from vendors, not from the authority (B5-17). | Promise no ABDM date. Check with the authority before planning Level 3. |

## 11. What to say, and what not to say

**Say**
1. "SpiroBuddy fits beside the hospital's own software. The hospital keeps its system; we add the part the patient uses at home."
2. "A spreadsheet import with a dry run, and export in the FHIR standard, are In development. A live feed and the ABDM link are Planned."
3. "The hospital can take all its data out on request, and nothing an import brings in reaches a patient until a named clinician approves it."

**Do not say**
1. "ABDM-integrated", "ABHA-enabled", "FHIR-certified" or "compliant" – none of these is done.
2. "Works with any hospital system", "plug and play" or "seamless integration" as a present fact – no hospital system has been connected.
3. "Doses taken" (say "doses reported by the patient"), or "real-time feed to the hospital" (Level 2 is Planned).

## 12. Sources

All from the repo. No new web page was opened for this file.

| Used for | Source |
|---|---|
| FHIR export design, ABDM milestones, effort for FHIR and ABDM, HL7 v2 "only when a paying hospital asks" | FA §3.8 (its sources [W9], [W10]) |
| Migrations, retention, encryption, consent records, India storage | FA §3.1, §3.3, §3.6, §3.7, §3.5 |
| ABDM steps, exit steps, vendor times, "a pilot does not need it" | `docs/research/business/05_icmr_ethics_abdm_evidence.md` B5-17 (not confirmed from a primary source) |
| Data-processing agreement contents | `docs/research/business/04_legal_and_regulatory.md` B4-16 (team synthesis) |
| "Expect CSV/PDF, not live FHIR"; cheapest ABDM path; medicine code gap | plan 11 §C-2, §C-3 (single source, preprint), §B |
| Table and column names | `supabase/schema_v2.sql`; `supabase/schema.sql` (alerts); `docs/ARCHITECTURE.md` §10 |
| Routes, rules, permission and audit names | `docs/ARCHITECTURE.md` Contracts E–L (§14–§21); `docs/REBUILD_PLAN.md` §3.3, §3.5, §3.6 |
| Two stores behind one interface | `backend/app/store.py` (`Store`, `SqliteStore`, `SupabaseStore`, `make_store`) |
| Stage names, host-move steps | `docs/SCALING_AND_COST.md` sections 4 and 7 |
| "No code yet" check | search of `backend/` and `web/` for "fhir" and "csv", 11 Oct 2026 |
