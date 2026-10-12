# Call demonstration verification — 12 October 2026

Read-only source review and isolated tests. No browser session, real provider, production patient, outbound call or deployment was used for this review. Findings describe the source inspected before any subsequent fixes by other workers.

## Actual screens and API paths

- `/demo.html` loads `web/js/phone-sim.js`, mounts `SB.commsDemo` and shows the patient/family browser phones. The **AI check-in call – optional, where consent allows** button calls POST `/api/comms/checkin-call/{pid}`. `/demo.html` itself also has **Simulate 2 missed slots**; that marks demo missed state, separately from placing a call.
- `/patient.html?id=1` has the care-circle/consent controls and the staff AI check-in trigger through `web/js/comms-patient.js`.
- `/dashboard.html` is the actual nurse alerts inbox via `web/js/comms-dashboard.js`. There is no `web/comms-dashboard.html` in the current checkout.
- Browser Answer → tap a prepared reason or speak → POST `/api/comms/calls/{cid}/agent-turn`; one reason then callback preference. Fixed application rules normalize the outcome and write the note/alert.
- **Replay saved Sarvam result** uses POST `/api/comms/demo/sarvam-replay/{pid}`. It feeds a stored fixture through the webhook handler; it is not a real Sarvam call or proof of recent provider integration.

## Safety findings requiring fixes before live operation

1. `backend/app/comms/common.py:182` `resolve_number` returns the valid stored number first, then a demo route fallback. It does **not** force a team number when `DEMO_MODE=1`. `e164` at line157 rejects X placeholders but accepts numeric all-zero sample numbers. Therefore documentation saying all demo calls always go to team phones is stronger than the current code. Never enable a live provider across sample data until mandatory routing/allowlisting is implemented and tested.
2. `backend/app/comms/sarvam.py:130` callback ending promises a nurse call “soon” and urges ten breaths. Line135 also urges breaths, including after a pain concern. Equivalent Hindi/Tamil translations need the same repair. Replace with neutral acknowledgement and callback-request language; do not coach exercise after reported distress.
3. `backend/app/comms/calls.py:53` `provider` honors `CALL_PROVIDER=dry_run` for check-in calls too. Use this setting for rehearsals even if Sarvam agent credentials exist. With `auto` and complete agent configuration, clicking the same button can attempt a live call.
4. `backend/app/routes_comms.py:395` direct `checkin_call` checks recorded consent and freshness but does not itself apply quiet-hour holding. Demo ladder quiet-hour checkbox controls the ladder route, not necessarily this direct button. Keep direct calls simulated during quiet hours.
5. Defaults include `COMMS_AUTO_ESCALATE=1`; source `backend/app/comms/escalation.py:474` gates automatic ladder launch. Disable autonomous escalation during controlled setup. A live provider plus valid existing stored phone/consent may create communications beyond the one visible demo interaction.

Root was informed of these findings before any live provider attempt. The review does not establish that later repairs are present or tested.

## Reproducible 40-second simulator recording

Use the existing isolated local sample database, `DEMO_MODE=1`, `CALL_PROVIDER=dry_run`, blank real messaging/voice-provider credentials, `COMMS_AUTO_ESCALATE=0`. Do not reset a shared/live database. Log in through the demo staff login and select one sample patient with recorded automation consent; otherwise record consent for the fictional demonstration in Care circle settings. Verify provider status says dry run.

1. **0–8 seconds:** `/demo.html`, select the same patient in the sample card and calls panel. Click **Simulate 2 missed slots**, show the labelled sample missed state. Caption: “Sample patient — simulated missed sessions.”
2. **8–24 seconds:** Click **AI check-in call – optional, where consent allows**. Answer the patient browser phone. Tap a prepared reason, then callback preference; use **forgot** for a non-distress scenario until unsafe endings are repaired. Speak-over can explain that the assistant gathers the reason; tapping is visibly a simulator input, not a live telephone transcript.
3. **24–35 seconds:** Show the actual generated note and switch to `/dashboard.html` to review the corresponding nurse alert if a callback was requested. Claim only the alert actually shown; ordinary “forgot” without callback may produce an OK result and no nurse-review alert.
4. **35–40 seconds:** End on the neutral note/inbox. Caption: “Simulated conversation; sample data; nurse review remains a human action.”

The longer ladder can be demonstrated separately with **Play escalation ladder (≈60 s)** and **Next step**. At 21:00–07:00 IST, keep the rehearsal dry run; unchecking **Respect quiet hours** fast-forwards the demo ladder only. Do not use that bypass to place real calls. Avoid red-flag/family-message controls while any live communications credentials are active.

Browser speech/STT availability and screenshots were not verified by this worker. Tapped answers avoid microphone permission/provider setup as a reliable fallback. Do not splice Sarvam Test Agent footage and fixture replay into a purported end-to-end live call.

## Tests

Focused isolated command (provider `_post` mocked by Sarvam tests):

```text
.venv\Scripts\python.exe -m pytest tests/test_comms.py -q -k "sarvam or simulated_conversation or replay or consent or quiet_hours or normalise_pain or red_flag_is" --tb=short
```

Result: **20 passed, 25 deselected in 98.09 seconds**. Relevant existing coverage checks request construction, secret rejection, unknown attempts, duplicate webhook handling, failure-to-simulator fallback, pain/red-flag normalization, simulated conversation, replay modes, missing/lapsed consent and quiet-hour ladder behavior. These do not prove live network connectivity or mandatory demo-number override.
