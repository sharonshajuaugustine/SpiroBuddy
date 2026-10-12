# Appointments: handoff (Claude checker, 12 Oct 2026)

**Verdict: works end to end, with gaps.** A patient can ask for a visit, the doctor can confirm it, suggest another time or decline it, and the patient sees each answer in words. Nothing is committed. No shared file was touched. The patches in section 5 are written out for Codex to apply.

## 1. What is finished

New files only (all in the working tree, none committed):

- `backend/app/routes_appointments.py` (11 routes, loaded by `main.py` automatically)
- `backend/app/appointments/` (`__init__.py`, `words.py`, `slots.py`, `service.py`)
- `tests/test_appointments.py` (25 tests)
- Pages: `web/patient-visits.html`, `web/doctor-day.html`, `web/appointments.html`
- Scripts and style: `web/js/patient-visits.js`, `web/js/doctor-day.js`, `web/js/appointments.js` (shared helpers plus the appointments page), `web/css/appointments.css`

Routes (as in Contract I):

- Staff: `GET/PUT /api/doctors/{doctor_id}/availability`, `GET /api/slots`, `GET/POST /api/appointments`, `POST /api/appointments/{appt}/{confirm|propose|decline|cancel|attended|no-show}`, `GET /api/doctor/day`
- Patient: `GET /api/me/appointments`, `GET /api/me/slots`, `POST /api/me/appointments`, `POST /api/me/appointments/{appt}/{accept|decline|cancel}`

Extra fields (harmless): `upcoming` on each visit and `counts.waiting_for_patient` on the doctor's day.

## 2. Test results (exact)

- Before my edits: `.venv/Scripts/python.exe -m pytest tests/test_appointments.py tests/test_auth.py tests/test_isolation.py -q` gave `59 passed in 195.36s (0:03:15)`.
- After my edits (I only changed `web/css/appointments.css`): `.venv/Scripts/python.exe -m pytest tests/test_appointments.py -q` gave `25 passed in 23.32s`.

## 3. Safety rules, checked in code, tests and by hand against a live local server

| Rule | Result |
|---|---|
| Double booking | Three layers: a check before the write, a lock around check and write, and the database unique index (its error also becomes 409 "That time was just taken. Please choose another."). A test with 4 real threads gets one 200 and three 409. By hand: staff booking a taken time gives 409. |
| Past or odd times | Past, more than 180 days ahead, junk text, a time that is not a free slot (10:07), a reason over 300 characters: all 400. A slot request for a past date gives an empty list. |
| Other hospital | Riverside admin gets 404 for the patient, the doctor, the slots, the availability and the appointment of Dawnlight. |
| Patient sees only their own | Patient 1 cannot cancel patient 2's visit (404) and does not see it in the list. A patient session on staff routes is refused (401, because the middleware treats it as "no staff login"). |
| Nurse needs `manage_appointments` | Nurse Thomas (no permission): 403 on the list and on slots, and no access to patients outside his keys. Nurse Anjali (has it): works inside her scope. Nurses cannot change a doctor's hours (403). |
| Doctor limits | A doctor cannot open another doctor's day (403) or change another doctor's hours (403). |
| Attended and no-show | Only on a confirmed visit whose date is today or earlier. A future or unconfirmed visit gives 409. |
| Wrong state | Confirm twice, cancel twice, accept a plain request, unknown action: 409 or 404 with a plain message. |
| Audit | Every write leaves an audit row (tested for all 11 actions, plus availability). A refused action writes nothing. The decline reason text is never stored, only "reason given". |
| Status words | Exactly: Requested, Confirmed, Alternative proposed, Declined, Cancelled, Attended, No-show. |
| Forbidden words | No payment or diagnosis words in any of the new files. The "A problem" choice shows the fixed line "tell your nurse now or call 112". |
| Header | A write without `X-SB: 1` gets 403. |

## 4. Browser checks (real Chrome through Playwright, own server on port 8013, now stopped)

Two separate browser contexts: the patient at 375 px, the doctor at 1440 px. Doctor logged in through `/login.html` with "Try as Doctor". I ran the whole journey twice, once in light and once in dark, with different patients.

- (a) Patient asks for a visit: "Requested".
- (b) Doctor opens `/doctor-day.html`: the request is under "Needs your answer". Confirm.
- (c) Patient reloads: "Confirmed", "Monday, 12 October 2026, 9:30 AM".
- (d) Second request. Doctor picks "Another time". Doctor sees "Waiting for the patient". Patient sees "Alternative proposed", presses "Yes, this time is fine", and now has two Confirmed visits.
- (e) Third request. Doctor declines with a reason. Patient sees "Declined" and the reason.
- Also looked at: the doctor day at 375 px, the appointments list at 1440 and 375 px, the "Book a visit" dialog (admin books for Abdul Rahman; the doctor switches to Dr. Kabir Rao by itself; the visit shows Confirmed), logged-out staff pages ("Please log in" card), logged-out patient page (calm "open from your app" card), a patient with no doctor ("No doctor is assigned to you yet. Please ask the hospital."), Hindi at 375 px.
- Result: no console errors, no failed requests (the only 4xx was the expected 401 for a logged-out visitor), no sideways scroll in any view. I looked at 11 screenshots by eye (patient proposal, ask flow, declined, Malayalam ask view, doctor request, propose dialog, doctor day at 375 px, appointments list, book dialog, both logged-out pages), in light and dark.
- Size rules measured by script on the staff pages, the book dialog and the patient pages: no text under 18 px, no heading under 24 px, every button, field and select at least 48 px high on staff pages and at least 64 px on patient pages.
- All four languages (Hindi, English, Tamil, Malayalam) x 4 patients, home and ask views at 375 px: text does not run out of its card or the page.

**What I fixed (all in `web/css/appointments.css`):**

1. Staff text was 17 px (labels, "Reason", place line, "7 visits", the small date): raised to 18 px.
2. The day headings in the appointments list were 20 px: raised to 24 px.
3. Two small patient labels were 17.6 px ("Today", "You are asking for"): raised to 18 px.
4. Long Malayalam words in two headings ("Coming up", "What is it about?") ran past the screen edge at 375 px and caused sideways scroll. They now wrap.

## 5. Proposed changes to shared files (not applied)

**a) `web/js/api.js` line 55: send logged-out visitors to the login page automatically.**

Before:
```
const STAFF_PAGES = ['/dashboard.html', '/doctor.html', '/prescribe.html', '/patient.html', '/demo.html', '/units.html', '/collect.html', '/branding.html'];
```
After:
```
const STAFF_PAGES = ['/dashboard.html', '/doctor.html', '/prescribe.html', '/patient.html', '/demo.html', '/units.html', '/collect.html', '/branding.html', '/doctor-day.html', '/appointments.html'];
```
(Until then the pages show their own "Please log in" card with a Log in button, which also works.)

**b) `web/js/ui.js`, old shell `PAGES` (after the "Register patient" line):**
```
    { group: 'Ward', href: 'doctor-day.html', label: 'My day', key: 'doctor-day', icon: 'calendar' },
    { group: 'Ward', href: 'appointments.html', label: 'Appointments', key: 'appointments', icon: 'calendar' },
```
The pages already call `SB.ui.boot('doctor-day')` and `SB.ui.boot('appointments')`, so the link shows as current.

**c) `web/js/ui.js`, new shell `HOSP_NAV`:** it already lists `/hospital/appointments.html` and `/hospital/availability.html`, and the folder `web/hospital/` does not exist yet. Either change the Appointments entry to `href: '/appointments.html'` and add `{ group: 'Care', key: 'doctor-day', href: '/doctor-day.html', label: 'My day', icon: 'calendar', roles: ['doctor'] }`, or make `/hospital/appointments.html` a copy or redirect of our page.

**d) `web/app.html`, a "My visits" button under the medicines button.**

Add after line 151 (`<a class="pa-btn primary" id="meds-link" href="meds.html"></a>`):
```
    <a class="pa-btn" id="visits-link" href="patient-visits.html"></a>
```
Add after the line that sets `#meds-link` href (about line 249):
```
      $('#visits-link').innerHTML = ic('calendar', { size: 24 }) + esc(tr('visits'));
      $('#visits-link').href = 'patient-visits.html?id=' + pid + '&lang=' + lang;
```
Add `visits` to the four language tables in `app.html`: English `My visits`, Hindi `डॉक्टर से मुलाक़ातें`, Tamil `என் மருத்துவ சந்திப்புகள்`, Malayalam `എന്റെ ഡോക്ടർ സന്ദർശനങ്ങൾ`.

**e) `backend/app/features.py` (lines 178-183), what each key can honestly say:**

- `appt.booking`: `live`. Patient asks, doctor confirms, suggests another time or declines, patient answers; it works end to end on the sample hospital. Keep the note honest: "in the app only, no SMS or WhatsApp is sent".
- `appt.availability`: keep `in_development`. The API and the default hours (Monday to Saturday, 9:30 AM to 1:00 PM, 15-minute slots) work, but there is no screen where a doctor edits hours or leave days.
- `appt.reminders`: keep `in_development`. Nothing is built.
- `doctor.my_day` (line 129, now `planned`): can become `live` for the visits part only. The page shows requests, proposals and visits. It does not show prescriptions ending, patients to call or missed doses, so change the note to say so.
- `doctor.ot_reminders` and `appt.teleconsult`: stay `planned`.

**f) `docs/ARCHITECTURE.md` section 18:** replace the short table with the shapes in `appt_backend_notes.md` (state, status_words, when_words, can, upcoming, doctor/day, me/slots).

## 6. Honest gaps (not done or not tested)

- No screen to edit a doctor's hours or leave days (the API works and is tested).
- No reminders, no WhatsApp or SMS, no calendar file, no rescheduling of a confirmed visit (cancel and ask again).
- A patient can have at most 3 requests waiting. The 4th gets a plain 409 message.
- Staff can book any future time, including a leave day or outside the doctor's hours (by design of Builder A). Patient requests must be one of the free slots.
- If staff book a visit with a doctor who is not the patient's own doctor or on the care team, that doctor cannot see it (the middleware answers 404 for patients they cannot see). I did not change the middleware.
- Nurses have no route to list doctors. A nurse sees only doctors who already have visits. Fix: `GET /api/doctors` for staff with `appt.manage`.
- Tamil and Malayalam wording is not checked by a native speaker.
- Not tested: a real phone, Safari, Firefox, the Supabase database (the "duplicate key" text match is covered only by a unit test), and more than one server process at the same time (the lock is per process; the database index covers the rest).
- The logged-out staff pages have an empty band above the title at 375 px. The shell (`ui.js`) causes it; `/register.html` does the same.
- A logged-out visitor on the patient page sees Hindi first (same default as the medicines page).
- Other test files were not run (Codex has edits in progress). The three files named above are the only ones judged.
