# Architecture & interface contracts

## 1. Overview
```
[Sensor: VL53L0X/VL53L1X] -> [ESP32 or Arduino] --USB serial--> [Chrome: web/collect.html]
                                                     (or Simulator)
Nurse & doctor website (web/)  -- REST /api/* (poll every 2 s) -->  backend (FastAPI)
                                                                    |-- data store: DEMO (SQLite, auto-seeded) or SUPABASE (Postgres)
                                                                    |-- ML model (ml/), Claude summary, Twilio WhatsApp
3D showroom (web/showcase/) – standalone Three.js page + pre-rendered MP4 videos
Patient mobile app – OUT OF SCOPE for now (the user builds it separately; it will call the same /api)
```
- **Everything runs in DEMO mode for now:** fake patients, no login, a "DEMO" badge, demo control buttons.
- The backend serves `web/` as static files at `/`. The browser only ever talks to our FastAPI. Supabase keys stay on the server.
- **Local:** `scripts\run.ps1` → http://localhost:8000. **Hosted:** Render web service from `render.yaml` (see §11).

## 2. Folder layout
```
SpiroBuddy/
  CLAUDE.md  START_PROMPT.md  .env.example  render.yaml
  scripts/run.ps1  scripts/setup.ps1
  docs/        REQUIREMENTS, ARCHITECTURE, ROLES, HANDOFF, PROGRESS, HARDWARE, 3D_SOURCES, DEPLOY, plans/
  firmware/spirobuddy_serial/spirobuddy_serial.ino
  supabase/schema.sql  supabase/seed.sql       Postgres tables (§10) + demo rows
  backend/
    __init__.py  requirements.txt
    app/__init__.py
    app/main.py         FastAPI app, static mount of web/, routers
    app/store.py        Store interface + SqliteStore (demo) + SupabaseStore, chosen by DATA_BACKEND
    app/models_ml.py    load model via ml/predict.py, classify(features), rules fallback
    app/llm.py          Claude summary + template fallback
    app/whatsapp.py     Twilio send + dry-run fallback
    app/rules.py        status colours, missed-slot logic, score
    app/seed.py         fake patients (used by both stores)
    data/               spirobuddy.db (git-ignored), breaths_labelled.csv
  ml/
    features.py  synth.py  train.py  predict.py  model.joblib  metrics.json
  web/                  NURSE & DOCTOR WEBSITE (plain HTML/CSS/JS, no build step)
    index.html          dashboard: patient list, colour status, live updates
    patient.html        patient detail: today's slots, 7-day chart, sessions, AI summary, target, WhatsApp
    demo.html           demo control panel: simulate sessions, miss slots, reset, message log
    collect.html        labelled-breath recorder for ML (Simulator + Web Serial)
    css/styles.css
    js/api.js  js/breath.js  js/sources.js  js/charts.js ...
    showcase/           3D SHOWROOM (owned by the 3D agent)
      index.html  showcase.js  videos/*.mp4
  tools/render/         headless video renderer for the showroom (3D agent)
  hardware/3d/          exported 3D model files (.glb/.stl) (3D agent)
```

## 3. CONTRACT A – serial line protocol (firmware → browser)
115200 baud, one line per reading, about 30 per second:
```
D,<millis>,<distance_mm>
```
Optional status lines: `S,<text>` (e.g. `S,READY,VL53L1X`). Errors: `E,<text>`. Anything else is ignored.
The browser can send `B\n` to make the device beep (optional; ignored if there's no buzzer).
The firmware also prints `S,BOOT,<board>` at start-up and re-sends the `S,READY,...` line when it receives `I\n` (the XIAO doesn't reset when the port opens). Invalid readings (or > 2000 mm) are skipped, so the stream can have short gaps.

## 4. CONTRACT B – sample stream inside the browser
Every source emits `{t: ms, raw: number}` (mm for serial, mL for the simulator, which uses identity calibration).
Calibration maps raw → mL via linear interpolation over sorted points `[{raw, ml}]`. Distance shrinks as the disc rises, so the mapping may be decreasing. Values are clamped to 0–max.
Smoothing: median of the last 5 values.

## 5. CONTRACT C – breath state machine and features
States: `IDLE → INHALING → HOLDING → FALLING → IDLE`
- IDLE→INHALING: vol > 150 mL and rising
- INHALING→HOLDING: |slope| < 150 mL/s for ≥ 0.3 s
- INHALING/HOLDING→FALLING: vol < 0.9 × peak
- FALLING→IDLE: vol < 100 mL → emit the breath. Ignore it if duration < 0.5 s or peak < 250 mL. Reset if a state lasts > 20 s.
- Live warning: during INHALING, if the 0.3 s rise rate > `FAST_RATE` (default 1200 mL/s) → event `too_fast_live`.

**Breath features object** (the same names in JS, Python, CSV and the database):
```json
{
  "peak_ml": 1800, "pct_target": 0.9, "time_to_peak_s": 3.1,
  "mean_rise_ml_s": 580, "max_rise_ml_s": 900, "hold_s": 3.2,
  "smoothness": 0.12, "duration_s": 8.4
}
```
- `smoothness` = standard deviation of the first difference of the rising segment ÷ its mean (lower = smoother).
- `hold_s` = time with vol ≥ 0.9 × peak (for each point ≥ 0.9 × peak, add the gap to the next point — as ml/features.py does).
- Breath start = first point ≥ 10 % of peak; the rising segment runs from there to the peak; `duration_s` = start → last point ≥ 10 % of peak.
- `max_rise_ml_s` = fastest rise over any 0.3 s window of the rising segment (if the rise lasts < 0.3 s, use its average rate).
- Times are in seconds (ml/features.py converts ms automatically). Real `smoothness` values are about 0.3–1.0 at 30 Hz; it isn't used by the rules or the score.

**Score** (0–10, one decimal):
- depth = 4 × min(peak / target, 1)
- speed = 3 if max_rise ≤ 900, 1 if ≤ 1400, else 0
- hold = 3 × min(hold_s / hold_target, 1)

**Labels:** `good`, `too_fast`, `too_shallow`, `no_hold`.

**Rule fallback:**
1. `too_fast` if max_rise > 1400
2. else `too_shallow` if pct_target < 0.5
3. else `no_hold` if hold_s < 1.0
4. else `good`

## 6. CONTRACT D – REST API (all JSON, prefix /api)
| Method & path | Body / query | Returns |
|---|---|---|
| GET /api/health | – | `{ok, model_loaded, llm_enabled, whatsapp_enabled, data_backend:"demo"\|"supabase", demo_mode:bool}` |
| GET /api/patients | – | list of `{id, name, age, sex, surgery, surgery_date, language, target_ml, status, done_today, due_today, best_today, personal_best_ml, trend, last_session_at, red_flag_open}` (`red_flag_open` = an unresolved red-flag alert exists; added Q-06) |
| GET /api/patients/{id} | – | patient + `today` (list of `{hour, status:"done"\|"missed"\|"pending"\|"upcoming", session_id?}`) + `history` (7 days: `{date, best_ml, sessions_done, avg_score}`) |
| PUT /api/patients/{id} | `{target_ml?, hold_target_s?, language?, family_phone?}` | patient |
| GET /api/patients/{id}/sessions | `?limit=20` | list of `{id, started_at, slot_hour, breaths_count, best_ml, avg_score, label_counts:{good,too_fast,too_shallow,no_hold}}` |
| POST /api/classify | features object | `{label, proba:{...}, source:"model"\|"rules"}` |
| POST /api/sessions | `{patient_id, started_at, breaths:[{t, features, label, score}]}` | `{session_id, slot_hour, slot_status}` |
| POST /api/collect | `{person, label, samples:[{t,ml}], features}` | `{ok, count_by_label}` |
| POST /api/train | – | runs ml/train.py and reloads the model → metrics |
| GET /api/model | – | metrics.json |
| POST /api/summary/{id} | `{language?}` | `{text, source:"llm"\|"template"}` |
| POST /api/whatsapp/{id} | `{kind:"summary"\|"missed", to?:"family"\|"nurse"}` | `{sent:bool, dry_run:bool, text, to_role}`; when consent blocks it also `blocked:true, blocked_reason, error` (sent=false, dry_run=false). Goes through `comms.messages.send_care_update` (consent/STOP, AI disclosure, footer, throttle; Q-01). `family` = primary guardian in their language (Malayalam falls back to English) |
| GET /api/messages | `?limit=50` | recent message log `{id, patient_id, patient_name, kind, to_role, text, sent, dry_run, created_at}` |
| POST /api/demo/simulate/{id} | `{quality?:"good"\|"mixed"\|"poor", breaths?:10}` | server makes a realistic session with ml/synth, classifies and stores it → same as POST /api/sessions + `breaths` |
| POST /api/demo/miss/{id} | – | marks the last 2 slots missed and triggers the missed alert |
| POST /api/demo/reset | – | wipes and re-seeds the demo data → `{ok, patients}` |

`/api/demo/*` only works when `DEMO_MODE=1` (the default for now). Patient id 1 = "Ravi Kumar", the live demo patient.

**Status rules** (rules.py):
- red: 2+ consecutive missed slots up to now, or done/due < 0.4
- yellow: done/due < 0.7, or best today < 0.8 × personal best
- green: otherwise
- override: an unresolved red-flag alert (open, acknowledged or snoozed) always makes the status red, with reason "Open red-flag alert" first (`service.red_flag_patient_ids`)
- `due` = slots from 8:00 up to the current hour (max 14). Times use `TZ_NAME` (default `Asia/Kolkata`).

### D2 – comms (`backend/app/routes_comms.py`, prefix `/api/comms`; plain-English guide: `docs/COMMS.md`)
Everything works with no keys (dry run + browser simulators). Code: `backend/app/comms/` (common, guardians, alerts, messages, calls, sarvam, consent, escalation, trend, cards, script, audio, progress, seed_comms). Browser: `web/js/comms.js` (`SB.comms.api.*`), `comms-dashboard.js`, `comms-patient.js`, `phone-sim.js`, `web/guardian.html`.

| Method & path | Body / query | Returns / does |
|---|---|---|
| GET /status | – | providers (`calls_provider`, `checkin_provider`: twilio\|exotel\|sarvam_agent\|dry_run), `sarvam_agent_ready`, `sarvam_agent_missing`, WhatsApp state + `whatsapp_hint` (sandbox rejoin) + `whatsapp_last`, quiet hours, ticker |
| POST /tick | – | runs one ladder pass now |
| GET /alerts | `?status=active\|open\|acknowledged\|snoozed\|resolved\|all&patient_id&limit` | alerts `{id, patient_id, patient_name, kind, kind_label, severity red\|amber\|info, title, detail, status, assigned_to, snooze_until, run_id, created_at}`; kinds: missed, red_flag, no_answer, low_trend, callback, help, question, call_review |
| GET /alerts/counts | `?me=` | `{open, red, amber, acknowledged, snoozed, mine, by_patient}` |
| POST /alerts/{id}/{action} | action = ack\|snooze\|assign\|resolve\|reopen; `{by, minutes?, to?}` | alert |
| GET /escalations | `?patient_id&active&limit` | ladder runs `{id, status, speed, steps:[{key,label,state}], outcome, seconds_to_next, held_until, red_flag,…}` |
| POST /escalations/start/{pid} | `{speed: real\|fast, reason?, override_quiet?}` | run |
| POST /escalations/{id}/stop · /advance | `{by?}` | run (advance = run the next step now) |
| POST /demo/ladder/{pid} | `{override_quiet?}` | demo fast-forward run (≈60 s) |
| POST /demo/red-flag/{pid} · /demo/trend/{pid} | `{text?}` | red-flag flow / trend check |
| GET /timeline/{pid} · GET /events | `?limit` · `?since_id&limit&patient_id` | timeline events `{id, kind, icon, title, detail, status, channel, actor, run_id, created_at}` |
| GET /calls · GET /calls/{id} | `?active&patient_id&limit` | calls `{id, to_role, purpose: reminder\|checkin\|guardian\|guardian_red_flag\|nurse_bridge, provider, style: ivr\|agent, status, script, answers[], result:{pending, label, outcome, neutral_note, patient_words, red_flag, callback_requested, possible_distress, transcript_reference}\|null, simulated}` |
| POST /calls/{id}/answer · /hangup | `{reason?: hangup\|declined}` | call (simulator) |
| POST /calls/{id}/press | `{digit: 1\|2\|3}` | `{say, end, dial, call}` – keypad (IVR) calls only |
| POST /calls/{id}/agent-turn | `{text, source: voice\|tap}` | `{say, end, stage, answers, result?, call}` – simulated AI conversation |
| POST /checkin-call/{pid} | `{missed?}` | AI check-in call (Sarvam Voice Agent, else simulator); **409** without consent |
| POST /webhooks/sarvam | `?token=SARVAM_WEBHOOK_SECRET`; Sarvam Instant Outbound payload | `{ok, duplicate, call_id, result}` (normalised: `{provider, status, outcome: ok\|needs_nurse_review\|red_flag\|unclear\|no_answer\|failed, reason_category, patient_words, neutral_note, red_flag, callback_requested, transcript_reference, possible_distress}`); 403 bad token, 404 unknown attempt; idempotent |
| GET /demo/sarvam-samples · POST /demo/sarvam-replay/{pid} | `{sample: pain\|red_flag\|fine\|no_answer}` | saved webhook payloads (`comms/samples/sarvam_webhooks.json`) fed through the real handler |
| POST /call-patient/{pid} | `{nurse_name, nurse_phone?}` | nurse click-to-call (nurse rings first) |
| POST /call-script/{pid} | – | `{text, source: llm\|template, facts}` |
| GET+POST /twilio/voice/{cid} · POST /twilio/gather/{cid} · /twilio/status/{cid} | Twilio form | TwiML |
| GET /exotel/greeting · /exotel/gather · /exotel/passthru · POST /exotel/status/{cid} | Exotel applet query (`CustomField` = call id) | text / JSON |
| POST /webhooks/whatsapp · /webhooks/whatsapp/status | Twilio form (From, Body, ButtonPayload) | `<Response/>`; keywords 1/2/3, done, status/स्थिति, help (red flag), STOP/रोको/நிறுத்து |
| GET /wa/thread/{pid} | `?role=patient\|guardian&guardian_id` | simulator chat `{items:[{dir, kind, text, buttons, image?, audio?}]}` |
| POST /wa/reply | `{patient_id, role, text?, payload?, guardian_id?}` | `{intent, reply}` (same logic as the webhook) |
| GET /card/{pid}.png · POST /weekly-card/{pid} | `?lang` · `{to, language?}` | weekly progress card PNG / send it |
| POST /voice-note/{pid} | `{to}` | evening summary voice note `{audio_url?, speak_text}` |
| GET/PUT /care/{pid} | `{patient_phone, consent, renew_consent, quiet_start, quiet_end, trigger_missed, auto, snooze_min, ring_s, call_style: ivr\|agent, steps}` | `{settings (+consent_ok, consent_age_days, consent_renew_due), guardians}` |
| POST /guardians · PUT/DELETE /guardians/{id} | `{patient_id, name, relation, phone (any country code), language, channel, quiet_*, is_primary, consent, new_link}` | guardian (+ magic `link`) |
| GET /consent-text/{pid} | `?lang` | `{text, items[], valid_days: 7, stop_word, audio_url}` – read aloud to the patient |
| POST /consent/ask/{pid} | `{to: patient\|family, guardian_id?}` | weekly WhatsApp question "keep reminders? ✅ yes / ⛔ STOP" |
| GET /guardian/{token} | – | family page data (status, ticks, streak, last breath, call, cheers, quiet hours) |
| POST /guardian/{token}/cheer · PUT /guardian/{token}/quiet · POST /guardian/{token}/call-log | `{preset}` · `{quiet_start, quiet_end}` · – | family actions (no login) |
| GET /cheers/{pid} · POST /cheers/{id}/played | `?status` | cheers |
| GET /trend/{pid} | – | `{flag, today_best, avg3, pct_below, text}` (observation, never a diagnosis) |
| GET /patient/{pid} | – | one poll for the patient page: active run, runs, alerts, trend, calls, guardians, settings |

Rules in code, not in the AI: red flags = fixed word lists (`voice.red_flag` + `messages.RED_FLAG_RE`); consent = flag + date, real automated calls only while consent is under 7 days old (`common.consent_current`); quiet hours default 21:00–07:00 IST; real WhatsApp sends ≥ 3 s apart; every automated call/message opens with the AI disclosure in the person's language.
Tables added (SQLite + `supabase/schema.sql`): guardians, care_settings, alerts, escalations, escalation_events, calls, cheers, inbound_messages.

## 7. ML
- `ml/synth.py` generates volume curves per label with noise, so a model exists before any real data. It also exposes `make_breath(label, target_ml, rng)` → `(samples, features)` used by `/api/demo/simulate`.
- `ml/train.py` trains on synthetic + `backend/data/breaths_labelled.csv` (real data weighted ×3). It saves `ml/model.joblib` and `ml/metrics.json`.
- `ml/predict.py`: `load()` and `predict(features) -> {label, proba}`. Features order = the 8 keys above.

## 8. LLM & messaging
- `app/llm.py`: Anthropic SDK with model `claude-opus-5-5`, `output_config={"effort":"low"}` and max_tokens 400. If there's no `ANTHROPIC_API_KEY` or any error → template text. Check `stop_reason`.
- `app/whatsapp.py`: Twilio, if `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` and `TWILIO_WHATSAPP_FROM` are set. Otherwise dry run. Every attempt is stored in `messages`.

## 9. Environment variables (.env locally, Render dashboard when hosted)
`DEMO_MODE=1`, `DATA_BACKEND=demo|supabase` (default `demo`), `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` (server only, never sent to the browser), `TZ_NAME=Asia/Kolkata`, `ANTHROPIC_API_KEY`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_FROM` (e.g. `whatsapp:+14155238886`), `DEMO_FAMILY_WHATSAPP`, `DEMO_NURSE_WHATSAPP`, `SARVAM_API_KEY` (optional), `PORT=8000`.
Comms (calls, WhatsApp, Sarvam Voice Agent, demo routing, quiet hours): `CALL_PROVIDER`, `TWILIO_VOICE_FROM`, `EXOTEL_*`, `SARVAM_AGENT_*`/`SARVAM_ORG_ID`/`SARVAM_WORKSPACE_ID`/`SARVAM_CONNECTION_ID`/`SARVAM_WEBHOOK_SECRET`, `DEMO_PATIENT_PHONE`/`DEMO_GUARDIAN_PHONE`/`DEMO_NURSE_PHONE`, `NURSE_DESK_PHONE`, `QUIET_HOURS`, `COMMS_*` – listed with comments in `.env.example`, explained in `docs/COMMS.md` §8.
If `DATA_BACKEND=supabase` but the keys are missing or Supabase is unreachable at start-up → log a warning and use demo (SQLite).

## 10. Data store (same tables in SQLite and Supabase Postgres)
| Table | Columns |
|---|---|
| patients | id (pk), name, age, sex, surgery, surgery_date, language ('en'\|'hi'\|'ta'), target_ml (default 2000), hold_target_s (default 3), family_phone, nurse_phone, personal_best_ml, created_at |
| sessions | id (pk), patient_id → patients, started_at, slot_date, slot_hour, breaths_count, best_ml, avg_score, source ('demo'\|'device'\|'app') |
| breaths | id (pk), session_id → sessions, patient_id, t, features (json/jsonb), label, score |
| slots | patient_id, slot_date, slot_hour, status ('done'\|'missed'), session_id; primary key (patient_id, slot_date, slot_hour) |
| messages | id (pk), patient_id, kind, to_role, to_number, text, sent, dry_run, created_at |
| breaths_labelled | id (pk), person, label, samples (json), features (json), created_at |
`supabase/schema.sql` creates them (Row Level Security on, no public policies: only the server's service-role key can read/write). `supabase/seed.sql` or `python -m backend.app.seed --target supabase` loads the demo patients.

## 11. Hosting (Render)
`render.yaml` defines one Python web service: build `pip install -r backend/requirements.txt && python ml/train.py`, start `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`, health check `/api/health`. Render's disk is temporary, so in demo mode the SQLite data re-seeds on each start; use `DATA_BACKEND=supabase` to keep data. Step-by-step in `docs/DEPLOY.md`.

## 12. 3D showroom
`web/showcase/index.html` is a standalone Three.js page (from jsdelivr, exact version). It is a separate page and doesn't call `/api`. Every real-world dimension in the model must come from a cited source listed in `docs/3D_SOURCES.md`. Anything not published is flagged there as "not published – measure with caliper" and kept in one config object. Videos are rendered frame by frame with headless Chrome + ffmpeg (`tools/render/`) into `web/showcase/videos/`.

## 13. CONTRACT D3 – Voice & language (/api/voice, Sarvam AI) – called "Contract E" before 2.0
Full table and Python/JS interfaces: `docs/VOICE.md` §3–§4. Files: `backend/app/voice.py` (Sarvam client + fallbacks, red-flag words), `backend/app/voice_cues.py` (all spoken text, 31 cues × 11 languages), `backend/app/routes_voice.py` (router, auto-included by main.py), `web/js/voice.js` (`window.Voice` player), `web/js/voice-ui.js` (widgets), `tools/voice/make_clips.py` → `web/audio/<lang>/<cue>.mp3` + `web/audio/cues.json`.
Languages use short codes `en hi bn ta te kn ml mr gu pa or` (Odia = `od-IN` at Sarvam). Voice language per patient lives in `backend/data/voice_prefs.json` (the `patients.language` column stays en/hi/ta). With no `SARVAM_API_KEY` every endpoint answers with `fallback:"browser"` and the browser speaks. New env vars: `SARVAM_TTS_MODEL`, `SARVAM_TTS_SPEAKER`, `VOICE_GENDER`, `SARVAM_TTS_PACE`, `SARVAM_TTS_CODEC`, `SARVAM_STT_MODEL`, `SARVAM_TRANSLATE_MODEL`, `SARVAM_TIMEOUT_S`, `PUBLIC_BASE_URL`. New dependency: `python-multipart` (audio uploads).

---

# SpiroBuddy 2.0 contracts (E–K)

Added 11 Oct 2026 (Phase 0 of the 2.0 rebuild). Internal Python/JS interfaces that go with these are in `docs/REBUILD_PLAN.md` §3. **Rules for all of E–K:**
- All JSON. Errors look like `{"error": "...", "status": n}` (the existing handlers).
- Every non-GET request under `/api/` needs the header `X-SB: 1` (CSRF rule). Webhooks are exempt.
- Cookies: `sb_staff` (staff, 12 h), `sb_patient` (patient app, 30 days). HttpOnly, `SameSite=Lax`, `Secure` over https.
- Staff routes are scoped by `hospital_id` and the permission matrix (`backend/app/authz.py`). A patient id you can't see answers **404** (never 403), so nobody learns that it exists. Visible but not allowed → 403. Not logged in → 401.
- Times are ISO 8601 with the IST offset. Dates are `YYYY-MM-DD`. The UI shows DD/MM/YYYY and 12-hour time.
- Contract D's routes and fields keep working, behind the staff session (public exceptions in REBUILD_PLAN §3.4). D2 (comms) is unchanged apart from the new kinds `missed_dose` (alert) and `medicine_reminder`, `visit_reminder`, `family_missed_dose` (messages).

## 14. CONTRACT E – Auth (`backend/app/routes_auth.py`)
| Method & path | Body / query | Returns / does |
|---|---|---|
| POST /api/auth/login | `{email, password}` | `{ok, me}` + sets `sb_staff`. 401 `{"error":"wrong email or password"}`. 429 after 10 tries in 15 min per IP + email, then a 15-minute lockout. Pending or disabled staff → 403 with a plain reason. Audited (`auth.login`, `auth.login_failed`). |
| POST /api/auth/logout | – | `{ok}`, revokes the session, clears both cookies. |
| GET /api/auth/me | – | `{authenticated:false}` or `{authenticated:true, kind:"staff", id, name, email, role, hospital:{id,name}, department, permissions_summary, demo_mode}` or `{authenticated:true, kind:"patient", patient_id, name, language}` |
| POST /api/auth/signup | `{join_code, name, email, password, department?, specialty?, reg_no_display?}` | `{ok, status:"pending"\|"active"}`. Doctor role only. Pending when the hospital requires approval (auto-approve in DEMO_MODE). Passwords need at least 10 characters. |
| POST /api/auth/redeem | `{key, name?, email?, password?}` | Creates a nurse account (or adds the grant to the logged-in nurse) → `{ok, me}` + session. Expired, revoked or used-up key → 400 with a plain reason. |
| POST /api/auth/password | `{old_password, new_password}` | `{ok}`; needs the old password. |
| POST /api/me/session | `{token}` or, in DEMO_MODE only, `{patient_id}` | `{ok, patient_id, name, language}` + sets `sb_patient`. The page then removes `t=` from the address bar. |
| GET /api/keys | – | doctor: own keys; admin: every key in the hospital → `[{id, label, doctor:{id,name}, scope, patient_ids, permissions, expires_at, max_uses, uses, revoked_at, status:"active"\|"revoked"\|"expired"\|"used_up", key_hint, grants:[{staff_id,name}]}]` |
| POST /api/keys | `{label, scope:"all"\|"patients", patient_ids?, permissions:[…], expires_days?:30, max_uses?:1}` | doctor only → the key object + `key` (plain text, **shown once**). |
| POST /api/keys/{id}/revoke | – | doctor (own) or admin → key object. Access ends at the nurse's next request. |

## 15. CONTRACT F – Admin and staff (`backend/app/routes_admin.py`)
| Method & path | Body / query | Returns / does |
|---|---|---|
| GET/PUT /api/admin/hospital | `{name, city, address, phone, timezone, languages:[], departments:[], wards:[]}` | hospital profile (admin) |
| GET /api/admin/staff | `?role&status` | `[{id, name, email, role, department, specialty, status, last_login_at}]` |
| POST /api/admin/staff/{id}/{action} | action = `approve` \| `disable` \| `enable` \| `reset-password` \| `department` (`{department}`) | staff row; `reset-password` also returns `temp_password` (shown once) |
| GET /api/admin/join-code | – | `{code_hint, requires_approval, code?}` (`code` only in DEMO_MODE or right after regenerate) |
| POST /api/admin/join-code | `{regenerate?:true, requires_approval?:bool}` | `{code (once), requires_approval}` |
| GET/PUT /api/admin/settings | spec §8.3 settings object: `{grace_minutes:60, alert_thresholds:{…}, quiet_hours:"21:00-07:00", routine:{wake,breakfast,lunch,dinner,bed}, rx_confirm_by:"doctor_or_permitted_nurse", ai_enabled:true, ai_handwriting:false, reminder_channels:[…]}` | settings (admin) |
| GET /api/admin/audit | `?patient_id&actor_id&action&from&to&limit&format=csv` | audit rows (admin; doctors and nurses get their own scope) |
| GET/PUT /api/admin/pilot-checklist[/{step}] | `{status, owner, due, evidence_url, note}` | 14 steps (P1) |
| GET /api/admin/consents | – | consents overview: one row per patient with the item ticks and dates |

## 16. CONTRACT G – Patients (`backend/app/routes_patients.py`)
| Method & path | Body / query | Returns / does |
|---|---|---|
| GET /api/patients | `?doctor&ward&status&programme&q` | scoped list. Every Contract D field, plus `mrn, ward, primary_doctor:{id,name}, programme_status, days_since_discharge, meds_today:{reported,due,missed}, next_visit, open_alerts, device:{serial,state}\|null, consent_chips:[…]` |
| POST /api/patients | `{name, age, sex, surgery, discharge_date, language, ward?, bed?, phone?, city?, primary_doctor_id?, care_plan:{target_ml, hold_target_s, session_hours, breaths_per_session}, routine?}` | enrol → patient + `app_link` (shown once). Consent is posted separately (Contract K). |
| GET /api/patients/{id} | – | Contract D detail + every new column + `care_team`, `consent`, `programme_status`. Audited as `patient.view`. |
| PUT /api/patients/{id} | any editable field | field-level permission checks (care plan needs `careplan.edit`); each save audited; returns the detail |
| GET /api/patients/{id}/timeline | `?kinds=` | merged events from every module, newest first: `[{at, kind, title, detail, actor}]` |
| GET/POST /api/patients/{id}/notes | `{kind:"note"\|"call"\|"handover", text}` | human-written notes |
| GET/POST/DELETE /api/patients/{id}/care-team | `{staff_id, role}` | care team |
| POST /api/patients/{id}/link | – | regenerates the app token → `{app_link, qr_text}` (the old link stops working) |
| POST /api/patients/{id}/programme | `{status:"active"\|"paused"\|"completed"\|"stopped"\|"deceased", confirm?:true, reason?}` | deceased needs `confirm:true`. Paused and deceased stop reminders and alerts at once. Audited. |

## 17. CONTRACT H – Prescriptions and doses (`backend/app/routes_meds.py`, logic in `backend/app/meds/`)
| Method & path | Body / query | Returns / does |
|---|---|---|
| POST /api/patients/{id}/prescriptions | `{prescribed_on?, prescriber_on_paper?, lines:[{drug_name, form?, strength?, dose_qty, dose_unit?, frequency_raw\|frequency_code, times?, food_timing?, duration_days?\|end_date?\|until_stopped?, as_needed?, instructions_raw?}]}` | doctor-typed → **approved** at once (saving = approval) → prescription |
| POST /api/patients/{id}/prescriptions/upload | multipart `file`, `source:"doctor"\|"patient"` | a draft from Gemini (or an empty draft for manual typing) → `{prescription, ai:{ok, reason}}`, status `draft` (staff) or `needs_review` (patient) |
| GET /api/prescriptions/{rx} | – | `{prescription, items:[…with confidence, unclear_fields, status], warnings:[{code, text}], document:{id, file_url}}` |
| PUT /api/prescriptions/{rx}/items/{item} | item fields + `action:"confirm"\|"edit"\|"remove"` | item; a field that is still unclear can't be confirmed |
| POST /api/prescriptions/{rx}/items | a new line | item (manual typing next to the photo) |
| POST /api/prescriptions/{rx}/approve | – | needs every line confirmed or removed → builds the schedule and dose events; records the approver |
| POST /api/prescriptions/{rx}/reject | `{reason}` | rejected |
| POST /api/prescriptions/{rx}/stop | `{reason?}` or `{modify:true}` | stop, or a new draft version that supersedes it (history kept) |
| GET /api/review-queue | – | prescriptions in `draft`/`needs_review` that this actor may approve |
| GET /api/patients/{id}/medicines | – | `{active:[…], as_needed:[…], history:[…versions]}` |
| GET /api/patients/{id}/doses | `?from&to` | `[{id, item_id, drug_name, due_at, status:"upcoming"\|"due"\|"reported_taken"\|"missed"\|"paused"\|"cancelled", reported_at, reported_by_role}]` |
| POST /api/patients/{id}/doses/{dose}/report | – | staff reports on the patient's behalf (logged) |
| POST /api/me/doses/{id}/taken | – | patient → `reported_taken` |
| POST /api/me/doses/{id}/snooze | `{minutes?:10}` | patient snooze |
| POST /api/me/prescriptions | multipart `file` | patient upload → `needs_review` |

**Rules in code:** no dose event exists before approval; SOS/PRN lines are never scheduled; STAT is flagged; times come from the patient's routine and the normaliser, never from AI text; a missed dose (after `grace_minutes`) raises an amber `missed_dose` alert and, only with family consent, a family notice.

## 18. CONTRACT I – Appointments (`backend/app/routes_appointments.py`)
| Method & path | Body / query | Returns / does |
|---|---|---|
| GET/PUT /api/doctors/{id}/availability | `{weekly:[{weekday 0-6, start_time, end_time, slot_minutes, location}], exceptions:[{date, kind:"leave"\|"extra", start_time?, end_time?}]}` | availability |
| GET /api/slots | `?doctor&date` | `[{start_at, end_at, location}]` free slots only |
| GET /api/appointments | `?doctor&patient&from&to&status` | scoped list |
| POST /api/appointments | `{patient_id, doctor_id, start_at, kind:"follow_up"\|"review"\|"other", reason_text?}` | staff books (confirmed). Double booking → 409. |
| POST /api/appointments/{id}/{action} | action = `confirm` \| `propose` (`{start_at}`) \| `decline` (`{reason}`) \| `cancel` \| `attended` \| `no-show` | appointment |
| GET /api/me/appointments | – | the patient's visits, with `when_words` ("Thursday, 15 October, 10:30 AM") |
| POST /api/me/appointments | `{start_at}` (doctor = the patient's primary doctor) | status `requested` |

## 19. CONTRACT J – Documents (`backend/app/routes_documents.py`)
| Method & path | Body / query | Returns / does |
|---|---|---|
| POST /api/patients/{id}/documents | multipart `file`, `kind?`, `title?`, `doc_date?`, `visible_to_patient?`, `visible_to_family?` | validated + stored → document (+ `ai_suggested` {kind,title,doc_date} when AI is allowed) |
| GET /api/patients/{id}/documents | – | list (no deleted) |
| GET /api/documents/{id}/file | `?thumb=1` | the bytes, after a permission check (staff scope, own patient + visible_to_patient, or a guardian token + visible_to_family). Audited `doc.view`. |
| PUT /api/documents/{id} | `{kind, title, doc_date, visible_to_patient, visible_to_family}` | document |
| DELETE /api/documents/{id} | – | soft delete, audited |
| GET/POST /api/me/documents | multipart for POST | the patient's own visible documents / an upload by camera |

## 20. CONTRACT K – Patient app, twin, devices, trust, impact
| Method & path | Body / query | Returns / does |
|---|---|---|
| GET /api/me | – | `{patient_id, name, first_name, language, hospital:{name, nurse_phone}, doctor:{name}, programme_status, care_plan, consent}` |
| GET /api/me/today | – | `{now_card:{kind:"medicine"\|"breathing"\|"visit"\|"done", …}, today:[{kind, title, time, status, icon}], medicines:{…}, next_visit, offline_ok:true}` |
| POST /api/live/{pid} | `{frames:[{t, ml, state, label?, score?}], session_id?}` (batched every 300–500 ms) | `{ok}`; 60 s in-memory ring buffer |
| GET /api/live/{pid} | `?after=<ms>` | `{live:bool, frames:[…], target_ml, state, last_breath, battery_pct, connection}`; with no live session → `{live:false, replay:{samples}}` from `session_curves` |
| GET /api/twin/sim | `?mode=good\|too_fast\|too_shallow\|no_hold` | public simulated curve for `/twin.html` (no patient data) |
| GET/POST/PUT /api/devices | device fields | fleet list / add / edit (P1) |
| POST /api/devices/{id}/{action} | `assign` (`{patient_id}`) \| `return` \| `clean` \| `ready` \| `calibration-check` \| `lost` \| `faulty` \| `retire` | device + a `device_events` row (audited) |
| GET /api/ai-events | `?purpose&limit` | AI register rows (no content, only references) |
| GET /api/ai-events/stats | – | `{drafts, reviewed, lines_total, lines_edited_pct, rejected_pct}` (also shown on `/trust.html`) |
| GET /api/features | – | the status registry `[{key, name, status, where, note}]` (public) |
| GET /api/impact | – | live demo metrics `{patients_coached, sessions_completed, doses_reported_pct, follow_ups_kept_pct, families_informed, ai_lines_edited_pct, label:"demo data, fake patients"}` (public) |
| GET/POST /api/patients/{id}/consent | consent v2 `{items:{care_reminders, family_sharing, records_storage, ai_use, research_use, ai_training:false}, method:"self"\|"witness_thumbprint"\|"guardian", read_aloud, teach_back_ok?, language}` | the current consent; POST adds a new version (old ones kept), `withdraw:true` withdraws. Family sharing and AI use are enforced in code. |
| GET /api/patients/{id}/export.fhir.json | – | FHIR R4 Bundle (P1) |
| /api/demo/* (new) | `med-due/{pid}`, `dose-missed/{pid}`, `patient-upload/{pid}`, `visit-request/{pid}`, `prepare-recording` | DEMO_MODE + admin/doctor |
