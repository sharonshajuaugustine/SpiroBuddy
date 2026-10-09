# Feature plan – explore everything, then keep the best

**How this file works (user's rule):** first list every idea in full (Part A, diverge). Then score them (Part B) and keep only the best for each stage (Part C, converge). Nothing is cut until it has been written down and scored. The design rules that hold everything together are in Part D.

**The one big principle:** *complexity lives with the nurse and the server, never with the patient.* An elderly, ill patient, or a guardian who isn't good with technology, should be able to use SpiroBuddy without opening an app, typing, logging in or reading English.

---

## Part A – every idea (diverge)

### A1. The patient path ("zero-app patient")
1. **Press one button, breathe.** The device button starts a session. The device light and beep coach on their own; no phone is needed.
2. **The device counts by itself** and stores breaths offline; it uploads when a phone or Wi-Fi is near.
3. **Hourly nudge on the device:** a soft chime and blinking teal light when a session is due; a press snoozes it for 15 min.
4. **Voice coach on any phone** in the patient's language: "Breathe in slowly… hold… 3, 2, 1… great breath!"
5. **Counting aloud during the hold** (helps patients who can't see a screen).
6. **Spoken result**, number of breaths left and praise: "7 done, 3 to go."
7. **Big-screen mode:** a single giant gauge for a tablet next to the bed.
8. **Hindi, English and Tamil first,** then 10+ Indian languages (pre-recorded clips plus TTS).
9. **Patient voice questions** ("Is coughing normal?"): answered from a nurse-approved FAQ, with the red-flag filter, never diagnosing.
10. **Pain/breathless check after a session:** 3 big smiley buttons, or press 1/2/3 on a call.
11. **Low-literacy pictures:** icon-only steps; a looping video of the correct technique.
12. **Festival or encouraging messages** recorded by the family ("Papa, you can do it!") played after a good session.

### A2. Automated phone calls (IVR = an automatic phone menu)
13. **Reminder robocall** after 2 missed hours: "Namaste Ravi ji, it's time for your breathing exercise. Press 1 if you've done it, 2 to be reminded in 15 minutes, 3 to talk to your nurse."
14. **Breathing session over a normal phone call** for patients with no smartphone: the voice coaches; the device uploads the numbers.
15. **Daily check-in call** with 3 yes/no questions (fever? more breathless? chest pain?). Any "yes" to a red-flag question → alert the nurse and give the fixed 112 message.
16. **Escalation call to the guardian** when the patient doesn't answer or misses 3+ hours.
17. **"Missed call to get a callback"**, a common Indian pattern: the patient gives a missed call to a number and the system calls back with the menu, so it costs the patient nothing.
18. **Click-to-call from the nurse dashboard:** a "Call patient" button that connects the nurse's phone to the patient through the system, with the call logged.
19. **Voice-note summary:** the evening summary as a 20-second audio clip in the patient's language.
20. **Call outcome logging:** every call's result (answered, pressed 1, no answer) shows on the dashboard.

### A3. WhatsApp
21. **Evening family summary** (AI-written, Hindi or English), already built in dry-run.
22. **Missed-session alert** to the guardian and nurse, already built in dry-run.
23. **Quick-reply buttons** on reminders: "✅ Done", "⏰ Remind me in 15 min", "📞 Call me".
24. **Weekly progress card:** an image with the 7-day chart in our colours, easy to forward to relatives.
25. **Guardian commands:** the guardian types "status" or "स्थिति" and gets today's progress back.
26. **Patient "HELP" keyword:** red-flag handling plus a nurse alert.
27. **Discharge instructions + technique video** sent on day 1.
28. **Nurse broadcast:** "All patients: remember 10 breaths every hour."
29. **Voice-note replies** from the patient, transcribed and checked for red flags.
30. **Onboarding by QR code:** scan the QR on the device box → WhatsApp opens with "Join Ravi's care circle".
31. **Family cheer:** the guardian taps "Send a cheer" and the patient hears it after the next session.

### A4. Guardian / family
32. **Guardian web page by magic link** (no login): today's ticks, streak, last breath, a big "Call Papa" button.
33. **Care circle:** several family members, each choosing WhatsApp, call or SMS, and quiet hours.
34. **Escalation ladder settings:** who gets told, after how long.
35. **Weekly guardian report** in the guardian's own language (may differ from the patient's).

### A5. Nurse / doctor website (complex side, built for professionals)
36. **Triage dashboard:** red/amber/green with reasons (done).
37. **Alerts inbox:** every alert with acknowledge / snooze / assign, so nothing is lost.
38. **Escalation timeline per patient:** device beep → voice → WhatsApp → call → guardian → nurse, with times.
39. **Care plan editor:** target mL, hold time, sessions per day, quiet hours, languages, contacts.
40. **Notes and tasks** on each patient, with a handover view between shifts.
41. **Technique analytics:** label mix over time ("too fast" falling = coaching works).
42. **Lower-than-usual trend flag:** "volume 25% below his own 3-day average". Worded as an observation, never as a diagnosis.
43. **Cohort view:** all knee-surgery patients this month, adherence by ward or surgeon.
44. **PDF/print report** for the follow-up clinic visit.
45. **Discharge onboarding wizard:** add a patient in 60 seconds, print the QR, pair the device.
46. **Roles:** nurse, doctor, admin, with an audit log of who changed what.
47. **Multi-hospital / multi-ward** support.
48. **Export:** CSV now; FHIR / ABDM (India's national digital health records) later.

### A6. Device
49. LED colours with the same meaning as the app (teal, amber, green, red).
50. Buzzer tones: chime for good, low double-tone for slower.
51. Battery-low warning on the device and on the dashboard.
52. A tiny OLED screen with a breath count and score (optional extra).
53. Fit-check: the device tells you if it's mounted wrongly (readings out of range).
54. Bluetooth to the phone; USB backup; Wi-Fi upload.
55. On-device ML (emlearn), so coaching works even with no phone.

### A7. AI features
56. Our own breath-technique model (done).
57. AI evening summary (done, with template fallback).
58. AI-drafted nurse call script: "Ravi missed 3 hours; ask about pain; suggest a session now."
59. Speech-to-text for patient voice notes → red-flag check.
60. Multilingual TTS (text-to-speech: computer voices) for every message.
61. Personalised coaching: if a patient is often "too fast", the coach adds "very slowly" at the start of each breath.

### A8. Motivation
62. Streaks and gentle milestones ("5-day streak!") with no losing or shaming.
63. A "breath garden" that grows a plant with each good session.
64. Family leaderboard (opt-in) or a family cheer counter.

### A9. Safety, privacy, trust
65. Red-flag word filter everywhere (done in the AI).
66. Fixed emergency message plus a "call 112" button.
67. Consent at onboarding (recorded voice "yes" or a guardian tick).
68. DPDP Act 2023 privacy: minimal data, delete on request, data stored in India (a Supabase region choice).
69. Quiet hours: no calls at night unless it's red-flag.
70. Every automated message says it's automated and how to reach a human.

---

## Part B – scoring (converge)
Each idea is scored 1–5 on: **P**atient value · **E**ase for elderly users (5 = nothing new to learn) · **D**emo wow for judges · **F**easibility before the demo · **S**afety/trust. Total out of 25.

| # | Idea | P | E | D | F | S | Total |
|---|---|---|---|---|---|---|---|
| 13 | Reminder robocall with press-1/2/3 | 5 | 5 | 5 | 4 | 4 | **23** |
| 38 | Escalation ladder + timeline | 5 | 5 | 5 | 4 | 5 | **24** |
| 23 | WhatsApp quick-reply buttons | 4 | 5 | 4 | 4 | 4 | **21** |
| 32 | Guardian magic-link page | 4 | 5 | 4 | 5 | 4 | **22** |
| 37 | Alerts inbox with acknowledge | 4 | 5 | 4 | 5 | 5 | **23** |
| 15 | Daily red-flag check-in call | 5 | 5 | 4 | 3 | 5 | **22** |
| 18 | Click-to-call from dashboard | 4 | 5 | 4 | 4 | 4 | **21** |
| 24 | Weekly progress card image | 4 | 5 | 4 | 4 | 4 | **21** |
| 17 | Missed-call-to-callback | 4 | 5 | 4 | 3 | 4 | **20** |
| 19 | Voice-note summary | 4 | 5 | 4 | 4 | 4 | **21** |
| 1–6 | Zero-app device-first session + voice coach | 5 | 5 | 5 | 3 | 5 | **23** |
| 42 | Lower-than-usual trend flag | 4 | 5 | 3 | 5 | 4 | **21** |
| 58 | AI nurse call script | 3 | 5 | 4 | 5 | 4 | **21** |
| 30 | QR onboarding | 3 | 4 | 3 | 4 | 4 | 18 |
| 63 | Breath garden | 3 | 4 | 3 | 3 | 5 | 18 |
| 48 | FHIR/ABDM export | 2 | 5 | 2 | 2 | 4 | 15 |
(Ideas not listed are scored when we reach them. The research agent checks feasibility, e.g. which Indian voice-call provider allows Hindi TTS and what WhatsApp templates need.)

## Part C – what we build, in order
**Stage 1 – hackathon demo (build now, all in DEMO / dry-run mode with real providers if keys exist):**
1. **Escalation ladder engine** (server): rules → device beep → WhatsApp reminder with quick replies → automated call (press 1/2/3) → guardian WhatsApp + call → nurse alert. Every step is logged, with a timeline on the patient page.
2. **Automated calls:** Twilio Voice in dry-run, with a **browser "phone simulator"** on the demo panel that plays the call in Hindi/English (speech synthesis) and lets the presenter press 1/2/3, so the judges hear it even with no phone signal.
3. **Alerts inbox** on the dashboard (acknowledge, assign) + **click-to-call** button (dry-run).
4. **Guardian page** (magic link, giant text, "Call Papa" button, today's ticks, streak, in Hindi/English).
5. **WhatsApp:** quick-reply buttons (simulated in the demo panel's chat view), weekly progress card image, voice-note summary (TTS audio file in the demo; real when a TTS key exists).
6. **Lower-than-usual trend flag** + **AI nurse call script** on the patient page (with template fallbacks).

7. **Sarvam Voice Agent call (optional live path):** a conversational check-in call ("Are you okay, why did you miss it?") using spoken answers, a webhook into SpiroBuddy with the normalised outcome, a neutral nurse note and deterministic red-flag rules. Browser phone stays the guaranteed path. Spec: `docs/research/SARVAM_CALLS_AND_INSEE_FEASIBILITY.md` §5–§7.

**Stage 2 – after the hackathon:** the daily red-flag check-in call, missed-call callback, QR onboarding, care-circle settings, voice-note transcription, personalised coaching, PDF report, roles + audit log.
**Stage 3 – scale:** on-device ML, FHIR/ABDM export, multi-hospital, cohort analytics, breath garden, on-device OLED.

## Part D – simplicity rules for patients and guardians (non-negotiable)
1. Never require the patient to install, log in, type or read English.
2. One action at a time; the next step is always spoken.
3. Every message has at most one question, with at most 3 big options (1/2/3 or buttons).
4. Same words, same colours, same sounds everywhere (see DESIGN_SYSTEM.md).
5. Calls only within quiet hours unless red-flag; the guardian can always reach a human.
6. If anything fails (no internet, no keys), the patient still gets the device beep, the light and the stored count.
