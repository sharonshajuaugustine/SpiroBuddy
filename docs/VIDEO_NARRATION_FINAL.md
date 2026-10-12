# Video narration — Aarogya Saathi with the SpiroBuddy breathing coach

Team **GuGu GaGa** · Sharon Shaju Augustine and Fathima Shifana · 12 October 2026

**Target 5:40. Hard limit: under 6:00.** Say it in your own voice. You may change words, but keep every honesty line (marked ★).

Read this with [VIDEO_SHOT_LIST.md](VIDEO_SHOT_LIST.md) (what to click) and [VIDEO_RECORDING_CHECKLIST.md](VIDEO_RECORDING_CHECKLIST.md) (before and after recording).

How this script was checked: every click and on-screen message in the demo part was run on 12 Oct 2026, first on an isolated local copy, then on the **live site** (09:20–09:25 IST, fictional patient `REC-2026-12`). Both passed. The ready-made silent video in `output/video/` follows these exact times, and its teleprompter copy shows this text on screen.

---

## Part 1 — Explain (0:00–2:30) · 308 spoken words

Word counts treat "2024" as three spoken words ("twenty twenty-four"). Speak slowly. Leave a one-second pause when the slide changes. Slide numbers are from the current deck, `output/Aarogya_Saathi_DTI_With_SpiroBuddy.pptx` (19 slides).

### 0:00–0:25 · Theme and problem · 53 words
**Screen:** slide 1 (cover), then slide 2 (Problem Statement) at "After discharge".

> We are team GuGu GaGa, and our theme is Health and Well-being.
> After discharge, patients need their medicine times and exercise instructions, and nurses need to see who is missing.
> In one small 2024 Chennai study, only six in a hundred surgery patients used their breathing exerciser properly on day one.

Source for the last line: *J Pharm Bioallied Sci* 2024, PMID 39346353, 60 general-surgery patients (recorded in `docs/research/KNOWLEDGE_BASE.md`, F-ADH-6). Say "small study". Do not turn it into a national figure.

### 0:25–0:55 · Scope and personas · 52 words
**Screen:** slide 5 (Solution Overview), then slide 4 (Target Beneficiaries) at "We start with".

> Aarogya Saathi connects the hospital to the patient's phone.
> The doctor approves medicines and care instructions. The patient reads the plan in their language and reports doses. The nurse reviews missed reports and callback requests, and the admin manages beds.
> We start with older patients and ward nurses in one surgical ward.

### 0:55–1:25 · SpiroBuddy, the breathing module · 64 words
**Screen:** slide 7 (Inside SpiroBuddy), then slide 8 (How SpiroBuddy works) at "Per-model calibration".

> SpiroBuddy is the optional breathing module, clipped onto an ordinary incentive spirometer.
> As the patient breathes in, the piston rises. A laser sensor reads its distance, and a small controller sends it over USB. Per-model calibration estimates the volume.
> It coaches prescribed practice and alerts the nurse; ★ it is not a lung test. ★ The unit is not built yet, so today's breaths are simulated.

Slide 7 shows "Battery / Bluetooth version: future work". Leave it on screen; no need to say it.

### 1:25–1:55 · Market fit and two metrics · 60 words
**Screen:** slide 13 (Business & Sustainability Model), then slide 14 (Adoption & Retention) at "A pilot in one ward".

> The buyer is the hospital; patients never pay. Our proposal is a thousand rupees per care follow-up episode. ★ Pricing is unvalidated, and we have no paying customers.
> A pilot in one ward would track two numbers. Activation: patients who view their plan within forty-eight hours; illustrative target, eighty percent. Day-seven retention: activated patients still using it; illustrative target, sixty percent.

★ The targets and the pilot size (1 ward, 20 patients, 14 days) are the deck's illustrative assumptions, not measured results. Always say "illustrative target".

### 1:55–2:15 · Scalability and roadmap · 44 words
**Screen:** slide 12 (Scalability), then slide 16 (Implementation Roadmap) at "Roadmap".

> Records are scoped to each hospital, and modules switch on per hospital, one ward first.
> ★ Production still needs a shared database, real SMS and reviews.
> Roadmap: bench tests in ninety days, a reviewed pilot by six months, and an expansion review within a year.

### 2:15–2:30 · Architecture · 35 words
**Screen:** slide 9 (Technology Architecture). At "AI drafting", switch to `spirobuddy.onrender.com/architecture.html`, section **1. The system**.

> The patient and staff web apps talk to one service, which checks hospital access before reading any record.
> AI drafting is optional, with consent and a doctor's review. ★ Breathing input and calls are simulated today.

---

## Part 2 — Working product (2:30–5:20) · 282 words

Each block matches a scene in the shot list. Talk **while** you click. Stop talking for one beat when a success message appears, so viewers can read it.

### 2:30–2:47 · Doctor registers a patient (scene 2)
> ★ Now the working product, with sample patients only. Doctor Meera Nair registers a new patient with the hospital's own registration number and phone number, and switches on the breathing module.
> The patient is registered.

### 2:47–3:13 · Reviewed prescription (scene 3)
> She types the prescription in the notepad and prepares a draft. ★ It is only a draft. Anything unclear stays blank for her to decide, like "after food".
> She checks each line and sends it to the patient's phone. It is now issued.

### 3:13–3:36 · Patient login and medicines (scene 4)
> On the patient's phone: hospital, registration number, and a one-time code. ★ The code is simulated here. It appears on screen instead of an SMS.
> The patient sees the doctor's prescription, and taps "I took it". ★ That records the patient's own report.

### 3:36–3:58 · Visit request and confirmation (scene 5)
> The patient asks for a visit and picks a free time.
> The doctor sees the request on My day, and confirms it.
> The patient's phone now shows Confirmed.

### 3:58–4:11 · Bed management (scene 6)
> The hospital admin admits the patient to a bed. The hospital overview updates its counts from these recorded bed operations.

### 4:11–4:25 · Care document (scene 7)
> The doctor publishes the saved discharge instructions. The patient reads them and taps "I have read this version". ★ That records reading, not consent.

### 4:25–4:45 · Breathing session (scene 8)
> SpiroBuddy coaches the breathing exercise. ★ No device is connected, so these breaths come from a simulator. It gives feedback on each breath, and a short session is saved as partial, not complete.

### 4:45–5:20 · Simulated call in Hindi and nurse alert (scene 9)
> ★ Next, a simulated check-in call in Hindi, to Ravi, a sample patient who agreed to automated calls.
> The assistant asks why he missed his exercise. He reports mild pain near his stitches, and asks for a nurse to call back.
> ★ Fixed rules, not the AI, send this to the nurse.
> Sister Anjali sees the alert with his own words, and acknowledges it.

The call itself is in Hindi on screen (Ravi's language). The English meaning of each line is in the shot list, scene 9, if a judge-friendly caption is wanted.

---

## Part 3 — Close (5:20–5:40) · 52 words
**Screen:** slide 17 (Team Structure). Slide 19 shows the demo URL; use it instead if you prefer.

> Everything you saw works on sample data. ★ Simulated: the SMS code, breathing input and the call; the device is in development.
> ★ A real Gemini request and a Sarvam console chat were tested separately; phone calls and SMS come next.
> We are team GuGu GaGa: Sharon Shaju Augustine and Fathima Shifana. Thank you.

If you recorded on the **local** copy instead of the live site, replace the first sentence with: "This is our local working prototype, with sample data."

---

## Never say (these would be untrue today)

- "Used by" any hospital, any number of users, patients helped, pilots or results.
- "The AI wrote this prescription" (on screen it is a manual-format draft), or "AI diagnoses".
- "The SMS was sent", "a real phone call", "Sarvam called the patient" or "the device measured this breath".
- "Works when the app is closed" (spoken reminders only work while the page is open).
- A market size, or that no similar software exists.
- "Live" or "deployed" for any step you did not see working on the live site during your live check.

## Timing rule

Word counts guess the time; only a stopwatch proves it. Do one full rehearsal with a phone stopwatch. Write your real times in the table below. If Part 1 runs past 2:35, cut the optional "These are targets, not results" line first, then the sentence "SpiroBuddy is its breathing coach" (the breathing scene shows it).

| Part | Target | Your rehearsal |
|---|---|---|
| Part 1 · Explain | 2:30 | |
| Part 2 · Product | 2:50 | |
| Part 3 · Close | 0:20 | |
| **Total** | **5:40 (must be under 6:00)** | |
