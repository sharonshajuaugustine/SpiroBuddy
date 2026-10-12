# Video narration — Aarogya Saathi with the SpiroBuddy breathing coach

Team **GuGu GaGa** · Sharon Shaju Augustine and Fathima Shifana · 12 October 2026 (version 3, for the 11:30 PM deadline)

**Target about 5:45. Hard limit: under 6:00.** Say it in your own voice. You may change words, but keep every honesty line (marked ★).

Read this with [VIDEO_SHOT_LIST.md](VIDEO_SHOT_LIST.md) (what is on screen) and [VIDEO_RECORDING_CHECKLIST.md](VIDEO_RECORDING_CHECKLIST.md) (recording your voice and submitting).

**Built around the official marks.** The organisers' template (slide 1) scores: Problem Significance 15 · Understanding of Users 10 · Innovation 15 · Solution Quality 15 · MVP/Prototype 15 · Social Impact 15 · Scalability 5 · Sustainability/Business Model 5 · Responsible Technology 5. Each block below names the marks it serves, and the video shows the same name as a chapter label.

**How this was checked:** every demo click was run on the live site by an automated browser (12 Oct 2026, fictional patients only) after passing on an isolated local copy. The ready-made video in `output/video/` follows these exact times, and its teleprompter copy shows this text on screen.

---

## Part 1 — Explain (0:00–2:40) · 339 spoken words

Speak slowly. Leave a short pause when the slide changes. Slides are from the current deck, `output/Aarogya_Saathi_DTI_With_SpiroBuddy.pptx` (19 slides).

### 0:00–0:29 · Problem Significance
**Screen:** slide 1 (cover), then slide 2 at "India records".

> We are team GuGu GaGa, and our theme is Health and Well-being.
> India records about forty-nine lakh major operations a year, and in a large international study, one in ten surgical patients had a lung complication.
> Patients are told to do breathing exercises at home, but in one small Chennai study, only six in a hundred did them properly on day one.

Sources (all in `docs/research/KNOWLEDGE_BASE.md`): F-INDIA-1, *Int J Surg* 2024 (public records, an undercount); F-CLIN-1, LAS VEGAS study, *Eur J Anaesthesiol* 2017 (10.4% of 9,864 patients, mostly European hospitals); F-ADH-6, *J Pharm Bioallied Sci* 2024, PMID 39346353 (60 patients). Say "small study" and "international study"; do not turn them into Indian national rates.

### 0:29–0:53 · Understanding of Users
**Screen:** slide 4 (Target Beneficiaries), then slide 5 (Solution Overview) at "Aarogya Saathi".

> We design for two people: an older patient going home after surgery, who needs one simple screen in their own language, and a ward nurse, who must know whom to call first.
> Aarogya Saathi links them: the doctor's approved plan reaches the patient's phone, and the nurse sees who needs help.

### 0:53–1:10 · Innovation
**Screen:** slide 6 (Innovation & Differentiation).

> What is new: health-record apps hold documents and reminders, and breath trackers like InSee work inside US hospitals.
> We join the doctor's plan, dose reports and breathing coaching on one hospital record, in the patient's language.

Sources: InSee (Tidal Medical) FDA K241152, hospital use only — KNOWLEDGE_BASE F-COMP-1/F-COMP-5; record apps (ABHA / Aarogya Setu 2.0, Eka Care) — `docs/plan/11_HOME_RECOVERY_COMPANION.md`. Never say "no one else does this".

### 1:10–1:38 · Solution: the SpiroBuddy module
**Screen:** slide 7 (Inside SpiroBuddy); at "by USB cable", the architecture page's device-link section (Clip-on unit over USB: In development · Bluetooth link: Planned); at "Per-model calibration", slide 8 (How SpiroBuddy works).

> SpiroBuddy is the optional breathing module, clipped onto an ordinary incentive spirometer. A laser sensor reads how high the piston rises, and a small controller sends it by USB cable to our web app in Chrome; ★ Bluetooth to the phone is planned.
> Per-model calibration estimates the volume. ★ It coaches practice; it is not a lung test, and today's breaths are simulated.

Device facts (code: `web/js/sources.js`, `firmware/spirobuddy_serial/`; `backend/app/features.py`): USB = In development (no unit built or bench-tested), Bluetooth = Planned (Android phone or a hospital-lent phone; iPhones need the store app).

### 1:38–2:01 · Social Impact
**Screen:** slide 3 (Social Impact & SDG Alignment), then slide 14 (Adoption & Retention) at "In a one-ward pilot".

> Our intended impact, under SDG 3: more patients following their plan at home, and nurse time spent on those who need a call.
> In a one-ward pilot we would measure activation, patients viewing their plan within forty-eight hours, illustrative target eighty percent, and day-seven retention, illustrative target sixty percent.

★ The targets are the deck's illustrative assumptions (1 ward, 20 patients, 14 days), not measured results.

### 2:01–2:23 · Business Model and Scalability
**Screen:** slide 13 (Business & Sustainability Model), then slide 12 (Scalability) at "Records", then slide 16 (Roadmap) at "Next".

> The hospital pays a proposed, ★ unvalidated thousand rupees per follow-up episode; patients never pay.
> Records are scoped per hospital and modules switch on per hospital, so we grow ward by ward.
> Next: user interviews and device bench tests in ninety days, and a reviewed pilot by six months.

### 2:23–2:40 · Responsible Technology
**Screen:** slide 9 (Technology Architecture), then `spirobuddy.onrender.com/architecture.html`, section **1. The system**, at "AI drafting".

> One web service checks hospital access before reading any record.
> AI drafting is optional, needs consent and a doctor's review, and never diagnoses. ★ Production still needs a shared database and real SMS.

---

## Part 2 — Working product (2:40–5:25) · 290 words

Each block matches a scene in the shot list. A thin bar at the top of the video shows whose screen it is (Doctor · Patient · Admin · Nurse).

### 2:40–2:54 · Doctor registers a patient
> ★ Now the working product, live, with sample patients only. Doctor Meera Nair registers a patient with the hospital's own registration number and phone, and switches on the breathing module.

### 2:54–3:16 · Reviewed prescription
> She types the prescription and prepares a draft. ★ It is only a draft: anything unclear stays blank for her, like "after food".
> She checks each line and sends it to the patient's phone. It is now issued.

### 3:16–3:40 · Patient login, medicines and the pharmacy screen
> The patient logs in with the hospital number and a one-time code. ★ The code is simulated, shown on screen instead of an SMS.
> They see their medicines in their language, tap "I took it", and can show this screen at the pharmacy, with a QR code the chemist can check.

### 3:40–3:58 · Visit request and confirmation
> The patient asks for a visit and picks a free time. The doctor confirms it on My day, and the patient's phone shows Confirmed.

### 3:58–4:18 · Beds and the hospital's own branding
> The admin admits the patient to a bed, and the hospital overview updates from those bed operations.
> Each hospital also sets its own name, logo and colour for the patient app; safety messages stay fixed.

### 4:18–4:31 · Care document
> The doctor publishes the discharge instructions. The patient reads them and taps "I have read this version". ★ That records reading, not consent.

### 4:31–4:51 · SpiroBuddy session
> This is where the SpiroBuddy unit will connect by USB. ★ No device exists yet, so a simulator stands in.
> The coach gives feedback on each breath, and a short session is saved as partial, not complete.

### 4:51–5:25 · Simulated call in Hindi and nurse alert
> ★ Next, a simulated check-in call in Hindi, to Ravi, a sample patient who agreed to automated calls.
> The assistant asks why he missed his exercise. He reports mild pain near his stitches, and asks for a callback.
> ★ Fixed rules, not the AI, send this to the nurse. Sister Anjali reads his own words and acknowledges the alert.

The call is in Hindi on screen (Ravi's chosen language), with English subtitles in the video. The new patient cannot be called: calls need recorded consent, and the app refuses without it.

---

## Part 3 — Close (5:25–5:44) · 40 words
**Screen:** slide 17 (Team Structure), with the live link.

> Everything you saw runs live on sample data. ★ Simulated: the SMS code, breathing input and the call. A Gemini request and a Sarvam chat were tested separately.
> We are team GuGu GaGa: Sharon Shaju Augustine and Fathima Shifana. Thank you.

---

## Never say (these would be untrue today)

- "Used by" any hospital, any number of users, patients helped, pilots, interviews done or results.
- "The AI wrote this prescription" (on screen it is a manual-format draft), or "AI diagnoses".
- "The SMS was sent", "a real phone call", "Sarvam called the patient" or "the device measured this breath".
- "Proof the exercise was done" (device sessions are not tamper-proof yet), or "works without a smartphone" (the no-phone base is Planned).
- "Works when the app is closed" (spoken reminders only work while the page is open).
- A market size, or that no similar software exists.

## Timing rule

The teleprompter copy shows each sentence at its time. Do one rehearsal against it before recording. If you fall behind in Part 1, drop "in a large international study" and "in their own language" first.

| Part | Target | Your rehearsal |
|---|---|---|
| Part 1 · Explain | 2:40 | |
| Part 2 · Product | 2:45 | |
| Part 3 · Close | 0:19 | |
| **Total** | **about 5:44 (must be under 6:00)** | |
