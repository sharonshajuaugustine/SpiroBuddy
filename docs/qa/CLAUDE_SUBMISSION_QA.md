# Independent QA report: Aarogya Saathi + SpiroBuddy demo

Tested by the Claude QA session. Nothing in the application was edited, committed or deployed.

## Bottom line

The doctor to patient to nurse journey works end to end on a local copy. Of 247 checks, 229 passed, 13 failed (7 separate problems, F-1 to F-7 below, plus a polish list F-8), 1 could not be verified and 4 are notes. Nothing is a "demo will not run" blocker in the code. Two things need attention before submission:

1. **The live site is behind the local code.** On https://spirobuddy.onrender.com the new pages `patient-login`, `patient-pin`, `register`, `prescription-print`, `appointments` and `doctor-day` all answer 404, and the home page still has the old headline. The check against the live site will not see the OTP, registration or print journey until it is redeployed.
2. **The nurse alert for a missed medicine was unreadable in my final pass (F-1).** The inbox row said "Medicine follow-up at 2026-10-12T02:30:00+05:30" with no patient name (an edit to `backend/app/meds/reminders.py` at about 04:01). Another session fixed it at 04:38:45; I re-checked it on a fresh alert (5.40, 5.41) and the regression test now passes. Make sure the redeploy includes that fix.

## Test conditions (read this before trusting any result)

| Item | Value |
|---|---|
| Date and time | Mon 12 Oct 2026, 03:47 to 04:45 IST (system clock). Final full pass 04:25 to 04:34; the F-1 re-check and the last test run came after 04:38. |
| Commit | `043e0c7` at the start, `bb20be5` at the final pass (`git rev-parse --short HEAD`). Other sessions committed during testing. |
| Working tree | **Contained other sessions' uncommitted changes the whole time** (about 70 changed or new files). A failure can come from half-finished work. Files that changed under me while I tested: `backend/app/patient_otp.py`, `routes_me.py`, `routes_meds.py`, `meds/reminders.py`, `main.py`, `web/js/patient-otp.js`, `web/js/meds-patient.js`, `web/prescription-print.html`. The final pass started after all of them (only `web/js/patient-ai-consent.js` changed later, and no flow uses it). |
| Server | Local copy on `127.0.0.1:8021`, fresh data folder, never port 8010. `GET /api/health` returned `data_backend: demo`, `data_note: demo SQLite`, `llm_enabled: false`, `whatsapp_enabled: false` before any test. |
| Deployed site | Read only: public pages and `/api/features`. No login, OTP, prescription or reset there. |
| Browser | Playwright with installed Chrome, widths 375 (phone, touch) and 1440. Real phones were not used. |
| Data | Artificial patients only (`QA-1001`..`QA-1005`, `QA-2001`, fake numbers `+91900000001x`, plus the seeded sample patients). |

### Launch command (variable names only, no values)

The local `.env` holds live credentials, so the server was started with these names blanked in the process. python-dotenv never overrides a variable that already exists, even when empty. A PowerShell assignment such as `$env:X = ""` deletes the variable instead, so do not use that to blank them.

```
SPIROBUDDY_DATA_DIR=<fresh empty folder>  DEMO_MODE=1  DATA_BACKEND=demo  DEMO_AUTOPILOT=0
COMMS_TICKER=1  COMMS_AUTO_ESCALATE=0  COMMS_CONSENT_RENEWAL=0  CALL_PROVIDER=dry_run  ALLOW_TRAINING=0
blank: SUPABASE_URL SUPABASE_SERVICE_ROLE_KEY ANTHROPIC_API_KEY GEMINI_API_KEY SARVAM_API_KEY
       SARVAM_AGENT_API_KEY SARVAM_AGENT_ID TWILIO_ACCOUNT_SID TWILIO_AUTH_TOKEN TWILIO_WHATSAPP_FROM
       EXOTEL_API_KEY EXOTEL_API_TOKEN DEMO_*_WHATSAPP DEMO_*_PHONE NURSE_DESK_PHONE PUBLIC_BASE_URL RX_TOKEN_SECRET
.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8021
```

A shell-independent launcher that does the same (`os.environ[name] = ""` before `uvicorn.run`) was checked on port 8022 and gave the same health answer. It is reproduced in `CLAUDE_DEMO_SCRIPT.md`.

## Results matrix

Result key: PASS, FAIL, NOT VERIFIED. All rows are **local**. The deployed site could only be compared (see below).

| # | Flow | Result | Checks (pass / fail / other) | Evidence | Limits |
|---|---|---|---|---|---|
| 1 | Doctor sign-in, register patient, notes, notepad draft, approve | **PASS** (1 polish fail) | 52 / 1 / 0 | `m375_register_*`, `m375_prescribe_*`, `d1440_prescribe.png` | Real AI extraction not run (no Gemini key). Draft used the manual `\|` format. The AI review record was tested with a fixture row, not a real AI call. |
| 2 | Patient hospital number + OTP, PIN fallback | **FAIL** (core passes, 3 defects) | 38 / 3 / 1 note | `m375_patient_otp_*`, `m375_patient_pin.png` | Simulated delivery only; no SMS exists. Expiry tested by moving the stored expiry into the past. |
| 3 | Patient medicines on a phone, dose taken, print, reminders | **PASS** | 24 / 0 | `m375_meds_*`, `m375_print_view.png`, `print_view_prescription.pdf` | Spoken audio not listened to. Closed-app reminders are not built (registry: Planned). |
| 4 | Breathing only when assigned; bad / partial sessions; staff view | **FAIL** (1 defect) | 35 / 1 | `m375_breathing_*`, `d1440_staff_chart_with_simulated_session.png` | Browser simulator only. No hardware exists. |
| 5 | Nurse sign-in, missed-dose alert, scope, no duplicates, clearing | **PASS after fix** (F-1 failed in the final pass, was fixed at 04:38 and re-checked) | 22 / 3 (fixed) / 0 | `m375_nurse_*`, `d1440_nurse_*` | Overdue dose made by moving one dose time in the test database (no clock control exists). No family message exists to test. |
| 6 | Authorization (patient, nurse, doctor, admin, other hospital) | **FAIL** (rate limit) | 27 / 2 / 1 not verified | `all_checks.csv` rows 6.xx | Demo reset by a doctor not executed (to keep the test data). |
| 7 | 375 px and desktop layout, links, wording | **FAIL** (3 pages scroll sideways) | 31 / 3 / 3 notes | `m375_doctor_dashboard.png`, `m375_user_menu_open.png` | Chrome emulation, not a real phone. |

Every individual check, with its status and detail, is in `docs/qa/evidence/all_checks.csv`.

## Failures

Severity: **High** = visible in the demo or breaks a claim; **Medium** = real defect, workaround exists; **Low** = polish.

### F-1 (High, FIXED at 04:38:45 and re-checked) Missed-dose alert row had no patient name and a raw timestamp
- **Reproduce:** register `QA-2001`, issue a prescription, make a dose more than 60 minutes overdue, open `/dashboard.html` as Sister Anjali. Checks 5.02b, 5.31.
- **Expected:** "QA Sample UI One: medicine follow-up at 12 Oct 02:30 AM".
- **Actual (before the fix):** "Medicine follow-up at 2026-10-12T02:30:00+05:30". The API's `patient_name` was correct, but the row shows only the title.
- **After the fix:** "QA Sample UI One: medicine follow-up at 12 Oct 2026, 02:45 AM" (check 5.41, `m375_nurse_alert_row_after_fix.png`). Alerts already stored with the old ISO title still read badly, and `web/js/comms-dashboard.js:47` still prints only the title.
- **Source:** `backend/app/meds/reminders.py:49` (`title = f"Medicine follow-up at {due}"`); `web/js/comms-dashboard.js:47` prints `a.title` only. Evidence: `m375_nurse_new_alert_row.png`.
- Regression test: `test_missed_dose_alert_title_names_the_patient_and_uses_a_readable_time` (was a strict xfail; the marker was removed with the fix and the test now passes).

### F-2 (Medium) While `DEMO_MODE=1`, anyone can skip the OTP
- **Reproduce:** `POST /api/me/session` with `{"patient_id": 101}` and header `X-SB: 1`. Check 2.40. It returns 200 and the patient cookie, also for a patient the doctor just registered.
- **Expected:** a patient registered by a doctor needs the OTP (or the doctor's personal link).
- **Source:** `backend/app/routes_auth.py:446-456` (`patient_session`, the "demo id" branch). Patient ids are small numbers.
- **Why it matters:** the pitch says "hospital number + OTP". While demo mode is on, OTP is a demonstration, not a lock. Whether Render runs with `DEMO_MODE=1` was not checked (the setting defaults to on when unset, `config.demo_mode`).
- Regression test: `test_patient_id_shortcut_does_not_open_a_doctor_registered_patient` (strict xfail).

### F-3 (Medium) Asking for a code again inside 60 seconds leaves the patient stuck
- **Reproduce (API):** two `POST /api/me/otp/request` calls for the same number within 60 s. The second reply has a new `challenge_id` and no code; the code from the first reply then fails against the new id (check 2.18) although it is still valid with the first id (2.18b).
- **Reproduce (page):** `/patient-login.html`, request a code, reload the page, request again at once. No sample code appears and the first code is refused for up to a minute (check 2.71, `m375_patient_otp_reload_resend_no_code.png`). The page now disables "send again" for 60 s (2.70), which hides the problem unless the page is reloaded.
- **Source:** `backend/app/patient_otp.py:65-66` (also `:64`, `:70`, `:75`) return a fresh random `challenge_id` while throttled; `web/js/patient-otp.js` keeps the latest one.
- Regression test: `test_second_code_request_inside_cooldown_leaves_the_patient_able_to_log_in` (strict xfail).

### F-4 (Medium) Staff cannot tell a simulated session from a measured one
- **Reproduce:** run the simulator on `/app.html?id=<patient>`, then open the doctor's `patient.html?id=<patient>`. Check 4.34.
- **Expected:** each row in "Recent sessions" says where it came from (simulator, app, device).
- **Actual:** columns are Time, Slot, Breaths, Best, Average score, Breath quality. The word "Simulated" appears only on the assignment card and on the patient's own page ("Simulator (no device connected)").
- **Source:** `web/patient.html` around lines 200-207 (sessions table). `GET /api/patients/{pid}/sessions` already returns `source` (`demo` for the simulator, `app` otherwise; the browser cannot claim `device`, check 4.10).
- **Related:** `backend/app/main.py` `post_session` stores the simulator as `app` when `DEMO_MODE` is off, so outside demo mode the two cannot be told apart (code reading only).

### F-5 (Medium) Hospital pages scroll sideways on a phone
- **Reproduce:** 375 px wide, sign in, open `/dashboard.html` or `/patient.html?id=...`. Checks 7.02, 7.05, 7.30. Page is 399 px wide (24 px too wide); the top menu tabs are cut off ("Reg...").
- **Source:** the header chips `.sys-state` / `.sys-why` inside `.header-right` (`web/css/styles.css:164`). Register, prescribe, meds, print and public pages do not scroll sideways.

### F-6 (Medium) The per-IP limits can be reset by sending a made-up header
- **Reproduce:** 20 `POST /api/me/otp/request` calls get 429. The same calls with different `X-Forwarded-For` values keep returning 200 (6.41). The staff login limit (10 tries) is bypassed the same way (6.42).
- **Source:** `backend/app/audit.py:21-31` (`client_ip` takes the first `X-Forwarded-For` value). Used by `ratelimit.allow` in `routes_me.py` (OTP), `routes_auth.py` (login, patient session) and `routes_meds.py` (`rx-check`).
- **Not verified:** whether Render's proxy overwrites or appends the header. The per-patient OTP lock (5 wrong codes) and PIN lock still work (2.14, 2.32).
- Regression test: `test_per_ip_limit_cannot_be_reset_with_a_forged_forwarded_for_header` (strict xfail).

### F-7 (Low) Notes show "Staff #2" instead of the doctor's name
Check 1.65. `web/js/consultation.js` prints `Staff #${r.author_id}`; `GET /api/patients/{pid}/notes` (`routes_patients.py:notes`) returns only `author_id`. The registry says "with author and time".

### F-8 (Low) Polish found while testing
- Touch targets under 44 px: alert buttons 36 px high, top-bar logo 30 px, `logout-btn` 26 px, patient-login links 24 px (7.01, 7.20, `5.22`).
- Patient OTP page is plain and unlike the rest of the app: no shared header, only English and Hindi (the app offers four), the footer is not translated, the title says "Aarogya Saathi" while every other page says "SpiroBuddy" (2.50, 7.21).
- `register.html`, `patient-login.html` and `prescription-print.html` have no `<link rel="icon">`, so the browser asks for `/favicon.ico` and logs a 404.
- "Post-op Ward 3B" and the hospital name are typed into `web/js/ui.js:15` and the print header of `web/patient.html:14`.
- A custom hospital number typed without its dash (`QA1004` for `QA-1004`) is not found (2.24). Generated numbers work with or without it.
- Sessions made outside 08:00 to 21:00 count toward the 08:00 slot (`rules.clamp_slot_hour`): a session at about 04:00 completed the 8 am slot (4.01).
- Alert inbox tab strip is clipped at 375 px ("Resolve", "All" cut).

## What passed (the evidence behind the green rows)

- **Doctor:** header and account menu show the signed-in doctor and hospital; the registration form rejects bad age, sex, phone, language, doctor and duplicate numbers (even `qa-1001` for `QA-1001`) and leaves no stray rows; a nurse, admin or other doctor cannot record a consultation or draft a prescription.
- **Draft vs approval:** the notepad draft creates no prescription, no medicines and no dose rows (1.33, and in the UI the "Current medicines" box still says "No current prescription", 1.67). The page blocks sending while fields say "Needs review", then shows a confirm list, and only then issues (1.68 to 1.70). The patient's schedule contains only approved lines (1.44).
- **OTP:** unknown numbers get the same wording as real ones (2.02); a code is single use (2.12), expires (2.17), is stored hashed (2.17b), locks after 5 wrong tries (2.14, 2.15), and does not cross hospitals (2.05 to 2.07). Changing the registered phone kills an outstanding code (2.20). A patient with no phone gets no code and staff see "Phone number pending" (2.08, 2.35). The sample phone box is labelled "Sample phone Simulated" (2.51). The PIN is labelled "reusable ... not a one-time code" on the chart (`d1440_staff_chart_with_simulated_session.png`).
- **Medicines on a phone:** name, strength, "1 tablet", time, food timing and note are readable at 375 px with 24 px names (3.20, 3.21); "I took it" becomes "Reported at 4:29 AM" and survives a reload (3.23, 3.24); the pharmacy card and QR draw (3.28); a replaced prescription's QR says "no longer current" (3.10); the print view has no raw codes and the print stylesheet hides the buttons (3.29 to 3.31). Spoken reminders are opt-in and say "while this page is open" (3.26).
- **Breathing:** empty, malformed, NaN, infinite, negative, zero-peak, 101-breath and future-dated sessions are refused (4.02 to 4.05). A 5-breath session is saved but does not complete the slot (4.06b). An unassigned patient is refused by the server for patient and staff (4.13, 4.14) and the app says "Breathing exercise is not assigned" (4.22). A browser cannot claim hardware (4.10).
- **Nurse:** the missed dose raised one alert within 12 s with no patient app open (5.01); it stays single through repeated checks (5.03), is visible only to Sister Anjali, Dr. Meera and the admin (5.04), records the signed-in nurse even if the request names someone else (5.06, 5.07), clears within about 30 s of the patient's report (5.08; the check runs every 30 s), is not re-raised (5.09, 5.11), and sends no message (5.12).
- **Authorization:** 30 role by endpoint combinations behaved as designed, including 404 for other hospitals and other patients and 403 for nurse and admin on doctor-only actions (6.01 to 6.25).

## Deployed site (read only, 12 Oct about 04:12 IST)

| Page | Local | Deployed |
|---|---|---|
| `/` headline | "Every breath, coached and counted." | "After surgery, the hospital stays connected to the patient at home." |
| `/patient-login.html`, `/patient-pin.html`, `/register.html`, `/prescription-print.html`, `/appointments.html`, `/doctor-day.html` | 200 | **404** |
| `/login.html`, `/dashboard.html`, `/meds.html`, `/prescribe.html`, `/impact.html`, `/trust.html`, `/vision.html`, `/architecture.html`, `/units.html`, `/rx.html` | 200 | 200 |
| `/api/features` | 112 entries (37 live, 10 simulated, 30 in development, 35 planned) | 108 entries (30 live, 9 simulated, 34 in development, 35 planned) |

Registry entries that differ: `auth.patient_regno`, `chart.notes`, `doctor.enrol`, `doses.missed_alert`, `doses.reminders` (live locally, in development there), `hospital.branding` (live locally, planned there), and `auth.patient_otp`, `auth.otp_sms`, `rx.notepad`, `rx.print` (missing there). Never describe a local feature as live on the site until it is deployed.

Registry wording that no longer matches the build: `app.patient` says "no login" (there is now OTP and PIN); `chart.notes` says "with author" (the page shows a staff number). `CLAUDE.md` calls the PIN a "one-time desk code" but the build and the registry say it is reusable (2.31).

## Commands and actual results

| Command | Result |
|---|---|
| Scripts, copied to `docs/qa/evidence/scripts/` (paths inside point at this session's scratch folder; edit `DB`, `EV` and the launch script before reuse): `qa_part1..4.py` (API), `qa_ui_a..h.py` (Chrome), `qa_part5.py` (rate limit), run in that order by `run_all.sh` on a fresh server (`g` and `h` were run afterwards) | 247 checks: 229 pass, 13 fail, 1 not verified, 4 notes. Table: `docs/qa/evidence/all_checks.csv` |
| `pytest tests/test_submission_flow.py tests/test_patient_login.py tests/test_meds.py tests/test_auth.py tests/test_isolation.py` (provider variables blanked; the conftest also uses a temp folder) | **125 passed** in 297 s (04:14 to 04:19 IST) |
| `pytest tests/test_claude_submission_regressions.py -rxX` | First run 04:20: 8 passed, 4 xfailed. Last run 04:40, after the F-1 fix: **9 passed, 3 xfailed** in 87 s. The 3 xfails are confirmed defects F-2, F-3 and F-6 and become failures (strict) the moment they are fixed |
| Full test suite | Not run by me (13 minutes, shared tree). Another session's earlier run (`scratchpad/full_suite_3.txt`) reported 5 failures in `test_critical`, `test_public` and `test_supabase_store`, none in this QA scope |

The new test file asserts the correct behaviour; no assertion was weakened and no existing test was touched.

## Not verified

- Real Gemini notepad extraction, real SMS, real WhatsApp, Sarvam voice and any Supabase-backed run (all blanked on purpose).
- Anything that needs a logged-in or writing action on the deployed site (not allowed).
- Whether Render sets `DEMO_MODE=1` and how its proxy builds `X-Forwarded-For`.
- Spoken reminders and "read aloud" audio, a real QR scanner, real Android or iPhone browsers, screen readers, print on paper.
- Hindi, Tamil and Malayalam wording quality (only seen on screen, not read by a speaker).
- Real-time behaviour: the 15 minute lock, the 60 s resend gap (partly seen), alert grace by real clock. Expiry and overdue doses used database fixtures in the isolated copy.
- Concurrency or load, multi-process OTP races, other browsers than Chrome.
- Department, beds, discharge, appointments and doctor-day journeys (owned by other sessions; only checked that pages exist).
- Demo reset by a Dawnlight doctor or admin (allowed by design; not run, 6.26).
- Hardware, Bluetooth, store apps: not built (registry: In development or Planned).
