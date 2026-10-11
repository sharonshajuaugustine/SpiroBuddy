# Scaling and cost: from today's demo to many hospitals, and "are the AIC servers enough?"

**Written:** Sun 11 Oct 2026 · **Answers:** the founder's ask of 11 Oct (scaling, cost, AIC servers, easy moving) · **Confidence:** medium for the load arithmetic, **low** for every rupee figure beyond the pilot (no quotes, no load test yet).

**How to read this file**
- **FA** = `docs/FUTURE_ARCHITECTURE.md`. **plan 03** = `docs/plan/03_COSTS_AND_BUDGET.md`. **B3-x** = `docs/research/business/03_scale_funding_unit_economics.md`.
- Every number is a **fact** (with its file), or is labelled **estimate**, **assumption** or **target**. "Derived" = our arithmetic on repo numbers. "Ours" = this file's own guess, with no outside source.
- Status words: **Live**, **Simulated**, **In development**, **Planned**. Today's set-up (section 2) is Live. Every stage from the pilot onwards is Planned. The hospital and patients in the demo are fictional.
- Money: ₹96 = US$1 (plan 03 header). ₹1 lakh = ₹1,00,000. No salaries are included anywhere (plan 03 header).

> ## 1. Answer in 10 lines
> 1. **Today (Live):** one web service, one database and one keep-awake job run the demo. Hosting costs ₹0 a month. Fictional patients only.
> 2. **One patient is a light load:** about 7 sessions, 70 stored breaths (about 21 kB), 3 WhatsApp messages and 1 AI summary a day (estimates and assumptions, FA §1.1).
> 3. **Five stages:** Demo → Pilot (1 hospital, 25–50 patients at once) → 10 hospitals (about 250) → about 100 hospitals (2,500–5,000) → National (100,000+).
> 4. **The shape never changes:** one web service plus one database. Parts are added only when a named trigger happens (section 4).
> 5. **Cost to us per 14-day patient episode, unit lent:** about ₹670 in a pilot, about ₹470 at scale (estimates, plan 03 §2.2). **Planned price: about ₹1,000** (estimate).
> 6. **Monthly running cost, no salaries:** ₹32,000–59,000 for one hospital, ₹2.8–3.8 lakh for ten, ₹25.8–30.2 lakh for a hundred (estimates, plan 03 §3).
> 7. **Servers are the small part.** The unit's wear and loss is ₹375 of every lent episode. Free servers would save at most the hosting line: ₹5,500–21,000 a month at one hospital.
> 8. **AI and voice stay flat:** the AI reads a document only when it is uploaded, limits sit in the settings, and typed entry and recorded voice clips are the fallbacks.
> 9. **AIC servers:** we have no specification for them, so we answer by use. Good for building, testing, a rehearsal copy, training the small breath model and demos. **Not enough on their own for real patient records** unless the 10 conditions in section 7b hold in writing. The core product needs no graphics card.
> 10. **Moving hosts is 7 steps.** Estimated downtime at pilot size: 15–30 minutes (estimate, not rehearsed). Moving hospital data: `docs/INTEROPERABILITY.md`.

## 2. Where we are today (Live)
| Piece | What runs today | Source |
|---|---|---|
| Web service (the program that answers the app and the web pages) | One Python service on Render, free plan, region Singapore. It serves the website and the API (the list of requests the server accepts). Every push to `main` redeploys it | `render.yaml`; DEPLOY Part 2, "Good to know" |
| Database | One Supabase project (a hosted Postgres database). If its keys are missing, the server falls back to a built-in demo database | DEPLOY Parts 1 and 3; FA §0 |
| Keep-awake job | A Supabase timed job, `keep-spirobuddy-awake`, opens the health page every 5 minutes so the free service does not fall asleep | HANDOFF "Keep-awake" (`supabase/keepalive.sql`) |
| Data | 7 fictional patients, rebuilt automatically when the data is more than a day old. Breaths in the demo are **Simulated** | DEPLOY Part 1 step 6, "Good to know" |
| Cost | **₹0 a month** for hosting: both services are on free plans. AI, voice and message keys are optional and off by default | DEPLOY "In short", "Optional keys" |

**Limits today (facts).** Right for a demo with fictional data; not usable for real patients as it stands (FA "In plain English", point 1):
1. The free web service sleeps after 15 minutes without visitors, and its own disk is wiped on every restart (DEPLOY "Good to know").
2. A free database project pauses after a week without use (DEPLOY Part 3 table).
3. There is no login: the site runs in demo mode (FA §0, "Login").
4. Render has no India region, so the web service sits in Singapore (FA §0, "Hosting"). The database region is Mumbai if it was offered at set-up, otherwise Singapore (DEPLOY Part 1 step 2.3) – founder to confirm which.
5. The reminder timer runs inside the web service, so only one copy of the service can run (FA §0, "Background work").
6. The Live tables do not record which hospital a row belongs to (FA §0, "Tenancy"). The 2.0 tables add that tag (`supabase/schema_v2.sql`): **In development**.

## 3. The load model: what ONE patient creates per day
A **request** is one message from the app or a web page to our server. A **row** is one line in a database table.

| # | Input | Value | Label and source |
|---|---|---|---|
| a | Hourly session slots a day | 14 (08:00 to 21:00) | **Fact** – `backend/app/config.py`, `FIRST_SLOT, LAST_SLOT = 8, 21` |
| b | Breaths per session | 10 | **Fact** (design) – FA §1.1; ARCHITECTURE Contract D (`breaths?:10`) |
| c | Share of slots actually done | 50% | **Assumption** – FA §1.1. Shot 13 of the video uses a **target** of about 58% |
| d | Uploads per session | 1 (`POST /api/sessions` carries all 10 breaths) | **Fact** – ARCHITECTURE Contract D |
| e | Size of one stored breath row | about 300 bytes (measurements only, no raw curve) | **Estimate** – FA §1.1 |
| f | Requests per session | about 15: open the app (about 4), classify each of 10 breaths, 1 upload | **Estimate** – ours, not measured; `web/js/api.js` calls `/api/classify` and `/api/sessions` |
| g | WhatsApp messages a day | about 3 | **Assumption** – FA §1.1 |
| h | Automated phone calls | about 1 a week | **Assumption** – FA §1.1 |
| i | AI summaries | 1 a day | **Estimate** – FA §1.1 (about 50 a day for about 50 patients), §11 |
| j | AI reads of a document | only when a file is uploaded | **Fact** (design; the feature is In development) – `render.yaml`, `.env.example` |
| k | Uploaded files per episode | 2 files of about 1 MB | **Assumption** – ours; the repo has no figure; the pilot must measure it |
| l | Episode length | 14 days | **Assumption** – plan 03 §2.2 |

| Step | Sum | Per day | Per 14-day episode |
|---|---|---|---|
| 1 Sessions | 14 slots × 50% | 7 | 98 |
| 2 Breath rows | 7 × 10 | 70 (140 if every slot is done) | 980 |
| 3 Bytes stored | 70 × 300 bytes | 21,000 bytes ≈ 21 kB | ≈ 0.3 MB |
| 4 App requests | 7 × 15 | ≈ 105 | ≈ 1,470 |
| 5 WhatsApp | 3 × ₹0.115 (COMMS §9) | 3 messages, ₹0.35 | 42 messages, ≈ ₹5 |
| 6 Phone calls | 1 a week × about 2 minutes × ₹3.50 (COMMS §9) | – | 2 calls, ≈ ₹14–16 |
| 7 AI calls | 1 summary a day + 1 read per uploaded file | 1 | ≈ 16 |
| 8 Files | 2 × 1 MB | – | ≈ 2 MB |

**Check:** 50 patients × 70 = 3,500 breaths a day, the same as FA §1.1. One patient place kept filled for a year stores 70 × 365 = 25,550 rows ≈ 7.7 MB. At the 58% target the daily figures are about one sixth higher (8 sessions, 81 rows).

**The peak.** Patients breathe at the top of each hour, so load comes in bursts. FA §1.1 gives the worst case: under 5, about 100 and about 2,000 breaths a second for 50, 5,000 and 100,000 active patients – about one breath a second for every 50 active patients. With input f (15 requests for 10 breaths), **peak requests a second ≈ active patients ÷ 33** (derived). Our softer case (half the patients, spread over 10 minutes) gives about 40% of that (active patients ÷ 80). We size for the worst case, because the server must survive the worst hour.

**Staff screens add to it.** Today each open dashboard asks for fresh data every 2–3 seconds (FA §8.4; `web/js`), about 0.5 requests a second per open screen. If 1 in 5 staff has a screen open (**assumption**, ours), FA §1.1's staff counts (10, 500, 10,000) give about 1, 50 and 1,000 requests a second. This is why FA §8.4 plans to replace the repeated asking with a pushed feed at the multi-hospital stage.

## 4. The scaling stages
Stage names follow FA §1.1 (Pilot, Multi-hospital, National). The Multi-hospital phase is split in two so it lines up with plan 03 §3 (10 and 100 hospitals). **Only Stage 0 is Live. Stages 1–4 are Planned.**

| | **Stage 0 – Demo (today)** | **Stage 1 – Pilot (1 hospital)** | **Stage 2 – Multi-hospital (10 hospitals)** | **Stage 3 – Multi-hospital (about 100 hospitals)** | **Stage 4 – National (state or national programme)** |
|---|---|---|---|---|---|
| Active patients at once | 7 fictional (DEPLOY) | 25–50 (plan 03 §3; FA §11) | about 250 (plan 03 §3) | 2,500 (plan 03 §3) to 5,000 (FA §1.1) | 100,000+ (FA §1.1) |
| Peak requests a second (estimate, section 3) | under 1 | about 2–3 | about 10–20 | about 100–200 | about 1,250–3,000 (softer case to worst case) |
| Breath data added a year (300 bytes a row) | none kept: demo data rebuilds itself | 0.6–1.3 million rows ≈ 0.2–0.4 GB (FA §1.1: about 1 million, 0.3 GB) | about 6.4 million rows ≈ 2 GB (derived) | 64–128 million rows ≈ 19–38 GB (FA §1.1: about 40 GB at 5,000) | about 2.5 billion rows ≈ 750 GB (FA §1.1) |
| Files added a year (assumption k) | none | 1.2–2.4 GB | about 12 GB | 120–240 GB | about 4.8 TB |
| What it runs on | 1 free web service (Singapore), 1 free database, keep-awake job | 1 web service + 1 background worker in Mumbai; Mumbai database with rewind backups (FA §3.5, §11) | Same shape; a rehearsal copy added (FA §8.1, §14) | Several copies of the web service, queue workers, larger database with a second read-only copy (FA §1.2, §11) | Many web servers, main database plus copy, a standby in a second Indian region (FA §8.6, §11) |
| What must change, and the trigger | – | India hosting, staff login and roles, a record of who looked at what, consent records, backups, hospital tag on every row, versioned API, outside security test. **Trigger: a signed pilot agreement** (FA §1.2) | The database itself blocks one hospital from another's rows; an automated check proves it; on-call person. **Trigger: the 2nd hospital signs** (FA §14) | Hospital single sign-on, WhatsApp bought direct from Meta, breath table split by month, reminder timer moved to queue workers, pushed feed for dashboards. **Hard trigger: the 3rd hospital** (FA §1.2, §14, §8.4) | Read-only database copy, second region, managed queue, second message provider, on-call day and night. **Trigger: about 20,000 active patients or a government contract** (FA §1.2, §14) |
| Monthly running cost, units lent, no salaries (estimate) | ₹0 hosting | ₹32,000–59,000 (plan 03 §3) | ₹2.8–3.8 lakh (plan 03 §3) | ₹25.8–30.2 lakh at 2,500 active (plan 03 §3) | Technology only: about ₹50–60 lakh (FA §11 × 100,000). Units, people and travel: **not yet costed** |
| Same, hospital owns the units (estimate) | – | ₹12,000–40,000 | ₹0.8–1.8 lakh | ₹6.0–10.5 lakh | not yet costed |
| Cost to us per 14-day episode, unit lent (estimate) | not applicable | **≈ ₹670** (plan 03 §2.2) | ≈ ₹500–540 (derived: the §2.2 pilot column with server share ₹21,000–40,000 ÷ 500 episodes) | **≈ ₹470**–490 (plan 03 §2.2; derived for 2,500 active) | ≈ ₹450 (derived: §2.2 with FA §11 National lines) |

**All-in check (derived from plan 03 §3, which also counts company overheads and travel):** monthly total ÷ episodes = ₹640–1,180 at one hospital (50 episodes), ₹560–760 at ten (500), ₹516–604 at a hundred (5,000).

**Storage notes:** episodes a year = active patients × 24 (plan 03 §3: 25 active = 50 episodes a month). Allow about twice the breath-data figure for indexes and the other tables (**estimate**, ours). Raw breath curves are not kept by default: FA §1.1 keeps them only for a small consented sample.

**Where two repo sources disagree, and which one this file uses**

| Topic | Source A | Source B | Used here, and why |
|---|---|---|---|
| Exchange rate | ₹88 = US$1 (FA §11) | ₹96 (plan 03 header) | ₹96: newer file. FA's hosting totals of ₹19,000 / ₹1.6 lakh / ₹7 lakh become ₹21,000 / ₹1.78 lakh / ₹7.7 lakh (plan 03 §4) |
| Pilot size | about 50 active (FA §11) | 25 active, 50 episodes a month (plan 03 §3); the video's shot 13 assumes 40 of about 50 eligible join | Range 25–50; money follows plan 03 §3. This file adds no adoption numbers of its own |
| Patients per hospital | 10–50 hospitals carry about 5,000 active, so 100–500 each (FA §1.1) | 25 active each (plan 03 §3) | 25 each for money (the cautious figure). 5,000 is the size the Multi-hospital design must carry |
| Unit parts cost | ₹1,500 (B3-6); ₹1,000–1,700 (FA §11 note) | about ₹2,500 before GST (plan 03 §2) | ₹2,500: newest, from the hardware review, and what shot 14 of the video says |
| Sessions done | 50%, assumption (FA §1.1) | about 58%, target (video shot 13) | 50% for averages, 100% for the peak |
| WhatsApp messages a day | about 3 (FA §1.1) | an example of 14 reminders a day, ₹1.6 (COMMS §9) | 3. At 14 a day the episode line would be about ₹23, not ₹5 (derived) |

## 5. What grows with patients, and what does not
| Does **not** grow with each patient (fixed) | Grows with each patient |
|---|---|
| Hosting base: about ₹21,000 a month at pilot size, ₹1.78 lakh at about 5,000 active, ₹7.7 lakh at 100,000 (estimate, plan 03 §4 from FA §11) | WhatsApp: ₹0.115 a message, about ₹5 an episode (COMMS §9; plan 03 §2.2) |
| People: on-call, support leads, regulatory work – **not yet costed** (plan 03 header; FA §11 note) | AI phone calls: ₹3.50 a minute, about ₹18 an episode with nurse calls (COMMS §9; plan 03 §2.2) |
| Company overheads: ₹1,100–5,400 a month at one hospital (estimate, plan 03 §3) | AI summaries: about ₹8 an episode in a pilot, ₹4 at scale (estimate, plan 03 §2.2) |
| One-off checks, for example the outside security test: ₹40,000–3,50,000 (plan 03 §4, grade C) | Voice: about ₹9, falling to ₹5 (estimate, plan 03 §2.2) |
| Field visits, per hospital not per patient: ₹3,000–10,000 a month (estimate, plan 03 §3) | The unit's wear, loss and cleaning: ₹250 + ₹125 + ₹20; human support: ₹25 (plan 03 §2.2) |

Per active patient per month, technology only: about ₹450 at pilot size, ₹85–110 at about 5,000 active, ₹50–60 at 100,000 (estimate, FA §11). The fall is the fixed bill being shared by more patients.

**The cost of one 14-day patient episode (unit lent; estimate, plan 03 §2.2)**

| Cost line (₹) | Pilot (about 50 active) | Scale (about 5,000 active) | Basis |
|---|---|---|---|
| Unit share: ₹2,500 parts ÷ 10 loans | 250 | 250 | parts: estimate; 10 loans: assumption |
| Loss and breakage, 5% of a unit | 125 | 125 | assumption |
| Cleaning and check | 20 | 20 | assumption |
| WhatsApp | 5 | 5 | fact × assumption (section 3) |
| Voice | 9 | 5 | estimate |
| AI phone calls (about 2) | 18 | 18 | estimate |
| AI summaries | 8 | 4 | estimate |
| Server share (half a patient-month) | 213 | 18 | estimate |
| Human support (about 5 minutes) | 25 | 25 | assumption |
| **Total** | **≈ 673** | **≈ 470** | |
| Left over at the planned price of ₹1,000 | +327 | +530 | plan 03 §2.3, before GST |

**If the hospital owns the units,** our cost is messaging, voice, calls, AI, server and support only: about ₹278 a patient in a pilot and about ₹75 at scale (estimate, plan 03 §2.5). **What this means:** the unit's wear and loss is ₹375 of the ₹470. At 100 hospitals it is about ₹18.75 lakh of the ₹25.8–30.2 lakh monthly total, while hosting is ₹1–1.8 lakh (plan 03 §3). At national size the lend model's unit line would be about ₹7.5 crore a month (derived: 2,00,000 episodes × ₹375). So the decisions that move cost are the unit's price, how many patients share it and who owns it – not the servers.

## 6. Keeping AI and voice costs flat
| Rule | Why it keeps cost flat | Status |
|---|---|---|
| The AI reads a prescription or a document **only when it is uploaded** | AI reads follow the number of files (a few per episode), not the number of breaths (980 per episode) | **In development** (`render.yaml`, `GEMINI_API_KEY` comment) |
| Limits in the settings: 300 AI calls a day for the whole site, 20 an hour per visitor, 30 uploads an hour per visitor | One visitor or one fault cannot run up a bill | Setting names and defaults: **Live** (`.env.example`, `render.yaml`, `backend/app/config.py`). The code that enforces them: **In development** (on 11 Oct only `config.py` reads them) |
| Typed entry is the fallback | With no AI key, or when a limit is hit, staff type the prescription lines. Cost: ₹0 | **In development** (`render.yaml` header) |
| Daily summary: short, with a template fallback | One call per patient per day, capped at 400 output tokens (word pieces); template text if there is no key or the call fails | **Live** (`backend/app/llm.py`; DEPLOY "Optional keys") |
| A smaller AI model and batch pricing for summaries at scale | Takes the summary line from about ₹17 to about ₹1 per patient per month (estimate, FA §11) | **Planned** |
| Voice: recorded clips first | Coaching cues are fixed sentences, so they are recorded once. Made voice audio is cached. Browser voice is the fallback | **Live** (DEPLOY "Optional keys", "Good to know"). Voice cost: ₹0–18 falling to ₹0–5 per patient per month (estimate, FA §11) |

**One thing to change later:** the 300-a-day limit protects the free plan. At one summary per patient per day it covers at most 300 active patients (derived), so it must be raised, on purpose, from Stage 2 onwards.

## 7. "Are the AIC servers enough?"
**How we read the question.** "AIC servers" = servers the team can use through its incubation centre (AIC = Atal Incubation Centre, India's government-backed incubator programme). **Founder: please confirm this reading.** The repo holds no specification for them: no processor, memory, disk, graphics card, internet line, uptime, or name of who looks after them. So this section does not guess one. It answers by use. B3-12 found no incubator's standard terms in public either, and says to ask in writing.

### 7a. Short answer, by use
| Use | Real patient data on it? | Are such servers a fit? | Evidence |
|---|---|---|---|
| Building the software, automated test runs, demos | No: fictional data | **Yes** | FA §8.1: the `dev` and `demo` levels hold fictional data only |
| Training the small breath model | No, when trained on made-up or team-recorded breaths | **Yes** | It trains on an ordinary processor: today it trains inside the free Render build (`render.yaml` build command; FA §0 "ML") |
| A rehearsal copy ("staging") and load tests | No: fictional data plus made-up load | **Yes – the best use** | FA §8.1. A load test there would replace the estimates in 7c |
| An extra encrypted backup copy | Yes, encrypted | **Only if conditions 3, 4, 6, 7 and 8 hold** | FA §3.4 asks for a nightly encrypted copy in a separate account in India |
| Pilot with real patient records | Yes | **Not on their own.** Only if all 10 conditions hold, in writing | FA §8.4: up 99.5% of the month (at most 3.6 hours down) and a red-flag alert on the nurse's screen in under 60 seconds. FA §8.6: lose at most 5 minutes of data, be back within 4 hours. FA §3.4, §3.5 |
| Ten or more hospitals | Yes | **Not as the only home** | FA §8.4: 99.9% (at most 43 minutes down a month). FA §8.6: back within 1 hour, with a second database copy and a duty rota |

### 7b. The conditions (all 10, in writing, before any real patient record goes there)
1. A fixed public address, a domain name and a web certificate, reachable from hospital networks and by the WhatsApp and call providers (their call-backs need a public address: DEPLOY "Good to know").
2. Power backup and a measured uptime record of at least 99.5% a month, including holidays and campus shutdowns (FA §8.4).
3. Backups: continuous, so at most 5 minutes of data can be lost, plus a nightly encrypted copy kept off-site in a separate account, with a restore tested every quarter (FA §3.4, §8.6).
4. The servers are in India, and logs stay in India for 180 days (FA §3.5, §8.3).
5. A named person on call, with a phone number, who can bring the service back within 4 hours (FA §8.6).
6. A named owner for security updates and for the firewall (the filter that blocks unwanted connections).
7. Encrypted disks, our own separate login area (not shared with other start-ups), and a log of who logged in and who entered the server room.
8. A written data-processing agreement that names the AIC or its host institute, and that the pilot hospital accepts (FA §1.2 lists a signed agreement with the hospital).
9. Monitoring that pages a person when the alert path or the server fails (FA §8.3).
10. An exit clause: how long we may stay after incubation ends, the notice period, our right to a full copy, and written proof that our data was wiped.

### 7c. Minimum server needed at each stage (estimate)
**Estimate – ours, not load-tested.** Basis: the peak load in section 4; a working guess that one processor core handles roughly 20–50 of these small requests a second (**assumption**, ours); about 5 kB per request each way (**assumption**, ours); disk = two years of data and files, plus the same again for local backups. The line's reliability matters more than its speed: the data is tiny, and the real risk is a nurse missing an alert because a campus line dropped.

| Stage | Processor cores | Memory | Disk | Internet line | Basis |
|---|---|---|---|---|---|
| 0 Demo, or a rehearsal copy | 2 | 4 GB | 20 GB | any ordinary broadband | under 1 request a second; today it runs on Render's free plan |
| 1 Pilot | 2–4 | 8 GB | 50 GB | 10 Mbps is plenty (the load needs under 1 Mbps); fixed address; a second line as backup | about 3 requests a second; under 3 GB a year |
| 2 Ten hospitals | 4 | 16 GB | 100 GB | 50 Mbps, two lines | about 10–20 requests a second; about 14 GB a year |
| 3 About 100 hospitals | about 16, over at least 3 machines (2 web, 1 database, plus a database copy) | about 64 GB in total | 0.6–1.2 TB | 100 Mbps or more, two providers | about 100–200 requests a second; 140–280 GB a year |
| 4 National | Not a job for a few servers: a data-centre set-up | – | several TB a year | data-centre grade | 1,250–3,000 requests a second; FA §11 prices two large database machines |

**Graphics card: the core product needs none.** The breath model is small and runs on an ordinary processor. Prescription reading, summaries and voice are done by outside AI services over the internet. A graphics card would be needed only if we chose to run our own AI language or vision model on our own servers, for example for a hospital that lets no data leave its building. That is not planned.

### 7d. Fill-in table for the founder (ask the AIC, in writing)
| # | Fact to get | Their answer | Needed for |
|---|---|---|---|
| 1 | Which AIC, and who is our contact there? | | everything |
| 2 | How many servers, and are they ours alone or shared? | | 7b-7 |
| 3 | Processor cores and memory per server | | 7c |
| 4 | Disk size, and are the disks mirrored? | | 7c; 7b-3 |
| 5 | Graphics card: which, if any? | | only for an in-house AI model |
| 6 | Do we get full administrator rights, and can we install our own software? | | steps in 7f |
| 7 | Internet line: speed up and down, and is there a second line? | | 7c; 7b-2 |
| 8 | Fixed public address, and are web ports open to the internet? | | 7b-1 |
| 9 | Power backup hours; uptime over the last 12 months; planned shutdowns and holidays | | 7b-2 |
| 10 | City and building; who can enter the server room? | | 7b-4, 7b-7 |
| 11 | Who installs security updates and runs the firewall? Who is on call, and when? | | 7b-5, 7b-6, 7b-9 |
| 12 | Backups offered: how often, kept where, ever test-restored? | | 7b-3 |
| 13 | Cost: free or paid, for how long, and what happens when incubation ends? | | section 5; 7b-10 |
| 14 | Will they sign a data-processing agreement? | | 7b-8 |
| 15 | Any fee or equity asked in return? (B3-12) | | company decisions |

### 7e. Recommended set-up, in plain words
1. **Real patient records and the live service:** a managed cloud database and web service in an India region (Mumbai), as FA §3.5 plans. A managed service offers the rewind backups (a paid add-on, FA §3.4) and the upkeep that conditions 2, 3 and 5 ask for. Estimated cost at pilot size, add-on included: about ₹21,000 a month (plan 03 §4, from FA §11).
2. **AIC servers:** everything that holds no real patient data – building, automated tests, the rehearsal copy, load tests, training the breath model, demos.
3. **What this saves:** AIC servers can replace only part of the hosting line. They do not touch messages, calls, AI or the units, which are most of the cost (section 5).
4. **When an AIC or hospital-owned server becomes the right main home:** (a) a hospital insists its data stays on its own premises – FA §14 already plans a dedicated-database option for big customers; or (b) the AIC meets all 10 conditions in writing and the pilot hospital agrees.
5. **A caveat for that path:** today the server reaches its database through Supabase's own web interface (FA §0). A server without Supabase would need Supabase's self-hosted edition or a small adapter. Neither is built: **Planned**.

### 7f. Moving between hosts
The product is one web service plus one database, so a move is short. The same steps work in any direction: Render to Mumbai cloud, cloud to AIC, cloud to a hospital's own server.
1. **Prepare the new home:** install Python 3.12, fetch the code from GitHub, install the packages, start the service with the one start command (`render.yaml`).
2. **Copy the settings:** the values in `.env` (names in `.env.example`), entered by hand on the new host. Never through chat or email.
3. **Create the database there:** run the table-creation files (`supabase/schema.sql`, DEPLOY Part 1; `supabase/schema_v2.sql` for 2.0), then copy the data across.
4. **Copy the uploaded files** (the private `documents` store, `.env.example`).
5. **Test at the new address:** open `/api/health` and the dashboard (DEPLOY Part 3).
6. **Switch:** make the old site read-only, take a final data copy, point the web address at the new host, and update the public address used for WhatsApp and call call-backs (Render fills it in automatically; another host needs it set by hand – DEPLOY "Good to know").
7. **Keep the old home for a week** as a way back, then delete it.

| Size | Expected downtime (estimate, not rehearsed) | Basis |
|---|---|---|
| Demo today | 0–10 minutes | fictional data rebuilds itself; nothing to copy |
| Pilot (under 3 GB) | 15–30 minutes, at night | one small copy plus the address switch |
| About 100 hospitals (20–40 GB plus files) | 5–15 minutes with a live database copy on the new host; 1–2 hours without | files copied ahead; FA §8.6 plans a second database copy |
| National | minutes, rehearsed | switch to the standby copy (FA §8.6) |

The whole Singapore-to-Mumbai move is put at 2–3 days of work (estimate, FA §3.5), and must happen before any real patient. Moving a **hospital's own data** in and out (its existing patient software, exports, hand-back) is covered in `docs/INTEROPERABILITY.md`.

## 8. What we would watch as we grow (targets, FA §8.4 and §8.6)
All are **targets**, all **Planned**. None is measured today.

| What | Pilot | Multi-hospital | National |
|---|---|---|---|
| Red-flag alert visible to the nurse | under 60 s, 99.9% of the time | under 60 s, 99.9% | under 30 s, 99.95% |
| Red-flag WhatsApp or call to the nurse's phone | under 2 min, 99.5% | under 2 min, 99.9% | under 2 min, 99.9% |
| Service available in a month | 99.5% (at most 3.6 h down) | 99.9% (43 min) | 99.95% (22 min) |
| Dashboard freshness | under 5 s | under 5 s | under 5 s |
| Most data we could lose in a failure | 5 minutes | 1 minute | 1 minute |
| Time to be back after a failure | 4 hours | 1 hour | 30 minutes |

Also watched, with no target set yet: breath uploads a minute, the queue of unsent messages, AI fallback rate and AI spend, and cost per episode against section 5 (FA §8.3).

## 9. Say this in the video and the pitch
**Three sentences (45 words):**
1. "Today one web service and one database run our demo with fictional patients."
2. "Planned growth is staged: one pilot hospital, ten, a hundred, then state programmes."
3. "Each patient episode should cost five to seven hundred rupees, an estimate; our planned price is about one thousand."

On screen, keep the four figures shot 14 already shows: ₹2,500 parts per unit (estimate) · about 10 loans per unit (assumption) · about ₹1,000 per patient episode (planned price, estimate) · ₹0.12 per WhatsApp update.

**Do NOT say:**
- "Infinitely scalable", or any hospital count in the present tense. Stages 1–4 are Planned.
- "It costs ₹470", or any cost without the word estimate. No figure here is measured.
- "Hosting is free." It is free for the demo only.
- "Device plus software for ₹200" (plan 03 §2.6).
- "Data is stored in India." Today the web service is in Singapore.
- "The AIC servers will host patient data." There is no specification and no agreement.
- "Zero downtime" for a move, "compliant", "certified", "real-time monitoring", or any named hospital or customer.

## 10. Sources
| Repo source | Section used | Used for |
|---|---|---|
| `docs/FUTURE_ARCHITECTURE.md` | "In plain English", §0, §1.1, §1.2, §3.4, §3.5, §8.1, §8.3, §8.4, §8.6, §11, §14 | today's facts and limits, load assumptions, phase names, triggers, backups, India hosting, targets, technology cost |
| `docs/plan/03_COSTS_AND_BUDGET.md` | header, "Answer in 12 lines", §2.1–2.6, §3, §4 | exchange rate, episode cost, monthly cost, grades |
| `docs/research/business/03_scale_funding_unit_economics.md` | B3-1, B3-6, B3-12 | production steps, earlier episode model, incubator terms |
| `docs/DEPLOY.md` | Parts 1–3, "Good to know", "Optional keys" | what runs today, limits, move steps |
| `render.yaml`, `.env.example`, `backend/app/config.py` | plan and region, start command, AI and upload limits, `FIRST_SLOT, LAST_SLOT` | today's set-up, limits, 14 slots |
| `docs/ARCHITECTURE.md` | Contract D: `POST /api/sessions`, `POST /api/classify` | one upload per session |
| `docs/COMMS.md` | §9 | ₹0.115 a WhatsApp message, ₹3.50 a call minute |
| `docs/hackathon/DEMO_VIDEO_SHOTLIST.md` | shots 13 and 14 | figures the video already says |
| `docs/HANDOFF.md`, `supabase/schema_v2.sql` | "Keep-awake" line; hospital tag | the keep-awake job; limit 6 |
| `backend/app/llm.py`, `web/js/api.js` | file header; request names | summary cap and fallback; requests per session |

No new web pages were opened for this file. The "Adoption and retention – our assumptions" block named in the video's shot 13 was not in `PITCH_PLAN.md` when this was written, so shot 13's card was used instead.
