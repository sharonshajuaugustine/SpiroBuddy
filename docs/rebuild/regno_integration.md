# Patient login (registration number + PIN) – integration note for the lead

Builder P, Mon 12 Oct 2026. Brief: `docs/rebuild/REGNO_PIN_BRIEF.md`. Built and committed; the edits below are the ones in files I do not own.

## What exists now
- `backend/app/patient_login.py` – number generation, PIN make/verify, lockout, "columns ready?" probe.
- `backend/app/routes_me.py` – `POST /api/me/login` (public), `GET /api/me/login-demo` (public, DEMO_MODE only), `GET /api/patients/{pid}/login`, `POST /api/patients/{pid}/pin` (action `patient.edit`), `PUT /api/patients/{pid}/regno` (action `patient.edit`, staff types the hospital's own number).
- `backend/app/seed_patient_login.py` – numbers for every patient without one; Ravi (patient 1) = `DGH-000001`, demo PIN only in DEMO_MODE. Hooked into `seed.py` right after `st.insert("patients", patients)` (one guarded try/except).
- `main.py`: `/api/me/login` and `/api/me/login-demo` added to `PUBLIC_PATHS` (done).
- `store.py` / `supabase/schema_v2.sql`: `pin_hash`, `pin_failed`, `pin_locked_until` + a partial unique index on `(coalesce(hospital_id,0), lower(mrn)) where mrn is not null`, wrapped so a duplicate cannot abort the paste. The founder already pasted this block (STATE, 01:41).
- Pages: `web/patient-login.html` (+ `js/patient-login.js`, `css/patient-login.css`; English, Hindi, Tamil, Malayalam; demo box filled by the server), staff card on `web/patient.html` (`js/patient-login-card.js`), link on `web/login.html`.
- Tests: `tests/test_patient_login.py` (24 tests, includes the "columns missing" case and the demo-mode-only PIN).

## Edits for files I must not touch (please apply)
1. **`backend/app/features.py`** – key `auth.patient_regno` already exists as `in_development`. Flip it to `live` once the live site shows the flow working (make a PIN on Ravi's page, log in at `/patient-login.html`). It works locally (browser-checked with real clicks) and on the SQLite store. On Supabase it works only because the founder pasted the columns.
2. **`web/index.html`** (landing hero) – add one link under the hero buttons: `<a href="/patient-login.html">Patient? Log in with your hospital number</a>`.
3. **`web/app.html`** – two things.
   a. When there is no `?id` and no `?t` and no patient session, show a link to `/patient-login.html` (see the `errOpen`-style message in `meds-core.js`).
   b. **Important:** `app.html` takes its patient from `?id=` (else `localStorage.sb_app_pid`, else 1) and does not read the session cookie. So a patient who logs in as patient 3 lands on `/app.html?id=3` (the login page adds the id). Better fix for later: when there is no `id`/`t`, call `GET /api/auth/me` and use `patient_id` from it, then the login page can drop `?id=`.
4. **`web/meds.html`** – with no session and no `id`/`t`, the "open this page from your app" message should also link to `/patient-login.html`. (`meds.html` reads the session cookie, so it works right after a login with no id.)
5. **Newly created patients** – there is no "create patient" route in the code yet. When one is added (routes_patients), call this right after the insert so the patient gets a number (or saves the staff-typed one):
   ```python
   from . import patient_login
   patient_login.ensure_regno(service.store(), new_row)   # new_row has id and hospital_id; returns e.g. DGH-000008
   ```
6. **Old databases (optional)** – patients that already exist on the live Supabase have no number until the demo is reset. `GET /api/me/login-demo` (DEMO_MODE) makes Ravi's number and PIN on first call, and any staff "Make a new PIN" makes a number for that patient. To number everyone at start-up, add to the `lifespan` in `main.py`, next to the other seed hooks: `from . import seed_patient_login; seed_patient_login.ensure(st)` inside try/except.

## Feature keys to flip
- `auth.patient_regno` → `live` after the live check (see 1).

## Founder, by hand
1. After the push and deploy: log in as Doctor → `/demo.html` → "Reset demo data". That gives every patient a number and Ravi his demo PIN. (Or just open `/patient-login.html` once: the demo box makes Ravi's number and PIN.)
2. Tamil and Malayalam words on `/patient-login.html` need a check by a native speaker before real use (same note as the medicines page).
3. If the demo patient's PIN is changed on his staff page, the demo box stops showing the PIN (it shows the number and says the PIN was changed) until the next reset.

## Behaviour worth knowing
- Wrong number or wrong PIN: the same plain message, `401`. 5 wrong PINs in a row lock that patient for 15 minutes (`429`, a different message); a right PIN does not get in while locked. A new PIN clears the lock. One IP address may fail 20 times per 15 minutes.
- The number match ignores case and spaces; `dgh000001` finds `DGH-000001`.
- Audit rows: `auth.patient_login` (success and failure, no PIN), `patient.pin_create`, `patient.regno_set`. The PIN is never in the audit detail, the logs or the database (argon2 hash only), and the staff answer for the card (`GET .../login`) never contains it.
- Until the PIN columns exist on Supabase every route answers `503` "This login is not set up yet - please ask the hospital." and the seed saves numbers but skips the PIN; nothing else changes.
- The slip (print) shows hospital, patient, number, PIN and a QR to `/patient-login.html` (no number or PIN in the address). The wording says what the PIN does; it does not call anything secure or safe.
