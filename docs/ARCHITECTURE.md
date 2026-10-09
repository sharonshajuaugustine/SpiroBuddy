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

## 13. CONTRACT E – Voice & language (/api/voice, Sarvam AI)
Full table and Python/JS interfaces: `docs/VOICE.md` §3–§4. Files: `backend/app/voice.py` (Sarvam client + fallbacks, red-flag words), `backend/app/voice_cues.py` (all spoken text, 31 cues × 11 languages), `backend/app/routes_voice.py` (router, auto-included by main.py), `web/js/voice.js` (`window.Voice` player), `web/js/voice-ui.js` (widgets), `tools/voice/make_clips.py` → `web/audio/<lang>/<cue>.mp3` + `web/audio/cues.json`.
Languages use short codes `en hi bn ta te kn ml mr gu pa or` (Odia = `od-IN` at Sarvam). Voice language per patient lives in `backend/data/voice_prefs.json` (the `patients.language` column stays en/hi/ta). With no `SARVAM_API_KEY` every endpoint answers with `fallback:"browser"` and the browser speaks. New env vars: `SARVAM_TTS_MODEL`, `SARVAM_TTS_SPEAKER`, `VOICE_GENDER`, `SARVAM_TTS_PACE`, `SARVAM_TTS_CODEC`, `SARVAM_STT_MODEL`, `SARVAM_TRANSLATE_MODEL`, `SARVAM_TIMEOUT_S`, `PUBLIC_BASE_URL`. New dependency: `python-multipart` (audio uploads).
