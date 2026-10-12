# Sarvam follow-up call and demo video setup

Updated 12 October 2026. The account and agent setup below have progressed, but **no telephone call or application webhook integration has been verified**. The remaining checklist and API limitations still apply.

## Actual setup status

| Item | Verified status |
|---|---|
| Sarvam account | User-authorized Google sign-in to the Indus console completed. |
| Agent | **SpiroBuddy check-in** version 2 committed after its corrected greeting was verified in a real provider Chat test. Render's saved agent version is 2. No telephone configuration is verified. |
| Provider conversation | Sarvam's real provider **Chat** test accepted a sample report of forgetting the exercise plus an explicit callback request, and ended neutrally. This was a dashboard conversation, not a telephone call. |
| Extraction and application integration | Output-variable extraction, outbound calling, matching result webhook delivery and the application's nurse-inbox handoff remain unverified. |
| Telephony | No phone connection configured. The rental dashboard showed **₹59 promotional rental**, **₹159 standard renewal**, and **₹0.20 per 30 seconds telephony**. These are observed account-screen prices; eligibility and checkout terms still control. KYC is pending. No number rental, purchase or recharge completed. |
| Voice Agents API key | User approved creation; a new Voice Agents API key was created and saved to Render with organisation/workspace/agent settings and version 2, using **Save only**. CALL_PROVIDER is saved as dry_run for the user's selected browser/simulator demonstration. Credentialed outbound API access is still untested; no redeploy or phone connection is implied. |
| Gemini | A real SDK test succeeded using **`gemini-3.1-flash-lite`**. Render environment changes were retained with **Save only**; no redeploy occurred. This SDK result does not establish that the deployed website is already using the updated configuration. |

The safe submission claim is **“Sarvam agent conversation tested in the provider dashboard; telephone and hospital webhook integration pending.”** Keep the application simulator/replay clearly labelled until the full live acceptance sequence below succeeds. Do not expose credentials, phone numbers or callback tokens in recordings.

## Immediate account steps

Continue in [Sarvam Voice Agents](https://indus.sarvam.ai/) with the existing **SpiroBuddy check-in** agent. Current official [quickstart](https://docs.sarvam.ai/conversations/quickstart) uses this console; older repository instructions use `apps.sarvam.ai`. Review the draft greeting/instructions and English plus the language you will actually demonstrate, then test before committing another version or attempting telephone deployment.

In Settings → Billing, check that the reported **90 credits** belong to the selected organisation. Sarvam documents one balance shared by its products/workspaces; that does not prove a phone connection or outbound permission already exists. [Billing reference](https://docs.sarvam.ai/api/platform/billing).

The [published overview](https://docs.sarvam.ai/conversations/why-voice-agents) lists pay-as-you-go agent usage at ₹3.50/minute, a ₹59/30-day number example and ₹2 simulated tests. Telephony is separate. If the dashboard confirms ₹90 usable balance and a ₹59 eligible rental, the arithmetic leaves ₹31 before calls/other charges; this is **not a price quote or purchase instruction**. With an existing phone connection, no new rental may be needed. Keep auto-recharge off for a bounded hackathon demonstration unless the account owner deliberately chooses otherwise.

Phone setup is the main potential blocker. [Rent from Sarvam](https://docs.sarvam.ai/conversations/deploy/telephony/rent-from-sarvam) requires approved Individual/Corporate KYC, then a paid wallet rental. Catalog prices control; rental auto-renews after 30 days. Alternatively connect already-owned supported telephony. Do not promise KYC completion within the submission window. If absent, demonstrate browser voice and clearly label the telephone flow simulated.

## Exact existing application configuration

Set these only in backend environment settings, privately; do not paste credentials into chat or frontend code. Coordinate one final Render environment update with the tested build.

| Variable | Required value/source |
|---|---|
| `SARVAM_AGENT_API_KEY` | Voice Agents Settings → API Key; adapter falls back to `SARVAM_API_KEY`, but confirm that key has agent access. |
| `SARVAM_ORG_ID`, `SARVAM_WORKSPACE_ID` | Selected organisation/workspace identifiers from dashboard URL/settings. |
| `SARVAM_AGENT_ID` | Published agent's app ID, not its display name. |
| `SARVAM_AGENT_VERSION` | Published integer version; default `1` is only correct if that version exists. |
| `SARVAM_CONNECTION_ID` | Existing live phone connection identifier. |
| `SARVAM_AGENT_NUMBER` | Number attached to that connection, E.164 including `+91`. |
| `PUBLIC_BASE_URL` | `https://spirobuddy.onrender.com` for deployed callback reachability. |
| `SARVAM_WEBHOOK_SECRET` | Long random private value; app places it in the callback URL token. Never show that URL in the video. |
| `DEMO_PATIENT_PHONE` | Consenting presenter's real test number, E.164. Never route to fictional sample numbers. |
| `SARVAM_CALLBACK_NUMBER` | Verified team/nurse callback number; falls back to `NURSE_DESK_PHONE`. Do not promise an unavailable clinical service. |
| `SARVAM_AGENT_API_BASE` | Keep default `https://apps.sarvam.ai/api/outbounds`. |
| `SARVAM_TIMEOUT_S` | Existing default `25` seconds. |
| `DEMO_MODE` | Keep `1` for sample-data demonstration. Existing consent, phone-routing and quiet-hour checks still apply. |

Logged-in staff can inspect `/api/comms/status` and its `sarvam_agent_missing` list. Empty missing configuration means fields are present; it is not proof of valid credentials, telephony access or completed calls. Keep autonomous communications disabled during setup if no controlled test is intended (`COMMS_AUTO_ESCALATE=0`; preserve the original value for later deliberate restoration).

## API compatibility findings and remaining verification

Source inspected: `backend/app/comms/sarvam.py`: `missing`, `_post`, `build_request`, `webhook_url`; existing `docs/COMMS.md` section 5.

The current official [API introduction](https://docs.sarvam.ai/conversations/api/introduction) still specifies `X-API-Key` and the `apps.sarvam.ai/api/outbounds` base. [Create outbound](https://docs.sarvam.ai/conversations/api/instant-outbound/create) still uses POST `/v1/orgs/{org_id}/workspaces/{workspace_id}/outbounds`, app configuration with app ID/version/connection, recipient configuration, and returns `attempt_id`. These core fields match the existing adapter; the console-domain change does not imply a REST-base change.

The adapter additionally sends `app_config.agent_variables`, `app_config.app_overrides.initial_language_name`, and callback metadata. Their nested schemas were collapsed in the readable official page; **acceptance of these optional fields has not been independently live verified**. Do not claim full provider compatibility before a real response. A 422 response needs schema validation, not blind retries.

The documented [result webhook](https://docs.sarvam.ai/conversations/api/instant-outbound/webhook-payload) still contains attempt/status, final variables and agent/user English transcript turns, consistent with application normalization. The app callback is `/api/comms/webhooks/sarvam?token=<private secret>` and correlates placed attempts. No provider webhook signature was established by this review. Verify callback delivery and nurse alert creation before calling the integration live.

## Agent inputs, outputs and safe prompt

Define input text variables matching the adapter: `patient_id`, `patient_name`, `language`, `missed_slots`, `callback_number`. Use the builder's variable chips rather than assuming typed `@variable` syntax expands.

Output variables: `reason_category` enum `pain, breathing, cough, tired_unwell, forgot, busy_away, device_problem, feeling_fine, other`; `patient_words` text preserving only the patient's stated reason; `callback_requested` enum `yes, no`. Do not manufacture an answer when unclear. Publish after testing.

Use this prompt for the fictional, consenting-team demonstration:

> You are SpiroBuddy's automated follow-up assistant in a hospital-software demonstration. Clearly disclose that you are an automated assistant. Speak slowly in the configured language. Say: “Hello, this is SpiroBuddy's automated follow-up assistant. Our demo record shows a missed scheduled breathing session. Is now a suitable time for a short check-in?” If no, thank them and end. Ask one question at a time: “Would you like to tell me why the session was missed?” Listen and capture only their words. Say: “Thank you. Would you like the care team to call you back?” If yes, record that request without promising a callback time. Do not diagnose, change medicines, suggest doses, tell them symptoms are harmless or recommend exercise. If they report urgent symptoms or an emergency, tell them to contact their care team or local emergency service immediately and end the routine check-in. Do not continue coaching breaths. End: “Thank you. I will pass your response to the demo care-team inbox. Goodbye.” Keep the call under one minute. Do not request sensitive identity details.

For future real deployment, replace demo identity with an approved hospital identity and clinically reviewed escalation wording. The older `docs/COMMS.md` prompt ends with “try ten slow, deep breaths”; do not use that ending after reported pain/distress.

## Controlled rehearsal and 40-second video

Record only sample data and a consenting team speaker. Exclude keys, environment panels, full phone numbers and webhook tokens.

| Time | Screen/action | Narration |
|---|---|---|
| 0–8s | Sample patient's missed-session state; show the explicitly labelled demo trigger. | “A missed scheduled session is flagged for follow-up.” |
| 8–23s | Show a browser simulation, or a verified live team-phone call only after successful rehearsal. Speaker says: “I forgot this morning. Yes, please ask the team to call me.” | “The automated assistant asks for the patient's reason and callback preference.” |
| 23–35s | Nurse inbox, actual generated neutral note and callback request; acknowledge as the logged-in nurse. | “The response reaches the nurse for review.” |
| 35–40s | Close on patient/team workflow; retain mode label. | “Patient guidance and staff follow-up share one record.” |

Keep **“Simulated call — sample patient”** visible for a simulator/replayed webhook. If using Sarvam Test Agent plus a separately replayed application result, label both separately; don't edit them to imply a verified provider callback. Use **“Live Sarvam call — consenting team test”** only when the app placed the call and received its matching result. A dashboard-only conversation does not prove hospital integration.

Acceptance for a live claim: app request returns a tracked attempt; only the approved test phone rings; assistant discloses automation; result arrives through the configured callback; inbox shows the patient's stated reason; duplicate callback does not duplicate alerts. Retain the simulated fallback if any step fails. No real patient outcomes or automatic clinical decisions should be claimed.
