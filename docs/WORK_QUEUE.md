# Work queue – the single prioritised backlog

Owned by the quality & efficiency controller (`docs/QA_PROMPT.md`). **Updated:** Review 2, 10 Oct 2026, HEAD `f91b58f` (Review 1 was `23d8b0b`).
Format: `ID · task · why it matters for the demo · value 1–5 · cost S/M/L · owner · status`. At most 3 items are "next".

**Rules for every agent prompt:** name the exact files, give a "done when", say what not to redo, max 2 build agents + 1 research agent at once, never two agents on the same files.

---

## Next (start these now)

**Q-06 + Q-23 · Dashboard status clarity + care-team wording · in progress (web engineer, files `web/js/ui.js`, `backend/app/service.py`, `web/index.html`) · value 4 · S · next**
> Already under way (red-flag forces red + `red_flag_open`, contract D updated). **Done when:** "Volume (3 days)" label or blank trend when today has 0 sessions; red-flag badge on the card; nurse alerts say "care-team mode"; click-to-call shown first, AI call second; `pytest tests -q` green; PROGRESS line. QA re-checks the dashboard at 375 px afterwards.

**Q-04 · Person click-through of TEST_PLAN Level 2 + `docs/DEMO_GUIDE.md` · the demo is the product and nobody has walked the full story since comms landed · value 5 · M · lead · next**
> See the Q-04 row below for the story order. Start after Q-06/Q-23 lands so the guide matches the screens. Use the new patients (Abdul CABG red, Mohan post-TB red, Sreedevi Malayalam green). **Done when:** DEMO_GUIDE.md has the click order, what to say, and a backup per step.

**Q-28 · Malayalam comms text · the Malayalam demo patient's husband (Gopakumar, `ml`) gets the summary/alerts in English today (`backend/app/comms/common.py:32` `lang_of` maps `ml` → `en` by design) · value 3 · S–M · comms engineer · done (10 Oct, comms engineer; native-speaker check still open)**
> Scope: `backend/app/comms/messages.py` (disclosure + `FOOTER` + quick replies in `ml`), `backend/app/comms/common.py` (`LANGS` add `ml`), `backend/app/llm.py` (`template_summary` ml branch), `backend/app/whatsapp.py` (`missed_text` ml), `tests/test_comms.py`. Flag the strings "needs native-speaker check" (user step 5). Don't touch web/ or service.py. **Done when:** POST `/api/whatsapp/6 {kind:"summary",to:"family"}` returns Malayalam text with Malayalam disclosure + footer; STOP word in Malayalam blocks it; `pytest tests -q` green.

---

## Queued (in priority order)

| ID | Task | Why it matters for the demo | Value | Cost | Owner | Status |
|---|---|---|---|---|---|---|
| Q-01 | WhatsApp summary/missed through the comms sender | – | – | – | comms engineer | **done** (f91b58f; verified Review 2) |
| Q-02 | Lead housekeeping (commit, HANDOFF/PROGRESS) | – | – | – | lead | **done** (5de9e0a) |
| Q-03 | India-fit pass (12-hour times, demo patients, voice preset) | – | – | – | agent 9 | **done** (f91b58f; verified Review 2) |
| Q-29 | Summary text polish: before 8 am it says "0 of 0 sessions today" (say "today's sessions start at 8 am" + yesterday's numbers); drop the duplicated "SpiroBuddy - Name:" prefix now that the disclosure line names SpiroBuddy (`backend/app/main.py` `send_whatsapp`, `backend/app/llm.py` `template_summary`) | Judges may press "Send summary" at any hour | 2 | S | comms engineer (with Q-28) | done (10 Oct, with Q-28) |
| Q-30 | HANDOFF.md: add Q-01/Q-03/round 5 as done and name the new "next" (Q-06/Q-23, Q-04, Q-28) | CLAUDE.md rule: HANDOFF alone must be enough | 4 | S | lead (at next commit) | queued |
| Q-04 | **Person click-through of TEST_PLAN Level 2** (phone keypad 1/2/3, conversational mode, WhatsApp typed "status"/"स्थिति", voice check in hi/ml/ta, guardian "Send a cheer") and write `docs/DEMO_GUIDE.md`: the click order for the 10-min story, what to say, and which backup to use if a step fails. **Story order (round 4):** missed sessions → nurse alert → nurse clicks **☎ Call patient** (nurse and patient connected, a human call) as the *primary* call path; the AI reminder/check-in call is shown second as "optional, where consent allows" | The demo is the product; nobody has walked the full story since comms landed | 5 | M | lead (after Q-01–Q-03) | next |
| Q-05 | 12-hour time on slots and ticks | India-fit (HANDOFF checklist) | 3 | S | agent 9 | done (Review 2) |
| Q-06 | Dashboard status clarity: rename "TREND ▲ Improving" to "Volume (3 days)" or hide it when today has 0 sessions (`backend/app/service.py:114–119`, `web/js/ui.js:54`); show a red-flag badge on the patient card when a red-flag alert is open | "Needs a call" + "Improving" side by side confuses judges; a red-flag patient shown "On track" invites a hard question | 4 | S | web engineer (agent 4) | next (in progress) |
| Q-07 | Voice preset: pace 0.85, temperature 0.7 | Elderly listeners (research round 3) | 3 | S | agent 9 | done (Review 2; temperature cited from docs.sarvam.ai TTS page, VOICE.md §1.1) |
| Q-08 | Demo patients per India-fit list + one Malayalam patient | Realistic Indian story | 3 | S | agent 9 | done (Review 2) |
| Q-09 | Level 3 voice tests V1–V6 and clip library (`tools/voice/make_clips.py`, ~₹45) | Natural Hindi/Malayalam/Tamil voice instead of the browser's English fallback (this laptop has no Hindi browser voice) | 5 | S | lead, **after the user adds `SARVAM_API_KEY`** | waiting on user |
| Q-10 | Merge the two red-flag lists into one module (`voice.RED_FLAG_WORDS` + `comms/messages.RED_FLAG_RE`) | Less risk of a missed word later; no demo change | 2 | S | comms engineer | deferred (after demo) |
| Q-11 | Replay samples: use the selected patient's name instead of "Ravi" in the label (`backend/app/comms/samples/sarvam_webhooks.json`, replay route) | Cosmetic, only shows if presenter replays for another patient | 1 | S | comms engineer | deferred |
| Q-12 | Pick one word for the hardware ("base unit" as in the 3D model/videos, or "clip-on") and use it in CLAUDE.md, REQUIREMENTS, pitch | Same words everywhere; judges compare video and slides | 3 | S | lead + user decision | queued |
| Q-13 | Deploy: Supabase schema + seed, Render Blueprint, TEST_PLAN Level 6 | A public URL for judges' phones (guardian page on mobile data) and for the Sarvam webhook (C4) | 4 | M | lead, **after the user connects accounts** | waiting on user |
| Q-14 | Sarvam calls C3 → C5 (agent in Sarvam dashboard, webhook over Render/tunnel, one real call to a pre-consented presenter phone) | The "phone actually rings" moment; the browser simulator stays the guaranteed path | 4 | M | user + lead | waiting on user |
| Q-15 | Twilio WhatsApp sandbox, TEST_PLAN Level 5 | Real WhatsApp on a judge-visible phone; "would send" works meanwhile | 3 | S | user + lead | waiting on user |
| Q-16 | Hardware day, TEST_PLAN Level 7: flash firmware, calibrate at 500/1000/1500/2000 mL, record 20 breaths, report *measured* accuracy (never the ±100 mL target) | Real device in the demo; the video is the backup | 5 | M | user + lead (hackathon day) | waiting on hardware |
| Q-17 | Research round 4 (sensor ROI, CDSCO wording, calls, hands-on list) | – | – | – | research agent | **done** (KNOWLEDGE_BASE "Round 4 additions") |
| Q-22 | Firmware: VL53L1X ROI 4×4 centred by default; matte target on the piston; per-model calibration table at 3 printed marks | Wall echoes ruin readings otherwise (F-TECH-3) | 4 | S | lead | ROI done; calibration table on hardware day |
| Q-23 | Care-team wording: patient-facing "wellness" text never names a disease; nurse alerts labelled "care-team mode"; nurse click-to-call (human) shown as the primary call path, AI calls secondary; "some reminder calls need consent renewed weekly" | CDSCO software guidance (F-REG-4), TRAI (F-COMMS-12) | 4 | S | agent 9 (with Q-03) | next (with Q-06) |
| Q-24 | Research round 5: CDSCO 2021 respiratory list / Jan 2025 self-notified list for "incentive spirometer"; Indian 30-day post-op readmission; current Portea/Apollo prices; Indian home IS adherence; RBIPMT 2024 + TB completions | Judge Q&A depth; user wants research always running | 3 | M | research agent | done (as capped Q-26, f91b58f) |
| Q-25 | User hands-on: InPASS patent search (CAPTCHA), TRAI Gazette date on egazette.gov.in, caliper measurements incl. open floor under piston | Can't be done by agents | 3 | S | user | waiting on user |
| Q-26 | **Research round 5 – capped.** Run now in the research slot (standing rule: one research agent always on), limited to the 3 gaps that change the pitch: (1) CDSCO 2021 respiratory list / Jan 2025 self-notified list – is "incentive spirometer" listed, which class; (2) Indian 30-day post-op readmission rates (problem slide); (3) any Indian home IS adherence data (likely none – stop after ~5 sources and say so). **Defer** Portea/Apollo current prices and the RBIPMT 2024 rehab PDF + TB completions (business/vision slides only). Cap ~15 new sources, never re-read ledger URLs, output = KNOWLEDGE_BASE + PITCH_FACTS update | Strengthens 2 judge answers (regulation, size of the problem); the rest is nice-to-have | 3 | M (background, no build files) | research agent (agent 6) | **done** (commit f91b58f) |
| Q-27 | Research leftovers: Portea/Apollo home-care prices; RBIPMT 2024 rehab PDF + TB completions | Business and "vision" slides only | 2 | S | research agent | deferred (after round 5) |
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
7. **Hands-on measurements on hackathon day** (research round 4: none of these are published). With a caliper or ruler, on the Romsons Breazer 2500, write down:
   1. the inner diameter of the tube the piston moves in;
   2. the piston's full travel (bottom to top, in mm);
   3. the spacing in mm between the printed marks (e.g. 500 → 1,000 → 1,500 mL);
   4. whether the floor under the piston is open (can the sensor see up from the base?);
   5. with the sensor fitted: the reading at the top of travel (piston fully up).
   Also every dimension flagged "measure with caliper" in `docs/3D_SOURCES.md`. Send the numbers to Claude (they fill the calibration table, Q-23).
8. **Hardware on the day:** tell Claude which board (ESP32 or Uno/Nano) and sensor (VL53L0X or VL53L1X) you got.
9. **Decision:** call the device a "base unit" (as in the videos) or a "clip-on" (as in CLAUDE.md)? (Q-12)
10. **InPASS patent search** (it has a CAPTCHA, so only a person can do it): go to iprsearch.ipindia.gov.in → **Patent Search** → search the title/abstract for "incentive spirometer", then "respiratory exerciser" and "spirometer sensor". Send Claude a screenshot or the list of titles and application numbers.
11. **TRAI Gazette date check:** go to egazette.gov.in → **Search** → search "Telecom Commercial Communications Customer Preference (Third Amendment) Regulations, 2026". Send Claude the publication date and the gazette ID shown (it fixes the "from when" in the calls wording).
