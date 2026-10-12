# Discharge documents implementation handoff

Implemented 12 October 2026 for the hackathon prototype. No live deployment or clinical validation is claimed.

## Working behavior

- A scoped doctor creates and saves a draft, previews the saved draft, explicitly publishes it, creates a replacement draft or withdraws the current document with a retained reason.
- Published clinical content remains immutable. A replacement publication changes the old version to superseded in the same persisted aggregate. An unsuccessful publication leaves the prior published version intact.
- The patient sees only their own current published document using their authenticated patient session, acknowledges that exact version idempotently and prints it. Query-string patient IDs cannot change the patient identity.
- Existing scoped nurses and administrators can read published/history documents; draft reads are doctor-only. Nurse/admin authoring is denied. Access uses the existing staff permission scope without adding privileges or using an alternative patient cookie to authorize staff access.
- Plain clinician text preserves wording and line breaks. The module generates no clinical advice, medicines, translations or exercise targets. Medication navigation leads to the existing current approved list and explicitly distinguishes it from the document.
- Publication does not change beds, admissions, prescriptions or breathing assignments.

## Entry URLs

- Doctor editor: `/discharge-editor.html?id=1` (replace ID with an authorized patient).
- Nurse/admin reading: same URL with read-only controls.
- Patient: `/my-care.html`.
- Patient print: `/discharge-print.html`.
- Staff historical/draft print: `/discharge-print.html?id=1&version=1`.
- Staff current print: `/discharge-print.html?id=1`.

The print page escapes all displayed content through DOM `textContent`. Draft and historical documents have clear state notices. Browser print/save-PDF uses the user's print dialog.

## Route contracts

All routes are authenticated; POST/PUT retain the application's existing X-SB CSRF protection. None belongs in the public allowlist.

| Route | Access | Request / response |
|---|---|---|
| GET `/api/patients/{pid}/discharge` | Scoped doctor/nurse/admin | Patient/MRN, hospital, revision, current document. Doctors also receive version history. `can_edit` declares doctor editing capability. |
| GET `/api/patients/{pid}/discharge/versions/{version}` | Scoped staff; draft doctor-only | Same envelope with requested document. |
| POST `/api/patients/{pid}/discharge/drafts` | Scoped doctor with existing rx.create permission | `{revision, content?}`. Optional content defaults to current publication or blank. Only one draft at a time. |
| PUT `/api/patients/{pid}/discharge/versions/{version}` | Scoped doctor | `{revision, content}` replaces a draft's content only. |
| POST `.../versions/{version}/publish` | Scoped doctor | `{revision, confirm:true}`. Publishes saved content after required-field checks. |
| POST `.../versions/{version}/withdraw` | Scoped doctor | `{revision, reason}`. Current published document only. |
| GET `/api/me/discharge` | Patient session only | Own current publication, never draft/history. |
| POST `/api/me/discharge/acknowledge` | Patient session only | `{version}`. Records reading current version; repeated requests return unchanged state. |

Envelope document fields include version, status, content, author, timestamps and acknowledgement. Content has condition_summary, treatment_summary, home_care, warning_signs, follow_up, exercise_instructions (4,000 characters each), language (40 characters), optional ISO follow_up_date and discharge_date. Publication requires nonempty condition_summary, home_care and follow_up. A stale revision or invalid state transition returns 409, invalid input 400, missing scope/version 404, prohibited role 403 and no session 401.

## Integration patches

Root has mounted the router through its optional module list before the API catch-all. For any checkout without that integration:

```python
from .routes_discharge import router as discharge_router
app.include_router(discharge_router)
```

Place it before the catch-all route/static handling. Do not add discharge APIs to public paths. Existing `/api/me/` middleware already resolves the patient cookie exclusively. Existing per-patient authorization remains active.

Recommended navigation: link `/discharge-editor.html?id=<authorized pid>` from the staff patient chart; link `/my-care.html` from the authenticated patient medicines page. Add discharge-editor.html to the frontend staff-login redirect page list. Register the feature as a working prototype only after integration verification. Root owns these shared changes, not this worker.

## Storage and limits

One `app_settings` row per hospital/patient: `discharge:v1:<hospital_id>:<patient_id>`. Its JSON value holds revision and versions. The scoped key avoids whole-table/history scans; patient profile and credentials are not duplicated. History is bounded at 100 versions; clinical field lengths are bounded. This prototype cannot archive older versions once the limit is reached.

An in-process RLock protects read-modify-write and publication/supersession, including acknowledgement. The aggregate is saved with one upsert. It provides consistency only within ONE application process. Multiple workers or service instances can overwrite each other; optimistic revisions are not database compare-and-swap. Production needs normalized document/version/acknowledgement tables, immutable published content, database transactions, atomic revision checks, retention/access policies and migration of the aggregate data. No claim of distributed safety is made.

Audit entries contain patient/version, state, revision, author actor and replacement reference, not clinical text or withdrawal reasons. Acknowledgement means reading only, not consent, adherence or recovery.

## Verification

Tests use a separate FastAPI app containing this router with real seeded session resolution and the repository's isolated sample-data fixtures. They do not write to the live database or invoke providers.

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_discharge_docs.py -q --tb=short
```

Final reviewed module run: **6 tests passed in 50.73 seconds**. Full output is recorded in `.build/discharge-review-tests.log`. Three new JavaScript files passed bundled Node `--check`.

Coverage includes draft invisibility, publication, patient ownership, cross-hospital denial, nurse/admin write denial, nurse draft denial/scoped publication read, stale edit conflicts, immutable content, replacement and acknowledgement history, failed publication preserving current version, withdrawals, dates/lengths, persistence after reloading the service, simultaneous publish conflict and plain-text renderer source checks. Anonymous denial and explicit publication confirmation are included in the expanded suite.

This worker did not execute a browser or real print dialog. Mobile CSS and print styles are implemented; root owns browser QA. The source check for textContent does not replace runtime XSS/browser verification. No real patient or provider behavior has been tested.

## Sample demonstration and remaining work

Use an isolated sample patient and doctor. Open the editor, create draft, enter sample condition/home-care/follow-up text and save. Preview shows Draft. Publish saved draft explicitly. Sign into that sample patient's session, open My care, acknowledge and open print. Return as doctor, create replacement, change/save/publish; patient sees a new version with no acknowledgement. Withdraw it; patient sees the empty current-care state and staff history retains the reason.

Before submission: verify shared mounting/navigation, doctor-to-patient browser flow, 375px layout and printable page. Before real operation: transactional persistence/migration and governance review. Real SMS, bed discharge, clinical templates, clinical translation and automatic prescription snapshots are outside this module.

## Final source review

Added current-document read/print navigation for nurse/admin viewers, strict rejection of non-object clinical content, and wrapping of long staff metadata. Verified demo reset removes discharge aggregates through the coordinated shared seed cleanup, preventing old instructions from attaching to reseeded patient identities. Six isolated tests pass. The patient care interface remains English; translated medicines links do not translate clinician content. Browser and physical print verification remain pending.
