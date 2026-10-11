# Auth agent – integration notes (P1-1.3)

Written by the **auth** builder. Short notes for the lead and for builders whose files I don't own.

## What every builder can rely on

- `from . import authz, audit` – signatures are exactly REBUILD_PLAN §3.3 and §3.5.
- The middleware (`main.py`) already gives every `/api/` route: login needed (401), the `X-SB` header on writes (403), and **404 for any path parameter in `authz.RESOURCE_PARAMS` that the caller can't see**. So name path parameters from that table (`pid`, `rx`, `item`, `dose`, `appt`, `doc`, `note_id`, `aid`, `rid`, `cid`, `gid`, `staff_id`, `doctor_id`, `key_id`, `device_id`).
- Handlers still call `authz.require(action, pid)` for the **action** (the middleware only checks "may see"). `require` returns the actor to pass to `audit.write(..., actor=actor, request=request)`.
- A patient id that arrives in the **body** is not checked by the middleware – call `authz.require(...)` yourself.
- Lists: filter with `authz.visible_patient_ids(authz.current_actor())`. `service.visible_ids()` returns that set, or `None` when nobody is logged in (ticker, seed, public page) – then don't filter.
- Hashing: `authz.hash_token(x)` for session tokens, patient link tokens and nurse keys; `authz.hash_join_code(code)` for join codes (ignores case, spaces, dashes). **B1 (`routes_admin`) must use `hash_join_code` when it regenerates a join code**, or signup won't find it.
- Hospital settings: `authz.hospital_settings(hospital_id)` (defaults merged). Stored in `hospitals.settings`.
- Extra helpers (additive): `authz.nurse_permissions(actor, pid=None)`, `authz.alerts_allowed(row)`, `authz.v2_ok(st)`, `authz.ident()` (the store that holds logins and the audit log – use it for `staff`, `hospitals`, `access_keys`, `key_grants`, `auth_sessions`, `audit_events`), `ratelimit.peek()` and `ratelimit.reset()`.
- `comms.use` for nurses needs `acknowledge_alerts` **or** `update_care_plan` (the spec has no row for it – my decision; change in `authz._NURSE` if the lead disagrees).

## Tests

- `client` = demo admin. New fixtures in `tests/conftest.py`: `anon`, `login_as(email)`, `patient_client(pid)`, `riverside_patient`.
- Demo accounts and passwords: `backend/app/seed_auth.py` (`STAFF`, `DEMO_PASSWORDS`, `DEMO_NURSE_KEY`, `DEMO_JOIN_CODE`).
- **Riverside patient 100 is switched off in the test run by default** (`seed_auth.SEED_RIVERSIDE_PATIENT = False` in the `client` fixture), because two old tests count exactly 7 rows in `patients`. Use the `riverside_patient` fixture in a test that needs patient 100. On the real site it is seeded.
- Any `TestClient` a test builds itself starts as the demo admin (conftest patches it). For a logged-out client use `anon`.

## For the isolation agent (`routes_comms.py`, `routes_voice.py` – not my files)

1. **List routes still return every hospital's rows:** `GET /api/comms/alerts`, `/alerts/counts`, `/escalations`, `/events`, `/calls`. Filter them with `service.visible_ids()`.
2. **Body patient ids:** `POST /api/comms/guardians` and `POST /api/comms/wa/reply` take `patient_id` in the body – add `authz.require("comms.use", pid)` (or `patient.view`).
3. **Write actions are not checked yet in comms:** a view-only nurse can still `PUT /api/comms/care/{pid}`, start a ladder or call a patient for a patient **inside her scope**. Suggested: `authz.require("alerts.ack", pid)` on `POST /alerts/{aid}/{action}`; `authz.require("careplan.edit", pid)` on `PUT /care/{pid}` and the guardian writes; `authz.require("comms.use", pid)` on the other writes.
4. `POST /api/comms/tick` and `GET /api/comms/status`, `/demo/sarvam-samples` have no patient id: any staff member can call them (tick runs the ladder for every hospital).
5. `POST /api/voice/stt` takes `patient_id` as a form field – not checked by the middleware.
6. Alerts or calls with **no patient** (`patient_id` null, e.g. a message from an unknown number) are shown only to staff of hospital 1 (`authz.LEGACY_HOSPITAL_ID`).

## For B6 (patient app) and the kit

- The old patient pages call staff-only routes (for example `GET /api/comms/patient/{pid}`, `/api/patients/{pid}/sessions`, `/api/comms/trend/{pid}`). With only a patient cookie these answer **401**. The patient-allowed list is REBUILD_PLAN §3.4 item 3; everything else for the patient app must live under `/api/me/*`. Tell the lead if a path must be added to `PATIENT_PREFIXES` in `main.py`.
- When a browser has both cookies (doctor tab + patient app), the staff session wins everywhere except `/api/me/*`. On the patient-allowed routes the patient cookie is used when the staff login can't see that patient.

## For B7 (`routes_public.py`)

- `/api/impact` calls `service.list_patients()`. That list is now filtered by who is logged in, so a logged-in nurse would get smaller impact numbers than a logged-out visitor. Read the store directly (or wrap the call so no actor is set) if the public numbers must not depend on the viewer.

## For B8 (twin) and anyone who embeds a page

- `X-Frame-Options` is `DENY` everywhere **except** `/twin.html` and `/showcase/` (`SAMEORIGIN`), because the landing page and `demo.html` show them inside a frame. Add a path to `FRAMEABLE_PREFIXES` in `main.py` if another page must be framed.
- `/api/live/{pid}`: POST is open to the patient (own id) or staff; GET needs staff. `/api/twin/sim*` is public.

## For the lead

- `main.py` now skips a router module that **fails to import** (logs an error, lists it in `main.SKIPPED_MODULES`) instead of crashing the whole site. `tests/test_auth.py` fails if that list is not empty.
- FastAPI 0.143 no longer copies included routes into `app.routes`. The path-parameter check opens the nested routers itself (`main.api_route_table()`); a test guards it. Re-check this if FastAPI is upgraded.
- The strict-xfail test `test_open_nurse_api_needs_a_login_before_real_patients` (tests/test_critical.py) is **solved** by this step (an anonymous client gets 401 – covered in tests/test_auth.py), but it still shows as xfailed because its `raw` client is now logged in as the admin. To move it to passing, make it use the `anon` fixture and drop the xfail mark.
- Demo reset keeps hospitals, the six seeded staff and their sessions; it removes staff made during the demo and re-seeds keys 1–5, the demo passwords, join codes and hospital settings.
