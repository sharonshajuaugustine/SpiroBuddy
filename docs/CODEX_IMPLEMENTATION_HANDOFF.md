# Aarogya Saathi / SpiroBuddy: implementation and submission handoff

Updated 12 October 2026. This document records the work after the initial project audit. The audit remains a historical snapshot; use this handoff for subsequent implementation changes. Appointments were handed over by Claude; Codex completed department/bed operations and discharge documents after those delegated sessions stopped. Preserve unrelated session work and use each module's handoff when integrating or changing it.

**Publication boundary:** source checkpoint **6755f77** is published and deployed on Render; live HTTP/readiness checks passed. The combined suite completed with **930 passed, zero failures and zero expected failures in 1151.77 seconds**, before the final startup/phone-preservation guards. Those guards subsequently passed **5 focused startup checks** and **28 phone-preservation/PIN checks**. All **55 JavaScript syntax checks** passed. The local full-workflow results remain separate from live HTTP readiness; complete live browser acceptance is not claimed.

## Submission artifacts

- Detailed assessment: `docs/AAROGYA_SAATHI_PROJECT_AUDIT.md`.
- Canonical editable deck: `output/Aarogya_Saathi_DTI_With_SpiroBuddy.pptx`. Nineteen slides based on the supplied DTI template, seven native editable tables and larger fonts; all slides visually checked with zero issues. The original template is preserved; three workflow screenshots and planned AI automation are included. Original and earlier generated decks remain intact; deliver the readable deck as the canonical file.
- Team: **GuGu GaGa**, **Sharon Shaju Augustine**, **Fathima Shifana**. Team details are editable. No employer, college spelling, contact, interviews, pilot outcomes or paying customers were invented.
- Provider setup: `docs/HACKATHON_SETUP_CHECKLIST.md` and `docs/SARVAM_CALL_DEMO_SETUP.md`.
- Recording sequence and fallback: `docs/HACKATHON_DEMO_RUNBOOK.md` (5:50 main walkthrough and optional separately labelled provider-chat clip).
- Independent checks and integration notes: `docs/qa/`.

The readable deck is complete apart from a final cover refinement. Claude owns the submission video with the team's own narration: complete video under six minutes and 100 MB, including approximately 2.5 minutes explaining the product. These are current handoff targets, not completed-video claims.

Generated slides and private QA/runtime data are ignored. Never package the whole workspace: it contains environment credentials and local databases.

## Implemented core journey

1. A hospital admin or doctor can open `register.html`. Registration derives hospital from the authenticated actor, rejects duplicate MRNs and restricts doctor assignment appropriately. A phone is optional and explicitly pending when absent. New patients have breathing exercises disabled unless assigned.
2. The patient chart stores scoped consultation notes with authenticated author and time. Nurses cannot write doctor consultations. Existing medicine and chart data are reused rather than copied into a second patient model.
3. `prescribe.html?id=<sample-id>` has a prescription notepad. Gemini prepares a structured draft only when its key, hospital setting and the patient's AI consent allow it. Otherwise a pipe-separated manual format is available. Ambiguous fields stay blank for review. Preparation creates no prescription or scheduled doses.
4. The doctor reviews fields and explicitly confirms publication. A successful notepad event is checked against patient, hospital and purpose. Missing form/unit/timing/food decisions are rejected for AI-derived publication; reviewed draft references cannot be reused. The actual doctor is recorded. Existing structured prescription APIs retain their established behavior.
5. `patient-login.html` uses hospital + MRN + simulated OTP. Delivery is labeled Simulated; no SMS is sent. The challenge is hashed and persistent, expires after ten minutes, has wrong-code and resend limits and is single use. Phone or MRN changes invalidate outstanding challenges. Codes and challenges are not put in URLs or browser storage.
6. `patient-pin.html` preserves the existing reusable hospital PIN fallback. It is not a one-time desk code. Personal-link login remains supported by the existing app.
7. `meds.html` shows approved medicines, timing and patient-reported doses. Four interface languages are available. The print page uses the same readable medication summary. Breathing navigation appears only when assigned, including for patients without prescriptions. A spoken reminder is opt-in and works while the visible page is open; it is not a closed-app push service.
8. Missing scheduled medicine reports create scoped amber nurse follow-ups. Repeated checks do not duplicate scheduled-time alerts, patient name changes do not change identity, and late reports can resolve older alerts. A resolved staff follow-up is not automatically reopened. Family delivery for these medicine alerts remains planned.
9. Patient AI choice is recorded through authenticated `/api/me/ai-consent` and an independent medicine-page control. It defaults off, appends consent versions and preserves unrelated choices. Withdrawing AI blocks further provider drafting. A global clinical-consent withdrawal cannot be silently re-enabled by this control.
10. The existing breathing app rejects empty or malformed feature sets, recomputes labels/scores on the server and only counts a session complete after at least ten valid breaths. Browser submissions cannot claim to be verified physical-device measurements. Staff headers and alert actions show the actual authenticated actor.

## Newly completed platform modules

### Appointments and doctor day

`patient-visits.html`, `doctor-day.html` and `appointments.html` implement patient requests, doctor confirmation, alternative proposals, patient acceptance/decline, cancellation, attended/no-show states and the doctor's visit list. Availability APIs and free-slot queries exist; an availability-editing screen, appointment reminders and teleconsultation remain unfinished. Hospital and patient scope, nurse appointment permission, double-booking and state validation use the existing authorization model.

Routes are mounted before the API catch-all. Staff login redirects/navigation and translated patient My visits navigation have been integrated locally. The patient's session supplies identity; the medicines link does not expose tokens or MRNs. Claude's handoff records 25 appointment tests passed, plus its independent appointment/auth/isolation run and browser checks. Those are module evidence, not a substitute for the final combined suite or Render verification. Details and known booking-policy gaps: `docs/CLAUDE_APPOINTMENTS_HANDOFF.md`.

### Department operations and hospital overview

`department.html` and `hospital-overview.html` provide explicit bed inventory and admit, transfer, discharge, cleaning and ready transitions. Counts come from recorded operations, rather than existing chart labels or breathing activity. Transfer does not count as another admission. Ward/bed display fields follow confirmed allocation; duplicate patient/bed allocation, stale edits, invalid transitions and foreign-hospital access are rejected.

This is an **admin-operated prototype** using the existing hospital-admin account. Dedicated department provisioning/login remains Planned; doctor/nurse/patient access is rejected. Router and staff-page login handling are integrated locally. Five isolated module tests passed in 39.53 seconds, including concurrent allocation and storage-failure compensation. A later bed-reset regression also passed. Integrated localhost HTTP checks confirmed bed discharge and ready transitions; those are HTTP workflow evidence, not a completed mobile browser inspection. Details: `docs/CLAUDE_DEPARTMENT_HANDOFF.md`.

### Discharge documents and patient care instructions

`discharge-editor.html?id=<patient-id>` lets a scoped doctor save a draft, preview it and explicitly publish saved clinician-authored content. Published clinical text is immutable. Replacement publication supersedes the previous version only after successful validation; withdrawal retains the version and reason. Existing scoped nurses/admins can read published documents but cannot author or publish, and nurses cannot read drafts.

`my-care.html` resolves patient identity server-side, shows only the patient's current published document and records a version-specific, idempotent read acknowledgement. A replacement requires a fresh acknowledgement. `discharge-print.html` supports the patient's current document and authorized staff history/draft print views. All displayed clinical content uses textContent. No diagnosis, medicine, warning signs, translation or exercise targets are generated; approved medicines remain a separate current list.

Router, staff login handling, staff-chart link and translated medicines-page My care links are integrated locally. The final source-review module run passed six tests in 50.73 seconds, including removal of discharge aggregates on demo reset, malformed-content rejection and version/state safeguards. Nurse/admin current-view read/print navigation and long metadata wrapping were repaired. Integrated localhost HTTP checks saved/published version 1 for fictional patient 101, then verified that patient's OTP login, own-document read and acknowledgement. Browser checks showed patient version 1 and its print page, and the doctor saved/published replacement version 2 with a confirming screenshot. A physical print dialog/PDF export of this care document has not been verified. Detailed contracts: `docs/CODEX_DISCHARGE_HANDOFF.md`.

Bed discharge and document publication are deliberately independent operations: neither changes the other's state.

## Final hardening changes

Intent-normalization regressions passed 140 tests. Connection/timeout transport failures now return a neutral 503 response; unexpected handler errors return a neutral 500 response without internal exception text. Three fault-injection tests verified outage/recovery, public/static availability and ordinary unexpected errors. A stale-authentication regression passed separately. Demo reset now clears only namespaced department/discharge operational aggregates so old sample state cannot attach to reseeded patient identities; unrelated settings are preserved. The latest complete JavaScript syntax sweep passed 55 scripts. These checks are separate runs and must not be added together into one claimed suite total.

Final startup guards prevent lifespan from automatically resetting populated storage. Empty storage receives non-destructive initial seeding only. Phone/PIN preservation checks passed after these guards; no startup reset of existing local or live patient records is authorized by this implementation.

## Main new API contracts

| Endpoint | Access / behavior |
|---|---|
| GET `/api/registration/options` | Hospital-scoped admin/doctor registration choices |
| POST `/api/patients` | Admin/doctor registration; actor-derived hospital |
| GET/POST `/api/patients/{pid}/notes` | Scoped read; doctor consultation or existing permitted staff note |
| PUT `/api/patients/{pid}/phone` | Existing patient-edit permission; invalidates OTP |
| PUT `/api/patients/{pid}/breathing` | Existing care-plan-edit permission; strict boolean |
| POST `/api/patients/{pid}/prescriptions/draft-text` | Doctor-only draft; no prescription publication |
| GET `/api/me/otp/hospitals` | Public hospital login choices |
| POST `/api/me/otp/request` | Public, rate-limited simulated challenge request |
| POST `/api/me/otp/verify` | Public, rate-limited challenge consumption and patient cookie |
| GET/POST `/api/me/ai-consent` | Authenticated patient only; identity derived from cookie |
| GET `/api/me/prescription-card` | Existing authenticated patient data used by print page |
| GET `/api/department-ops` and POST `/api/department-ops/beds/...` | Existing hospital admin only; actor-derived hospital, operation-version checks |
| GET `/api/doctor/day`, staff `/api/appointments` and `/api/slots` | Existing scoped appointment permissions; doctor day restricted appropriately |
| GET/POST `/api/me/appointments` and patient appointment transitions | Authenticated patient's own visit requests and responses |
| GET `/api/patients/{pid}/discharge`; draft/version/publish/withdraw routes | Scoped staff reads; doctor-only authoring; revision checks |
| GET `/api/me/discharge` and POST `/api/me/discharge/acknowledge` | Own current publication and exact-version read acknowledgement |

All existing hospital/patient authorization remains in force. No patient ID supplied in an AI-choice request can change the authenticated patient.

## Verified provider status

The user's saved Render `GEMINI_API_KEY` is an `AQ.` authorization key. One authorized sample-only request through the actual `google-genai` application wrapper succeeded with `gemini-3.1-flash-lite` and returned one valid structured draft containing the sample medicine. No patient identifiers or real records were sent. The temporary key file was deleted before the request; the key was not printed or committed.

Google's current documentation supports authorization keys: https://ai.google.dev/gemini-api/docs/api-key . A prefix is not a valid reason to reject this credential. Successful local provider verification does not establish deployment of the new notepad UI or a completed patient/doctor browser journey on Render.

Render deployed checkpoint **6755f77** with the saved environment configuration. The live health response reports `llm_enabled=true`, `data_backend=supabase`, `demo_mode=true` and `v2_missing=false`. This verifies configuration/readiness, not a new actual Gemini provider request from the deployed application.

## Calls and recording

Existing communications code includes an AI conversation simulator, nurse-review alerts and a Sarvam outbound adapter. Google sign-in to the user's Sarvam Indus console succeeded. The corrected greeting was committed as **agent version 2**, and the real provider console chat was tested. With user approval, an API key was created and saved in Render using **Save only**, with organization/workspace metadata and version 2. The user's browser-only choice was saved as **`CALL_PROVIDER=dry_run`**. The saved configuration now applies to the deployed service; it does not verify outbound API authentication, calling or webhook delivery. No active phone connection or completed live outbound phone call is claimed. The user chose the browser/simulator demonstration instead of renting a number; phone rental/KYC is deferred.

Demo-mode destinations are fenced to configured team routes rather than fictional patient numbers, including communications and legacy WhatsApp paths. Simulator endings use neutral acknowledgement/callback-request language rather than prescribing extra exercise after a reported concern or promising an unscheduled callback. The final combined suite passed. The recording walkthrough is in `docs/SARVAM_CALL_DEMO_SETUP.md`; keep simulator/provider mode visible in the video. A provider console chat, fixture replay and browser-phone simulator must remain separately labelled.

## Verification record

- First complete suite: 828 passed, 14 expected failures and two outdated expectations. Those expectations were updated for the registration endpoint and accurate AI disclosure.
- Next complete suite, including the new appointments tests: 854 passed, 14 expected failures and two concurrency fixtures missing newly required valid breath timing. Fixture inputs were corrected without weakening their concurrency assertions.
- Final targeted core regressions after those fixes: **22 passed** (OTP, reviewed notepad, consent, reminder reconciliation, governance and concurrency).
- Public pages after architecture corrections: **37 passed**.
- Latest complete frontend sweep: **55 JavaScript syntax checks passed** (the earlier 38-script sweep was a historical subset).
- Call/Sarvam-focused existing tests: **20 passed**, using mocks and isolated data.
- New destination/simulator safety checks: **10 passed**; final combined verification is recorded below.
- Deck: integrity/layout/re-import passed, seventeen slides and seven native tables.
- Appointments module: **25 passed**, as recorded in Claude's handoff; independently documented browser checks remain distinct from the final integrated build.
- Department operations module: **5 passed in 39.53 seconds**.
- Department demo-reset regression: **1 passed**.
- Discharge final source-review module run: **6 passed in 50.73 seconds**, including demo-reset behavior; Python compilation and all three new script syntax checks passed.
- Combined run before final hardening: **904 passed, 14 expected failures**. This is historical evidence; later changes require their own verification.
- Final hardening subsets: **140 intent tests passed**, **3 exception-response tests passed**, **1 stale-authentication test passed**.
- Actual Gemini SDK request: valid sample-only structured result from `gemini-3.1-flash-lite` using the user's authorization key. This was a real provider request, not a mock.
- Sarvam: corrected greeting committed as agent version 2 and real console chat tested; approved key/configuration, version 2 metadata and `CALL_PROVIDER=dry_run` saved in Render with Save only. Telephony/application API integration remains unverified; user selected browser/simulator instead of phone rental.
- Integrated localhost HTTP: bed discharge/ready, doctor document save/publish, own-patient OTP/read/acknowledgement passed; evidence `.build/qa-integrated-http.json`.
- **Combined suite after webhook/frontend hardening: 930 passed, zero failures, zero expected failures in 1151.77 seconds**, before the final startup/phone-preservation guards. Earlier runs remain historical and are not added to this total.
- Startup preservation guards: **5 focused checks passed** (approximately 30 seconds), `.build/pytest-startup-preservation.log`.
- Latest phone preservation and PIN verification: **28 passed**, `.build/pytest-seed-phone-preservation.log`. These final focused runs are not folded into the 930-test full-run total.

Historical expected-failure markers are resolved in the current test suite:

| Earlier regression category | Current status |
| --- | --- |
| Webhook authentication and transport/outage error handling | Fixed; current regressions pass |
| Exact typed Tamil/Malayalam red-flag and stop phrases | Fixed; deterministic phrase regressions pass; broader native-speaker review remains needed |
| Newly registered patient shortcut, OTP resend and forged forwarded-IP behavior | Fixed; submission regressions pass |
| Current expected failures | **None** — final run reports zero xfails |

Local browser checks verified doctor registration, manual notepad draft and reviewed publication, OTP login, patient medicines, patient dose reporting and prescription print data. At 375 px the medicines and prescription print pages had no horizontal document overflow. Consent and appointments were browser-verified earlier. Latest discharge browser evidence showed the patient's published version 1 and print view, plus doctor replacement version 2 saved and published. The integrated HTTP evidence above adds bed/discharge transitions and own-patient acknowledgement. These are specific checks, not a claim that every role, viewport or latest webhook path completed browser verification. No closed-app push, real SMS, hardware measurements or completed live phone call has been verified.

The complete local browser call simulator was verified: Ravi answered the simulated AI check-in, selected mild pain, explicitly requested a callback and received a neutral ending. The screen showed **Nurse review requested**. Logging in through Try Nurse showed the actual **Sister Anjali** identity and Ravi's check-in call/nurse-review request in the inbox. Screenshots: `.build/qa-evidence/simulated-ai-callback.png` and `.build/qa-evidence/nurse-callback-alert.png`. This is simulator browser evidence, not a Sarvam telephone/API/webhook result.

## Remaining work and material prototype limits

1. Finish the readable deck's cover refinement and Claude-owned narrated video; review their final artifacts before submission.
2. Complete the specific remaining browser checks in `docs/qa/CODEX_FINAL_BROWSER_QA.md`, including bed discharge/ready clicks, loaded session-source labels and any required PDF export. Department and discharge exist and are mounted; a dedicated department login remains Planned.
3. Complete any additional live browser smoke checks required for submission. Checkpoint 6755f77 is already published/deployed and its live HTTP readiness passed. Preserve all schema and sample data; do not reset the live database as a setup shortcut.
4. Record the now browser-verified simulator call-to-nurse workflow honestly. A real Sarvam console chat can be shown as separate provider evidence; phone rental and live telephony are deferred.
5. Real SMS OTP requires a delivery adapter and provider setup. Physical spirometer input requires firmware, transport, mounting/calibration and real-device validation. These cannot be certified by simulated tests.

Locks, rate limits and consent/OTP serialization assume one application process. Production multi-worker operation needs database transactions/shared counters. Existing prescription publication is not fully transactional across replacement, dose refresh and audit writes; failures after approval can still need recovery. The reviewed-event guard is not a distributed idempotency solution. No clinical outcomes or production readiness are claimed.

Department operations and discharge documents persist bounded/versioned app_settings aggregates protected by per-process locks. They need transactional database compare-and-swap/normalized tables before multiple workers. Bed operations update patient display fields separately with compensation; process termination between writes remains a risk. Discharge documents allow at most 100 history versions per patient in this prototype. Acknowledgement records reading only, not consent or clinical adherence.

## Live deployment verification

Render deployed **6755f77**. Live GET/readiness checks returned 200 for registration, OTP login, prescription print, patient visits, doctor day, department operations, patient care and the public hospital-choice endpoint. Health reports Supabase, demo mode true, v2 missing false and LLM enabled true. Live registry entries show bed operations Live, OTP Simulated, doctor My day Live, appointment booking Live and discharge print Live. These checks verify publication and HTTP readiness; the full local patient/doctor/nurse journeys and local sample Gemini SDK request are separate evidence. No complete live browser acceptance, new live Gemini request or Sarvam phone/API-webhook integration is claimed.

## Additional live browser read checks

On the deployed service, Try as Doctor opened the actual Dr. Meera My day view with the 12 October schedule loaded. Ravi's sample patient medicines screen loaded the approved schedule and print/care/visits/assigned-breathing links; AI consent was off by default. These observations verify live read/navigation behavior only. No new live prescription publication, dose report, care acknowledgement or Gemini provider request is claimed.
