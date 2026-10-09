# Handoff – read this first in every new session

**Last updated:** 9 Oct 2026, lead session – 5 subagents started

## Scope (decided by the user, 9 Oct 2026)
- **Everything is DEMO for now:** fake patients, no login, demo control buttons.
- **Focus:** the nurse & doctor **website** (FastAPI serves `web/`; hosted on **Render**; data in **Supabase**, with a local SQLite demo store as default/fallback) and the **3D showroom + videos** (backup in case the hardware isn't ready).
- **Patient mobile app: set aside.** The user builds it separately against the same `/api`.
- **3D model rule:** every size must come from a cited web source (`docs/3D_SOURCES.md`); anything unpublished is flagged "measure with caliper".

## Where we are
- Docs updated for the new scope: ARCHITECTURE (contracts D, §9–§12), ROLES (5 agents), REQUIREMENTS (demo story), START_PROMPT, `.env.example`.
- 5 subagents started in parallel (see docs/ROLES.md): firmware, backend & data, ML, web (nurse site), 3D & video. Their code may be partly written – check each folder.
- Python packages are installed in `.venv`. `.env` exists (copied from `.env.example`; add the new DEMO_MODE / DATA_BACKEND / SUPABASE_* lines if missing).

## Standing rule from the user
- **Always keep one research subagent running** (docs/research/RESEARCH_PROMPT.md). If none is running at session start, launch one with the next gaps from docs/research/KNOWLEDGE_BASE.md. It must never re-read a URL in docs/research/SOURCES_LEDGER.md.
- Code is on GitHub: https://github.com/sharonshajuaugustine/SpiroBuddy (branch `main`; local `master` tracks `origin/main`). gh's active account is sharonshajuaugustine.

## Next steps (in order)
1. When the agents finish: start the server (`scripts\run.ps1`), test every endpoint, walk the demo story (REQUIREMENTS §3) in the browser, open `/showcase/`, play the videos. Fix the seams.
2. Update PROGRESS.md and this file, commit.
3. Deploy: follow `docs/DEPLOY.md` (Supabase project + Render Blueprint) – needs the user's accounts.
4. Nice-to-haves, then `docs/DEMO_GUIDE.md`.

## Waiting on the user
- **Deferred to 10 Oct by the user:** connect the Supabase + Render connectors in claude.ai (they weren't logged in to Claude on the web). GitHub is DONE (public repo, see above). Until then everything runs locally in demo mode.
- Supabase account + project (URL and service_role key) and a Render account linked to a GitHub repo. (The Supabase connector in Claude also needs authorising in claude.ai connector settings if we want Claude to set it up directly.)
- API keys in `.env`: Anthropic, Twilio (optional; fallbacks work).
- Which hardware they can get (hackathon day), and caliper measurements of the spirometer for any 3D dimension flagged in `docs/3D_SOURCES.md`.

## Known decisions
- Plain HTML/JS frontend, no build step. Browser only calls `/api`; Supabase keys stay on the server.
- Backend runs as `backend.app.main:app` from the repo root (same command locally and on Render).
- USB serial instead of Bluetooth for the hackathon. ML model runs on the server; rules fallback.
- LLM: `claude-opus-5-5` with effort low, plus a template fallback.

## Queued: India-fit QA agent (start when the comms agent finishes) – checklist from research round 3
- Voice preset for elderly: Bulbul v3, pace 0.85, temperature 0.7; female default per language (priya hi, pooja ml, ishita ta), male option; never "varun". Repeat key numbers; show the same words in large text.
- Formats everywhere: DD/MM/YYYY, 12-hour time, ₹ with lakh grouping, +91 numbers (allow non-+91 for guardians abroad).
- Address forms: "ji", "Amma/Appa", "Chechi" (team guidance – needs an Indian team member's check).
- Fictional hospital names only. Demo patients: man late 50s–60s after CABG; woman 60–68 after knee replacement; woman 40s after cholecystectomy; man ~50 post-TB rehab (plus Ravi).
- Consent: from the patient, in their language, read aloud, itemised data list, one-word "stop", weekly renewal for calls.
- Caregiver is the default WhatsApp recipient; ≥2 guardians.
- Never say: "prevents pneumonia", "first", "clinically proven", "FDA-approved", "diagnoses". Sensor accuracy: report measured numbers, not the ±100 mL target.
