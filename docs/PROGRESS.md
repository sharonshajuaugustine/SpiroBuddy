# Progress log

Newest entries at the top. Format: date/time – who – what was done – how it was tested.

- 9 Oct 2026 – voice agent – Sarvam AI integration: backend/app/voice.py (TTS bulbul:v3, STT saaras:v4, translate mayura:v1, language ID, red-flag filter in 11 languages), voice_cues.py (31 cues × 11 languages, need native-speaker check), routes_voice.py (/api/voice/*), web/js/voice.js + voice-ui.js, tools/voice/make_clips.py, docs/VOICE.md, CONTRACT E. Tested with no key (fallbacks); real Sarvam untested until SARVAM_API_KEY is added.
- 9 Oct 2026 – research round 1 – KNOWLEDGE_BASE.md, PITCH_FACTS.md, ledger (63 sources). Claims corrected in REQUIREMENTS (58% vs 28% = share of waking hours; Romsons ₹200–1,000).
- 9 Oct 2026 – firmware, ML (95.8% synthetic), backend (all endpoints, Supabase fallback, Render blueprint), website (dashboard, patient, demo panel, collect) – done and committed; code pushed to GitHub.

- 9 Oct 2026 – lead – Scope change from the user: demo-first nurse/doctor website on Render + Supabase, patient app set aside, new 3D & video agent with cited dimensions. Updated ARCHITECTURE/ROLES/REQUIREMENTS/START_PROMPT/.env.example; started 5 subagents in parallel.

- 9 Oct 2026 – setup session – Created the project folder, git repo, venv and docs (CLAUDE.md, REQUIREMENTS, ARCHITECTURE, ROLES, HANDOFF), plus START_PROMPT.md. Copied the earlier research and plans into docs/plans/. No code yet.
