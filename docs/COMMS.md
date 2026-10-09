# Calls, WhatsApp and family updates – SpiroBuddy comms

**In one line:** when a patient misses breathing sessions, SpiroBuddy nudges them step by step (device beep → WhatsApp → automated phone call → family → nurse), and everything works today with no keys, inside browser "phone simulators".

Status (9 Oct 2026): all of Stage 1 is built and tested in dry run (41 automated tests, `tests/test_comms.py`). Real Twilio, Exotel and Sarvam calls are coded against the official docs but **not yet tried with real keys** – they need your accounts (section 9).

---

## 1. How it works

**Main point:** SpiroBuddy is a polite reminder ladder. Each step only happens if the one before didn't work, and the nurse is told at the end.

**Everyday comparison:** a good ward sister doing rounds. First she taps the bed (device beep). Then she leaves a note (WhatsApp). Then she phones the room (automated call). If nobody answers, she calls the son (guardian). If he can't help either, she tells the duty nurse (red alert on the dashboard).

**What really happens:**
1. The server watches the hourly slots. After 2 missed sessions in a row (changeable per patient) a **ladder** starts.
2. Steps, each with a delay (default 0, 10, 10, 15, 15 minutes): device beep + teal light → WhatsApp reminder with 3 big buttons (✅ Done / ⏰ 15 min / 📞 Call me) → automated call → guardian WhatsApp + call → nurse alert.
3. The patient's call is either a **keypad call** ("press 1 if done, 2 for later, 3 for the nurse") or an **AI conversation** ("Are you okay? Why did you miss it?"). You choose per patient (Care circle → "Patient's call").
4. Any answer that solves it (a real session, "Done", "I'll check on him") stops the ladder. A request for the nurse goes to the **Alerts inbox**.
5. **Red-flag words** ("chest pain", "can't breathe", "साँस नहीं"… in 11 languages) skip everything: the fixed message "Please contact your nurse now. If it's an emergency, call 112", a red alert, and the family is told – even at night.
6. Every step lands on the patient's **timeline**, so the nurse can see exactly who was told what and when.

**Where the comparison breaks:** a ward sister uses judgement. SpiroBuddy does not. It follows fixed rules written in code, and it **never diagnoses** – the AI only words messages and summarises. Red flags come from fixed word lists, never from the AI.

---

## 2. What works right now with no keys (dry run)

| Feature | Where to see it |
|---|---|
| Escalation ladder, real speed or **fast-forward (≈60 s)** | Demo panel → "▶ Play escalation ladder"; patient page → "Escalation ladder" |
| Automated keypad call (press 1/2/3) in Hindi / English / Tamil | Demo panel → patient phone rings; tap ✆, then a button |
| **AI check-in call** (spoken answers) | Demo panel → "Patient's call: 🗣 AI conversation" or "🗣 AI check-in call now"; answer with 🎤 or tap a pre-written answer |
| **Replay a saved Sarvam result** (backup if a live call fails) | Demo panel → pick a sample → "⏯ Replay saved Sarvam result" |
| WhatsApp with quick-reply buttons, weekly progress card, voice note | Demo panel → patient and family phones |
| WhatsApp replies: 1/2/3, done, status, स्थिति, help, STOP | Type in the simulator box, or tap a button |
| Alerts inbox (acknowledge, snooze, assign to me, resolve) | Dashboard → "🔔 Alerts inbox"; bell in every header |
| Click-to-call (nurse's phone rings first, then the patient) | Alerts inbox or patient page → "☎ Call patient" (dry run says "would ring") |
| AI nurse call script (Claude, or a fixed template) | Patient page → "✨ AI call script" |
| Lower-than-usual trend flag (an observation, not a diagnosis) | Patient page; Alerts inbox ("Lower than usual") |
| Care circle: patient phone, consent, quiet hours, ladder steps, ≥2 guardians, magic links | Patient page → "Care circle & reminders" |
| Consent statement read aloud, weekly "keep reminders?" question, STOP | Patient page → "🔊 Read consent aloud" / "📨 Ask “keep reminders?”" |
| Family page (no login, giant text, "Call Papa", cheers, quiet hours) | Patient page → "Family page ↗", or `/guardian.html?t=ravi-amit-demo` |

Voices: with no Sarvam key the browser speaks (Edge has the most Indian voices). With `SARVAM_API_KEY` the voices are natural Indian voices (docs/VOICE.md).

---

## 3. Safety and the law (built in)

- **AI disclosure first.** Every automated call and message begins: "Namaste, this is SpiroBuddy's automated care assistant" (in Hindi / Tamil / English). Replies inside a chat start with "🤖 SpiroBuddy automated assistant:". Sarvam's terms require this.
- **Consent = yes + date.** No automated call or WhatsApp goes to a person without consent recorded with its date (patient: Care circle; family: per guardian). Missing → the step is skipped and the timeline says why.
- **Consent lasts 7 days.** TRAI's 2026 rules treat AI/robocalls as "A2P calls"; "ongoing use" calls need consent that lasts 7 days and can be renewed. After 7 days **real** calls are blocked (the simulator still rings, with a note) until the person says yes again. Once a week SpiroBuddy asks one question on WhatsApp: "Keep the reminders? ✅ Yes / ⛔ STOP" – one tap renews it.
- **One-word STOP.** "STOP", "रोको" or "நிறுத்து" withdraws consent at once (DPDP Rules). The nurse can still call as a person.
- **Consent statement** (Patient page → "🔊 Read consent aloud"): from the patient's point of view, in their language, read aloud, with an itemised list of the data kept (name/age/operation, phone and language, family names and numbers, breathing counts and readings, answers on calls and messages), "never diagnoses", the stop word and the 7-day validity.
- **Quiet hours** default **21:00–07:00 IST**. Changeable per patient (nurse) and per family member (on the family page, one tap). Only red flags break through.
- **Real calls only to consenting team phones in the demo.** Fake patients have placeholder numbers (…XXXX), which are never dialled; real calls go to `DEMO_PATIENT_PHONE` / `DEMO_GUARDIAN_PHONE` / `DEMO_NURSE_PHONE`.
- **No SMS in the hackathon.** Indian SMS needs DLT registration by an Indian company (1–3 weeks). The "SMS" channel is logged as a dry run only (roadmap).
- **Never diagnoses.** Call results are written as neutral notes: "Patient reported “…” and missed two sessions. Nurse review requested." Possible distress (from the provider's sentiment) is only shown as "possible distress – nurse to review (low confidence)".
- WhatsApp sends are spaced **at least 3 seconds apart** (Twilio sandbox limit).

---

## 4. Twilio – WhatsApp and demo calls (about 15 minutes)

**What you get:** real WhatsApp messages to your team's phones (sandbox) and real automated calls to verified phones. **Limits of a trial account:** 30 days, at most 5 verified numbers, calls only to verified numbers, Twilio's own WhatsApp templates only, about 75 free voice minutes. Calls to Indian numbers show an **international caller ID** (+1…) – that is Twilio's India rule. Fine for a demo; a real product uses an Indian number (Exotel or Sarvam).

1. Go to https://www.twilio.com/try-twilio and sign up. Verify your email and phone.
2. In the Console home page, copy the **Account SID** and **Auth Token**.
3. Open `.env` in the SpiroBuddy folder (Notepad). Paste them after `TWILIO_ACCOUNT_SID=` and `TWILIO_AUTH_TOKEN=`. Save.
4. **WhatsApp sandbox:** Console → **Messaging → Try it out → Send a WhatsApp message**. You see a code like `join silver-tiger`.
5. On **each** team phone, open WhatsApp and send that exact text (`join silver-tiger`) to **+1 415 523 8886**.
6. In `.env` set `DEMO_FAMILY_WHATSAPP=whatsapp:+91XXXXXXXXXX` (the "son" phone) and `DEMO_NURSE_WHATSAPP=whatsapp:+91…` (the "nurse" phone). Optional: `DEMO_PATIENT_PHONE=+91…`, `DEMO_GUARDIAN_PHONE=+91…`.
7. ⚠ **Rejoin on demo morning.** The sandbox session ends after **3 days**. Send the `join …` text again from every phone on demo morning. It also opens the 24-hour window that free-form messages need. If a send fails, the demo panel shows "Sandbox: rejoin needed".
8. **Calls (optional):** Console → **Phone Numbers → Buy a number** (a US number is fine on trial). Put it in `TWILIO_VOICE_FROM=+1…`. Then **Phone Numbers → Verified Caller IDs → Add** each team phone (max 5). Then **Voice → Settings → Geo permissions → tick India**.
9. Calls and WhatsApp replies need Twilio to reach our server, so the server must be on the internet (Render, section 7) with `PUBLIC_BASE_URL` set.
10. **WhatsApp replies (optional):** Console → Messaging → Try it out → **Sandbox settings** → "When a message comes in": `https://<your-app>.onrender.com/api/comms/webhooks/whatsapp` (method POST). Save.
11. Restart the server. The demo panel line should say "WhatsApp: live (Twilio)".

---

## 5. Sarvam Voice Agent – the AI check-in call (about 1 hour, plus KYC time)

**What it is:** a real phone call from an Indian number where an AI voice says (in Hindi, Tamil, Malayalam…): "We noticed you missed your breathing exercise. Are you okay, and would you like to tell me why?" The patient just talks. SpiroBuddy receives the answer, checks it with its own fixed red-flag rules, and writes a neutral note for the nurse.

**Price:** Sarvam's launch page says **₹3.50 per minute** for Voice Agents, including authoring, simulation, phone numbers, evaluation and analytics. A 2-minute check-in ≈ ₹7–8. New accounts get ₹100 free credit (about 28 minutes, if it applies to Voice Agents – check in the dashboard). Numbers rented from Sarvam are paid from the Sarvam wallet (price shown in the catalogue; 30-day rental, auto-renews).

### 5.1 Verified API facts (read on 9 Oct 2026)
- Base URL for calls: `https://apps.sarvam.ai/api/outbounds`. Auth header: `X-API-Key: <key>` (Settings → API Key). Source: https://docs.sarvam.ai/conversations/api/introduction
- **Place a call:** `POST /v1/orgs/{org_id}/workspaces/{workspace_id}/outbounds` with `app_config` (`app_id`, `app_version`, `connection_config: {connection_id, agent_phone_number}`, `agent_variables`, `app_overrides: {initial_language_name}`), `user_config: {user_phone_number}`, `webhook_config: {url, metadata}` → `{attempt_id}`. Source: https://docs.sarvam.ai/conversations/api/instant-outbound/create
- **Result:** Sarvam POSTs once per attempt to our URL: `attempt_id`, `status` (connected / no_answer / busy / failed), `duration`, `interaction_id`, `failure_reason`, `final_agent_variables`, `webhook_config` (our metadata echoed back), `interaction_transcript` (`role`, `en_text`). Source: https://docs.sarvam.ai/conversations/api/instant-outbound/webhook-payload
- **No webhook signature is documented**, so SpiroBuddy puts a secret in the URL (`?token=…`) and only accepts attempts it placed itself.
- **Keypad (DTMF) input is still "planned"** at Sarvam → the patient answers by speaking. Source: https://docs.sarvam.ai/conversations/build/run-time
- Variables: input variables come from the call request; output variables (String or Enum) are extracted by the AI after the call. Source: https://docs.sarvam.ai/conversations/build/variables-personalization
- Numbers: rent from Sarvam (KYC first, Individual or Corporate) or bring Exotel/Twilio/Vobiz/Plivo. Sources: https://docs.sarvam.ai/conversations/deploy/telephony , https://docs.sarvam.ai/conversations/deploy/telephony/rent-from-sarvam
- Price ₹3.50/min: https://www.sarvam.ai/epoch/summary

### 5.2 Set it up, click by click
1. Open https://apps.sarvam.ai (Voice Agents) and sign in with the same account as your Sarvam API key.
2. **Settings → API Key** → create a key → copy it into `.env` as `SARVAM_AGENT_API_KEY=`.
3. Look at the browser address bar (or Settings): copy the **org id** and **workspace id** into `SARVAM_ORG_ID=` and `SARVAM_WORKSPACE_ID=`.
4. **Create an agent** (name: "SpiroBuddy check-in"). Languages: the ones you will demo (Hindi + English at least).
5. **Variables tab → Input variables** – add exactly these (all text): `patient_id`, `patient_name`, `language`, `missed_slots`, `callback_number`. Turn off "send to LLM" for `patient_id` and `callback_number`.
6. **Output variables** – add:
   - `reason_category` – **Enum**: `pain, breathing, cough, tired_unwell, forgot, busy_away, device_problem, feeling_fine, other`. Prompt: "Why the patient missed the breathing exercise, from their own words."
   - `patient_words` – **String**. Prompt: "The patient's own words about why they missed it or how they feel, in English, as close to verbatim as possible. Do not add anything."
   - `callback_requested` – **Enum**: `yes, no`. Prompt: "Did the patient ask for, or agree to, a call back from the nurse?"
   - `sentiment` (optional) – **Enum**: `positive, neutral, negative`.
7. **Instructions (paste and adjust):**
   > You are SpiroBuddy's automated care assistant calling from the hospital. Start every call with: "Namaste, this is SpiroBuddy's automated care assistant, calling from the hospital." Speak slowly, warmly and simply, in @language. Address the patient as "@patient_name ji". Say: "We noticed you missed your breathing exercise @missed_slots times. Are you okay, and would you like to tell me why?" Ask ONE question at a time. Listen to the answer and thank them. Never diagnose, never name an illness, never suggest a medicine, never say a symptom is fine. If they mention pain: "Thank you for telling me. I will pass that to your care team. If the pain is severe, new, or you feel breathless, please seek urgent help." Then ask: "Would you like your nurse to call you back? Please say yes or no." If they mention chest pain, difficulty breathing, fainting, bleeding, confusion or an emergency, say exactly: "Please contact your nurse now. If it's an emergency, call 112. I am telling your nurse right away." and end the call. End with: "Please try ten slow, deep breaths when you can. Goodbye." Keep the call under 2 minutes.
8. **Publish** the agent. Copy its **app id** (in the address bar / agent settings) into `SARVAM_AGENT_ID=` and the published **version number** into `SARVAM_AGENT_VERSION=`.
9. **Phone number:** Deploy → **Phone Numbers → Add Connection → Rent from Sarvam** → choose Individual or Corporate → complete **KYC** (can take time – start early) → **Buy Number**. Open the "Sarvam Vobiz" connection: copy the **connection id** into `SARVAM_CONNECTION_ID=` and the number (with +91) into `SARVAM_AGENT_NUMBER=`. *(Not verified yet: exactly where the dashboard shows the connection id – if you can't find it, ask Sarvam support.)*
10. In `.env` set `SARVAM_WEBHOOK_SECRET=` to any long random text (e.g. `sb-7f3k9q2m8x`), `PUBLIC_BASE_URL=https://<your-app>.onrender.com`, and `DEMO_PATIENT_PHONE=+91…` (the presenter's phone, with their consent).
11. Restart the server. On the demo panel the line should say **"AI check-in calls: Sarvam Voice Agent (live)"**. `GET /api/comms/status` lists anything still missing under `sarvam_agent_missing`.

### 5.3 Rehearse (do this the day before)
1. In the Sarvam dashboard, test the agent in its **web test** first (talk to it in the browser).
2. Demo panel → choose Ravi → **🗣 AI check-in call now**. The presenter's phone rings from the Sarvam number.
3. Say: "I had mild pain near the incision this morning." Then "Yes, please call me."
4. Within a few seconds of hanging up, the patient page shows **"⚠ Nurse review requested"** with the neutral note, and the Alerts inbox has a "Check-in call note". Until Sarvam's result arrives it shows "call completed; result pending".
5. Try once more saying "I can't breathe properly" → **RED FLAG**, red alert, family told.
6. **Backup:** if the live call doesn't connect within a few seconds, switch to the browser phone (same story), or press **⏯ Replay saved Sarvam result** – it feeds a saved real-format result through the same code.

---

## 6. Exotel – Indian caller ID for keypad calls (production path)

Exotel gives an Indian "ExoPhone" so calls don't show a foreign number. **Needs an Indian registered business and KYC (1–3 business days).** No public per-minute price.
1. Sign up at https://exotel.com, finish KYC, get an ExoPhone.
2. Dashboard → API settings: copy SID, API key, API token into `EXOTEL_SID`, `EXOTEL_API_KEY`, `EXOTEL_API_TOKEN`; the ExoPhone into `EXOTEL_CALLER_ID`.
3. **App Bazaar → create a flow:** Greeting (dynamic text, URL `…/api/comms/exotel/greeting`) → Gather (dynamic URL `…/api/comms/exotel/gather`) → Passthru (`…/api/comms/exotel/passthru`) → Hangup. Copy the flow's app id into `EXOTEL_APP_ID`.
4. Set `PUBLIC_BASE_URL`, restart. Status should show "Exotel (Indian caller ID)".

---

## 7. Webhook addresses when hosted on Render

Set `PUBLIC_BASE_URL=https://<your-app>.onrender.com` in Render → Environment. Then:

| Who calls us | URL |
|---|---|
| Sarvam result (sent automatically with each call) | `https://<app>/api/comms/webhooks/sarvam?token=<SARVAM_WEBHOOK_SECRET>` |
| Twilio WhatsApp "when a message comes in" | `https://<app>/api/comms/webhooks/whatsapp` |
| Twilio WhatsApp status (optional) | `https://<app>/api/comms/webhooks/whatsapp/status` |
| Twilio voice (set automatically per call) | `https://<app>/api/comms/twilio/voice/<call id>`, `/gather/…`, `/status/…` |
| Exotel flow applets | `https://<app>/api/comms/exotel/greeting`, `/gather`, `/passthru`, `/status/<call id>` |

Render's free disk is temporary: in demo mode the data re-seeds on restart. Use Supabase (`DATA_BACKEND=supabase`) to keep call results.

---

## 8. Settings (`.env`)
All are listed with comments in `.env.example` (comms block). The important ones:

| Variable | Meaning |
|---|---|
| `CALL_PROVIDER` | `auto` (default), `twilio`, `exotel`, `sarvam_agent` or `dry_run` |
| `TWILIO_*`, `TWILIO_VOICE_FROM` | Twilio WhatsApp + voice (section 4) |
| `EXOTEL_*` | Exotel (section 6) |
| `SARVAM_AGENT_API_KEY`, `SARVAM_ORG_ID`, `SARVAM_WORKSPACE_ID`, `SARVAM_AGENT_ID`, `SARVAM_AGENT_VERSION`, `SARVAM_CONNECTION_ID`, `SARVAM_AGENT_NUMBER`, `SARVAM_WEBHOOK_SECRET`, `SARVAM_CALLBACK_NUMBER` | Sarvam Voice Agent (section 5) |
| `PUBLIC_BASE_URL` | Our internet address; without it no real call is placed (providers can't send results back) |
| `DEMO_PATIENT_PHONE`, `DEMO_GUARDIAN_PHONE`, `DEMO_NURSE_PHONE`, `NURSE_DESK_PHONE` | Team phones that stand in for the fake people |
| `QUIET_HOURS` | Default `21:00-07:00` (IST) |
| `COMMS_TICKER`, `COMMS_AUTO_ESCALATE`, `COMMS_CONSENT_RENEWAL` | Background ladder, automatic ladders, weekly consent question (1/0) |

---

## 9. Costs (₹, Oct 2026)

| Item | Cost |
|---|---|
| WhatsApp utility message in India (Meta) | ₹0.115 per message, plus Twilio's fee of $0.005 (under half a rupee) |
| 14 WhatsApp reminders a day | about ₹1.6 per patient per day (Meta fee) + Twilio fee |
| Sarvam AI check-in call | ₹3.50/min → a 2-minute call ≈ ₹7–8 |
| Sarvam rented number | shown in the catalogue; 30-day rental from the Sarvam wallet |
| Plivo (alternative Indian provider) | ₹0.38/min (30-second pulses) + ₹200/month per Indian number |
| Exotel | no public price; KYC 1–3 business days |
| Twilio trial | free credit, ~75 voice minutes, 5 verified numbers |
| SMS | not used (needs DLT registration by an Indian company, 1–3 weeks) |

Plivo, Exotel and Sarvam-rented numbers all need KYC; Plivo and Exotel need an Indian registered business.

---

## 10. Demo script (2 minutes)
1. Open **Demo panel**. Pick **Ravi Kumar ★**. Set **Patient's call → 🗣 AI conversation**.
2. Press **▶ Play escalation ladder**. Say: "Time is fast-forwarded – one minute is one hour."
3. The device beeps, the WhatsApp reminder appears on Ravi's phone, then his phone rings. Tap ✆.
4. The assistant introduces itself as automated and asks one question. Tap 🎤 and say "I had mild pain near the incision this morning" (or tap that answer). Then "Yes".
5. Show the result card: "Nurse review requested" – the nurse note uses Ravi's own words and does not diagnose.
6. Open the **Dashboard** → Alerts inbox → "Check-in call note". Acknowledge it.
7. Optional: the red-flag path ("I can't breathe properly"), or open the **Family page** (giant text, Call Papa, cheers, quiet hours).
8. If anything fails: **⏯ Replay saved Sarvam result**.

---

## 11. Tests and troubleshooting
- Run: `.venv\Scripts\python.exe -m pytest tests\test_comms.py -q` (no keys needed, temporary database).
- "WhatsApp send failed – rejoin needed": send `join <code>` again from that phone (section 4, step 7).
- "Real call failed (twilio) – would call": usually a trial limit (unverified number) or India not enabled in Geo permissions. The call rings in the simulator instead, so the demo continues.
- "Sarvam call failed": check `GET /api/comms/status` → `sarvam_agent_missing`, the credit balance, and that the number is active. The simulator rings instead.
- AI check-in shows "call completed; result pending" for long: Sarvam's webhook didn't reach us – check `PUBLIC_BASE_URL`, the `?token=` secret and Sarvam's webhook delivery list (dashboard). Use the replay button meanwhile.

## 12. Not done yet / limits
- Real Twilio / Exotel / Sarvam calls not tried with real keys (no accounts yet).
- Where the Sarvam dashboard shows the connection id and app id is not documented on the pages read; ask Sarvam support if unclear.
- Hindi and Tamil call wording is hand-written – a native speaker should read it once (same as docs/VOICE.md).
- Simulator AI conversation lines exist in English, Hindi and Tamil; other languages fall back to English text in the simulator (the real Sarvam agent speaks all its languages).
- Live transfer to a nurse during an AI call (Sarvam "call transfer") is not wired; the nurse gets an alert and calls back.
