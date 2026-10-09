# SpiroBuddy test plan – how we test everything

**Goal:** before the demo, every part has been tested in three ways:
1. **Automatic tests** that a computer runs in seconds.
2. **A click-through by a person** following the checklists below.
3. **A full rehearsal** of the demo story.

Anything that needs a key or an account (Sarvam, Twilio, Supabase, Render) is tested in steps, from "no key" up to "real". The demo must still work if a real step fails.

Legend: 🤖 = automatic test · 👤 = a person clicks through · 🔑 = needs a key or account · ⏱ = rough time.

---

## Level 1 – automatic tests (run before every commit) 🤖 ⏱ 2 min
| Area | What is checked | How to run |
|---|---|---|
| ML | Model accuracy ≥ 90% on synthetic breaths; `predict()` works | `.venv\Scripts\python.exe ml/train.py` |
| Breath maths | `web/js/breath.js` features = `ml/features.py` features (0 differences on 20 breaths) | parity script (the web agent's Node check) |
| Backend API | Every CONTRACT D endpoint answers with no keys; errors come back as JSON | `.venv\Scripts\python.exe -m pytest tests` |
| Comms | Escalation ladder in fast-forward, IVR key presses, quiet hours, consent blocking, webhook normalisation + replay + red-flag rule, WhatsApp keywords, guardian token | `pytest tests/test_comms.py` |
| Voice | `/api/voice/*` fallbacks with no key; red-flag words caught in 11 languages + romanised Hindi | `pytest tests` (voice tests) |
| Supabase fallback | `DATA_BACKEND=supabase` with no keys → demo store + warning | included in backend tests |

**Pass rule:** all green. A red test blocks the commit until it's fixed.

## Level 2 – click-through checklists 👤 ⏱ 25 min
Start the server: `scripts\run.ps1`, then open http://localhost:8000 in Chrome. Press **Reset demo data** on the demo panel first.

### Dashboard (`/`)
- [ ] The DEMO badge and status chips (data, model, AI, WhatsApp) are visible.
- [ ] Red, yellow and green patients all appear, each with a "why" line.
- [ ] Search, filter and sort work.
- [ ] Dark mode (◐) looks right.
- [ ] Simulate a session for Ravi on the demo panel → his card flashes and the slot ticks within 2 s.
- [ ] The alerts inbox shows alerts; Acknowledge, Snooze and Assign each work and the header count updates.

### Patient page (`/patient.html?id=1`)
- [ ] Slots 08:00–21:00, the 7-day chart and the sessions table all appear.
- [ ] Save target (2000 → 2200 → back to 2000).
- [ ] Generate AI summary → text shown, labelled template or Claude.
- [ ] Send WhatsApp to family and nurse → "would send" is clearly shown.
- [ ] Play summary as voice note → audio plays (Sarvam), or the browser voice speaks.
- [ ] The escalation timeline and care-circle (guardians) settings appear; edit a guardian and save.
- [ ] Call patient (click-to-call) → a dry-run log entry appears.
- [ ] The AI nurse call script appears.
- [ ] The trend flag is worded as an observation, not a diagnosis.

### Demo panel (`/demo.html`)
- [ ] Simulate good, mixed and poor sessions → "model agreed X/10".
- [ ] 2 missed slots → the patient turns red and an alert is logged.
- [ ] **Escalation ladder (fast-forward)** plays: device beep → WhatsApp with buttons → phone rings → guardian → nurse, in about 60 s.
- [ ] **Phone simulator – keypad mode:** it rings, speaks the disclosure + reminder, and pressing 1/2/3 changes the outcome.
- [ ] **Phone simulator – conversational (Sarvam) mode:** the agent speaks; answer by voice or tap "I had mild pain near the incision" → a neutral nurse note appears ("Patient reported … Nurse review requested").
- [ ] **Replay webhook** (normal + red-flag samples) → the nurse note and the red-flag alert appear.
- [ ] WhatsApp simulator: tap ✅ Done / ⏰ 15 min / 📞 Call me; type "status" and "स्थिति" → correct replies.
- [ ] Voice check card: play 5 cues in Hindi, Malayalam and Tamil.
- [ ] The 3D showroom link opens.

### Guardian page (`/guardian.html?t=<token>` – the link is on the patient page)
- [ ] Phone width (375 px): giant text, today's ticks, streak, last breath.
- [ ] "Call Papa" opens the phone dialler (tel: link).
- [ ] "Send a cheer" → the patient hears it after their next simulated session.
- [ ] Switch language (Hindi/English); the "automated updates" notice is visible.

### Record breaths (`/collect.html`)
- [ ] Simulator keys g/f/s/n make breaths; the live graph, "⚠ Slower…" warning and spoken cues all work.
- [ ] (With hardware) Connect over USB → `S,READY` → live mm values → calibration points → breaths detected.

### 3D showroom (`/showcase/`)
- [ ] It loads with no console errors.
- [ ] The breath buttons, exploded slider, X-ray, laser, labels, guided tour (←/→) and GLB export all work.
- [ ] All 4 videos play on `/showcase/videos.html`.
- [ ] The sources page lists every dimension.

## Level 3 – voice (Sarvam AI) 🔑 ⏱ 20 min
| Step | Test | Pass when |
|---|---|---|
| V0 | No key: `GET /api/voice/status` | `enabled:false`; every page still speaks with the browser voice |
| V1 | Add `SARVAM_API_KEY`, restart, `GET /api/voice/status` | `enabled:true` |
| V2 | Text-to-speech (TTS): play 3 cues each in Hindi, Malayalam, Tamil and English | Natural, calm voice; correct language; no clipped words |
| V3 | Make the clip library: `tools\voice\make_clips.py` | About 340 files in `web/audio/<lang>/`; cost about ₹45 |
| V4 | Speech-to-text (STT): record "mujhe saans lene mein dikkat hai" | Red flag = true, the fixed 112 message plays in Hindi, a nurse alert is created |
| V5 | STT: record a normal question ("how many breaths?") | An FAQ answer; no red flag |
| V6 | Translation of the summary into Malayalam/Tamil + voice note | Audio plays; a native speaker says it's understandable |
| V7 | **Native-speaker check** of the 31 cues (at least Hindi, Malayalam, Tamil) | Fixes written back into `voice_cues.py` |

## Level 4 – automated calls, including Sarvam AI calls 🔑 ⏱ 45 min, in this order
We climb from safest to most real. **If any level fails, the demo uses the level below it.**

| Level | What | Needs | Pass when |
|---|---|---|---|
| **C0 – replay** | Demo-panel "Replay webhook" with saved Sarvam payloads (normal, pain, red flag) | Nothing | The nurse note, outcome and red-flag alert appear exactly as specified |
| **C1 – browser phone, keypad** | Fast-forward ladder; answer; press 1/2/3 | Nothing | Each key gives the right outcome and timeline entry |
| **C2 – browser phone, conversational** | Sarvam-style conversation in the simulator; answer by voice (uses Sarvam STT if a key exists) | Optional Sarvam key | Same normalised outcome as C0 |
| **C3 – Sarvam agent web test** | Build the "SpiroBuddy care check-in" agent in the Sarvam dashboard; test it in Sarvam's browser test window, in Hindi and Malayalam | Sarvam account | It opens with the AI disclosure, asks why the session was missed, never diagnoses, and fills the output variables (outcome, reason_category, patient_words, callback_requested) |
| **C4 – Sarvam webhook to us** | Point the Sarvam outbound webhook at our server. Locally this needs a public URL (a tunnel such as Cloudflare Tunnel, or the Render deployment) | C3 + public URL | A real Sarvam webhook arrives, passes the authenticity check, is stored once (idempotent), and the dashboard updates |
| **C5 – one real call** | SpiroBuddy triggers a Sarvam outbound call to **one pre-consented presenter phone** | Rented Sarvam number (KYC) or a connected provider; consent recorded | The phone rings from the service number within 10 s; the conversation works; the webhook arrives; the nurse note appears; total cost about ₹3.50/min |
| **C6 – Twilio / Exotel (optional)** | One IVR call through Twilio (trial: verified number only; India needs a non-Indian caller ID) or Exotel | Accounts and keys | It rings; key presses are logged. Otherwise it falls back to "would call" with a clear reason |
| **C7 – red-flag drill** | In C2 and C5, say "I can't breathe properly" | – | The fixed emergency message plays, a high-priority alert is created and the rule that fired is logged. The AI never gives medical advice |

**Safety checks on every call level:**
- [ ] The call starts with "automated care assistant".
- [ ] No diagnosis and no reassurance that "it's nothing".
- [ ] The patient's own words are stored separately from the summary.
- [ ] Quiet hours (21:30–07:30) block routine calls.
- [ ] No consent means no real call.

**Rehearsal rule:** on demo morning, run C0 → C2 and, if available, C5 from the venue's network. Keep the simulator tab open as the backup.

## Level 5 – WhatsApp 🔑 ⏱ 15 min
1. With no Twilio keys, check that every WhatsApp action shows "would send" plus the exact text.
2. Twilio sandbox: on each demo phone, send `join <code>` to the sandbox number. **Repeat this on demo morning, because it expires after 3 days.**
3. Send the summary, the missed-session alert, the quick replies, the progress card image and the voice note. All should arrive.
4. Reply "1", "done", "status", "स्थिति" and "help" → the right responses come back, and "help" triggers the red-flag flow.
5. Check the rate limit: there should be at least 3 s between sends.

## Level 6 – deploy (Supabase + Render) 🔑 ⏱ 30 min (after the user connects the accounts)
1. Run `supabase/schema.sql`, then the seed. Check that the tables exist and RLS (row-level security) is on.
2. Render Blueprint deploy → `/api/health` shows `data_backend:"supabase"`.
3. Repeat the Level 2 dashboard checks on the Render URL from a phone on mobile data.
4. Restart the Render service → the data is still there (it lives in Supabase).
5. Set `PUBLIC_BASE_URL` → the Sarvam, Twilio and WhatsApp webhooks point at Render, and C4 passes there.

## Level 7 – hardware (hackathon day, when parts arrive) 👤 ⏱ 60 min
Follow `docs/HARDWARE.md`:
1. Compile and upload the firmware → the serial monitor shows `S,READY` and about 30 `D,…` lines per second.
2. Check the reading is steady: with the disc still for 30 s, readings vary by less than ±5 mm.
3. Calibrate at 500, 1,000, 1,500 and 2,000 mL (3 times each).
4. Check accuracy: 20 breaths compared with the printed scale by eye → within ±100 mL.
5. Run `collect.html` live → breaths are detected and labelled, then the dashboard updates.

## Level 8 – full demo rehearsal (go / no-go) 👤 ⏱ 2 × 10 min
Run the demo story in REQUIREMENTS §3 twice, timed, with one person playing the judge:
- [ ] 3D video or showroom (60–90 s)
- [ ] Simulate a session → live dashboard tick
- [ ] Missed slots → red → escalation ladder → phone rings (C5 if live, otherwise C2) → nurse note
- [ ] Send summary → WhatsApp arrives (or "would send")
- [ ] Guardian page on a phone
- [ ] Answer 5 judge questions from `docs/research/KNOWLEDGE_BASE.md` → JUDGE

**Go** = both runs complete in time with no crashes. Otherwise cut to the backups:
- the pre-rendered video
- the browser phone
- a screenshot of a WhatsApp message
- mock mode (`?mock=1`)

## Who does what
- **Lead (Claude):** keeps Levels 1–2 green and runs C0–C2, V0 and the deploy checks.
- **The user:**
  - adds the keys (Sarvam, Twilio)
  - builds and rehearses the Sarvam agent (C3, with Claude's script)
  - rents or connects a number (C5)
  - joins the WhatsApp sandbox on the demo phones
  - does the native-speaker voice check (V7)
  - handles the hardware on the day (Level 7)
