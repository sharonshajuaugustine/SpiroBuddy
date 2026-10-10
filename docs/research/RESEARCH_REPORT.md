# SpiroBuddy – consolidated research report

**Written:** 10 Oct 2026. **What this is:** one document that pulls together all research already in this repo (research rounds 1–9, the plans, and the hardware, voice, comms and architecture notes). Nothing new was looked up for it and no web page was opened.

**Added later on 10 Oct 2026:** section 4.2a (how InSee is mounted). This one part *is* new: the InSee website, its US patent and the IEEE Spectrum interview were re-opened for it.

**How to read the references**
- `F-…` = a finding in `docs/research/KNOWLEDGE_BASE.md` (for example F-CLIN-1).
- `#n` = a row in `docs/research/SOURCES_LEDGER.md`. The full list with web addresses is in section 12.
- **Grades** (from the knowledge base): **A** = peer-reviewed study, guideline or regulator document · **B** = reputable organisation, major news or a company's official page · **C** = retailer, blog, forum, press release or a search snippet that was not opened.
- **"Team estimate"** = our own arithmetic, not a source. **"Not confirmed"** / **"unverified"** = the research could not confirm it. These labels are kept exactly as the research notes had them.
- Two findings share an ID in the knowledge base (F-VOICE-7 to 9 and F-COMP-7 were used twice). The second set is cited here as "(imported)".

**Privacy note:** this repo is public. Round 9 looked at the team's own WhatsApp product (WaBI) using private material. This report gives only the conclusions from that round.

---

## 1. Executive summary

**The problem.** After an operation, about 1 in 10 patients gets a lung problem such as pneumonia or a partly collapsed lung. Doctors call these *post-operative pulmonary complications*. To help prevent them, patients are given an *incentive spirometer*: a cheap plastic device with a disc that rises when you breathe in slowly and deeply. In practice patients forget the exercise or do it wrong, and nobody can see that, least of all once the patient is home.

**Who it affects in India.** India's public records alone show about 49 lakh major operations a year, and that is an undercount (F-INDIA-1). The typical patient is older. Most older Indian women can't read, over a third of older Indians have low vision, and most older people don't own a smartphone. But two in three live with their children, and nearly every home has a mobile phone (F-INDLOC-3, F-INDLOC-7, F-INDIA-5).

**What SpiroBuddy does.** A small base unit sits under an ordinary spirometer. A laser sensor measures how high the disc rises. Software judges each breath (good, too fast, too shallow, no hold) and a voice coach speaks in the patient's language. A nurse dashboard shows who is falling behind, and a family member gets a short WhatsApp update. It coaches and summarises. It does not diagnose.

**The strongest evidence-backed facts**

| # | Fact | Grade | Ref |
|---|---|---|---|
| 1 | About 1 in 10 surgical patients gets a lung complication: 10.4% of 9,864 patients in 146 hospitals, 29 countries. | A | F-CLIN-1, #35 |
| 2 | With a lung complication, 19.5% died within 30 days, against 0.5% without one (2,464 patients, Spain). This is a link, not proof of cause. | A | F-CLIN-2, #36 |
| 3 | In an Indian study (Udaipur), patients with lung complications stayed 21.7 days instead of 12.5, spent 8.5 days in ICU instead of 1.4, and 28% of them died. Small, single centre. | A | F-CLIN-8, #83 |
| 4 | An hourly reminder doubled the share of **waking hours** in which heart-bypass patients did the exercise: 58% vs 28% (randomised trial, 145 patients, USA). | A | F-ADH-1, #2 |
| 5 | 86% of 1,681 US nurses and respiratory therapists say patients don't use the spirometer as they should. Top reason: they forget (83.5%). | A | F-ADH-2, #48 |
| 6 | In Chennai only 6% of 60 patients did the exercise properly on day 1 after surgery. In Hyderabad 26 of 100 cancer-surgery patients couldn't do it correctly. Both small. | A | F-ADH-6 #157, F-ADH-4 #47 |
| 7 | Among Indians aged 60+, only 24% of women can read and write, 37% have low vision when tested, and about two in three live with their children. | A | F-INDLOC-3, #117 |
| 8 | The US regulator (FDA) cleared InSee, a clip-on spirometer tracker that also uses an infrared distance sensor, on 21 Aug 2025. It fits one US spirometer family and is for hospital use only. | A/B | F-COMP-1 #31 #3, F-COMP-5 #88 |
| 9 | Ayushman Bharat pays a hospital a flat ₹1,62,400 for a heart bypass with a 10-day stay built in. A ward bed-day costs about ₹2,307 and an ICU bed-day about ₹25,927. | A | F-BIZ-1 #128, F-BIZ-4 #141, F-BIZ-5 #142 |
| 10 | **Honest limit:** the evidence that incentive spirometry *on its own* prevents complications is weak (Cochrane 2014; a 2024 heart-surgery review). Those trials rarely recorded whether patients did the exercise. | A | F-CLIN-3 #39, F-CLIN-7 #81 |

**What we must not claim:** that SpiroBuddy prevents pneumonia, cuts readmissions, is the first of its kind, or that laser sensing is our invention. Section 10 has the full list with safe wording.

---

## 2. The clinical problem

### 2.1 Lung complications after surgery
- **How common, worldwide.** 10.4% of 9,864 patients; 7.0% in low-risk and 19.2% in higher-risk patients. Mostly European hospitals. (F-CLIN-1, #35, A)
- **How serious.** 30-day death rate 19.5% with a lung complication vs 0.5% without. Single source; shows a link only. (F-CLIN-2, #36, A)
- **India.**
  - Udaipur, emergency abdominal surgery: complication rate 2.9%; stay 21.7 vs 12.5 days; ICU 8.5 vs 1.4 days; 28% of those with a complication died. (F-CLIN-8, #83, A, small)
  - JIPMER Puducherry, 100 gut-surgery patients: 34% had a lung complication. Lower education was linked to more complications. (F-CLIN-8, #82, A, small)
  - CMC Vellore, 1,711 heart-surgery patients: a lung complication was an independent risk factor for going back to ICU; those patients stayed 17.6 vs 7.6 days. (F-BIZ-10, #169, A, single centre)
  - **From the earlier plans, not re-checked by the research rounds:** "about 3–30% depending on surgery and study", and an Apollo Chennai series of 330 patients (9.4% overall, about 14% after upper-abdominal surgery, over 55% after chest surgery). (Final Research §3; #10, #11 are marked "known, from plans" in the ledger.)
  - A Pune study seen in search results (29 of 150, 11 deaths) was **not confirmed. Don't use it.** (F-CLIN-8 caveat)
- **The two Indian rates disagree widely** (2.9% and 34%). They cover different surgeries and definitions. Quote each with its setting, not as "the Indian rate".

### 2.2 What incentive spirometry is
A hand-held plastic device. The patient breathes in slowly through a mouthpiece, a disc (or balls) rises, and they hold the breath for a few seconds. Two types matter here:
- **Volume type** (a piston or disc): the height shows how many millilitres were breathed in. This is what SpiroBuddy reads.
- **Flow type** (usually 3 balls): shows how fast the air moves, not how much. SpiroBuddy's sensor can't read it. (F-INDIA-4)

**Standard technique:** slow breath in, hold 3–5 seconds, about 10 breaths every 1–2 waking hours. MedlinePlus says 3–5 s; Cleveland Clinic says at least 5 s. (F-CLIN-5, #44, #45, B)

### 2.3 Evidence FOR
| Finding | Grade | Ref | Limits |
|---|---|---|---|
| 2024 review, 9 trials, 1,209 lung-cancer patients: spirometry **as part of a breathing-exercise bundle** cut complications and shortened stays. | A | F-CLIN-6, #80 | Its own effect can't be separated from the bundle; includes Chinese-language trials. No gain in walking distance or quality of life. |
| US guideline (AARC 2011) suggests a volume-type device, used with deep breathing, coughing, walking and pain control. | A | F-CLIN-4, #42 | The same guideline says not to rely on it alone. |
| Indian trial (Mangalore 2016, 50 patients): both device types were safe; the volume type gave better walking-test gains. | A | F-CLIN-9, #89 | Small, short, no complication outcomes. |
| Reminder trial (Eltorai 2019): 58% vs 28% of waking hours with use; 35 vs 17 breaths a day; X-ray lung-collapse score 1.5 vs 1.8 (P=.04). | A | F-ADH-1, #2 | Counts hours, not patients. One hospital. The X-ray effect is small. The author filed a patent on the reminder device. |
| Penn Airalux trial: 14.7 sessions a day; more use linked to shorter stays. | A/B | F-ADH-3, #5, #6, #34 | 30 patients, **no control group**. |

### 2.4 Evidence AGAINST (say this before judges ask)
| Finding | Grade | Ref |
|---|---|---|
| Cochrane 2014, 12 trials, 1,834 people, upper-abdominal surgery: **no proof** it prevents complications (risk ratio 0.59, range 0.30–1.18). Evidence quality low. Adherence was never recorded. | A | F-CLIN-3, #39 |
| 2024 heart-surgery review, 22 trials, 1,677 people: **not better** than standard breathing care; worse on blood oxygen. Authors say it shouldn't be widely recommended until better trials exist. The comparison was against other active breathing care, not against nothing. | A | F-CLIN-7, #81 |
| AARC 2011: don't use it alone. | A | F-CLIN-4, #42 |
| Korea's Go-breath (hourly alarm + nurse dashboard, 42 patients): no significant benefit (P=.22). Use was self-reported, with no sensor. | A | F-ADH-5, #52 |
| Thailand 2025 trial, 32 patients: a digital spirometer vs a 3-ball device after open-heart surgery showed no difference in lung function. | A | F-TECH-2, #120 |
| InSee's FDA study proved measurement accuracy, **not** better patient outcomes. | A/B | F-COMP-7 (imported), #101–#103 |

**Our honest position:** on its own, the evidence is weak or mixed. As part of a nurse-led bundle, it helps. The trials mostly did not check whether patients actually did the exercise, and that is the gap SpiroBuddy fills. We never say it prevents pneumonia.

### 2.5 Adherence (do patients actually do it?)
- 86% of US nurses and therapists call adherence poor: patients forget (83.5%), use it ineffectively (74.4%) or not often enough (70.7%). (F-ADH-2, #48, A)
- Chennai: day 1 after surgery, 6% adequate, 40% moderate, 54% inadequate; 72% adequate by day 3 with teaching. In hospital, flow-type device. (F-ADH-6, #157, A, small)
- Hyderabad: 26 of 100 couldn't use it correctly; reasons were not understanding instructions, too little practice, limited family support. (F-ADH-4, #47, A)
- Family support helps: an Indian pilot trial (Tata Memorial unit, Bihar, 75 patients) that supported caregivers with a Hindi website and a WhatsApp group halved unplanned follow-up visits (1.23 vs 2.64). **Complications were unchanged.** (F-ADH-7, #158, A, pilot)
- Digital reminders alone help only modestly: 76 TB studies, odds ratio 1.14 for treatment success (very low certainty); apps did better (2.17, low certainty); side-effect reporting went up (1.57, moderate certainty). TB medicines, not breathing exercise. (F-ADH-8, #159, A)
- An Indian WhatsApp lung-rehab service (Respira) saw 18% of sign-ups finish, but about 30% of hospital referrals. Self-reported by the founders. (F-COMP-9, #133, C)
- **Gap:** no Indian data on spirometer use **after discharge** was found in three rounds. (F-ADH-6, F-ADH-9 caveats)

### 2.6 Readmission
- Worldwide, 12.9% of heart-bypass patients are back in hospital within 30 days (53 studies, 8.9 million patients). Lung problems cause 1–20% of those readmissions. Mostly Western data. (F-BIZ-8, #152, A)
- India, major abdominal cancer surgery: 4.7% within 30 days (30 centres, 810 patients). Causes not reported. (F-BIZ-10, #170, A)
- India, Whipple surgery (Lucknow, 997 patients): about 5.3% within 30 days; main cause was fluid in the abdomen, not the lungs. (F-BIZ-10, #168, A)
- India, knee replacement (Ludhiana, 609 patients): only 1.1% at 30 days. (F-BIZ-8, #153, A)
- **India, heart bypass: no published 30-day figure.** Three rounds of searching found none. (F-BIZ-12, #180, #181, #188, #189)
- An Indian trial protocol (Amrita, Kochi) puts bypass readmission at 10–20%, "particularly in LMICs". This is a statement in a protocol, not a measured Indian rate. (F-BIZ-8, #154)
- **Nothing shows SpiroBuddy reduces readmissions.** Say "we'd measure it in a pilot". (Claim check C25)

### 2.7 What a complication costs
- A ward bed-day costs an Indian hospital about ₹2,307 on average; a procedure about ₹10,686 (57 hospitals, 11 states). Provider cost, pre-2023 data. (F-BIZ-4, #141, A)
- An ICU bed-day at PGIMER Chandigarh: ₹25,927. A patient with ventilator pneumonia cost ₹5.44 lakh vs ₹2.07 lakh without. Trauma ICU; ventilator pneumonia is **not** the same as a post-surgery lung complication. (F-BIZ-5, #142, A)
- Older proxy: ventilator pneumonia in a north Indian ICU added about US$5,200 and doubled the stay (2015). Proxy only. (F-BIZ-2, #129, A)
- **Team estimate, label it as such:** about 7 extra ICU days (Udaipur) × ₹25,927 ≈ ₹1.8 lakh, "up to about ₹2 lakh". It joins two different studies. (F-BIZ-5)
- **No direct rupee cost of a post-surgery lung complication in India was found.** (Claim check C21)
- From the earlier plans, not re-checked: an Australia/New Zealand study (1,473 patients) put the extra cost at about A$29,000 and 9 extra days. (Final Research §3, #12, B)

### 2.8 After TB, and long-term lung disease (COPD)
- India notified about 26 lakh TB patients in 2024 and 90% are treated successfully. (F-VIS-4, #161, A)
- In Madurai, 59% of 132 adults finishing treatment still had impaired lungs, mostly the "stiff lung" type. A Haryana hospital study of 150 survivors found 48% stiff-lung and 34% mixed patterns. (F-VIS-4, #162, #163, A, single sites)
- About 74% of India's new and relapse TB cases in 2024 were in the lungs: about 18.5 lakh. Computed by the team from WHO's data columns; single source. (F-VIS-7, #187, A)
- **Team estimate:** about 16–17 lakh people a year finish treatment for lung TB; if roughly half have lasting damage, that is several lakh a year. Earlier rounds said 23 lakh, then "under 19 lakh" (F-VIS-4, F-VIS-6 #177; see section 11.4). Say "lakhs of people a year".
- India's TB programme asks that every patient finishing treatment be checked for lung damage, and lists home-based activity plans in rehab. (F-VIS-2, #146, A)
- India's 2024 RBIPMT guidance on TB lung rehab lists the incentive spirometer among its breathing exercises. It is a **draft**, for **supervised centre sessions**, with no dose given. (F-VIS-5, #176, A)
- Home rehab works in India: 246 of 260 TB survivors at 5 centres finished 12 weeks with phone follow-up; walking and quality of life improved. No comparison group. (F-VIS-1, #116, A)
- Rural COPD patients in the Thar Desert (45 people, mean age 64): 76% still exercising after 8 weeks of Hindi video rehab, 58% after a year. Self-reported, small. (F-ADH-9, #171, A)
- Pune survey: 87% of 370 chronic-lung patients wanted rehab; 84% liked a home web programme. Stated preference only. (F-VIS-3, #147, A)
- Among Indians aged 60+, 8.3% report a diagnosed chronic lung disease. (F-INDLOC-3, #117, A)

---

## 3. Users and context in India

### 3.1 Older patients (LASI = the Government's Longitudinal Ageing Study in India, 2017–18)
| Fact (age 60+) | Number | Ref |
|---|---|---|
| Can read and write | 39.6% overall; men 56.6%; **women 24.2%**; rural 30% | F-INDLOC-3, #117, A |
| Low vision when tested | 37.1% (55.3% report an eye problem) | F-INDLOC-3 |
| Hearing problems | 9.6% report them; 0.7% use a hearing aid | F-INDLOC-3 |
| Trouble with at least one everyday task | 48%; 24.8% need help | F-INDLOC-3 |
| Live alone | 5.7% (women 9.0%) | F-INDLOC-3 |
| Live with children | about two in three (40.6% with spouse and children + 27.6% with children and others) | F-INDLOC-3 |
| Difficulty making a phone call | 28.6%; women 34.8%; no schooling 37.7%; rural 32.8% | F-INDLOC-7, #175, A |

The survey is from 2017–18.

**Design consequences the research draws:** the device must speak; nothing on it should need reading; the patient should only have to listen or breathe, never dial or type; the family member is the default WhatsApp recipient.

### 3.2 Phones
- 87% of households have a mobile phone (94% urban, 84% rural). Household, not personal, ownership. (F-INDLOC-7, #175, A)
- Only 41% of older Indians own a smartphone; 71% use basic phones; 13% use the internet. News report of an NGO survey; method not seen; **single source**. (F-INDIA-5, #65, B)
- Telangana health centres, age **45+**: smartphone 19.5% rural, 36.5% urban; only 20.4% had good digital health literacy. One region, clinic sample. (F-INDLOC-8, #184, A)
- Other figures seen only in snippets, **not opened**: 65% in one city survey; 50% own any mobile in rural Karnataka. (F-INDIA-5 caveat, F-INDLOC-8 caveat, #179, C)
- **Gap:** no national figure for *personal* phone ownership among people aged 60+.
- India has 886 million active internet users; 57% prefer Indian-language content. Secondary report; no age split. (F-INDIA-6, #64, B)

### 3.3 Does voice work?
- **No peer-reviewed Indian study of voice or phone-menu health tools for older adults was found.** A PGIMER trial is testing it now and calls the evidence "scarce". (F-INDLOC-5, #164, A, protocol)
- So the voice-first case rests on literacy and vision data, not on a voice trial. Never say "elderly Indians prefer voice".
- The Government's Kilkari voice-call service (10 million+ subscribers): 50% answer the first call, 76% by the third. Of answered calls, about half are heard for most of the message. (F-INDLOC-6, #173, A)
- Kilkari's own randomised trial found **no effect on its main outcome** and only small gains elsewhere. (F-INDLOC-6, #174, A)
- A later analysis: morning calls are picked up most, listening drops around festivals, and pickup overstates success because someone else may answer. Preprint, not peer-reviewed. (F-INDLOC-9, #186, B)
- These are young mothers, not older patients.
- A UK WhatsApp AI coach saw 28% of chats sent as voice notes. UK pilot, 83 users. (F-INDLOC-5, #165, A)

### 3.4 Caregivers
- Usually a spouse, son, daughter or daughter-in-law in the same home; sometimes a child abroad, so two contacts in different time zones are allowed. **Team guidance, not a cited source.** (F-INDLOC-4)
- An adult son or daughter is not a "lawful guardian" in data law. The patient must consent personally. (F-REG-3, #122, A)

### 3.5 Languages
- Hindi is the mother tongue of 43.6% of Indians (Census 2011). Bengali 8.03%, Marathi 6.86%, Telugu 6.70%, Tamil 5.70%, Malayalam 2.88%. Those six add up to 73.8%. Don't claim a higher total for the 11 supported languages until the other five are checked. (F-INDIA-8, #69, B)
- Names, forms of address ("ji", "Amma/Appa", "Chechi"), date and money formats: **team guidance that needs an Indian team member's check.** (F-INDLOC-4)

### 3.6 Hospitals and nurses
- India has 2.60 registered nursing staff per 1,000 people, below the WHO benchmark of 3. Kerala 10.47, Karnataka 7.69; north and east far lower. Registered is not the same as working. An earlier figure (March 2025) was 2.20. (F-INDIA-7, #67, B; the primary document timed out, #66)
- **Gap:** ward-level nurse-to-patient ratios were not found.
- Heart bypass, angioplasty, hip-fracture fixation and knee replacement are among the top Ayushman Bharat procedures (2019–2021 data). (F-INDIA-9, #90, #91, B)

### 3.7 Who the patients are (used for realistic fake patients)
| Group | Typical profile | Ref |
|---|---|---|
| Heart bypass | About 87–89% men, late 50s to early 60s, often diabetic | F-INDLOC-1, #114 (A); snippets (C) |
| Knee replacement | 60–65% women, mean age about 62 | F-INDLOC-2, #113, A |
| Gallbladder removal | Mostly women in their 40s | F-INDLOC-2, #115, A |
| Lung damage after TB | Mean age about 50, 55% men | F-INDLOC-2, #115, A |
| Lung-lobe surgery | **Not found** | F-INDLOC-2 |

Single-hospital studies, not national averages.

### 3.8 Home-care market and prices – **thin: no official published price from any big provider**
- Apollo HomeCare sells home physiotherapy and a "Chest Physiotherapy" package but shows no prices. (F-BIZ-11, #178, B)
- Max@Home and Portea pages show no rupee prices. (F-BIZ-9, #155, #156, B)
- Snippets only, not opened (all C): home physio "from ₹499" or ₹700–2,000 a visit; attendants ₹1,800–3,200 a shift; Apollo home nursing ₹2,000–3,600 a day at launch; Portea home ICU ₹6,500–12,000 a day (2018); Max COVID monitoring from ₹333 a day. (F-BIZ-6, F-BIZ-9, F-BIZ-11, F-BIZ-3; #149, #160, #179)
- The research says: stop web searching; get a phone quote. Never put a specific provider's price on a slide.

---

## 4. The device

### 4.1 Spirometer models and prices
| Model | Type | Price | Ref |
|---|---|---|---|
| Romsons Breazer 2500 (REF SH-6083), up to 2,500 mL | Volume (piston) – **our target** | MRP about ₹1,067; online about ₹146–₹960 | F-INDIA-3, #7, #8, C; 3D_SOURCES B01 |
| Romsons SH 6082 "Respirometer" | Flow (3-ball) – our sensor can't read it | MRP ₹688 | F-INDIA-4, #33, C |
| Vyaire AirLife 2500 / 4000 | Volume – the only models InSee fits | – | F-COMP-1 |

- **The plans disagree with the knowledge base on price.** The plans say "₹300", "under ₹500", "₹220–500" and "₹217–855, Medikabazaar ₹477". The claim check says to use **"sold online for about ₹200–₹1,000"**. (Claim check C6–C7)
- Popular Hindi how-to videos mostly show 3-ball devices. Weak evidence (view counts are not market share). (F-INDIA-10, #92, C)

### 4.2 How the sensing works
**Main point:** a tiny laser sensor times how long light takes to bounce off the disc, which gives the distance, and we turn distance into millilitres.

**Everyday comparison:** like shouting into a well and timing the echo to judge the depth. A longer wait means a longer distance.

**The real mechanism:** the chip (ST's VL53L1X, a "time-of-flight" sensor) sends invisible 940 nm laser light, which is eye-safe (Class 1), and measures the return time about 30 times a second. A small board (an ESP32 or Arduino) passes the distance to the laptop over USB. The website converts millimetres to millilitres using a table recorded once per spirometer model at its printed marks. (HARDWARE.md; 3D_SOURCES E06, E07)

**Where the comparison breaks:** a well has one bottom. A narrow plastic tube also reflects light off its walls, which makes the reading too short (section 4.3).

**This idea is not ours.** InSee reads the piston with the same kind of infrared time-of-flight sensor, built at a university lab in 2020. (F-COMP-5, #88, B)

### 4.2a How InSee is mounted (checked 10 Oct 2026)
**Main point:** InSee uses the same layout as our base unit: a reusable tray under a disposable spirometer, with the sensor looking up at the piston from below.

| What was seen | Where | Grade |
|---|---|---|
| The product picture shows a pink tray. The AirLife spirometer stands in it. A raised white block with a small sensor window sits in the middle of the tray, directly under the main piston tube. | InSee home page, product picture (#102) | B |
| "An infrared sensor monitors the movement of the spirometer's internal cylinder"; time-of-flight is converted to volume. The spirometer is called disposable and the InSee reusable. | InSee "How InSee Works" page (#103) | B |
| The patent claims "a plurality of connectors disposed on a top of the device configured to mate with a base of the incentive spirometer", and a sensor that tracks the piston's displacement by time of flight. It also lists a **sound**-based time-of-flight option. | US10610129B1, claims 1–2 and description (#86) | A |
| The 2020 interview repeats the website's description. | IEEE Spectrum (#88) | B |

- **No source says whether the floor under the piston tube is an open hole or thin clear plastic.** None of the four mentions an opening. The FDA summary (#3) was not re-read this time.
- **What it supports:** the light does reach the piston from below on the AirLife, with no cutting or gluing. The sound-based option in the patent hints at an open air path (sound can't pass through solid plastic). This is a hint, not a fact.
- **What it does not prove:** anything about the Romsons Breazer. The AirLife is clear plastic all over. The Breazer has a **blue seat** under its piston, so our laser may meet blue plastic even if InSee's does not. Check B26 in section 4.7 is still open.
- **Effect on our design: none.** Our base unit (section 4.5) is already a tray with the sensor under the volume tube looking up through a short dark tunnel. InSee's tray is thinner (about 29 mm against our 46 mm); ours is taller on purpose, to keep the sensor at least 5 cm from the piston.
- **Fallbacks if the Breazer's floor is closed** (team reasoning, not sourced): (1) test whether the blue plastic lets infrared through, by pointing a TV remote through it at a phone camera, then run the sensor's crosstalk calibration; (2) cut an opening in the floor, which is the room-air side of the piston so the seal is not affected (demo only); (3) a camera watching the piston through the clear wall (roadmap). Never cut the top: that is the suction side.
- **Safe wording for the pitch:** "the same layout as the FDA-cleared InSee: a reusable tray under a disposable spirometer". Don't say "the Breazer has an open base" until a real unit has been checked.

### 4.3 Sensor accuracy facts
| Fact | Ref | Grade |
|---|---|---|
| Typical error out of the box: ±20 mm in the dark, ±25 mm in room light | F-TECH-1, #118 | B |
| Repeatability (how steady repeated readings are): about 1%, down to 0.15% with longer readings | F-TECH-1 | B |
| Nothing closer than 4 cm reads reliably | F-TECH-1; 3D_SOURCES E07 | B |
| Up to 50 readings a second; 20 ms per reading only in short-distance mode | F-TECH-1 | B |
| The beam spreads 27°; it can be narrowed in software to about 15° (the smallest "4×4" window) | F-TECH-1; 3D_SOURCES E05; F-TECH-3 #136, #149 | B / C |
| Inside a tube, wall echoes make the sensor **under-read**. Fix: narrowest window, dull dark walls, a clear target | F-TECH-3, #136 | C (forum, includes ST staff) |
| Light passing through clear plastic causes false readings ("crosstalk") | Final Research §2, #14 | B |
| Reading a volume scale by eye is itself imprecise: a Thai study found single readings differing by −469 to +567 mL between two devices (average difference 49 mL) | F-TECH-2, #120 | A |
| A US university clip-on (Michigan 2023) tracked the piston 99% accurately, volume within 7.5%, breath classification 100% sensitivity / 99% specificity | F-COMP-4, #50 | A |
| InSee's FDA study: 30 subjects, 240 data points, 100% agreement with blinded doctors (range 98.5–100%) | F-COMP-7 (imported), #101 | A/B |

- **No published test of this sensor inside an incentive spirometer exists.** Our own bench test is the real proof. (F-TECH-3)
- **Our "±100 mL" target is a target, not a result.** It is plausible only with calibration at 2–3 printed marks. Report the measured number. (Claim check C16)
- The plans mention a company press-release claim of 97% accuracy for InSee (not independently checked); the FDA summary gives the 100% agreement figure above. Use the FDA figure. (Final Research §1 vs F-COMP-7 imported)

### 4.4 Millimetres to millilitres
- Romsons publishes **no** inner size or mL-per-mm figure for the Breazer. (F-TECH-4, #137, #138, C; 3D_SOURCES)
- The printed scale is a factory calibration, not simple tube geometry. A piston of the size we derived, rising its full travel, would sweep only about 143 mL, yet the scale reads 2,500 mL. (3D_SOURCES note under table B)
- So: **never compute mL from the tube's diameter.** Map distance to the printed marks. (Claim check C22)

### 4.5 Dimensions with a source
- **Published by the maker (HIGH):** model name and capacity; marks every 250 mL from 250 to 2,500, printed on both sides; the goal-indicator slider; colours. (3D_SOURCES B01, B13, B20, B23)
- **Everything else on the spirometer is derived** from the maker's official drawing, scaled from one assumption: total height 200 mm (the only size three retailers agree on). Confidence LOW to MEDIUM. Examples: base 172.5 × 28 × 80 mm; piston 40.5 mm wide × 30.7 mm tall; 11.14 mm of travel per 250 mL. (3D_SOURCES B02–B28)
- Retailers disagree on box size and weight (250–350 g). (3D_SOURCES)
- **Electronics (HIGH, maker pages):** XIAO ESP32-C3 board 21 × 17.8 mm; sensor chip 4.9 × 2.5 × 1.56 mm (the datasheet contradicts itself: one table says 4.4); Pololu sensor board 13 × 18 × 2 mm. (3D_SOURCES E01, E04, E08)
- **Our base unit (our own design, derived):** 181.5 × 89 × 46 mm; sensor to piston 51.5 mm at rest and 162.9 mm at 2,500 mL; with the narrowed beam the spot is 42.9 mm wide at the top of travel against a tube bore of about 44.2 mm. That margin is thin and rests on derived sizes. (3D_SOURCES D02–D06)
- InSee for comparison: about 158 × 85 × 29 mm, 119 g, 1,200 mAh battery, USB-C. (F-COMP-7 imported; 3D_SOURCES)

### 4.6 Parts and cost
| Source of the estimate | Figure |
|---|---|
| Knowledge base (team estimate, hobby prices from unopened snippets): sensor ₹399–859, board ₹299, battery/buzzer/case ₹300–500 | **About ₹1,000–1,700 per unit** (F-BIZ-7, #149, C) |
| Complete Plan shopping list: board ₹500–900, sensor ₹500–1,000, battery ₹200–400, small parts | **About ₹1,400–2,600 per unit** at retail (Plan §3, §19) |
| Plan's mass-production aim | Under ₹1,000 – "an estimate, not a quote" (Plan §19) |

**The two estimates differ.** Both are the team's own, not quotes. Reuse assumptions differ too: 10+ patients per unit (≈ ₹100–170 each, F-BIZ-7) vs 20 patients (≈ ₹100 each, Plan §19).

### 4.7 What must be measured by hand
The web has nothing more to give here. With a caliper (a sliding ruler with a screen), on a real Breazer 2500:
1. **Is the floor under the piston open?** This decides whether a sensor underneath can see the piston at all. The single most important check. (3D_SOURCES B26)
2. Total height (if it isn't 200 mm, every derived size scales). (B02)
3. Base width, depth, height. (B04–B06)
4. Height of the 250 mL and 2,500 mL marks above the table. (B14)
5. Piston size and resting height; tube outer diameter and wall thickness. (B09–B12)
6. A bench test of the sensor at its narrowest window inside the tube at the top of travel. (Open gap 1)

Also not yet done: the firmware sketch has **not been compiled** on this laptop (checked against library documentation only). (HARDWARE.md §10)

---

## 5. Software and AI

### 5.1 Breath classification
- **Detecting a breath:** a "state machine" (a program that steps through fixed stages): waiting → breathing in → holding → falling. Bumps under 0.5 s or under 250 mL are ignored; InSee also counts only attempts above 250 mL. (Plan §5.3; REQUIREMENTS FR3)
- **Describing a breath:** 8 numbers ("features"): peak mL, % of target, time to peak, average and fastest rise speed, hold time, smoothness, duration. (Plan §6.2)
- **Labelling:** our own trained model, a *random forest* (many small decision trees that vote), gives one of four labels: good, too fast, too shallow, no hold. If the server is unreachable, fixed rules do the same job. (REQUIREMENTS FR4)
- **Score out of 10:** depth (4) + speed (3) + hold (3). Plain arithmetic anyone can check. Demo thresholds: target 2,000 mL, hold 3 s, "too fast" above 1,400 mL/s. (REQUIREMENTS FR5; 3D_SOURCES C01, C02)
- **Status today:** the model scores **95.8% on synthetic (computer-generated) breaths**. That is not accuracy on real people. The plan's real test (train on everyone except one person, test on that person; target 85% or more) has not been run on real breaths yet. (PROGRESS.md; Plan §6.2)
- **Prior art:** the Michigan clip-on already classified breaths (F-COMP-4). Hobby projects already speak "slow down / speed up" (F-COMP-10, #119, C). A US patent on a spirometer with "simulated humanlike voices" exists (title seen in search only; page failed to load, #87). **Our novelty is the combination for Indian homes, not any single feature.**
- **A camera mode** for 3-ball devices is roadmap only: one feasibility demo (Turkey 2025) on scripted data, no patients; no open-source tracker found. (F-TECH-2, #120, #119)

### 5.2 Voice (Sarvam AI, an Indian speech company)
| Fact | Ref | Grade |
|---|---|---|
| ₹100 free credit at sign-up; credits don't expire | F-VOICE-1, #53, #55 | B |
| Text-to-speech ₹3 per 1,000 characters (a 200-character message ≈ ₹0.60, our maths); speech-to-text ₹30 an hour; translation ₹0.005 per character | F-VOICE-2, #53 | B |
| The default voice model (Bulbul v3) covers **11 languages**: Hindi, Bengali, Tamil, Telugu, Gujarati, Kannada, Malayalam, Marathi, Punjabi, Odia, Indian English | F-VOICE-3, #54; VOICE.md §1.1 | B |
| The newest model (v4 Flash) has no Malayalam or Odia voices | F-VOICE-3 | B |
| Speed adjustable 0.5–2.0×; up to 2,500 characters a request; no pitch or loudness control on v3 | F-VOICE-3, F-VOICE-11; VOICE.md §1.1 | B |
| Sarvam's guide for wellness content: slower pace (0.8–0.9) and a "warm" setting; named voices per language (for example priya for Hindi, pooja for Malayalam, ishita for Tamil); avoid the dramatic voice "varun" | F-VOICE-11, #126 | B |
| Audio made with credits can be used commercially | F-VOICE-4, #56 | B |
| Speech-to-text (Saaras v4) covers 22 Indian languages plus English; 30 seconds per request; can be given up to 50 special words | F-VOICE-7, #75; VOICE.md §1.2 | B |
| **Terms of service:** no tailored medical advice without professional review; users must be told it is AI; human oversight required | F-VOICE-8, #78 | B |
| Phone "Voice Agents": ₹3.50 a minute launch price | F-VOICE-7 (imported), #99 | B |
| Keypad input is still "planned", so callers must speak their answer; a call transfers to one number only | F-VOICE-8 (imported), #94, #97 | B |
| "Emotion" is only after-call sentiment from the words, not a validated reading of tone of voice | F-VOICE-9 (imported), #104, #105 | B |
| Free offline backup: AI4Bharat Indic-TTS (open licence, 13 languages). Not tested; needs a strong computer | F-VOICE-10, #79 | B |
| Bhashini (government platform): no official terms or limits found | F-VOICE-12 | C |

- **Not checked / vendor claim only:** "first audio in under 250 ms" comes only from Sarvam's marketing. No independent test. (F-VOICE-11; claim check C10)
- **Notes disagree on the language count and the phone price.** Text-to-speech covers 11. The separate calls report lists 12 for phone agents (adds Assamese). The platform claims 22. Round 2 said the per-minute phone price was "not published" (F-VOICE-9); the imported report then found ₹3.50 a minute on a launch page. Say "11 Indian languages" for the voice coach.
- Nobody has listened to the voices with older listeners yet. Malayalam and Tamil wording is flagged for a native-speaker check. (F-VOICE-11 caveat; PROGRESS.md)

### 5.3 The language model (LLM = an AI that reads and writes text) and its guardrails
- **Use:** a 3-sentence daily summary and call scripts, written by Claude (`claude-opus-5-5`, effort "low"), with a fixed template whenever the key is missing or a call fails. (REQUIREMENTS FR10; CLAUDE.md)
- **Guardrails already in the design:**
  1. The AI never decides alerts, colours or red flags. Fixed rules in code do. (Plan §6.5, §6.7; FUTURE_ARCHITECTURE §6.5)
  2. Red-flag words (chest pain, can't breathe… in 11 languages) skip the AI and trigger a fixed "contact your nurse / call 112" message. (COMMS.md §1)
  3. Every automated message says it is automated. (COMMS.md §3; required by F-VOICE-8)
  4. Call results are stored as the patient's own words plus a neutral note, never a diagnosis. (SARVAM_CALLS… §6)
  5. Only the first name and the day's numbers are sent to the AI today; the proposal is to send a placeholder instead of the name. (FUTURE_ARCHITECTURE §0, §6.5)
- **Cost (list prices, #198, B):** Opus 5.5 $4 / $20 and Haiku 5.5 $0.10 / $0.50 per million input / output tokens; batch jobs are 50% off. **The two notes give different per-summary costs** because they assume different lengths: about ₹0.9 (Plan §6.5) vs about ₹0.56 (FUTURE_ARCHITECTURE §6.5) on Opus. Both are estimates.
- **Regulator's view of AI:** India's 2026 software guidance asks AI software to document its training data and the risks of bias, drift and made-up output, and may ask for testing on Indian patients. (F-REG-1, #123, B)

---

## 6. Communication

### 6.1 WhatsApp Business rules
| Rule | Ref | Grade |
|---|---|---|
| Health messages are **not banned**. They are barred only where local law demands special ("heightened") systems for health data. We found no such Indian rule. | F-COMMS-14 #207; F-REG-8 | B |
| You may message someone only if they gave their number **and opted in**. Every stop request must be honoured. | F-COMMS-14 | B |
| Don't ask for ID numbers in chat (no Aadhaar or ABHA numbers). | F-COMMS-14 | B |
| The "medical and healthcare products" restriction is about buying, selling and promoting. Our messages sell nothing. | F-COMMS-14 | B |
| Opt-in can be collected on paper, in person, by phone menu, SMS or a website. It must name the business. | F-COMMS-16, #213 | B |
| A business-started chat needs a Meta-approved **template** (a pre-approved message with blanks). Free-form text is allowed only within 24 hours of the person's last message. | F-COMMS-2, F-COMMS-14 | B |
| A plain care update should fit the cheap **"utility"** category. If Meta judges it promotional it is approved as "marketing" (about 7× the price); repeat abuse loses utility templates for 7–30 days. Whether ours qualifies is **our reading, not a Meta ruling**. | F-COMMS-15, #209 | B |
| Template review can take up to 24 hours. | F-COMMS-19, #227 | B |
| No health-specific template rule was found. | F-COMMS-15 | B |

**Two consents are needed, not one:** the family member opts in on WhatsApp (Meta's rule), and the patient consents to sharing their data with that person (data law). (R-WA-1)

**Precedent:** the Government's MyGov Corona Helpdesk ran on WhatsApp and delivered vaccine certificates from August 2021. News snippets only; pages not opened; current status not checked. **No Indian hospital example was verified.** (F-INDLOC-10, #218, B)

### 6.2 WhatsApp prices
- Meta's India rate from 1 Oct 2026: utility ₹0.115 a message; marketing ₹0.8631. Replies inside the 24-hour window are free. (F-COMMS-2, #61, #62, B)
- Twilio adds US$0.005 to every message, sent or received – several times Meta's own fee. (F-COMMS-10, #107, B)
- **Per-patient figures in the notes differ because they assume different message counts:** 14 reminders a day ≈ ₹1.6 a day (F-COMMS-2); 3 updates a day ≈ ₹5 per 14-day recovery (F-BIZ-7); about 90 templates a month ≈ ₹10 (FUTURE_ARCHITECTURE §7). All are team estimates.

### 6.3 Phone calls and TRAI rules (TRAI = India's telecom regulator)
- TRAI's 2026 rule text (read in full, a scanned PDF) defines an **"A2P call"**: any call started by software with no human dialling, including robocalls and AI voices. Every sender must **declare** A2P calling and its caller IDs in advance; an undeclared A2P call counts as spam. (F-COMMS-8, #106, A; F-COMMS-12, #139, A)
- A "service call" about something the customer already has needs no explicit consent. A call supporting "ongoing use" needs explicit consent that lasts **7 days** and can be renewed. Which type a post-discharge reminder is: **our reading, not a ruling.** (F-COMMS-8)
- Telecom consent does not replace data-law duties. (F-COMMS-8)
- The receiving operator may charge up to 5 paise a minute for A2P calls. (F-COMMS-8, F-COMMS-12)
- Start dates: 30 and 60 days after publication in the official Gazette. **The Gazette date was not found**, so the rules may already be in force around the hackathon. (F-COMMS-12; risk 24)
- Only an India-registered business with identity checks done can rent Indian numbers and make domestic calls. The trusted "1600" number series is for banks, insurers and government only. (F-COMMS-3 #71, F-COMMS-4 #70, F-COMMS-11 #110; B)
- Twilio calls to India show a foreign caller ID. Twilio trial accounts allow 5 verified numbers. How these rules interact is undocumented; **test one call.** (F-COMMS-1 #60, F-COMMS-5 #74)
- An industry player asked TRAI to exempt calls where a live person is on the line. **Whether the final rule accepted this is unknown.** (F-COMMS-13, #140, B)
- Prices: Plivo ₹0.38 a minute plus ₹200 a month per number; Exotel publishes no per-minute price. Team maths: a 2-minute AI call ≈ ₹8, about 70 times a WhatsApp message. (F-COMMS-11, #109, #111, B; F-COMMS-7)
- SMS needs "DLT" registration by an Indian company, about 1–3 weeks. The fee is unclear: vendor guides quote about ₹5,900; another says free. **Both shown; neither confirmed.** (F-COMMS-9, #108)

**Design decisions the research led to:** WhatsApp first; calls only as an escalation; the safest call is "nurse clicks, a human talks"; record consent at discharge and renew weekly; no SMS in the hackathon; live calls only to a consenting team phone, otherwise the browser phone simulator.

### 6.4 Reminder timing evidence – **thin: 3 sources, none on older surgical patients**
- Hourly reminders in waking hours worked in the US bypass trial. (F-ADH-1)
- Kilkari: retry up to 3 times (50% → 76%); morning slots do best; ease off around festivals; count a call as done only if the person listened. (F-INDLOC-6, F-INDLOC-9)
- **Kilkari reach figures conflict:** one paper says 99.5% are reached by the 9th call; a later preprint says about 23% are never reached after 9 attempts. Different groups and definitions. Quote "half answer the first call" and "retries matter". (Risk 36)
- Quiet hours are team guidance, and the notes differ: 9 pm–7 am (F-INDLOC-4, COMMS.md) vs 10 pm–8 am (Plan §10.1). The built default is 21:00–07:00.

### 6.5 WaBI vs Meta's Cloud API vs Twilio (round 9, conclusions only)
- **WaBI is the team's own product (Coyot AI), built on Meta's WhatsApp Cloud API.** So "WaBI or Meta direct" really means "use the layer we already have, or write it again". Company's own material, grade B. (F-COMMS-17, #219, #221, #222)
- **Yes, a server can send through WaBI by itself with an API key.** (F-COMMS-17)
- It supports **templates and plain text only**: no images (so no weekly progress card), no voice notes. (F-COMMS-17)
- WaBI adds no per-message charge; Meta bills the WhatsApp account. (F-COMMS-18)
- **Nothing was test-sent.** There are no public API documents. (Round 9 notes)
- **Not confirmed:** whether WaBI can keep message data stored in India; whether a separate, bot-free number exists for a demo. (Round 9 "still uncertain")
- Meta's Cloud API used directly gives a free test number at once, but none of it is written in SpiroBuddy yet. (F-COMMS-19, #224–#230, B)
- The Twilio sandbox is already coded: each phone must send a join code, the session lasts 3 days, so re-join on demo morning. (F-COMMS-6, #29/#85, B)

| | WaBI | Meta Cloud API direct | Twilio sandbox |
|---|---|---|---|
| New code needed | Small | Larger | **None** |
| Demo-ready | Probably; untested | Possible; more new code | **Yes** |
| Right for a hospital pilot | **Yes, with fixes** | Yes, but rebuilds what WaBI has | No |
| Cost | Meta's fee | Meta's fee | Meta's fee + Twilio's |

**Recommendation from the research:**
- **Demo:** keep the Twilio sandbox plus the built-in phone simulators. No new code the night before.
- **Pilot:** WaBI with the hospital's own verified WhatsApp number, so families see the hospital's name. Before the first real patient: confirm India hosting and India storage of message data, add image or voice-note sending if the pilot needs it, and sign a data-processing agreement with the hospital. If that can't be done in time, use Meta's Cloud API directly.
- **Risk:** don't use the company's live sales number for patient-family messages. (R-WA-6)

---

## 7. Regulation and privacy

### 7.1 Medical-device class (CDSCO = India's medical-device regulator; classes run A, lowest risk, to D)
The answer changed over four rounds. All four are shown; **the latest is the one to use.**

| Round | What was found | Ref |
|---|---|---|
| 3 | Guidance decides by what software does. Diagnostic and monitoring spirometers are Class B. No incentive-spirometer row found. "As an exercise coach it may count as wellness." | F-REG-1 #123 (B), F-REG-2 #124, #125 (B, consultancy copies) |
| 4 | Primary text: wellness software must not mention any disease, and software that **alerts** about a condition is never wellness. Stand-alone software that only *informs* care of a serious condition points to Class A, but a device that measures needs a licence. | F-REG-4, #135, A |
| 5 | CDSCO's own list names "Incentive spirometer" (item 496) as Class A, non-sterile, **non-measuring**, "not a diagnostic device": registration only. Our clip-on measures, so it is very likely not covered. | F-REG-5, #150, A |
| 7 | The law itself (Medical Devices Rules 2017): an accessory is classed **on its own**. A powered device that gives monitoring information about a vital body process is **Class B**; Class C if it monitors for immediate danger; Class A only if no such rule applies. | F-REG-6, #183, A |

- **Current position (team reading, not a ruling):** the plastic spirometer is Class A. **We expect our clip-on to be Class B** and would confirm with CDSCO or a consultant. It should not be Class C as long as we never claim real-time danger monitoring.
- The guidance drops the older labels "software as a medical device" (SaMD) and "software in a medical device" and uses one term, **"medical device software"**. It is guidance "for public awareness", not law. (F-REG-1, F-REG-4)
- **Wording that keeps us out of trouble:** "an exercise coach and adherence tracker for a spirometer the nurse has already prescribed". Avoid "real-time monitoring", "detects deterioration", "prevents pneumonia": these push the class up. (F-REG-6 caveat)
- Not found: whether Romsons has registered the Breazer; CDSCO's rules for changing software after approval. (Open gap 2; FUTURE_ARCHITECTURE §6.6)
- In the US, incentive spirometers are Class II (search snippet only, C). InSee's US clearance says nothing about India. (F-REG-4 caveat; SARVAM_CALLS… §8)
- For later: a quality system (ISO 13485), software life-cycle (IEC 62304), risk file (ISO 14971), usability testing (IEC 62366-1). Catalogue pages only, from search results. (FUTURE_ARCHITECTURE §10, #202, B)

### 7.2 Data protection (DPDP = India's Digital Personal Data Protection Act 2023 and Rules 2025)
Read in the primary text (F-REG-3, #122, A):
- Most duties start about **May 2027** (18 months after November 2025).
- A stand-alone notice in plain language listing **each item** of data and each purpose.
- Withdrawing consent must be as easy as giving it.
- Encryption, access control, and **access logs kept one year**.
- Breach: tell affected people without delay and the Data Protection Board within **72 hours**.
- The adult patient consents personally; a son or daughter is not a lawful guardian.
- There is **no special "health data" category**: all personal data gets the same basic protection.

Also:
- An older rule set (IT Act SPDI Rules 2011) treats health information as sensitive and asks for written consent. Whether the new Act replaces it: **not verified from primary text.** (F-REG-8)
- Cyber-incident rules (CERT-In 2022): report within 6 hours; keep logs 180 days in India. From search results, not opened by the research agent. (FUTURE_ARCHITECTURE §3.7, #194, A)
- Our reading of roles, **not legal advice**: hospital = the party responsible for the data; SpiroBuddy = its processor; Meta = sub-processor. (F-REG-7; FUTURE_ARCHITECTURE §3.3)
- The India Telemedicine Practice Guidelines 2020 reportedly list WhatsApp as an allowed text tool. **The primary PDF could not be opened**; this rests on secondary summaries (C as read), and the guidelines cover doctors' consultations, not family updates. (F-REG-8, #214–#218)

### 7.3 Where the data lives
- On Meta's Cloud API, Meta acts as a data processor, keeps message content at most 30 days, encrypted at rest, and can store it **in India** if the number is registered that way. (F-REG-7, #210–#212, B)
- Even then, content may be processed abroad for **up to 60 minutes**. So "the data never leaves India" is false. (F-REG-7)
- Cloud API decrypts messages on Meta's servers. So it is not "end-to-end encrypted to the hospital"; say "encrypted in transit and at rest". (F-REG-7; R-WA-3)
- The data law does not ban transfers abroad; it lets the government blacklist countries. Whether any list exists: **not checked.** (F-REG-7; FUTURE_ARCHITECTURE §3.5, #196)
- Today's demo runs on fake data, with the web server outside India and the database in Mumbai. The architecture note says real data must sit in Mumbai before the first real patient. (HANDOFF.md; FUTURE_ARCHITECTURE §3.5)
- Outside processors (the LLM, Twilio, Meta) should get no data that identifies the patient. (FUTURE_ARCHITECTURE §3.5)

### 7.4 ABDM (India's national digital health records programme) – **thin: 2 sources, from search results**
- A read-only export in the national FHIR format (a standard for health records) is proposed. The Indian profile set has no lung-function or device profile. (FUTURE_ARCHITECTURE §3.8, #199, A)
- Joining ABDM means passing three milestones (M1–M3) in a test environment. The forum source is grade C; confirm with ABDM. (#200)

### 7.5 Consent as built
Patient consent in their language, read aloud, with an itemised data list; a yes plus a date; weekly "keep reminders?" renewal for calls; one-word STOP in each language; a separate opt-in from each family member. (COMMS.md §3; F-REG-3; F-COMMS-16)

---

## 8. Market, business model and costs

### 8.1 Competitors and prior art
| Name | What it is | Why it matters | Ref |
|---|---|---|---|
| **InSee** (Tidal Medical, USA) | FDA-cleared clip-on (K241152, 21 Aug 2025, Class II). Fits AirLife 2500/4000 only; hospital, prescription use; reminders every 10–120 min | Closest product. **No public price; no verified India distributor.** | F-COMP-1 #31 #3; F-COMP-7 (imported) #102 |
| Tidal's patents | US patents active to about 2038. Their international application is listed as "Ceased" with no Indian filing. | Patents are national. **The Indian patent office database was not searched.** Legal status is Google's assumption. Not legal advice. | F-COMP-6 #86; F-COMP-8 #132 |
| Michigan optical clip-on (2023) | University add-on with breath classification | Closest technical prior art | F-COMP-4 #50 |
| Airalux (Penn) | A whole new digital spirometer, not a clip-on | 30-patient trial, no control | F-COMP-3 #34 |
| Go-breath (Korea) | Hourly alarm + nurse dashboard, self-reported | Showed no benefit; prior art for our schedule | F-ADH-5 #52 |
| Smart CABGuard (Amrita, Kochi) | Nurse-led AI chatbot + heart patch after bypass; needs a smartphone; no breathing exercise | Never say "first AI follow-up in India". A possible partner. Protocol only. | F-COMP-12 #154 |
| Zorgers + Clinitouch, Tricog, Dozee | Indian home or hospital monitoring | None tracks spirometer exercise | F-COMP-11 #144 (B), #145 (C) |
| Respira Health | WhatsApp lung rehab for COPD | 18% completion; 30% when hospital-referred (self-reported) | F-COMP-9 #133 (C) |
| Alveofit, SpiroPRO | Indian *diagnostic* spirometers | Not exercise coaches. Snippets only. | F-COMP-7, C |

- **"No Indian smart incentive spirometer was found"** is absence of evidence from web search, with no Indian patent search. Safe wording: "we found no Indian product that tracks incentive-spirometer exercise at home". (F-COMP-7)
- Names seen only in search results, not checked: SpiroTimer, TryBreath, QUT "ISy", trial NCT03686631. (F-COMP-2)
- InSee being "English-only" is **unverified**; say "designed for US hospitals". Airalux being "iPhone-only" is **weak**; say "an iPhone/iPad app in the trial". (Claim check C8, C5)

### 8.2 Who pays, and pricing anchors
- **Ayushman Bharat (PM-JAY, the government insurance scheme)** pays a fixed bundle: bypass ₹1,62,400 (10-day stay), gallbladder removal ₹31,100, lung-lobe removal ₹32,900, knee replacement ₹36,400 plus ₹60,500 implant. Extra days come out of the hospital's pocket. One state's copy of the 2022 list; rates vary by city tier and may have been revised. (F-BIZ-1, #128, A)
- Indian chains already pay for post-surgery home monitoring (Manipal + ConnectedLife, 2022). No prices or results published. (F-BIZ-3, #130, B)
- **Model the research points to:** hospital-paid, units lent at discharge and reused. (F-BIZ-3; Plan §19)
- **Price idea (team estimate, not validated with any hospital):** ₹500–1,000 per patient episode – less than half a ward bed-day. (F-BIZ-7)

### 8.3 Cost per patient (all team estimates)
| Line | Figure | Ref |
|---|---|---|
| Hardware share per patient | ≈ ₹100–170 | F-BIZ-7; Plan §19 |
| WhatsApp, 14-day recovery | ≈ ₹5 | F-BIZ-7 |
| Voice | ≈ ₹0.6 a message, or ₹0 with pre-made clips | F-VOICE-2 |
| AI phone call | ≈ ₹8 for 2 minutes | F-COMMS-11 |
| Running cost per active patient-month at pilot size (~50 patients) | ≈ ₹450 (mostly the fixed server bill) | FUTURE_ARCHITECTURE §11 |
| …at 5,000 patients | ≈ ₹85–110 | same |
| …at 100,000 patients | ≈ ₹50–60 | same |

Not included: staff, security testing, quality-system certification, regulator fees. The judge answers disagree on parts cost: J11 says "a few hundred rupees"; J23 and the estimates above say ₹1,000–1,700. Use the latter.

### 8.4 Market size
- Surgery: about 356 major operations per 100,000 people (2019), about 49 lakh a year in public records (an undercount), growing about 4% a year. (F-INDIA-1, #63, A)
- Next market: lung-TB survivors, "lakhs of people a year" (section 2.8).

### 8.5 Go-to-market – **thin: 2 sources plus team reasoning**
- Enrol patients at discharge through the nurse, not through adverts (Respira: 30% vs 14% completion). (F-COMP-9, C)
- Lead with bypass and abdominal surgery, and with length of stay and adherence. A readmission story is weak for knee patients (about 1%) and for Indian abdominal surgery (4.7%, lungs not named as a cause). (Risks 29, 31)
- First step proposed: one pilot hospital, about 50 patients, with ethics approval. (FUTURE_ARCHITECTURE §1; Plan §21)

---

## 9. Judge Q&A

Short answers prepared in the knowledge base (J1–J38 and J-WA). Where a later research round corrected an earlier answer, the corrected version is given and marked **(updated)**.

### Does it work?
| # | Question | Short answer | Evidence |
|---|---|---|---|
| J1 | Does incentive spirometry even work? | On its own, the evidence is weak. As part of a nurse-led breathing bundle, it helps. The trials never checked whether patients did the exercise. We make that visible. | F-CLIN-3, 4, 6, 7 |
| J2 | What proof is there that reminders help? | In a randomised trial of 145 bypass patients, hourly reminders doubled the share of waking hours with exercise (58% vs 28%) and breaths per day (35 vs 17). | F-ADH-1 |
| J14 | A Korean app with hourly alarms showed no benefit. | Go-breath relied on patients reporting their own use, with no sensor. We record every breath automatically, as the successful US trial did. | F-ADH-5, F-ADH-1 |
| J30 | Digital reminders for TB barely worked. Why would yours? | Right: on average they help only modestly. Our sensor records each breath, so there's no self-reporting, and digital follow-up reliably brings problems to the nurse earlier. | F-ADH-8, F-ADH-1 |
| J27 | Will you cut readmissions? | We don't claim that. Worldwide about 1 in 8 bypass patients is readmitted within a month, with lung problems among the causes. Our pilot would measure it. For knee replacement, readmissions are already low. | F-BIZ-8 |
| J32 | What's the readmission rate in India? | In 30 Indian cancer centres, about 1 in 20 major abdominal-surgery patients was back within a month (4.7%). For bypass we found no Indian number; worldwide it's about 1 in 8. | F-BIZ-10, F-BIZ-8 |
| J38 | And after bypass in India? | Indian centres don't publish it; we searched three rounds. Measuring it is part of our pilot. | F-BIZ-12 |
| J15 | Is India's problem big enough? | Public records alone show about 49 lakh major operations a year (an undercount). About 1 in 10 surgical patients gets a lung complication, and in one Indian study 28% of those died. India also has fewer nurses than WHO recommends. | F-INDIA-1, F-CLIN-1, F-CLIN-8, F-INDIA-7 |
| J16 | What does a lung complication cost an Indian hospital? | A ward day costs about ₹2,300 and an ICU day about ₹26,000 at a public teaching hospital. These patients spend about a week more in ICU, so roughly up to ₹2 lakh. That's our rough estimate from two Indian studies. | F-BIZ-4, F-BIZ-5, F-CLIN-8 |

### The competition and the idea
| # | Question | Short answer | Evidence |
|---|---|---|---|
| J3 | InSee is FDA-cleared. Why you? | InSee proves laser tracking works in US hospitals. It fits one US spirometer and is for hospital use only. We add home use, Indian devices, technique AI, coaching in Indian languages and WhatsApp for the family. | F-COMP-1, F-COMP-5, F-COMP-7 (imported) |
| J4 | Aren't you infringing Tidal's patents? | Patents are national. Their US patents don't cover India, and public databases show their international application lapsed without an Indian filing. We'd do a formal check before any US launch. (We are not lawyers; the Indian patent office database has not been searched.) | F-COMP-6, F-COMP-8 |
| J28 | Amrita already has an AI chatbot for bypass patients. | It shows hospitals want this. Smart CABGuard watches the heart and needs a smartphone. We check the breathing exercise and work by voice. We'd plug in alongside it. | F-COMP-12 |
| J21 | Who else does home monitoring in India? | Zorgers with Clinitouch for COPD, Tricog after discharge, Dozee in hospital. None checks whether patients do their breathing exercise, or how well. | F-COMP-11 |
| J6 | Most Indian patients get the 3-ball type. | True for many home patients. The US guideline suggests the volume type, and an Indian trial found it better for walking recovery. A camera mode for 3-ball devices is on the roadmap: shown feasible, not yet tested on patients. | F-INDIA-10, F-CLIN-4, F-CLIN-9, F-TECH-2 |

### The device
| # | Question | Short answer | Evidence |
|---|---|---|---|
| J5 | How accurate is the sensor? | Out of the box the chip is accurate to about ±2 cm, but its readings are very steady, so we calibrate it to each spirometer's printed marks. Even reading the scale by eye varies by hundreds of mL. We coach good breaths; we don't claim lab-grade volume. | F-TECH-1, F-TECH-2 |
| J18 | Can a laser work inside a plastic tube? | Wall echoes are a known problem. We narrow the sensor's view from 27° to about 15°, aim it down the middle and calibrate on the printed marks. | F-TECH-3, F-TECH-1 |
| J19 | How do you turn millimetres into millilitres? | We don't use geometry. We read the distance at the device's own printed marks and map between them, once per spirometer model. | F-TECH-4 |

### Users
| # | Question | Short answer | Evidence |
|---|---|---|---|
| J7 | Old patients don't use smartphones. | Right: only 41% own one, and 3 in 4 older women can't read. So the device speaks and the WhatsApp update goes to a family member. Two in three older Indians live with their children. | F-INDIA-5, F-INDLOC-3 |
| J33 | Will older people even pick up a phone call? | The Government's Kilkari service shows half pick up on the first try and three in four by the third. And 29% of over-60s find making a call hard. So we retry, the patient only has to listen, and the family gets WhatsApp. | F-INDLOC-6, F-INDLOC-7 |
| J29 | Does putting the family on WhatsApp help? | An Indian pilot at a Tata Memorial unit supported caregivers via WhatsApp. Unplanned follow-up visits halved and family stress fell. (Complications did not change.) | F-ADH-7, F-INDLOC-3 |
| J13 | WhatsApp bots lose most users. | True: an Indian WhatsApp rehab bot saw 18% completion, but 30% when hospitals referred patients. We enrol at discharge through the nurse, and the device beeps and speaks even if nobody opens WhatsApp. | F-COMP-9 |
| J35 | Do older rural patients keep up home exercise? | In the Thar Desert, 76% of older COPD patients were still exercising after 8 weeks of phone-guided Hindi rehab, and 58% after a year. | F-ADH-9 |
| J25 | Do Indian patients want home programmes? | In Pune, 87% of chronic lung patients wanted rehab and 84% liked a home-based digital programme. | F-VIS-3 |

### Rules and safety
| # | Question | Short answer | Evidence |
|---|---|---|---|
| J26 **(updated)** | Is an incentive spirometer regulated in India? | Yes, at the lowest level: CDSCO lists it as Class A, non-measuring, not a diagnostic. Our clip-on measures and alerts, so it needs its own registration and licence. We expect Class B and will confirm with CDSCO before selling. | F-REG-5, F-REG-4, F-REG-6 |
| J36 | Isn't your clip-on just an accessory to a Class A device? | No. Indian law classes an accessory on its own. Ours is battery-powered and gives monitoring information, so we expect Class B. The demo is a prototype, not a device on sale. | F-REG-6 |
| J8 / J17 **(updated)** | Is it a medical device? Don't nurse alerts make it one? | Yes, probably. CDSCO says software that alerts about a condition isn't "wellness". We expect Class B and would apply before launch. The hackathon build is an exercise coach and adherence tracker. (Earlier answers said "we'll get a ruling first" and "points to Class A"; round 7 replaced both.) | F-REG-1, F-REG-2, F-REG-4, F-REG-6 |
| J9 | Data privacy? | The demo uses fake patients. For launch we follow the DPDP Rules: a notice in the patient's language listing each piece of data, read aloud; one-word withdrawal; encryption and access logs; breach reports within 72 hours. The patient consents, not the son. | F-REG-3 |
| J12 | Won't the AI give medical advice? | No. It only coaches and summarises, and says it's an AI. Red-flag words trigger a fixed "call your nurse or 112" message, and a nurse reviews every flag. Sarvam's terms require this too. | F-VOICE-8 |
| J10 / J24 | Can you legally robocall patients in India? | Under TRAI's 2026 rules AI calls are "A2P calls": declared in advance, from an Indian registered number, and some reminder calls need consent renewed weekly. So calls are an escalation step, and ours is a nurse-to-patient call with a human on the line. WhatsApp and the device work today. | F-COMMS-8, 11, 12, 13 |
| J20 | Won't patients ignore calls marked as spam? | Calls are only the backup. TRAI now bars caller-ID apps from blanket-tagging official commercial series, and a hospital's declared number is the right channel. | F-COMMS-12, F-COMMS-13 |
| J-WA | How is sending health updates on WhatsApp allowed? | WhatsApp's business rules allow health messages unless local law demands special health-data systems, and we found no Indian rule that does. We message only a family member who has opted in, after the patient has consented, using approved non-promotional templates, and anyone can reply STOP. The messages are progress updates, never a diagnosis. Meta acts as our data processor, deletes content within 30 days and can store it in India. | F-COMMS-14, 15, 16; F-REG-7, F-REG-8; F-INDLOC-10 |

### Money and scale
| # | Question | Short answer | Evidence |
|---|---|---|---|
| J11 **(updated)** / J23 | What does it cost, and who pays? | About ₹1,000–1,700 of parts for a reusable clip-on (roughly ₹150 a patient over 10 uses), plus about ₹5 of WhatsApp per recovery. The hospital pays ₹500–1,000 per patient: Ayushman Bharat pays a flat ₹1.6 lakh for a bypass, so avoiding extra days protects its margin. (All our estimates. J11 originally said parts cost "a few hundred rupees".) | F-BIZ-7, F-BIZ-1, F-BIZ-3, F-BIZ-4 |
| J22 / J34 | Is this just for surgery? Is it used for TB survivors? | Surgery first. India's TB programme asks for every patient finishing treatment to be checked, and the 2024 RBIPMT rehab guidance lists the incentive spirometer among its breathing exercises (a draft, for supervised sessions). An Indian study completed 246 of 260 patients at home. | F-VIS-1, F-VIS-2, F-VIS-5 |
| J31 **(updated)** / J37 | How big can this get? | In 2024 India notified about 18.5 lakh lung-TB cases. With 90% treated successfully, roughly 16–17 lakh people a year finish treatment; studies find about half still have weak lungs. That's our estimate: "lakhs of people a year". (J31 originally said 23 lakh.) | F-VIS-7, F-VIS-4 |

---

## 10. Claims we must NOT make

Collected from `PITCH_FACTS.md`, `HANDOFF.md`, the plans and the Sarvam/InSee report.

| Don't say | Why | Say instead |
|---|---|---|
| "Prevents pneumonia" | Not shown (F-CLIN-3, F-CLIN-7); also pushes the device class up | "Helps patients do the exercise the nurse prescribed, and makes it visible" |
| "Clinically proven" | No trial of SpiroBuddy exists | "A prototype; our pilot would measure adherence" |
| "58% of patients vs 28%" | The trial counted hours, not patients | "doubled the share of waking hours with exercise: 58% vs 28%" |
| "Reduces readmissions" / "₹X saved per patient" | Never measured; knee readmissions are about 1% | "We'd measure readmissions in a pilot" |
| "No Indian readmission data" | There is: 4.7% after abdominal cancer surgery | "About 1 in 20 after major abdominal surgery in India; for bypass, about 1 in 8 worldwide" |
| "Indian bypass readmission is X%" | No published figure | "Indian centres don't publish it" |
| "First in the world" / "nobody has done this" | InSee, Michigan, Airalux, Go-breath exist | "Built for India: Indian spirometers, Indian languages, home use" |
| "First AI follow-up in India" | Amrita's Smart CABGuard | "Complements nurse-led AI follow-up already being trialled" |
| "Laser sensing is our invention" | InSee uses the same principle | "Like InSee, we read the disc with a laser sensor; our AI judges technique and coaches in Indian languages at home" |
| "Diagnoses" / "detects pneumonia" / "measures lung function" | We don't; and it changes the device class | "Tracks breathing exercises; flags patients for a nurse to review" |
| "Real-time monitoring" / "detects deterioration" | Pushes the class towards C | "Exercise reminders and an adherence summary for the care team" |
| "CDSCO-approved" / "FDA-approved" / "FDA-like" | Not true | "A prototype, not a medical device on sale" |
| "No licence needed" / "no regulation applies" | The exemption is for non-measuring devices only | "We expect Class B and will confirm with CDSCO" |
| "It's just an accessory, so it's Class A" | Accessories are classed on their own | Same as above |
| "Accurate to ±100 mL" | That's a target, not a result | Report the number we measure on the day |
| "Costs ₹1,000" | Unproven | "About ₹1,000–1,700 of parts as a hand-built prototype (our estimate)" |
| "A ₹300 spirometer" | Prices vary widely | "Sold online for about ₹200–₹1,000" |
| "InSee is English-only" / "Airalux is iPhone-only" | Unverified / weak | "Designed for US hospitals" / "an iPhone/iPad app in the trial" |
| "InSee costs X" / "ships to India" | No price or distributor found | "No public price was found" |
| "Elderly Indians prefer voice" | No trial | "Voice-first because 3 in 4 older women can't read" |
| "AI calls change behaviour" | Kilkari's trial: no effect on its main outcome | "Calls are a backup; the sensor, live feedback and a nurse do the work" |
| "The agent diagnoses pain" / reads emotion from the voice | Only after-call sentiment from words exists | "Possible distress – nurse to review (low confidence)" |
| "Sarvam speaks in under 250 ms" | Vendor claim only | "Fast enough for live coaching", or measure it ourselves |
| "No TB guideline uses incentive spirometry" | RBIPMT 2024 lists it | "India's TB rehab guidance (2024, draft) includes it, in supervised sessions" |
| "The TB programme recommends home spirometry" | The guidance is for supervised centre sessions | Same as above |
| "WhatsApp is end-to-end encrypted to the hospital" | Cloud API decrypts on Meta's servers | "Encrypted in transit and at rest" |
| "The data never leaves India" | Up to 60 minutes of processing abroad | "Message content rests in India with the local-storage setting" |
| "WhatsApp/Meta approved us for health" / "DPDP-certified" | No such approval exists | "We follow WhatsApp's business policy and the DPDP Rules" |
| "The telemedicine guidelines approve our updates" | They cover doctors' consultations; we read only summaries | Don't cite them as approval |
| "We message the family" | Incomplete | "…a family member who opted in, with the patient's consent" |
| "We can robocall any number right away" | Needs an Indian registered sender, declared caller IDs and consent | "Calls are an escalation step through an Indian telephony partner" |

---

## 11. Open questions and gaps

### 11.1 Needs a person (the web can't answer these)
1. **Caliper measurements** of a real Breazer 2500, above all whether the floor under the piston is open, and a bench test of the narrowed sensor inside the tube. (Open gap 1; 3D_SOURCES)
2. **Indian patent office search** (the site needs a human to pass a CAPTCHA): "incentive spirometer", "spirometer", "respiratory exerciser"; applicant "Tidal". (Open gap, rounds 3–5)
3. **TRAI Gazette date** for the 2026 rules, and whether the final text exempts calls with a live person. A telecom lawyer's view on which call type applies. (Open gap 4)
4. **CDSCO:** confirm our class (pre-submission query or a regulatory consultant); check whether Romsons registered the Breazer (box label or CDSCO's registration portal). (Open gap 2)
5. **Native-speaker checks:** Hindi, Tamil and Malayalam wording; forms of address; one older listener per language to choose the voice. (PROGRESS.md; F-VOICE-11; F-INDLOC-4)
6. **Clinical-trial registry (CTRI) search by hand** for Indian post-discharge spirometer trials. (Open gap 5)
7. **A phone quote** for home physiotherapy, if a price is needed. (F-BIZ-11)
8. **Ask a cardiac surgeon** for their unit's 30-day readmission rate. (Open gap 3)
9. **Download the Telemedicine Practice Guidelines 2020** in a browser; all automated attempts were blocked. (Round 8 gap 1)
10. **A lawyer** to confirm that no hospital IT policy or state rule forbids WhatsApp updates, and to check the old IT-Act health-data rules. (F-REG-8)
11. **A nurse or physiotherapist** to agree the alert rules. The plans ask for this call; no record of it was found in the research notes.

### 11.2 What the research looked for and did not find
- Indian data on incentive-spirometer use **after discharge** (three rounds).
- A published Indian 30-day readmission rate after heart bypass (three rounds; "stop web searching").
- The rupee cost of a post-surgery lung complication in India.
- Any trial of voice or phone-menu health tools for older Indians; any data on WhatsApp voice-note use by older Indians.
- A national figure for personal phone ownership among people aged 60+.
- Ward-level nurse-to-patient ratios.
- Any published size or mL-per-mm figure for the Breazer; any published test of this sensor inside a spirometer.
- InSee's price and any India distributor.
- Whether the floor under the piston tube is open, on the AirLife or on the Breazer (section 4.2a).
- An Indian smart incentive spirometer (absence of evidence only).
- Official current home-care prices from Portea, Apollo or Max.
- An Indian **hospital** using the WhatsApp Business API for patient or family updates.
- Sarvam's response time from an independent test; Bhashini's official terms.
- Typical age and sex of Indian lung-lobe surgery patients.
- The India TB Report's own table (to cross-check the lung-TB share).

### 11.3 Not yet tested by us
- A live WhatsApp send through WaBI; whether WaBI can keep message data in India. (Round 9)
- Real Twilio, Exotel or Sarvam calls with real keys. (COMMS.md §12)
- The firmware compiled and run on real hardware; measured volume accuracy; battery life. (HARDWARE.md §10)
- The breath model on real people (only 95.8% on synthetic breaths so far).
- Whether the ₹100 Sarvam credit covers phone calls. (F-VOICE-7 imported)

### 11.4 Where the research notes disagree
| Topic | Version A | Version B | Use |
|---|---|---|---|
| Our device class | Round 3: "may count as wellness"; round 4: "points to Class A" | Round 5: "Class A measuring or Class B"; round 7: expect **Class B** | Round 7 |
| "No CDSCO class found for incentive spirometers" (plans, F-REG-2) | – | Round 5 found it: Class A, item 496 | Round 5 |
| Reminder result | Plans: "58% vs 28% of patients" | Trial: share of waking **hours** | Hours |
| Udaipur study link | Plans and ledger #9: article 2439 | Numbers are in article 3176 (#83) | 3176 |
| Spirometer price | Plans: ₹300, "under ₹500", ₹217–855 | Knowledge base: MRP ₹1,067; online ₹146–960 | "about ₹200–₹1,000" |
| Languages | Plans: "10 Indian languages" | 11 for the voice coach; 12 listed for phone agents; 22 claimed platform-wide | "11" |
| InSee accuracy | Plans: 97% (company press release) | FDA summary: 100% agreement, 30 subjects | FDA figure |
| Sarvam phone-call price | Round 2: not published | Imported report: ₹3.50 a minute (launch page) | ₹3.50, "launch price" |
| Parts cost per unit | ₹1,000–1,700 (F-BIZ-7); J11 "a few hundred rupees" | ₹1,400–2,600 (Plan §3) | Give the range and say "our estimate" |
| Reuse per unit | 10+ patients | 20 patients | Say which you assume |
| Cost of one AI summary | ≈ ₹0.9 (Plan) | ≈ ₹0.56 (architecture note) | Either, labelled estimate |
| WhatsApp cost per patient | ₹1.6 a day for 14 reminders | ₹5 per 14 days; ₹10 a month | Depends on message count |
| TB survivors a year | 23 lakh (round 5, incl. TB outside the lungs) | Under 19 lakh (round 6); 16–17 lakh (round 7) | Round 7 |
| TB notified, 2024 | 26.07 lakh (PIB, all notified) | 24.99 lakh (WHO, new + relapse) | Different counts; say which |
| "No TB guideline names the spirometer" | F-VIS-2, F-VIS-4 caveat | RBIPMT 2024 does (F-VIS-5) | F-VIS-5 |
| "No Indian readmission figure" | F-BIZ-8 | 4.7% abdominal (F-BIZ-10) | F-BIZ-10 |
| Kilkari reach | 99.5% by the 9th call | About 23% never reached after 9 attempts | Quote neither as "the" rate |
| Older Indians with a smartphone | 41% (HelpAge, national, B) | 19.5% rural / 36.5% urban (Telangana, 45+, A); 65% in one city (snippet) | Give source with each |
| Nurses per 1,000 | 2.20 (March 2025) | 2.60 (July 2026) | 2.60 |
| Indian complication rate | 2.9% (Udaipur) | 34% (JIPMER); plans: 3–30%, Apollo 9.4% | Quote with setting |
| Breath-hold time | 3–5 s (MedlinePlus) | at least 5 s (Cleveland Clinic) | 3 s default; nurse can raise it |
| Quiet hours | 9 pm–7 am | 10 pm–8 am (Plan) | 9 pm–7 am is what's built |
| SMS registration fee | About ₹5,900 | Free | Unconfirmed |
| Beam vs tube | Team geometry: tube 5–7 cm, narrowed beam ≈ 4 cm at 15 cm | Derived drawing: bore ≈ 44 mm, beam 42.9 mm at the top | Measure it |
| Sensor library | Plans: SparkFun | Hardware guide and firmware: Pololu | Pololu |
| Sensor datasheet | Research used Rev 3 (2018) | 3D sources used Rev 8 (2024); its own tables disagree on chip length (4.9 vs 4.4 mm) | Minor |
| Duplicate finding IDs | F-VOICE-7–9, F-COMP-7 (round 2) | Same IDs in the imported section | Add "(imported)" |

---

## 12. Source list

Numbers match `docs/research/SOURCES_LEDGER.md`. Rows that begin "Search snippets only" were **not opened**. Rows #9–#14 and #29 came from the earlier plans, and #191–#206 from the architecture note (mostly search results); the research agent did not re-read them. Two WaBI rows are deliberately described without their location because they are private.

| # | Source | Address or locator | Grade |
|---|---|---|---|
| 2 | Eltorai et al. 2019, full text (JAMA Surgery via PMC) | https://pmc.ncbi.nlm.nih.gov/articles/PMC6583822 | A |
| 3 | FDA 510(k) clearance letter + summary, InSee (US FDA) | https://www.accessdata.fda.gov/cdrh_docs/pdf24/K241152.pdf | A |
| 5 | Penn digital IS adherence trial (ClinicalTrials.gov) | https://clinicaltrials.gov/study/NCT06629454 | A |
| 6 | Moosvi et al., "Digital IS improves adherence and might decrease LOS" (AATS meeting abstract) | https://www.aats.org/resources/abstract.pdf?abstract=3136448 | B |
| 7 | Romsons Breazer 2500 product page (Medikabazaar (retailer)) | https://www.medikabazaar.com/products/romsons-breazer-2500-volumetric-lung-exerciser-mbpgmrsmmssrre15739 | C |
| 8 | Romsons exerciser brand page (Medikabazaar (retailer)) | https://www.medikabazaar.com/physiotherapy-rehabilitation-medical-aids/physiotherapy-rehabilitation/exerciser/brand-20282.html | C |
| 9 | Indian PPC study (Int J Surgery (India)) | https://www.ijsurgery.com/index.php/isj/article/view/2439 | A |
| 10 | Indian PPC study (DOAJ record) | https://doaj.org/article/8ce7474ddd114cdbb332bb5c0d16b782 | A |
| 11 | Indian PPC study (PMC) | https://pmc.ncbi.nlm.nih.gov/articles/PMC12535847/ | A |
| 12 | PPC hospital costs, Australia/NZ (World Physiotherapy congress abstract) | https://world.physio/congress-proceeding/impact-postoperative-pulmonary-complications-hospital-costs-and-length-stay | B |
| 14 | ST AN5231 cover glass (ST app note) | https://www.st.com/resource/en/application_note/an5231-cover-glass-guidelines-for-the-singlezone-timeofflight-sensor-stmicroelectronics.pdf | B |
| 29 | Twilio WhatsApp sandbox (Twilio docs) | https://www.twilio.com/docs/whatsapp/sandbox | B |
| 31 | FDA 510(k) database entry K241152 (US FDA) | https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K241152 | A |
| 33 | Romsons SH 6082 Respirometer (3-ball) (Truemeds (retailer)) | https://www.truemeds.in/otc/romsons-sh-6082-respirometer-1-tm-cram1-000444 | C |
| 34 | Airalux Digital Incentive Spirometer study listing (Penn Medicine) | https://clinicalresearch.pennmedicine.org/us/en/listing/8389/airalux-digital-incentive-spirometer | B |
| 35 | LAS VEGAS, 29-country observational study (Eur J Anaesthesiol 2017) (Eur J Anaesthesiol via PMC) | https://pmc.ncbi.nlm.nih.gov/articles/PMC5502122 | A |
| 36 | Canet et al., ARISCAT (Anesthesiology 2010) (Anesthesiology (author PDF)) | https://hospitaldelmar.cat/media/upload_web/pdf/article_Anesthesiology_editora_46_3389_1.pdf | A |
| 39 | do Nascimento Junior et al., Cochrane 2014 (abstract) (Cochrane via Europe PMC) | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:24510642%20AND%20SRC:MED&resultType=core&format=json | A |
| 42 | Restrepo et al., "Incentive spirometry: 2011" AARC CPG (abstract) (Respiratory Care via Europe PMC) | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.4187/respcare.01471&resultType=core&format=json | A |
| 44 | Using an incentive spirometer (reviewed 19 Oct 2025) (MedlinePlus, US NLM) | https://medlineplus.gov/ency/patientinstructions/000451.htm | B |
| 45 | Incentive spirometer (updated 26 May 2026) (Cleveland Clinic) | https://my.clevelandclinic.org/health/articles/4302-incentive-spirometer | B |
| 47 | IS compliance before major cancer surgery, Hyderabad (Anesth Essays Res 2018) (Anesth Essays Res via PMC) | https://pmc.ncbi.nlm.nih.gov/articles/PMC6020596 | A |
| 48 | Eltorai et al. 2018, IS adherence national provider survey (abstract) (Respiratory Care via Europe PMC) | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.4187/respcare.05882&resultType=core&format=json | A |
| 50 | Burns et al. 2023, data capture device for clinical IS (abstract) (JMIR Biomed Eng via Europe PMC) | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.2196/46653&resultType=core&format=json | A |
| 52 | Soh et al. 2019, Go-breath app RCT, Korea (abstract) (JMIR mHealth uHealth via Europe PMC) | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.2196/12204&resultType=core&format=json | A |
| 53 | Sarvam API Pricing (via Jina Reader) (Sarvam AI official page) | https://www.sarvam.ai/api-pricing | B |
| 54 | Bulbul model page (v4 Flash, v3) (Sarvam docs) | https://docs.sarvam.ai/api/getting-started/models/bulbul.md | B |
| 55 | Credits & Rate Limits (₹100 free credits) (Sarvam docs) | https://docs.sarvam.ai/api/getting-started/ratelimits.md | B |
| 56 | Commercial Licensing (Sarvam docs) | https://docs.sarvam.ai/api/getting-started/commercial-licensing.md | B |
| 60 | India: Voice Guidelines (page dated 8 Oct 2026) (Twilio official) | https://www.twilio.com/en-us/guidelines/in/voice | B |
| 61 | WhatsApp Business Platform pricing (effective 1 Oct 2026) (Meta for Developers) | https://developers.facebook.com/docs/whatsapp/pricing | B |
| 62 | WhatsApp INR rate card (xlsx), effective 1 Oct 2026 (Meta) | https://scontent-atl3-1.xx.fbcdn.net/v/t39.8562-6/830985615_1819783359150737_3237041219299440415_n.csv (linked from #61 as "INR list rates") | B |
| 63 | Population-level surgical rates and unmet need in India 2011–2019 (HMIS), Int J Surg 2024;110:1884 (Int J Surg via PMC (WebFetch hit limit; read via Jina Reader)) | https://pmc.ncbi.nlm.nih.gov/articles/PMC10942208 | A |
| 64 | India's internet revolution: IAMAI–Kantar Internet in India 2024 (Jina) (Business Today) | https://www.businesstoday.in/amp/technology/news/story/indias-internet-revolution-key-insights-from-kantar-and-iamai-report-461043-2025-01-16 | B |
| 65 | 88% seniors offline, HelpAge report (14 Jun 2025) (Jina) (Deccan Herald) | https://www.deccanherald.com/india/karnataka/bengaluru/88-seniors-offline-helpage-urges-action-3585484 | B |
| 66 | Lok Sabha unstarred Q 4811 (nurse ratio), Mar 2025 (Parliament of India) – timed out, nothing read | https://eparlib.sansad.in/bitstream/123456789/3015026/1/AU4811_PZ1pou.pdf | A |
| 67 | Nurse ratio 2.60/1,000, Rajya Sabha reply 21 Jul 2026 (Jina) (The South First) | https://thesouthfirst.com/health/south-india-leads-indias-nursing-workforce-as-national-ratio-remains-below-who-benchmark/ | B |
| 69 | Census 2011 language data (Jina) (Factly) | https://factly.in/a-major-dravidian-language-is-now-the-mother-tongue-of-only-18-9-indians-down-from-23-in-1971 | B |
| 70 | TRAI clarifies 1600 and 140 series (10 Jul 2026 press note) (Jina) (SCC Online (legal news)) | https://www.scconline.com/blog/post/2026/07/18/trai-clarifies-1600-and-140-series-number-framework/ | B |
| 71 | India Calling Regulations (TCCCPR Third Amendment 2026 summary) (Plivo docs) | https://www.plivo.com/docs/voice/concepts/india-calling.md | B |
| 74 | Twilio trial account: restrictions (Jina) (Twilio docs) | https://www.twilio.com/docs/usage/trials | B |
| 75 | Saaras model page (Sarvam docs) | https://docs.sarvam.ai/api/getting-started/models/saaras.md | B |
| 78 | Sarvam Terms of Service (effective 29 Jul 2026) (Jina) (Sarvam AI) | https://www.sarvam.ai/terms-of-service | B |
| 79 | AI4Bharat Indic-TTS repo + README (gh api) (GitHub / AI4Bharat (IIT Madras)) | https://github.com/AI4Bharat/Indic-TTS | B |
| 80 | Liang et al. 2024, IS in perioperative lung cancer, SR/MA (abstract); alias PMC10870616 (BMC Pulm Med via Europe PMC) | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=PMCID:PMC10870616&resultType=core&format=json | A |
| 81 | Silva et al. 2024, IS vs standard care after cardiac surgery, SR/MA (abstract); alias PMC11020284 (Braz J Cardiovasc Surg via Europe PMC) | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=PMCID:PMC11020284&resultType=core&format=json | A |
| 82 | Sinouvassan et al., PPC risk factors after GI surgery, JIPMER, Int Surg J 2020;7:93-7 (Int Surg J) | https://www.ijsurgery.com/index.php/isj/article/download/4636/3454/20290 | A |
| 83 | Post-operative pulmonary complications study (Udaipur), Int Surg J 2018;5:3057-65 (Int Surg J) | https://www.ijsurgery.com/index.php/isj/article/download/3176/2303/11735 | A |
| 85 | Twilio Sandbox for WhatsApp (Jina), RE-OPEN of #29 to fact-check the plan (Twilio docs) | https://www.twilio.com/docs/whatsapp/sandbox | B |
| 86 | US10610129B1, portable monitoring of incentive spirometry (Tidal Medical) (Jina) (Google Patents) | https://patents.google.com/patent/US10610129B1/en | A |
| 87 | US7998085, IS with simulated humanlike voices (Google Patents) – page failed to load, title seen in search only | https://patents.google.com/patent/US7998085B1/en | A |
| 88 | Infrared device helps monitor COVID-19 patients' breathing therapy (InSee interview, 16 Jun 2020) (Jina) (IEEE Spectrum) | https://spectrum.ieee.org/infrared-device-helps-monitor-covid19-patients-breathing-therapy | B |
| 89 | Kumar et al. 2016, flow vs volume IS RCT, Mangalore (abstract); alias PMC4740618 (J Clin Diagn Res via Europe PMC) | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.7860/JCDR/2016/16164.7064&resultType=core&format=json | A |
| 90 | 2 crore PM-JAY admissions, top specialities (19 Aug 2021) (Jina) (The Tribune) | https://www.tribuneindia.com/news/nation/indian-poor-seek-2-crore-hospital-admissions-under-ayushman-bharat-most-in-general-medicine-general-surgery-299041 | B |
| 91 | Top PM-JAY procedures, Lok Sabha reply (27 Jul 2019) (Jina) (The Quint) | https://www.thequint.com/fit/medical-procedures-performed-under-ayushman-bharat | B |
| 92 | YouTube search results (yt-dlp): ids 5IuWF1LMxo4, Tbhgs0QSbi0, JIg5vKN6MXU, Nog8S8u4m5Q, je0w0Elt0dI, 5tyE16Z7pys (YouTube) | ytsearch6:incentive spirometer kaise use kare hindi | C |
| 94 | Voice Agent call transfer providers, destination and testing limits (Sarvam docs) | https://docs.sarvam.ai/conversations/build/tools/call-transfer | B |
| 97 | Voice runtime, DTMF status and scale claims (Sarvam docs) | https://docs.sarvam.ai/conversations/build/run-time | B |
| 99 | Voice Agents general availability and ₹3.50/min launch price (Sarvam official site) | https://www.sarvam.ai/epoch/summary | B |
| 101 | FDA database entry for InSee K241152, decision 21 Aug 2025 (US FDA) | https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K241152 | A |
| 102 | InSee capabilities and free hospital trial form; no public price (Tidal Medical / manufacturer) | https://www.breathe-insee.com/ | B |
| 103 | InSee sensor, stored/displayed data and reminder workflow (Tidal Medical / manufacturer) | https://www.breathe-insee.com/care-provider | B |
| 104 | Call Analytics product page: transcript-derived sentiment and structured reports (Sarvam official site) | https://www.sarvam.ai/call-analytics | B |
| 105 | Batch transcription, diarisation and LLM sentiment-analysis workflow (Sarvam docs) | https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline | B |
| 106 | TCCCPR (Third Amendment) Regulations 2026, full text (Jina returned empty; read by direct download + pdftotext, scanned/OCR) (TRAI (regulator)) | https://www.trai.gov.in/sites/default/files/2026-09/Regulation_18092026.pdf | A |
| 107 | WhatsApp pricing: Twilio $0.005/msg fee + Meta pass-through (Jina) (Twilio official) | https://www.twilio.com/en-us/whatsapp/pricing | B |
| 108 | DLT registration guide (Jio/Airtel/ViLPower; headers; templates) (Jina) (Exotel docs) | https://developer.exotel.com/docs/sms-support/dlt-guide | B |
| 109 | India Voice API pricing (₹0.38/min, ₹200/month number) (Jina) (Plivo official) | https://www.plivo.com/voice/pricing/in/ | B |
| 110 | India calling compliance: eligibility, KYC, media anchoring, number series (Jina). Same TCCCPR summary as #71 (near-alias) (Plivo support) | https://support.plivo.com/hc/en-us/articles/45875255505305-Requirements-for-Sending-SMS-and-Calls-to-India | B |
| 111 | KYC verification: documents, 1–3 business days (Jina) (Exotel docs) | https://developer.exotel.com/docs/getting-started/kyc-verification | B |
| 113 | Indian TKA cohorts (J ISAKOS 2026; J Exp Orthop 2026) (Europe PMC) | Europe PMC search: "total knee arthroplasty" India "mean age" female 2019–2026 (hits PMID 41651067, 41560970) | A |
| 114 | Robotic CABG, Indian experience, IJTCVS 2024 (Europe PMC) | Europe PMC search: TITLE "coronary artery bypass" + India + "mean age" 2017–2026 (hit PMID 38125327) | A |
| 115 | Indian cholecystectomy and post-TB cohorts (Europe PMC) | Europe PMC searches: cholecystectomy India "mean age" (PMIDs 42630774, 41059748, 41243490, 41623756); post-TB lung disease India (PMID 42031463) | A |
| 116 | Sinha et al. 2025, multicentre PR for post-TB lung disease, IJMR (abstract); PMC12550408 (Indian J Med Res via Europe PMC) | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40844105%20AND%20SRC:MED&resultType=core&format=json | A |
| 117 | LASI Wave 1, India factsheet, elderly 60+ (pdftotext) (IIPS / MoHFW (official survey)) | https://www.iipsindia.ac.in/sites/default/files/other_files/LASI_W1_Elderly_India.pdf | A |
| 118 | ST VL53L1X datasheet DocID031281 Rev 3 (Nov 2018), mirror; alias of st.com/resource/en/datasheet/vl53l1x.pdf (#134, failed) (ST via Pololu) | https://www.pololu.com/file/0J1506/vl53l1x.pdf | B |
| 119 | GitHub hobby/study IS projects (GitHub) | gh search repos "incentive spirometer" (+ READMEs of d-eniz/incentive-spirometer-voice, shaoyuancc/spiro-android, malikzt/IntelligentIncentiveSpirometer) | C |
| 120 | Camera/digital IS studies (Turkey 2025, Thailand 2025/2026, Colombia 2025) (Europe PMC) | Europe PMC search "incentive spirometer" camera/smartphone/sensor 2019–2026 + abstracts PMIDs 41228060, 40327873, 42505437, 41214067 | A |
| 122 | Digital Personal Data Protection Rules, 2025, G.S.R. 846(E), gazette text (MeitY (official)) | https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf | A |
| 123 | Decoding CDSCO MDSW guidance (21 Jul 2026, CDSCO/MD/GD/MDSW/01/2026) (Jina) (Nishith Desai Associates (law firm)) | https://nishithdesai.com/research-and-articles/hotline/pharma-healthcare-update/from-code-to-compliance-decoding-indias-medical-device-software-guidance-15623 | B |
| 124 | CDSCO respiratory device classes (copy of notifications) (Jina) (Morulaa (consultancy)) | https://morulaa.com/knowledge-hub/regulations/india/cdsco-medical-device-classification-respiratory-equipment | B |
| 125 | CDSCO anaesthesiology device classes (Jina) (Morulaa (consultancy)) | https://morulaa.com/knowledge-hub/regulations/india/cdsco-medical-device-classification-anesthesiology | B |
| 126 | Bulbul v3 best practices: pace, temperature, speakers by language, transport (Sarvam docs) | https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/bulbul-v3-best-practices.md | B |
| 128 | HBP 2022 rate list (AB PM-JAY packages, adopted by Nagaland CMHIS) (Nagaland State Health Agency (govt)) | https://cmhis.nagaland.gov.in/storage/pageFiles/381.pdf | A |
| 129 | Incidence and attributable costs of VAP, north Indian ICU, J Infect Public Health 2015 (abstract) (Europe PMC) | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:25444392%20AND%20SRC:MED&resultType=core&format=json | A |
| 130 | Manipal Hospitals + ConnectedLife post-surgery monitoring (Mar 2022) (Jina) (Healthcare IT News) | https://www.healthcareitnews.com/news/asia/manipal-hospitals-partners-connectedlife-post-surgery-monitoring | B |
| 132 | Tidal PCT, "Systems and methods for monitoring of incentive spirometry" (status Ceased) (Jina) (Google Patents) | https://patents.google.com/patent/WO2022204480A1/en | A |
| 133 | Respira Health: WhatsApp pulmonary rehab pilot, India (Jina) (EA Forum (founders' post)) | https://forum.effectivealtruism.org/posts/D59GPfsNWHDayPe2c/piloting-a-digital-treatment-for-copd-the-second-biggest | C |
| 135 | CDSCO Guidance Document on Medical Device Software, CDSCO/MD/GD/MDSW/01/2026 (curl + pdftotext) (CDSCO (regulator)) | https://www.cdsco.gov.in/opencms/export/sites/CDSCO_WEB/Pdf-documents/Guidance-document-on-Medical-Device-Software-under-MDR-2017.pdf | A |
| 136 | "VL53L1X in a tube.. Tips and tricks?" forum thread (Jina); alias community.st.com/t5/imaging-sensors/vl53l1x-in-a-tube-tips-and-tricks/m-p/137857 (ST Community forum) | https://community.st.com/imaging-sensors-49/vl53l1x-in-a-tube-tips-and-tricks-20936 | C |
| 137 | YouTube search results (YouTube) | yt-dlp ytsearch8 "Romsons Breazer 2500" (titles only: mcpwkMKiUdU, G0wj9IYKxZQ, 0bqgZUEcf2k, U4066fKRIs8 …) | C |
| 138 | Breazer supplier listing (Jina) (B2B listing) | https://www.indianbusinessportal.in/products/breazer-volumetric-respiratory-exerciser | C |
| 139 | TRAI Press Release 119/2026, TCCCPR Third Amendment salient features, 18 Sep 2026 (curl + pdftotext) (TRAI (regulator)) | https://www.trai.gov.in/sites/default/files/2026-09/PR_No119of2026.pdf | A |
| 140 | Exotel comments on draft Third Amendment (Apr 2026) (Exotel via TRAI) | https://www.trai.gov.in/sites/default/files/2026-04/Exotel_TRAI_TCCCPR_Comments_v2.pdf | B |
| 141 | CHSI cost function for PM-JAY payment weights, BMJ Open 2023 (Europe PMC / BMJ Open) | Europe PMC search ABSTRACT "2307" "bed-day" India → PMID 37857541 (doi 10.1136/bmjopen-2023-076155) | A |
| 142 | VAP cost at PGIMER trauma ICU, Lung India 2024 (Europe PMC / Lung India) | Europe PMC search ICU "bed day" India cost trauma 2016–2026 → PMID 38953191 | A |
| 144 | Zorgers + Clinitouch home RPM for COPD (updated 29 Nov 2024) (Jina) (Digital Health News) | https://www.digitalhealthnews.com/how-uk-s-clinitouch-plans-to-disrupt-india-s-rpm-offerings-with-mohali-based-healthtech-startup-zorgers | B |
| 145 | Home health monitoring in Bengaluru (news reprint, 28 Sep 2023) (Jina) (Tricog site (news reprint)) | https://tricog.com/news/home-health-monitoring-services-in-bengaluru/ | C |
| 146 | Clinical Standards for assessment, management and rehabilitation of Post-TB Lung Disease (Annexure 2) (Jina) (NTEP / MoHFW) | https://ntep.in/node/6657 | A |
| 147 | PR needs survey, Pune, Chron Respir Dis 2024 (Europe PMC) | Europe PMC search "pulmonary rehabilitation" Pune survey 2022–2026 → PMID 39075037 (alias figshare.le.ac.uk 26426476) | A |
| 149 | various (retail / news / forum) | Search snippets only, NOT opened: probots.co.in VL53L1X (₹399–₹859) and ESP32-C3 (₹299) listings; medicaldialogues Apollo Homecare launch (₹2,000–3,600/day); medianama 2018 Portea home ICU (₹6,500–12,000/day); ST/SparkFun/Pololu forum posts on ROI 4x4 ≈ 15° FoV; 21 CFR 868.5690 (US IS = Class II); ntep.in/node/6610 (RBIPMT PR guidance July 2024) | C |
| 150 | Risk classification list of Class A (non-sterile and non-measuring) medical devices, F. No. MED-16014(12)/1/2024-eoffice-Part(2) (curl + pdftotext) (CDSCO (regulator)) | https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadPublic_NoticesFiles/Risk%20based%20classification%20list%20of%20Class%20A(non-sterile%20and%20non-measuring)%20medical%20device.pdf | A |
| 152 | 30-day readmissions after CABG: systematic review and meta-analysis, J Cardiothorac Surg 2021 (Europe PMC) | Europe PMC PMID 34112216 (doi 10.1186/s13019-021-01556-1; alias PMC8194115, link.springer.com/10.1186/s13019-021-01556-1) | A |
| 153 | Readmission rate after TKA, Fortis Ludhiana, World J Orthop 2024 (Europe PMC) | Europe PMC PMID 39165878 (doi 10.5312/wjo.v15.i8.713) | A |
| 154 | Smart CABGuard nurse-led LLM chatbot RCT protocol, Amrita Kochi, JMIR Res Protoc 2026 (Europe PMC) | Europe PMC PMID 42550966 (doi 10.2196/103717; alias researchprotocols.org/2026/1/e103717) | A |
| 155 | Max@Home nursing care at home cost, Delhi (Jina) (Max Healthcare (company)) | https://www.maxathome.in/cost/service/nursing-care-at-home/delhi | B |
| 156 | Portea physiotherapy at home, Bangalore (Jina) (Portea (company)) | https://www.portea.com/physiotherapy/bangalore/ | B |
| 157 | Practice of incentive spirometer among postoperative patients, Chennai, J Pharm Bioallied Sci 2024 (Europe PMC) | Europe PMC PMID 39346353 (doi 10.4103/jpbs.jpbs_565_24) | A |
| 158 | Cancer Caregiver Support System pilot RCT, Tata Memorial Muzaffarpur, Indian J Cancer 2026 (Europe PMC) | Europe PMC PMID 42301659 (doi 10.4103/ijc.ijc_109_25) | A |
| 159 | Digital adherence technologies in TB: systematic review, BMC Infect Dis 2025 (Europe PMC) | Europe PMC PMID 41087928 (doi 10.1186/s12879-025-11503-3) | A |
| 160 | various (company / directory / news / government) | Search snippets only, NOT opened: lp.portea.com/portea-avisa-jan22 (attendants ₹1,800–3,200); portea.com/physiotherapy/bangalore metadata "₹499"; care.samarth.community home nursing cost Chennai/Delhi 2026; medicaldialogues.in Class A list news (3 Nov 2025); pib.gov.in PRID 2189415 (Nov 2025, 26.18 lakh diagnosed 2024) and "25.5 / 26.07 lakh notified" statement; CDSCO dispatch 2may22.pdf (Romsons "NIL LETTER") | C |
| 161 | India Speeding Towards TB Elimination, 24 Mar 2026 (curl + pdftotext) (PIB / Government of India) | https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/mar/doc2026324833001.pdf | A |
| 162 | Lung function impairment at TB treatment completion, Madurai, Cureus 2026 (Europe PMC) | Europe PMC PMID 41873289 (doi 10.7759/cureus.103941) | A |
| 163 | Spectrum of lung disorders in TB survivors, Mullana, Indian J Tuberc 2025 (Europe PMC) | Europe PMC PMID 42031463 (doi 10.1016/j.ijtb.2025.08.009) | A |
| 164 | Virtual Baithak IVR RCT protocol for older adults, PGIMER, BMJ Open 2026 (Europe PMC) | Europe PMC PMID 41922061 (doi 10.1136/bmjopen-2025-103354) | A |
| 165 | E.M.M.A WhatsApp AI health coach pilot (UK), Indian J Ophthalmol 2026 (Europe PMC) | Europe PMC PMID 41884918 (doi 10.4103/ijo.ijo_2205_25) | A |
| 168 | Readmissions following pancreaticoduodenectomy, SGPGIMS Lucknow, Cureus 2024 (Europe PMC) | Europe PMC PMID 39176340 (doi 10.7759/cureus.65140; alias PMC11338694) | A |
| 169 | Recidivism (ICU readmission) after cardiac surgery, CMC Vellore, Ann Card Anaesth 2024 (Europe PMC) | Europe PMC PMID 39365131 (doi 10.4103/aca.aca_68_24; alias PMC11610776) | A |
| 170 | I-INFUSE: intraoperative fluids in major GI cancer surgery, 30 Indian centres, Indian J Anaesth 2026 (Europe PMC) | Europe PMC PMID 41788757 (doi 10.4103/ija.ija_1190_25; full text via europepmc REST PMC12959532/fullTextXML) | A |
| 171 | Smartphone/social-media pulmonary rehab for COPD, Thar Desert (Jodhpur), Lung India 2025 (Europe PMC) | Europe PMC PMID 40296389 (doi 10.4103/lungindia.lungindia_455_24) | A |
| 173 | Assessing exposure to Kilkari: call data across 13 states, BMJ Glob Health 2021 (Europe PMC) | Europe PMC PMID 34312148 (doi 10.1136/bmjgh-2021-005213; alias PMC8327807) | A |
| 174 | Kilkari RCT, Madhya Pradesh, BMJ Glob Health 2022 (Europe PMC) | Europe PMC PMID 35835477 (doi 10.1136/bmjgh-2022-008838; alias PMC9288869) | A |
| 175 | LASI Wave 1 (2017–18) India Report, full report (curl + pdftotext; Table 4.16 text, Table 11.9) – different document from the factsheet in #117 (IIPS / MoHFW (official survey)) | https://www.iipsindia.ac.in/sites/default/files/LASI_India_Report_2020_compressed.pdf | A |
| 176 | Guidance Document on Pulmonary Rehabilitation for People affected with TB, RBIPMT Delhi, July 2024 [marked Draft] (NTEP / RBIPMT (government)) | https://ntep.in/node/6610 (+ full book via https://ntep.in/book/export/html/6610, Jina) | A |
| 177 | WHO Global TB Report 2025, 2.1 Case notifications (WebFetch) (WHO) | https://www.who.int/teams/global-programme-on-tuberculosis-and-lung-health/tb-reports/global-tuberculosis-report-2025/tb-diagnosis-and-treatment/2-1-case-notifications | A |
| 178 | Apollo HomeCare physiotherapy at home (Jina) (Apollo HomeCare (company)) | https://www.apollohomecare.com/physiotherapy-at-home | B |
| 179 | various (aggregator / Q&A / WHO / journals) | Search snippets only, NOT opened: Delhi home-physio aggregator page (₹700–2,000 per visit, no provider, no date); careers360 Q&A (₹300–500 per clinic session, 2022); WHO GTB 2024 table (SEAR extrapulmonary 20% in 2023); PMC12182644 Datia/Tikamgarh (MP) Nikshay EPTB 11.3%→13.8%; PMC7740952 / PMC8938771 (older adults' smartphone training, DAHLIA rural Karnataka: 50% own a mobile phone, n=150) | C |
| 180 | Isolated CABG in septuagenarians (618 CABG, Indian centre), IJTCVS 2024 (Europe PMC) | Europe PMC PMID 39416327 (doi 10.1007/s12055-024-01767-w; full text PMC11473761 grepped) | A |
| 181 | COHOS: hybrid revascularisation vs CABG, Indian Heart J 2025 (Europe PMC) | Europe PMC PMID 40054580 (doi 10.1016/j.ihj.2025.03.002; full text PMC12138072 grepped) | A |
| 183 | Medical Devices Rules 2017 (consolidated, 211 pages), First Schedule Part I + rule 2 definitions (curl + pdftotext) (CDSCO / MoHFW (primary law)) | https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2022/m_device/Medical%20Devices%20Rules%2C%202017.pdf | A |
| 184 | Digital health literacy among ageing adults (45+), rural vs urban Telangana, MJAFI 2024 (Europe PMC) | Europe PMC PMID 38799990 (doi 10.1016/j.mjafi.2023.09.006; alias PMC11117001) | A |
| 186 | Analyzing and Predicting Low-Listenership Trends in a Large-Scale Mobile Health Program (Kilkari, with ARMMAN), arXiv 2023 (arXiv preprint (Google Research / ARMMAN collaboration)) | https://arxiv.org/pdf/2311.07139 (via Jina; alias ar5iv.labs.arxiv.org/html/2311.07139) | B |
| 187 | WHO Global TB Programme notifications dataset (CSV), India rows 2019–2024 (WHO (official data)) | https://extranet.who.int/tme/generateCSV.asp?ds=notifications | A |
| 188 | Early and midterm outcomes after off-pump CABG, Amrita Kochi, IJTCVS 2023 (Europe PMC) | Europe PMC PMID 37346442 (doi 10.1007/s12055-023-01475-x; alias PMC10279599) | A |
| 189 | Extubation in OR after on-pump CABG, Aachen (Germany), IJTCVS 2025 (Europe PMC) | Europe PMC PMID 40535205 (doi 10.1007/s12055-025-01908-9; alias PMC12170970) | A |
| 191 | Supabase pricing & PITR usage docs (Supabase (company docs)) | https://supabase.com/pricing ; https://supabase.com/docs/guides/platform/manage-your-usage/point-in-time-recovery | B |
| 192 | Supabase HIPAA / Team plan (Supabase (company docs)) | https://supabase.com/docs/guides/security/hipaa-compliance (+ supabase.com/pricing, alias of #191) | B |
| 193 | Render regions (no India region) (Render (company docs)) | https://render.com/docs/regions | B |
| 194 | CERT-In Directions 28 Apr 2022 (6-hour reporting, 180-day logs in India) (CERT-In / MeitY (government)) | https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf (+ FAQs) | A |
| 195 | Supabase TimescaleDB deprecation / pg_partman guide (Supabase (company docs)) | https://supabase.com/docs/guides/database/extensions/timescaledb ; https://supabase.com/docs/guides/database/migrating-to-pg-partman | B |
| 196 | Digital Personal Data Protection Act 2023, text (ss. 11–13 rights, s. 16 transfers) (MeitY (primary law)) | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf | A |
| 197 | Supabase regions (Mumbai ap-south-1) (Supabase (company docs)) | https://supabase.com/docs/guides/platform/regions | B |
| 198 | Claude API pricing (Opus 5.5, Haiku 5.5, Batch 50% off) (Anthropic (company docs)) | https://platform.claude.com/docs/en/about-claude/pricing | B |
| 199 | ABDM FHIR Implementation Guide v6.5.0 (NRCeS / ABDM (government standard)) | https://www.nrces.in/ndhm/fhir/r4/index.html | A |
| 200 | ABDM sandbox forum (M1/M2/M3) + NHA DHIS operational guidelines (ABDM forum (C) / NHA (A)) | https://devforum.abdm.gov.in/t/regarding-m1-m2-m3-testcases/7525 ; https://abdm.gov.in/static/media/OperationalGuidelinesDHIS.a35651cdf843e0b399c2.pdf | A/C |
| 201 | ESP-IDF Secure Boot v2 and OTA docs (ESP32-C3) (Espressif (company docs)) | https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/security/secure-boot-v2.html ; .../api-reference/system/ota.html | B |
| 202 | ISO 14971:2019, ISO 13485, IEC 62304, IEC 62366-1 catalogue pages (ISO (standards body)) | https://www.iso.org/standard/72704.html ; https://www.iso.org/iso-13485-medical-devices.html ; https://www.iso.org/standard/38421.html ; https://www.iso.org/standard/63179.html | B |
| 203 | FDA roundup 3 Dec 2024 (final PCCP guidance) (US FDA) | https://www.fda.gov/news-events/press-announcements/fda-roundup-december-3-2024 | A |
| 204 | WhatsApp messaging limits (2k/10k/100k/unlimited, 80 msg/s) and templates overview (Meta for Developers) | https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits ; .../templates/overview | B |
| 205 | CERT-In empanelled IT security auditing organisations (CERT-In (government)) | https://www.cert-in.org.in/PDF/Empanel_org.pdf | A |
| 206 | Supabase compute sizes and prices (Supabase (company docs)) | https://supabase.com/docs/guides/platform/manage-your-usage/compute | B |
| 207 | WhatsApp Business Messaging Policy (Jina; no date on page; Meta's opt-in doc refers to a Nov 2024 update) (WhatsApp / Meta (official policy)) | https://business.whatsapp.com/policy | B |
| 209 | Template categorization (utility / marketing / authentication rules, re-categorisation, penalties) (Meta for Developers) | https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization.md (curl) | B |
| 210 | Cloud API Data Privacy & Security (Meta for Developers) | https://developers.facebook.com/documentation/business-messaging/whatsapp/data-privacy-and-security.md (curl; alias developers.secure.facebook.com/docs/whatsapp/cloud-api/overview/data-privacy-and-security) | B |
| 211 | Cloud API Local storage (data-at-rest in a chosen country) (Meta for Developers) | https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage.md (curl) | B |
| 212 | Business phone number registration (data_localization_region list incl. India "IN") (Meta for Developers) | https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/registration.md (curl) | B |
| 213 | Get opt-in for WhatsApp (Meta for Developers) | https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in.md (curl) | B |
| 214 | Telemedicine Practice Guidelines 2020 (MoHFW copy) (MoHFW) | https://covid19dashboard.mohfw.gov.in/pdf/Telemedicine.pdf (curl) | not graded (blocked; nothing read) |
| 215 | Telemedicine Practice Guidelines 2020 (copy) (nursing council site) | https://nmcn.in/oldsite/pdf/Telemedicine%20Practice%20Guidelines.pdf (curl) | not graded (blocked; nothing read) |
| 216 | Telemedicine Practice Guidelines 2020 (MoHFW) (MoHFW) | https://www.mohfw.gov.in/pdf/Telemedicine.pdf (Jina: empty; WebFetch: HTTP 403) | not graded (blocked; nothing read) |
| 217 | Telemedicine Practice Guidelines (Vikaspedia copy) (Vikaspedia (govt portal)) | https://en.vikaspedia.in/viewcontent/health/health-care-innovations/telemedicine-practice-guidelines?lgn=en (Jina) | not graded (blocked; nothing read) |
| 218 | Secondary summaries of the Telemedicine Practice Guidelines 2020; news reports on the MyGov Corona Helpdesk (law firms / news / vendors) | Search snippets only, NOT opened: TPG 2020 summaries naming WhatsApp/Facebook Messenger as allowed text tools (vikaspedia snippet, psalegal.com FAQ, mondaq.com, acuitylaw.co.in, ibanet.org); MyGov Corona Helpdesk on WhatsApp 2021 (businesstoday.in 24 Aug 2021, tribuneindia.com, etvbharat.com 9 Aug 2021, businessworld.in); third-party template guides (help.egrow.com, ycloud.com); Meta search snippet on Cloud API data privacy | B/C |
| 219 | Coyot AI home page, WaBI section (the team's own company) | https://coyot.ai | B |
| 221 | Coyot WaBI public app page, terms and privacy policy | public pages; address in the ledger | B |
| 222 | Coyot WaBI internal documentation and code (the team's own product; private, location not given here) | not public | B |
| 224 | WhatsApp Cloud API Get Started (test number, temporary token, test webhook) (Meta for Developers) | https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started.md (curl) | B |
| 225 | Service messages / Messages API (POST /<PHONE_NUMBER_ID>/messages, 24-hour window) (Meta for Developers) | https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages.md (curl) | B |
| 226 | WhatsApp webhooks overview (permissions, fields) (Meta for Developers) | https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview.md (curl) | B |
| 227 | Template review (decision can take up to 24 hours) (Meta for Developers) | https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review.md (curl) | B |
| 228 | Become a Tech Provider (business verification, then App Review) (Meta for Developers) | https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/get-started-for-tech-providers.md (curl) | B |
| 229 | Business phone numbers (test number auto-created; verification by SMS/voice; display name) (Meta for Developers) | https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers.md (curl) | B |
| 230 | Access tokens (System User vs Business Integration System User tokens) (Meta for Developers) | https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens.md (curl) | B |


### Sources outside the ledger (cited in other repo documents)
| Label | Source | Address | Where cited |
|---|---|---|---|
| 3D-1 | Romsons Breazer 2500 official product page (and its product images) | https://www.romsons.in/products/romsons-breazer-2500-volumetric-respiratory-exerciser | 3D_SOURCES B01, B13, B20 |
| 3D-2 | Amazon.in listing (box size, weight) | https://www.amazon.in/dp/B0BDVLW63J | 3D_SOURCES B02, B24 |
| 3D-3 | IndiaMART listing (Romsons Medsource) | https://www.indiamart.com/ms-romsons-medsource/respiratory-exerciser.html | 3D_SOURCES B02 |
| 3D-4 | FDA 510(k) K182847 summary (Voldyne, same device class; how the air moves) | https://fda.innolitics.com/submissions/AN/subpart-f%E2%80%94therapeutic-devices/BWF/K182847 | 3D_SOURCES B25 |
| 3D-5 | ST VL53L1X datasheet DS12385 Rev 8 | https://www.st.com/resource/en/datasheet/vl53l1x.pdf | 3D_SOURCES E04–E07 |
| 3D-6 | Pololu VL53L1X carrier board #3415 | https://www.pololu.com/product/3415 | 3D_SOURCES E08 |
| 3D-7 | Adafruit product pages: battery #1578, buzzer #160, LED #1612, button #367 | https://www.adafruit.com/product/1578 (and /160, /1612, /367) | 3D_SOURCES E09–E12 |
| HW-1 | Pololu VL53L1X and VL53L0X Arduino libraries | https://github.com/pololu/vl53l1x-arduino · https://github.com/pololu/vl53l0x-arduino | HARDWARE.md §10 |
| HW-2 | Espressif Arduino core (board pins) | https://raw.githubusercontent.com/espressif/arduino-esp32/master/variants/XIAO_ESP32C3/pins_arduino.h | HARDWARE.md §10 |
| V-1 | Sarvam API reference: text-to-speech, speech-to-text, translate, voices | https://docs.sarvam.ai/api-reference/text-to-speech/convert.md · https://docs.sarvam.ai/api-reference/speech-to-text/transcribe.md · https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices.md | VOICE.md §1 |
| C-1 | Sarvam Voice Agents call API and result format | https://docs.sarvam.ai/conversations/api/introduction · https://docs.sarvam.ai/conversations/api/instant-outbound/webhook-payload | COMMS.md §5.1 |
