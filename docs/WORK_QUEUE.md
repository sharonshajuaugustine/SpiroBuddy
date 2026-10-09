# Work queue – the single prioritised backlog

Owned by the quality & efficiency controller (`docs/QA_PROMPT.md`). **Updated:** Review 1, 9 Oct 2026, HEAD `23d8b0b`.
Format: `ID · task · why it matters for the demo · value 1–5 · cost S/M/L · owner · status`. At most 3 items are "next".

**Rules for every agent prompt:** name the exact files, give a "done when", say what not to redo, max 2 build agents + 1 research agent at once, never two agents on the same files.

---

## Next (start these now)

**Q-01 · Route "Send summary" / "missed alert" WhatsApp through the comms sender · safety seam: today it skips consent/STOP, the AI disclosure and the footer · value 5 · S · comms engineer (agent 8) · next**
> Scope: `backend/app/main.py` (`send_whatsapp`, `_send`, ~lines 200–250), `backend/app/whatsapp.py`, `backend/app/comms/messages.py` (`send`), `tests/test_api.py` / `tests/test_comms.py`. Make `/api/whatsapp/{pid}` call `comms.messages.send(...)` (role `family` → each consented guardian, or the patient's family number; role `nurse` unchanged), so the text gets the "automated" disclosure + footer, the ≥3 s throttle, and is skipped (logged "skipped – no consent") when the guardian said STOP. Keep the response shape `{sent, dry_run, text, to_role}` (CONTRACT D) and the "would send" UI. Don't touch the escalation ladder, voice or web files. **Done when:** a new test proves STOP blocks the summary and the text contains the disclosure; `pytest tests -q` all green; PROGRESS.md line added.

**Q-02 · Lead housekeeping: commit the QA fixes, rewrite HANDOFF.md and PROGRESS.md, stop the port-8003 server · the next session must be able to continue from HANDOFF alone (CLAUDE.md rule) · value 5 · S · lead · next**
> Scope: `docs/HANDOFF.md` (still says "5 subagents started"; list what's built: website, comms, voice, 3D + 4 videos, 61+ tests, research round 3), `docs/PROGRESS.md` (add 3D, comms, tests, research rounds 2–3, QA review 1), `.claude/launch.json` (commit or revert the reformat). Kill the comms agent's leftover uvicorn on port 8003 (PIDs 43052/41828 at review time). Commit with the Review 1 fixes listed in `docs/QA_REPORT.md`. **Done when:** `git status` is clean and HANDOFF names the next 3 items from this queue.

**Q-03 · India-fit pass on formats, demo patients and voice preset · judges in India notice US-style times, odd patients and a too-fast voice · value 4 · M · India-fit QA agent (agent 9) · next**
> Scope (bundle of Q-05, Q-07, Q-08): (a) 12-hour times in the UI: slot labels "08:00–21:00" in `web/index.html:68,149`, `web/patient.html`, guardian ticks `web/guardian.html:99` (show "8 am … 9 pm"; keep 24-hour values in the API). (b) `backend/app/seed.py` + `backend/app/comms/seed_comms.py`: make the demo set match HANDOFF's India-fit list (man late 50s–60s after CABG ✓ Abdul; woman 60–68 after knee replacement; woman 40s after cholecystectomy ✓ Priya; man ~50 post-TB rehab; Ravi unchanged as id 1) and give one patient Malayalam; fictional hospital names only. Keep ids 1–7 so tests and guardian tokens (`ravi-amit-demo`) still work. (c) `backend/app/voice.py:90` + `.env.example:18` + `docs/VOICE.md:150`: default pace 0.85, add `temperature` 0.7 if the Sarvam API supports it (check the docs page, don't guess). Don't touch comms logic or the 3D files. **Done when:** `pytest tests -q` green, dashboard shows the new patients after "Reset demo data", a short note in PROGRESS.md.

---

## Queued (in priority order)

| ID | Task | Why it matters for the demo | Value | Cost | Owner | Status |
|---|---|---|---|---|---|---|
| Q-04 | **Person click-through of TEST_PLAN Level 2** (phone keypad 1/2/3, conversational mode, WhatsApp typed "status"/"स्थिति", voice check in hi/ml/ta, guardian "Send a cheer") and write `docs/DEMO_GUIDE.md`: the click order for the 10-min story, what to say, and which backup to use if a step fails | The demo is the product; nobody has walked the full story since comms landed | 5 | M | lead (after Q-01–Q-03) | queued |
| Q-05 | 12-hour time on slots and ticks | India-fit (HANDOFF checklist) | 3 | S | agent 9 | in Q-03 |
| Q-06 | Dashboard status clarity: rename "TREND ▲ Improving" to "Volume (3 days)" or hide it when today has 0 sessions (`backend/app/service.py:114–119`, `web/js/ui.js:54`); show a red-flag badge on the patient card when a red-flag alert is open | "Needs a call" + "Improving" side by side confuses judges; a red-flag patient shown "On track" invites a hard question | 4 | S | web engineer (agent 4) | queued |
| Q-07 | Voice preset: pace 0.85, temperature 0.7 | Elderly listeners (research round 3) | 3 | S | agent 9 | in Q-03 |
| Q-08 | Demo patients per India-fit list + one Malayalam patient | Realistic Indian story | 3 | S | agent 9 | in Q-03 |
| Q-09 | Level 3 voice tests V1–V6 and clip library (`tools/voice/make_clips.py`, ~₹45) | Natural Hindi/Malayalam/Tamil voice instead of the browser's English fallback (this laptop has no Hindi browser voice) | 5 | S | lead, **after the user adds `SARVAM_API_KEY`** | waiting on user |
| Q-10 | Merge the two red-flag lists into one module (`voice.RED_FLAG_WORDS` + `comms/messages.RED_FLAG_RE`) | Less risk of a missed word later; no demo change | 2 | S | comms engineer | deferred (after demo) |
| Q-11 | Replay samples: use the selected patient's name instead of "Ravi" in the label (`backend/app/comms/samples/sarvam_webhooks.json`, replay route) | Cosmetic, only shows if presenter replays for another patient | 1 | S | comms engineer | deferred |
| Q-12 | Pick one word for the hardware ("base unit" as in the 3D model/videos, or "clip-on") and use it in CLAUDE.md, REQUIREMENTS, pitch | Same words everywhere; judges compare video and slides | 3 | S | lead + user decision | queued |
| Q-13 | Deploy: Supabase schema + seed, Render Blueprint, TEST_PLAN Level 6 | A public URL for judges' phones (guardian page on mobile data) and for the Sarvam webhook (C4) | 4 | M | lead, **after the user connects accounts** | waiting on user |
| Q-14 | Sarvam calls C3 → C5 (agent in Sarvam dashboard, webhook over Render/tunnel, one real call to a pre-consented presenter phone) | The "phone actually rings" moment; the browser simulator stays the guaranteed path | 4 | M | user + lead | waiting on user |
| Q-15 | Twilio WhatsApp sandbox, TEST_PLAN Level 5 | Real WhatsApp on a judge-visible phone; "would send" works meanwhile | 3 | S | user + lead | waiting on user |
| Q-16 | Hardware day, TEST_PLAN Level 7: flash firmware, calibrate at 500/1000/1500/2000 mL, record 20 breaths, report *measured* accuracy (never the ±100 mL target) | Real device in the demo; the video is the backup | 5 | M | user + lead (hackathon day) | waiting on hardware |
| Q-17 | ~~Research round 4~~ DONE (commit ee887e6) – (gaps 1–4 in KNOWLEDGE_BASE "Open gaps after round 3"): mL per mm for the Breazer 2500, TRAI type (i)/(ii) for reminders, rupee cost of a lung complication, CDSCO MDSW matrix | Judge Q&A strength; mL/mm also fixes the 3D/calibration numbers | 3 | M | research agent (agent 6, always on) | queued (relaunch with these gaps; never re-read ledger URLs) |
| Q-22 | Firmware: VL53L1X ROI 4×4 centred by default; matte target on the piston; per-model calibration table at 3 printed marks | Wall echoes ruin readings otherwise (F-TECH-3) | 4 | S | lead | ROI done; calibration table on hardware day |
| Q-23 | Care-team wording: patient-facing "wellness" text never names a disease; nurse alerts labelled "care-team mode"; nurse click-to-call (human) shown as the primary call path, AI calls secondary; "some reminder calls need consent renewed weekly" | CDSCO software guidance (F-REG-4), TRAI (F-COMMS-12) | 4 | S | agent 9 (with Q-03) | queued |
| Q-24 | Research round 5: CDSCO 2021 respiratory list / Jan 2025 self-notified list for "incentive spirometer"; Indian 30-day post-op readmission; current Portea/Apollo prices; Indian home IS adherence; RBIPMT 2024 + TB completions | Judge Q&A depth; user wants research always running | 3 | M | research agent | next (runs alongside builds) |
| Q-25 | User hands-on: InPASS patent search (CAPTCHA), TRAI Gazette date on egazette.gov.in, caliper measurements incl. open floor under piston | Can't be done by agents | 3 | S | user | waiting on user |
| Q-18 | Full rehearsal, TEST_PLAN Level 8, twice, timed | Go / no-go | 5 | S | user + lead (demo morning) | queued |
| Q-19 | Remove two stray `console.log` lines in `web/showcase/showcase.js` | Clean console if a judge opens DevTools | 1 | S | 3D engineer | deferred |
| Q-20 | FEATURE_PLAN Stage 2 (daily red-flag check-in call, missed-call callback, QR onboarding, voice-note transcription, PDF report, roles + audit log) | Not needed for the demo; on the "what's next" slide | 2 | L | – | deferred (user rule: never cut, only defer) |
| Q-21 | Patient mobile app | Set aside by the user (built separately against `/api`) | – | L | user | deferred |

FEATURE_PLAN Stage 1 items 1–7 are all built in dry-run (ladder, calls + simulator, alerts inbox, click-to-call, guardian page, quick replies, weekly card, voice note, trend flag, call script, Sarvam agent path). Remaining Stage 1 work is only the live-provider steps (Q-09, Q-13–Q-15).

---

## Waiting on the user (exact steps)

1. **Sarvam key** (natural Indian-language voice, ~₹45 for all clips; ₹100 free credit).
   1. Go to dashboard.sarvam.ai and sign up / log in.
   2. Open **API Keys** → **Create key** → copy it.
   3. Open the `.env` file in the SpiroBuddy folder with Notepad.
   4. Find the line `SARVAM_API_KEY=` and paste the key right after `=` (no spaces). Save.
   5. Tell Claude "Sarvam key added". (Full guide: `docs/VOICE.md`.)
2. **Anthropic key** (AI summary and call script; the template works without it).
   1. Go to console.anthropic.com → **API Keys** → **Create Key** → copy.
   2. In `.env`, paste it after `ANTHROPIC_API_KEY=`. Save. Tell Claude.
3. **Supabase + Render** (public URL for judges; deferred by you to 10 Oct).
   1. In claude.ai → **Settings → Connectors**, connect **Supabase** and **Render** (the Supabase connector also shows as "needs authorisation" in this session; Zapier too, if you want it).
   2. Or follow `docs/DEPLOY.md` by hand: create a Supabase project, copy the URL and `service_role` key into `.env`, then create a Render Blueprint from the GitHub repo.
4. **Twilio WhatsApp sandbox** (optional; "would send" works without it).
   1. Sign up at twilio.com → **Messaging → Try it out → Send a WhatsApp message**.
   2. On each demo phone, send the `join <code>` message shown there. **Repeat on demo morning (it expires after 3 days).**
   3. Paste Account SID and Auth Token into `.env` (`TWILIO_ACCOUNT_SID=`, `TWILIO_AUTH_TOKEN=`). See `docs/COMMS.md`.
5. **Native-speaker check** of the voice cues (Hindi, Malayalam, Tamil at least): open the demo panel → **Voice check** card → pick the language → **▶ Play the coaching sequence**; write down any word that sounds wrong and send it to Claude. Also check the address forms ("ji", "Amma/Appa", "Chechi") with an Indian team member.
6. **Hindi browser voice on the demo laptop** (backup if Sarvam fails): Windows **Settings → Time & language → Speech → Add voices** → add **Hindi (India)**. (Claude can't change system settings.)
7. **Caliper measurements** of the Romsons spirometer for every dimension flagged "measure with caliper" in `docs/3D_SOURCES.md`, plus mL per mm of piston travel.
8. **Hardware on the day:** tell Claude which board (ESP32 or Uno/Nano) and sensor (VL53L0X or VL53L1X) you got.
9. **Decision:** call the device a "base unit" (as in the videos) or a "clip-on" (as in CLAUDE.md)? (Q-12)
