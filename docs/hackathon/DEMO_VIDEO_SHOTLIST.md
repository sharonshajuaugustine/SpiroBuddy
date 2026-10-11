# Demo video – shot list (5½ minutes, in the organisers' order)

**Deadline:** upload with the submission by **Mon 12 Oct 2026, 11:00 AM IST**.
**What the organisers asked for (spoken, Sun 11 Oct, about 1:15 pm and 1:25 pm):** a demo video of **5 to 6 minutes**, **in your own words** (you narrate it yourself; no AI voice), **under 100 MB**, covering in this order: the theme, the problem, the impact, the user personas (briefly, but they called personas "very very important"), the architecture, a detailed demo of the whole product, the scalability model and the future roadmap. In a second answer they asked for **estimated user adoption and retention**, built on clearly labelled assumptions, in both the pitch and the video. Estimates are allowed where no real numbers exist, and features still in development may be shown, as long as each is clearly labelled.
**Target:** **5:30**. Hard limits **5:00–6:00**. Voice-over: **733 words** at a calm 140–145 words a minute, plus about 20 seconds of pauses while the app speaks. **27 of those words are optional** (marked ((like this))): cut them if your take runs long.
**Format:** one MP4, 1920×1080, English (the form also allows Hindi), 60–95 MB.

Replaces the 2:30–3:00 version. Every change asked for in `PITCH_PLAN.md` §5 (old) is applied, plus the 11 Oct rules: status labels, labelled estimates, the 11-language wording and the adoption shot.

---

## Coverage: organiser requirement → shots

| # | What the organisers asked for (their order) | Shot(s) | Time |
|---|---|---|---|
| 1 | The theme selected | 1 | 0:00–0:11 |
| 2 | The problem statement | 2 | 0:11–0:41 |
| 3 | The impact you are creating | 3 (and the same number live in the product, shot 9) | 0:41–1:02 |
| 4 | User personas, brief ("very very important") | 4 (and the demo follows each persona: Ravi 7–8, Sister Anjali 9–10, Amit 12) | 1:02–1:28 |
| 5 | The architecture | 5 | 1:28–1:58 |
| 6 | A detailed demo of the whole product | 6 (In development: the base unit), 7–12 (the live product) | 1:58–4:08 |
| + | Estimated adoption and retention, clearly labelled (second answer) | 13 | 4:08–4:39 |
| 7 | The scalability model | 14 | 4:39–5:08 |
| 8 | The future roadmap | 15, then 16 (honest status and close) | 5:08–5:34 |
| – | Status labels and labelled estimates (organisers allow both if labelled) | 3, 5, 6, 10, 11, 13, 14, 16 and the on-screen labels | – |
| – | Own words, 5–6 minutes, under 100 MB | whole video; "Getting under 100 MB" below | 5:34 |

---

## Use exactly these four status words (screen and voice)

| Word | Means | Examples in SpiroBuddy |
|---|---|---|
| **Live** | Works today on the live site | Patient app, nurse dashboard, patient page, family page, breath model, safety rules, the recorded voice clips (11 languages), the fixed-text summary |
| **Simulated** | Works end to end, but the input is simulated | The breaths (a simulator stands in for the base) |
| **In development** | Designed, partly built, not working end to end yet | The base unit (firmware and 3D design exist; nothing built or bench-tested) · Claude-written summaries (code exists, switched off on the live site, never run) · live Sarvam voice (code exists, no key on the live site) · real WhatsApp and phone sends (previews today) · the Units screen (a mock-up) |
| **Planned** | Not started (roadmap) | Bluetooth link and Android app · nurse login and roles · a speaking base with a SIM for patients without a smartphone · a three-ball reader (phone camera) · TB lung rehab |

**Never say in the video:** "prevents pneumonia" · "first" (in any sense) · "clinically proven" · "diagnoses" (only "never diagnoses") · "real-time monitoring" · "reduces readmissions" · "approved", "certified", "compliant" · "partner hospitals" · "works with any spirometer" · "the ordinary exerciser" · "no smartphone needed" or "the device speaks" (say: Planned) · "coaches in 10 Indian languages" as a fact (say: voice coaching recorded in 11 languages; the app's screens run in 4) · "we charge" (say: we plan to charge, estimate) · "95.8%" · "Android app" for today's app (say "mobile web app" or "app") · "laser sensing is our invention" · "data never leaves India" · "we message the family" without "who opted in, with the patient's consent". Full lists: `docs/research/PITCH_FACTS.md`, `docs/plan/06_LEGAL_DEEP_DIVE.md`, `docs/research/business/08_why_this_wins.md`.

---

## Before you record

1. **Wake the site.** Open `https://spirobuddy.onrender.com/api/health`. It should show `"ok":true` within a few seconds (up to a minute if the free server was asleep).
2. **Reset the demo.** Open `https://spirobuddy.onrender.com/demo.html` → click **Reset demo data** (red button, top right) → click **OK** → wait for "Demo data reset". Ravi's card must say **On track** (green). If it shows a red flag, click **Reset demo data** again. Do this before **every** take of shots 7–12.
3. **Reset the units.** Open `https://spirobuddy.onrender.com/units.html` → click **Reset mock units**.
4. **Clean screen.** Use a Chrome window with no personal profile showing (click your profile picture, top right → **Guest**). Hide bookmarks (**Ctrl + Shift + B**). Turn on Do Not Disturb (**Win + N** → **Do not disturb**). Close WhatsApp, email and chat apps. No real names, phone numbers or emails may appear anywhere.
5. **Open these tabs in this order**, so you only press **Ctrl + Tab** while recording:
   1. The deck in Google Slides, **Slideshow** mode (slides 1, 2, 3, 7, 7b, 8, 9, 10; see `PITCH_PLAN.md` §2)
   2. `docs\hackathon\architecture.png` (drag the file from File Explorer into a Chrome tab)
   3. `https://spirobuddy.onrender.com/showcase/videos.html` (tour video) and `https://spirobuddy.onrender.com/showcase/` (3D showroom)
   4. `https://spirobuddy.onrender.com/app.html?id=1` in a phone-sized view: press **F12**, click the phone-and-tablet icon at the top left of the panel, pick a phone (for example "Pixel 7"). Or simply make the window narrow.
   5. `https://spirobuddy.onrender.com/` (nurse dashboard)
   6. `https://spirobuddy.onrender.com/patient.html?id=1` (Ravi's page)
   7. `https://spirobuddy.onrender.com/demo.html` (demo controls)
   8. `https://spirobuddy.onrender.com/guardian.html?t=ravi-amit-demo` (Amit's family page)
   9. `https://spirobuddy.onrender.com/units.html` (Units mock-up)
6. **Sound.** Unmute the tabs. Click **Good breath** in the app once to check you hear the Hindi voice, then reset again (step 2).
7. **Recorder.** Press **Win + G**; in the **Capture** box turn the **microphone** on. Record a window with **Win + Alt + R** (press again to stop). Test 10 seconds and play it back: you must hear both your voice and the app. OBS works too.
8. **Record each shot separately** and join them afterwards (section "After recording"). A clean 20-second take is easier than one perfect 5-minute take.
9. **In your own words.** The script below is a guide. Say it your way, but keep every number, every status word and every honesty phrase.

---

## The shots

Conventions: **[bold brackets]** = an action, not spoken. ((Double brackets)) = optional words. Word counts exclude actions and your name.

### Shot 1 · 0:00–0:11 · Theme
- **Covers:** the theme selected.
- **On screen:** deck slide 1 (title card): logo, "SpiroBuddy", **"Theme: Health & Well-being (SDG 3)"**, tagline "Every breath, coached and counted.", "Social Impact Hackathon 2026", team name.
- **Voice-over (25 words):**
> Hello, I'm **[your name]**, founder of SpiroBuddy. Our theme is Health and Well-being, SDG 3. SpiroBuddy is the adherence and coaching layer for breathing exercise after surgery.

### Shot 2 · 0:11–0:41 · Problem
- **Covers:** the problem statement.
- **On screen:** `showcase/videos.html` → play **tour.mp4** from 0:00 to 0:10 (patient outline holding the exerciser; captions "After surgery, patients go home with an incentive spirometer" and "At home nobody sees if they use it"). Then cut to deck slide 2 (three numbers: 1 in 10 · 86% of US nurses · 6%).
- **Voice-over (70 words, 4 optional):**
> After surgery, many patients go home with an incentive spirometer, a plastic breathing exerciser: ten slow breaths every waking hour. About one in ten surgical patients gets a lung complication. Reviews say the exerciser on its own makes little difference, but those trials almost never checked whether patients actually did it. In Chennai, only six percent did it right on day one. ((Nobody can see that.)) We make it visible.
- Say "almost never", not "never" (the cross-check judge found "never" overstates the evidence; `PITCH_FACTS.md` #33 says "rarely recorded").

### Shot 3 · 0:41–1:02 · Impact
- **Covers:** the impact you are creating (and SDG 3).
- **On screen:** deck slide 7: the metric name in large type, a screenshot of the dashboard's **Sessions today** tile, the target line, the SDG box (3.8 main; 3.4; 3.c). Footnote on the slide: *"Target, not a result – basis: Eltorai et al., JAMA Surgery 2019 (US, 145 bypass patients; waking hours with exercise: 28% without reminders, 58% with)."*
- **Voice-over (49 words):**
> The impact we want is one number: the share of due hourly sessions completed, counted automatically. Our target is about fifty-eight percent, the level hourly reminders reached in a US trial, up from twenty-eight percent without them. We will not claim fewer complications until a proper study shows it.

### Shot 4 · 1:02–1:28 · User personas
- **Covers:** user personas (keep this shot even if you must cut elsewhere).
- **On screen:** deck slide 3: three persona cards (Ravi · Sister Anjali · Amit), each with a big number, under the label **"Illustrative, based on our research – not real people"**. The same names appear in the demo, so viewers can follow each person.
- **Voice-over (61 words, 6 optional):**
> Three illustrative people, based on our research. Ravi, fifty-eight, goes home after abdominal surgery. He forgets the exercise, or breathes too fast, and nobody sees. Sister Anjali, his ward nurse, teaches it once and can't check every patient every hour. His son Amit works in Bengaluru; he worries, but can only ask on the phone. ((Everything we built serves these three.))

**The three personas** (illustrative, based on our research – not real people; the names match the fake demo data in `backend/app/seed.py` and `backend/app/comms/seed_comms.py`):

| Persona | Who | Their pain | What SpiroBuddy does for them |
|---|---|---|---|
| **Ravi, 58** – the patient | Going home to Lucknow after abdominal surgery; speaks Hindi; uses the family phone | Told to do 10 slow breaths every waking hour, he forgets or breathes too fast, and nobody sees. Forgetting is the top reason in a US nurse survey (83.5%); in Chennai only 6% did it right on day 1; only 41% of older Indians own a smartphone | A voice coach in Hindi for every breath ("slower… hold… well done"), one big Start button, nothing to read or type, and a safety button with one fixed message (Live; breaths Simulated) |
| **Sister Anjali** – the ward nurse | Nurse on a busy post-operative ward; teaches the exercise once, at discharge | Can't check every patient every hour: India has 2.6 nurses per 1,000 people, below WHO's 3; in a US survey 86% of nurses said patients don't use the exerciser properly | One list, most urgent first, with sessions done ÷ due for each patient; alerts only when someone needs a call; fixed rules, not AI (Live) |
| **Amit** – the son, far away | Works in Bengaluru, far from his parents' home | Worries, but can only ask "did you do it, Papa?" on the phone. Two in three older Indians live with their children, and only 41% own a smartphone, so the family's phone is the channel | With Ravi's consent, Amit opts in: a private family page with today's ticks and a cheer Ravi hears after his next session (Live); a short daily WhatsApp update (In development: previews today) |

Sources: `docs/research/PITCH_FACTS.md` #5, #6, #9, #10, #12, #13, #15 (`KNOWLEDGE_BASE.md` F-ADH-2, F-ADH-6, F-INDLOC-3, F-INDLOC-7, F-ADH-7, F-INDIA-5, F-INDIA-7). The same cards are slide 3 in `PITCH_PLAN.md`.

### Shot 5 · 1:28–1:58 · Architecture
- **Covers:** the architecture you are using.
- **On screen:** `docs/hackathon/architecture.png`, full screen (**F11**). Optional: in the editor, zoom slowly from the left column to the right as you speak. Every box carries one of the four status words.
- **Voice-over (70 words, 9 optional):**
> Our architecture. The laser base is in development; today a simulator sends the breaths. The phone app is live and talks to our server, with the database in Mumbai. AI sits in three places: a breath model, with rules as backup; Sarvam voices recorded in eleven languages; and Claude summaries, in development, with a fixed-text backup. ((Danger words are caught by fixed lists, not AI.)) WhatsApp and calls are previews today.

### Shot 6 · 1:58–2:14 · Demo, part 1: the base unit (In development)
- **Covers:** detailed demo (the part still in development, labelled as such).
- **On screen:** `showcase/` 3D showroom. Its chip already says "3D concept model · sizes from published specs". Click **Side** (Camera), then **Good** (or key **1**) to show the disc rising and the laser beam. Or use **tour.mp4** from 0:10 to 0:16 and from 0:34 to 0:47. **Skip tour 0:20–0:34**: its captions name an older board and battery.
- **On-screen label (add in the editor):** *"In development – 3D concept with sourced sizes · firmware written · not built or bench-tested"*.
- **Voice-over (38 words):**
> Now, in development: the base. This is a 3D concept with sourced dimensions; it is not built yet. In the design, the exerciser stands on it and, like InSee in US hospitals, a laser sensor reads the disc.

### Shot 7 · 2:14–2:52 · Demo, part 2: Ravi's phone (Live, breaths Simulated)
- **Covers:** detailed demo; persona Ravi.
- **On screen:** `app.html?id=1`, phone size, in Hindi.
  1. Click the big teal button **व्यायाम शुरू करें** (Start). Demo-breath buttons appear under it.
  2. Click **Good breath** (or key **G**). Stay silent for about 5 seconds: the coach speaks Hindi, and the English words show under the Hindi line (these are your subtitles).
  3. Click **Too fast** (key **F**): the frame turns amber and the coach says "धीरे…" (slower).
  4. Click **अभी समाप्त करें** (Finish now): "Session saved", and today's ticks update.
  5. Tap **English**, then **தமிழ்** (Tamil), then **English** again. Leave it in English for shot 8.
- **On-screen label (add in the editor):** *"Live app · breaths Simulated (no device yet)"*.
- **Voice-over (68 words, 3 optional):**
> This is Ravi's app, live, on a family phone. The breaths are simulated. **[Good breath]** Listen. **[pause while the coach speaks]** **[Too fast]** Too fast: it says "slower" at once, and the frame turns amber. Our model scores each breath; it is trained on simulated breaths, so real-patient accuracy isn't measured yet, and rules back it up. **[Finish now]** The session saves itself. ((Nothing to type.)) **[English, Tamil]** Voice coaching is recorded in eleven languages, ten Indian plus English; the app's screens run in four today.

### Shot 8 · 2:52–3:03 · Demo, part 3: the safety button (Live)
- **Covers:** detailed demo; persona Ravi.
- **On screen:** same app, in English. Scroll down, click **I do not feel well**. A red box shows "Please contact your nurse now. If it is an emergency, call 112", then "Your nurse has been told". **Do not click "Call 112".**
- **Voice-over (24 words):**
> One safety button. It always shows the same fixed message, contact your nurse or call 112, and alerts the nurse. No AI decides this.

### Shot 9 · 3:03–3:23 · Demo, part 4: Sister Anjali's dashboard (Live)
- **Covers:** detailed demo; persona Sister Anjali; the impact metric live in the product.
- **On screen:** **Ctrl + Tab** to the dashboard (`/`). It refreshes every 2 seconds. Point with the mouse at: Ravi at the top of the list with **Red flag** and **Needs a call**; then the **Sessions today** tile ("x / y" and "z% of sessions due so far"); then Ravi's "x of y due" bar.
- **Voice-over (42 words, 8 optional):**
> Now Sister Anjali's screen, live. Every patient, most urgent first. Ravi is at the top with his red flag. This tile is our impact metric: sessions done out of sessions due so far today. ((Every row shows the same for one patient.))

### Shot 10 · 3:23–3:36 · Demo, part 5: Ravi's page and the summary
- **Covers:** detailed demo; the AI summary, honestly labelled.
- **On screen:** click Ravi's row (opens `patient.html?id=1`). Scroll to **AI summary** → click **Generate AI summary**. The tag next to it says **Template** on the live site.
- **Voice-over (25 words):**
> On Ravi's page, one click makes a short progress summary. Claude-written summaries are in development; this live site shows the fixed-text version. It never diagnoses.

### Shot 11 · 3:36–3:56 · Demo, part 6: missed sessions and the reminder ladder
- **Covers:** detailed demo; consent; honest "previews".
- **On screen:** **Ctrl + Tab** to `demo.html`.
  1. On Ravi's card ("Live demo patient") click **Simulate 2 missed slots** (key **X**). The result line says the slots are marked missed.
  2. Scroll to **Calls & WhatsApp – live simulators** (Patient: Ravi Kumar) → click **Play escalation ladder (≈60 s)** (key **L**). Record about 15 seconds: the unit's light, the WhatsApp reminder with three buttons on "Ravi's phone", the ladder steps. Then stop.
- **On-screen label (add in the editor):** *"Previews – real WhatsApp and calls In development"*.
- **Voice-over (40 words):**
> If Ravi misses two sessions, a reminder ladder starts: a message on his phone, then the family member who opted in, with Ravi's consent, then a nurse alert, and the nurse calls. These sends are previews, not real messages yet.

### Shot 12 · 3:56–4:08 · Demo, part 7: Amit's family page (Live)
- **Covers:** detailed demo; persona Amit.
- **On screen:** **Ctrl + Tab** to `guardian.html?t=ravi-amit-demo` (or click **Family page** in the simulators card). Tap **English**. Show the status card, today's hour-by-hour ticks and **Send a cheer**. **Do not press the Call button** (it would try to dial).
- **Voice-over (25 words):**
> And Amit's family page, live: a private link and no login. Today's ticks, a one-tap call, and a cheer Ravi hears after his next session.

### Shot 13 · 4:08–4:39 · Adoption and retention (estimates)
- **Covers:** estimated user adoption and retention (organisers' second answer); personas again (each step names who acts).
- **On screen:** deck slide 7b, a six-step journey with one number per step and the word **estimate**, **assumption** or **target** under each number. Full table with sources and what the pilot measures: `PITCH_PLAN.md`, block "Adoption and retention – our assumptions". The card shows:

| Step | Who | Number (per hospital department, per month) | Label |
|---|---|---|---|
| 1 Reach | the hospital | about 50 eligible patients | estimate |
| 2 Join | Ravi (consents) · Amit (opts in) | 40 join (8 in 10) · 24 families opt in (6 in 10 of those who join) | assumption |
| 3 Start | Ravi | 36 do a home session on day 1 (9 in 10) | assumption |
| 4 Stay | Ravi | still going: 34 on day 3 · 30 on day 7 · 26 on day 14 (85% · 75% · 65%) | assumption |
| 5 Do | Ravi · Sister Anjali | about 58% of due sessions done · the nurse opens the list on 9 days in 10 | target · assumption |
| 6 Pay | the hospital | 1 pilot hospital in 3 goes on to pay | target |

  Footnote on the card: *"Estimates, not results. Basis: plan 03 §3 and plan 05 (volumes); Lung India 2025 and Indian J Med Res 2025 (home rehab); Respira Health (self-reported); LASI; Eltorai, JAMA Surg 2019; our arithmetic. A pilot of 30–50 patients measures every step."*
- **Voice-over (67 words, 5 optional):**
> Adoption and retention, as estimates, not results. One hospital department: about fifty eligible patients a month. We assume forty join and thirty-six start on day one; three in four are still going at day seven, two in three at day fourteen. Six in ten families opt in ((and nurses check the list daily)). One pilot hospital in three goes on to pay. A pilot of thirty to fifty patients would test every step.

### Shot 14 · 4:39–5:08 · Scalability model
- **Covers:** the scalability model.
- **On screen:** `units.html` (after **Reset mock units**). The page itself says "Mock-up for the demo. No real units exist yet". Point at the list (who has each unit, battery, where it is in its cycle). On **SB-0011** click **Take back** → **Clean and check** (tick the three boxes, **Sign as cleaned**) → **Wipe unit**: it returns to "In stock". Then cut to deck slide 8 for the last 8–10 seconds (₹2,500 parts per unit, estimate · about 10 loans per unit, assumption · about ₹1,000 per patient episode, planned price, estimate · ₹0.12 per WhatsApp update).
- **On-screen label (add in the editor):** *"In development – mock-up, no real units yet"*.
- **Voice-over (69 words):**
> How it scales. Units would be lent and reused, so hospitals would buy no hardware. This screen is a mock-up, in development. By design, a unit stores nothing about a person, so after cleaning it moves to the next patient with one scan. Parts should cost about two thousand five hundred rupees a unit, and we plan to charge about one thousand rupees per patient episode; both are estimates.

### Shot 15 · 5:08–5:25 · Future roadmap
- **Covers:** the future roadmap.
- **On screen:** deck slide 10: four steps (1 bench-test one unit · 2 record real breaths, retrain · 3 ethics committee and CDSCO's written view · 4 pilot, 30–50 patients, one hospital), then a **Planned** row: speaking base with a SIM · three-ball reader (phone camera) · TB lung rehab.
- **Voice-over (41 words):**
> Our roadmap: bench-test one unit, record real breaths and retrain, get ethics approval and the regulator's written view, then the pilot. Planned after that: a speaking base for patients without a smartphone, a reader for three-ball exercisers, and TB lung rehab.

### Shot 16 · 5:25–5:34 · Honest status and close
- **Covers:** readiness (TRL) and the close.
- **On screen:** 5 seconds of deck slide 9 as a still card: *"Live: the software (TRL 4). Simulated: the breaths. In development: the base unit (TRL 3), Claude summaries, live Sarvam voice, real WhatsApp and calls. Planned: speaking base, three-ball reader, TB rehab."* Then deck slide 1 with the tagline. No music.
- **Voice-over (22 words):**
> Honestly: the software is live, TRL four; the device is in development, TRL three. SpiroBuddy: every breath, coached and counted. Thank you.

### Totals

| Shot | Section | Time | Words (optional) |
|---|---|---|---|
| 1 | Theme | 0:00–0:11 | 25 |
| 2 | Problem | 0:11–0:41 | 70 (4) |
| 3 | Impact | 0:41–1:02 | 49 |
| 4 | Personas | 1:02–1:28 | 61 (6) |
| 5 | Architecture | 1:28–1:58 | 70 (9) |
| 6 | Demo: base unit (In development) | 1:58–2:14 | 38 |
| 7 | Demo: Ravi's app | 2:14–2:52 | 68 (3) |
| 8 | Demo: safety button | 2:52–3:03 | 24 |
| 9 | Demo: Sister Anjali's dashboard | 3:03–3:23 | 42 (8) |
| 10 | Demo: summary | 3:23–3:36 | 25 |
| 11 | Demo: reminder ladder | 3:36–3:56 | 40 |
| 12 | Demo: Amit's family page | 3:56–4:08 | 25 |
| 13 | Adoption and retention (estimates) | 4:08–4:39 | 67 (5) |
| 14 | Scalability | 4:39–5:08 | 69 |
| 15 | Roadmap | 5:08–5:25 | 41 |
| 16 | Status and close | 5:25–5:34 | 22 |
| | **Total** | **5:34** | **736 (35 optional)** |

Times assume about 143 words a minute plus the pauses in shot 7. **Time your first full take:** over 5:50 → drop the ((optional)) words (saves about 15 seconds); under 5:05 → slow down and let the app finish speaking in shot 7.

---

## After recording: join, label, export (Clipchamp, free in Windows 11)

1. Press **Start**, type **Clipchamp**, open it → **Create a new video**.
2. Click **Import media** and add your clips. Drag them onto the timeline in shot order.
3. Trim each clip: click it, drag its ends to cut silences and mistakes.
4. Add the on-screen labels (shots 6, 7, 11, 14): click **Text** on the left → drag **Plain text** onto the timeline above the clip → type the label → place it in a top corner, at least 28 px high.
5. No music. If you want any, use only a track that Clipchamp marks as free to use (`docs/plan/09_DOMAIN_SWEEP.md` DS-35).
6. Click **Export** → **1080p**. Name the file `SpiroBuddy_demo.mp4`.
7. Watch the whole file once, start to finish: sound on every shot, length between 5:00 and 6:00, no real names, numbers or emails visible.

## Getting under 100 MB

A 5½-minute 1080p export is often 100–250 MB. If yours is over 95 MB, either export again at **720p**, or tell Claude the file name: Claude will shrink it to about 85 MB at full 1080p with a two-pass encode (about 2 Mbit/s video, 128 kbit/s sound), which keeps screen text sharp.

## Shortcuts that help while recording

- **Patient app keys:** `G` good breath · `F` too fast · `S` too shallow · `N` no hold · `A` full 10-breath session.
- **Demo panel keys (for Ravi):** `G` good session · `M` mixed · `P` poor · `X` 2 missed slots · `S` send summary to family · `L` play the reminder ladder.
- **3D showroom keys:** `1`–`4` breath types; `←` `→` tour chapters.
- If something looks wrong, click **Reset demo data** and record that shot again.

## If the internet fails

Run it on the laptop: start the server (`scripts\run.ps1`) and use `http://localhost:8000` in place of `https://spirobuddy.onrender.com`. Everything in this list works the same. If you record the summary shot (10) on the laptop with an Anthropic key in `.env`, the tag shows "AI (Claude)" instead of "Template": then say "recorded on our laptop with the AI key switched on", not "live".

## Hindi version (if you record in Hindi)

Keep the slides in English. Keep numbers, "SDG 3", "TRL", "WhatsApp" and "AI" in English. Hindi runs 10–15% longer: drop all ((optional)) words first. The never-say list applies in Hindi too (`PITCH_PLAN.md` §3, Hindi note).
