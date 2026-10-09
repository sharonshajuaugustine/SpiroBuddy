# Sarvam Calls and InSee Feasibility for SpiroBuddy

**Research date:** 9 October 2026  
**Decision:** build the missed-session call as a controlled demo. Keep the existing browser-phone path as the guaranteed presentation route, and add a real Sarvam outbound call only after the account, KYC, number and Indian calling rules are verified. InSee is a real FDA-cleared competitor, but its public evidence describes a hospital-only accessory for two AirLife models, not SpiroBuddy's multilingual home-recovery workflow.

## 1. Executive verdict

### Can the proposed call demo work without sensor hardware?

Yes. The hardware is not needed for this story. SpiroBuddy already has the software events that matter:

1. Two elapsed sessions are marked missed.
2. The escalation engine changes the patient to red / needs-a-call.
3. A call is created through the configured provider.
4. If real telephony is unavailable, the browser phone simulator plays the same flow.
5. The patient's answer is stored as a neutral note and shown to the nurse.

The clean judge-facing flow is:

> Ravi misses two scheduled sessions → SpiroBuddy triggers a check-in → the patient's phone rings → the agent asks why → Ravi says, “I had mild pain near the incision” → the system records the patient's own words, creates a conservative nurse-review note, and flags the nurse → no diagnosis is made.

### How much can be built in one day?

| Scope | One-day feasibility | Recommendation |
|---|---:|---|
| Existing browser call simulator and fast-forward ladder | Already present | Make this the guaranteed demo |
| Sarvam agent in its web test interface | High | Configure and rehearse first |
| A live call to one verified Indian number | Medium | Attempt only after account/KYC/number setup |
| Webhook that writes outcome and note into SpiroBuddy | Medium | Use a small, fixed schema and test with saved payloads |
| Safe red-flag routing and nurse alert | High | Use deterministic rules, not free-form medical advice |
| Live transfer to one nurse number | Medium | Supported on Sarvam-rented/Vobiz or Plivo; rehearse on a real phone |
| Simultaneously ring several nurses | Not a native Sarvam transfer feature found | Use a PBX/SIP ring group later, or sequential escalation |
| Production-ready Indian automated calling | No | Requires consent, provider/KYC and regulatory work |

## 2. What is already in SpiroBuddy

The current repository is farther along than the earlier plan implies:

- `POST /api/demo/miss` marks the last two elapsed slots missed and creates the red state.
- The escalation engine triggers after the configured number of consecutive missed slots (default: two) and respects quiet hours.
- The communications layer supports dry-run, Twilio and Exotel providers.
- Real-call failure falls back to the browser phone simulator.
- The demo ladder can fast-forward device reminder → WhatsApp → call → guardian → nurse in about a minute.
- The demo page already has patient and guardian phone simulators, a live communications feed, red-flag state, voice-note handling and call outcomes.
- Click-to-call rings the nurse first and then bridges the patient, so neither party needs to expose a personal number.
- Patient responses such as done, snooze and callback request are already logged and can create nurse alerts.

This means Sarvam should be integrated as another communications provider / agent layer, not allowed to process raw laser readings. Breath measurement and safety rules remain deterministic in SpiroBuddy.

## 3. Recommended architecture

```text
Simulator or sensor
       |
       v
SpiroBuddy session + missed-slot rules
       |
       +---- normal dashboard / WhatsApp escalation
       |
       v
Call job: patient, language, missed slots, safe context
       |
       v
Sarvam Voice Agent + rented/BYO provider number
       |
       +---- speaks/listens in the patient's language
       +---- optional API tool during call
       +---- one-number human transfer when configured
       |
       v
On-end webhook / output variables
       |
       v
Transcript reference + structured outcome + neutral note
       |
       v
Nurse dashboard alert and audit timeline
```

The caller ID is the number rented through Sarvam or connected from Exotel, Twilio, Smartflo, Pulse, Intalk, Vobiz or Plivo. It is **not** the nurse's personal phone. Sarvam says renting a number is the fastest route when no provider account already exists.

## 4. Sarvam capability and limits

### Confirmed capabilities

- Inbound and outbound telephony, plus web, API and SDK channels.
- A hosted real-time speech-recognition → language-model → speech-synthesis loop.
- Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, Assamese and English, including code-mixed speech.
- Input variables from phone metadata, a start hook, or outbound campaign rows.
- Output variables extracted after the call; String and Enum are documented.
- API tools can read/write variables during the call.
- An end hook or outbound webhook can send the final variables and outcome back to SpiroBuddy.
- Transcripts, recordings, connectivity, outcomes and analytics are available in the platform/API.
- Real phone transfer to one PSTN number or SIP URI. Sarvam-rented numbers use Vobiz and support self-serve transfer; Plivo also supports it. Other providers may require Sarvam support.
- Browser voice/chat testing cannot validate call transfer; transfer must be tested on a real call.

### Pricing and free access

- Sarvam's current launch page states **₹3.50 per minute** for Voice Agents, including authoring, simulation, phone numbers, evaluation and analytics.
- New accounts receive **₹100 of free universal credit** according to the credits documentation. That is enough for roughly 28 minutes at the stated Voice Agent rate if all of it can be applied to Voice Agents; verify the balance and product eligibility in the account before the demo.
- Model APIs are pay-as-you-go from the same credit balance. Sarvam lists real-time/streaming TTS at ₹3 per 1,000 characters and STT at ₹30 per hour.
- Renting a real number may require KYC and availability; do not promise instant activation until the account shows an active number.

### Concurrency and forwarding

- Sarvam documents a default limit of **10 concurrent active or scheduled campaigns**. This is a campaign-count limit, not proof that a starter account can run any particular number of simultaneous phone calls.
- The runtime page advertises enterprise scale beyond 20,000 concurrent calls, but actual account/provider concurrency must be verified in the plan.
- The documented call-transfer action chooses **one destination type and one destination value** per invocation: one phone number or one SIP URI.
- No official evidence was found for a native “ring several nurses at the same time” transfer. For that, transfer to a hospital PBX/SIP hunt group, or implement sequential escalation in SpiroBuddy.

### Important demo caveats

- Sarvam's current runtime documentation says broader DTMF/keypad productisation is planned. Use spoken answers for the demo rather than depending on “press 1/2/3.”
- Sarvam documents post-call **sentiment** extraction from the transcript, but no primary documentation was found for medically reliable, real-time emotion recognition from vocal tone. Treat sentiment as a soft operational signal, never as a clinical fact.
- Indian automated calls require a real consent and telephony-compliance path. Keep consent logging, quiet hours and an opt-out. Treat production rollout as work with an Indian telephony provider and legal/compliance review.
- A healthcare check-in agent must not diagnose, prescribe, minimise pain or claim an emergency is absent.

### Can it read emotion from the patient's voice?

Partly, but the distinction matters:

- Sarvam's official Call Analytics pipeline can label **sentiment** after a call by transcribing the recording and asking its language model to classify the words and conversation as positive, negative or neutral.
- A live Voice Agent can also react to explicit language such as “I am scared,” “the pain is worse,” repeated confusion, or a request for a nurse.
- The official material reviewed does not establish a dedicated, validated real-time model that reliably recognises emotions from acoustic features such as pitch, tremor or speaking rate alone.

For SpiroBuddy, use a label such as **possible distress — review call**, show low confidence, and require the nurse to confirm it. Never present “patient is anxious/depressed/in severe pain” as a fact inferred from voice. In the demo, the strongest and safest feature is to extract the patient's stated reason and red-flag phrases, with post-call sentiment as optional context.

## 5. Exact demo plan

### Five-minute setup before presenting

1. Put the presenter's mobile number in the demo patient record and record explicit demo consent.
2. Choose Malayalam, Hindi or another rehearsed language.
3. Keep the browser simulator open in a second tab even if a real number is ready.
4. Confirm the Sarvam number/connection and agent version are active.
5. Place one test call to the same phone from the same network and room.
6. Keep a saved webhook payload available so the dashboard result can be replayed if the external call fails.

### Live sequence

1. Show Ravi as on track.
2. Click the existing “miss two sessions” action; explain that time is being fast-forwarded.
3. Dashboard changes to “Needs a call.”
4. SpiroBuddy sends a single instant outbound request with Ravi's name, language, missed count and a short allowed context.
5. Phone rings from the configured service number.
6. Agent: “Ravi, we noticed you missed your breathing exercise. Are you okay, and would you like to tell me why?”
7. Presenter: “I had mild pain near the incision this morning.”
8. Agent acknowledges without diagnosing: “Thank you for telling me. I will pass that to your care team. If the pain is severe, new, or you feel breathless, please seek urgent help.”
9. Webhook writes structured values such as `outcome=needs_nurse_review`, `reason_category=pain`, `patient_words`, `callback_requested` and `red_flag`.
10. Nurse dashboard shows a neutral note: “Patient reported mild pain near the incision and missed two sessions. Nurse review requested.”

If the real call does not connect within a few seconds, switch immediately to the browser phone. The product story remains valid; only the transport changed.

## 6. Safety design for the care check-in

Do not call it a doctor, consultant or clinical decision-maker. Use **multilingual care check-in assistant**.

Store the patient's own words separately from any summary. The summary should use phrases such as “patient reported” and “nurse review requested.” Never convert “pain near the incision” into a diagnosis.

Use deterministic red-flag matching outside the language model. Examples include severe/worsening chest pain, severe breathlessness, fainting, blue lips, confusion, bleeding, or an explicit emergency request. When triggered:

1. stop routine coaching;
2. play the fixed emergency / contact-care-team wording;
3. create a high-priority nurse alert;
4. optionally offer transfer to the configured clinical number;
5. log exactly which rule fired.

Only collect the minimum data needed for follow-up. Obtain consent for calling and recording/transcription, define retention, restrict dashboard access and mask PII in analytics where possible.

## 7. Minimal integration contract

SpiroBuddy should send:

```json
{
  "patient_id": "demo-ravi",
  "phone": "+91...",
  "language": "Malayalam",
  "missed_slots": 2,
  "patient_name": "Ravi",
  "callback_number": "+91..."
}
```

The completed-call callback should be normalised to:

```json
{
  "provider": "sarvam",
  "status": "completed",
  "outcome": "needs_nurse_review",
  "reason_category": "pain",
  "patient_words": "I had mild pain near the incision this morning.",
  "neutral_note": "Patient reported mild pain near the incision and missed two sessions. Nurse review requested.",
  "red_flag": false,
  "callback_requested": true,
  "transcript_reference": "provider-side reference"
}
```

Validate webhook authenticity, make processing idempotent, and never trust provider text to directly create medical advice. If the webhook is late, the dashboard should show “call completed; result pending” rather than guessing.

## 8. InSee competitor assessment

The device the user called “IN-C” is almost certainly **InSee** by Tidal Medical Technologies, LLC.

### Regulatory status and intended use

- FDA 510(k) **K241152**, decision 21 August 2025, Class II therapeutic incentive-spirometer accessory; FDA found it substantially equivalent to the predicate.
- Prescription use, for the **hospital environment** by clinicians and patients.
- Compatible only with the Vyaire Medical AirLife volumetric incentive spirometers in **2,500 mL and 4,000 mL** versions.
- Reusable, non-invasive, one patient at a time.

The manufacturer website still contains older “pending clearance” material in places. Use the FDA database and 510(k) summary as the authoritative current source.

### Confirmed capabilities

- A plastic base attachment with an infrared time-of-flight sensor that tracks the AirLife internal piston/cylinder.
- Counts attempts above 250 mL, stores target volume, counts successful attempts and records maximum target volume.
- Audible/visual reminders and success feedback.
- Reminder intervals: off, 10, 20, 30, 60 or 120 minutes.
- LED display; measurements shown in 250 mL increments over 250–4,000 mL.
- 1,200 mAh rechargeable lithium battery and USB-C.
- Approximate dimensions 6.24 × 3.34 × 1.14 inches; weight 4.2 oz; stated shelf life two years.

The public FDA summary confirms local recording, display and reminders. It does **not** establish a cloud dashboard, caregiver messaging, multilingual coaching or automated calls, so do not attribute those capabilities to InSee without newer primary evidence.

### Validation evidence

The FDA summary reports a prospective IRB-approved performance study with 30 subjects, six production devices and eight tests per subject: 240 data points over 250–4,000 mL. It reported 100% agreement with blinded physician observation for target crossing, alerting and volume logging, with a 95% confidence interval of 98.5–100%, 100% repeatability and no reported adverse events.

That validates the measurement/task performance studied. It does **not** prove that InSee itself reduces pneumonia, length of stay or mortality. Outcome claims on the manufacturer site largely cite reminder-based incentive-spirometry studies and should not be presented as direct InSee outcome trials.

### Price, purchasing and international shipping

- **No public list price was found** on the manufacturer site or in the FDA material.
- The official site offers a **free hospital trial request** through a contact form; it does not expose a consumer checkout.
- **No verified international distributor or India shipping policy was found.** International shipping and India availability are therefore unknown, not “yes.”
- FDA clearance permits US marketing under the cleared indication; it does not establish registration, import permission or lawful sale in India.

The most defensible answer is: InSee appears to be sold/trialled hospital-to-hospital rather than as a public retail product. Contact Tidal Medical for a quotation, minimum order, supported countries, shipping terms, warranty and India regulatory status.

## 9. InSee versus SpiroBuddy

| Area | InSee | SpiroBuddy prototype |
|---|---|---|
| Maturity | FDA-cleared production medical accessory | Hackathon prototype; not a medical device claim |
| Setting | Hospital, prescription use | Proposed hospital-to-home recovery workflow |
| Parent device | Only AirLife 2,500/4,000 mL | Intended for low-cost piston-style devices used in India; compatibility must be validated |
| Sensing | IR time-of-flight piston tracking | Laser/ToF clip-on concept with simulator fallback |
| Local feedback | Display, alarm, LEDs, reminders | Web coaching, voice, reminders and 3D demo |
| Recorded measures | Attempts, successes, target and maximum volume | Breath features, technique classification, adherence and score |
| Languages | No multilingual capability found in cleared summary | Sarvam-supported Indian languages plus browser fallback |
| Care-team workflow | No cloud/call workflow established by public 510(k) | Nurse dashboard, family WhatsApp, escalation calls and notes |

### Honest positioning

Do not claim SpiroBuddy invented the smart accessory, is “the first,” is FDA-like, or has clinically proven outcomes. InSee proves that the base idea—using optical sensing to digitise an incentive spirometer—is technically and regulatorily plausible.

The differentiation is the care system around it: affordable Indian-device compatibility, multilingual coaching, technique feedback, home follow-up, family communication and nurse escalation. These are prototype goals that still need hardware validation, usability work, clinical evidence and regulatory review.

Tidal also holds US patents around monitoring incentive-spirometer use. Before commercialisation, obtain a formal freedom-to-operate review rather than assuming a different enclosure or country removes risk.

## 10. Go / no-go checklist

### Go for the hackathon

- Show the full missed-session story with simulated time and sensor data.
- Make browser-phone mode the guaranteed path.
- If the Sarvam number is active, let it call one pre-consented presenter phone.
- Show the structured outcome and nurse note, not an open-ended medical chatbot.
- State clearly which parts are live, simulated and future work.

### No-go claims

- “The agent diagnoses pain.”
- “Sarvam can ring any number immediately with no KYC or compliance setup.”
- “One transfer rings unlimited nurses simultaneously.”
- “InSee costs X” or “ships to India” without a written quote from Tidal.
- “SpiroBuddy is clinically proven,” “FDA-approved,” or “prevents pneumonia.”

## 11. Primary sources

### Sarvam

- [Voice Agents overview](https://docs.sarvam.ai/conversations/overview)
- [Phone numbers and telephony](https://docs.sarvam.ai/conversations/deploy/telephony)
- [Call transfer](https://docs.sarvam.ai/conversations/build/tools/call-transfer)
- [Variables and personalisation](https://docs.sarvam.ai/conversations/build/variables-personalization)
- [Campaign lifecycle](https://docs.sarvam.ai/conversations/deploy/campaigns/campaign-lifecycle)
- [Voice Agents runtime](https://docs.sarvam.ai/conversations/build/run-time)
- [Outbound webhook release note](https://docs.sarvam.ai/changelog/2026/8/20)
- [Epoch launch summary and Voice Agent price](https://www.sarvam.ai/epoch/summary)
- [API pricing](https://www.sarvam.ai/api-pricing)
- [Credits and rate limits](https://docs.sarvam.ai/api/getting-started/ratelimits)
- [Call Analytics product page](https://www.sarvam.ai/call-analytics)
- [Call Analytics pipeline cookbook](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)

### InSee

- [FDA 510(k) database entry K241152](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K241152)
- [FDA 510(k) summary PDF](https://www.accessdata.fda.gov/cdrh_docs/pdf24/K241152.pdf)
- [InSee official site](https://www.breathe-insee.com/)
- [InSee healthcare-professional page](https://www.breathe-insee.com/care-provider)
- [Tidal patent US10610129B1](https://patents.google.com/patent/US10610129B1/en)

## 12. Questions requiring vendor confirmation

1. Can the current ₹100 signup balance pay for Voice Agent calls and number rental, and are there separate KYC/number charges?
2. What real-call concurrency is enabled on a new non-enterprise account?
3. Can a Sarvam-rented Indian number be activated in time for the event?
4. What consent, DND and caller-ID configuration does Sarvam require for a healthcare reminder demo in India?
5. Does Tidal currently sell InSee, what is the hospital unit price/minimum order, and is there an India distributor?
6. Does InSee have any current connectivity or remote-dashboard option beyond the capabilities described in K241152?
