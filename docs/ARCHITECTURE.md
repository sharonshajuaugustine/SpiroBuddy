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
- `hold_s` = time with vol ≥ 0.9 × peak (summed time between consecutive points both ≥ 0.9 × peak).
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
| GET /api/patients | – | list of `{id, name, age, sex, surgery, surgery_date, language, target_ml, status, done_today, due_today, best_today, personal_best_ml, trend, last_session_at}` |
| GET /api/patients/{id} | – | patient + `today` (list of `{hour, status:"done"\|"missed"\|"pending"\|"upcoming", session_id?}`) + `history` (7 days: `{date, best_ml, sessions_done, avg_score}`) |
| PUT /api/patients/{id} | `{target_ml?, hold_target_s?, language?, family_phone?}` | patient |
| GET /api/patients/{id}/sessions | `?limit=20` | list of `{id, started_at, slot_hour, breaths_count, best_ml, avg_score, label_counts:{good,too_fast,too_shallow,no_hold}}` |
| POST /api/classify | features object | `{label, proba:{...}, source:"model"\|"rules"}` |
| POST /api/sessions | `{patient_id, started_at, breaths:[{t, features, label, score}]}` | `{session_id, slot_hour, slot_status}` |
| POST /api/collect | `{person, label, samples:[{t,ml}], features}` | `{ok, count_by_label}` |
| POST /api/train | – | runs ml/train.py and reloads the model → metrics |
| GET /api/model | – | metrics.json |
| POST /api/summary/{id} | `{language?}` | `{text, source:"llm"\|"template"}` |
| POST /api/whatsapp/{id} | `{kind:"summary"\|"missed", to?:"family"\|"nurse"}` | `{sent:bool, dry_run:bool, text}` |
| GET /api/messages | `?limit=50` | recent message log `{id, patient_id, patient_name, kind, to_role, text, sent, dry_run, created_at}` |
| POST /api/demo/simulate/{id} | `{quality?:"good"\|"mixed"\|"poor", breaths?:10}` | server makes a realistic session with ml/synth, classifies and stores it → same as POST /api/sessions + `breaths` |
| POST /api/demo/miss/{id} | – | marks the last 2 slots missed and triggers the missed alert |
| POST /api/demo/reset | – | wipes and re-seeds the demo data → `{ok, patients}` |

`/api/demo/*` only works when `DEMO_MODE=1` (the default for now). Patient id 1 = "Ravi Kumar", the live demo patient.

**Status rules** (rules.py):
- red: 2+ consecutive missed slots up to now, or done/due < 0.4
- yellow: done/due < 0.7, or best today < 0.8 × personal best
- green: otherwise
- `due` = slots from 8:00 up to the current hour (max 14). Times use `TZ_NAME` (default `Asia/Kolkata`).

## 7. ML
- `ml/synth.py` generates volume curves per label with noise, so a model exists before any real data. It also exposes `make_breath(label, target_ml, rng)` → `(samples, features)` used by `/api/demo/simulate`.
- `ml/train.py` trains on synthetic + `backend/data/breaths_labelled.csv` (real data weighted ×3). It saves `ml/model.joblib` and `ml/metrics.json`.
- `ml/predict.py`: `load()` and `predict(features) -> {label, proba}`. Features order = the 8 keys above.

## 8. LLM & messaging
- `app/llm.py`: Anthropic SDK with model `claude-opus-5-5`, `output_config={"effort":"low"}` and max_tokens 400. If there's no `ANTHROPIC_API_KEY` or any error → template text. Check `stop_reason`.
- `app/whatsapp.py`: Twilio, if `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` and `TWILIO_WHATSAPP_FROM` are set. Otherwise dry run. Every attempt is stored in `messages`.

## 9. Environment variables (.env locally, Render dashboard when hosted)
`DEMO_MODE=1`, `DATA_BACKEND=demo|supabase` (default `demo`), `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` (server only, never sent to the browser), `TZ_NAME=Asia/Kolkata`, `ANTHROPIC_API_KEY`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_FROM` (e.g. `whatsapp:+14155238886`), `DEMO_FAMILY_WHATSAPP`, `DEMO_NURSE_WHATSAPP`, `SARVAM_API_KEY` (optional), `PORT=8000`.
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
