# Fix handoff for Codex (from the independent QA, 12 Oct 2026)

Companion to `docs/qa/CLAUDE_SUBMISSION_QA.md` (reproductions, evidence, check numbers). No application file was edited by QA. Each fix below is the smallest change that closes a **verified** defect. Three have a strict-xfail test in `tests/test_claude_submission_regressions.py` (fixes 2, 3 and 6 below): delete its `@pytest.mark.xfail` marker when you fix it.

## Top five fixes (do these, in this order)

The missed-dose alert text (item 1 of my first list) was already fixed by another session at 04:38:45 and re-checked, so it is not in the top five any more. It is kept below, marked fixed, for the record.

| # | Fix | Where | Effort |
|---|---|---|---|
| 1 | Stop the `patient_id` shortcut from opening doctor-registered patients (the OTP can be skipped) | `backend/app/routes_auth.py:446-456` (`patient_session`) | 10 min |
| 2 | Asking for an OTP again inside 60 s must not strand the patient | `backend/app/patient_otp.py:65-66`, `web/js/patient-otp.js` | 15 min |
| 3 | Show where each session came from in the staff "Recent sessions" table | `web/patient.html` ~lines 200-207 | 10 min |
| 4 | Stop the 24 px sideways scroll of dashboard and patient chart at 375 px | `web/css/styles.css:164` (`.header-right`, `.sys-state`, `.sys-why`) | 10 min |
| 5 | Per-IP limits must not be resettable with a made-up `X-Forwarded-For` | `backend/app/audit.py:21-31` (`client_ip`) | 5 min |

Still open on the alert fix: show `patient_name` in `web/js/comms-dashboard.js:47`, so alerts saved before the fix also name the patient. After the five: "Staff #2" on notes (fix 7) and the polish list.

## Submission blocker that is not a code fix

**B-1 Redeploy and smoke-test.** The live site is missing the whole new journey (read-only check, about 04:10 IST): `/patient-login.html`, `/patient-pin.html`, `/register.html`, `/prescription-print.html`, `/appointments.html`, `/doctor-day.html` return 404; the home page still has the old headline; `/api/features` has 108 entries against 112 locally and shows `auth.patient_regno`, `chart.notes`, `doctor.enrol`, `doses.missed_alert`, `doses.reminders` as "in development".
Before the 11:00 submission:
1. Deploy a commit that includes the alert-text fix and whichever of the five fixes above you finish, and run the full test suite on it.
2. On Render check `GET /patient-login.html` and `/register.html` return 200 and `/api/features` shows `auth.patient_otp` as `simulated`.
3. Confirm Render has `DEMO_MODE=1` (the sample phone only shows the code in demo mode) and that the Supabase tables and columns used by the new code exist: `app_settings` (key, hospital_id, value, created_at, updated_at, used for OTP state), `notes`, `ai_events` (decision, lines_total, lines_edited, lines_removed), `patients.routine`, `patients.app_token_hash`, the PIN columns. Not verified by QA (Supabase was blanked on purpose).
4. Smoke test with the sample patient only: "Use Ravi's hospital number", read the sample code, open medicines, tap "I took it". Do not run reset.

## Verified defects (smallest fix each)

### 1. Alert text (High, demo-facing) - FIXED at 04:38:45, re-checked (5.40, 5.41)
Before the fix `reminders.tick()` wrote `title = f"Medicine follow-up at {due}"`, so the nurse inbox shows "Medicine follow-up at 2026-10-12T02:30:00+05:30" and no patient. The inbox row prints only `a.title`.
```python
# backend/app/meds/reminders.py, where the title is built (line 49)
title = f"{p['name']}: medicine follow-up at {parse_dt(due).strftime('%d %b %I:%M %p')}"
```
`_matches_due()` already recognises that shape through its `endswith(": medicine follow-up at ...")` branch, so there is no duplicate risk. Keep its first branch for alerts already stored with the ISO title. Also show the name in the row even for old alerts: in `web/js/comms-dashboard.js` `row()` change the title line to `<b>${esc(a.patient_name || '')}</b> ${esc(a.title)}`.
Tests: `test_missed_dose_alert_title_names_the_patient_and_uses_a_readable_time` now passes (marker removed). `test_missed_dose_alert_is_scoped_single_and_cleared_by_the_patient_report` must stay green. The applied change is the one-liner above with the year added to the time.

### 2. OTP can be skipped in demo mode (Medium) [top-five item 1]
`POST /api/me/session {"patient_id": N}` returns a patient session for any N while `DEMO_MODE=1`, including patients a doctor just registered.
```python
# backend/app/routes_auth.py, patient_session(), in the "else:" branch after the DEMO_MODE check
from .seed import PROFILES            # the seeded sample patients 1..7
from .seed_auth import RIVERSIDE_PATIENT_ID
SAMPLE_IDS = set(PROFILES) | {RIVERSIDE_PATIENT_ID}
...
cur = authz.session_row(request.cookies.get(authz.PATIENT_COOKIE), "patient")
if int(pid) not in SAMPLE_IDS and not (cur and cur.get("patient_id") == int(pid)):
    raise HTTPException(403, "this patient signs in with the hospital number and a code")
```
Take care: the breathing page opens with `app.html?id=<n>`. After an OTP login the cookie already exists, so the `cur` clause keeps it working; test `/app.html?id=<registered patient>` right after an OTP login. Sample patients (Ravi, id 1) keep the one-tap demo path.
Test: `test_patient_id_shortcut_does_not_open_a_doctor_registered_patient` (xfail). `tests/conftest.py` `patient_client()` uses this shortcut for the sample patients 1 to 7, which stay allowed. My regression tests open doctor-registered patients with the personal link token, so this fix does not break them.

### 3. OTP resend dead-end (Medium, recoverable after 60 s) [top-five item 2]
While throttled (`issued_at` less than 60 s ago, locked, over 5 per hour) `request_code` returns a fresh random `challenge_id` and no code. The page keeps that id, so the code the patient already has (or saw) no longer verifies.
```python
# backend/app/patient_otp.py request_code(): in the cooldown branch (line 65-66)
if state.get("issued_at") and parse_dt(state["issued_at"]) + timedelta(seconds=60) > stamp:
    answer["challenge_id"] = state.get("challenge_id") or challenge   # hand back the id the first code belongs to
    return answer
```
```js
// web/js/patient-otp.js, in the request handler: keep the first challenge when no new code was issued
const d = await api('/api/me/otp/request', requestedIdentity);
const sameNumber = loginIdentity && loginIdentity.registration_no === requestedIdentity.registration_no && loginIdentity.hospital_id === requestedIdentity.hospital_id;
if (!(sameNumber && challenge && !d.demo_code)) challenge = d.challenge_id;
```
Unknown numbers have no stored state, so they still get a random id and the generic answer: nothing new is revealed. The sample code itself cannot be shown again (only the hash is stored): the message should say "Your code was sent a moment ago. Use it, or wait a minute for another."
Test: `test_second_code_request_inside_cooldown_leaves_the_patient_able_to_log_in` (xfail).

### 4. Session origin not shown to staff (Medium) [top-five item 3]
`GET /api/patients/{pid}/sessions` returns `source` (`demo` = browser simulator, `app`, `device`). The table in `web/patient.html` (rows built near lines 200-207) has no column for it.
```js
// header: <th>Source</th>   row cell:
`<td>${s.source === 'demo' ? 'Simulated (browser)' : s.source === 'device' ? 'Device' : 'App'}</td>`
```
Also consider (hypothesis H3 below) storing the simulator as `source: 'simulator'` even when `DEMO_MODE` is off. No automated test (browser only): check by running the simulator and reading the chart.

### 5. Sideways scroll at 375 px (Medium) [top-five item 4]
On `/dashboard.html`, `/patient.html` and other hospital-shell pages the page is 399 px wide. The wide elements are `.header-right` with `.sys-state` / `.sys-why` ("2 fallbacks on" chips).
```css
.header-right { min-width: 0; flex-wrap: wrap; }
@media (max-width: 480px) { .sys-why { display: none; } .header-right .sys-state { max-width: 100%; overflow: hidden; text-overflow: ellipsis; } }
```
Verify with `document.documentElement.scrollWidth - document.documentElement.clientWidth === 0` at 375 px on dashboard, patient chart and prescribe pages. QA's `METRICS_JS` helper is in `qa_ui_lib.py` in the session scratch folder if useful.

### 6. Per-IP limits reset by a made-up header (Medium) [top-five item 5]
`audit.client_ip()` (`backend/app/audit.py:21-31`) takes the **first** `X-Forwarded-For` value, which the client controls. Use the **last** value (the one the platform's proxy adds). That is correct whether the proxy appends or overwrites the header.
```python
fwd = [h.strip() for h in (request.headers.get("x-forwarded-for") or "").split(",") if h.strip()]
if fwd: return fwd[-1][:64]
```
Test: `test_per_ip_limit_cannot_be_reset_with_a_forged_forwarded_for_header` (xfail). After the change confirm on Render, using only a harmless GET, that rate-limited routes still see distinct visitors as distinct (hypothesis H1).

### 7. "Staff #2" on notes (Low)
`routes_patients.notes()` returns rows with `author_id` only. Add the name and use it:
```python
ids = sorted({r["author_id"] for r in rows if r.get("author_id")})
names = {s["id"]: s["name"] for s in authz.ident().select("staff", [("id", "in", ids)], columns="id,name")} if ids else {}
for r in rows: r["author_name"] = names.get(r.get("author_id"))
```
and in `web/js/consultation.js` print `esc(r.author_name || 'Staff')` instead of `Staff #${r.author_id}`.

## Polish (smallest first)

- Add `<link rel="icon" href="data:,">` to `register.html`, `patient-login.html`, `prescription-print.html` (the browser logs a 404 for `/favicon.ico`).
- `web/js/ui.js:15` `SITE.ward = 'Post-op Ward 3B'` and the print header in `web/patient.html:14` hard-code the sample hospital and ward. Use `me.hospital.name` and drop the ward.
- Patient OTP page: use the same header and styling as `patient-pin.html`, offer all four languages, translate the footer, and make the title match the other pages (it says "Aarogya Saathi", the rest say "SpiroBuddy"); `web/patient-login.html`, `web/js/patient-otp.js`.
- Touch targets under 44 px: alert buttons (`.btn.sm`, 36 px), the top-bar logo link, `logout-btn`, the three links on `patient-login.html`.
- Alert inbox tab strip is clipped at 375 px: allow it to scroll or wrap (`#ai-tabs`).
- Custom hospital numbers typed without the dash are not found (`patient_login.regno_candidates` only handles the generated `ABC-000123` shape). Say "type it exactly as on your slip" on the page, which `patient-pin.html` already does.
- Wording: `CLAUDE.md` calls the PIN a "one-time desk code"; the build and registry say reusable. Align the doc (or make the PIN expire).
- Registry text: `app.patient` still says "no login"; `chart.notes` says "with author" until fix 7 is in.

## Hypotheses (not verified, do not treat as bugs yet)

- **H1** Render's proxy may append rather than overwrite `X-Forwarded-For`. QA proved only that the code trusts the first value.
- **H2** `config.demo_mode()` defaults to **on** when `DEMO_MODE` is unset. If Render lacks `DEMO_MODE=0` in a real deployment, codes would show on screen and fix 2's shortcut would still apply to sample ids.
- **H3** `main.py` `post_session` stores `source='app'` for the simulator when `DEMO_MODE` is off, so staff could not tell simulator from device data (code reading only).
- **H4** Anyone who knows a hospital and a number can lock that patient out of OTP for 15 minutes with 5 wrong codes (mechanism seen in check 2.14; impact not tested). The per-IP limit would normally slow this, but see fix 6.
- **H5** `reminders.tick()` reads every patient and their doses every 30 s. Fine for ten sample patients; with Supabase it becomes many network calls per tick.
- **H6** A session at 04:00 completes the 08:00 slot (`rules.clamp_slot_hour`), seen in checks 4.01 and 4.32. Probably intended for the sample, but it lets an out-of-hours session satisfy "done today".
- **H7** Doctors and admins of the sample hospital may call `POST /api/demo/reset` (`main.py` `DEMO_PREFIXES`). On the live demo site that wipes the demo data for everyone; the Demo panel has the button at the top.

## What to leave alone

Registration validation, the draft-versus-approval separation, OTP hashing/expiry/single use/lockout, hospital isolation, partial and malformed session handling, nurse scoping and actor names, and the pharmacy QR check all passed every test. Do not refactor them before submission.
