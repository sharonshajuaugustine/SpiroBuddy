# Handoff – read this first in every new session

**Last updated:** 10 Oct 2026, lead session – UI 1 saved; UI 2 + critical testing running

## Scope (decided by the user, 9 Oct 2026)
- **Everything is DEMO for now:** fake patients, no login, demo control buttons.
- **Focus:** the nurse & doctor **website** (FastAPI serves `web/`; hosted on **Render**; data in **Supabase**, with a local SQLite demo store as default/fallback) and the **3D showroom + videos** (backup in case the hardware isn't ready).
- **Patient mobile app: set aside.** The user builds it separately against the same `/api`.
- **3D model rule:** every size must come from a cited web source (`docs/3D_SOURCES.md`); anything unpublished is flagged "measure with caliper".

## Where we are (9 Oct 2026, evening)
- **Built and committed:** firmware (VL53L1X/VL53L0X, ROI 4×4), ML model (95.8% synthetic), backend (CONTRACT D + demo + Supabase fallback + Render blueprint), nurse/doctor website (dashboard, patient, demo panel, collect), Sarvam voice (11 languages, fallbacks), comms (escalation ladder, IVR + phone/WhatsApp simulators, Sarvam voice-agent provider + webhook + replay, consent with weekly renewal, guardian page, alerts inbox, click-to-call), 3D showroom + 4 videos + GLB, research rounds 1–4 (docs/research/), TEST_PLAN.md, 61 passing pytest tests.
- **QA Review 1** done (docs/QA_REPORT.md): no blockers; fixes made (Indian date formats, cache headers, guardian sizes). **The single backlog is docs/WORK_QUEUE.md — take tasks from its "Next" list.**
- Python packages in `.venv`; `.env` exists (no keys yet).

## Standing rules from the user
- **Quality & efficiency controller** (docs/QA_PROMPT.md) reviews after every build agent and before new launches; max 2 build + 1 research agents at once.
- Never simplify early; explore fully, then converge (docs/FEATURE_PLAN.md). One palette (docs/DESIGN_SYSTEM.md). Patient/guardian side effortless for elderly users.
- **Always keep one research subagent running** (docs/research/RESEARCH_PROMPT.md). If none is running at session start, launch one with the next gaps from docs/research/KNOWLEDGE_BASE.md. It must never re-read a URL in docs/research/SOURCES_LEDGER.md.
- Code is on GitHub: https://github.com/sharonshajuaugustine/SpiroBuddy (branch `main`; local `master` tracks `origin/main`). gh's active account is sharonshajuaugustine.

## Status 10 Oct 2026 (read this before the older notes)
- **Done and pushed:** deploy-readiness (schema fix, DEPLOY.md, 77 tests), Malayalam/Tamil messages, **UI 1** = hospital-grade nurse/doctor screens (index, patient, collect + styles.css, ui.js, icons.js), commit 48fa19c.
- **LIVE (10 Oct, 2:10 am IST):** https://spirobuddy.onrender.com (Render free plan, service `srv-db4l1c49v7es73a7sqog`, Singapore, auto-deploys on every push to `main`). Data: Supabase project `spirobuddy` (ref `lnhdiedfjlqasrtkxweb`, Mumbai, free plan); schema applied, demo data auto-seeded (7 patients, 14 guardians, 308 sessions). `/api/health` says `data_backend: supabase`. No AI/WhatsApp/Sarvam keys set on Render yet (fallbacks in use). Free plan sleeps after ~15 min idle: open the site a minute before demoing.
- **In progress (background agents; if the session died, check `git status` and re-launch):** **UI 2** = restyle `web/guardian.html`, `web/demo.html`, `web/showcase/*` to match DESIGN_SYSTEM.md. **Critical testing** = security, safety, failure and load tests → `tests/test_critical.py` + `docs/CRITICAL_TEST_REPORT.md` (may fix backend bugs, must not touch `web/`).
- **After both land:** QA review (docs/QA_PROMPT.md), then Q-04 click-through + `docs/DEMO_GUIDE.md`, commit, push.
- **Waiting on the user:** (1) authorise the Supabase connector (type /mcp in the session) or follow docs/DEPLOY.md by hand; a Render connector exists in the directory but is not installed. (2) Sarvam AI has no connector: paste the key after `SARVAM_API_KEY=` in `.env`. (3) WaBI question: can the server send through WaBI with an API key, or should we use Meta's WhatsApp Cloud API directly?

## Next steps (older list)
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
- Long-run architecture (demo → many hospitals) and the "top 10 decisions to make now" (tenant_id, /api/v1, UUIDs + idempotency, no PHI in LLM/logs, Mumbai hosting…): see `docs/FUTURE_ARCHITECTURE.md`.

## Queued: India-fit QA agent (start when the comms agent finishes) – checklist from research round 3
- Voice preset for elderly: Bulbul v3, pace 0.85, temperature 0.7; female default per language (priya hi, pooja ml, ishita ta), male option; never "varun". Repeat key numbers; show the same words in large text.
- Formats everywhere: DD/MM/YYYY, 12-hour time, ₹ with lakh grouping, +91 numbers (allow non-+91 for guardians abroad).
- Address forms: "ji", "Amma/Appa", "Chechi" (team guidance – needs an Indian team member's check).
- Fictional hospital names only. Demo patients: man late 50s–60s after CABG; woman 60–68 after knee replacement; woman 40s after cholecystectomy; man ~50 post-TB rehab (plus Ravi).
- Consent: from the patient, in their language, read aloud, itemised data list, one-word "stop", weekly renewal for calls.
- Caregiver is the default WhatsApp recipient; ≥2 guardians.
- Never say: "prevents pneumonia", "first", "clinically proven", "FDA-approved", "diagnoses". Sensor accuracy: report measured numbers, not the ±100 mL target.
