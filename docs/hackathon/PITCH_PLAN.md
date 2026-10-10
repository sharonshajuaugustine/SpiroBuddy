# Pitch plan – deck, script, demo, judge answers, checklist

**For:** Social Impact Hackathon 2026, Health & Well-being (SDG 3). **Submission due Mon 12 Oct 2026, 11:00 AM IST.** Then a 5-minute pitch.
**Written:** Sun 11 Oct 2026. **Sources:** `docs/research/PITCH_FACTS.md` (numbers and the "Never say" list), `docs/hackathon/CHECKPOINT_1.md`, `docs/plan/03`, `06`, `07`, `08`, `docs/research/business/07_competitors_and_alternatives.md`, `docs/research/RESEARCH_REPORT.md` §9–10.
**Rule for this whole file:** every number below is already in `PITCH_FACTS.md`. Where a number from `docs/research/business/08_why_this_wins.md` belongs, there is a marked slot: **[insert from 08_why_this_wins.md]**. Do not fill it with a guess.

---

## 1. The story in one breath

**Hook (one sentence, say it first):**
> After surgery, patients go home with a plastic breathing exerciser and are told to use it every hour, and nobody, not the nurse, not the family, not even the clinical trials, has checked whether they actually do; SpiroBuddy makes that visible.

**One-line description for the form (182 characters with spaces, under the 200 limit):**
> A clip-on base for the breathing exerciser given after surgery: it checks each breath, coaches by voice in 10 Indian languages and English, and updates the nurse and opted-in family.

**Tagline:** *Every breath, coached and counted.*

**How to frame it (decided):** "the adherence and coaching layer for breathing exercise". Always introduce the device as **"an incentive spirometer, a breathing exerciser"**, so nobody hears "spirometry", the lung-function test. Turn the weak evidence into the hook: "the trials never checked if patients actually did it; we make it visible."

---

## 2. Slide-by-slide deck plan (11 slides + backups, 300 seconds)

The organisers' template must cover **Problem, Who is affected, Solution, Technology/AI, Impact, Scalability**. Pitch order: Problem → Who is affected → Solution → Demo → Technology/AI → Impact → Scale → Roadmap. The table maps each slide to that.

All URLs below are on `https://spirobuddy.onrender.com`. "Screenshot" means take it from the live site in Chrome at 1280 px wide, light theme, after **Reset demo data** on `/demo.html`.

| # | Template section | Slide title | The ONE message | What's on it | Seconds |
|---|---|---|---|---|---|
| 1 | (Title) | SpiroBuddy | A coach for the breathing exerciser patients take home | Logo, tagline, "Health & Well-being · SDG 3", one photo-like frame from `web/showcase/videos/hero.mp4` (pause at a clean frame, screenshot it). Team name, live link, GitHub link in small text | 10 |
| 2 | Problem | Nobody sees whether patients do it | The exercise is prescribed but invisible | Left: a frame of the plastic exerciser from `tour.mp4` (first 5 s). Right, three big numbers: **1 in 10** surgical patients gets a lung complication · **86%** of nurses say patients don't use it properly (top reason: forgetting) · **6%** did it right on day 1 (Chennai). Bottom line in teal: "Trials never checked if patients actually did it." | 35 |
| 3 | Who is affected | Older patients, busy nurses, worried families | The people who need it most can't use an app | Three columns with icons (user, hospital, users): **Patients** – ~49 lakh major operations a year in public records (an undercount) · **Nurses** – 2.6 per 1,000 people, below WHO's 3 · **Families** – 2 in 3 older Indians live with their children; 3 in 4 older women can't read. Strip at the bottom: "We interviewed: [insert 3 interviewees: role, city]" + one quote | 25 |
| 4 | Solution | SpiroBuddy: the coaching layer for breathing exercise | Base reads the breath, voice coaches, nurse and family see progress | A 4-step flow left to right: base under exerciser (screenshot `/showcase/` "Side" camera) → voice coach (screenshot `/app.html?id=1` mid-breath) → nurse list (screenshot `/` dashboard) → family WhatsApp preview (screenshot the WhatsApp simulator on `/demo.html`). Caption: "Works with no smartphone in the patient's hand." | 25 |
| 5 | (Demo) | Live demo | It works today, end to end, on simulated breaths | Just the link in large type and a small label "Device simulated · messages are previews". Switch to the browser (section 4) | 80 |
| 6 | Technology / AI | Where the AI is (and where it isn't) | Three small AI parts; safety rules are fixed, not AI | Three boxes: **Breath model** (good / too fast / too shallow / no hold; "trained on simulated breaths, rules as backup") · **Voice** (10 Indian languages + English, 341 offline clips) · **Daily summary** (Claude, with a template if offline; never diagnoses). A grey box: "Not AI, on purpose: red-flag words → fixed 'contact your nurse / call 112'; alerts and the reminder ladder." Footer: "Laser sensor reads the disc, like InSee (US). We add home use, Indian languages, nurse and family." | 30 |
| 7 | Impact | One number we can move: sessions done ÷ sessions due | The impact metric is counted automatically | Huge metric name. Screenshot the **"Sessions today"** tile on `/` (it shows "x% of sessions due so far"). Reference: "Hourly reminders alone: **28% → 58%** of waking hours with exercise (US trial, 145 patients)." Pilot target: **[insert from 08_why_this_wins.md]**. SDG box (see below). Small line: "We will not claim fewer complications until a proper study." | 30 |
| 8 | Scalability | Lent, reused, paid by the hospital | The money works at about ₹1,000 per patient | Three big numbers: **₹2,500** unit (our estimate), lent and reused across ~10 patients · **₹1,000** per patient episode = less than half a ward day (₹2,307) · **₹0.12** per WhatsApp update. Below: "Next: TB survivors – India's 2024 TB rehab guidance (draft) lists the incentive spirometer." Screenshot of `/units.html` as a small inset ("one unit, many patients – mock-up"). **[insert from 08_why_this_wins.md]** if it has a market-size line | 25 |
| 9 | (Readiness) | Where we honestly are: TRL 3–4 | Software works; device not built; no patients yet | Two-column "Working / Not yet": Working – live site, breath model, voice in 11 languages, reminder ladder, consent + STOP, 400+ automated tests. Not yet – the sensor unit (3D model only), real breaths, any patient. Line: "We expect Class B under India's device rules; we'll confirm with CDSCO before any patient." | 15 |
| 10 | Future roadmap | Next 6 months | Bench unit → real breaths → 30-patient pilot | Timeline of 4 steps: 1 bench-test one unit · 2 record real breaths, re-train · 3 ethics committee + CDSCO's written view · 4 30-patient, 3-month pilot at one hospital (~₹5.5 lakh, middle estimate). Then: three-ball reader, TB rehab | 15 |
| 11 | (Team + ask) | Team and our ask | We need one hospital partner team and regulatory guidance | Team photos/names, each with **the part they own** (sensor, breath model, alerts, money/legal, pitch). The ask, two bullets: an introduction to one nurse or physio team for a pilot; mentoring on CDSCO steps (or a NIDHI-PRAYAS application, up to ₹10 lakh). Tagline + link | 10 |
| | | | | **Total** | **300** |

**Backup slides (after "Thank you", not presented; open only if asked):**
B1 Evidence, honestly (Cochrane 2014, 2024 cardiac review; lung-cancer bundle review; the 28→58% trial) · B2 Competitors table (InSee, Airalux, Michigan ISTracker, phone apps, Cipla, Lupin) from `07_competitors_and_alternatives.md` · B3 Regulation and data (Class B expectation; DPDP; WhatsApp conditions; TRAI call rules) · B4 Unit economics table (`03_COSTS_AND_BUDGET.md` §2.2–2.3) · B5 Three-ball vs volume type · B6 Interview notes summary.

### SDG mapping (checked against the UN target wording)
| Target | UN wording (short) | Our honest link |
|---|---|---|
| **3.8 (main)** | Universal health coverage: access to quality essential health-care services | Brings follow-up of a standard post-surgery exercise into the home, in the patient's language, with no smartphone needed |
| **3.4** | Reduce premature deaths from non-communicable diseases through prevention and treatment; promote well-being | Supports recovery after heart and cancer surgery and, later, lung-disease rehab. We support it; we do not claim to move the death rate |
| **3.c** | Recruit, develop, train and retain the health workforce | Lets one nurse see which of many patients needs a call, instead of checking everyone |
| (3.3, later) | End TB and other epidemics | Only via the TB-survivor rehab roadmap. Mention as future, not as current impact |

### Readiness level (TRL), one line
**TRL 3–4:** the software works end to end on a live site with simulated breaths (TRL 4 for software), but the sensor unit is only a design and 3D model and nothing has been tested with real users or patients (TRL 3 for the device).

### Team slide (fill in)
| Name | Role | Owns and can explain in 60 seconds |
|---|---|---|
| [founder name] | Lead, pitch, video | Problem, users, money |
| [name] | | Sensor and the unit design |
| [name] | | Breath detection and the model ("trained on simulated breaths") |
| [name] | | Alerts, WhatsApp, consent, safety words |
(Names, college and contact go in the deck and the form only. Never in the repo.)

---

## 3. The 5-minute script (word for word, about 680 words; the two slots add about 30)

Speak slowly. The demo part has pauses while clicks happen, which is why it is shorter than its 80 seconds. Text in [brackets] is an action or a slot, not spoken.

**[0:00–0:10] Slide 1 – Title**
Good afternoon. I'm [name], from team SpiroBuddy, in the Health and Well-being track.

**[0:10–0:45] Slide 2 – Problem**
After an operation, many patients go home with this: an incentive spirometer, a plastic breathing exerciser. Breathe in slowly, the disc rises, hold, ten times every waking hour. About one in ten adults having surgery gets a lung complication. Now the strange part. Reviews say the exerciser on its own makes little difference. But those trials almost never checked whether patients actually did it. Eighty-six percent of nurses say patients don't use it properly, mostly because they forget. In a Chennai study, only six percent did it right on day one. Nobody can see who is doing it. We make it visible.

**[0:45–1:10] Slide 3 – Who is affected**
Who is affected? Older patients after heart, abdominal and chest surgery. India records about forty-nine lakh major operations a year, and that is an undercount. Ward nurses, who teach it once and can't watch every patient every hour. And families. Two in three older Indians live with their children, but three in four older women can't read. We spoke to [number and roles of interviewees]. One told us: "[best quote]".

**[1:10–1:35] Slide 4 – Solution**
SpiroBuddy is the adherence and coaching layer for breathing exercise. The ordinary exerciser stands on a small base. A laser sensor reads how high the disc rises. A voice coaches each breath in the patient's own language: slower, hold, well done. The nurse sees who is falling behind. And a family member who opted in, with the patient's consent, gets one short WhatsApp update a day.

**[1:35–2:55] Slide 5 – Live demo** [switch to browser, section 4]
Let me show you the live site. We have no hardware yet, so breaths come from a simulator. I start a session. [Good breath] Listen: the coach speaks Hindi. [Too fast] Too fast. It says "slower" at once, and the screen turns amber. [Finish now] The session saves itself. Nothing to type. [I do not feel well] One safety button. It shows a fixed message: contact your nurse, or call one-one-two. That part uses no AI.
Now the nurse's screen. [dashboard] Ravi is at the top, with his red flag. Every row shows sessions done out of sessions due today. [demo panel, missed slots, send summary] If Ravi misses two sessions, a ladder starts: a reminder, a family message, a nurse alert, then the nurse calls. These sends are previews, not real messages yet.

**[2:55–3:25] Slide 6 – Technology and AI**
Where is the AI? Three places. A small model labels each breath: good, too fast, too shallow, no hold. It is trained on simulated breaths, so its accuracy on real patients isn't measured yet, and simple rules run as a backup. A voice service speaks ten Indian languages and English, with recorded clips for offline use. A language model writes a short daily summary. It never diagnoses. Alerts come from fixed rules, on purpose. InSee in the US already reads the disc with a laser, in hospitals. We take the idea home, in Indian languages.

**[3:25–3:55] Slide 7 – Impact**
Our impact metric is one number: the share of due hourly sessions completed. It is counted automatically. In a US trial, hourly reminders alone doubled the share of waking hours with exercise, from twenty-eight to fifty-eight percent. [insert from 08_why_this_wins.md: our pilot target, one sentence]. This serves SDG 3: target 3.8, access to quality care, and 3.4, recovery from heart and lung disease. We will not claim fewer complications until a proper study shows it.

**[3:55–4:20] Slide 8 – Scale**
Who pays? The hospital. Under Ayushman Bharat, a bypass is paid at a fixed rate, so every extra bed-day comes out of the hospital's pocket. A ward day costs about twenty-three hundred rupees. Our unit costs about twenty-five hundred rupees, is lent at discharge and reused. We charge about one thousand rupees per patient episode, less than half a ward day. Next, TB survivors: India's draft TB rehab guidance lists this exerciser.

**[4:20–4:40] Slides 9 and 10 – Readiness and roadmap**
Honestly: about TRL three to four. The software works end to end, live. The sensor unit is not built, and nothing is tested on patients. Next: build one unit, record real breaths, then a thirty-patient pilot, with an ethics committee and the regulator's written view first. We expect Class B under India's device rules.

**[4:40–5:00] Slide 11 – Team and ask**
We are [names, one role each]. Our ask: an introduction to one hospital's nurse or physio team for that pilot, and guidance on the regulatory steps. SpiroBuddy. Every breath, coached and counted. Thank you.

### Hindi version note
- The video may be in Hindi; the live pitch language depends on the judges. **Keep the slides in English** either way (judges read them).
- Say the device's name in both: "इंसेंटिव स्पाइरोमीटर, यानी साँस का व्यायाम करने वाला उपकरण".
- Hook in Hindi (ask a native speaker to smooth it before recording): "ऑपरेशन के बाद मरीज़ को साँस का एक प्लास्टिक व्यायाम-उपकरण देकर हर घंटे इस्तेमाल करने को कहा जाता है। पर वह सच में करता है या नहीं, यह न नर्स देख पाती है, न परिवार। स्पाइरोबडी इसे दिखाता है।"
- Keep numbers, "TRL", "SDG 3", "WhatsApp", "AI" and "CDSCO" in English. Say "लाख" for lakh figures.
- The never-say list applies in Hindi too: no "निमोनिया से बचाता है", no "पहला/सबसे पहला", no "बीमारी पहचानता है / निदान", no "मंज़ूर / अप्रूव्ड".
- Hindi runs about 10–15% longer for the same content. If recording in Hindi, cut slide 3's quote or slide 8's TB line to stay at 5:00.

---

## 4. Live-demo plan (80 seconds)

### Set up (at T–10 minutes)
1. **T–10 min:** open `https://spirobuddy.onrender.com/api/health` in Chrome. It should answer within a few seconds (a keep-awake job pings it every 5 minutes). If not, wait 2 minutes and reload.
2. **T–8 min:** open `/demo.html`, click **Reset demo data**, wait for the refresh.
3. **T–6 min:** open these tabs, in this order, in one Chrome window:
   1. `/app.html?id=1` (Ravi's phone app). Make the window narrow, or press F12 → phone icon → a phone size, then close DevTools' side panel.
   2. `/` (nurse dashboard).
   3. `/demo.html` (demo panel).
   4. A local copy of the demo video, open in a player and paused at 0:40 (the fallback).
4. Chrome zoom **125%** so judges on Zoom can read it. Turn off notifications. In Zoom, **Share screen → the Chrome window → tick "Share sound"** so the Hindi voice is heard.
5. **T–2 min:** reload tab 1 once more. Unmute the tab.

### Click path (the "Live demo" lines in the script)
| Time | Tab | Click | Say |
|---|---|---|---|
| 0–10 s | app | **व्यायाम शुरू करें** (Start) | "We have no hardware yet, so breaths come from a simulator." |
| 10–25 s | app | Open **Demo controls** at the bottom → **Good breath** (or key `G`); wait for the coach | "Listen: the coach speaks Hindi." |
| 25–35 s | app | **Too fast** (key `F`) | "It says 'slower' at once; the screen turns amber." |
| 35–42 s | app | **अभी समाप्त करें** (Finish now); today's ticks update | "Saves itself. Nothing to type." |
| 42–52 s | app | **I do not feel well** | "Fixed message: contact your nurse or call 112. No AI." |
| 52–65 s | dashboard | Point to Ravi at the top (red flag), then to the "x of y due" meter and the **Sessions today** tile | "Sessions done out of sessions due: our impact metric." |
| 65–80 s | demo panel | Ravi's card → **Simulate 2 missed slots** (key `X`) → **Send summary to family (WhatsApp)** (key `S`) | "The ladder starts… previews, not real messages." |

### If something breaks
- **Site slow or asleep (nothing after 15 s):** say "The free server is waking up; here's the same flow recorded an hour ago," and play the local video from 0:40 to 2:40. Do not wait in silence.
- **Voice doesn't play:** keep going; say "you'll hear it in the video." The amber frame still shows.
- **Better backup if you have time:** before the pitch, run `scripts\run.ps1` on the laptop and keep `http://localhost:8000/app.html?id=1` in a second window. It works the same with no internet.
- **Zoom fails to share sound:** narrate the coach's words yourself ("breathe in slowly… hold").
- After the demo, click back to the deck. Practise this switch twice.

---

## 5. Demo video shot list: changes for the new framing

Checked `docs/hackathon/DEMO_VIDEO_SHOTLIST.md` against the decided framing, the never-say list and `07_CROSS_CHECK.md`. The deadline line is already correct. Changes:

| Shot | Change | Why |
|---|---|---|
| 1 | Open with "an incentive spirometer, a breathing exerciser". End with the hook: "Trials never checked whether patients actually did it. Nobody can see that. We make it visible." | New framing; "spiro" alone sounds like a lung test (08 BS-17) |
| 2 | Add "Like InSee in US hospitals, we read the disc with a laser sensor." Do **not** mention battery life or the board name (the caption burned into `tour.mp4` names an older board and battery) | Never say "our invention"; cross-check P5 |
| 3 | Add one sentence: "The breath model is trained on simulated breaths; real-patient accuracy isn't measured yet, and simple rules back it up." | 08 BS-28; never say "95.8%" without "simulated" |
| 4 | Say "10 Indian languages and English" | Cross-check P4 |
| 6 | Point at the **Sessions today** tile ("x% of sessions due so far") and the "x of y due" meter: "This is our impact metric." | Shows the metric is real, in the product |
| 7 | Say "a family member who opted in, with the patient's consent" | Never say "we message the family" alone |
| 8 | Replace "reminders alone doubled use" with "doubled the share of waking hours with exercise, 28 to 58 percent". Name the metric. Add "the adherence and coaching layer for breathing exercise" | Trial counted hours, not patients |
| Units extra | Add: "Units are lent and reused, about 1,000 rupees per patient episode." Keep "this screen is a mock-up" | Price story decided |
| 9 | Tagline → "Every breath, coached and counted." Track → "Health and Well-being, SDG 3" (not "Healthcare and Wellbeing") | New tagline; organisers' track name |
| New, 5 s, before shot 9 | A still card: "Working today: software, live. Simulated: the device, WhatsApp and calls. Next: one real unit, then a pilot." | Honest TRL in the video too |

Length stays 2:30–3:00. MP4 under 100 MB.

---

## 6. Judge Q&A: the 20 hardest questions (answers ≤30 words)

| # | Question | Answer |
|---|---|---|
| 1 | Does the incentive spirometer even work? | On its own, reviews find little benefit. But those trials rarely recorded whether patients did it. It helps inside a nurse-led breathing bundle; we make the doing visible. |
| 2 | So you're building on a weak device? | We coach the breathing exercise the physio prescribes. The base reads one exerciser today; the coach, dashboard and family link can take any breath source, even a manual tap. |
| 3 | You have no hardware. Is this real? | The software is live and works end to end. The device is a simulator plus a 3D model with sourced sizes. Building one bench unit is step one. |
| 4 | How accurate is your AI? | 95.8% on simulated breaths. Real-patient accuracy isn't measured yet; recording real breaths comes first. Simple rules run as a backup, and it only labels technique. |
| 5 | Most Indian patients get the three-ball type. | True, it is common and cheap. We read the volume type, which the US guideline suggests. Reading three-ball devices, perhaps by phone camera, is our first extension. |
| 6 | InSee is FDA-cleared. Why you? | InSee proved laser tracking works: in US hospitals, for one US spirometer. We add home use, voice in Indian languages, technique coaching, and nurse and family follow-up. |
| 7 | What stops Cipla, Lupin or a phone app copying you? | Nothing stops them trying. Our edge is elders without smartphones, 10 Indian languages, the nurse workflow and the family link. We'll accept phone-based breaths too. |
| 8 | Is this a medical device? | We expect so. It measures and alerts, so we expect Class B under India's device rules, and will confirm with CDSCO before any patient study. |
| 9 | Can you start a pilot with just ethics approval? | We won't assume that. Prototypes under a test licence, a hospital-led study with a registered ethics committee, and CDSCO's written view before enrolling anyone. |
| 10 | What about data privacy? | Fake patients only today. For launch: consent from the patient, in their language, read aloud; an itemised data list; one-word STOP; database in Mumbai; built towards India's DPDP Rules. |
| 11 | Could the AI give wrong medical advice? | It never diagnoses; it coaches and summarises. Red-flag words trigger a fixed "contact your nurse or call 112" message from word lists, not AI. Alerts follow fixed rules. |
| 12 | Is WhatsApp allowed for health updates? | Its business policy allows it with conditions: the family member opts in, the patient consents, approved non-promotional templates, STOP honoured. Progress updates only, never a diagnosis. |
| 13 | Who pays? | The hospital. Under fixed-price insurance, extra bed-days come from its margin. About ₹1,000 per patient episode, less than half a ward day. Not yet tested with a hospital. |
| 14 | PM-JAY hospitals can't bill patients extra. | Right. Our fee has to fit inside the hospital's package, not appear as a separate line. How that works is a question for our first hospital interviews. |
| 15 | What does a unit cost? Why not ₹200? | About ₹2,500 of parts, our estimate, lent and reused across about ten patients. ₹200 works only later, as a software fee on units hospitals own. |
| 16 | Will you cut readmissions or complications? | We don't claim that. We measure completed sessions now. Complications and readmissions would be measured in a proper study, not promised in a pitch. |
| 17 | Isn't a paper tally sheet enough? | Paper counts sessions, if someone fills it in. We also record how each breath is done: speed, depth, hold. Whether that helps is our first study question. |
| 18 | What about TB? | Our next market. India's 2024 TB rehab guidance, still a draft, lists the incentive spirometer for supervised sessions. By our estimate, 16–17 lakh people finish lung-TB treatment yearly. |
| 19 | Why you? Can you explain code an AI helped write? | Yes: each of us owns one part and can explain it. We mapped evidence, law and costs before building. [insert from 08_why_this_wins.md: one strongest point] |
| 20 | What happens after the hackathon, and how does it scale? | Bench-test one unit, record real breaths, then a 30-patient pilot. Units are lent and reused, so hospitals buy no hardware. One NIDHI-PRAYAS grant could fund the pilot. |

**Spare (if time):** "Will old people pick up calls?" → "Calls are a backup only. India's Kilkari service reaches half on the first call, three in four by the third. The device speaks; the family gets WhatsApp." · "Doesn't messaging after a readmission upset families?" → "Yes, so before any real patient we add one switch that stops all messages, and a 'not synced' state kept apart from 'missed'."

**Never say (short version, full list in `PITCH_FACTS.md`):** prevents pneumonia · first / first in India · clinically proven · diagnoses · real-time monitoring / detects deterioration · reduces readmissions · ₹X saved per patient · CDSCO/FDA-approved, certified, DPDP compliant · no licence needed / only an ethics committee · Class A because it's an accessory · patent pending / we own all the IP · doctors recommend it · partner hospitals · works with any spirometer · device plus software for ₹200 · our radio module is approved · 95.8% without "on simulated breaths" · "we message the family" without "who opted in, with the patient's consent" · Android app (say "mobile web app") · laser sensing is our invention · data never leaves India.

---

## 7. Design guidance for the deck

**Use the organisers' template as the frame** (their logo, footer, section order). Put our content inside it with our colours as accents. If the template's own colours clash, keep theirs for the frame and use teal only for highlights.

**One palette** (from `docs/DESIGN_SYSTEM.md`, light theme):
| Use | Colour |
|---|---|
| Brand, headings accents, big numbers | Teal `#0b6e8a` |
| Pale panels behind a number | `#e4f1f5` |
| Background | `#f4f6f8` or white |
| Body text | `#101c27`; secondary `#445263` |
| Good / done | Green `#1b7035` |
| Watch / slow down | Amber `#8f5100` on `#fff5e1` |
| Needs a person | Red `#c62828` (only for the "call 112" and red-flag examples) |
Meaning stays fixed: teal = SpiroBuddy, green = done, amber = slow down, red = a person is needed. Never colour alone: add a word or icon.

**Type:** Segoe UI (or the template's sans-serif); Nirmala UI / Noto Sans Devanagari for any Hindi. Title 36–44 pt, body at least 20 pt, **big numbers 72–96 pt in teal**.

**Rules for Zoom:**
1. One idea per slide; the slide title *is* the message (write it as a sentence).
2. At most 3 numbers per slide, each with a 4–6 word label and a tiny source line (e.g. "LAS VEGAS study, 2017").
3. Screenshots cropped tight to the part that matters; add a teal outline box around the point you talk about.
4. Nothing important in the bottom 10% (Zoom's controls cover it).
5. Label anything simulated with a small grey tag "Simulated" or "Mock-up".
6. Test once: share the deck on Zoom to a phone and check every slide is readable on the phone.
7. Export a PDF copy too; upload the format the form asks for, under 100 MB.

---

## 8. Rehearsal and submission checklist (Sun 11 Oct → Mon 12 Oct, 11:00 AM IST)

**First, check one thing:** the old slide said pitches on **Sun 3:30 pm**; the newer email moved only the submission. **Confirm the pitch time with the organisers now.** If a Sunday pitch still stands, rehearse the script today with a simple deck and submit the final files Monday.

| When (IST) | What | Who |
|---|---|---|
| **Sun, now → 2 pm** | Download the template (section 9, step 1). Do any missing interviews (step 2). Choose the backup person (step 4) | Founder |
| Sun 2–5 pm | Build the deck in the template from section 2. Take screenshots after **Reset demo data**. Fill the [insert…] slots from `08_why_this_wins.md` and the interviews | Founder (+ Claude to check wording) |
| Sun 5–6 pm | Each team member rehearses a 60-second "my part" explanation (Q&A #19) | Everyone |
| Sun 6–8 pm | Record the demo video with the updated shot list (section 5). Voice-over in English or Hindi. Check: under 100 MB, plays on a phone | Founder |
| Sun 8–9 pm | **Rehearsal 1:** full 5 minutes with the live demo, timed. Cut words, not slides, if over | Founder + one listener |
| Sun 9–9:30 pm | Ask Claude to run a never-say check on the deck text and video script | Founder |
| Sun 9:30–10 pm | **Rehearsal 2:** live demo with a deliberate failure (switch to the video). Then Q&A drill: listener asks 10 of the 20 questions | Founder + listener |
| Sun 10 pm | Put everything in one shared Google Drive folder: deck (PPTX + PDF), video MP4, one-liner text, problem and impact statements, team info. Share with the backup person (Editor) | Founder |
| **Mon 7:30 am** | Open the live site in an **incognito window**: `/`, `/app.html?id=1`, `/showcase/`. Open the GitHub link logged out. Check the deck link opens without login ("Anyone with the link – Viewer") | Founder |
| Mon 8:00 am | **Rehearsal 3**, timed | Founder |
| **Mon 9:00 am** | **Submit.** Fill the form; upload; save the reference number (screenshot + email) | **Founder presses submit** |
| Mon 9:15 am | If the founder hasn't confirmed by 9:15, the **backup person** submits from the shared folder (they rehearsed the form on Sunday) | Backup person |
| Mon 9:30 am | Freeze `main`: no more pushes until results (an auto-deploy could break the live site judges open) | Founder |
| Mon 11:00 am | Deadline. Two hours of buffer are already built in | – |
| Daily until results | Open the live link once a day; check the keep-awake job is still running | Founder |

---

## 9. What the founder must do (click by click)

1. **Get the organisers' pitch-deck template.**
   1. Open the organisers' slide or email that has the Google Drive link to the template.
   2. Click the link. In Google Slides click **File → Make a copy**, name it "SpiroBuddy – pitch deck".
   3. Also click **File → Download → Microsoft PowerPoint (.pptx)** and keep it in the shared folder.
   4. Tell Claude the slide titles the template has, so section 2 can be mapped exactly.
2. **Do the 3 user interviews** (if not yet done). Use `docs/hackathon/INTERVIEW_GUIDE.md`.
   1. Call one nurse or physiotherapist, one patient or ex-patient, one family carer (10–15 minutes each).
   2. Fill one notes sheet per person. Ask if you may quote them.
   3. Send Claude the notes (typed or photos). Claude writes `INTERVIEW_FINDINGS.md` and fills the slide 3 slot. Say "we interviewed 3 people", never "validated".
3. **Collect team information** for the form and slide 11: full names, role, the one part each person owns, college, leader's email and mobile, state. Keep it in the Drive folder, **not in the repo**.
4. **Pick a backup person and give them access.**
   1. In Google Drive, right-click the shared folder → **Share** → add their email → **Editor**.
   2. Send them the form link `https://social-impact-hackathon-submission.netlify.app/` and walk through it together once (don't submit).
   3. Add them as a second admin where you can (GitHub collaborator, Render team, Supabase member).
5. **Set link sharing for judges.** For the deck and video in Drive: **Share → General access → Anyone with the link → Viewer**. Test each link in an incognito window.
6. **Record the demo video** with the updated shot list (section 5 + `DEMO_VIDEO_SHOTLIST.md`). Start each take with **Reset demo data**. If the file is over 100 MB, give Claude the file name to shrink it.
7. **Wait for `08_why_this_wins.md`**, then paste its numbers into the five slots marked **[insert from 08_why_this_wins.md]** (slides 7 and 8, script slide 7, Q&A #19). Leave a slot out rather than guess.
8. **Confirm the pitch time** with the organisers (Sun 3:30 pm or later?).
9. **Submit by Mon 9:00 am** (section 8). Screenshot the reference number. Then tell Claude, so it can update HANDOFF.md and you freeze `main`.
