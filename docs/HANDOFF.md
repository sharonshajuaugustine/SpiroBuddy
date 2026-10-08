# Handoff – read this first in every new session

**Last updated:** 9 Oct 2026, project setup session (before any code)

## Where we are
- Project folder, git repo, Python venv (`.venv`) and docs are created.
- No application code yet.
- Hardware: **nothing bought yet**. The user will confirm on hackathon day what they can get. Design for: any ESP32/Arduino + VL53L0X/VL53L1X over USB, plus Camera and Simulator modes.
- Python 3.12.13, Node 22 and Git are installed on this laptop. Python packages aren't installed yet: run `scripts\setup.ps1`, or `.venv\Scripts\python -m pip install -r backend\requirements.txt`.

## Next steps (in order)
1. Create `backend/requirements.txt`, `scripts/setup.ps1` and `scripts/run.ps1`, and install the packages.
2. Start the 4 subagents from docs/ROLES.md **in parallel** (firmware, backend, ML, frontend).
3. Integrate: run the server, test the demo story in Simulator mode, fix the seams.
4. Nice-to-haves (REQUIREMENTS §4) only after the MVP passes.
5. Keep this file and PROGRESS.md updated, and commit after each milestone.

## Waiting on the user
- Which hardware they can get (hackathon day).
- API keys in `.env`: Anthropic, and Twilio (WhatsApp sandbox joined from the demo phones). The app works without them using fallbacks.

## Known decisions
- Plain HTML/JS frontend (no build step), served by FastAPI at http://localhost:8000.
- USB serial instead of Bluetooth for the hackathon.
- ML model runs on the server; the browser uses rules if the server isn't reachable.
- LLM: `claude-opus-5-5` with effort low, plus a template fallback.
