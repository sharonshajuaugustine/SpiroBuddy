# Requirements – SpiroBuddy hackathon MVP

## 1. Problem
Patients get an incentive spirometer after surgery (or for lung disease). At home they skip the exercise or do it wrong (too fast, too shallow, no hold), and nobody can see it. An hourly reminder doubled adherence, 58% vs 28% (Eltorai et al., *JAMA Surgery* 2019). InSee, a US clip-on tracker, was FDA-cleared in 2025, but it fits one US spirometer, works only in hospitals and is English-only. **SpiroBuddy brings this to India:** it fits Indian spirometers, works at home, coaches in Indian languages and updates families on WhatsApp.

## 2. Users
| User | Needs |
|---|---|
| Patient (often elderly, may not read English) | Big simple screen, voice in their language, instant feedback, reminders |
| Family member | Simple WhatsApp updates |
| Nurse / physiotherapist | All patients on one screen, who needs a call, ability to set targets |
| Hackathon judges | A live demo that works, a clear story, honest limits |

## 3. The demo story (acceptance test – everything serves this)
1. Breathe into the spirometer → a live gauge rises in mL.
2. Too fast → the voice says "Slower…" and the screen goes amber. Good breath → "Great breath!", a beep, a score out of 10.
3. The label (good / too_fast / too_shallow / no_hold) comes from **our own trained ML model**.
4. After 10 breaths, the current hour's reminder slot ticks itself ✅.
5. The nurse dashboard updates live; a red patient is visible.
6. Pressing **Send summary** sends an AI-written WhatsApp message (Hindi or English).

## 4. Functional requirements
### Must have (MVP)
- **FR1 Input sources** (one is chosen in the app):
  - (a) **USB serial** from an ESP32/Arduino with a VL53L0X/VL53L1X sensor, via Web Serial
  - (b) **Camera**: tracks the disc height in the video
  - (c) **Simulator**: generates realistic breaths of each type from keyboard keys/buttons. This mode is the default and is used for development and as a demo backup.
- **FR2 Calibration:** convert raw distance (mm) or camera height (px) to mL, using 2+ calibration points (the printed spirometer marks). Saved in localStorage.
- **FR3 Breath detection:** a state machine (IDLE → INHALING → HOLDING → FALLING) produces breath events with features.
- **FR4 Classification:** a server ML model (RandomForest) labels each breath. If the server is unreachable, fall back to client-side rules.
- **FR5 Score 0–10:** depth (4) + speed (3) + hold (3), as specified in ARCHITECTURE.md.
- **FR6 Live coaching:** instant "slower" warning while breathing in; spoken result after each breath. Languages: English + Hindi (Tamil optional). Voice: pre-recorded clips if present, otherwise the browser's speechSynthesis.
- **FR7 Session:** 10 breaths = one completed session, which ticks the current hour's slot.
- **FR8 Patient app:** home (today's checklist 8:00–21:00, streak, Start), session (gauge, speed meter, counter, hold countdown), results, progress chart, settings (language, input source, calibration, target).
- **FR9 Nurse dashboard:** patient list with colour status (rules), patient detail with a 7-day chart, AI summary, set target, Send summary, live updates (poll every 2 s).
- **FR10 AI summary:** Claude writes 3 sentences in the chosen language from the day's stats, with a template fallback.
- **FR11 WhatsApp:** send via Twilio (sandbox). If no credentials, log "would send" and show it in the UI. Also a missed-session alert after 2 missed slots in a row.
- **FR12 Data collection & training:** a page for recording labelled breaths (keys g/f/s/n) → saved to the server → a training script → model file → the server reloads it. A synthetic data generator gives a first model before real data exists.
- **FR13 Demo data:** a seed script creates 6 fake patients with 7 days of history (mixed colours), plus the live demo patient "Ravi".

### Nice to have (only after the MVP works)
Bluetooth (Web Bluetooth) firmware path · on-chip model (emlearn) · buzzer/LED on the device · web push reminders · patient Q&A with red-flag filter · more languages via Sarvam TTS clips · "fast clock" demo mode · PDF report.

## 5. Non-functional requirements
- Runs on **one Windows laptop**: `scripts\run.ps1` → http://localhost:8000. Localhost counts as a secure context, so Web Serial and the camera work without HTTPS.
- **Works offline** except for Claude and WhatsApp, which both have fallbacks.
- **No frontend build step.** Python 3.12, FastAPI, SQLite.
- Readable for elderly patients: font of 18 px or more, high contrast, one main action per screen.
- Live loop latency under 100 ms from reading to gauge.
- Safety: never diagnose; red-flag words get a fixed message; alerts come from rules, not the LLM.

## 6. Hardware assumptions (confirmed only on hackathon day)
Any ESP32 or Arduino (Uno/Nano) + a VL53L0X or VL53L1X sensor, connected over USB. The firmware supports both sensors with a compile-time switch. If there's no hardware, use Camera or Simulator mode. See `docs/HARDWARE.md`.

## 7. Out of scope
Diagnosis, real patient data, app stores, iPhone Bluetooth, regulatory filing.
