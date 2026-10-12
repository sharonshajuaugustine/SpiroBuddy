# SpiroBuddy pitch deck – the complete brief for ChatGPT

**What this file is:** everything ChatGPT needs to rebuild the SpiroBuddy pitch deck on the organisers' PowerPoint template. ChatGPT cannot see our code or our website, so every fact, every page, every number and every rule is written here.

**Event:** Dolphin Tank India – Social Impact Hackathon 2026 · track **Health & Well-being (SDG 3)** · team **GuGu GaGa** · submission closes **Mon 12 Oct 2026, 11:00 AM IST**.
**Written:** Mon 12 Oct 2026, about 02:30 IST, from the project's own fact files and from the live pages.

**Words used in this file**
- **Incentive spirometer** = a plastic breathing exerciser given after surgery. You breathe in slowly and a disc (piston) rises. Always call it "an incentive spirometer, a breathing exerciser", so nobody hears "spirometry", the lung test.
- **Status words** (the only four allowed): **Live** = works on the site today, with sample patients · **Simulated** = works, but its input or its sending is a built-in simulator · **In development** = partly built, not switched on · **Planned** = not built.
- **Sample patients / sample hospitals** = made-up people and places on the site. The hospitals are "Dawnlight General Hospital" and "Dawnlight Riverside Clinic". Write "Sample patient" on a slide, not "demo", "fake" or "fictional".
- **[ADD: ...]** = a gap only the founder can fill. **[FOUNDER: ...]** = a note for the founder to read and then delete.

---

## A. How to use this file (for the founder)

**What to do, in order**
1. Open ChatGPT. Start a **new chat**. Pick the strongest model you have (one that can run code and make files).
2. Click the paper-clip and upload these files together:
   1. `DECK_BRIEF_FOR_CHATGPT.md` (this file)
   2. `DTI_SIH_Pitch Deck_Template.pptx` (the organisers' template – do not rename it)
   3. `deck_shots.zip` (the screenshot pack; it also holds the product logo `00_product_logo.png` and the QR picture `00_qr_live_demo.png`)
   4. Team photos, if you want them on the Team slide (optional)
3. Copy everything inside the grey box in **section B** and paste it as your first message. Send.
4. ChatGPT should first answer with a list of the template's slides and its plan (keep / delete / duplicate). Read it. If it matches section I, reply: **"Yes, build it."**
5. Download the `.pptx` it makes. Open it in PowerPoint and go through the checklist below.
6. Fill every yellow **[ADD: ...]** box yourself (section J lists them). Delete every **[FOUNDER: ...]** line.
7. Save a PDF copy too (File → Save As → PDF).

**Why one of the template's two title pages is "missing" (your question)**
The organisers' template has **two alternative title pages**. Slide 2 is the title with the hero picture in a frame on the right. Slide 3 is the **same title again** with the hero picture as the full background. They are two looks for one page. You use one and delete the other. Nothing is lost.
**Recommended: keep slide 2 (picture on the right), delete slide 3.** Reason: our hero picture is a 3D design model, and it must carry the label "3D design model – device in development". On a full-background picture that label and the title are hard to read, and the model could be mistaken for a photo of a finished product.

**Checklist for ChatGPT's result (tick each one)**
- [ ] The Dolphin Tank India logo is on the title page, where the template had it. It is not pasted onto other slides.
- [ ] Background, colours, fonts, title bar and page numbers look exactly like the template.
- [ ] Footer on every slide reads: `DOLPHIN TANK INDIA  •  SOCIAL IMPACT HACKATHON`.
- [ ] Slide order follows the template's sections (section C1). Extra slides sit inside their own section.
- [ ] The instruction slide, the second title page, the duplicate Business slide and all sample text ("Include:", "<Product Name>", "Table Example", "abc@xyz.com") are gone.
- [ ] No word from the never-say list (section C3). Search the deck for: "first", "proven", "approved", "certified", "compliant", "prevents", "reduces readmission", "real-time", "partner hospital", "COVID".
- [ ] Every number has a small source line or the word "estimate", "assumption" or "target" next to it (section G).
- [ ] Every status word matches section E and section D (Live / Simulated / In development / Planned).
- [ ] Every screenshot is one of the supplied files. No invented or redrawn screens.
- [ ] Every slide that shows a patient says "Sample patient" once, and every picture of the device says "device in development".
- [ ] Every placeholder is still marked **[ADD: ...]** in yellow. Nothing was made up (no names, college, quotes, hospitals, users).
- [ ] The team name is **GuGu GaGa**.
- [ ] **[FOUNDER: check /api/features on the live site before submitting; if the OTP login is there, say Simulated]** – see section D6.

---

## B. THE PROMPT FOR CHATGPT (paste this as the first message)

```text
You are a careful pitch-deck builder. I have uploaded three things:
1. DECK_BRIEF_FOR_CHATGPT.md – the complete brief. It is the only source of truth.
2. "DTI_SIH_Pitch Deck_Template.pptx" – the organisers' PowerPoint template.
3. deck_shots.zip – real screenshots of my product, a product logo and a QR picture.

YOUR TASK
Build my pitch deck as a .pptx file ON the uploaded template, using python-pptx.
Open the template file and edit it. Do NOT start a new presentation and do NOT redesign anything.
Save the result under a NEW name: SpiroBuddy_DTI_Pitch_v2.pptx. Never overwrite the template.

WORKING METHOD (follow in this order)
Step 1. Read the whole brief, start to end, before you write any code.
Step 2. Open the template with python-pptx. List every slide: number, title text, the shapes on it
        (name, position, text). Note the fonts, sizes and colours the template's own text uses.
        Unzip deck_shots.zip and list the files.
Step 3. Tell me, in a short table, what you will do with each template slide (keep / delete /
        duplicate for an extra slide) and the final slide order. It must match section I of the brief.
        Then WAIT for my "Yes, build it."
Step 4. Build the deck:
        - Keep the template's frame on every slide (title bar, coloured bars, footer line, footer
          text, page number). The template draws these as ordinary shapes on each slide, so copy
          them when you make an extra slide (duplicate a template content slide).
        - Put the text from section I on each slide: the title-bar text, one headline sentence,
          the body, the status tags, the small source line.
        - Place the screenshots named in section I. Keep their proportions. Crop only where
          section L says so. Never redraw or invent a screen.
        - Put the speaker notes from section I into each slide's notes.
        - Mark every [ADD: ...] gap with a yellow highlight so I can find it.
Step 5. Check your own work: re-open the saved file, print every slide's text, and test it against
        the hard rules in section C and the checklist in section A. Fix what fails. Then give me
        the file and a short list: slide number, title, anything you were unsure about.

IF YOU CANNOT PRODUCE A .pptx FILE
Say so in one line. Then give me, slide by slide: the title-bar text, the headline, the exact
body text, the position and size of every text box and picture (in inches on a 13.33 x 7.5 inch
slide), the screenshot file names, and the speaker notes, so I can build it by hand.

HARD RULES (the brief's section C has the full list; these are the ones you must never break)
1. Template: never change or remove the Dolphin Tank India logo, the background, the colours,
   the fonts, the slide order, the title bar style or the page numbers.
2. Footer on every slide: "DOLPHIN TANK INDIA  •  SOCIAL IMPACT HACKATHON".
3. Use ONLY the facts and numbers written in the brief. Each number carries its source tag or
   the word estimate / assumption / target. Never add a number, a study or a statistic from
   your own knowledge.
4. Invent nothing: no users, pilots, partners, hospitals, awards, testimonials, results, pilot
   targets, team names, college, quotes or contact details. Where the brief says [ADD: ...],
   leave a clearly marked yellow placeholder.
5. Honest status: the clip-on device is NOT built (a design and a 3D model). Breaths are
   simulated. Patients and hospitals on the site are sample ones. Use exactly the status words
   the brief gives: Live / Simulated / In development / Planned.
6. Never write that nothing like this exists, never mention COVID use, never say the AI
   diagnoses, never use a word from the never-say list in section C3.
7. No payments, bills or prices inside the hospital, nurse or patient apps. The business slides
   may show our own labelled estimates.
8. One message per slide and few words. Body text at least 14 pt. Detail goes in the notes.
9. Team name: GuGu GaGa. The product and the live site are named SpiroBuddy. The planned
   whole-hospital app is written "Arogya Sathi (working name), with the SpiroBuddy breathing coach".

Begin with Step 1 and Step 2 now, then show me the Step 3 table.
```

---

## C. Hard rules

### C1. The template rules (do not break these)

The organisers' file must **not be redesigned**.

**Never change or remove:** the Dolphin Tank India logo · the background · the colours · the fonts · the slide order · the title bar style · the page numbers.
**Ours to fill in:** the product content, the hero visual and the product logo.

**Details**
1. **DTI logo:** it goes where the template has it, on the **title page** (top right). Do **not** add it to the other slides. (The template's content slides do not carry it.)
2. **Footer:** the template's instruction slide says in writing to have the text `DOLPHIN TANK INDIA  •  SOCIAL IMPACT HACKATHON` in the footer. The template's own content slides say `DOLPHIN TANK INDIA  •  IDEA TO SOCIAL IMPACT`. **Use the instructed text, `DOLPHIN TANK INDIA  •  SOCIAL IMPACT HACKATHON`, on every slide**, in the template's footer text box, with the template's font, size and colour. On the title page (which has no footer text box of its own) copy the footer line and footer text shapes from a content slide.
   **[FOUNDER: if an organiser tells you to keep the template's own footer, say so and ChatGPT changes this one line]**
3. **Two title pages:** the template has two alternative title pages. Slide 2 has the hero picture in a frame on the right. Slide 3 is the same title with the hero picture as the full background. **Use slide 2 and delete slide 3.**
4. **Extra slides** are allowed **only inside the matching section**, and they are made by **duplicating a template content slide** (so the frame is identical). The title-bar text of an extra slide is the section's own title plus a short label, for example "Solution Overview: The Prescription".
5. **Delete:** the instruction slide (slide 1), the unused title variant (slide 3), the duplicate "Business & Sustainability Model" slide (slide 14) and **all sample text** ("Include: ...", "<Product Name>", "Table Example", "Recommended Structure", "abc@xyz.com", the sample closing quote).
6. **Page numbers:** the template types them by hand in a small text box at the bottom right ("02", "03" ...). The title page has none. Keep that box and its style, and number the slides in order: the first slide after the title is `02`.
7. **How the template is made (so you do not fight it):** slide size 13.333 x 7.5 inches (12192000 x 6858000 EMU). Every slide uses the same layout. The slides are built from ordinary shapes, not layout placeholders. On each content slide the frame is: the title text box at the top, a thin full-width bar under it with a short accent bar at its left end, a small upright accent bar beside the title, a thin footer line, the footer text and the page number. The body area between them is free.
8. **Colours and fonts:** read them from the template's own shapes and reuse them. In the template the titles are dark navy (about #253653), the bar under the title is blue (about #38A0D8), the accent is orange (about #E57116) and the footer text is grey (about #5B6B7D). Use tints of these for panels. Do not bring in a new colour scheme or a new font. Green, amber and red may be used only for the small status tags and the "call 112" example, always with a word beside the colour.

**The template's slides, in order, with each slide's "Include:" list**

| # in template | Title | What the template asks for | What we do |
|---|---|---|---|
| 1 | Instructions | Evaluation criteria; the logo and footer rule; "check the comments on slide for examples" (the file holds no comments) | **Delete** |
| 2 | Title page (hero picture in a frame on the right) | Product logo · Hackathon theme · Product name · one-line elevator pitch / tagline · "- By team name" · hero visual · DTI logo | **Keep** |
| 3 | Title page (hero picture as full background) | The same fields | **Delete** |
| 4 | Problem Statement | Include: what problem are you solving? · who is affected? · why is it important? · supporting statistics/research · current challenges. Answer: What? Who? Why now? How big? | Keep |
| 5 | Social Impact & SDG Alignment | Include: primary beneficiaries · UN SDG alignment · expected outcomes · impact metrics. Sample table: Metric / Year 1 / Year 3 (Beneficiaries, Jobs Created, CO₂ Reduction, Income Increase) | Keep + 1 extra |
| 6 | Target Beneficiaries | Include: user persona #1 · user persona #2 · key pain points · interview findings · user journey. Show: demographics · needs · motivations · challenges | Keep + 1 extra |
| 7 | Solution Overview | Include: solution overview · how it works · key features · benefits. Framework: Problem → Solution → Outcome | Keep + 2 extra |
| 8 | Innovation & Differentiation | Include: what makes it unique? · existing alternatives · innovation matrix. Sample table: Existing Solution / Your Solution | Keep |
| 9 | Technology Architecture | Include: architecture diagram · tech stack · AI/ML usage · cloud infrastructure · security · privacy · accessibility · ethical considerations. Architecture flow: User → Application → APIs → AI Layer → Database → Dashboard | Keep + 1 extra |
| 10 | MVP / Prototype Screens | Include: screenshots · wireframes · user flow · demo explanation. Show: login · main dashboard · feature screens · reporting module | Keep + 2 extra |
| 11 | Market Validation | "Supports Problem + Users + Solution". Include: surveys conducted · user interviews · customer discovery · pilot feedback. Sample table: Validation Activity / Result (Interviews, Survey Responses, Pilot Users, Waitlist) | Keep |
| 12 | Scalability | Include: geographic expansion · digital scalability · partnerships · automation opportunities. Roadmap: City → State → Country → Global | Keep + 1 extra |
| 13 | Business & Sustainability Model | Include: revenue streams · cost structure · sustainability plan. Sample table: Business Model Canvas Snapshot (Revenue / Costs) | Keep + 1 extra |
| 14 | Business & Sustainability Model (an exact duplicate of 13) | The same | **Delete** |
| 15 | Risks & Mitigation | Include: operational risks · adoption risks · technology risks · regulatory risks. Sample table: Risk / Impact / Mitigation | Keep |
| 16 | Implementation Roadmap | 90 Days: MVP completion, pilot program · 180 Days: user acquisition, partner onboarding · 365 Days: scale, revenue generation. "Use a timeline visualization." | Keep |
| 17 | Team Structure | Include: founders · technical team · business team · advisors/mentors. Recommended structure: CEO → CTO → Product Lead → Developers; CEO → COO → Partnerships → Growth | Keep |
| 18 | Financial Requirements | Include: development cost · marketing cost · operations cost · funding requirement. Sample table: Category / Amount (Product Development, Marketing, Operations, Total) | Keep |
| 19 | Ask & Next Steps | Include: what support do you need? · mentorship · funding · pilot customers · pilot partners · technology support · strategic partnerships · closing statement · "Queries & Feedback @ ..." · QR code "Scan For Demo" · "Link For Demo" | Keep |

**The evaluation criteria and their marks (from the template's instruction slide), mapped to our slides**
(Slide numbers are the new deck's numbers from section I.)

| Criterion | Marks | Answered on slide(s) |
|---|---|---|
| Problem Significance | 15 | 2 |
| Understanding of Users | 10 | 5, 6, 16 |
| Innovation | 15 | 8, 10 |
| Solution Quality | 15 | 7, 8, 9, 11 |
| MVP / Prototype | 15 | 13, 14, 15 (and the QR to the live site on 25) |
| Social Impact | 15 | 3, 4 |
| Scalability | 5 | 17, 18 |
| Sustainability / Business Model | 5 | 19, 20, 24 |
| Responsible Technology | 5 | 12 (also 11, 15, 21) |
| **Total** | **100** | |

### C2. The honesty rules

The organisers check the submission against the live website. An unfinished feature is fine **only if it is clearly labelled**. So:

1. **Only the numbers in section G.** Each one is printed with its source tag, or with the word **estimate**, **assumption** or **target**. Do not round them differently and do not add numbers from memory.
2. **Invent nothing.** No users, pilots, partners, hospitals, awards, testimonials, results or pilot targets. SpiroBuddy has had **no patient, no pilot, no survey, no hospital and no pharmacy test**. Say so plainly where the template asks.
3. **The device is NOT built.** It is a design and a 3D model (the registry line: "The firmware and the 3D design exist; no unit is built or bench-tested"). Every picture of it carries the label "3D design model – device in development".
4. **Breaths are simulated.** The breathing coach runs on a built-in breath simulator. The breath model was trained on simulated breaths; its accuracy on real people is not measured.
5. **Patients and hospitals on the site are sample ones** ("Sample patient", "Dawnlight General Hospital", "Dawnlight Riverside Clinic"). The three people in the story (Ravi, Sister Anjali, Amit) and Dr. Meera Nair are illustrative, not real.
6. **Never claim that nothing like it exists.** Hospital-chain apps and ABHA health-locker apps exist. A US clip-on tracker (InSee) exists. Our line is: "any hospital or clinic, built for the elderly, in the patient's language, shown at the pharmacy counter".
7. **Never say it was used during COVID,** or anywhere else. It has not been used.
8. **The AI never diagnoses.** It coaches and summarises only. Red-flag words trigger a fixed "contact your nurse / call 112" message from a word list, with no AI.
9. **No payments in the apps.** Nothing about money, bills, prices or insurance appears in the hospital, nurse or patient apps, ever. Hospitals would pay us through our own company console only. The business slides may show **our labelled estimates**.
10. **Medicines = a digital prescription.** The doctor types it in the hospital software; the patient sees it on the phone and shows that screen at the pharmacy. It is **not** "AI reads a prescription photo".
11. **Patients never switch a medicine off themselves.** They report it; only the doctor changes the plan.
12. **Names:** the entry and the live site are **SpiroBuddy**. The planned whole-hospital app is always written **"Arogya Sathi (working name), with the SpiroBuddy breathing coach"**. It is a working name because the Government of India already has an app called "TB Aarogya Sathi".
13. **Status words** must match sections D and E exactly. If a feature is not listed there, it is **Planned**.

### C3. The never-say list

Do not write any of these, in any form:

- "prevents pneumonia" · "reduces readmissions" · "fewer complications" as a result of ours · "₹X saved per patient"
- "first", "first in the world", "first in India", "first AI follow-up in India" · "no such software exists" · "nothing like it"
- "clinically proven" · "validated" · "accurately" · "guarantee" · "cures"
- "diagnoses" · "detects deterioration" · "real-time monitoring"
- "approved", "CDSCO-approved", "FDA-approved", "certified", "compliant", "DPDP compliant", "HIPAA" · "WhatsApp / Meta approved us"
- "no licence needed" · "no regulation applies" · "we only need an ethics committee" · "it's just an accessory, so it's Class A"
- "patent pending" · "patentable" · "we own all the IP" · "laser sensing is our invention"
- "doctors recommend it" or any named real clinician · "partner hospitals" (we have none) · any named real hospital or customer
- "works with any spirometer" (our sensor cannot read three-ball types)
- "device plus software for ₹200" · "hosting is free" (it is free for the demo only) · any cost without the word estimate
- "95.8% accurate" without the words "on simulated breaths"
- "we message the family" without "who opted in, with the patient's consent"
- "Android app" or "iPhone app" for today's product (say "mobile web app"; store apps are Planned)
- "the data never leaves India" · "data is stored in India" (today's web service runs in Singapore) · "WhatsApp is end-to-end encrypted to the hospital"
- "used during COVID" · "elderly Indians prefer voice" (use the literacy numbers instead)
- "Indian bypass readmission is X%" (no published figure) · "the TB programme recommends home spirometry"
- "infinitely scalable" · "zero downtime" · any hospital count in the present tense
- "our radio module is already approved" · "AI calls change behaviour"
- Any Year-1 / Year-3 beneficiary number, any pilot result, any pilot target number.

### C4. There is NO question round – the slides must answer the judges themselves

In the selection round the judges cannot ask us anything. So each likely question below must be answered by a line on a slide. The slide number is given.

| # | The judge's question | The one-line answer (30 words or fewer) | Slide |
|---|---|---|---|
| 1 | Does the incentive spirometer even work? | On its own, reviews find little benefit. But those trials rarely recorded whether patients did it. It helps inside a nurse-led breathing bundle; we make the doing visible. | 2, 10 |
| 2 | So you're building on a weak device? | We coach the breathing exercise the physio prescribes. The base reads one exerciser today; the coach, dashboard and family link can take any breath source, even a manual tap. | 10 |
| 3 | You have no hardware. Is this real? | The software is live and works end to end. The device is a simulator plus a 3D model with sourced sizes. Building one bench unit is step one. | 15, 22 |
| 4 | How accurate is your AI? | 95.8% on simulated breaths. Real-patient accuracy isn't measured yet; recording real breaths comes first. Simple rules run as a backup, and it only labels technique. | 11, 15 |
| 5 | Most Indian patients get the three-ball type. | True, it is common and cheap. We read the volume type, which the US guideline suggests. Reading three-ball devices, perhaps by phone camera, is our first extension. | 18, 21 |
| 6 | InSee is FDA-cleared. Why you? | InSee proved tracking works: in US hospitals, for one US spirometer. We add home use, voice in Indian languages, technique coaching, and nurse and family follow-up. | 10 |
| 7 | What stops Cipla, Lupin or a phone app copying you? | Nothing stops them trying. Our edge is elders without smartphones, 10 Indian languages, the nurse workflow and the family link. We'll accept phone-based breaths too. | 10 |
| 8 | Is this a medical device? | We expect so. It measures and alerts, so we expect Class B under India's device rules, and will confirm with CDSCO before any patient study. | 12, 21 |
| 9 | Can you start a pilot with just ethics approval? | We won't assume that. Prototypes under a test licence, a hospital-led study with a registered ethics committee, and CDSCO's written view before enrolling anyone. | 21, 22 |
| 10 | What about data privacy? | Sample patients only today. For launch: consent from the patient, in their language, read aloud; an itemised data list; one-word STOP; designed for India's DPDP Act. | 12 |
| 11 | Could the AI give wrong medical advice? | It never diagnoses; it coaches and summarises. Red-flag words trigger a fixed "contact your nurse or call 112" message from word lists, not AI. Alerts follow fixed rules. | 11, 12 |
| 12 | Is WhatsApp allowed for health updates? | Its business policy allows it with conditions: the family member opts in, the patient consents, approved non-promotional templates, STOP honoured. Progress updates only, never a diagnosis. | 12 |
| 13 | Who pays? | The hospital. Under fixed-price insurance, extra bed-days come from its margin. About ₹1,000 per patient episode, less than half a ward day. Not yet tested with a hospital. | 19 |
| 14 | PM-JAY hospitals can't bill patients extra. | Right. Our fee has to fit inside the hospital's package, not appear as a separate line. How that works is a question for our first hospital interviews. | 19 |
| 15 | What does a unit cost? Why not ₹200? | About ₹2,500 of parts, our estimate, lent and reused across about ten patients. ₹200 works only later, as a software fee on units hospitals own. | 17, 19 |
| 16 | Will you cut readmissions or complications? | We don't claim that. We measure completed sessions now. Complications and readmissions would be measured in a proper study, not promised in a pitch. | 3 |
| 17 | Isn't a paper tally sheet enough? | Paper counts sessions, if someone fills it in. We also record how each breath is done: speed, depth, hold. Whether that helps is our first study question. | 10 |
| 18 | What about TB? | A later group. India's 2024 TB rehab guidance, still a draft, lists the incentive spirometer for supervised sessions. By our estimate, 16–17 lakh people finish lung-TB treatment yearly. | 17 |
| 19 | Why you? Can you explain code an AI helped write? | Yes: each of us owns one part and can explain it. We mapped evidence, law and costs before building. We measure what the trials almost never recorded: actual use. | 23 |
| 20 | What happens after the hackathon, and how does it scale? | Bench-test one unit, record real breaths, then a 30-patient pilot. Units are lent and reused, so hospitals buy no hardware. One NIDHI-PRAYAS grant could fund the pilot. | 22, 24 |
| 21 | How is this different from a hospital-chain app or an ABHA app? | Those serve one chain's own patients, or store records. Ours is for any hospital or clinic, built for the elderly, in the patient's language, shown at the pharmacy counter. | 10 |
| 22 | Is this only a spirometer gadget? | No. The spirometer is module 1. The same platform already carries the doctor's prescription to the patient's phone, and is planned to grow into a whole-hospital app. | 9, 18, 20 |

---

## D. The product, complete

### D1. The story in one breath

> After surgery, patients go home with a plastic breathing exerciser and are told to use it every hour, and nobody, not the nurse, not the family, not even the clinical trials, has checked whether they actually do; SpiroBuddy makes that visible.

- **Tagline:** *Every breath, coached and counted.*
- **One line for the title page:** After surgery, the hospital stays connected to the patient at home.
- **One-line description (182 characters):** A clip-on base for the breathing exerciser given after surgery: it checks each breath, coaches by voice in 10 Indian languages and English, and updates the nurse and opted-in family.
- **How we frame it:** "the adherence and coaching layer for breathing exercise" (adherence = actually doing what was prescribed). The weak evidence is our opening: "the trials never checked if patients actually did it; we make it visible."

### D2. The two pillars (this is how the live site's front page tells it: "Two things go home with the patient")

| Pillar | What it is | Status |
|---|---|---|
| **1. Proof the breathing exercise was done** (the headline) | A clip-on unit under an ordinary breathing exerciser reads each breath. A voice coach guides it in the patient's language. The nurse's list shows who needs a call. A family member who opted in, with the patient's consent, sees progress. | Patient app, voice coach, nurse list, family page: **Live**. Breaths and breath labels: **Simulated**. The clip-on unit: **In development** (design + 3D model, not built). WhatsApp and calls: **Simulated**. |
| **2. The doctor's prescription, on the patient's phone** | The doctor types the prescription in the hospital software. The patient sees every medicine on their own phone, in plain words and in their language. At the pharmacy counter they show that screen. The chemist can scan a QR and see the hospital's own copy. No paper. | **Live** with sample patients. Not yet tried with a real pharmacy. |

Both end at the same place: the hospital can see, and the patient can show, what was really done.

### D3. Who it is for

- **Patients** recovering at home after heart, chest and upper-abdominal surgery. Mostly older people. Many cannot read small text or use a complicated app.
- **Ward nurses and physiotherapists**, who teach the exercise once and cannot watch every patient every hour.
- **Doctors**, who write the plan and the prescription.
- **Families**, often in another city, who worry.
- **Chemists**, who need to trust the prescription they are shown.
- **The buyer is the hospital** (or clinic). Patients and families never pay.

### D4. THE BIG PICTURE – Arogya Sathi (working name), with the SpiroBuddy breathing coach

**The idea:** SpiroBuddy starts with one thing (the assisted breathing exerciser) and grows into the link between a whole hospital and its patients at home. "Arogya Sathi" means "health companion". It is a **working name**. The hackathon entry and the live site stay named **SpiroBuddy**.

**Five kinds of account, all under one hospital**

| Account | Used on | Made by | What it does (the plan) | What works today |
|---|---|---|---|---|
| **Hospital** | Laptop | Us, during onboarding (with the hospital's name, logo and colour) | Whole-hospital view: patients checked in and out, beds in use, departments, staff, settings | Hospital admin login: **Live**. "App branding" page: **Live**. Hospitals kept apart in one system: **Live**. Whole-hospital view (check-ins, beds): **Planned**. Admin screens for staff, join code and settings: **In development**. |
| **Department** | Laptop | The hospital | Registers new patients; bed board (who is where, under which doctor); appointments; nurse duty roster | **Planned** (plan only). Department exists today only as a field on a staff account. |
| **Doctor** | Laptop | The hospital | Today's patients, patient records, prescriptions; saving updates the department and hospital views at once | Doctor login, "My patients" triage list, writing / changing / stopping a prescription: **Live**. "My day" page: **Planned**. Operation-theatre reminders: **Planned** (needs the hospital's own theatre schedule). |
| **Nurse** | Phone (laptop today) | The department | Her duty, rooms, patients, tasks, alerts | Nurse login, triage list, alerts inbox, "nurses see only their patients": **Live**. Nurse phone app with duty roster and rooms: **Planned** (plan only). |
| **Patient** | Phone | Department (registration number) + doctor (prescriptions) | Every prescribed medicine, pharmacy screen with QR, medicine times with "I took it", spoken missed-dose reminder, printable prescription, breathing coach if given a spirometer | Patient app, breathing coach (breaths **Simulated**), medicines page, pharmacy screen, QR check, dose tracking, "I do not feel well": **Live**. Medicine reminders in the app: **In development**. Spoken missed-dose reminder and printable PDF: **Planned** (plan only). |

Accounts hang from the hospital: Hospital → Departments → Doctors and Nurses; each patient belongs to a department and a doctor.

**Connected-device modules**
- The SpiroBuddy spirometer clip-on is **device module 1**. Status: **In development** (design + 3D model; not built).
- Later modules plug into the same screens over Bluetooth: pulse oximeter, blood-pressure cuff, peak-flow meter, other breathing or exercise devices a hospital lends out. Each is **Planned**. (Registry: "Pulse oximeter and BP cuff by Bluetooth" = Planned; "Bluetooth pairing" = Planned.)
- More device ideas, all **Planned**: a reader for three-ball exercisers (light gate or phone camera); a speaking base with a SIM for homes with no smartphone.
- In the patient app the device gets a big card on the home screen and a **Breathing** tab, shown only if the hospital gave that patient a device (**Planned**). In the nurse app it sits under More → Devices (**Planned**).
- A plain fact for the notes: Bluetooth from a web page works in Chrome on Android, not in Safari on iPhone, so iPhones need the store app.
- A device that measures a patient may fall under India's Medical Devices Rules 2017. We claim only "practice and recording" until we have the regulator's written view.

**More patient groups later (all Planned):** breathing practice before surgery; rehabilitation after TB treatment; long-term lung conditions (COPD). Today's focus, recovery after heart, chest and upper-abdominal surgery, is **Simulated** (sample patients).

**Business architecture**
- **One shared platform; each hospital kept apart.** Every record carries its hospital and the app checks it on each request, with tests: **Live**. Database-level row security on top: **Planned**.
- **A core plus add-on modules, switched on per hospital.** Core = the five accounts + prescriptions. Add-ons = the spirometer (module 1), later other devices. Per-hospital module switches: **Planned** (plan only).
- **Our own company console** (our staff only): the list of hospitals, their set-up and branding, which modules each has, usage, and the hospital's subscription invoices. **Planned** (plan only). **Money appears only there**, never in the hospital, nurse or patient apps.

### D5. The custom build (highlight this – it is part of the plan and of the business)

**[FOUNDER: I wrote 'custom build' as (a) + (b) + (c). Delete what you did not mean.]**

| | What "custom build" means | Honest status |
|---|---|---|
| **(a) A custom build for each hospital** | Each hospital gets its **own app name and logo inside the patient app** (for example "Dawnlight Care – with SpiroBuddy"), plus an accent colour on the name strip. The hospital admin sets it on an "App branding" page with a live phone preview; we set it up during onboarding. Safety messages and status labels stay fixed and cannot be changed by a hospital. | Own name and logo inside the app: **Live**. Home-screen icon with the hospital's own name and logo (each hospital gets its own web address): **Planned**. One SpiroBuddy app in the Play Store and App Store that shows the hospital's name inside after login: **Planned**. A hospital's own store listing: later, only from the hospital's own developer account. Hospitals registering themselves: **Planned** (today we set a hospital up). |
| **(b) Modules switched on per hospital** | One shared platform, each hospital a separate tenant. A core for every hospital, and add-on modules a hospital chooses (spirometer today, more devices later). "Land with one module, expand with more." | Separate hospitals in one system: **Live**. Module switches per hospital and our company console: **Planned** (plan only). |
| **(c) Our own custom-built clip-on device** | A small base that an ordinary breathing exerciser stands on. A sensor reads how high the disc rises. Designed by us for the volume (piston) type. Lent at discharge, cleaned, and reused for the next patient. | **In development: design + 3D model only. NOT built, not bench-tested.** Bluetooth pairing: **Planned**. |

**Moving a hospital in within minutes (Planned)**
A hospital's doctors, departments and patients can be moved in from a spreadsheet (or a standard FHIR health-records file). There is always a practice run first that shows what would happen and saves nothing. Old prescriptions arrive as "to confirm": a doctor must approve them before anything reaches a patient's phone. A hospital can export everything at any time (no lock-in). Status: **Planned**. Honest claim: "a hospital's doctors, departments and patients can be moved in within minutes from a spreadsheet; medicines need a doctor's confirm". SpiroBuddy sits **beside** the hospital's existing software; it does not replace it.

**Store apps – what they can and cannot do (Planned)**
- One generic app on the Play Store and the App Store that rebrands **inside** after login: possible.
- The **home-screen name and icon** of a store app **cannot change** after install.
- The home-screen name and icon **can** be the hospital's own for the web app: each hospital gets its own web address, and "Add to home screen" from the hospital's QR shows its name and logo (**Planned**).
- A hospital can publish its own listing (for example "Dawnlight Care") only from its own developer account.

### D6. Patient login (state it exactly like this)

- **Today:** a patient opens the app from a personal link or QR, no password. **Live.**
- **The design (being built now):** the patient types the **hospital registration number**, then a **one-time code (OTP)** sent to the phone number they gave at registration. Status in the registry at the time of writing: **In development**. A real SMS needs a paid SMS service and telecom (DLT) registration, so until then the code shows in an on-screen sample phone: that delivery will be labelled **Simulated**. "Login code sent by SMS" is **Planned**.
- **[FOUNDER: check /api/features on the live site before submitting; if the OTP login is there, say Simulated]**
- A staff-issued one-time **desk code** covers the special cases (section F8). Status: **In development**.
- Never call the login "secure" or "safe". Say what it does.

---

## E. EVERY PAGE THAT EXISTS TODAY

All pages are on the live site `https://spirobuddy.onrender.com`. All patients are sample patients. "Shot" = the screenshot file in `deck_shots.zip` (full list in section L).

### E1. Public pages (no login)

| Address | Who uses it | What it does | Status | Shot |
|---|---|---|---|---|
| `/` | Anyone, judges | The story site. Headline "Every breath, coached and counted." Sections: the two pillars · the problem (four sourced numbers) · who it helps (Ravi, Sister Anjali, Amit) · how it works in 3 steps · what is inside · "Safety is in the code, not left to the AI" · how we label what is real · try it yourself. A looping 3D model of the device sits beside the headline. | **Live** | 01, 02, 03, 04 |
| `/impact.html` | Judges | "Impact: who it helps, and how sure we are": who can use it · how many people · adoption and retention step by step · an impact calculator (sliders, rough estimates only) · numbers from this site · SDG 3. Every number cites its source or is labelled estimate, assumption or target. | Page and calculator **Live** · the site's own counts **Simulated** | 14, 14b, 14c, 14d |
| `/trust.html` | Judges | "Trust and safety": the rules and what SpiroBuddy does · ten safe-medication rules · AI audit · what we do not claim · what happens before a real pilot · how the AI is used. No outside body has reviewed the product. | **Live** | 15, 15b |
| `/vision.html` | Judges, mentors | "Vision: from a breathing exerciser to a recovery link between hospital and home": problem, solution, three tiers · business model in words · where we would start · roadmap · honest risks · the ask · scale and cost · "Works beside your hospital's software" · why drug-interaction checks are deliberately not built. | **Live** | 16, 16b, 16c, 16d |
| `/architecture.html` | Judges | The system diagram. Every box is coloured by its status. It also shows the path of a prescription: doctor types it → patient's phone → pharmacy counter → chemist scans the QR. | **Live** | 17, 17b |
| `/showcase/` | Judges | The 3D showroom: a turnable 3D model of the clip-on unit under a breathing exerciser, with a phone beside it. | A 3D design model. The device itself is **In development** (not built). | 18 |

### E2. Hospital side (staff log in)

| Address | Who uses it | What it does | Status | Shot |
|---|---|---|---|---|
| `/login.html` | Admin, doctors, nurses | "Hospital login": email and password. A "Sample logins" box lets a judge try as doctor, nurse or admin. Hashed passwords, 12-hour sessions, limits on wrong tries. | **Live** | 05 |
| `/dashboard.html` | **Nurse** (and doctor) | **The nurse dashboard, "Patients today".** Top bar: hospital and ward name, alert bell, clock. Four tiles: **Patients** (how many on track / to watch) · **Needs a call** · **Open alerts** (red / amber / mine) · **Sessions today** (done ÷ due – this is our impact metric, counted live). Below: the **triage list**, most urgent first (red flag → needs a call → watch → on track), with search, filter tabs and sort. Each row: status tag, patient, operation and day after surgery, the reason in plain words (for example "9 of 14 sessions done · best breath below 80% of personal best"), sessions done of due today, best breath against the goal, 3-day trend, last session, a **Call** button and an eye to open the patient. Fixed rules pick who needs a call; no AI decides. A nurse sees only her own patients. Side menu: Dashboard · Alerts · Patients · Units · Demo panel · Record breaths · 3D showroom. | Triage list, tiles, alerts: **Live**. The breath numbers behind them: **Simulated** | 06, 06b |
| `/patient.html?id=1` | **Nurse** (and doctor) | **The nurse's page for one patient (Ravi Kumar).** Header: name, status, age, operation, day after surgery, ward and bed, language, family members; buttons **Call patient**, **Print**, **Medicines**. Then: sessions today, best breath today, goal, 3-day trend · **Today's sessions** hour by hour (8 am–9 pm: done / missed / due now / upcoming) · **Best breath – last 7 days** chart against the goal · **Breath quality** bar (good / too fast / too shallow / no hold) · **Recent sessions** table with a score out of 10 and quality tags · **AI summary** (three plain sentences; a fixed template unless an AI key is set; it never diagnoses) · **WhatsApp** buttons (send summary to family / to nurse, send missed alert) · **Voice & language** · **Care team actions** ("Nurse: call patient now", call script) · open alerts for this patient with acknowledge · the **escalation ladder** with its steps · a communications timeline · **Patient login** card (hospital registration number DGH-000001, give a one-time desk code) · **Messages** sent for this patient · **Goal & settings** · **Care circle & reminders** (quiet hours, consent recorded, each family member with "Withdraw consent"). | Page **Live** with sample data · daily summary **Live** · triage rules **Live** · breath numbers **Simulated** · WhatsApp and calls **Simulated** · patient-login card **In development**. (The larger tabbed "patient chart" of the next version is **In development**.) | 07, 07b |
| `/prescribe.html?id=1` | **Doctor** | **"Medicines for Ravi Kumar".** Left: **Current medicines** – the issued prescription with its date and doctor (Dr. Meera Nair), each medicine in plain words, and **Change** and **Stop** buttons. Right: **Write a prescription** – medicine name, strength, form, dose, when to take it (Morning / Afternoon / Night buttons, or a typed code such as 1-0-1, BD, TDS), with food, for how long, "only when needed (SOS) – no reminder", a note for the patient. Then **What the patient sees** (a preview) and a confirm box "Send to the patient's phone?". No AI is involved. | **Live** | 08, 08b |
| `/units.html` | Nurse | **Units: lending the clip-on units.** Ward stock (who has each unit, battery, where it is in its cycle) and a hand-over log (who did what, and when). Flow: hand over a unit → take back → clean and check (three ticks, sign as cleaned) → wipe unit → back in stock. By design a unit stores nothing about a person. | **Simulated** (sample data). The page says "Preview – device in development". | 09, 09b |
| `/demo.html` | Presenter, judges | **The simulators page ("Demo control panel").** Reset the sample data. A card per patient: simulate a good / mixed / poor session, simulate 2 missed slots, send a summary to family. **"Calls & WhatsApp – live simulators"**: two on-screen phones (the patient's and the family member's) show the WhatsApp messages and calls that would be sent; **Play escalation ladder** runs the reminder ladder step by step; red-flag message; weekly progress card; voice note; "Nurse calls patient"; a live feed and a message log. | Controls **Live** · WhatsApp, calls and the ladder **Simulated** ("dry run" – nothing is really sent) | 10, 11, 12, 12b |
| `/branding.html` | **Hospital admin** | **"App branding".** App name, short name, accent colour (used only on the name strip; the page refuses colours that are hard to read), logo upload (checked, shrunk, cleaned). A live phone preview "What patients see" (for example "Dawnlight Care – with SpiroBuddy"). A list "What a hospital can not change": the safety messages, the status labels and their colours. | **Live** | 13, 13b |
| `/collect.html` | The team | "Record labelled breaths": a tool for recording breaths with a label (good, too fast ...) to train the breath model. Works with the simulator today. | An internal tool; no real breaths recorded yet | – |

### E3. Patient, family and chemist side (phone)

| Address | Who uses it | What it does | Status | Shot |
|---|---|---|---|---|
| `/app.html?id=1` | **Patient (Ravi)** | **The breathing coach app.** Large text, no typing. The hospital's own name and logo at the top. One big **Start** button. During a breath: a simple piston picture, the volume, a spoken cue in the patient's language ("breathe in slowly… hold… well done"), amber "slower" when too fast. The session saves itself; today's ticks update. Buttons to **My medicines** and **I do not feel well** (a fixed message: contact your nurse / call 112, and a nurse alert – no AI). A cheer from family is played after the next session. Shows the last saved day when offline. Installs to the home screen. | App, voice, help button, offline view: **Live** · breaths and breath labels: **Simulated** | 20, 20b, 21 (four moments), 22 |
| `/meds.html?id=1` | **Patient** | **"My medicines".** Every medicine the doctor prescribed, in plain words, grouped by time of day, in the patient's language (English, Hindi, Tamil, Malayalam). "I took it" is recorded as *reported*, never as *taken*. A button **Show at the medicine shop**. | **Live** (Tamil and Malayalam text still needs a native-speaker check) | 23, 24 |
| `/meds.html` → "Show at the medicine shop" | **Patient, at the pharmacy** | **The pharmacy screen.** One clear "paper" on the phone: hospital, doctor, date, patient, every medicine, and a **QR code** the chemist can scan. Says "Sample patient". | **Live** (sample data; not tried with a real pharmacy) | 25 |
| `/rx.html?t=<code>` | **Chemist** | **"Prescription check".** Opens when the chemist scans the QR. No login. Shows the issuing hospital's own copy, marked **Current** (or not current if the doctor changed or stopped it), so the chemist can compare it with the phone. | **Live** (sample patients only) | 26, 26b |
| `/guardian.html?t=<code>` | **Family (Amit)** | **The family page.** A private link for one family member, shown only with the patient's consent. Today's status in plain words, today's ticks, and a way to send a cheer. | **Live** | 27, 27b |
| `/patient-login.html` | Patient | **Patient login** with the hospital registration number (see D6). In English, Hindi, Tamil and Malayalam. | **In development** | 28, 28b |

---

## F. ALL THE USE CASES (short journeys; every step has its status)

### F1. Ravi, 58, the patient at home – a breathing session
1. Ravi opens the app from his personal link or QR. No password. **Live**
2. The top of the app shows his hospital's own name and logo. **Live**
3. He taps the one big **Start** button. **Live**
4. He breathes in through the exerciser. The breath comes from the built-in simulator today. **Simulated** (the clip-on unit that would read it is **In development**)
5. The voice coach speaks in Hindi: breathe in slowly, hold, well done. Voice in 10 Indian languages and English. **Live**
6. Each breath gets a label and a score: good, too fast, too shallow, no hold. **Simulated** (the model was trained on simulated breaths)
7. Too fast → the coach says "slower" at once and the screen turns amber. **Live** (on a simulated breath)
8. The session saves itself. Nothing to type. Today's ticks update. **Live**
9. No internet → the app shows the last saved day with a clear notice. **Live**

### F2. Ravi – medicines
1. Ravi taps **My medicines**. He sees every medicine Dr. Meera Nair prescribed, in plain words, in Hindi. **Live**
2. He taps "I took it". It is shown as *reported*, never as *taken*. Nobody measures it. **Live**
3. A full-screen reminder with a chime and voice at the due time (while the app is open). **In development**
4. Reminders when the app is closed; a spoken missed-dose reminder. **Planned**
5. Ravi cannot switch a medicine off. He can tell the doctor; only the doctor changes the plan. (design rule)

### F3. Ravi – at the pharmacy counter
1. Ravi taps **Show at the medicine shop**. **Live**
2. The phone shows one clear prescription screen with a QR code. No paper. **Live** (not tried with a real pharmacy)
3. The chemist scans the QR (section F6).

### F4. Ravi – "I do not feel well"
1. Ravi taps **I do not feel well**. **Live**
2. The app shows one fixed message: contact your nurse, or call 112. No AI writes it. **Live**
3. A red-flag alert goes to the nurse's list. **Live**
4. The same happens if red-flag words (for example "chest pain") appear in a message. **Live**

### F5. Sister Anjali, the ward nurse
1. She logs in. She sees only her own patients. **Live**
2. The dashboard shows four numbers: patients, needs a call, open alerts, sessions done ÷ due today. **Live**
3. The triage list puts the most urgent patient on top, with the reason in plain words. Fixed rules, not AI. **Live**
4. She opens Ravi's page: today's sessions hour by hour, best breath over 7 days, breath quality, a three-sentence daily summary. **Live** (breath numbers **Simulated**)
5. Ravi misses two sessions → the **reminder ladder** starts: the unit beeps and lights → a WhatsApp reminder to Ravi → an automated call → a message and call to the family member who opted in → an alert to the nurse → the nurse calls. The steps run for real; the messages and calls go to the built-in simulators. **Simulated**
6. She acknowledges each alert in the alerts inbox. **Live**
7. She taps **Call patient**. Today the call plays in the phone simulator. **Simulated**
8. A missed-dose alert after the grace time. **In development**
9. A phone app for nurses with her duty roster, rooms and tasks. **Planned**

### F6. Dr. Meera Nair, the doctor
1. She logs in and sees her patients, the ones who need a call at the top. **Live**
2. She opens Ravi → **Medicines** → **Write a prescription**: name, strength, form, dose, when, with food, how long, a note. She can tap Morning / Afternoon / Night or type a code such as 1-0-1 or BD. **Live**
3. She checks "What the patient sees" and confirms "Send to the patient's phone?". The prescription is **Issued**. **Live**
4. **Change:** she edits it and sends a new version. Ravi's phone shows the new one. **Live**
5. **Stop:** she stops the prescription. The chemist's QR check then no longer says "Current". **Live**
6. A "My day" page (patients to call, prescriptions ending soon, visit requests, missed doses). **Planned**
7. Operation-theatre reminders. **Planned** (needs the hospital's own theatre schedule)
8. AI that drafts a prescription from a photo, with a person checking every line. **In development** – a side helper, never the headline.

### F7. The chemist
1. The patient shows the pharmacy screen. **Live**
2. The chemist scans the QR with any phone camera. No app, no login. **Live**
3. The page shows the issuing hospital's own copy, marked **Current**, to compare with the phone. **Live** (sample patients only; not tried with a real pharmacy)

### F8. Amit, the son far away (family, with consent)
1. Ravi agrees to share; Amit opts in. Consent is recorded on Ravi's staff page and can be withdrawn there. **Live** (a fuller itemised consent screen is **In development**)
2. Amit opens his private link: today's status and ticks. **Live**
3. He sends a cheer; Ravi hears it after his next session. **Live**
4. A short daily WhatsApp update to Amit. **Simulated** (previews; real sending is **In development**, only to the team's own test numbers)
5. One word, STOP, or "Withdraw consent", ends the updates. **Simulated** / **Live** on the staff page
6. Family sees medicines, visits and shared papers. **Planned**

### F9. The hospital admin
1. Logs in as admin. **Live**
2. Opens **App branding**: types the app name and short name, picks an accent colour, uploads the logo, sees the live phone preview, saves. Patients of that hospital now see it at the top of their app. **Live**
3. Cannot change the safety messages or the status labels. **Live**
4. Staff logins for admin, doctors and nurses exist. **Live**. The screens to manage staff, the join code for new doctors and the hospital settings: **In development**
5. Two sample hospitals run side by side and cannot see each other's patients. **Live**
6. Moving a whole hospital in from a spreadsheet. **Planned**

### F10. The unit moves from one patient to the next
1. The nurse hands a unit to a patient at discharge (**Hand over a unit**). **Simulated**
2. The patient brings it back; the nurse taps **Take back**. **Simulated**
3. **Clean and check:** three ticks, sign as cleaned. **Simulated**
4. **Wipe unit:** it returns to "In stock" for the next patient. By design the unit stores nothing about a person. **Simulated**
5. Every step lands in the hand-over log: who, what, when. **Simulated** (sample data; the device is **In development**)

### F11. Special cases in the login design (all part of the login now **In development**)
| Case | What happens |
|---|---|
| **Admitted unconscious, or no phone with them** | Staff register the patient with the phone box empty. The record shows **"Phone number pending"**. Nothing in the hospital's own work depends on it. When the patient is awake and agrees, staff add the number. |
| **The code does not arrive, the phone is lost, or the number changed** | Staff check who the person is at the desk, correct the number, or give a **one-time desk code** (made by the server, shown once, stored only scrambled). |
| **No smartphone** | No app login is needed. The hospital side works as usual. Reminders by call or WhatsApp to a basic phone are the existing channels (**Simulated**). A speaking base with a SIM is **Planned**. |
| **A family member's phone instead** | Only with the patient's recorded consent. For a patient who cannot consent: **Planned**, needs a real hospital's own policy. |

Login limits in the design: a code works once and for 10 minutes; 5 wrong tries lock that login for 15 minutes; the page answers the same way whether or not a number exists.

---

## G. The facts and numbers ChatGPT may use

**Rule:** use a number only with the source tag in the last column, in small text on the same slide. "Estimate", "assumption" and "target" are our own figures and must carry that word.

### G1. The problem

| Number | What it means | Print this source tag |
|---|---|---|
| **1 in 10** (10.4% of 9,864 patients, 146 hospitals, 29 countries) | Adults having surgery who get a lung complication | LAS VEGAS study, Eur J Anaesthesiol 2017 |
| **19.5% vs 0.5%** | Died within 30 days with vs without a lung complication (2,464 patients, Spain). A link, not proof of cause | Canet et al., Anesthesiology 2010 |
| **21.7 vs 12.5 days in hospital; 8.5 vs 1.4 days in ICU; 28% died** | Patients with lung complications in a Udaipur study | Int Surg J 2018 (small, single centre) |
| **12.9%** (53 studies, 8.9 million patients) | Heart-bypass patients back in hospital within 30 days; mostly Western data | J Cardiothorac Surg 2021 |
| **4.7%** (30 centres, 810 patients) | Back in hospital within a month after major abdominal cancer surgery in India | Indian J Anaesth 2026 |
| **86%**; top reason **forgetting (83.5%)**; 1,681 respondents | US nurses and respiratory therapists who say patients don't use the exerciser as they should | Eltorai et al., Respir Care 2018 |
| **6%** did it properly on day 1; 54% poorly; **72%** right by day 3 with teaching (60 patients) | A Chennai hospital | J Pharm Bioallied Sci 2024 (small study) |
| **1 in 4** (100 patients) | Cancer-surgery patients in Hyderabad who couldn't do the exercise correctly | Anesth Essays Res 2018 (small study) |
| **About 49 lakh a year** | Major operations in India's public records, an undercount | India HMIS public records 2019, Int J Surg 2024 |

### G2. Why India needs a different design

| Number | What it means | Source tag |
|---|---|---|
| **3 in 4** older Indian women can't read (literacy 24%); **37%** of older Indians have low vision | So SpiroBuddy speaks | LASI Wave 1 |
| **2 in 3** older Indians live with their children; about 6% live alone | So the update goes to the family | LASI Wave 1 |
| **87%** of households have a mobile; **29%** of over-60s have difficulty making a call (35% of older women) | So the patient never has to dial or type | LASI Wave 1 India Report |
| **41%** of older Indians own a smartphone | So it must work on the family's phone | HelpAge India 2025 (single source) |
| **19.5%** of rural patients aged 45+ had a smartphone (urban 36.5%; 318 people, Telangana) | Same point | Med J Armed Forces India 2024 (one region) |
| Hindi is the mother tongue of **43.6%** of Indians | So many languages | Census 2011 |
| **2.6** nursing staff per 1,000 people; WHO benchmark **3** | Nurses are short of time | Rajya Sabha reply, July 2026 |
| Reaches **half** on the first call, **3 in 4** by the third | India's Kilkari voice-call service; so calls are retried up to 3 times | BMJ Glob Health 2021 |
| Unplanned visits **1.2 vs 2.6** (75 patients, Bihar) | Supporting caregivers through a Hindi website and WhatsApp group | Indian J Cancer 2026 (pilot) |

### G3. Proof that tracking and reminders help

| Number | What it means | Source tag |
|---|---|---|
| **28% → 58%** of waking hours with exercise (145 bypass patients, USA). Say "hours", never "patients" | An hourly reminder doubled it | Eltorai et al., JAMA Surgery 2019 (randomised trial) |
| **17 → 35** breaths a day | The same trial | Eltorai et al., JAMA Surgery 2019 |
| **9 trials, 1,209 lung-cancer patients** | Spirometry inside a breathing-exercise bundle cut lung complications and shortened stays | BMC Pulm Med 2024 |
| **246 of 260** TB survivors completed 12 weeks (5 Indian centres) | Home lung rehab with phone follow-up | Indian J Med Res 2025 (no comparison group) |
| **76%** still exercising after 8 weeks, **58%** after a year (45 patients, Thar Desert) | Phone-guided Hindi rehab for older rural patients | Lung India 2025 (feasibility study) |

### G4. What exists already (never say nothing exists)

| Fact | Source tag |
|---|---|
| The US FDA cleared **InSee**, a clip-on spirometer tracker, on 21 August 2025 (K241152). It reads the piston with an infrared sensor, fits one US spirometer and is cleared for hospital use only | US FDA database; IEEE Spectrum 2020 |
| Amrita (Kochi) is running a trial of a nurse-led AI chatbot with an ECG patch after bypass surgery. It needs a smartphone and does not track breathing exercise | JMIR Res Protoc 2026 (protocol) |
| Hospital-chain apps and ABHA health-locker apps exist | general knowledge; no number |
| Standard instructions: breathe in slowly, hold 3–5 seconds, about 10 breaths every waking hour | MedlinePlus 2025; Cleveland Clinic 2026 |
| The evidence that the exerciser alone prevents complications is weak; those trials rarely recorded whether patients did the exercise | Cochrane 2014; a 2024 cardiac-surgery review |

### G5. Money (all our own figures are estimates)

| Number | What it means | Source tag / label |
|---|---|---|
| **₹1,62,400** | Flat Ayushman Bharat payment for a bypass, 10-day stay built in. Extra days come out of the hospital's pocket | HBP 2022 rate list (state copy) |
| **₹2,307** | Average cost of one ward bed-day (57 hospitals, 11 states) | CHSI, BMJ Open 2023 |
| **₹25,927** | One ICU bed-day at PGIMER | Lung India 2024 |
| **About ₹2,500** | Parts per clip-on unit | estimate (team, from shop prices) |
| **About ₹1,365** | A hand-built cable prototype | estimate |
| **About 10** | Loans per unit (lent, cleaned, reused) | assumption |
| **About ₹1,000** | Price per patient episode; less than half a ward day | planned price, estimate; not tested with a hospital |
| **About ₹500–700** | Our cost to serve one patient episode | estimate |
| **₹0.12** (₹0.115) | One WhatsApp update | Meta India utility rate card |
| **About ₹8** | A 2-minute AI phone call, roughly 70 times a WhatsApp message; so WhatsApp first, calls only to escalate | our maths from published prices |
| **About ₹5.5 lakh** | A 30-patient, 3-month pilot at one hospital (range about ₹2.1–12.4 lakh) | middle estimate (team) |
| **Up to ₹10 lakh** | One NIDHI-PRAYAS grant – the grant's upper limit, not money we hold | grant scheme limit |
| **₹200 per patient** | Only later, at scale, as a software fee once hospitals own the units | estimate; never "device plus software for ₹200" |

### G6. Scale stages (only Stage 0 is Live; Stages 1–4 are Planned; every cost is an estimate)

| Stage | Patients active at once | Monthly running cost, units lent (estimate) |
|---|---|---|
| 0 – Today | sample patients only | ₹0 hosting (free for the demo only) |
| 1 – Pilot, 1 hospital | 25–50 | ₹32,000–59,000 |
| 2 – 10 hospitals | about 250 | ₹2.8–3.8 lakh |
| 3 – about 100 hospitals | 2,500 | ₹25.8–30.2 lakh |
| 4 – State or national programme | 100,000+ | not yet fully costed |

Three sentences that may be used as they are: "Today one web service and one database run this site, with sample patients." · "Planned growth is staged: one pilot hospital, ten, a hundred, then state programmes." · "Each patient episode should cost five to seven hundred rupees, an estimate; our planned price is about one thousand."

### G7. The later TB group (Planned)

| Number | What it means | Source tag |
|---|---|---|
| **About 26 lakh** TB patients notified a year; **90%** finish treatment | India | PIB, March 2026 |
| **59%** still had impaired lungs at the end of treatment | A Madurai study | published study, Madurai |
| **16–17 lakh** people a year finish treatment for lung TB | Our estimate from WHO data (74% of cases are in the lungs, about 18.5 lakh in 2024) | team estimate from WHO notification data |
| India's 2024 TB rehab guidance (a draft) lists the incentive spirometer among its breathing exercises, for supervised sessions | | RBIPMT 2024 draft guidance (ntep.in) |

### G8. SDG 3 mapping (wording checked against the UN targets)

| Target | UN wording (short) | Our honest link |
|---|---|---|
| **3.8 (main)** | Universal health coverage: access to quality essential health-care services | Brings follow-up of a standard post-surgery exercise into the home, in the patient's language |
| **3.4** | Reduce premature deaths from non-communicable diseases; promote well-being | Supports recovery after heart and cancer surgery. We do not claim to move the death rate |
| **3.c** | Recruit, develop, train and retain the health workforce | Lets one nurse see which of many patients needs a call |
| (3.3, later) | End TB and other epidemics | Only through the TB-survivor rehab roadmap. Future, not current impact |

### G9. Readiness (TRL) – one line

**TRL 3–4:** the software works end to end on a live site with simulated breaths (about TRL 4 for the software), but the sensor unit is only a design and a 3D model, and nothing has been tested with real users or patients (TRL 3 for the device).

### G10. The impact metric

**Sessions done ÷ sessions due** – the share of the prescribed hourly sessions a patient actually completes. It is counted automatically and shown live on the nurse dashboard ("Sessions today"). The only reference point is the US trial: 28% → 58% of waking hours. **No Indian baseline exists yet. We state no pilot target.** First pilot: 30 patients on one ward for 3 months; we report the number whatever it is. We will not claim fewer complications until a proper study shows it.

### G11. Adoption and retention – our assumptions (never present these as results)

Per hospital department, per month:

| Step | Who | Number | Label to print |
|---|---|---|---|
| 1 Reach | the hospital | about 50 eligible patients | estimate |
| 2 Join | Ravi consents · Amit opts in | 40 join (8 in 10) · 24 families opt in (6 in 10 of those who join) | assumption |
| 3 Start | Ravi | 36 do a home session on day 1 (9 in 10) | assumption |
| 4 Stay | Ravi | still going: 34 on day 3 · 30 on day 7 · 26 on day 14 (85% · 75% · 65%) | assumption |
| 5 Do | Ravi · Sister Anjali | about 58% of due sessions done · the nurse opens the list on 9 days in 10 | target · assumption |
| 6 Pay | the hospital | 1 pilot hospital in 3 goes on to pay | target |

Footnote that must sit under it: "Estimates, not results. Basis: Lung India 2025 and Indian J Med Res 2025 (home rehab); LASI; Eltorai, JAMA Surg 2019; our arithmetic. A pilot of 30–50 patients measures every step."

### G12. Product facts

- Voice coach: **10 Indian languages and English**; 341 recorded clips for offline use; the browser voice is the second fallback.
- Screen languages: English, Hindi, Tamil, Malayalam (Tamil and Malayalam still need a native-speaker check).
- Breath model: labels good / too fast / too shallow / no hold; **95.8% on simulated breaths**; real-patient accuracy not measured; simple rules as a backup.
- Sessions: one per hour, 8 am to 9 pm (14 a day).
- 400+ automated tests.
- Regulation: the plain incentive spirometer is Class A (lowest risk) on CDSCO's list. Our clip-on measures and alerts, so we **expect Class B** and would confirm with CDSCO before any patient.
- Sensor: the chip is ±2 cm out of the box but steady, so we calibrate it to each exerciser's printed marks (ST datasheet).
- Tech: web pages in plain HTML, CSS and JavaScript (nothing to install) · Python FastAPI server · Postgres database · hosted in the cloud. Every AI or internet feature has an offline fallback.
- AI parts: (1) the breath model; (2) the voice; (3) a three-sentence daily summary written by a language model, with a fixed template as the fallback. Not AI, on purpose: red-flag messages, alerts, triage, reminders.

---

## H. WHAT IS LEFT TO BUILD AND TO CONFIGURE

This is the honest list. "In development" = partly built. "Planned" = not started. Most important first inside each group.

### H1. To build

**The device (our own clip-on unit)**
1. Build and bench-test one clip-on unit (firmware and 3D design exist; no unit is built). **In development**
2. Record real breaths with it and re-train the breath model (today's model has seen only simulated breaths). **Simulated today**
3. Bluetooth pairing (the design sends by USB for now). **Planned**
4. A reader for three-ball exercisers (light gate or phone camera). **Planned**
5. A speaking base with a SIM, for homes with no smartphone. **Planned**
6. More device modules: pulse oximeter, blood-pressure cuff, peak-flow meter by Bluetooth. **Planned**
7. A live 3D twin of the device on the staff page and a public twin page. **In development**

**The patient app**
1. Patient login with the hospital registration number + a one-time code. **In development**
2. Medicine reminders in the app (full-screen card, chime, voice). **In development**
3. Ask for and book a visit; visit reminders. **In development**
4. A document vault for discharge papers and reports. **In development**
5. Tabs: Today · Medicines · Breathing (only if given a device) · Help. **Planned**
6. Reminders when the app is closed; saving taps while offline. **Planned**
7. A printable prescription (PDF); a spoken missed-dose reminder. **Planned**
8. Patient or family sends a prescription photo (it waits for a doctor). **Planned**
9. Family sees medicines, visits and shared papers. **Planned**
10. Tele-consult. **Planned**

**The hospital side**
1. Enrol a patient step by step (details, consent, plan, link); printed handout with QR. **In development**
2. The full patient chart (breathing, medicines, visits, papers, care team, notes, device, timeline). **In development**
3. Missed-dose alert to the nurse. **In development**
4. Admin screens: hospital profile, staff management, join code, settings. **In development**
5. Doctor sign-up with a hospital join code; nurse access keys. **In development**
6. Doctor availability and slots. **In development**
7. Pause, complete or stop a programme. **In development**
8. Doctor's "My day" page. **Planned**
9. Operation-theatre reminders (needs the hospital's theatre schedule). **Planned**
10. Reports and CSV exports; printable discharge plan. **Planned**

**The platform (Arogya Sathi, working name)**
1. Department account with a bed board, check-in and check-out. **Planned**
2. Whole-hospital overview (checked in, checked out, beds in use). **Planned**
3. Nurse phone app (duty roster, rooms, tasks). **Planned**
4. Moving a hospital in from a spreadsheet, with a practice run. **Planned**
5. Home-screen icon with the hospital's own name and logo. **Planned**
6. One app in the Play Store and the App Store. **Planned**
7. Modules switched on per hospital, and our own company console. **Planned**
8. Hospitals registering themselves. **Planned**
9. Database-level row security per hospital (today the app does the check). **Planned**
10. FHIR export (a standard health-records file) for one patient. **In development**
11. Link to India's national health records (ABDM) and an ABHA number field. **Planned**
12. Hospital single sign-on. **Planned**

**AI**
1. AI drafts a prescription from a photo, a person confirms every line; turning "1-0-1, BD, TDS" into times by fixed rules. **In development** (a side helper only)
2. AI reads handwriting (experimental, off by default). **In development**
3. AI suggests a paper's type, title and date. **In development**
4. An AI register: every AI call logged by reference with the human decision. **In development**
5. Drug-interaction and dose-range checks: **deliberately not built** (that would be clinical decision support).

**Messaging**
1. Real WhatsApp sending and real phone calls (today they work only to the team's own test numbers). **In development**
2. Login code by SMS. **Planned**
3. Medicine reminders by phone call or WhatsApp. **Planned**

**Trust and compliance**
1. Itemised consent (separate choices for reminders, family sharing, records, AI) and a "no AI" choice. **In development**
2. Audit log viewer with filters; a tamper-evident audit log. **Planned** (the log itself is written today: **Live**)
3. Data export and deletion requests. **Planned**
4. A pilot readiness checklist (14 steps before any real pilot; none done for a real hospital). **Planned**
5. Teach-back question at consent; rules for any use of data to train AI. **Planned**

### H2. To configure / to arrange (needs an account, a key, an approval or a partner)

| What | Why it is needed | State today |
|---|---|---|
| A paid **SMS service + telecom (DLT) registration** of the sender name and message | To send the login code by real SMS. Takes days | Not arranged. Code delivery is Simulated until then |
| A **WhatsApp Business account** with Meta-approved "utility" message templates | To send real updates to patients and family | Not arranged. Messages are previews |
| A **registered Indian caller ID** and call-provider account; advance declaration of automated calls (TRAI's 2026 rules) | For real reminder and escalation calls | Not arranged. Calls are simulated |
| The **Gemini API key** (on the laptop and on the hosting service) | For the AI helper that drafts from a photo | Not added. The helper stays In development |
| A paid **voice service key** | For live voice in all languages (recorded clips and the browser voice work without it) | Optional; fallbacks are on |
| **Device parts and a bench test** | To build the first real unit (about ₹2,500 of parts, estimate) | Not bought |
| A **registered ethics committee** and **CDSCO's written view** on the device class (we expect Class B) | Before any real patient | Not started |
| A **pilot hospital** (one nurse or physio team) | For the 30-patient, 3-month pilot | None yet – this is our ask |
| **Data-law (DPDP Act 2023) checks**; hosting in India | Before real patient data. Today's web service runs in Singapore | Designed for; nothing checked by an outside body |
| **Play Store and App Store developer accounts** | For the store apps | Not opened |
| **Trademark and store search for the name "Arogya Sathi"** | The Government has a "TB Aarogya Sathi" app; a registry search has not been done | Working name until checked |
| **Native-speaker check** of the Tamil and Malayalam screens | Before real use | Pending |
| **Funding** for the pilot: about ₹5.5 lakh (middle estimate) | A grant such as NIDHI-PRAYAS could cover it | Not applied yet |
| A **pharmacy** willing to try the phone prescription and QR check | To test pillar 2 for real | None yet |

### H3. How to PRESENT this in the deck

Show it as **the growth path and the ask, not as an apology**. Say what works first (the site is live and can be tried from the QR), then show the rest as a clear, staged plan: module 1 today, more modules next, the whole-hospital platform after. Each unbuilt piece gets a calm status word (Simulated · In development · Planned), never "not yet", "only" or "just". The long list above proves the product has a lot of room to grow; the roadmap slide turns it into three steps (90 / 180 / 365 days); the ask slide says exactly what would unlock it: one hospital team, regulatory guidance, about ₹5.5 lakh. One "Honest status" slide carries the limits, so the other slides can speak with confidence.

---

## I. THE SLIDE-BY-SLIDE PLAN (template order)

**How every content slide is laid out**
- **Title bar:** the template's own title box, with the text given below.
- **Headline:** one sentence right under the bar, navy, bold, about 20–22 pt. It is the slide's ONE message.
- **Body:** between the headline and the footer. At least 14 pt. Few words.
- **Status tags:** small rounded labels with the word (Live / Simulated / In development / Planned).
- **Source line:** one small grey line (10 pt) just above the footer.
- **Notes:** the speaker notes. "Script" = the matching lines of the 5-minute talk. "Extra" = not in the 5-minute talk; for the reader.
- Extra slides are marked **(extra)**. They are duplicates of a template content slide, inside the same section.

**Final order: 25 slides** (16 from the template + 9 extra).

---

### Slide 1 – Title page (template slide 2)
- **Hackathon theme line:** Health & Well-being · SDG 3
- **Product name:** SpiroBuddy
- **Tagline (the elevator-pitch line):** Every breath, coached and counted.
- **One line under it:** After surgery, the hospital stays connected to the patient at home.
- **Team line:** - By GuGu GaGa
- **Small text, bottom left:** Live site: spirobuddy.onrender.com · Sample patients and simulated breaths. The clip-on device is in development.
- **Product logo (top-left circle):** `00_product_logo.png`. Remove the words "Product Logo".
- **Hero visual (the frame on the right):** `18_showroom_3d_device.png`, cropped to the device. Caption above: "Clip-on unit under an ordinary breathing exerciser". Tag below: **3D design model – device in development**.
- **Keep:** the DTI logo, top right, untouched. **Add:** the footer line and footer text copied from a content slide. No page number.
- **Notes (script 0:00–0:10):** Good afternoon. I'm [ADD: name], from team GuGu GaGa. This is SpiroBuddy, in the Health and Well-being track. After surgery, patients go home with a plastic breathing exerciser and are told to use it every hour, and nobody, not the nurse, not the family, not even the clinical trials, has checked whether they actually do. SpiroBuddy makes that visible.

### Slide 2 – Problem Statement
- **Headline:** After surgery, patients are told to do a breathing exercise every hour. Nobody sees whether they do it.
- **Left column (four labelled rows):**
  - **WHAT?** Patients go home with a breathing exerciser (an incentive spirometer) and a paper prescription. Nobody can see if the exercise is done, or done right.
  - **WHO?** Older patients after heart, chest and abdominal surgery; their ward nurses; their families.
  - **WHY NOW?** 87% of households have a mobile phone, and flat-rate insurance makes every extra bed-day the hospital's own cost.
  - **HOW BIG?** About 49 lakh major operations a year in India's public records, an undercount.
- **Right column (three big numbers):**
  - **1 in 10** adults having surgery gets a lung complication – LAS VEGAS study, 29 countries, 2017
  - **86%** of US nurses and therapists say patients don't use the exerciser properly. Top reason: forgetting – Eltorai et al., Respir Care 2018
  - **6%** of 60 patients in a Chennai hospital did the exercise properly on day 1 after surgery – J Pharm Bioallied Sci 2024 (small study)
- **Bottom band:** **Why the evidence looks weak, and what we fix:** reviews find the exerciser on its own makes little difference. But those trials rarely recorded whether patients actually did the exercise. **SpiroBuddy makes that visible.**
- **Source line:** LAS VEGAS, Eur J Anaesthesiol 2017 · Eltorai et al., Respir Care 2018 (1,681 respondents) · J Pharm Bioallied Sci 2024 · LASI Wave 1 (87%) · Ayushman Bharat HBP 2022 rate list · India HMIS 2019, Int J Surg 2024 (49 lakh) · Cochrane 2014 and a 2024 cardiac-surgery review
- **Screenshots:** none.
- **Notes (script 0:10–0:45):** After an operation, many patients go home with this: an incentive spirometer, a plastic breathing exerciser. Breathe in slowly, the disc rises, hold, ten times every waking hour. About one in ten adults having surgery gets a lung complication. Now the strange part. Reviews say the exerciser on its own makes little difference. But those trials almost never checked whether patients actually did it. Eighty-six percent of nurses say patients don't use it properly, mostly because they forget. In a Chennai study, only six percent did it right on day one. Nobody can see who is doing it. We make it visible.

### Slide 3 – Social Impact & SDG Alignment
- **Headline:** Our impact metric is one number, counted automatically: sessions done ÷ sessions due.
- **Top left card – Primary beneficiaries:** **Patients** recovering at home after major surgery · **Nurses**, who see which patient needs a call · **Families**, updated only with the patient's consent. **Expected outcome:** more of the prescribed sessions really done, and done right. We will not claim fewer complications until a proper study shows it.
- **Top right table – SDG 3:** the three rows 3.8 (main), 3.4, 3.c from section G8 (columns "SDG 3 target" / "Our honest link").
- **Bottom left table (replaces the template's "Year 1 / Year 3" table):**

  | Impact metric | Today (sample patients) | First pilot (Planned) |
  |---|---|---|
  | Sessions done ÷ sessions due | Counted automatically; simulated breaths | Measured on one ward: 30 patients, 3 months. No Indian baseline exists yet |
  | Breaths done correctly (speed, depth, hold) | Labelled by a model trained on simulated breaths | Real breaths recorded and the model re-trained before the pilot |

- **Bottom right big number:** **28% → 58%** of waking hours with exercise, when patients got an hourly reminder – US randomised trial, 145 bypass patients, JAMA Surgery 2019
- **Source line:** SDG wording checked against the UN targets. The pilot size is a plan; we state no Year-1 or Year-3 numbers and no outcome target, because no baseline exists.
- **Screenshot (optional, small inset):** the "Sessions today" tile cropped from `06_nurse_dashboard.png`, with the caption "Counted live on the nurse dashboard (0 / 0 here: the picture was taken at night, before the first session of the day)".
- **Notes (script 3:25–3:55):** Our impact metric is one number: the share of due hourly sessions completed. It is counted automatically. In a US trial, hourly reminders alone doubled the share of waking hours with exercise, from twenty-eight to fifty-eight percent. In our first pilot, thirty patients on one ward, we will measure that same number on an Indian ward, and report it whatever it is. This serves SDG 3: target 3.8, access to quality care, and 3.4, recovery from heart and lung disease. We will not claim fewer complications until a proper study shows it.

### Slide 4 – Social Impact & SDG Alignment: Adoption and Retention (extra)
- **Headline:** How we expect people to join and stay: our assumptions, step by step. A pilot measures every step.
- **Body:** the six-step table from section G11 as a left-to-right funnel (Reach → Join → Start → Stay → Do → Pay), one number per step, with the word **estimate**, **assumption** or **target** under each number in small type.
- **Footnote on the slide:** Estimates, not results. Basis: Lung India 2025 and Indian J Med Res 2025 (home rehab); LASI; Eltorai, JAMA Surg 2019; our arithmetic. A pilot of 30–50 patients measures every step.
- **Screenshot (optional):** `14b_impact_adoption_steps.png` as a small inset, caption "The same steps on the live site's Impact page".
- **Notes (extra):** Adoption and retention, as estimates, not results. One hospital department: about fifty eligible patients a month. We assume forty join and thirty-six start on day one; three in four are still going at day seven, two in three at day fourteen. Six in ten families opt in. One pilot hospital in three goes on to pay. A pilot of thirty to fifty patients would test every step.

### Slide 5 – Target Beneficiaries
- **Headline:** The people who need it most cannot be asked to learn a complicated app.
- **Three persona cards:**
  - **Ravi, 58 – the patient.** Going home after abdominal surgery. Speaks Hindi; uses the family phone. **Pain:** forgets the exercise or breathes too fast, and nobody sees. Paper prescriptions get lost. **Needs:** a voice in his language, one big button, no typing. *Only 41% of older Indians own a smartphone* – HelpAge India 2025
  - **Sister Anjali – the ward nurse.** Teaches the exercise once, at discharge. **Pain:** cannot check every patient every hour. **Needs:** one list with the most urgent patient on top, and an alert only when someone needs a call. *2.6 nurses per 1,000 people; the WHO benchmark is 3* – Rajya Sabha reply, July 2026
  - **Amit – the son, far away.** Works in another city and worries. **Pain:** can only ask on the phone. **Needs:** a short daily update, and only if his father agrees to share it. *2 in 3 older Indians live with their children; 3 in 4 older women can't read* – LASI Wave 1
- **Thin strip:** Also served: **Dr. Meera Nair** (writes the plan and the prescription) and **the chemist** (checks the prescription with a QR).
- **Yellow placeholder strip:** **Interview findings:** [ADD: 3 interviewees – role, city] · [ADD: one short quote, used with permission]
- **Source line:** The personas are illustrative, not real people. They are based on published research and appear as sample patients on the site.
- **Screenshot (optional):** `03_landing_who_it_helps.png` as a small inset.
- **Notes (script 0:45–1:10):** Who is affected? Older patients after heart, abdominal and chest surgery. India records about forty-nine lakh major operations a year, and that is an undercount. Ward nurses, who teach it once and can't watch every patient every hour. And families. Two in three older Indians live with their children, but three in four older women can't read. We spoke to [ADD: number and roles of interviewees]. One told us: "[ADD: best quote]".

### Slide 6 – Target Beneficiaries: User Journeys (extra) – ALL THE USE CASES
- **Headline:** One product, six people, six short journeys – and most of each journey already runs on the live site.
- **Body: six rows (or six small cards). Each row = who → 3 or 4 steps → status tags.**
  1. **Ravi, the patient:** taps Start → the voice coaches each breath in Hindi → the session saves itself → "I do not feel well" shows a fixed message: nurse / 112. **Live** · breaths **Simulated**
  2. **Ravi's medicines:** opens My medicines → sees every medicine in plain Hindi → shows the screen at the pharmacy counter. **Live**
  3. **Sister Anjali, the nurse:** opens her list → the most urgent patient is on top → a missed session starts the reminder ladder → she acknowledges the alert and calls. **Live** · messages and calls **Simulated**
  4. **Dr. Meera Nair, the doctor:** writes the prescription → sends it to the patient's phone → can change or stop it. **Live**
  5. **The chemist:** scans the QR on the patient's phone → sees the hospital's own copy, marked Current. **Live** · not tried with a real pharmacy
  6. **Amit, the family:** opts in, with Ravi's consent → sees today's ticks on a private page → sends a cheer. **Live** · daily WhatsApp update **Simulated**
- **Bottom strip (two more, smaller):** **The hospital admin** sets the hospital's own app name and logo – **Live**. **The clip-on unit** is lent, taken back, cleaned and passed to the next patient – **Simulated** (device in development).
- **Second strip – special cases:** Admitted unconscious → "Phone number pending" until the patient is awake and agrees. Code not arriving → a one-time desk code from staff. No smartphone → the hospital side still works; calls and WhatsApp to a basic phone. (Login design: **In development**.)
- **Source line:** Sample patients. Status words are the ones shown on the live site.
- **Screenshots:** none needed (text slide). If there is room, three tiny phone crops: `21_phone_breathing_coach_breath3.png`, `25_phone_pharmacy_screen_qr.png`, `27_phone_family_page.png`.
- **Notes (extra):** Every person in the story has a short journey, and the notes for the reader are in the brief's use-case list. The patient breathes with a voice coach, sees his medicines and shows his phone at the pharmacy. The nurse sees who needs a call. The doctor writes, changes and stops the prescription. The chemist checks it with a QR. The family follows along, with consent. What is simulated today is the breath itself and the sending of messages and calls.

### Slide 7 – Solution Overview
- **Headline:** Pillar 1: proof that the breathing exercise was really done.
- **Four steps, left to right, each with a picture, a caption and a tag:**
  1. **Clip-on unit** – `18_showroom_3d_device.png` (cropped to the device). "A small base under an ordinary breathing exerciser reads how high the disc rises." Tag: **3D design model · device in development**
  2. **Voice coach** – `21_phone_breathing_coach_breath3.png`. "Coaches every breath in the patient's language: slower, hold, well done." Tag: **Live · breaths Simulated**
  3. **Nurse list** – `06_nurse_dashboard.png` (cropped to the triage list). "Shows who is falling behind. Fixed rules, not AI, pick who needs a call." Tag: **Live · sample patients**
  4. **Family update** – `27_phone_family_page.png`. "A family member who opted in, with the patient's consent, sees today's progress." Tag: **Live page · WhatsApp Simulated**
- **Bottom band:** **Problem:** nobody sees → **Solution:** measure, coach, show → **Outcome we measure:** sessions done ÷ sessions due
- **Source line:** Pictures 2–4: real screenshots, sample patient. Picture 1: 3D design model – device in development.
- **Notes (script 1:10–1:35):** SpiroBuddy is the adherence and coaching layer for breathing exercise. The ordinary exerciser stands on a small base. A sensor reads how high the disc rises. A voice coaches each breath in the patient's own language: slower, hold, well done. The nurse sees who is falling behind. And a family member who opted in, with the patient's consent, gets one short update a day.

### Slide 8 – Solution Overview: The Prescription (extra)
- **Headline:** Pillar 2: the doctor's prescription goes straight to the patient's phone. No paper to lose.
- **Four pictures, left to right, with captions:**
  1. **The doctor types the prescription** – `08_doctor_prescribe.png` (crop to the "Current medicines" and "Write a prescription" cards)
  2. **The patient sees it, in Hindi** – `24_phone_medicines_hindi.png`
  3. **Shown at the pharmacy counter** – `25_phone_pharmacy_screen_qr.png`
  4. **The chemist scans the QR and checks** – `26_phone_chemist_qr_check.png`
- **Right-hand bullets:** The doctor writes it. No AI reads a photo. · Saved under the patient's hospital registration number. · The QR opens the hospital's own copy, marked Current. · A tap on "I took it" is shown as reported, never as taken. · Only the doctor can change or stop a medicine.
- **Tags:** **Live** · small amber line: "Sample patient. Not yet tried with a real pharmacy."
- **Source line:** Real screenshots from the site, 12 Oct 2026. Sample patient, sample hospital and doctor.
- **Notes (extra):** The doctor types the prescription in the hospital software. The patient sees every medicine on their own phone, in their own language, and shows that screen at the pharmacy counter. The chemist scans the QR and sees the hospital's own copy, marked current. It is not AI reading a prescription photo. Sample data; not yet tried with a real pharmacy.

### Slide 9 – Solution Overview: The Whole Product, by Role (extra) – THE MAP OF PAGES
- **Headline:** It is already a whole product: 18 pages for six kinds of user, and one honest label on each.
- **Body: a map with four columns (one colour band per column), each a short list of pages with a tag.**
  - **Patient and family (phone)**
    - Breathing coach app – **Live** · breaths **Simulated**
    - My medicines (4 languages) – **Live**
    - Pharmacy screen with QR – **Live**
    - "I do not feel well" – **Live**
    - Family page – **Live**
    - Patient login (number + one-time code) – **In development**
  - **Nurse and doctor (hospital)**
    - Staff login – **Live**
    - Nurse dashboard and triage list – **Live**
    - The nurse's patient page – **Live**
    - Doctor's prescribing page – **Live**
    - Alerts inbox – **Live**
    - Units: lend, take back, clean – **Simulated**
  - **Hospital admin and our team**
    - App branding (own name and logo) – **Live**
    - Two hospitals kept apart – **Live**
    - Simulators: WhatsApp, calls, reminder ladder – **Simulated**
    - Breath recorder (to train the model) – internal tool
  - **Chemist and public**
    - QR prescription check (no login) – **Live**
    - Story site, Impact, Trust, Vision, Architecture – **Live**
    - 3D showroom of the device – 3D design model
- **Bottom line:** Every label comes from one status list in the code, shown on the site itself. The clip-on device is in development; breaths are simulated; patients are sample patients.
- **Screenshots (small, as a strip under the map if there is room):** `06_nurse_dashboard.png`, `08_doctor_prescribe.png`, `13_admin_app_branding.png`, `20_phone_breathing_coach_idle.png`.
- **Notes (extra):** This is the whole product on one page. The patient and the family use a phone. The nurse and the doctor use the hospital pages. The hospital admin sets the hospital's own name and logo. The chemist needs no login. Every page carries the same four honest labels as the live site.

### Slide 10 – Innovation & Differentiation
- **Headline:** Trackers and hospital apps already exist. Our difference: any hospital, built for the elderly, in the patient's language.
- **Table (replaces the template's "Existing Solution / Your Solution"):**

  | Existing alternative | What it does today | What SpiroBuddy adds |
  |---|---|---|
  | Paper tally sheet, or a phone call from the ward | Counts sessions, if someone fills it in | Counts sessions automatically and records how each breath is done: speed, depth, hold |
  | Smart spirometer trackers (InSee, USA) | Reads the piston with an infrared sensor. Fits one US spirometer; cleared for hospital use only | Home use, voice coaching in Indian languages, a nurse list and a family update |
  | Hospital-chain apps and ABHA health-locker apps | Serve one chain's own patients, or store health records | Any hospital or clinic, built for the elderly, in the patient's language, shown at the pharmacy counter |

- **Two cards below:**
  - **What is new:** Not the sensor: InSee showed that tracking the disc works. New is the whole chain for Indian homes: measure, coach by voice, show the nurse and the family, and carry the doctor's prescription on the same phone – with each hospital's own name on it.
  - **Why the weak evidence is our opening:** Reviews found little benefit from the exerciser alone, but the trials almost never recorded actual use. That is exactly the number we measure.
- **Small line:** Nothing stops a drug company or a phone app from trying. Our edge is elders without smartphones, 10 Indian languages, the nurse workflow and the family link.
- **Source line:** InSee: US FDA clearance K241152, 21 Aug 2025; IEEE Spectrum 2020 · Evidence: Cochrane 2014; 2024 cardiac-surgery review. We do not claim that nothing similar exists.
- **Notes (script, part of 2:55–3:25):** InSee in the US already reads the disc with a sensor, in hospitals. We take the idea home, in Indian languages. Hospital-chain apps and ABHA health-locker apps exist too; our line is: any hospital or clinic, built for the elderly, in the patient's language, shown at the pharmacy counter.

### Slide 11 – Technology Architecture
- **Headline:** Simple parts that run today. Three small AI helpers; the safety rules are fixed rules, not AI.
- **Flow row (six boxes with arrows, following the template's flow):** Patient + unit (unit in development; breaths simulated) → Patient web app (phone, big text, voice) → API server (Python, FastAPI) → AI layer (three small helpers) → Database (Postgres; hospitals kept apart) → Dashboards (nurse, doctor, family)
- **Four cards:**
  - **AI 1 · Breath model:** Labels each breath: good, too fast, too shallow, no hold. Trained on simulated breaths; simple rules run as a backup.
  - **AI 2 · Voice:** Speaks 10 Indian languages and English. Recorded clips and the browser voice still work when the internet is down.
  - **AI 3 · Daily summary:** A language model writes three plain sentences from the day's numbers. A fixed template is the fallback. It never diagnoses.
  - **Not AI, on purpose:** Red-flag words trigger a fixed message: contact your nurse / call 112. Alerts, triage and reminders follow fixed rules.
- **Two lines:** **Stack:** web pages in plain HTML, CSS and JavaScript, so nothing to install · Python FastAPI server · Postgres database · hosted in the cloud. **Security and privacy:** staff logins with hashed passwords · every record carries its hospital · an audit log of every write · limits on login tries, AI calls and uploads.
- **Screenshot:** `17b_architecture_diagram.png` as a right-hand or lower inset, caption "The live site's own diagram: every box is coloured by its status."
- **Source line:** Flow follows the template: user → application → APIs → AI layer → database → dashboard. Every AI or internet feature has an offline fallback.
- **Notes (script 2:55–3:25):** Where is the AI? Three places. A small model labels each breath: good, too fast, too shallow, no hold. It is trained on simulated breaths, so its accuracy on real patients isn't measured yet, and simple rules run as a backup. A voice service speaks ten Indian languages and English, with recorded clips for offline use. A language model writes a short daily summary. It never diagnoses. Alerts come from fixed rules, on purpose.

### Slide 12 – Technology Architecture: Responsible Technology (extra)
- **Headline:** Responsible by design: the software coaches and records. It never gives medical advice.
- **Six cards (3 x 2):**
  - **The AI never diagnoses.** It coaches and summarises only. No dose advice and no drug-interaction checks, on purpose.
  - **Red flags reach a person.** A fixed word list triggers a fixed message, "contact your nurse / call 112", and a nurse alert. No AI is involved.
  - **Consent and STOP.** Family updates only if the patient consents and the family member opts in. STOP ends them. Itemised consent screen: In development.
  - **Hospitals kept apart.** Every record carries its hospital, checked on each request and covered by tests. An audit log records who did what.
  - **Sample patients only.** The site holds no real health data and collects no government ID. No outside body has reviewed the product.
  - **No money in the apps.** Nothing about payments, bills or insurance in the hospital, nurse or patient apps.
- **Bottom band:** **Accessible:** large text, one action per screen, voice in the patient's language, no typing. **Law:** we expect Class B under India's Medical Devices Rules and will confirm with CDSCO before any patient; designed for India's DPDP Act 2023; we claim nothing until it is checked. **WhatsApp:** progress updates only, with opt-in, consent and approved templates.
- **Screenshot (optional):** `22_phone_i_do_not_feel_well.png` beside the "Red flags" card; or `15b_trust_what_we_do_not_claim.png` as an inset.
- **Notes (extra):** The AI never diagnoses; it coaches and summarises. Red-flag words trigger a fixed "contact your nurse or call 112" message from word lists, not AI. Alerts follow fixed rules. Sample patients only today. Consent from the patient, in their language; the family member opts in; one word, STOP, ends messages. Nothing to do with payments in the hospital, nurse or patient apps.

### Slide 13 – MVP / Prototype Screens
- **Headline:** It runs today, end to end, at spirobuddy.onrender.com – the patient's side, on a phone.
- **Five phone screenshots in a row, each with a one-line caption:**
  1. `20_phone_breathing_coach_idle.png` – **Home:** the hospital's own name on top, one big Start button
  2. `21_phone_breathing_coach_breath3.png` – **A coached breath** (breath Simulated)
  3. `24_phone_medicines_hindi.png` – **My medicines,** in Hindi
  4. `25_phone_pharmacy_screen_qr.png` – **The pharmacy screen** with its QR
  5. `22_phone_i_do_not_feel_well.png` – **Safety button:** a fixed message, no AI
- **Line under them:** **Try the flow:** scan the QR on the last slide → Start → make a sample breath → My medicines → Show at the medicine shop.
- **Tags:** **Live: patient app, voice, medicines, pharmacy screen, safety button** · **Simulated: breaths** · **In development: the clip-on device, login with a one-time code**
- **Source line:** Real screenshots, 12 Oct 2026, from a local copy of the site. Sample patient. The free server can take a moment to wake.
- **Notes (script 1:35–2:15):** Let me show you the live site. We have no hardware yet, so breaths come from a simulator. I start a session. Listen: the coach speaks Hindi. Too fast: it says "slower" at once, and the screen turns amber. The session saves itself. Nothing to type. One safety button. It shows a fixed message: contact your nurse, or call one-one-two. That part uses no AI.

### Slide 14 – MVP / Prototype Screens: The Hospital Side (extra) – THE NURSE AND DOCTOR PAGES
- **Headline:** The hospital side is live too: the nurse sees who needs a call, the doctor writes the prescription, the admin sets the hospital's own name.
- **Large picture, left (about half the slide):** `06_nurse_dashboard.png` – caption **Nurse dashboard:** four numbers on top, then the triage list, most urgent first. Outline the "Sessions today" tile and the top row of the list. Small note: "0 / 0 sessions: the picture was taken at night, before the day's first session."
- **Three smaller pictures, right (stacked or 2 + 1):**
  - `07_nurse_patient_page.png` – **The nurse's page for one patient:** sessions hour by hour, best breath over 7 days, breath quality, a three-sentence summary, call and alert actions
  - `08_doctor_prescribe.png` – **The doctor's page:** write, change or stop a prescription
  - `13_admin_app_branding.png` – **The admin's page:** the hospital's own app name and logo, with a live phone preview
- **Thin strip under them (two small pictures):** `11_simulators_whatsapp_calls.png` – **Reminder ladder, WhatsApp and calls** (Simulated: previews, nothing is sent) · `09_units_handover.png` – **Units:** lend, take back, clean (Simulated; device in development)
- **Tags:** **Live: staff logins, dashboard, patient page, prescribing, app branding** · **Simulated: breath numbers, WhatsApp, calls, units**
- **Source line:** Real screenshots, 12 Oct 2026. Sample patients at the sample hospital "Dawnlight General Hospital".
- **Notes (script 2:15–2:55):** Now the nurse's screen. Ravi is on her list. Every row shows sessions done out of sessions due today. If Ravi misses two sessions, a ladder starts: a reminder, a family message, a nurse alert, then the nurse calls. These sends are previews, not real messages yet. The doctor's page is where the prescription is written, changed or stopped. And the hospital admin sets the hospital's own name and logo for the patient app.

### Slide 15 – MVP / Prototype Screens: Honest Status (extra)
- **Headline:** Honest status: the software works, the device is in development, and no patient has used it.
- **Three columns:**
  - **Live today:** Public site and staff logins; hospitals kept apart · Nurse triage list and alerts, by fixed rules · Patient app with a voice coach in 10 Indian languages and English · The doctor's prescription on the patient's phone, pharmacy screen and QR check · Each hospital's own name and logo in the patient app · 400+ automated tests
  - **Simulated:** Breaths: from a built-in simulator · Breath model: 95.8% on simulated breaths; real-patient accuracy is not measured · WhatsApp updates, phone calls and the reminder ladder: previews, nothing is sent · Every patient, staff member and hospital on the site is a sample one
  - **In development / to come:** The clip-on unit: a design and a 3D model · Real breaths from real people · Patient login with registration number + a one-time code · Medicine reminders · Any patient, any pilot, any result · Any review by a regulator or outside body · A test with a real pharmacy
- **Bottom band:** **Readiness: TRL 3–4.** Software about TRL 4: it runs end to end on a live site with simulated breaths. Device TRL 3: a design and a 3D model.
- **Source line:** Every status label on the site comes from one list in the code: Live / Simulated / In development / Planned.
- **Notes (script 4:20–4:30):** Honestly: about TRL three to four. The software works end to end, live. The sensor unit is not built, and nothing is tested on patients.

### Slide 16 – Market Validation
- **Headline:** What we know so far comes from published studies. No pilot, no survey and no users yet.
- **Left table (replaces the template's):**

  | Validation activity | Result so far |
  |---|---|
  | Interviews | [ADD: 3 interviewees – role, city] |
  | Survey responses | None yet |
  | Pilot users | None yet. No patient has used SpiroBuddy |
  | Waitlist | None |
  | Desk research | Evidence, law and costs mapped before building. Every number here carries its source or the word estimate |

- **Yellow placeholder under it:** [ADD: one short interview finding or quote, used with permission]
- **Right – "What published research already tells us" (three numbers):**
  - **28% → 58%** of waking hours with exercise, when patients got an hourly reminder – US randomised trial, 145 patients, JAMA Surgery 2019
  - **6% → 72%** did the exercise properly: day 1, then day 3 after teaching – Chennai hospital, 60 patients, J Pharm Bioallied Sci 2024
  - **246 of 260** TB survivors completed 12 weeks of home lung rehab with phone follow-up – 5 Indian centres, no comparison group, Indian J Med Res 2025
- **Source line:** Next step: interviews with hospital teams on who pays (the price is not yet tested with a hospital), then the 30-patient ward pilot.
- **Notes (extra):** We mapped evidence, law and costs before building. We measure what the trials almost never recorded: actual use. We have no pilot, no survey and no users yet. [ADD: the interviews, once done: say "we interviewed N people", never more than that.]

### Slide 17 – Scalability
- **Headline:** One shared platform, each hospital kept apart. Growth is staged; every stage after today is Planned.
- **Stage arrows (five chevrons):** Today (live site, sample patients) → 1 pilot hospital (Planned) → 10 hospitals (Planned) → 100 hospitals (Planned) → State programmes (Planned). Under the row: City → State → Country.
- **Four number boxes:** **₹2,500** parts per unit – estimate · **about 10** loans per unit – assumption · **about ₹1,000** per patient episode – planned price, estimate · **₹0.12** per WhatsApp update – Meta India rate card
- **Three lines:**
  - **Digital scale:** a hospital's doctors, departments and patients can be moved in from a spreadsheet, with a practice run before anything is saved (Planned). SpiroBuddy sits beside the hospital's own software.
  - **Automation:** reminders, the escalation ladder and the daily summary run by themselves (message sends are Simulated today).
  - **Partners and the next group:** hospital nurse and physio teams first; later TB survivors (Planned). India's draft 2024 TB rehab guidance lists the incentive spirometer for supervised sessions.
- **Screenshot (small inset):** `09_units_handover.png`, caption "One unit, many patients – preview, device in development".
- **Source line:** Costs are team estimates; none is measured. WhatsApp: Meta India utility rate. TB: RBIPMT 2024 draft guidance (ntep.in).
- **Notes (script, part of 3:55–4:20):** Today one web service and one database run this site, with sample patients. Planned growth is staged: one pilot hospital, ten, a hundred, then state programmes. Each patient episode should cost five to seven hundred rupees, an estimate; our planned price is about one thousand. Next, TB survivors: India's draft TB rehab guidance lists this exerciser.

### Slide 18 – Scalability: The Growth Path (extra) – THE BIG PICTURE
- **Headline:** The spirometer is module 1. The plan is a whole-hospital companion: Arogya Sathi (working name), with the SpiroBuddy breathing coach.
- **Left (two-thirds): five account rows, each = name · what it does · tag**
  - **Hospital** – whole-hospital view: check-ins, check-outs, beds; its own app name and logo – **Live: admin login, app branding** · view **Planned**
  - **Department** – registers patients; bed board, appointments, nurse roster – **Planned**
  - **Doctor** – today's patients, records, prescriptions – **Live: prescriptions** · "My day" page **Planned**
  - **Nurse** – duty, rooms, tasks and alerts – **Live: triage list, alerts** · phone app **Planned**
  - **Patient** – prescriptions, pharmacy screen, breathing coach – **Live / Simulated** · reminders **In development**
- **Right (one-third): three stacked cards = the three ways it grows**
  - **More device modules.** Module 1: the spirometer clip-on (In development). Next, on the same screens: pulse oximeter, blood-pressure cuff, peak-flow meter, a three-ball reader, a speaking base for homes with no smartphone (Planned).
  - **More of the hospital.** From one ward to departments, bed board and the whole hospital; a hospital moves in from a spreadsheet (Planned).
  - **More patient groups.** After surgery today; before surgery, TB survivors and long-term lung conditions later (Planned).
- **Small note at the bottom:** "Arogya Sathi" is a working name for the planned whole-hospital app. This entry and the live site stay named SpiroBuddy.
- **Screenshot (optional small inset):** `16b_vision_roadmap.png`, caption "The roadmap on the live site".
- **Source line:** A roadmap, not a claim: everything here beyond what the site marks Live or Simulated is Planned.
- **Notes (extra):** The spirometer is where we start, not where we stop. The same platform already carries the doctor's prescription to the patient's phone. The plan is one companion app for the whole hospital: hospital, department, doctor, nurse and patient accounts, with the spirometer as device module one and more devices plugging into the same screens later. Arogya Sathi is a working name.

### Slide 19 – Business & Sustainability Model
- **Headline:** The hospital pays: under flat-rate insurance, every extra bed-day comes out of its own pocket.
- **Table (replaces "Business Model Canvas Snapshot"):**

  | Revenue (planned) | Costs (estimates) |
  |---|---|
  | About ₹1,000 per patient episode; the unit is lent at discharge and reused | About ₹2,500 of parts per unit, reused across about 10 patients (assumption) |
  | Later: a subscription per hospital, with add-on modules such as the spirometer (Planned) | ₹0.12 per WhatsApp update; phone calls only to escalate |
  | Patients and families never pay. No money is handled inside the hospital, nurse or patient apps | About ₹500–700 to serve one patient episode. Hosting is free for the demo only |

- **Two number boxes, right:** **₹2,307** average cost of one ward bed-day; our ₹1,000 is less than half – 57 hospitals, 11 states, BMJ Open 2023 · **₹1,62,400** flat Ayushman Bharat payment for a bypass, 10-day stay built in – HBP 2022 rate list
- **Bottom card:** **Sustainability plan:** a grant funds the pilot (one NIDHI-PRAYAS grant, up to ₹10 lakh, could cover it) → a paid pilot with one hospital → a per-episode fee, later a subscription. **Honest gap:** the price is not yet tested with any hospital. How the fee fits inside a PM-JAY package is a question for our hospital interviews.
- **Source line:** All prices and costs are team estimates; none is measured. Sources: HBP 2022 rate list (state copy) · CHSI, BMJ Open 2023 · Meta India rate card.
- **Notes (script 3:55–4:20):** Who pays? The hospital. Under Ayushman Bharat, a bypass is paid at a fixed rate, so every extra bed-day comes out of the hospital's pocket. A ward day costs about twenty-three hundred rupees. Our unit costs about twenty-five hundred rupees, is lent at discharge and reused. We plan to charge about one thousand rupees per patient episode, less than half a ward day.

### Slide 20 – Business & Sustainability Model: A Custom Build for Every Hospital (extra)
- **Headline:** Every hospital gets its own build: its own name on the app, its own set of modules, and our own clip-on device.
- **Three columns, each with a picture, three short lines and tags:**
  - **(a) Its own app.** The hospital's own name and logo at the top of the patient app, set on an "App branding" page; we set it up during onboarding. Safety messages stay fixed. Picture: `13_admin_app_branding.png` (crop to the phone preview "Dawnlight Care – with SpiroBuddy"). Tags: **Live: name and logo inside the app** · **Planned: own home-screen icon, store apps**
  - **(b) Its own modules.** One shared platform, each hospital kept apart. A core for every hospital, and add-on modules switched on per hospital: the spirometer today, more devices later. Picture: a simple diagram – a "Core" block (accounts + prescriptions) with add-on blocks "Spirometer", "Pulse oximeter", "BP cuff", "Peak-flow meter" (the last three drawn with a dashed outline). Tags: **Live: hospitals kept apart** · **Planned: module switches, our company console**
  - **(c) Our own device.** A clip-on base we designed for the ordinary breathing exerciser: lent at discharge, cleaned and reused. Picture: `18_showroom_3d_device.png` (crop to the device). Tags: **In development: design + 3D model; not built**
- **Bottom band – why it is good business:** Land with one module, grow with more. A hospital can move in from a spreadsheet within minutes (Planned), keeps its own software, and can export everything at any time. Hospitals pay us through our own company console only; no money appears in the hospital, nurse or patient apps.
- **Visible line for the founder (yellow, to delete):** [FOUNDER: I wrote 'custom build' as (a) + (b) + (c). Delete what you did not mean.]
- **Source line:** The home-screen name and icon of a store app cannot change after install; a web-app install from the hospital's own address can carry the hospital's name (Planned).
- **Notes (extra):** Custom build is part of the plan and of the business. Each hospital sees its own name and logo in the patient app: that works today. Each hospital would switch on the modules it wants: that is planned. And the device itself is our own design: a 3D model today, the first unit is the next step.

### Slide 21 – Risks & Mitigation
- **Headline:** Our biggest risks are an unbuilt device and unproven adoption. Each one has a named next step.
- **Table:**

  | Type | Risk | Impact | Mitigation |
  |---|---|---|---|
  | Operational | The clip-on unit is not built. The sensor chip is ±2 cm out of the box (ST datasheet) | No real breaths can be recorded | Bench-test one unit and calibrate it to each exerciser's printed marks. The coach also runs from a simulator or a manual tap |
  | Adoption | Older patients without smartphones; busy nurses; a chemist may not accept a phone screen | Low use at home; no trust at the counter | Voice, big buttons and the family's phone. Alerts only when a call is needed. The QR opens the hospital's own copy; pharmacy acceptance is still to be tested |
  | Technology | The breath model has seen only simulated breaths. The internet or an AI service may be down. Our sensor reads the volume type, not three-ball exercisers | Wrong labels; a silent app; fewer patients covered | Record real breaths and re-train before any pilot. Rules run as a backup; every AI feature has an offline fallback. A three-ball reader is Planned |
  | Regulatory | A device that measures and alerts: we expect Class B under India's Medical Devices Rules. The DPDP Act applies | No patient study without the right permissions | CDSCO's written view and a registered ethics committee before enrolling anyone. We claim only practice and recording |

- **Notes (extra):** We expect Class B under India's device rules, and will confirm with CDSCO before any patient study. The breath model is trained on simulated breaths; recording real breaths comes before any pilot.

### Slide 22 – Implementation Roadmap
- **Headline:** Next: build one unit, record real breaths, get the regulator's written view, then run a 30-patient pilot.
- **A timeline with three blocks (90 / 180 / 365 days):**
  - **90 days – Build and measure:** Bench-test one clip-on unit · Record real breaths and re-train the breath model · Patient login with registration number + one-time code; medicine reminders · A home-screen icon with each hospital's own name
  - **180 days – Permissions and pilot:** A registered ethics committee and CDSCO's written view, before any patient · Start a 30-patient, 3-month pilot at one hospital (about ₹5.5 lakh, middle estimate) · Department page with a bed board; the doctor's "My day" page
  - **365 days – Report and widen:** Report the pilot's number, whatever it is · Store apps, once a pilot hospital agrees · A reader for three-ball exercisers; a second device module; rehab for TB survivors
- **Line under it:** A plan, not a promise: everything on this slide is Planned or In development.
- **[FOUNDER: you confirmed the 90 / 180 / 365-day split. Change the items here if your plan has moved.]**
- **Notes (script 4:30–4:40):** Next: build one unit, record real breaths, then a thirty-patient pilot, with an ethics committee and the regulator's written view before that. We expect Class B under India's device rules.

### Slide 23 – Team Structure
- **Headline:** Team GuGu GaGa: a small team where each person owns one part and can explain it.
- **Four cards (photo circle, name, role, "Owns:"):**
  - [ADD: founder name] · Lead · pitch · video · **Owns:** problem, users, money
  - [ADD: name] · [ADD: role] · **Owns:** sensor and the unit design
  - [ADD: name] · [ADD: role] · **Owns:** breath detection and the model (trained on simulated breaths)
  - [ADD: name] · [ADD: role] · **Owns:** alerts, WhatsApp, consent, safety words
- **Two yellow boxes:** [ADD: college or organisation, city, state] · **Advisors / mentors:** [ADD: names and roles, or "none yet – mentoring is part of our ask"]
- **[FOUNDER: change the number of cards to match your real team. Do not leave a card you cannot fill.]**
- **Notes (script 4:40–4:50):** We are [ADD: names, one role each]. Each of us owns one part and can explain it in sixty seconds.

### Slide 24 – Financial Requirements
- **Headline:** Our near-term need is one pilot: about ₹5.5 lakh (middle estimate).
- **Table (replaces "Category / Amount"):**

  | Category | Amount | What it covers |
  |---|---|---|
  | Product development | About ₹2,500 of parts per unit (estimate) | Building and bench-testing the clip-on unit. A hand-built cable prototype is about ₹1,365 |
  | Marketing | None planned | We need introductions to hospital teams, not advertising |
  | Operations | About ₹5.5 lakh (middle estimate) | A 30-patient, 3-month pilot at one hospital. Hosting is free for the demo only |
  | Funding requirement | About ₹5.5 lakh for the pilot | One NIDHI-PRAYAS grant (up to ₹10 lakh) could fund it |

- **Band:** **Read this as estimates:** these are our own figures from shop prices and published rate cards, not quotes from a supplier or a hospital.
- **Source line:** All amounts are team estimates. The NIDHI-PRAYAS figure is the grant's upper limit, not money we hold.
- **Notes (extra):** Bench-test one unit, record real breaths, then a 30-patient pilot. Units are lent and reused, so hospitals buy no hardware. One NIDHI-PRAYAS grant could fund the pilot.

### Slide 25 – Ask & Next Steps
- **Headline:** Our ask: one hospital team to pilot with, and guidance on the regulatory steps.
- **Three ask rows:**
  - **Pilot partner** – an introduction to one hospital's nurse or physiotherapy team
  - **Mentorship** – the CDSCO steps for a device that measures, and help with a NIDHI-PRAYAS application
  - **Funding** – about ₹5.5 lakh for a 30-patient, 3-month pilot (middle estimate)
- **Closing statement (replaces the template's sample quote):** After surgery, the hospital stays connected to the patient at home. SpiroBuddy. Every breath, coached and counted.
- **Yellow box:** **Queries & feedback:** [ADD: leader's name, email, phone]
- **Right panel (the template's QR area):** "Scan for the demo" · picture `00_qr_live_demo.png` in the template's QR box · link text **spirobuddy.onrender.com** · small grey text: "Opens the patient app. Sample patient, simulated breaths. The free server can take a moment to wake."
- **Notes (script 4:50–5:00):** Our ask: an introduction to one hospital's nurse or physio team for that pilot, and guidance on the regulatory steps. SpiroBuddy. Every breath, coached and counted. Thank you.

**If the founder wants a shorter deck:** slides 4, 6, 9 and 12 can be dropped without breaking the story. Keep 8, 14, 15, 18 and 20: they answer the points the first deck missed.

---

## J. The placeholders only the founder can fill

Team name is **GuGu GaGa** (already filled). Everything else below is not written anywhere and must **not** be invented.

| Slide | Placeholder | What to put |
|---|---|---|
| 1 | Product logo | `00_product_logo.png` is supplied; swap it if you have a newer logo |
| 1 notes | [ADD: name] | The presenter's name |
| 5 | [ADD: 3 interviewees – role, city] · [ADD: one short quote, used with permission] | Only real interviews. If none were done, delete the strip and write "Interviews: planned" |
| 5 notes | [ADD: number and roles of interviewees] · [ADD: best quote] | The same |
| 16 | [ADD: 3 interviewees – role, city] · [ADD: one short interview finding or quote] | The same. Say "we interviewed N people", never "validated" |
| 20 | [FOUNDER: custom build (a) + (b) + (c)] | Delete the readings you did not mean, then delete the line |
| 22 | [FOUNDER: 90 / 180 / 365-day items] | Confirm or change, then delete the line |
| 23 | [ADD: founder name] · [ADD: name] x3 · [ADD: role] x3 · [ADD: photo] x4 · [ADD: college or organisation, city, state] · [ADD: advisors or "none yet"] | Real team details |
| 25 | [ADD: leader's name, email, phone] | The contact the organisers should use |
| Whole deck | Footer | [FOUNDER: if an organiser tells you to keep the template's own footer, say so and ChatGPT changes this one line] |
| Whole deck | Login status | [FOUNDER: check /api/features on the live site before submitting; if the OTP login is there, say Simulated] |

---

## K. Optional – a prompt for ChatGPT's image tool to draw a product logo

The site already has a mark: **a teal rounded square with a white pill shape and two white arcs** (like a breath). It is supplied as `00_product_logo.png`. **Keeping it is fine**, and it matches the live site the judges will open. Use the prompt below only if you want a new one.

```text
Design a simple flat logo mark for "SpiroBuddy", a breathing-exercise coach for patients
recovering at home after surgery.
- One flat mark, no gradients, no shadows, no 3D.
- Colour: teal #0b6e8a on a transparent background (also give a white-on-teal version).
- Idea: a single breath, or the rising float (piston) inside a breathing exerciser. Soft, calm, round shapes.
- It must stay readable at 32 x 32 pixels: at most three shapes, thick lines.
- No medical cross, no heart, no lungs drawn in detail, no stethoscope.
- No text other than the name "SpiroBuddy" (give one version with the name to the right, one mark alone).
- Square canvas, 1024 x 1024, PNG with a transparent background.
```

---

## L. The screenshot pack (`deck_shots.zip`)

All pictures were taken on Mon 12 Oct 2026 from a local copy of the site (the same code as the live site), light theme, with sample patients at the sample hospital "Dawnlight General Hospital". Desktop pages are 1280 px wide; phone pages are 390 px wide. Files ending in `_full` or with a `b` are the whole page from top to bottom, for cropping.

**Notes before using them**
- The nurse dashboard and the patient page show **"0 / 0" and "0 of 0 due"** for today's sessions, because the pictures were taken at night and sessions run 8 am–9 pm. This is correct behaviour, not an error. Say so in the caption, or crop to the triage list.
- Never show a `localhost` or `127.0.0.1` address. The supplied phone pictures have none.
- Do not redraw, recolour or edit the content of a screenshot. Cropping and a thin outline around the part that matters are fine.

| File | What it shows | Use on slide |
|---|---|---|
SCREENSHOT_TABLE_PLACEHOLDER
