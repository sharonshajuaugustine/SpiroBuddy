# Progress log

Newest entries at the top. Format: date/time – who – what was done – how it was tested.

- 10 Oct 2026 – QA controller – Review 2 (HEAD f91b58f): Q-01 and Q-03 verified (live server on 8010: new demo patients after reset, summary WhatsApp has disclosure + footer, nurse path works); CDSCO "Class A + clip-on needs its own licence" wording in docs/plans; CONTRACT D /api/whatsapp row updated. No code changed.
- 10 Oct 2026 – comms + India-fit (commit f91b58f) – Q-01: /api/whatsapp/{pid} goes through comms `send_care_update` (consent/STOP block, AI disclosure, footer, throttle; new test). Q-03: 12-hour slot labels/ticks, India-fit demo patients (CABG 63 M, knee 66 F, cholecystectomy 44 F, post-TB 50 M, Malayalam patient Sreedevi Nair), Sarvam pace 0.85 + temperature 0.7 (from docs.sarvam.ai TTS page). 62 tests pass.

- 10 Oct 2026 – web engineer – Q-06/Q-23: unresolved red-flag alert now forces status red + new `red_flag_open` field on /api/patients (ARCHITECTURE contract D updated), "🚨 Red flag" badge on dashboard card and patient page; AI check-in call relabelled "optional, where consent allows" (human nurse call stays primary); test added.
- 9 Oct 2026 – QA controller – Review 1: no blockers; Indian date/number formats, no-cache static files, guardian page sizes, comms feed chip fixed; WORK_QUEUE.md created. 61 tests pass.
- 9 Oct 2026 – research rounds 3–4 – TRAI A2P rules, LASI elderly data, VL53L1X accuracy, DPDP/CDSCO, PM-JAY rates, cost anchors, post-TB rehab, 25 judge Q&As.
- 9 Oct 2026 – comms – escalation ladder, IVR + simulators, Sarvam voice-agent provider/webhook/replay, consent, guardian page, alerts inbox, COMMS.md, tests/test_comms.py.
- 9 Oct 2026 – 3D – showroom, 4 MP4s (tour 92 s fixed ch. 4, hero, breath-types, exploded), GLB, 3D_SOURCES.md with caliper checklist.
- 9 Oct 2026 – lead – TEST_PLAN.md (8 levels, staged Sarvam calls), pytest suite (API + voice), SPIROBUDDY_DATA_DIR for tests.

- 9 Oct 2026 – voice agent – Sarvam AI integration: backend/app/voice.py (TTS bulbul:v3, STT saaras:v4, translate mayura:v1, language ID, red-flag filter in 11 languages), voice_cues.py (31 cues × 11 languages, need native-speaker check), routes_voice.py (/api/voice/*), web/js/voice.js + voice-ui.js, tools/voice/make_clips.py, docs/VOICE.md, CONTRACT E. Tested with no key (fallbacks); real Sarvam untested until SARVAM_API_KEY is added.
- 9 Oct 2026 – research round 1 – KNOWLEDGE_BASE.md, PITCH_FACTS.md, ledger (63 sources). Claims corrected in REQUIREMENTS (58% vs 28% = share of waking hours; Romsons ₹200–1,000).
- 9 Oct 2026 – firmware, ML (95.8% synthetic), backend (all endpoints, Supabase fallback, Render blueprint), website (dashboard, patient, demo panel, collect) – done and committed; code pushed to GitHub.

- 9 Oct 2026 – lead – Scope change from the user: demo-first nurse/doctor website on Render + Supabase, patient app set aside, new 3D & video agent with cited dimensions. Updated ARCHITECTURE/ROLES/REQUIREMENTS/START_PROMPT/.env.example; started 5 subagents in parallel.

- 9 Oct 2026 – setup session – Created the project folder, git repo, venv and docs (CLAUDE.md, REQUIREMENTS, ARCHITECTURE, ROLES, HANDOFF), plus START_PROMPT.md. Copied the earlier research and plans into docs/plans/. No code yet.
