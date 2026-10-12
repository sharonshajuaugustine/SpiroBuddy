# Video narration — Aarogya Saathi with the SpiroBuddy breathing coach

Team **GuGu GaGa** · Sharon Shaju Augustine and Fathima Shifana · 12 October 2026

**Target 5:40. Hard limit: under 6:00.** Say it in your own voice. You may change words, but keep every honesty line (marked ★).

Read this with [VIDEO_SHOT_LIST.md](VIDEO_SHOT_LIST.md) (what to click) and [VIDEO_RECORDING_CHECKLIST.md](VIDEO_RECORDING_CHECKLIST.md) (before and after recording).

How this script was checked: every click and on-screen message in the demo part was run on 12 Oct 2026, first on an isolated local copy, then on the **live site** (09:20–09:25 IST, fictional patient `REC-2026-12`). Both passed. The ready-made silent video in `output/video/` follows these exact times, and its teleprompter copy shows this text on screen.

---

## Part 1 — Explain (0:00–2:30) · 315 spoken words

Word counts treat "2024" as three spoken words ("twenty twenty-four"). Speak slowly. Leave a one-second pause when the slide changes. Slide numbers are from `output/Aarogya_Saathi_DTI_GuGu_GaGa_Readable.pptx`.

### 0:00–0:30 · Theme and problem · 64 words
**Screen:** slide 1 (cover), then slide 2 (Problem) at "When patients go home".

> We are team GuGu GaGa. Our theme is Health and Well-being.
> When patients go home, their care plan often goes on paper. Medicines, exercises and instructions get lost, and nurses cannot check on everyone.
> After surgery, patients are asked to do breathing exercises. But in one small 2024 study in Chennai, only six in a hundred did them properly on day one.

Source for the last line: *J Pharm Bioallied Sci* 2024, PMID 39346353, 60 general-surgery patients (recorded in `docs/research/KNOWLEDGE_BASE.md`, F-ADH-6). Say "small study". Do not turn it into a national figure.

### 0:30–1:05 · Scope and personas · 73 words
**Screen:** slide 5 (Solution Overview), then slide 4 (Target Beneficiaries) at "We design first".

> Aarogya Saathi connects the hospital to the patient.
> The doctor registers the patient and publishes the prescription. The patient sees medicines, visits and care instructions on their phone. Nurses get follow-up alerts, and the admin manages beds. SpiroBuddy is its breathing coach.
> We design first for an older patient going home after surgery, who needs one simple screen in their language, and a ward nurse, who needs to know whom to call first.

### 1:05–1:40 · Market fit and two metrics · 74 words
**Screen:** slide 11 (Business model), then slide 3 (measures) at "A pilot would track".

> The buyer is the hospital or clinic; patients never pay. We would start with one surgical department.
> Our proposal is a fee per patient episode, about one thousand rupees in our planning estimate. ★ We have no paying customers or pilot yet.
> A pilot would track two numbers. Activation: patients who log in within two days of going home; illustrative target, seventy percent. Retention: patients still using it after thirty days; illustrative target, fifty percent.

★ If you have two spare seconds, add: "These are targets, not results." The two targets are our own illustrative pilot targets. They are not measured, and no source backs them; always say "illustrative target".

### 1:40–2:10 · Scalability and roadmap · 61 words
**Screen:** slide 10 (Scalability), then slide 14 (Roadmap) at "Our roadmap".

> Every record belongs to one hospital, so hospitals stay separate, and modules switch on per hospital.
> ★ Today the prototype runs on one server. Production needs a shared database with proper transactions, real SMS, privacy and clinical reviews, and a tested device.
> Our roadmap: bench-test the device in ninety days, a reviewed pilot by six months, and retention results within a year.

### 2:10–2:30 · Architecture · 43 words (12 s on slide 7, 8 s on the site diagram)
**Screen:** slide 7 (Technology Architecture). At "AI drafting", switch to `spirobuddy.onrender.com/architecture.html`, section **1. The system**.

> The patient's phone and the staff portal talk to one backend, which checks who you are and which hospital you belong to before reading any record.
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
**Screen:** slide 15 (Team Structure). Slide 17 shows the URL; use it instead if you prefer.

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
