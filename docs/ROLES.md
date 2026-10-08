# Roles – how work is split between subagents

The lead session (senior engineer) owns the contracts in ARCHITECTURE.md, starts the subagents, joins their work together, tests end to end and updates the docs. Subagents work **in parallel, each only in its own folder**, and must follow the contracts exactly.

| Agent | Folder(s) | Builds | Done when |
|---|---|---|---|
| **1. Firmware & Hardware engineer** | `firmware/`, `docs/HARDWARE.md` | An Arduino sketch for ESP32 *or* Arduino Uno/Nano, VL53L0X *or* VL53L1X (switch by `#define`), serial contract A, optional buzzer on `B`. HARDWARE.md: wiring tables for each board/sensor combination, library install steps, mounting guide (base vs top, ≥5 cm), calibration steps, troubleshooting. | It compiles in principle (correct library APIs, checked against the web docs) and the docs are complete |
| **2. Backend engineer** | `backend/`, `scripts/` | A FastAPI app with contract D, SQLite, seed data, rules, Claude + template, Twilio + dry run, static serving of `web/`, run/setup scripts. | `scripts\run.ps1` starts it, every endpoint answers, and it works with no keys |
| **3. ML engineer** | `ml/` | features.py (contract C), synth.py, train.py → model.joblib + metrics.json. The server loads the model through backend/app/models_ml.py (written together with agent 2: ML provides `ml/predict.py` with `load()` and `predict(features)`). | `python ml/train.py` gives a model with 90%+ accuracy on synthetic data |
| **4. Frontend engineer** | `web/` | Patient app, nurse dashboard, collection page; sources (serial/camera/simulator), breath.js (contract C), voice, i18n en/hi/ta. | In Simulator mode the full demo story works in Chrome |
| **Lead (QA & integration)** | everything | Starts the server, clicks through the demo story, fixes the seams, updates PROGRESS/HANDOFF, commits. | The demo story in REQUIREMENTS §3 passes |

Prompts for each agent should say: read CLAUDE.md + REQUIREMENTS + ARCHITECTURE first, stay inside your folders, and report the files created plus how to test them.
