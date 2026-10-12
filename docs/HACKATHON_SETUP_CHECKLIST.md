# Hackathon setup checklist — 12 October 2026

Core registration, manual prescribing, patient medicines and simulated breathing/OTP work without a paid AI or communications provider. The important setup is persistent storage and access to the existing deployment; Gemini is the first optional enhancement.

| Priority | Sign in / open now | What to prepare | Configuration / completion check |
|---|---|---|---|
| 1 | [Render dashboard](https://dashboard.render.com/) → existing **spirobuddy** service → Environment | Access to the account already hosting the app. Do not create a duplicate service. | Keep `DEMO_MODE=1`, `DATA_BACKEND=supabase`, `TZ_NAME=Asia/Kolkata`. Confirm the existing database variables are present without copying values into chat. Coordinate one environment/deployment update with Codex after the tested build is ready. |
| 1 | [Supabase dashboard](https://supabase.com/dashboard) → existing project → Settings → Data API / API Keys; SQL Editor | Existing project's URL and backend `service_role` key. Keep the same project and existing data. | Server variables: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`. This app expects the backend service-role credential, never a browser anon/publishable key. Verify the additive `supabase/schema_v2.sql` migration against the existing schema, including `patients.pin_hash`; apply only missing additions after review. Do not run seed/reset/delete operations. |
| 2, optional | [Google AI Studio API keys](https://aistudio.google.com/apikey) | Create a Gemini API key in your own Google project if you want the notepad-to-draft demonstration. | Set backend `GEMINI_API_KEY`; retain `GEMINI_MODEL=gemini-3.1-flash-lite`, `GEMINI_TIMEOUT_S=30`, `AI_DAILY_LIMIT=300`, `AI_PER_IP_HOUR=20`. The hospital AI setting must permit use and that patient's latest consent must permit AI; a key alone does not bypass these checks. Verify using fictional text, then review every proposed prescription field before issue. Manual entry remains available. |
| 3, optional | [Sarvam dashboard](https://dashboard.sarvam.ai/) | Existing Sarvam API subscription key if improved Indian-language voice is useful. | Set backend `SARVAM_API_KEY`. Repository defaults: `SARVAM_TTS_MODEL=bulbul:v3`, `SARVAM_STT_MODEL=saaras:v4`, `SARVAM_TRANSLATE_MODEL=mayura:v1`, `SARVAM_TIMEOUT_S=25`. Account/model availability and voice quality still require a sample check; browser/recorded voice fallbacks remain available. This key does not provision a telephone voice agent. |
| Later, optional | [Twilio console](https://console.twilio.com/) | Only if already provisioned: credentials, permitted sender and consenting team test numbers. | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_FROM`; calls additionally need `TWILIO_VOICE_FROM`. Existing communications configuration uses `PUBLIC_BASE_URL=https://spirobuddy.onrender.com`, signature checks and team-routing/consent controls. Sender onboarding, trial restrictions and webhooks need separate verification. Do not spend submission time purchasing/provisioning telephony. |

## What credentials cannot finish today

- **Real patient SMS OTP:** the current patient OTP module is explicitly simulated; there is no SMS delivery adapter. A Twilio key will not make these OTPs arrive on a phone. Keep the simulated label and demonstrate the displayed sample code in demo mode.
- **Physical SpiroBuddy readings:** API keys do not provide the laser sensor, firmware, calibration or authenticated device transport. Browser/demo readings remain labelled accordingly.
- **Closed-app phone reminders:** current medication voice reminders require the page to be open, visible and opted in. Push notifications require additional implementation.
- **Optional advanced integrations:** Exotel KYC, Sarvam outbound agents and Anthropic summaries are not requirements for the core submission. Leave their environment entries blank unless already configured and separately tested.

## Do now, then hand back

1. Sign into Render and Supabase, and optionally AI Studio/Sarvam. Keep those tabs available for your own input.
2. Prepare key values privately. Enter them directly into the backend's environment settings or your local ignored `.env`; never into chat, frontend JavaScript, screenshots, slide decks or committed files. Do not rotate an existing database key during this submission unless required.
3. Tell Codex only which services are ready, for example: “Render and Supabase ready; Gemini key configured; Sarvam skipped.” No credential values are needed.
4. Coordinate the final environment save with the tested deployment. Render offers save/deploy choices; a rebuild/deploy choice restarts the service. Avoid repeated restarts while parallel work is being verified. Gemini free-tier access/quotas vary by project; application limits do not guarantee provider quota. Paid billing is optional and should only be enabled deliberately.
5. After deployment, verify [health](https://spirobuddy.onrender.com/api/health), [staff login](https://spirobuddy.onrender.com/login.html) and [patient login](https://spirobuddy.onrender.com/patient-login.html). New local pages may be absent from the old live build until deployment. `/api/health` alone is not proof that storage, provider keys or every flow works.

## Source of these requirements

Repository: `.env.example`, `render.yaml`, `backend/app/config.py`, `backend/app/ai_gemini.py` (`ai_allowed`), `backend/app/patient_otp.py`, `supabase/schema_v2.sql`, `docs/VOICE.md`, `docs/COMMS.md`.

Official references checked: [Render environment variables](https://render.com/docs/configure-environment-variables), [Supabase API key types](https://supabase.com/docs/guides/getting-started/migrating-to-new-api-keys), [Gemini key creation](https://ai.google.dev/gemini-api/docs/api-key), [Gemini model ID](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite), [Sarvam authentication](https://docs.sarvam.ai/api-reference/authentication). Provider calls and credentials were not tested by this checklist author.

The older `docs/SETUP_STEPS.md` contains stale advice: do not use its reset-demo instruction on retained data, its unverified alternate model example, or its promise that free quota cannot run out. Use this checklist for the current submission.
