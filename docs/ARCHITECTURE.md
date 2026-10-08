# Architecture & interface contracts

## 1. Overview
```
[Sensor: VL53L0X/VL53L1X] -> [ESP32 or Arduino] --USB serial--> [Chrome: web/ app]
                                                        (or Camera / Simulator)
web/app (patient)  -- REST /api/* -->  backend (FastAPI, SQLite, ML model, Claude, Twilio)
web/nurse (dashboard) -- REST /api/* (polling every 2 s) --> backend
```
One laptop runs everything. The backend serves `web/` as static files at `/`.

## 2. Folder layout
```
SpiroBuddy/
  CLAUDE.md                 rules for every session
  START_PROMPT.md           prompt to start a new session
  .env.example              secret names (copy to .env)
  scripts/run.ps1           start the server (creates the venv if needed)
  scripts/setup.ps1         install dependencies
  docs/                     REQUIREMENTS, ARCHITECTURE, ROLES, HANDOFF, PROGRESS, HARDWARE, plans/
  firmware/spirobuddy_serial/spirobuddy_serial.ino
  backend/
    requirements.txt
    app/main.py             FastAPI app, static mount, routers
    app/db.py               SQLite (sqlite3 or SQLModel) + schema
    app/models_ml.py        load model, classify(features)
    app/llm.py              Claude summary + template fallback
    app/whatsapp.py         Twilio send + dry-run fallback
    app/rules.py            status colours, missed-slot logic, score
    app/seed.py             fake patients
    data/                   spirobuddy.db, breaths_labelled.csv (git-ignored db)
  ml/
    synth.py                synthetic breath generator (shares features.py logic)
    features.py             feature extraction from a breath sample array
    train.py                trains RandomForest -> ml/model.joblib + ml/metrics.json
  web/
    index.html  app.js  styles.css         patient app
    nurse.html  nurse.js                   dashboard
    collect.html collect.js                data collection page
    js/sources.js   serial / camera / simulator input
    js/breath.js    calibration, state machine, features, score, rules fallback
    js/voice.js     voice cues (clips -> speechSynthesis fallback)
    js/i18n.js      en / hi / ta strings
    audio/<lang>/<cue>.mp3   optional pre-recorded clips
```

## 3. CONTRACT A – serial line protocol (firmware → browser)
115200 baud, one line per reading, about 30 per second:
```
D,<millis>,<distance_mm>
```
Optional status lines: `S,<text>` (e.g. `S,READY,VL53L1X`). Errors: `E,<text>`. Anything else is ignored.
The browser can send `B\n` to make the device beep (optional; ignored if there's no buzzer).

## 4. CONTRACT B – sample stream inside the browser
Every source emits `{t: ms, raw: number}` (mm for serial, px for camera, mL for the simulator, which uses identity calibration).
Calibration maps raw → mL via linear interpolation over sorted points `[{raw, ml}]`. Distance shrinks as the disc rises, so the mapping may be decreasing. Values are clamped to 0–max.
Smoothing: median of the last 5 values.

## 5. CONTRACT C – breath state machine and features
States: `IDLE → INHALING → HOLDING → FALLING → IDLE`
- IDLE→INHALING: vol > 150 mL and rising
- INHALING→HOLDING: |slope| < 150 mL/s for ≥ 0.3 s
- INHALING/HOLDING→FALLING: vol < 0.9 × peak
- FALLING→IDLE: vol < 100 mL → emit the breath. Ignore it if duration < 0.5 s or peak < 250 mL. Reset if a state lasts > 20 s.
- Live warning: during INHALING, if the 0.3 s rise rate > `FAST_RATE` (default 1200 mL/s) → event `too_fast_live`.

**Breath features object** (the same names in JS, Python and CSV):
```json
{
  "peak_ml": 1800, "pct_target": 0.9, "time_to_peak_s": 3.1,
  "mean_rise_ml_s": 580, "max_rise_ml_s": 900, "hold_s": 3.2,
  "smoothness": 0.12, "duration_s": 8.4
}
```
- `smoothness` = standard deviation of the first difference of the rising segment ÷ its mean (lower = smoother).
- `hold_s` = time with vol ≥ 0.9 × peak.

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
| GET /api/health | – | `{ok, model_loaded, llm_enabled, whatsapp_enabled}` |
| GET /api/patients | – | list of `{id, name, age, surgery, language, target_ml, status, done_today, due_today, best_today, trend}` |
| GET /api/patients/{id} | – | patient + `today` slots + `history` (7 days: date, best_ml, sessions_done) |
| PUT /api/patients/{id} | `{target_ml?, hold_target_s?, language?, family_phone?}` | patient |
| POST /api/classify | features object | `{label, proba:{...}, source:"model"\|"rules"}` |
| POST /api/sessions | `{patient_id, started_at, breaths:[{t, features, label, score}]}` | `{session_id, slot_hour, slot_status}` |
| POST /api/collect | `{person, label, samples:[{t,ml}], features}` | `{ok, count_by_label}` |
| POST /api/train | – | runs ml/train.py and reloads the model → metrics |
| GET /api/model | – | metrics.json |
| POST /api/summary/{id} | `{language?}` | `{text, source:"llm"\|"template"}` |
| POST /api/whatsapp/{id} | `{kind:"summary"\|"missed", to?:"family"\|"nurse"}` | `{sent:bool, dry_run:bool, text}` |
| POST /api/demo/miss/{id} | – | marks the last 2 slots missed and triggers the alert (demo button) |
| GET /api/messages | – | recent message log |

Patient id 1 = "Ravi Kumar", the live demo patient.

**Status rules** (rules.py):
- red: 2+ consecutive missed slots up to now, or done/due < 0.4
- yellow: done/due < 0.7, or best today < 0.8 × personal best
- green: otherwise
- `due` = slots from 8:00 up to the current hour (max 14)

## 7. ML
- `ml/synth.py` generates volume curves per label with noise, so a model exists before any real data.
- `ml/train.py` trains on synthetic + `backend/data/breaths_labelled.csv` (real data weighted ×3). It saves `ml/model.joblib` and `ml/metrics.json` (accuracy, per-class report, confusion matrix, leave-one-person-out if 3+ people).
- Features order = the 8 keys above, in that order.

## 8. LLM & messaging
- `app/llm.py`: Anthropic SDK with model `claude-opus-5-5`, `output_config={"effort":"low"}` and max_tokens 400. If there's no `ANTHROPIC_API_KEY` or any error → template text. Check `stop_reason`.
- `app/whatsapp.py`: Twilio, if `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` and `TWILIO_WHATSAPP_FROM` are set. Otherwise dry run. Every attempt is stored in the messages table.

## 9. Environment variables (.env)
`ANTHROPIC_API_KEY`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_FROM` (e.g. `whatsapp:+14155238886`), `DEMO_FAMILY_WHATSAPP` (e.g. `whatsapp:+91XXXXXXXXXX`), `DEMO_NURSE_WHATSAPP`, `SARVAM_API_KEY` (optional), `PORT=8000`.
