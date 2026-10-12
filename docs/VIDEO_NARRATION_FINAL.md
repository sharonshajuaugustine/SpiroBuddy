# Video narration — Aarogya Saathi with the SpiroBuddy breathing coach

Team **GuGu GaGa** · Sharon Shaju Augustine and Fathima Shifana · 12 October 2026 (version 4, for the 11:30 PM deadline)

**Target 5:54. Hard limit: under 6:00.** Say it in your own voice. You may change small words, but keep every honesty line (marked ★) and every number exactly as written.

The on-screen text for every block is in `docs/video/spec_v4.json`. It holds the on-screen text for every block below: chapter labels, cards, captions, the call subtitles and the end card.

**Built around the official marks.** The organisers' template (slide 1) scores: Problem Significance 15 · Understanding of Users 10 · Innovation 15 · Solution Quality 15 · MVP/Prototype 15 · Social Impact 15 · Scalability 5 · Sustainability/Business Model 5 · Responsible Technology 5. Each block below names the marks it serves, and the video shows the same name as a chapter label.

**What changed from version 3 (four judges and the accuracy audit):** the Chennai study is now said as an in-hospital study, with the day-three figure; two named, illustrative personas and one line of informal nurse feedback; the device is described as a design ("would"), with "no unit is built yet" said in Part 1; who gains is named under Social Impact; "modules switch on per hospital" and "needs a shared database" are gone; Part 2 follows one fictional patient, Savitri Devi, in care order; nobody taps "I took it"; the call is described as a simulator with scripted lines. Added for the ICMR request (founder, 12 October): the Responsible Technology block now says the design is informed by ICMR ethics guidance, not approved by ICMR; it shows the live Trust page's two ICMR tables with their honest status badges, and adds ethics committee review to what is still needed before real use (the block grows from 14 to 21 seconds; the breathing and branding scenes give back 3 seconds).

**Who reads the nurse-feedback line:** as written ("a nurse in a team member's family") it is true for either speaker. If you are the team member whose mother gave the feedback, you may say "a nurse in my family" instead.

**Pace:** Part 1 and Part 3 stay at or under 2.2 spoken words a second; Part 2 at or under 1.9. Words are counted the same way as in version 3 (each written word, with a hyphenated word as one).

**What Part 2 is:** the shots recorded on the live site (spirobuddy.onrender.com, hospital "Dawnlight General Hospital", fictional data only). The narration says only what those shots show.

---

## Part 1 — Explain (0:00–2:57) · 381 spoken words

Speak steadily. The cards on screen appear when you reach the words they belong to, so do not skip a number.

### 0:00–0:31 · Problem Significance
**Screen:** title card (Aarogya Saathi, "Connecting hospital care to the patient's phone."). At "India's public records", three number cards appear one by one, each when its number is spoken: 49 lakh · 1 in 10 · 6% → 72%. At "That was in hospital", a footer line names the gap after discharge.

> We are team GuGu GaGa.
> India's public records show about forty-nine lakh major operations a year. In an international study, about one in ten adults having surgery had a lung complication.
> In one small Chennai hospital study, only six percent used their spirometer properly the day after surgery; with teaching, seventy-two percent did by day three.
> ★ That was in hospital; we found no Indian home-use data.

Sources (all in `docs/research/KNOWLEDGE_BASE.md`): *Int J Surg* 2024 (public records, 2019 data, an undercount); LAS VEGAS study, *Eur J Anaesthesiol* 2017 (10.4% of 9,864 patients, 29 countries, mostly Europe); *J Pharm Bioallied Sci* 2024 (60 inpatients, Chennai). Always say "international study" and "percent". Never say the Chennai figure is about home.

### 0:31–1:00 · Understanding of Users
**Screen:** two persona cards (Savitri, 68 · Sister Anjali), each labelled "Illustrative persona". At "Informal feedback", the nurse-feedback card with its full source label. At "five steps", the journey strip: In hospital › Discharge › At home › Follow-up › Concern.

> We design for two illustrative people: Savitri, sixty-eight, home after lung surgery, who reads Hindi; and Sister Anjali, a ward nurse who must know whom to call first.
> ★ Informal feedback from one nurse in a team member's family: patients may skip painful breathing exercises and forget medicine schedules.
> Aarogya Saathi covers five steps: hospital, discharge, home, follow-up, and a concern reaching the nurse.

Source: `docs/INFORMAL_NURSE_FEEDBACK.md`. It is one nurse's second-hand, informal feedback. Never say "we interviewed nurses", "our research" or "a study". The personas are made up for design; they are not real people.

### 1:00–1:20 · Innovation
**Screen:** three columns, no ticks or crosses: Health-record apps · Hospital breath trackers (InSee) · Aarogya Saathi. The second column appears at "InSee", the third at "We join".

> Health-record apps such as Eka Care hold records and reminders. InSee, a US breath tracker, is FDA-cleared for hospital use only.
> We join the doctor's plan, dose reports and breathing coaching on one hospital record, with each hospital's own name, logo and colour.

Sources: InSee (Tidal Medical), FDA 510(k) K241152, cleared for hospital use only; record apps (Aarogya Setu 2.0, Eka Care) in `docs/plan/11_HOME_RECOVERY_COMPANION.md`. Never say "no one else does this" or "InSee is used in US hospitals".

### 1:20–1:45 · Solution Quality
**Screen:** deck slide 7 (Inside SpiroBuddy) with the tag "3D concept render, not built". At "Firmware is written", the architecture page's device-link section (Clip-on unit over USB: In development · Bluetooth link: Planned). At "A laser sensor", deck slide 8 (How SpiroBuddy works).

> SpiroBuddy is our optional breathing module, designed to clip onto an ordinary piston-type incentive spirometer.
> ★ Firmware is written; no unit is built yet. It would link by USB cable to a laptop; Bluetooth is planned.
> A laser sensor would read how high the piston rises. It coaches practice; it is not a lung test.

Device facts (`backend/app/features.py`): the firmware and the 3D design exist; no unit is built or bench-tested (In development); Bluetooth is Planned; the USB link is to Chrome or Edge on a laptop. Always "would", never "reads" or "sends".

### 1:45–2:19 · Social Impact
**Screen:** three cards, each tagged "Intended, not measured": Older patients · Families · Ward nurses. At "A one-ward pilot", four dashed cards: Activation 80% of enrolled · Day-7 return 60% of activated · Nurse minutes per day · Health benefit: not claimed.

> Our intended impact, under SDG three: older patients get the doctor's plan with Hindi, Tamil or Malayalam screen labels; families follow, with consent; nurses see whom to call first.
> ★ A one-ward pilot would measure plan views within forty-eight hours, day-seven return, and nurse minutes per day. Illustrative targets, not results: eighty percent of enrolled, sixty percent of activated patients.
> ★ Evidence that the exercise alone prevents lung complications is mixed; we claim no health benefit.

★ The targets are the deck's illustrative assumptions (1 ward, 20 patients, 14 days), not measured results. Only the screen's labels are in Hindi, Tamil or Malayalam; what the doctor types is shown as typed.

### 2:19–2:36 · Sustainability / Business Model · Scalability
**Screen:** three cards: what the hospital gets · proposed Rs 1,000 per follow-up episode · we do not charge patients. At "Every record carries", the two sample hospitals (Dawnlight General Hospital · Dawnlight Riverside Clinic), each with its own records, name and colour; at "Our plan", the next targets in the footer.

> ★ The hospital is the buyer, at a proposed, unvalidated thousand rupees per follow-up episode. No paying customers yet. We do not charge patients.
> Every record carries its hospital, checked on each request. Our plan: ward by ward.

The price is the deck's proposal (slide 13). Do not speak the unit price. The breathing module is switched on per patient, not per hospital.

### 2:36–2:57 · Responsible Technology
**Screen:** the live Trust page (spirobuddy.onrender.com/trust.html), three excerpts in page order, tagged "Live site: Trust page, excerpts": the ICMR 2017 table's Privacy (Live) and Ethics committee review (Planned) rows; the whole ICMR AI-in-health 2023 table (Human oversight, Accountability, Audit: In development · Transparency: Live). (Section 4's banner is left out: its first sentence, "Designed to follow these guidelines", is stronger than "informed by".) At "Before real use", three cards, each when it is spoken: Ethics committee review (Planned) · Database transactions (Not done yet) · Ask CDSCO for a ruling (No ruling yet).

> ★ Our design is informed by ICMR ethics guidance, not approved by ICMR.
> AI drafting, in development, needs consent and doctor review, and never diagnoses.
> ★ Before real use we still need ethics committee review, database transactions, real SMS, and a ruling from the regulator, CDSCO.

Say "I-C-M-R" as four letters (the Indian Council of Medical Research). Said aloud the block is 46 words in 21 seconds (2.19 a second), so do not add words. The two guidelines are the ICMR National Ethical Guidelines for biomedical and health research (2017) and the ICMR Ethical Guidelines for AI in biomedical research and healthcare (2023); do not speak the years. Approved statement: `docs/ICMR_ETHICS_CONTEXT.md` ("informed by ... No ICMR approval, certification or full compliance is claimed"); deck slide 15 says the same. The full guideline assessment (the 17-item ICMR AI checklist) and any ethics committee review are not done: both are pilot steps on the Trust page, section 5 (Planned). The site already runs on a Supabase database; what is missing is transactions and shared rate limits. No regulator has ruled on the product; never name a device class. The image leaves out the Trust page's "Vulnerable participants" row on purpose: it says the patient screens take no typing, and Part 2 shows Savitri typing her number and code.

---

## Part 2 — Working product (2:57–5:38) · 288 words

Each block matches one scene in `spec.json`. A thin bar at the top of the video shows whose screen it is (Doctor · Patient · Admin · Nurse), and a five-step journey bar shows where Savitri is.

### 2:57–3:08 · Doctor registers Savitri
**Screen:** shot s1_register (Doctor).

> ★ Our live site; doctor and patient are fictional. Doctor Meera Nair registers Savitri Devi, sixty-eight, and assigns the breathing module.

### 3:08–3:17 · Admin admits her to a bed
**Screen:** shots s2a_admit, then s2b_overview (Admin).

> The admin admits her to a Chest Ward bed; the overview counts come from recorded bed operations.

### 3:17–3:36 · Prescription: draft, review, send
**Screen:** shot s3_prescribe (Doctor). The video zooms on "Needs review" for two seconds.

> Doctor Nair types the prescription. Missing details, like food timing, are marked Needs review.
> ★ It is only a draft, with no AI.
> She chooses After food and sends it to Savitri's phone.

### 3:36–3:42 · Care instructions published
**Screen:** shot s4_publish (Doctor).

> Then she publishes the care instructions she wrote, as version one.

### 3:42–4:11 · Savitri's phone: login, medicines, pharmacy screen
**Screen:** shots s5a_login, s5b_meds, s5c_pharmacy (Patient phone). Say the Hindi line while the Hindi page is on screen.

> Savitri logs in with her hospital number and a one-time code.
> ★ The code is real, but its delivery is simulated: it shows on screen, not by SMS.
> The screen labels are in Hindi; the doctor's words stay as typed.
> She can show this at the pharmacy; the QR lets the chemist check the hospital's copy.

### 4:11–4:18 · Care instructions read
**Screen:** shot s6_ack (Patient phone).

> Savitri taps "I have read this version". ★ That records reading, not consent.

### 4:18–4:38 · SpiroBuddy breathing session
**Screen:** shots s7a_device, then s7b_breathing (Patient phone).

> ★ On a laptop, the unit would connect here. None exists yet; a simulator stands in.
> The coach gives feedback on each simulated breath.
> ★ This short session is saved as partial; a complete one needs ten valid breaths.

### 4:38–4:55 · Follow-up visit
**Screen:** shots s8a_request (Patient phone), s8b_confirm (Doctor), s8c_confirmed (Patient phone). Leave a short pause before "Doctor Nair" and before "and Savitri's phone".

> For follow-up, Savitri asks for a visit tomorrow and picks a time.
> Doctor Nair confirms it on My day, and Savitri's phone shows Confirmed.

### 4:55–5:29 · Simulated check-in call and nurse alert
**Screen:** shot s9a_call (the doctor's Demo page, call simulator), then s9b_nurse (Nurse). English subtitles run under the call.

> ★ Next, a simulated check-in call in Hindi, with her recorded consent; no real call is placed.
> It asks why sessions were missed. The sample answer: mild pain near her stitches, and please call back.
> ★ The assistant's lines are scripted; the presenter taps sample answers.
> ★ Fixed rules, not AI, alert the nurse. Sister Anjali reads the report, assigns it to herself and acknowledges it.

Savitri's consent for automated calls is recorded on her chart, off camera. The assistant's lines are fixed text and the replies are preset buttons, so never say "the AI asks", "Savitri says" or "her own words". The three English subtitles are in `spec.json` (`call_subs`); the scripted reply also tells her to get urgent help if the pain is severe, and the closing line gives 112.

### 5:29–5:38 · The hospital's own branding
**Screen:** shot s10_branding (Admin).

> Hospitals set their own name, logo and colour. Name and colour: previewed, undone. Safety messages stay fixed.

---

## Part 3 — Close (5:38–5:54) · 34 words
**Screen:** end card with four status cards (Live · Simulated · In development · Planned), the ask, the live link and the team names.

> Every product screen was recorded on our public site, with fictional patients.
> ★ Simulated: code delivery, breaths and the call. The device is not built.
> Our ask: one surgical ward to test this. Thank you.

---

## Never say (these would be untrue today)

- That the Chennai figure is about home ("at home, only six in a hundred"), "at home, nobody teaches", or "one in ten Indian patients".
- "Prevents lung complications", "faster recovery", "fewer readmissions" or "saves nurse time". Nothing is measured.
- "We interviewed nurses", "our research", "a study" or "nurses told us". It is one nurse's informal, second-hand feedback.
- "No one else does this", "first", or "InSee is used in US hospitals".
- "In the patient's language" with no limit, or that the prescription or care plan is translated. Only the screen's labels change.
- The device in the present tense ("the sensor reads, sends"), "connects to her phone by USB", "works with any spirometer", "measures lung function" or "the device measured this breath".
- "Session complete" or "exercise done". The session is saved as partial.
- "Eighty percent of patients" as a result, or without "of enrolled" and "of activated".
- "Patients never pay" or "free for patients". Say "we do not charge patients".
- "Modules switch on per hospital", "the whole app takes the hospital's colours" or "needs a shared database".
- "CDSCO-approved", "no licence needed" or any device class.
- "ICMR-approved", "ICMR-certified", "ICMR-endorsed", "ICMR-validated", "ICMR-compliant", "complies with ICMR" or "follows all ICMR guidelines". Say "informed by ICMR ethics guidance, not approved by ICMR".
- "Ethics approval obtained", "ethics-cleared", "an ethics committee reviewed it", or anything that suggests a study or pilot has run. Ethics committee review is Planned.
- "The ICMR checklist is done" or "a full ICMR assessment". The full guideline assessment is still pending.
- "The patient screens take no typing" (the Trust page's "Vulnerable participants" row says so, but Savitri types her number and code). Never show that row.
- "The code is simulated" or "an SMS was sent". The code is real; its delivery is simulated.
- "The AI drafted this prescription", "AI call", "the AI asks", "a real call", "Savitri says", "her own words" or "the AI alerts the nurse".
- "Tap I took it" or "she took her medicine". No dose is tapped in this video.
- "The chemist dispenses from this screen". The screen says "Not for dispensing".
- "Everything you saw runs live", "fully working", "used by", "pilot done", "partner hospital", "customers" or "works without a smartphone".

## Timing rule

The teleprompter copy shows each sentence at its time. Do one rehearsal against it before recording. Do not drop words: the cards on screen appear on the words they belong to. If you fall behind, shorten the pauses between sentences. Never drop a ★ line or a number.

| Block | Seconds | Words | Words a second |
|---|---|---|---|
| Problem Significance | 31 | 66 | 2.13 |
| Understanding of Users | 29 | 63 | 2.17 |
| Innovation | 20 | 43 | 2.15 |
| Solution Quality | 25 | 54 | 2.16 |
| Social Impact | 34 | 74 | 2.18 |
| Business Model and Scalability | 17 | 37 | 2.18 |
| Responsible Technology | 21 | 44 | 2.10 |
| Register | 11 | 20 | 1.82 |
| Admit and overview | 9 | 17 | 1.89 |
| Prescription | 19 | 32 | 1.68 |
| Publish | 6 | 11 | 1.83 |
| Login, medicines, pharmacy | 29 | 55 | 1.90 |
| Read acknowledgement | 7 | 12 | 1.71 |
| Breathing session | 20 | 37 | 1.85 |
| Visit | 17 | 24 | 1.41 |
| Call and nurse alert | 34 | 63 | 1.85 |
| Branding | 9 | 17 | 1.89 |
| Close | 16 | 34 | 2.12 |

| Part | Target | Your rehearsal |
|---|---|---|
| Part 1 · Explain | 2:57 | |
| Part 2 · Product | 2:41 | |
| Part 3 · Close | 0:16 | |
| **Total** | **5:54 (must be under 6:00)** | |
