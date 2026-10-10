# 07 – Cross-check: what falls between the planning files

**Written:** 10 Oct 2026, late evening · **Checked:** `docs/plan/00`–`06`, `docs/research/business/BUSINESS_BRIEF.md` and `06_sell_vs_share.md`, `docs/DEVICE_LIFECYCLE.md`, `docs/HANDOFF.md`, `docs/research/RESEARCH_REPORT.md`, `docs/research/PITCH_FACTS.md`, `docs/research/KNOWLEDGE_BASE.md` (by search), `docs/FEATURE_STATUS.md`, `docs/hackathon/*`, `web/*.html`, `web/showcase/*`. No web research. No other file was changed.

**Short names used below.** "Plan 01" … "Plan 06" = the files in `docs/plan/`. "Biz 03", "Biz 06" = the files in `docs/research/business/`. Watch out: "06" means the **legal** file in `docs/plan/` but the **sell-vs-lend** file in `docs/research/business/`. Plan 04 and Plan 05 use "06" for the business one.

---

## Answer in 10 lines

1. **The seven files mostly agree. The big problem is old numbers in the pitch material,** not disagreement between the new files.
2. **Old unit cost is still in 6 pitch-facing places** (₹1,000–1,700 a unit, "₹150 a patient", ₹500 an episode). The new figure is about ₹2,500 a unit (Plan 01 §H-9, Plan 03 §2).
3. **The price story changed and the pitch has not caught up:** at ₹2,500 a unit, ₹500 an episode loses money. Say ₹1,000 an episode, or ₹200 a patient software fee once the hospital owns the units (Plan 03 §2.6).
4. **The hardware and legal files disagree on radio approval.** Plan 01 says each product needs its own ₹10,000 declaration. Plan 06 says an India-made unit with an approved module needs none. Plan 06 even tells the pitch to say "our radio module is already approved", but nobody has picked that module yet.
5. **Plan 06 asks "battery or USB?" as if it were open.** Plans 01 and 02 both need a battery: without it there is no "connects automatically", no "is it on?" and no reminder beeps.
6. **The scale design in DEVICE_LIFECYCLE (built-in 4G, SIM, speaker) is in no hardware build and no cost table.** Bluetooth SIG listing fees were passed to the hardware and cost files, and neither covers them.
7. **The pitch says "11 Indian languages".** The code has 10 Indian languages plus English (Plan 05 says 10).
8. **The demo-video shot list still gives the old deadline (Sun 11 Oct, 3 pm).** The real deadline is **Mon 12 Oct 2026, 11:00 AM IST** (HANDOFF).
9. **Every founder request has an answer somewhere except two:** a "daily / monthly / yearly" client count (only yearly and per-hospital exist), and the state the team lives in (still unknown, and it blocks the most work).
10. **Do the 11 fixes marked BEFORE SUBMISSION first.** They are text edits, not new work. Total about 1–2 hours.

---

## 1. Contradictions

| # | Topic | One side (file, place) | Other side (file, place) | Which is right / what to do |
|---|---|---|---|---|
| C1 | **Unit cost** | ₹1,000–1,700 a unit: `PITCH_FACTS.md:46` (#31), `CHECKPOINT_1.md:114`, `KNOWLEDGE_BASE.md:933`, `RESEARCH_REPORT.md:558`, `Biz 06` B6-1, `BUSINESS_BRIEF.md:22` (₹1,500) | About ₹2,300–2,500 before GST for a battery pilot unit: Plan 01 §H-9(b) and line 21; Plan 03 line 22 and §2 | Plan 01/03 are right. ₹1,000–1,700 only fits the cable prototype with no battery (₹1,365, Plan 01 §H-9(a)) |
| C2 | **Price per episode** | ₹500 an episode is the model: `BUSINESS_BRIEF.md:8`; Biz 06 line 24 (₹500–1,000); Plan 05 line 20 and E-6 (all at ₹500) | ₹500 loses money at pilot size and makes about ₹30 at scale; "charge ₹1,000 or let the hospital own the units": Plan 03 line 26, §2.3, §3 | Plan 03 is the newer maths. Plan 05 E-6 should add a ₹1,000 row |
| C3 | **Cost per lent episode** | ₹505 pilot / ₹318 scale: `BUSINESS_BRIEF.md:29`, Biz 06 line 16 and B6-5, Plan 04 J-12 (`04:404`) | ₹673 pilot / ₹470 scale: Plan 03 §2.2 | Plan 03 |
| C4 | **Radio approval (WPC)** | Module approval does **not** cover the finished product; ₹10,000 self-declaration per model: Plan 01 lines 171–173, 629, 687 | India-made unit with an approved module used unchanged needs **no** separate approval: Plan 06 §L-2 and line 16 | Plan 06 read the WPC FAQ itself (but it is old, about 2019). Plan 01 used consultancy notes. Ask one WPC agent; until then say nothing about radio approval in the pitch |
| C5 | **Which radio chip** | Use "an ESP32 module variant that has an ETA": Plan 06 line 75 | Switch to nRF52840 for any battery unit; ESP32-C3 cannot stay findable on a battery: Plan 01 §H-2, line 15. The nRF module's Indian approval is "not stated": Plan 01 §H-9(c) | Plan 01 for the chip. The legal advice must be redone for an nRF52840 module: find one with an Indian ETA |
| C6 | **Battery or USB** | "Battery in the box or USB-powered" is open; USB avoids BIS battery rules: Plan 06 line 520, §L-4 | Battery is needed (1,000–1,200 mAh); USB-only is "prototype only": Plan 01 §H-4. Auto-connect and unit-driven reminders need a battery: Plan 02 line 20, steps 1 and 8 | A USB-only unit cannot meet founder requests 2 and 3. Treat "battery, BIS-marked cell" as decided; the legal cost is small (buy a BIS-registered cell) |
| C7 | **Bluetooth vs SIM at scale** | Scale = built-in 4G + SIM + speaker, no phone: `DEVICE_LIFECYCLE.md:18`, `:79` | Version 1 = Bluetooth only, no SIM: Plan 06 line 519, §L-3. Plan 01's 1,000-unit build (§H-9(c)) and Plan 03's costs have no 4G module, SIM or speaker | Not a conflict for the pilot. But the scale design is uncosted (see O3) |
| C8 | **Device class** | "Expect Class B": `PITCH_FACTS.md:52` (#35), `RESEARCH_REPORT.md:411`, `CHECKPOINT_1.md:124` | Plan 06 L-1 builds a "cheaper route" on CDSCO accepting **Class A (measuring)**; decision 5 asks whether showing mL changes the class (`06:517`) | Both say "ask CDSCO". Keep the pitch on "we expect Class B and will confirm". Do not mention the Class A route in the pitch |
| C9 | **Is ethics approval enough for the first study?** | "Every deployment is a free, ethics-approved research pilot": `BUSINESS_BRIEF.md:8`; "about 50 patients, with ethics approval": `CHECKPOINT_1.md:112`; assumption J-18 "A free pilot needs only an ethics committee": Plan 04 | On the text of the rules an unlicensed prototype needs CDSCO permission too; plan for it: Plan 06 §L-1 and line 414 | Plan 06. Pitch wording must change (P6) |
| C10 | **Pilot size** | 30 patients, 15–36 units: Plan 03 §C | About 50 patients, 10–20 units: Plan 05 E-5 line 347, E-20; `CHECKPOINT_1.md:112`; Biz 02 line 224. "Build 5–10 units": `BUSINESS_BRIEF.md:62` | Say "30–50 patients" until the hospital is chosen. 5–10 units is too few for either |
| C11 | **Pilot timeline** | "3 months running plus about 1 month of set-up": Plan 03 line 65 | Company first, test licence 30 days, CDSCO permission up to 90 days, ethics committee: Plan 06 Gate 1. Plan 05 E-20 puts the first pilot at 6–18 months | Set-up is 4–6 months, not 1. Plan 03 hosting months may be low |
| C12 | **What the grant pays for** | "One NIDHI-PRAYAS grant covers a realistic pilot": Plan 03 line 27 | NIDHI-PRAYAS is "for a physical prototype", paid to individuals: Biz 03 §B3-7 | Check the scheme's allowed spending before counting on it for insurance, ethics fees or hosting |
| C13 | **Exchange rate** | ₹88 = US$1: `FUTURE_ARCHITECTURE.md:360`, Biz 03 line 47 | ₹96 = US$1: Plan 02 line 9, Plan 03 line 8 | Use ₹96 (Plan 03 settled it). Update the two old places |
| C14 | **Languages** | "Voice in 11 Indian languages": `CHECKPOINT_1.md:51`, `PITCH_FACTS.md:45` (#30) | "The current 10 Indian languages": Plan 05 line 24. The code lists `en-IN` plus 10 Indian language codes | Say "10 Indian languages plus English" |
| C15 | **Repo public or private** | "Make the repo private or scrub it"; Plan 04 says founder note 23 also says so: `04:484`, G-42 | Founder note 23 only says private *team material* must not be published; it does not ask to make the repo private (`00:56`). The hackathon needs a GitHub link that opens without login (`HANDOFF.md:106`) | Keep it public until judging ends. Then decide (D9) |
| C16 | **Publishing hardware details** | "Do not publish new hardware details before deciding on patent and design filings": Plan 06 red line 8 | Plan 01 (sealed window, keyed pocket, chip choices, thinner case) is already pushed to the public repo (`origin/main` at 6f698af) | Those details are now public prior art. From now on keep new hardware design notes out of the public repo |
| C17 | **Battery life numbers** | Showcase and 3D model: 500 mAh LiPo with an ESP32-C3 (`showcase.js:57, 837, 1081`) | That pairing lasts about 1.5 days if it stays findable: Plan 01 §H-3 table, design A | Fine as a cable-demo model; wrong if presented as the product (P5) |
| C18 | **Deadline** | Sun 11 Oct, 3:00 pm: `00_FOUNDER_NOTES.md:61`, `DEMO_VIDEO_SHOTLIST.md:3` | Mon 12 Oct 2026, 11:00 AM IST (organisers' email): `HANDOFF.md:106` | HANDOFF is right |

---

## 2. Stale numbers (exact file:line)

Plan files that show the old figure only as "was …" for comparison (Plan 03 lines 22–23, 173, 199, 201, 212–213) are fine and are not listed.

| File:line | Stale text | Replace with |
|---|---|---|
| `docs/research/PITCH_FACTS.md:46` (#31) | "about ₹1,000–1,700 of parts … (≈ ₹150 a patient over 10 uses) … Price idea: ₹500–1,000 per patient" | "About ₹2,500 of parts per pilot unit (our estimate from shop prices; Plan 01 §H-9). Lent 10 times that is ₹250 a patient for the unit. Price idea: ₹1,000 an episode, or ₹200 a patient for software on units the hospital owns (Plan 03 §2)" |
| `docs/hackathon/CHECKPOINT_1.md:114` | "₹1,000–1,700 per unit, or about ₹100–170 per patient" | Same as above |
| `docs/research/KNOWLEDGE_BASE.md:933` (J23) | ₹1,000–1,700, ₹150 a patient, ₹500–1,000 | Same as above |
| `docs/research/KNOWLEDGE_BASE.md:897`, `:958` | "₹500–1,000 per patient episode" | "about ₹1,000 per episode" (₹958 comparison with a home physio visit then needs a re-check) |
| `docs/research/RESEARCH_REPORT.md:558` (J11/J23) | ₹1,000–1,700, ₹150 a patient | Same as PITCH_FACTS fix |
| `docs/research/RESEARCH_REPORT.md:474` | "₹500–1,000 per patient episode" | "about ₹1,000 per episode (Plan 03 §2.3)" |
| `docs/research/RESEARCH_REPORT.md:585`, `:654` | "About ₹1,000–1,700 of parts as a hand-built prototype" | Keep for the cable prototype only; add "a battery pilot unit is about ₹2,500" |
| `docs/research/RESEARCH_REPORT.md:266–268` | Three parts estimates | Add one row: "Plan 01 §H-9(b), shop prices 10 Oct 2026: ₹2,300–2,500 before GST" |
| `docs/research/business/BUSINESS_BRIEF.md:8` | "charge the hospital per patient episode (about ₹500)" | "about ₹1,000 an episode, or ₹200 software fee on hospital-owned units" |
| `docs/research/business/BUSINESS_BRIEF.md:22–29` | ₹1,500 unit; +₹182 / +₹682; ₹505 / ₹318; "pays for itself after about 5 patients" | Plan 03 §2.2–2.3: ₹2,500 unit; ₹673 / ₹470; +₹30 / +₹530; 9 patients at ₹500, 4 at ₹1,000 |
| `docs/research/business/06_sell_vs_share.md:15–17, 32–44, 63–89, 229` | ₹1,000–1,700 parts; ₹1,880 sold unit; ₹505 / ₹318; ₹73 / ₹127 | Add a banner at the top: "Unit-cost figures superseded by `docs/plan/03_COSTS_AND_BUDGET.md` §2 (₹2,500 unit)". Do not rewrite the research |
| `docs/research/business/03_scale_funding_unit_economics.md:13, 63, 81–84` | ₹1,500 unit; +₹182 / +₹682; break-even 5 at ₹500 | Same banner |
| `docs/research/business/02_sales_and_go_to_market.md:292` | "Build 5–10 units … Parts ₹1,000–1,700 each" | "Build 10–20 units … about ₹2,700–2,950 each with GST" |
| `docs/plan/04_GAPS_AND_RISKS.md:403` (J-11) | "A unit costs about ₹1,500 to make" | "about ₹2,500 (Plan 01 §H-9)" |
| `docs/plan/04_GAPS_AND_RISKS.md:404` (J-12) | "₹318–505 per episode" | "₹470–673 per episode (Plan 03 §2.2)" |
| `docs/plan/05_EXPANSION_AND_CUSTOMERS.md:20, 368–372` | All hospital-side maths at ₹500 a patient | Add a ₹1,000 row (break-even then doubles: about 0.43 day per patient) |
| `docs/FUTURE_ARCHITECTURE.md:360` | ₹88 = US$1 | ₹96 = US$1 (or a note pointing to Plan 03) |
| `docs/research/business/03_scale_funding_unit_economics.md:47` | ₹88 = US$1 | Same |
| `web/showcase/showcase.js:57, 677, 837, 1081`; `web/showcase/sources.html:199` | 500 mAh LiPo with ESP32-C3 shown as the unit | Fine as the model of today's design. Caption should say it is the prototype design (P5) |
| `docs/hackathon/DEMO_VIDEO_SHOTLIST.md:3` | "Sun 11 Oct, 3:00 pm" | "Mon 12 Oct 2026, 11:00 AM IST" |

**Searched and clean:** `web/index.html`, `app.html`, `patient.html`, `demo.html`, `guardian.html`, `collect.html`, `units.html`, `web/showcase/index.html`, `videos.html` – no rupee figures, no cost claims. The four `.mp4` videos could not be text-searched; the tour captions in `showcase.js:1076–1090` are what they show.

---

## 3. Orphans (one file hands something to another that does not cover it)

| # | Handed off in | Handed to | What is missing |
|---|---|---|---|
| O1 | Plan 02 M-37 item 13 (line 481) and open questions (line 563): **Bluetooth SIG listing fee** "flag for the hardware and cost agents" | Plan 01, Plan 03 | Neither mentions it. Could be the largest single fee in Plan 02. Needs one check on bluetooth.com: is it needed, how much, does a pre-listed module reduce it |
| O2 | Plan 02 line 571: "one rupee–dollar rate for all plan files" → cost agent | Plan 03 | Plan 03 chose ₹96 but did not fix `FUTURE_ARCHITECTURE.md:360` or Biz 03 (C13) |
| O3 | `DEVICE_LIFECYCLE.md:18, 79`: scale unit with 4G, SIM, speaker, voice pack | Plan 01 (hardware), Plan 03 (costs) | Plan 01 only says the choice "is reopened" (line 182) and lists cellular modules as a watch item (line 527). No parts list, no cost, no M2M fees in Plan 03 |
| O4 | Plan 02 open question: "Can the hardware sense 'spirometer on the base'?" → hardware reviewer | Plan 01 | Partly: Plan 01 puts "seated" in the status message (line 205) and compares a reed switch (line 224), but never picks a method. Likely answer: the laser itself sees whether the piston is there. Confirm on the bench |
| O5 | Plan 06 L-2: "use an ESP32 module variant that has an ETA" | Plan 01 | Plan 01 moved to nRF52840. Nobody has found an nRF52840 module with an Indian ETA (C5) |
| O6 | Plan 04 "Hand to the costs file": helpline number and staff time (G-30); tax deducted at source by hospitals (cash flow); monitoring tools (G-49) | Plan 03 | Not in Plan 03's tables (monitoring only as a note under hosting) |
| O7 | Plan 04 "Hand to the costs file": spare units "unit cost in B6-1" | Biz 06 | Points to the old ₹1,880 figure; should point to Plan 03 §2.4 |
| O8 | Plan 04 decide #6: "Lend or sell? File 06 recommends lend" | Biz 06 | Correct file, but "06" reads like Plan 06 (legal). Write `research/business/06_sell_vs_share.md` |
| O9 | `BUSINESS_BRIEF.md:40` "the one question that blocks everything" (CDSCO permission) and `:67` "radio approval for a finished Bluetooth product" | Plan 06 | Plan 06 L-1 and L-2 now answer both (as "our reading"). The brief does not say so |
| O10 | Plan 05 E-12: "first interview question: one piston or three balls?" | `INTERVIEW_GUIDE.md` | Covered (question 8). But Plan 04 J-3 and Plan 03 Q10 want **price** asked in every interview, and the guide has no price question |
| O11 | Plan 06 L-25: "Fees: see the costs file" | Plan 03 | Covered (Plan 03 C2, D). OK |
| O12 | Plan 01 open question: device class "already open in RESEARCH_REPORT §7.1" | Plan 06 | Plan 06 turns it into adviser questions but does not settle it. Correct: only CDSCO can |

---

## 4. Founder requests: where each is answered

| # | Request (`00_FOUNDER_NOTES.md`) | Answered where | Status |
|---|---|---|---|
| 1 | Android app that connects by Bluetooth | Plan 02 M-1 to M-3, "Recommended app path" | Answered (not built) |
| 2 | Connects automatically every time | Plan 02 M-7, "auto-connect design in 8 steps"; Plan 01 §H-3 | Answered (needs a battery and nRF52840 – C6) |
| 3 | How do we detect the device is on? | Plan 01 "The direct answer…" (line 592); Plan 02 M-15, M-16 | Answered |
| 4 | Play Store and App Store, and their cost | Plan 02 M-21 to M-24; Plan 03 line 25 | Answered: ₹2,400 once (Android), ₹9,500 a year (Apple, skip for now) |
| 5 | Sell vs lend; settings swap to the next patient | Biz 06; `DEVICE_LIFECYCLE.md` §5.3; Plan 02 M-32; Plan 03 §2.2–2.5; Units screen built (commit ce6c610) | Answered; the final choice is still a decision (D7) |
| 6 | How login and connections work | `DEVICE_LIFECYCLE.md` §3, §6; Plan 02 | Answered (not built) |
| 7 | Device + software for ₹200? | Plan 03 §2.6 | Answered: no, except as a software fee on hospital-owned units at scale |
| 8 | Client base daily, monthly, yearly | Biz 01 (yearly market); Plan 05 E-5 (patients a month per hospital) | **Partly.** No daily figure and no "patients a day / month / year for us" at each stage. Plan 03 §3 assumes 50 episodes a month per hospital; Plan 05 says 30–400 depending on hospital |
| 9 | Best, most compact hardware now | Plan 01 lines 10–25, verdict table | Answered |
| 10 | "Don't want it to break the second time" | Plan 01 §H-6 | Answered |
| 11 | Future technology in a year | Plan 01 §H-10 | Answered |
| 12 | No hardware at all today | Plan 01 §H-11 shopping list; Plan 03 Stage A (₹8,000–13,000) | Answered (still waiting on purchase) |
| 13 | Human figure in the videos | Done (founder notes) | Done |
| 14 | Startup: scale, sales, customers, legal, ICMR | Biz 01–05, BUSINESS_BRIEF; Plan 05; Plan 06 | Answered |
| 15 | How much to get it out; pilot budget | Plan 03 §1 | Answered (half the figures are estimates pending quotes) |
| 16 | Customers in minute detail | Plan 05 E-1 to E-4 | Answered (nobody contacted yet) |
| 17 | How to expand | Plan 05 Part B | Answered |
| 18 | What did we miss | Plan 04; Plan 02 M-37; this file | Answered |
| 19 | One sub-agent per section, own file | Plans 01–06 | Done |
| 20 | Think first, then brief agents | Process | Done (not checkable from files) |
| 21 | Order: notes → hardware → rest | Plans 00, 01, then 02–06 | Done |
| 22 | Plain English, lead with the answer | Every plan file has an "Answer in N lines" | Mostly. Plans 01, 02 and 06 are long and technical below the summary; fine for advisers, heavy for the founder |
| 23 | Private team material stays private | Plan 04 G-96 | Respected: no plan file copies private details. Note Plan 04 misreads it as "make the repo private" (C15) |
| 24–26 | Hackathon context; startup intent | HANDOFF | Noted |
| 27 | Founder records the video; everything on screen | `DEMO_VIDEO_SHOTLIST.md` | Answered; its deadline line is stale (C18) |
| 28 | At least 3 user interviews | `INTERVIEW_GUIDE.md` | **NOT DONE** (0 interviews as of 10 Oct evening). Guide lacks a price question (O10) |
| F | Team names, email, college | – | **NOT ANSWERED** (waiting on founder) |
| F | Which state | – | **NOT ANSWERED**. Blocks the most work (D1) |
| F | Anyone interviewed? | – | **NOT ANSWERED** |
| F | Organisers' deck template | – | **NOT ANSWERED** (still in their Drive) |
| F | Show the Units screen in the video? | Units screen built (ce6c610); shot list line 35 points at it | Answered in practice; founder to confirm |
| F | Sarvam key on Render? | – | **NOT ANSWERED** (live site uses pre-recorded clips) |

---

## 5. Decisions – one merged list

Ordered by how much other work each one blocks. "Files waiting" = files whose numbers or plans change with the answer.

| # | Decision | Asked in | Files waiting on it | Blocks |
|---|---|---|---|---|
| D1 | **Which state, and which first hospital (government-funded or private)?** | 00 §F; Plan 03 Q1–2; Plan 04 #5; Plan 05 E-1; Plan 06 #2 | 03 (stamp duty, ₹1–1.5 lakh swing in CDSCO + ethics fees, travel), 05 (target list), 06 (licensing authority, grants) | Company, grants, hospital outreach, pilot budget |
| D2 | **Who is on the team: ages (all signers 18+), founders' agreement with vesting and IP assignment, company form and date; read the college and hackathon IP terms** | Plan 03 Q6; Plan 04 #1, #10, #12; Plan 06 #1, #3, Gate 0 #1–4; Plan 02 open questions | 02 (D-U-N-S, store accounts), 03 (C3), 06 (every gate) | Test licence, store accounts, grants, contracts |
| D3 | **Who is the clinical lead?** | Plan 04 #2, gap #1 | 04 (exclusions, target-volume rule, consent), 06 (lead investigator) | Ethics submission, anything clinical |
| D4 | **Bench test first, and a written stop rule** ("if the laser cannot read the piston through the tube, we …") | Plan 01 §H-11; Plan 04 #11, risk 1 | 01 (sensor chip, case height), 02 (protocol), 03 (unit cost) | All hardware spending beyond ₹8,000–13,000 |
| D5 | **Volume-type or 3-ball spirometer: which do wards use, and do we supply the spirometer?** | Plan 05 E-12; Plan 03 Q3; Interview guide Q8 | 03 (+₹146–1,067 a patient), 05 (market size), pitch | Offer, price, market size |
| D6 | **First-study route** (government hospital + CDSCO permission / licence first / usability-only) **and whether the app shows millilitres** | Plan 06 #4, #5, L-1; Plan 04 risk 4; Plan 02 M-26 | 03 (C3 fees, timeline – C11), 04, 05 E-20, 02 (store listing) | Pilot start date; store listing |
| D7 | **Business model and price**: lend free in the pilot; then ₹1,000 an episode, or hospital-owned units + ₹200 software fee | Plan 03 Q10; Plan 04 #6; Plan 06 #6; Biz 06 B6-19 | 03, 05 E-6, BUSINESS_BRIEF, PITCH_FACTS, CHECKPOINT_1 | The pitch's money slide; GST rate; data role |
| D8 | **Version-1 hardware**: Bluetooth only, no SIM; battery (1,000–1,200 mAh, BIS-marked) not USB; nRF52840 with an India-approved module | Plan 06 #7, #8, L-2; Plan 01 §H-2, §H-4; Plan 02 | 01, 02, 03, 06 (C4–C7) | Parts order for Stage B; radio paperwork |
| D9 | **Repo public or private after judging**, and where hardware design notes live | Plan 04 #3; Plan 06 #9, red line 8, L-10 | 04 G-42, 06 (patents), hackathon form | Patent/design options; security exposure |
| D10 | **Pilot size and kit**: 30 or 50 patients; reuse units (15) or one each (36); hospital lends phones or we buy | Plan 03 Q4, Q5; Plan 05 E-5 | 03 C1 (₹0.6–3.1 lakh), 05 | Unit order size |
| D11 | **Money and time**: apply to NIDHI-PRAYAS (check it pays for pilot costs – C12); who goes full-time first | Plan 03 Q8; Plan 04 #10 | 03 | Everything after the bench test |
| D12 | **Who collects the five quotes and the four paid adviser hours, by when** | Plan 03 Q9, line 28; Plan 06 #10 | 03 (half its numbers), 06 | Budget accuracy |
| D13 | **Promise on service hours**; **template or AI as default writer** of patient/family text | Plan 04 #7, #8 | 04, pilot agreement | Pilot agreement |
| D14 | **Keep the name?** Trademark and domain check first | Plan 04 #9; Plan 06 Gate 0 #6 | Printing, store listing | Any printed material |
| – | Already decided, just apply: Android first, iPhone later by rule (Plan 02 M-25); ₹96 = US$1 (Plan 03); no public store listing before the regulatory answer (Plan 02 M-26, Plan 06 Gate 1 #23) | | | |

---

## 6. Pitch risk (claims now wrong or risky)

| # | File:line | Claim | Why it is now risky (source) | Safer wording |
|---|---|---|---|---|
| P1 | `PITCH_FACTS.md:46`; `CHECKPOINT_1.md:114`; `KNOWLEDGE_BASE.md:933`; `RESEARCH_REPORT.md:558` | ₹1,000–1,700 a unit; ₹100–170 or ₹150 a patient | Plan 01 §H-9: ₹2,300–2,500 for a battery unit | See Stale-numbers table |
| P2 | `PITCH_FACTS.md:46`; `RESEARCH_REPORT.md:474`; `KNOWLEDGE_BASE.md:897, 958`; `BUSINESS_BRIEF.md:8` | Price ₹500 (or ₹500–1,000) a patient | Plan 03 §2.3, §3: ₹500 loses money even at 100 hospitals | "About ₹1,000 a patient episode; or ₹200 a patient for software when the hospital owns the units" |
| P3 | Plan 06 line 581 ("Say" list) | "The radio module we will use is already approved in India" | No module chosen; nRF52840 module approval unknown (Plan 01 §H-9(c)); Plan 01 disagrees on the rule (C4) | Leave it out of the pitch |
| P4 | `CHECKPOINT_1.md:51`; `PITCH_FACTS.md:45` | "Voice in 11 Indian languages" | 10 Indian + English (Plan 05 line 24; code) | "Voice in 10 Indian languages and English" |
| P5 | `web/showcase/showcase.js:1081` (tour caption; also burned into `tour.mp4`) and `:837` label | "Inside: … a XIAO ESP32-C3 and a 500 mAh LiPo battery" | Plan 01: that pair cannot run a findable battery unit (1.5 days); pilot moves to nRF52840 + 1,000–1,200 mAh | Caption: "Today's prototype design: a VL53L1X laser sensor, a XIAO board and a LiPo cell…". The MP4 can stay for the hackathon if the voice-over does not claim battery life |
| P6 | `CHECKPOINT_1.md:112`; `BUSINESS_BRIEF.md:8` | Pilot "with ethics approval" / "ethics-approved research pilot" | Plan 06 L-1 and "Do not say": not established that ethics alone is enough | "…with ethics approval, and CDSCO's written view on central permission before we enrol anyone" (Plan 06 "Say" list) |
| P7 | `PITCH_FACTS.md:58` (never-say list) | List is missing Plan 06 and Plan 05 items | Plan 06 "Do not say" (line 583 on); Plan 05 "What NOT to claim" | Add: "we only need an ethics committee", "no CDSCO permission needed", "patent pending" / "we own all the IP", "doctors recommend it", "certified", "approved", "works with any spirometer", "we have partner hospitals", "device plus software for ₹200", any rupee figure for consultants, tests or insurance |
| P8 | `web/showcase/showcase.js:1087` (caption) | "Our trained model labels every breath" | Model trained only on practice (synthetic) breaths: Plan 04 gap #13, `BUSINESS_BRIEF.md:46` | Acceptable if the voice-over adds "trained on practice breaths so far". Low risk |
| P9 | Plan 05 E-1 target list in any deck | Naming CMC Vellore, Amrita etc. | Plan 05 "What NOT to claim": nobody has been contacted | Say "hospitals we plan to approach", never "partners" |
| P10 | `CHECKPOINT_1.md:84` | "voice coach in 11 languages" | True (10 + English) | OK as is |

Checked and fine: `web/index.html:89`, `web/patient.html:101–102`, `web/app.html:7, 190`, `web/guardian.html:57` (all say "does not diagnose", fake patients); `CHECKPOINT_1.md:107, 124`; `DEMO_VIDEO_SHOTLIST.md:17` (already bans "Android app", "first", "prevents pneumonia").

---

## Fix list (ranked)

**BEFORE SUBMISSION** = do before Mon 12 Oct 2026, 11:00 AM IST. All are text edits.

| Rank | When | File | Change |
|---|---|---|---|
| 1 | **BEFORE SUBMISSION** | `docs/research/PITCH_FACTS.md:46` (#31) | Replace unit economics: "About ₹2,500 of parts per pilot unit (our estimate from shop prices, Plan 01 §H-9); a hand-built cable prototype is about ₹1,365. Price idea: about ₹1,000 a patient episode, or ₹200 a patient for software once the hospital owns the units (Plan 03 §2)." |
| 2 | **BEFORE SUBMISSION** | `docs/hackathon/CHECKPOINT_1.md:114` | Same wording as rank 1 (this file feeds the deck) |
| 3 | **BEFORE SUBMISSION** | `docs/research/KNOWLEDGE_BASE.md:933` (J23) and `docs/research/RESEARCH_REPORT.md:558` | Same judge answer as rank 1 |
| 4 | **BEFORE SUBMISSION** | `docs/research/PITCH_FACTS.md:58` | Add the never-say items in P7 |
| 5 | **BEFORE SUBMISSION** | `docs/hackathon/CHECKPOINT_1.md:112` | "about 50 patients, with ethics approval" → "30–50 patients, with ethics approval and CDSCO's written view on central permission first" |
| 6 | **BEFORE SUBMISSION** | `docs/hackathon/CHECKPOINT_1.md:51`, `docs/research/PITCH_FACTS.md:45` | "11 Indian languages" → "10 Indian languages and English" |
| 7 | **BEFORE SUBMISSION** | `docs/hackathon/DEMO_VIDEO_SHOTLIST.md:3` | Deadline → "Mon 12 Oct 2026, 11:00 AM IST" |
| 8 | **BEFORE SUBMISSION** | `web/showcase/showcase.js:1081` | Caption → "Today's prototype design: a VL53L1X laser sensor, a XIAO board and a LiPo cell…". Do not re-render the MP4s now; keep battery life out of the voice-over |
| 9 | **BEFORE SUBMISSION** | `docs/plan/06_LEGAL_DEEP_DIVE.md:581` | Strike the "radio module is already approved" bullet from the "Say" list, or mark it "only once the module's ETA number is in hand" |
| 10 | **BEFORE SUBMISSION** | `docs/research/business/BUSINESS_BRIEF.md` (top) | Add one line: "Unit cost and per-episode figures below are superseded by `docs/plan/03_COSTS_AND_BUDGET.md` §2: ₹2,500 unit, ₹470–673 an episode, price about ₹1,000." Change line 8 "about ₹500" to "about ₹1,000" |
| 11 | **BEFORE SUBMISSION** | `docs/hackathon/INTERVIEW_GUIDE.md` (after Q8) | Add: "If the hospital paid per patient for this, would ₹200, ₹500 or ₹1,000 be acceptable? Who would sign, from which budget?" |
| 12 | After | Get one WPC agent's answer on C4; then fix whichever of Plan 01 (lines 173, 629, 687) or Plan 06 §L-2 is wrong; and find an nRF52840 module with an Indian ETA (Plan 06 line 75) | |
| 13 | After | `docs/plan/06_LEGAL_DEEP_DIVE.md:520` | Mark decision 8 as "battery, BIS-registered cell" with reason (Plans 01, 02); keep USB for the bench prototype only |
| 14 | After | `docs/plan/03_COSTS_AND_BUDGET.md:65` and C2 hosting months | Set-up "about 1 month" → "4–6 months (company, test licence, ethics, possible CDSCO permission)"; re-check hosting months |
| 15 | After | `docs/plan/03_COSTS_AND_BUDGET.md:27` | Check NIDHI-PRAYAS allowed spending; if prototype-only, say which pilot lines it cannot pay |
| 16 | After | Plan 01 and Plan 03 | Add Bluetooth SIG listing (O1): needed or not, fee, module effect |
| 17 | After | `docs/DEVICE_LIFECYCLE.md:18` or Plans 01/03 | Either mark the 4G/SIM/speaker unit as "later, not costed", or add it to Plan 01 §H-9(c) and Plan 03 (module, SIM, M2M rules from Plan 06 §L-3) |
| 18 | After | `docs/plan/04_GAPS_AND_RISKS.md:403, 404, 484, 487` | J-11 → ₹2,500; J-12 → ₹470–673; decision 3 wording (founder note 23 does not ask for a private repo; judges need it public until results); "File 06" → `research/business/06_sell_vs_share.md` |
| 19 | After | `docs/research/business/06_sell_vs_share.md`, `03_scale_funding_unit_economics.md` | Add the "superseded by Plan 03 §2" banner at the top; leave the research text as it is |
| 20 | After | `docs/research/business/02_sales_and_go_to_market.md:292` | "Build 5–10 units, ₹1,000–1,700 each" → "Build 10–20 units, about ₹2,700–2,950 each with GST" |
| 21 | After | `docs/plan/05_EXPANSION_AND_CUSTOMERS.md:20, 368–372` | Add a ₹1,000-a-patient row to the hospital break-even table |
| 22 | After | `docs/FUTURE_ARCHITECTURE.md:360`, Biz 03 line 47 | ₹88 → ₹96 = US$1 |
| 23 | After | `docs/research/RESEARCH_REPORT.md:266–268, 474, 585, 654`; `KNOWLEDGE_BASE.md:897, 958` | Add the Plan 01 pilot-unit row; ₹500–1,000 → about ₹1,000 |
| 24 | After | `docs/plan/03_COSTS_AND_BUDGET.md` | Add helpline, monitoring tools and TDS cash-flow lines handed over by Plan 04 (O6) |
| 25 | After | `docs/plan/00_FOUNDER_NOTES.md` | Append (do not rewrite item 25): "Deadline moved to Mon 12 Oct 2026, 11:00 AM IST (organisers' email)." Append a line under §F that the Units screen is built |
| 26 | After judging | Decide D9 (repo public or private). Keep new hardware design notes out of the public repo from now on (C16) | |
| 27 | After | `docs/HANDOFF.md` | Point to this file and list ranks 12–25 as open |
