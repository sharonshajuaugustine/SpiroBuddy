# SpiroBuddy – instructions for every Claude session

SpiroBuddy is a hackathon project (Dolphin Tank India Social Impact Hackathon, Healthcare & Wellbeing track). It links the hospital to the patient at home: a clip-on smart unit for an ordinary incentive spirometer (proof the breathing exercise was done) plus an AI breathing coach, a patient web app, a nurse dashboard, WhatsApp updates, and the doctor's prescription on the patient's phone. **Submission closes Mon 12 Oct 2026, 11:00 AM IST; build freeze 03:00 IST. Speed and a working demo beat completeness.**

## Founder decisions (11–12 Oct 2026) – these override older docs
- **Medicines = a digital prescription:** the doctor types it in the hospital software → the patient sees every medicine on their phone → shows that screen (with a QR the chemist can check) at the pharmacy counter, no paper. It is **not** "AI reads a prescription photo".
- **For every hospital and clinic:** each doctor has their own login; each patient's medicines are saved under their hospital registration number (`patients.mrn`); the patient logs in with registration number + PIN (brief: `docs/rebuild/REGNO_PIN_BRIEF.md`). Nothing to do with money or payments, ever.
- **Per-hospital branding, onboarding, store apps, doctor reminders, patient app tabs:** plan in `docs/plan/12_HOSPITAL_ONBOARDING_AND_BRANDING.md` (home-screen name/icon can't change after login in store apps; in-app branding and per-hospital web-app installs can).
- `/` is the public landing page; the nurse dashboard is at `/dashboard.html`.
- **Honesty:** every badge comes from `backend/app/features.py` (Live / Simulated / In development / Planned); flip a key to Live only when it really works. The device is **not built yet**. Never invent usage, pilots or results (e.g. "used during COVID"); never claim "no such software exists" (hospital-chain apps and ABHA apps exist).
- **Deck:** wait for the founder's Dolphin Tank slide template; don't make slides before it arrives.

## Read these first (in order)
1. `docs/HANDOFF.md` – where things stand right now and what to do next
2. `docs/PROGRESS.md` – log of completed work
3. `docs/REQUIREMENTS.md` – what we're building (MVP scope)
4. `docs/ARCHITECTURE.md` – structure and the **interface contracts** (don't break them)
5. `docs/ROLES.md` – how work is split between subagents

## Redesign in progress (SpiroBuddy 2.0) – resume rule
- If the founder asks to **continue the redesign** (or the rebuild or redesign process, or just says "continue" at the start of a fresh session), resume the 2.0 build:
  1. Read `docs/rebuild/STATE.md` first.
  2. Then read the spec `docs/private/ULTRACODE_BUILD_PROMPT.md`: section §R (the resume protocol), then only the sections the next step needs.
  3. Never restart from Phase 0. Never redo steps marked `done`.
- The build may move between Claude accounts. Keep all progress in files: after every finished step, commit, then update and commit `docs/rebuild/STATE.md`.
- If the spec file is missing (fresh clone or another computer), stop and ask the founder to copy it over.

## Rules
- **Keep the contracts in `docs/ARCHITECTURE.md`.** If you must change one, update that file in the same step and note it in PROGRESS.md.
- **Must work with NO hardware.** Every feature has to run in Simulator mode. Real hardware is confirmed only on hackathon day.
- **No build step for the frontend:** plain HTML/CSS/JS in `web/`, served by FastAPI. External libraries come from cdnjs or jsdelivr, with exact versions.
- **Every AI or internet feature needs an offline fallback** (template text, pre-recorded or browser voice).
- **Secrets** go only in `.env` (git-ignored). Never commit keys. `.env.example` lists the variable names.
- **Use fake patients only.** No real health data.
- **The AI never diagnoses.** It coaches and summarises only. Red-flag words → a fixed "contact your nurse / call 112" message.
- **After each milestone:** update `docs/PROGRESS.md` and `docs/HANDOFF.md`, then `git commit`. The next session may be on a different account with zero memory of this one, so HANDOFF.md must always be enough to continue.
- Python: use the venv at `.venv` (`.venv\Scripts\python.exe`). Run the server with `scripts\run.ps1`.
- LLM: provider order Anthropic (Python SDK, model `claude-opus-5-5`, effort "low", short outputs) → Gemini (`gemini-3.1-flash-lite` via `backend/app/ai_gemini.py`) → template text whenever a key is missing or a call fails.

## How to talk to the user
The user is smart but not an engineer. Use plain, short English. Lead with the answer. Say clearly what is **done**, what **failed**, and what is **waiting on them**. When they must act, give numbered click-by-click steps.
