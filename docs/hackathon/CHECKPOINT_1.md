# Checkpoint 1 – problem and concept (Sat 10 Oct 2026, 6:00 pm)

**Team:** SpiroBuddy · **Track:** Health & Well-being · **SDG 3** (good health and well-being; target 3.8, access to quality essential health care)
**Live prototype:** https://spirobuddy.onrender.com · **Code:** https://github.com/sharonshajuaugustine/SpiroBuddy

Laid out in the organisers' four stages: Problem → Technology → Innovation → Impact. References like `F-CLIN-1` point to `docs/research/RESEARCH_REPORT.md`, where every number has its source.

---

## In one breath (say this first, about 25 seconds)
> After surgery, patients are sent home with a plastic breathing exerciser that costs a few hundred rupees and told to use it every hour. Most forget, or do it wrong, and nobody can see that. SpiroBuddy is a small base the ordinary exerciser stands on. It watches each breath, coaches the patient by voice in their own language, shows the nurse who is falling behind, and sends the family one short WhatsApp update a day.

---

## 1. PROBLEM – identify the real need

**Who is affected**
- **Patients recovering from major surgery** (heart bypass, abdominal, chest), mostly older. India's public records show about 49 lakh major operations a year, an undercount. (F-INDIA-1)
- **Ward nurses**, who teach the exercise once and cannot watch every patient every hour.
- **Family caregivers** at home. About two in three older Indians live with their children. (F-INDLOC-3)

**What happens today**
- About **1 in 10** surgical patients gets a lung complication such as pneumonia or a partly collapsed lung (10.4% of 9,864 patients, 29 countries). (F-CLIN-1)
- Patients are given an **incentive spirometer**: breathe in slowly, the disc rises, hold for a few seconds, ten breaths every waking hour.
- **They don't do it.** 86% of 1,681 nurses and respiratory therapists say patients don't use it as they should; the top reason is forgetting. (F-ADH-2)
- **Or they do it wrong.** In a Chennai study only 6% of 60 patients did it properly on day 1 after surgery. (F-ADH-6, small study)
- **At home, nobody knows.** We found no data at all on how Indian patients use it after discharge. (Research report §2.5)

**Why it matters**
- In an Indian study, patients with a lung complication stayed 21.7 days instead of 12.5, and spent 8.5 days in ICU instead of 1.4. (F-CLIN-8, small, single hospital)
- Government insurance pays the hospital a fixed amount per operation, so every extra day is the hospital's cost. A ward day is about ₹2,307; an ICU day about ₹25,927. (F-BIZ-1, F-BIZ-4, F-BIZ-5)
- The usual fix, a phone app, misses our users: among Indians over 60, only 24% of women can read and write and 37% have low vision. (F-INDLOC-3)

**Evidence or user insight**
- Desk research: 9 rounds, 183 sources, graded, with a list of contradictions (`docs/research/RESEARCH_REPORT.md`).
- **User interviews: 0 so far. 3 planned today** (nurse or physiotherapist, patient, family carer). Guide: `docs/hackathon/INTERVIEW_GUIDE.md`. *Fill in before 6 pm:*
  - Interview 1: ________
  - Interview 2: ________
  - Interview 3: ________

**Honest limit (say it before a judge does):** studies have **not** proved that the exerciser on its own prevents complications (Cochrane 2014). Those trials rarely recorded whether patients actually did the exercise. That missing record is the gap we fill: we measure and improve the doing, we do not claim a medical outcome. (F-CLIN-3)

---

## 2. TECHNOLOGY – select the right enabler

| Need | Technology | Why this one |
|---|---|---|
| See each breath without touching the air path | A small **laser distance sensor** under the exerciser, measuring how high the disc rises | Nothing touches the patient's breath, so the exerciser stays exactly as its maker designed it. The same sensing idea is used by a US-cleared product (InSee, 2025). (F-COMP-1) |
| Judge the breath | **Our own small model** trained on breath curves, with simple rules as the backup: good / too fast / too shallow / no hold | Runs on the server, cheap, explainable. Each label has one plain tip. |
| Coach people who can't read small text | **Voice in 10 Indian languages and English** (Sarvam AI, an Indian speech company), slowed for older listeners; 341 pre-recorded clips so it works offline | Voice suits low literacy and low vision. Offline clips mean no internet is needed for coaching. |
| Tell the nurse who needs help | **Web dashboard**, most urgent patient first | No app to install; works on any ward computer or phone. |
| Reach the family | **WhatsApp** message and optional phone call, with recorded consent and a one-word STOP | The family already uses it. Nearly every home has a phone. |
| Write the daily summary | A language model (Claude), with a fixed template when it is unavailable | It only summarises. It never diagnoses. |

**Access, privacy, reliability**
- Works with **no smartphone** in the patient's hand.
- **Safety words** (chest pain, can't breathe, bleeding…) in four languages trigger a fixed "contact your nurse / call 112" reply. This check uses word lists, not AI.
- Data sits in India (Mumbai). Fake patients only at this stage. Consent is asked from the patient, in their language, and renewed weekly for calls.
- Every AI or internet feature has an offline fallback.

---

## 3. INNOVATION – create a useful solution

**What is different**
1. **It upgrades the low-cost exerciser patients already get** (about ₹150–1,000 online, F-INDIA-3), instead of replacing it with an expensive new device.
2. **It coaches the technique, not only the timing.** Most reminder tools only say "it's time". Ours says "slower" or "hold" during the breath.
3. **Built for Indian homes:** voice first, Indian languages, the family in the loop, WhatsApp and phone calls instead of an app.
4. **A human stays in charge.** Missed sessions lead to a nurse calling the patient. Alerts come from fixed rules, not from AI.

**What exists already (so we don't overclaim)**
- InSee (USA) is the closest product: a clip-on tracker for one US spirometer family, for hospital use. We are **not the first** smart spirometer add-on.
- We found no Indian product that tracks this exercise at home. That is a web search result, not a patent search.

**User journey**
1. At discharge, the nurse hands over the exerciser on its base and records consent.
2. Each waking hour the base chimes. The patient breathes; the voice coaches; the light turns green on a good breath.
3. Each session ticks itself off. Nothing to type.
4. Two missed sessions start a gentle ladder: reminder → family message → nurse alert → nurse calls.
5. Each evening the family gets one short update.

**Smallest useful version (what exists today)**
- **Working:** nurse and doctor dashboard, patient page, family page, breath model, voice coach in 11 languages (10 Indian + English), reminder ladder, consent and STOP handling, 3D showroom and 4 videos, over 400 automated tests. Live at the link above.
- **Simulated, and we say so:** the device. **We have no hardware yet**, so breaths come from a built-in simulator and the device is shown as a 3D model with cited dimensions. WhatsApp and phone calls run as on-screen previews ("would send"), not real sends.
- **Readiness level, honestly:** a working software prototype, not yet tested with real users (about TRL 3–4 on the organisers' scale).

---

## 4. IMPACT – define the change

**Our one headline metric**
> **Share of due hourly sessions completed** (sessions done ÷ sessions due, per patient per day).

It is counted automatically by the base, needs nobody to fill a form, and is the exact thing the existing studies failed to record.

**Supporting indicators**
| Indicator | How we measure it | Why |
|---|---|---|
| Share of breaths done correctly | Model label per breath | Doing it wrong is as common as not doing it |
| Hours from "2 missed sessions" to a nurse contact | Timestamps in the alert log | Shows the safety net works |
| Families reached, and STOP rate | Message log and consent record | Shows the updates are wanted |
| Languages served | Count of patients per language | Inclusion |

**A reference point:** in a US trial, an hourly reminder alone doubled the share of waking hours with use, from 28% to 58%. (F-ADH-1; it counts hours, not patients.) We aim to match that in a pilot, then add technique.

**What we will NOT claim** until a proper study: that SpiroBuddy prevents pneumonia, shortens stays, or cuts readmissions.

**Evidence plan**
1. **Today:** 3 interviews.
2. **Next 4 weeks:** build one real unit; measure sensor accuracy against the exerciser's printed marks; record real breaths to re-train the model (today it has only practice data).
3. **Pilot:** one hospital, 30–50 patients, with ethics approval and CDSCO's written view on central permission first; compare completed sessions against usual care.

**Scale path:** units are lent at discharge and reused. Estimated parts cost about ₹2,500 per pilot unit with Bluetooth and battery (a hand-built cable prototype is about ₹1,365). Price idea: about ₹1,000 per patient episode, with the unit lent and reused (team estimate). The same tool fits lung rehabilitation after TB and for long-term lung disease.

---

## Questions we expect at this checkpoint
| Question | Short answer |
|---|---|
| Did you talk to users? | "Three interviews today: ___, ___, ___." (Fill in. If fewer, say so.) |
| Is the device real? | "Not yet. The software is live; the device is a 3D model with sourced dimensions and a simulator. First real unit is step one after the hackathon." |
| Does the exerciser even work? | "Evidence for it alone is weak, and those trials never checked whether patients did it. We measure and improve the doing." |
| Is this a medical device? | "It coaches and summarises; it never diagnoses. Our reading of India's rules is to expect Class B, which we would confirm with the regulator before a pilot." |
| Why not just an app? | "Our users are older, many can't read small text, and most don't own a smartphone. Voice, a light and the family's WhatsApp reach them." |
| Who pays? | "The hospital. Under fixed-price insurance, every extra bed-day is the hospital's cost. Not yet tested with any hospital." |
