# Feature status – everything we discussed, checked against the code

**Current status, 12 October 2026:** use [CODEX_IMPLEMENTATION_HANDOFF.md](CODEX_IMPLEMENTATION_HANDOFF.md) and the application's feature registry for the current local build. The rest of this file is the **10 October historical snapshot**, including its counts, missing artifacts and provider observations. Local completion does not establish deployment or real-provider verification.

**Checked:** 10 Oct 2026, about 2:45 am IST, by the quality controller. **No code was changed.**

## Summary (5 lines)
1. **The demo works today without any hardware or keys.** The website is live at https://spirobuddy.onrender.com on Supabase, and the full story (simulate a session → live tick → missed → reminder ladder → nurse alert → family message) runs in "dry run" (a pretend send that shows the exact text).
2. **Counts (167 features):** Done and verified 84 · Built but not tested live 18 · Partly built 14 · Not built 12 · Deferred on purpose 22 · Waiting on you 17.
3. **Nothing real has been sent or measured yet:** no real WhatsApp, no real phone call, no real Claude summary, and the device has never been switched on (no hardware). The pitch must say "simulated" for these.
4. **The biggest gaps for the demo:** no `docs/DEMO_GUIDE.md`, no full click-through or rehearsal, no pitch slides, and tonight's work (safety tests, new voice clips, new videos) is not saved to GitHub yet, so the live site does not have it.
5. **Top things to do before the demo:** (a) save and push tonight's work, (b) put the Sarvam key on Render, (c) click through the whole story and write the demo guide, (d) make the slides, (e) rehearse twice.

## How I checked (so you know how far to trust each line)
- **Tests I ran myself:** `tests/test_api.py` (13 tests), `tests/test_voice.py` and `tests/test_comms.py` (45 tests, 3 min 10 s). All passed.
- **Tests I did not run:** `tests/test_critical.py` (another agent is still editing it) and `tests/test_supabase_store.py`. Where a line leans on these, it says "not run by me".
- **Live site:** I opened `/api/health` (answer: `data_backend: supabase`, `llm_enabled: false`, `whatsapp_enabled: false`), `/api/voice/status` (`enabled: false`, so Render has no Sarvam key), and `/showcase/` (loads).
- **Everything else:** I read the code and give the file and line. Web pages have no automatic tests; "Done" for a page means the code is there and an earlier browser check is logged in `docs/PROGRESS.md`.
- **Told to me, not re-checked:** real Sarvam voice and translation worked on the laptop in Hindi, Malayalam, Tamil and English.

**Status words:** **Done** = built and checked · **Built, not live-tested** = code is there but needs a key or hardware to prove · **Partly** = some of it is missing · **Not built** · **Deferred** = put off on purpose (it says who and where) · **Waiting on you** = you must do a step.

---

## 1. Device & firmware
| Feature | Status | Evidence | What is left |
|---|---|---|---|
| Firmware reads the laser sensor and sends distance over USB (about 30 readings a second) | Built, not live-tested | `firmware/spirobuddy_serial/spirobuddy_serial.ino` (276 lines) | Never compiled onto a real board. Flash it on hackathon day (TEST_PLAN Level 7). |
| Works with either sensor (VL53L1X or VL53L0X) by changing one line | Built, not live-tested | `.ino:22–23` | Try on the real sensor. |
| Narrow "4×4" sensor window so the tube walls don't confuse it (Q-22) | Built, not live-tested | `.ino:29–30` | Try on the real sensor. |
| Works on 3 board types (XIAO ESP32-C3, ESP32 DevKit, Arduino Uno/Nano) | Built, not live-tested | `.ino:42–60` | Tell Claude which board you got. |
| Device beeps when the website asks | Built, not live-tested | `.ino:111` | Needs a buzzer wired. |
| Device light with the same colour meaning as the app (teal, amber, green, red) | Partly | `.ino:105` (one on/off light only) | A colour light is not written. |
| Hardware guide: wiring, mounting, calibration, troubleshooting | Done | `docs/HARDWARE.md` §1–10 | – |
| USB input in the browser (Web Serial) | Built, not live-tested | `web/js/sources.js:67–78` | Needs a device plugged in. |
| Simulator input (pretend breaths, the default) | Done | `web/js/sources.js:34`; `web/collect.html:113` | – |
| Camera input (track the disc with a webcam, the "Plan B" in REQUIREMENTS FR1b) | Not built | none (`sources.js` has only Simulator and USB) | Build it only if you want a no-sensor live demo. |
| Calibration: turn distance into mL from 2+ marks, saved in the browser | Built, not live-tested | `web/collect.html:79,112` | Only the simulator's 1:1 setting has been used. |
| Per-spirometer calibration table at the printed marks (Q-22) | Waiting on you | none | Needs the device and the spirometer (hardware day). |
| Measured accuracy of the sensor (Q-16, TEST_PLAN Level 7) | Waiting on you | none | Needs hardware. Never quote "±100 mL" until measured. |
| Patient presses one button on the device to start; device counts and stores breaths on its own; hourly chime on the device | Not built | none (the ladder's "device beep" step is simulated on screen) | Future; needs hardware. |
| Bluetooth and Wi-Fi | Deferred | HANDOFF "Known decisions": USB instead of Bluetooth; hackathon plan "Cut for now" | After the hackathon. |
| Battery, battery-low warning, small screen (OLED), fit-check | Deferred | Hackathon plan "Cut for now"; FEATURE_PLAN Stage 3 | After the hackathon. |
| 3D-printed case for the unit | Deferred | Hackathon plan "Cut for now"; only a `.glb` 3D file exists, no print file (`.stl`) | Needs a printer and caliper sizes. |
| One name for the device: "base unit" or "clip-on" (Q-12) | Waiting on you | WORK_QUEUE step 9 | Pick one word. |

## 2. AI/ML breath model
| Feature | Status | Evidence | What is left |
|---|---|---|---|
| Pretend-breath generator (so a model exists before real data) | Done | `ml/synth.py`; `test_demo_simulate_miss_reset` | – |
| Our own trained model, 95.8% correct on pretend breaths | Done | `ml/metrics.json:25` (2,400 pretend breaths, **0 real**) | Say "on synthetic data" in the pitch. |
| Model trained on real breaths | Waiting on you | `ml/metrics.json:22` (`n_real: 0`) | Needs hardware: record breaths, press Train. |
| Server labels each breath (good / too fast / too shallow / no hold), with simple rules as backup | Done | `backend/app/main.py:183`; `test_classify_good_and_fast` | – |
| Breath detection steps (idle → breathing in → holding → falling) and the 8 measurements | Done | `web/js/breath.js:4–21`; `ml/features.py` | The "browser maths = Python maths" check script is not in the repo. |
| Score out of 10 (depth 4 + speed 3 + hold 3) | Done | `backend/app/rules.py`; `test_post_session_ticks_a_slot` | – |
| Record-breaths page (keys g/f/s/n) → save → train → server reloads the model | Done | `web/collect.html:113,205`; `main.py:210,225` | Only tried with simulated breaths. |
| Model details endpoint | Done | `test_model_info` | – |
| "Lower than usual" flag (25% below own 3-day average, worded as an observation) | Done | `backend/app/comms/trend.py`; `test_status_script_trend_card` | – |
| Model on the device chip | Deferred | FEATURE_PLAN Stage 3 | – |
| Personalised coaching ("very slowly" for patients who are often too fast) | Deferred | FEATURE_PLAN Stage 2 | – |

## 3. Patient coaching & voice
| Feature | Status | Evidence | What is left |
|---|---|---|---|
| Patient app (home checklist, big gauge, results, progress, settings, big-screen mode) | Deferred | You set it aside on 9 Oct (HANDOFF "Scope"; WORK_QUEUE Q-21) | You build it separately on the same API. |
| Live "Slower…" warning and spoken coaching during a breath | Partly | `web/collect.html:40,107` (on the record-breaths page only) | There is no patient screen; it shows only on the nurse's recording page. |
| Spoken text for 21 coaching lines in 11 Indian languages (incl. counting 3-2-1, "great breath", reminder, red flag) | Done | `backend/app/voice_cues.py:22–234` | Wording needs a native speaker (see below). |
| Natural Indian voice (Sarvam text-to-speech) | Built, not live-tested | `backend/app/voice.py`; `routes_voice.py:135` | Worked on the laptop (told to me). **Not on the live site**: `/api/voice/status` there says `enabled: false`. |
| Sarvam key on Render | Waiting on you | live `/api/voice/status` | Add `SARVAM_API_KEY` in Render → Environment (or ask Claude to, via the Render connector). |
| Pre-recorded clip library | Partly | `web/audio/<lang>/`: 11 languages × 31 files = 341 files on the laptop | Not saved to git, so not on the live site. Nobody has listened to all of them. |
| Browser voice as the fallback when Sarvam is missing | Done | `test_tts_falls_back_to_browser`; `web/js/voice.js:109` | This laptop has no Hindi browser voice (see below). |
| Translation of the summary (Sarvam) | Built, not live-tested | `routes_voice.py:181` | Worked on the laptop (told to me); not on Render. |
| Speech-to-text: patient speaks, red-flag words are caught | Built, not live-tested | `routes_voice.py:230`; typed path: `test_red_flags_get_fixed_message` | Real recorded speech not tried (TEST_PLAN V4, V5). |
| Patient voice questions answered from a nurse-approved list | Partly | `routes_voice.py:207,266` (one answer only: "how often?") | Other questions just get "noted, your nurse will see it". |
| Voice setting per patient (language, speaker, speed) | Done | `routes_voice.py:76–84` | – |
| Slow, calm voice preset for elderly listeners (speed 0.85) | Done | live `/api/voice/status`: `pace 0.85, temperature 0.7` | – |
| Voice-check card on the demo panel | Done | `web/js/voice-ui.js`; `web/demo.html` | – |
| Native-speaker check of the wording (Hindi, Malayalam, Tamil) | Waiting on you | WORK_QUEUE step 5 | Demo panel → Voice check → pick language → Play; note wrong words. |
| Hindi voice installed on the demo laptop (backup) | Waiting on you | WORK_QUEUE step 6 | Windows Settings → Time & language → Speech → Add voices → Hindi (India). |
| Pain / breathless check after a session (3 big buttons) | Not built | none | Not scheduled. |
| Picture-only steps and a looping technique video for patients | Not built | none (the showroom videos explain the device, not the technique) | Not scheduled. |
| Streak ("5 days in a row") | Done | `backend/app/comms/progress.py:13`; shown on the family page | – |
| Breath garden, family leaderboard | Deferred | FEATURE_PLAN Stage 3 | – |
| Phone notification reminders (web push) | Deferred | Hackathon plan "Cut for now" | – |

## 4. Nurse/doctor website
| Feature | Status | Evidence | What is left |
|---|---|---|---|
| Dashboard: all patients, red / amber / green with a reason, updates live | Done | `web/index.html`; `test_patients_list_has_all_colours`; live site | – |
| Search, status filter with counts, sort, summary tiles | Done | `web/index.html:26–61` | – |
| Light and dark mode; works at phone width | Done | `web/css/styles.css`; PROGRESS "UI 1" browser check | – |
| Patient page: today's hourly slots, 7-day chart, recent sessions | Done | `web/patient.html`; `test_patient_detail_and_update`; `test_sessions_list` | – |
| Set the goal volume and hold time | Done | `web/patient.html:92–93`; `main.py:144` | – |
| Evening summary text (fixed template, in English, Hindi, Tamil, Malayalam) | Done | `test_summary_falls_back_to_template`; `test_malayalam_guardian_gets_malayalam_summary` | – |
| Evening summary written by Claude | Built, not live-tested | `backend/app/llm.py:17,192` | No Anthropic key anywhere, so it has never run. |
| Anthropic key | Waiting on you | live `/api/health`: `llm_enabled: false` | console.anthropic.com → API Keys → Create Key → paste after `ANTHROPIC_API_KEY=` in `.env` and on Render. Optional. |
| Demo panel: simulate good / mixed / poor session, 2 missed slots, reset | Done | `test_demo_simulate_miss_reset`; `web/demo.html` | – |
| Alerts inbox: acknowledge, snooze, assign to me, resolve | Done | `routes_comms.py:175–188`; `web/js/comms-dashboard.js:54–79` | – |
| Red-flag badge; an open red flag always turns the patient red (Q-06) | Done | `test_red_flag_badge_on_patient_list` | – |
| Reminder-ladder timeline on the patient page | Done | `routes_comms.py:263`; `web/js/comms-patient.js` | – |
| Care circle editor (family members, language, channel, quiet hours) | Done | `routes_comms.py:692–736`; `test_guardian_abroad_number` | – |
| Care plan editor | Partly | goal, hold, quiet hours, call type, contacts are editable | "Sessions per day" is fixed at 14 (8 am–9 pm). |
| "Call patient" button (nurse's phone connects to the patient) | Built, not live-tested | `routes_comms.py:358` (logs a pretend call) | A real call needs Twilio or Exotel. |
| Nurse call script (what to ask on the call) | Done | `routes_comms.py:423`; `test_status_script_trend_card` (template) | The Claude version needs the Anthropic key. |
| Breath-quality breakdown (share of good / too fast / shallow / no hold) | Partly | `web/patient.html:204–206` (recent sessions as one bar) | No "over time" view. |
| Print an A4 patient summary (also "Save as PDF" from the print box) | Done | `web/patient.html:158,167`; `styles.css:824` | A server-made PDF is Deferred (Stage 2). |
| Works offline with built-in sample data (`?mock=1`) | Done | `web/js/api.js:3–12` | – |
| Hospital-grade look, one design system on every screen (UI 1 + UI 2) | Done | commits `48fa19c`, `aa8dedf`; `docs/DESIGN_SYSTEM.md` | – |
| Demo board keeps itself realistic through the day (autopilot) | Done | `backend/app/seed.py:237`; `main.py:110` | – |
| Nurse notes, tasks and shift handover | Not built | none | Not scheduled. |
| Login, roles (nurse / doctor / admin), audit log | Deferred | HANDOFF "Scope": no login for the demo; FEATURE_PLAN Stage 2 | Must exist before real patients. |
| Add-a-patient wizard, QR code onboarding | Deferred | FEATURE_PLAN Stage 2 | – |
| Cohort view, many hospitals, CSV / national health-record export | Deferred | FEATURE_PLAN Stage 3 | – |

## 5. Family/guardian
| Feature | Status | Evidence | What is left |
|---|---|---|---|
| Family page by private link, no login: status, today's ticks, streak, last breath | Done | `routes_comms.py:791`; `test_guardian_token_page`; `web/guardian.html` | – |
| Giant text, big buttons, Hindi / English / Tamil | Done | `web/guardian.html:54–61`; PROGRESS "UI 2" | Hindi/Tamil words need a native-speaker check. |
| Big "Call" button (opens the phone dialler) | Done | `web/guardian.html:114` | Not tried on a real phone. |
| "Send a cheer" that the patient hears after the next session | Done | `routes_comms.py:827,877,886`; `web/js/phone-sim.js:393` | – |
| Family member sets their own quiet hours | Done | `test_guardian_sets_own_quiet_hours` | – |
| "Listen" button (speaks the status) | Done | `web/guardian.html:90,129` | – |
| Two or more family members per patient; numbers outside India allowed | Done | `test_guardian_abroad_number`; seed has 14 guardians for 7 patients | – |
| Weekly progress picture in the family member's language | Done | `routes_comms.py:622,632`; `test_status_script_trend_card` | – |
| Family page tried on a real phone on mobile data (TEST_PLAN Level 6 step 3) | Waiting on you | none | Open a guardian link from the live site on your phone. |

## 6. Messaging & calls (WhatsApp, IVR, escalation)
| Feature | Status | Evidence | What is left |
|---|---|---|---|
| Reminder ladder: device beep → WhatsApp → phone call → family → nurse, every step logged | Done | `backend/app/comms/escalation.py`; `test_ladder_fast_forward_reaches_nurse` | Runs in dry run only. |
| 60-second fast-forward of the ladder for the demo | Done | `routes_comms.py:236` | – |
| Keypad call (press 1 / 2 / 3) in the browser phone simulator | Done | `test_ivr_press`; `web/js/phone-sim.js` | – |
| AI conversation call in the simulator ("why did you miss it?") → neutral nurse note | Done | `test_simulated_conversation_same_outcome` | Simulator lines exist in English, Hindi, Tamil only. |
| Real AI phone call through Sarvam Voice Agent | Built, not live-tested | `backend/app/comms/sarvam.py`; `test_sarvam_call_request_and_webhook` (pretend Sarvam) | No real call ever made. |
| Sarvam agent set-up and one real call (TEST_PLAN C3–C5, Q-14) | Waiting on you | `docs/COMMS.md` §5 | Build the agent in the Sarvam dashboard, rent a number (ID check), then tell Claude. |
| Sarvam result arrives and is replayable from saved samples | Done | `test_replay` (4 samples) | – |
| Real keypad calls through Twilio or Exotel | Built, not live-tested | `backend/app/comms/calls.py:348,372` | No accounts or keys. |
| WhatsApp evening summary and missed-session alert (dry run, shows exact text) | Done | `test_whatsapp_is_dry_run_without_keys`; `test_whatsapp_summary_endpoint_respects_consent_and_discloses` | – |
| Real WhatsApp message arriving on a phone (Q-15) | Waiting on you | live `/api/health`: `whatsapp_enabled: false` | twilio.com → Messaging → Try it out → Send a WhatsApp message; send the `join <code>` from each demo phone; paste SID and token into `.env`. |
| WhatsApp quick-reply buttons (Done / 15 min / Call me) | Done | `backend/app/comms/messages.py:50–53`; `test_whatsapp_patient_keywords` | – |
| Family types "status" / "स्थिति" and gets today's progress | Done | `test_whatsapp_webhook_identifies_guardian` | – |
| "help" keyword → fixed emergency message + nurse alert | Done | `test_whatsapp_patient_keywords` | – |
| WhatsApp chat simulator on the demo panel | Done | `web/js/phone-sim.js:41–46`; `routes_comms.py:549,604` | – |
| Summary as a voice note | Done | `routes_comms.py:656` | Natural voice only where the Sarvam key is set. |
| Every call's outcome shows on the dashboard | Done | `routes_comms.py:290–297` | – |
| Messages in Malayalam and Tamil (Q-28) | Done | `test_malayalam_guardian_gets_malayalam_summary` | Native-speaker check. |
| Before 8 am the summary gives yesterday's numbers, not "0 of 0" (Q-29) | Done | `test_early_morning_summary_has_no_zero_of_zero` | – |
| At least 3 seconds between real WhatsApp sends | Done | `test_whatsapp_rate_limit` | – |
| Which WhatsApp provider for a pilot (WaBI or Meta directly) | Done | Research round 9 in `KNOWLEDGE_BASE.md`: keep Twilio for the demo | – |
| Hand the call to a live nurse in the middle of an AI call | Not built | `docs/COMMS.md` §12 | The nurse gets an alert and calls back instead. |
| Breathing session coached over a normal phone call | Not built | none | Not scheduled. |
| Day-1 discharge instructions + technique video; nurse broadcast to all patients | Not built | none | Not scheduled. |
| Daily yes/no red-flag check-in call; missed-call-to-get-a-callback; voice-note replies turned into text | Deferred | FEATURE_PLAN Stage 2; WORK_QUEUE Q-20 | – |

## 7. Safety & consent
| Feature | Status | Evidence | What is left |
|---|---|---|---|
| Red-flag words (11 languages) → fixed "contact your nurse / call 112" message + nurse alert | Done | `test_red_flags_get_fixed_message`; `test_quiet_hours_hold_but_red_flag_goes_through` | – |
| Red flags decided by our fixed word list, never by the AI | Done | `test_red_flag_is_our_rule_not_the_providers` | – |
| The AI never diagnoses: strict instructions, and any reply that sounds like a diagnosis is thrown away | Built, not live-tested | `backend/app/llm.py:27,33` | Its tests are in `test_critical.py` (not run by me); no real Claude call has ever been made. |
| Every automated message and call says it is automated | Done | `test_every_automated_message_and_call_discloses_ai` | – |
| Consent needed before automated calls and messages; it expires after 7 days | Done | `test_no_consent_blocks_automated_calls_and_messages`; `test_lapsed_consent_blocks_real_calls` | – |
| Weekly "keep reminders? yes / STOP" question | Done | `test_weekly_renewal_yes_and_stop` | – |
| One-word STOP in any language | Done | `test_stop_word_any_language` | – |
| Consent text read aloud in the patient's language, with the list of data | Done | `test_consent_text_itemised_in_language` | – |
| Quiet hours (9 pm–7 am) hold routine calls; red flags still go through | Done | `test_default_quiet_hours_are_21_to_07` | – |
| Fake patients only, "Demo mode" label | Done | `backend/app/seed.py`; live `/api/health`: `demo_mode: true` | – |
| Outside callers can't fake a webhook (a webhook = a message another company's server sends to ours) | Partly | `tests/test_critical.py:247–400`; uncommitted changes in `routes_comms.py` | Being finished now by the testing agent; not saved, not on the live site. |
| Safe handling of bad input, heavy load, outages | Partly | `tests/test_critical.py` (about 75 tests, uncommitted) | Same agent; `docs/CRITICAL_TEST_REPORT.md` is not written yet. |
| One shared red-flag word list instead of two (Q-10) | Deferred | WORK_QUEUE Q-10: "after demo" | – |
| Privacy law (DPDP): delete on request, consent records per purpose | Deferred | `docs/FUTURE_ARCHITECTURE.md` §3.7 | Before real patients. |

## 8. Data/deploy/infrastructure
| Feature | Status | Evidence | What is left |
|---|---|---|---|
| Server with every agreed endpoint, working with no keys | Done | `tests/test_api.py` (13 passed) | – |
| Local demo database that fills itself with fake patients | Done | `backend/app/store.py`; `backend/app/seed.py` | – |
| Supabase database (Mumbai) live with demo data | Done | live `/api/health`: `data_backend: supabase`, "supabase connected" | – |
| Falls back to the local demo database if Supabase is down | Built, not live-tested | `backend/app/store.py`; tests in `test_critical.py:1156–1185` (not run by me) | – |
| Website hosted on Render, public address | Done | https://spirobuddy.onrender.com answers | Free plan sleeps after ~15 min: open it a minute before demoing. |
| Deploy recipe and click-by-click guide | Done | `render.yaml`; `docs/DEPLOY.md` | – |
| Code on GitHub | Done | 34 commits; `origin/main` | – |
| Tonight's work saved and pushed | Partly | `git status`: 9 backend files, `tests/test_critical.py`, 341 voice clips, 3 videos, the 3D file all unsaved | Commit and push once the agents finish. Until then the live site is behind the laptop. |
| Data survives a Render restart (TEST_PLAN Level 6 step 4) | Built, not live-tested | data lives in Supabase | Nobody restarted it to check. |
| Start and set-up scripts for the laptop | Done | `scripts/run.ps1`, `scripts/setup.ps1` | – |
| HANDOFF.md up to date (Q-30) | Partly | `docs/HANDOFF.md:14,27,36–38` | Still says "no keys yet" and "authorise Supabase", which are out of date. |

## 9. 3D showroom & videos
| Feature | Status | Evidence | What is left |
|---|---|---|---|
| Interactive 3D showroom of the spirometer + SpiroBuddy unit | Done | live `/showcase/` loads; `web/showcase/showcase.js` (1,506 lines) | – |
| Showroom controls: breath types, exploded view, X-ray, laser, guided tour, 3D file export | Done | `showcase.js:8,332`; PROGRESS "UI 2" browser check | – |
| 4 videos (tour, hero, breath types, exploded) | Done | `web/showcase/videos/*.mp4`; `videos.html` | Older versions are the ones on the live site. |
| Videos re-rendered with fixes and a simple outline patient figure | Partly | `showcase.js:108–112`; 3 of 4 MP4s changed, `tour.mp4` not yet | In progress now; then watch them and commit. |
| 3D model file | Done | `hardware/3d/spirobuddy_setup.glb` | – |
| Every size cited from a source, or flagged "measure with caliper" | Done | `docs/3D_SOURCES.md`; `web/showcase/sources.html` | – |
| Caliper measurements of the real spirometer | Waiting on you | `docs/3D_SOURCES.md` "Measure these"; WORK_QUEUE step 7 | Needs the spirometer and a caliper or ruler. |

## 10. Testing & QA
| Feature | Status | Evidence | What is left |
|---|---|---|---|
| Automatic tests for the server, voice and messaging | Done | 58+ tests passed when I ran 3 of the 5 files today | – |
| Automatic tests for the Supabase path | Built, not live-tested | `tests/test_supabase_store.py` (12 tests; not run by me) | Run with the full suite before the commit. |
| Critical tests: security, safety, failures, load | Partly | `tests/test_critical.py` (uncommitted, still being edited) | Finish, run the whole suite, write the report. |
| Written test plan (8 levels) | Done | `docs/TEST_PLAN.md` | – |
| QA reviews 1 and 2 | Done | `docs/QA_REPORT.md` | Review 3 is due after UI 2 and the critical tests. |
| Person click-through of every screen (TEST_PLAN Level 2, Q-04) | Not built | none since the calls and family features landed | Claude can do it in the browser. |
| `docs/DEMO_GUIDE.md`: click order, what to say, backup per step | Not built | file does not exist | Claude writes it after the click-through. |
| Real voice tests with speech (V4–V6), real call tests (C3–C7), real WhatsApp tests (Level 5) | Waiting on you | TEST_PLAN Levels 3–5 | Need the keys and accounts above. |
| Hardware tests (Level 7) | Waiting on you | TEST_PLAN Level 7 | Needs hardware. |
| Full timed rehearsal, twice (Level 8, Q-18) | Waiting on you | none | Demo morning, with Claude. |

## 11. Research & pitch
| Feature | Status | Evidence | What is left |
|---|---|---|---|
| Research rounds 1–9 with a list of every source read | Done | `docs/research/KNOWLEDGE_BASE.md`, `SOURCES_LEDGER.md` | – |
| Safe numbers and wording for slides; answers to 25 judge questions | Done | `docs/research/PITCH_FACTS.md`; KNOWLEDGE_BASE "JUDGE" | – |
| Long-term plan: demo → pilot → many hospitals | Done | `docs/FUTURE_ARCHITECTURE.md` | – |
| Pitch slides | Not built | no slide file in the repo | Claude can draft them from PITCH_FACTS. |
| One-page printed summary for judges | Not built | none | Claude can draft it. |
| Patent search (has a CAPTCHA), TRAI gazette date (Q-25) | Waiting on you | WORK_QUEUE steps 10–11 | Only a person can do these. |
| Check the hackathon rules; 10-minute talk with a nurse or physiotherapist | Waiting on you | plan checklists (`docs/plans/`) | – |
| Leftover research: home-care prices, TB rehab report (Q-27) | Deferred | WORK_QUEUE Q-27 | – |

## 12. Future (deferred)
The architect's "top 10 decisions to make now" (`docs/FUTURE_ARCHITECTURE.md` §13). **None is built**; I searched the code and found no hospital id, no `/api/v1`, no audit table. Nobody has formally said yes or no to them.

| Feature | Status | Evidence | What is left |
|---|---|---|---|
| 1. A hospital id on every table | Deferred | none in `supabase/schema.sql` | ~2–3 days, before a second hospital. |
| 2. Versioned API (`/api/v1`) | Deferred | none | ~1 day, before the patient app ships. |
| 3. Unguessable ids + "send twice, count once" protection | Deferred | none | ~2 days, before offline sync. |
| 4. No patient names or details sent to the AI or written in logs | Partly | a test in `test_critical.py:915` says the operation is not sent | Names are still sent; log scrubbing not built. |
| 5. Stamp model, rules and firmware version on every breath | Deferred | none | ~1 day. |
| 6. Audit trail and per-purpose consent tables | Deferred | none | ~3–4 days, before real patients. |
| 7. Sending done by a separate worker with a queue | Deferred | sending runs inside the web server today | ~3–5 days, before scaling. |
| 8. Real data only in Mumbai | Partly | Supabase is in Mumbai; Render is in Singapore | Fine for fake data; move the server before real patients. |
| 9. Keep the medical core separate from the messaging features | Deferred | design rule only | – |
| 10. Plain Postgres, no special time-series add-on | Done | `supabase/schema.sql` uses plain tables | – |

---

## Left to build (prioritised)
Value for the demo: 5 = must have, 1 = nice. Effort: S = under an hour, M = a few hours, L = a day or more.

### Can be done by Claude now
| # | Task | Value | Effort |
|---|---|---|---|
| 1 | Finish the critical tests, run the full test suite, then commit and push tonight's work (backend fixes, 341 voice clips, new videos) so the live site matches the laptop | 5 | S |
| 2 | Click through every screen on the live site (TEST_PLAN Level 2) and fix what breaks | 5 | M |
| 3 | Write `docs/DEMO_GUIDE.md`: click order, what to say, the backup for each step | 5 | M |
| 4 | Draft the pitch slides and the one-page summary from `PITCH_FACTS.md` | 5 | M |
| 5 | Finish the `tour.mp4` re-render, watch all 4 videos, commit | 4 | S |
| 6 | Bring HANDOFF.md up to date (site is live, Sarvam key is on the laptop) and run QA review 3 | 4 | S |
| 7 | Add more nurse-approved voice answers (today there is only one) | 2 | S |
| 8 | Camera input mode (only if you want a live breath on stage with no sensor) | 3 | L |
| 9 | Pain / breathless check with 3 big buttons | 2 | M |
| 10 | Nurse notes and shift handover | 2 | M |
| 11 | Hospital id and `/api/v1` (top-10 decisions 1 and 2) | 1 | L |

### Needs the user
| # | Task | Value | Effort |
|---|---|---|---|
| 1 | Put the Sarvam key on Render (Render → your service → Environment → add `SARVAM_API_KEY`), or tell Claude to do it through the Render connector | 5 | S |
| 2 | Rehearse the full demo twice, timed (demo morning) | 5 | S |
| 3 | Listen to the Hindi, Malayalam and Tamil voice lines and report wrong words | 4 | S |
| 4 | Decide "base unit" or "clip-on" | 3 | S |
| 5 | Anthropic key (so the summary is really AI-written) | 3 | S |
| 6 | Twilio WhatsApp sandbox (a real message on a judge-visible phone) | 3 | S |
| 7 | Install the Hindi voice on the demo laptop | 3 | S |
| 8 | Sarvam voice agent + rented number for one real phone call | 3 | M |
| 9 | Open the family page on your phone on mobile data | 3 | S |
| 10 | Patent search and gazette date | 2 | S |

### Needs hardware
| # | Task | Value | Effort |
|---|---|---|---|
| 1 | Flash the firmware, check steady readings | 5 | M |
| 2 | Calibrate at the printed marks; measure real accuracy on 20 breaths | 5 | M |
| 3 | Record real breaths and retrain the model (today: 0 real breaths) | 4 | M |
| 4 | Caliper measurements for the 3D model | 2 | S |
| 5 | Colour light, on-device button and hourly chime | 2 | M |
