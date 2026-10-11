# SpiroBuddy 2.0 – rebuild plan (Phase 0 output)

Written Sun 11 Oct 2026, 16:30 IST, by the lead session. The spec is `docs/private/ULTRACODE_BUILD_PROMPT.md` (local only). Progress lives in `docs/rebuild/STATE.md`. HTTP contracts E–K are in `docs/ARCHITECTURE.md` §14–§20. **This file adds the internal (Python and JS) contracts that let the builders work in parallel.** Don't change a signature here without updating this file and noting it in `docs/PROGRESS.md`.

---

## 1. Decisions made in Phase 0

| Topic | Decision |
|---|---|
| Gemini model | `gemini-3.8-flash` (Google's models page, checked 11 Oct 2026: the newest **stable** Flash; it takes image and PDF input and supports structured output). Env var `GEMINI_MODEL`, default `gemini-3.8-flash`. |
| Gemini SDK | `google-genai==2.29.0` (`from google import genai`). Call `client.models.generate_content(model=…, contents=[types.Part.from_bytes(data=…, mime_type=…), PROMPT], config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=<Pydantic model>, thinking_config=types.ThinkingConfig(thinking_level="low"), http_options=types.HttpOptions(timeout=GEMINI_TIMEOUT_S*1000)))`. Check the exact names against the installed SDK by introspection; never call the network in tests. |
| Temperature | The spec says 0. Google's Gemini 3 guide **strongly recommends keeping the default 1.0** (lower values may loop or degrade). We **leave temperature unset** (the default). Safety does not depend on it: code normalises and a human approves every line. Logged in PROGRESS. |
| Password hashing | `argon2-cffi==25.1.0`, `argon2.PasswordHasher()` with its defaults. |
| Token hashing | Session tokens, patient app tokens, nurse keys and join codes: `secrets.token_urlsafe(…)`; the database stores `sha256(token).hexdigest()` only. Nurse keys: `token_urlsafe(18)`. Session and patient tokens: `token_urlsafe(32)` (≥ 128 bits). The join code is 8 characters from `ABCDEFGHJKMNPQRSTUVWXYZ23456789`, e.g. `DGH-7K3Q-M9PX` style shown as `XXXX-XXXX`. |
| Cookies | `sb_staff` (staff session) and `sb_patient` (patient session): HttpOnly, `SameSite=Lax`, `Path=/`, `Secure` when the request is https (or `X-Forwarded-Proto: https`). Staff: 12 h. Patient: 30 days. |
| CSRF | Every non-GET/HEAD/OPTIONS request under `/api/` must have the header `X-SB: 1`, **except** webhook paths (`/api/comms/webhooks/*`, `/api/comms/twilio/*`, `/api/comms/exotel/*`). Missing → 403 `{"error":"missing X-SB header"}`. `web/js/api.js` adds it once. |
| Patient sessions | Stored in `auth_sessions` too, with two extra columns (`kind` = `staff`/`patient`, `patient_id`). Additive and logged. |
| Demo reset vs logins | `POST /api/demo/reset` re-seeds the clinical data. Hospitals, the seeded staff and their sessions keep their **fixed ids**, so a logged-in admin or doctor stays logged in. Staff created during the demo (signups, redeemed nurses) and all keys are removed and re-seeded. |
| Identity ids on Supabase | The seed inserts fixed small ids. `schema_v2.sql` makes every new identity start at 1000, and restarts `patients.id` at 1000, so later inserts never collide with seeded ids. |
| Old Contract E | The existing "CONTRACT E – Voice & language" is renamed **CONTRACT D3**. E–K are the new 2.0 contracts. |
| Old `/` dashboard | `/` becomes the landing page (B7). The old triage dashboard moves to `/hospital/patients.html` (B2). B2 takes the old code from git: `git show 4cf4862:web/index.html`. |

## 2. Demo accounts (all fictional; shown on `/login.html` in DEMO_MODE)

| Who | Email | Password | Notes |
|---|---|---|---|
| Admin, Demo General Hospital (fictional) | `admin@demo-general.example` | `demo-admin-2026` | staff id 1, hospital 1 |
| Dr. Meera Nair, surgeon | `meera.nair@demo-general.example` | `demo-doctor-2026` | staff id 2; primary doctor of patients 1, 2, 4, 6 |
| Dr. Kabir Rao, chest physician | `kabir.rao@demo-general.example` | `demo-doctor-2026` | staff id 3; primary doctor of patients 3, 5, 7 |
| Sister Anjali, ward nurse | `anjali@demo-general.example` | `demo-nurse-2026` | staff id 4; key from Dr. Meera, scope = all of Dr. Meera's patients, every permission |
| Nurse Thomas Mathew | `thomas@demo-general.example` | `demo-nurse-2026` | staff id 5; key from Dr. Kabir, scope = patients 3 and 5 only, view + acknowledge alerts |
| Admin, Demo Riverside Clinic (fictional) | `admin@demo-riverside.example` | `demo-riverside-2026` | staff id 50, hospital 2 (isolation tests) |

- Hospital 1 join code in DEMO_MODE: `DEMO-2026` (stored hashed; "regenerate" makes a random one).
- Keys seeded: Anjali's (active, id 1), Thomas's (active, id 2), one revoked (id 3) and one expired (id 4). The plain text of an unused demo key, `DEMO-NURSE-KEY-0001`, is shown on the demo page for the redeem step (key id 5, active, unused, Dr. Meera, patients 1 and 2, view + confirm prescriptions + manage appointments).
- Patients 1–7 = hospital 1. Patient 100, "Kiran Joseph", = hospital 2 (Riverside).

## 3. Internal contracts (Phase 1 provides these; Phase 2 builds on them)

### 3.1 `backend/app/config.py` (new names)
`ALLOW_TRAINING` (0), `SHOW_API_DOCS` (0), `GEMINI_API_KEY`, `GEMINI_MODEL` (`gemini-3.8-flash`), `GEMINI_TIMEOUT_S` (30), `AI_DAILY_LIMIT` (300), `AI_PER_IP_HOUR` (20), `UPLOAD_PER_IP_HOUR` (30), `SUPABASE_BUCKET` (`documents`), `UPLOAD_DIR` = `DATA_DIR / "uploads"`. Read them with the existing `env()` and `env_flag()`.

### 3.2 `backend/app/store.py`
- `TABLES_V2` = every table in spec §9 plus `app_settings`. `TABLES` stays the v1 list.
- SQLite creates every v2 table, and adds the new `patients` columns with `SQLITE_ADD_COLUMNS`.
- JSON columns are added to `JSON_COLS` (`settings, languages, departments, wards, permissions, patient_ids, routine, items, times, unclear_fields, box_2d, output, detail, calibration, health, samples, ai_suggested, value, emergency_contact`). Boolean columns go in `BOOL_COLS` (`join_requires_approval, as_needed, visible_to_patient, visible_to_family, read_aloud, teach_back_ok, ok`). New timestamptz columns go in `TS_COLS`.
- `SupabaseStore` checks the v2 tables **after** the v1 tables. If v1 is fine but any v2 table is missing, `make_store()` returns SQLite with note `"v2 tables missing on Supabase – run supabase/schema_v2.sql; using demo SQLite"`, and `service.v2_missing()` returns True. `/api/health` adds `v2_missing: bool`. The hospital shell shows the red banner "Database update needed – see SETUP_STEPS.md".

### 3.3 `backend/app/authz.py` – the one place for permissions
```python
@dataclass
class Actor:
    kind: str              # "staff" | "patient"
    id: int                # staff id, or patient id for a patient
    role: str              # "admin" | "doctor" | "nurse" | "patient"
    hospital_id: int
    name: str
    email: str | None = None
    patient_id: int | None = None          # patients only
    grants: list[dict] = field(default_factory=list)  # nurses: [{key_id, doctor_id, scope, patient_ids, permissions, expires_at}]

PERMS = ("view", "update_care_plan", "confirm_prescriptions", "manage_appointments",
         "upload_documents", "acknowledge_alerts")          # nurse key permissions

def current_actor() -> Actor | None              # from a contextvar set by the middleware
def resolve_actor(request) -> Actor | None       # cookie -> Actor (checks expiry, revoked, disabled, key revoked/expired)
def visible_patient_ids(actor) -> set[int]       # admin: every patient in the hospital; doctor: primary_doctor_id == me or care_team; nurse: union of live grants; patient: {own}
def patient_permissions(actor, pid) -> set[str]  # actions this actor may do on this patient (see the matrix below)
def can(actor, action: str, pid: int | None = None) -> bool
def require(action: str, pid: int | None = None) -> Actor
    # uses current_actor(); no actor -> 401; pid not visible (or other hospital, or missing) -> 404;
    # visible but not allowed -> 403. Returns the actor.
def require_staff(*roles) -> Actor               # 401 / 403
def hospital_settings(hospital_id) -> dict       # merged with defaults (spec §8.3)
```
**Action names** (use exactly these): `patient.view`, `patient.edit`, `careplan.edit`, `programme.change`, `rx.create`, `rx.approve`, `rx.upload`, `dose.report`, `appt.manage`, `appt.request`, `doc.upload`, `doc.view`, `doc.view_family`, `alerts.ack`, `comms.use`, `keys.create`, `keys.revoke`, `admin.manage`, `governance.read`, `demo.control`, `device.manage`.
- Nurses: `patient.view` needs `view`; `careplan.edit`/`patient.edit` need `update_care_plan`; `rx.approve` needs `confirm_prescriptions` **and** the hospital setting `rx_confirm_by == "doctor_or_permitted_nurse"`; `appt.manage` needs `manage_appointments`; `doc.upload`/`doc.view` need `upload_documents` (viewing is allowed with `view`); `alerts.ack` needs `acknowledge_alerts`; `dose.report` on behalf of a patient is allowed with `view` and is logged.
- Patients: `patient.view`, `dose.report`, `appt.request`, `doc.upload`, `doc.view` (own, visible_to_patient), `rx.upload` – own id only.
- A patient whose programme status is `deceased` or `stopped` gets no reminders. `paused` stops reminders and alerts. Use `authz.reminders_allowed(patient_row) -> bool`.

### 3.4 Middleware policy (in `main.py`, uses `authz`)
1. Resolve the actor once per request and put it in the contextvar.
2. **Public** (no actor needed): `/api/health`, `/api/features`, `/api/impact*`, `/api/twin/sim*`, `/api/auth/login`, `/api/auth/signup`, `/api/auth/redeem`, `/api/auth/me` (returns `{"authenticated": false}` when logged out), `/api/auth/logout`, `/api/me/session`, `/api/voice/status`, `/api/voice/cues`, `/api/voice/clip/*`, `/api/voice/audio/*`, `/api/comms/card/*` (fetched by Twilio as media), `/api/comms/guardian/*` (guardian tokens), webhooks (`/api/comms/webhooks/*`, `/api/comms/twilio/*`, `/api/comms/exotel/*`).
3. **Patient or staff**: `/api/me/*` (patient cookie only), `/api/sessions` (POST; the handler checks the body's patient_id), `/api/classify`, `/api/voice/tts`, `/api/voice/stt`, `/api/voice/translate`, `/api/voice/detect`, `/api/voice/prefs/{pid}`, `/api/voice/summary-audio/{pid}`, `/api/comms/cheers/*`, `/api/comms/demo/red-flag/{pid}` (patient: own id, DEMO_MODE only), `/api/live/{pid}` (POST: patient own id or staff), `GET /api/patients/{pid}` (patient: own id only).
4. **`/api/demo/*` and `/api/comms/demo/*`**: staff admin or doctor **and** DEMO_MODE (except the red-flag rule above).
5. `/api/collect`, `/api/train`: admin **and** `ALLOW_TRAINING=1`, otherwise 403.
6. **Everything else under `/api/`** needs a staff session.
7. **Generic patient-id check** for the old routes: a patient id in a known path position (`/api/patients/{pid}…`, `/api/summary/{pid}`, `/api/whatsapp/{pid}`, `/api/demo/*/{pid}`, `/api/comms/<seg>/{pid}`, `/api/voice/prefs|summary-audio/{pid}`, `/api/live/{pid}`) must be in `visible_patient_ids(actor)`, otherwise **404**. Resource ids are looked up first (`/api/comms/alerts/{id}`, `escalations/{id}`, `calls/{id}`, `guardians/{id}`, `cheers/{id}`) and their `patient_id` is checked the same way. Handlers that take a patient id in the body (`POST /api/sessions`, `POST /api/comms/guardians`, `POST /api/comms/wa/reply`) call `authz.require(...)` themselves.
8. **Lists are filtered** to `visible_patient_ids`: `GET /api/patients`, `/api/messages`, `/api/comms/alerts`, `/alerts/counts`, `/escalations`, `/events`, `/calls`.
9. New routers (Phase 2) always call `authz.require(action, pid)` in each handler. The middleware only guarantees "a staff session or an allowed patient" for them.
10. Security headers on every response: `X-Content-Type-Options: nosniff`, `Referrer-Policy: same-origin`, `X-Frame-Options: DENY`. The API docs are hidden unless `SHOW_API_DOCS=1`.

### 3.5 `backend/app/audit.py`
```python
def write(action: str, resource_type: str, resource_id=None, patient_id=None, detail: dict | None = None,
          actor: Actor | None = None, request=None) -> None   # never raises; actor defaults to current_actor()
def list_events(hospital_id, filters: dict, limit=200) -> list[dict]
```
Action names look like `auth.login`, `auth.login_failed`, `auth.logout`, `patient.view`, `patient.update`, `rx.approve`, `dose.report`, `doc.view`, `key.create`, `key.revoke`. Never put a token, password or document content in `detail`. `hospital_id` goes in `detail` for staff without a patient. P1 adds the hash chain (`prev_hash`, `hash`).

### 3.6 `backend/app/features.py`
`FEATURES: list[dict]` with `key, name, status ("live"|"simulated"|"in_development"|"planned"), where, note`. `get(key) -> dict`, `public_list() -> list`. A router serves `GET /api/features`. `tools/gen_feature_status.py` writes `docs/FEATURE_STATUS.md` from it (P4). **Every badge key used in a page must exist here** (a test checks this: it greps `data-feature="…"` in `web/`).

### 3.7 `backend/app/ai_gemini.py` and `backend/app/ai_register.py`
```python
# ai_gemini.py
RX_PROMPT_V1: str; RX_PROMPT_VERSION = "rx-v1"
DOC_PROMPT_V1: str; DOC_PROMPT_VERSION = "doc-v1"
def gemini_enabled() -> bool                              # key present
def ai_allowed(hospital_id, patient_id, ip) -> tuple[bool, str]   # key, hospital AI setting, patient AI consent, daily + per-IP limits -> (ok, reason)
def extract_prescription(data: bytes, mime: str, *, patient_id, hospital_id, ip, input_ref) -> dict
    # -> {"ok": bool, "reason": str|None, "ai_event_id": int|None, "draft": {...RX output fields...} | None}
def suggest_document(data: bytes, mime: str, *, patient_id, hospital_id, ip, input_ref) -> dict
    # -> {"ok", "reason", "ai_event_id", "suggestion": {"kind","title","doc_date"} | None}   (nothing else is kept)
def summarize_text(prompt: str) -> str | None             # used by llm.py as the 2nd provider
# ai_register.py
def log_event(purpose, provider, model, prompt_version, input_ref, output, latency_ms, ok, error=None, patient_id=None) -> int
def record_review(ai_event_id, reviewer_id, decision, lines_total, lines_edited, lines_removed) -> None
def stats(hospital_id) -> dict   # {drafts, reviewed, lines_total, lines_edited_pct, rejected_pct, by_purpose}
```
No key, error, timeout, limit hit or no consent → `{"ok": False, "reason": …}` and the caller uses the manual path. Tests mock `ai_gemini._call_model`.

### 3.8 `backend/app/storage.py`
```python
def save(data: bytes, mime: str, *, prefix: str) -> str     # returns a random storage path; Supabase bucket "documents" if configured, else UPLOAD_DIR
def load(path: str) -> bytes
def delete(path: str) -> None
def validate_upload(data: bytes, filename: str, declared_mime: str | None) -> tuple[str, bytes, bytes | None]
    # -> (mime, cleaned_bytes, thumbnail_png_or_None); raises ValueError(reason) on a bad file.
    # jpg/png/webp/pdf only, max 10 MB, magic bytes checked, images re-encoded (strips EXIF), SVG/HTML refused even if renamed.
def ensure_bucket() -> None   # called at start-up; never raises
```

### 3.9 `backend/app/ratelimit.py`
`allow(bucket: str, key: str, limit: int, per_seconds: int) -> bool`, in memory. Buckets: `login` (10 per 15 min per IP+email, then a 15-minute lockout via `staff.locked_until`), `ai`, `upload` (30/h/IP), `live` (frames).

### 3.10 Front-end kit (Phase 1)
- `web/js/api.js`: adds `X-SB: 1` to every non-GET call. `SB.api.upload(path, formData)` for multipart. `SB.auth.me()` (cached) and `SB.auth.logout()`. On a 401 in a hospital page → redirect to `/login.html?next=<path>`.
- `web/js/ui.js`: `SB.ui.boot(pageKey)` becomes role-aware for `/hospital/*` pages (nav per §3.11, the user's name and role, Logout, the dashed "Fake patients only" ribbon in DEMO_MODE, and the red "Database update needed" banner when `v2_missing`). `SB.ui.esc(s)` escapes **every** user string. `SB.ui.badge(featureKey)` returns the status badge from `/api/features` (cached once per page). `SB.ui.plannedCard(featureKey)` returns a disabled card with a "Planned" badge and the one-line note.
- `web/css/styles.css`: one new section "8 – 2.0 additions" (status badges `.fbadge.live/.simulated/.in_development/.planned`, `.planned-card`, `.ribbon-fake`, `.banner.db`, `.amber-field`, form and inline-edit pieces). After Phase 1, only the lead edits `styles.css`. Builders put page-only styles in their own `web/css/<area>.css` (e.g. `chart.css`, `public.css`, `patient-app.css`, `twin.css`) using the same tokens.

### 3.11 Hospital navigation (keys for `SB.ui.boot`)
`home` (/hospital/), `patients`, `review`, `appointments`, `availability`, `keys`, `staff` (admin), `devices`, `settings` (admin), `governance`, `demo` (admin/doctor + DEMO_MODE). Nurses see home, patients, review (only with the confirm permission), appointments (only with the manage permission), devices.

### 3.12 Service functions that builders share (so B2 and B6 don't wait)
Each owner exposes these in their module. A caller wraps the import in `try/except ImportError` and shows an empty state if it isn't there yet.
- B3 `backend/app/meds/service.py`: `medicines_for(pid) -> dict` (active, as_needed, history), `doses_for(pid, date_from, date_to) -> list`, `today_doses(pid) -> list`, `report_dose(dose_id, actor, channel) -> dict`, `snooze_dose(dose_id, minutes=10)`, `make_due_now(pid) -> dict`, `mark_missed(dose_id) -> dict`, `tick(now)` (called by the comms ticker), `counts_today(pid) -> {"reported": n, "due": n, "missed": n}`.
- B4 `backend/app/appointments.py`: `next_for(pid) -> dict | None`, `list_for(pid) -> list`, `free_slots(doctor_id, date) -> list`, `request(pid, doctor_id, start_at, by_role) -> dict`.
- B5 `backend/app/documents.py`: `list_for(pid, audience: "staff"|"patient"|"family") -> list`, `create(pid, data, filename, mime, kind, title, by_actor, visible_to_patient, visible_to_family) -> dict`.
- B8 `backend/app/routes_twin.py`: `live_push(pid, frames)`, `live_after(pid, after_ms) -> dict`, `store_curve(session_id, pid, samples)`.
- The patient chart timeline (B2) reads `audit_events` + sessions + dose_events + appointments + documents directly via the store.

## 4. Phase 1 split (foundations)

| Stage | Agent | Owns (only these files) |
|---|---|---|
| 1A | **data** | `backend/app/config.py`, `backend/app/store.py`, `backend/app/service.py` (only `v2_missing` and `store_note`), `supabase/schema_v2.sql`, `.env.example`, `render.yaml`, `backend/requirements.txt`, `tests/test_store_v2.py` |
| 1A | **platform** | `backend/app/features.py`, `backend/app/audit.py`, `backend/app/ai_gemini.py`, `backend/app/ai_register.py`, `backend/app/storage.py`, `backend/app/ratelimit.py`, `backend/app/llm.py` (Gemini provider), `tests/test_platform.py` |
| 1A | **samples** | `tools/demo/make_samples.py`, `web/samples/*` |
| 1B | **auth** | `backend/app/authz.py`, `backend/app/routes_auth.py` (auth, keys, `/api/me/session`), `backend/app/seed_auth.py`, `backend/app/main.py`, `backend/app/routes_comms.py` + `backend/app/routes_voice.py` (scoping only), `backend/app/seed.py` (hooks only), `tests/conftest.py`, `tests/test_auth.py`, `tests/test_isolation.py` |
| 1B | **kit** | `web/js/api.js`, `web/js/ui.js`, `web/css/styles.css`, `web/app.html` (only the `?id=` → `/api/me/session` shim), `web/login.html` (a minimal working page; B1 polishes it) |
| 1B | **seed2** | `backend/app/seed_v2.py`, `tests/test_seed_v2.py` |
| 1C | verify ×2 | read-only, then the lead fixes |

## 5. Phase 2 file ownership (builders own disjoint files)

| Builder | Owns | Builds |
|---|---|---|
| B1 Hospital shell and admin | `web/hospital/{index,staff,settings,keys,governance,demo}.html`, `web/js/hospital-*.js`, `web/login.html`, `web/signup.html`, `web/redeem.html`, `web/css/hospital.css`, `backend/app/routes_admin.py` (`/api/admin/*`, `/api/ai-events*`, governance), `tests/test_admin.py` | §8.2–8.3, key UI, governance, demo controls page |
| B2 Chart and review UI | `web/hospital/{patients,patient,review}.html`, `web/js/chart-*.js`, `web/css/chart.css`, `backend/app/routes_patients.py` (Contract G new routes; the old patient routes in `main.py` are removed by the lead), `tests/test_patients_v2.py` | §8.4–8.6, the review screen in §8.7 |
| B3 Medicines backend | `backend/app/meds/*`, `backend/app/routes_meds.py` (Contract H + `/api/me/doses/*`, `/api/me/prescriptions`), `tests/test_meds.py`, `tests/test_normalise.py` | §8.7 normaliser and pipeline, §8.8 doses, `missed_dose` alerts |
| B4 Appointments | `backend/app/appointments.py`, `backend/app/routes_appointments.py` (Contract I + `/api/me/appointments`), `web/hospital/{appointments,availability}.html`, `web/js/appt-*.js`, `tests/test_appointments.py` | §8.9 |
| B5 Documents | `backend/app/documents.py`, `backend/app/routes_documents.py` (Contract J + `/api/me/documents`), `web/js/docs-vault.js`, `web/css/docs.css`, `tests/test_documents.py` | §8.10 |
| B6 Patient app and family | `web/app.html`, `web/js/patient-*.js`, `web/css/patient-app.css`, `web/guardian.html`, `backend/app/routes_me.py` (`/api/me`, `/api/me/today`), `tests/test_me.py` | §8.12, §8.13 |
| B7 Public site | `web/index.html`, `web/impact.html`, `web/trust.html`, `web/vision.html`, `web/architecture.html`, `web/data/*.json`, `web/css/public.css`, `web/js/public-*.js`, `backend/app/routes_public.py` (`/api/impact`), `docs/hackathon/architecture_v2.svg`, `tests/test_public.py` | §8.1 |
| B8 Digital twin and devices | `web/js/twin-model.js`, `web/twin.html`, `web/hospital/{twin,devices}.html`, `web/showcase/*`, `web/css/twin.css`, `backend/app/routes_twin.py` (`/api/live`, `/api/twin/sim`), `backend/app/routes_devices.py`, `tests/test_twin.py` | §8.14 |
| X1 Consent v2 | `backend/app/consent_v2.py`, `backend/app/routes_consent.py`, `tests/test_consent_v2.py` | §8.15 itemised consent |

- **Shared files edited only by the lead** between stages: `main.py` router registration (Phase 1 pre-registers every router name above, so a missing module is simply skipped), `styles.css`, `api.js`, `ui.js`, `DESIGN_SYSTEM.md`, `seed.py`, `seed_v2.py` after Phase 1, `features.py` after Phase 1. Builders write what they need in those files to `docs/rebuild/<builder>_integration.md`.
- Old addresses (redirect pages `/patient.html`, `/demo.html`, `/units.html`) belong to B1 (demo), B2 (patient) and B8 (units).

## 6. Risks and what we do about them

| Risk | Plan |
|---|---|
| Auth breaks the 420 old tests | conftest logs in as the demo admin and sends `X-SB: 1` by default. Demo reset keeps staff sessions. The auth agent runs the whole suite before finishing. |
| Scoping misses an old route (data leak across hospitals) | Generic path check in the middleware, plus `test_isolation.py`, which walks **every** route in `app.routes` as Riverside with Demo General ids and expects 404. |
| Supabase without the v2 tables | Automatic SQLite fallback + red banner (§3.2). The live site keeps working before the founder pastes the SQL. |
| Parallel builders collide | Disjoint ownership (§5), integration notes, worktrees only where needed. |
| Usage limit mid-build | STATE.md after every step; `wip/` branches; at most one step lost. |
| Gemini changes or no key | Every path has the manual fallback; tests mock the model. |
| Time | Drop P2, then P1. Never ship a half-working P0 screen: hide it behind a Planned card. |

## 7. Priority list

- **P0:** Phase 1 completely; B1a–c, B1d basic (consents overview + AI register); B2a–c; B3a–c; B4a; B4b in-app; B5a; B6a; B7a–d; B8a–b; X1; Phase 3; Phase 4.
- **P1:** B1d full (audit viewer, pilot checklist); B3d; B4b simulators; B6b; B6c; B8c fleet twin; X2 planned cards; X3 FHIR + discharge plan; X4 CSP + hash chain + multilingual filter; X5 nightly reset; teach-back.
- **P2:** X6 data-rights requests, hospital self-registration (Planned cards otherwise).
