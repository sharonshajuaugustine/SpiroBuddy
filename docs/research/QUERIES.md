# Search queries log

Every query run by the research agent, with date and usefulness, so no query is repeated.

## Round 1 plan (9 Oct 2026)
1. Claim check: Eltorai 2019 numbers, InSee FDA 510(k), Penn Airalux results, Romsons Breazer price.
2. CLIN: PPC size (incidence, mortality), Cochrane on IS, AARC technique.
3. ADH: real-world IS adherence; reminders/feedback evidence.
4. COMP: other smart/digital IS devices and apps; Indian competitors.
5. (Added mid-round by lead) VOICE: Sarvam AI docs, pricing, languages, voice agents. COMMS: Twilio India voice rules, WhatsApp India pricing.
6. INDIA: surgical volume (started).

## Queries
| date | channel | query | useful? |
|---|---|---|---|
| 2026-10-09 | WebSearch | Airalux digital incentive spirometer Penn Medicine | High: Penn listing names Airalux |
| 2026-10-09 | WebSearch | Romsons Breazer 2500 volumetric lung exerciser price | High: MRP ₹1,067, discount prices |
| 2026-10-09 | WebSearch | postoperative pulmonary complications incidence mortality LAS VEGAS study JAMA | Medium: found LAS VEGAS (not JAMA) |
| 2026-10-09 | WebSearch | ARISCAT Canet 2010 Anesthesiology postoperative pulmonary complications 30-day mortality 19.5% | High: found full-text PDF |
| 2026-10-09 | WebSearch | Cochrane review incentive spirometry prevention postoperative pulmonary complications upper abdominal surgery | High |
| 2026-10-09 | WebSearch | AARC clinical practice guideline incentive spirometry 2011 Restrepo Respiratory Care recommendations | High (recommendations); full text paywalled |
| 2026-10-09 | WebSearch | incentive spirometry technique slow inhalation breath hold 3 to 5 seconds 10 times every hour StatPearls | Medium: led to MedlinePlus / Cleveland Clinic |
| 2026-10-09 | WebSearch | incentive spirometry adherence observed postoperative patients percentage correct use study | High: Hyderabad study PMC6020596 |
| 2026-10-09 | WebSearch | Eltorai 2018 national survey respiratory therapists nurses incentive spirometry perspectives adherence poor 1,681 | High |
| 2026-10-09 | WebSearch | smart digital incentive spirometer Bluetooth app trial adherence 2023 2024 2025 | High: Michigan add-on, NCT03686631, TryBreath |
| 2026-10-09 | WebSearch | India startup smart incentive spirometer IoT lung exerciser app post-surgery | Medium: Go-breath RCT; no Indian product found |
| 2026-10-09 | WebSearch | India annual surgical volume number of surgeries per year per 100,000 population study | Medium: no national figure; HMIS paper PMC10942208 to read |
| 2026-10-09 | WebSearch | Twilio India outbound voice calls guidelines caller ID requirements international calls to Indian numbers | High: led to Twilio India page |
| 2026-10-09 | Jina Reader | sarvam.ai/api-pricing; docs.sarvam.ai TTS, Bulbul, ratelimits, licensing, llms.txt, Twilio guide, Voice Agents overview | High |
| 2026-10-09 | Jina Reader | twilio.com/en-us/guidelines/in/voice | High |
| 2026-10-09 | Jina Reader | developers.facebook.com/docs/whatsapp/pricing + INR rate card | High |
| 2026-10-09 | Jina Reader | pmc.ncbi.nlm.nih.gov/articles/PMC10942208 (HMIS surgical rates India) | High: 356 major surgeries per 100,000 in 2019 |

## Round 2 plan (9 Oct 2026)
1. INDIA: smartphone/WhatsApp use among older adults; nurse ratio; language census.
2. COMMS: TRAI TCCCPR for automated calls; Twilio trial + WhatsApp sandbox limits; Exotel/Plivo, Indian caller ID.
3. VOICE: Saaras; voice-agent price; Sarvam terms on health use; AI4Bharat/Bhashini.
4. CLIN: reviews 2015+; Indian PPC studies; India cost.
5. COMP: Indian smart IS / patents; InSee price. 6. Volume vs 3-ball in India. 7. INDLOC start (common surgeries).

| date | channel | query | useful? |
|---|---|---|---|
| 2026-10-09 | WebSearch | LASI India older adults 60+ smartphone ownership mobile phone use percentage | Low: no LASI figure |
| 2026-10-09 | WebSearch | IAMAI Kantar Internet in India 2024 report active internet users age 50+ rural urban | Medium: totals and Indic preference, no age split |
| 2026-10-09 | WebSearch | HelpAge India 2024 report elders smartphone use percentage digital access survey | High: 41% smartphone, 13% internet |
| 2026-10-09 | WebSearch | India nurses per 1000 population registered nurses PIB Lok Sabha 2024 2025 nurse population ratio | High |
| 2026-10-09 | WebSearch | Census 2011 language data Hindi 43.63% speakers scheduled languages percentage Bengali Marathi Telugu Tamil | High |
| 2026-10-09 | WebSearch | TRAI TCCCPR 2018 amendment 2025 transactional service voice calls 1600 series 140 series consent DLT registration rules | High |
| 2026-10-09 | Jina / curl | exotel.com/pricing; plivo india-calling.md; twilio trials + sandbox; sarvam saaras/pricing/TOS | Mixed (Exotel nothing; rest high) |
| 2026-10-09 | GitHub (gh) | search repos "Indic TTS AI4Bharat"; api repos/AI4Bharat/Indic-TTS | High (via api) |
| 2026-10-09 | WebSearch | incentive spirometry systematic review meta-analysis 2022 2023 2024 postoperative pulmonary complications randomized trials | High |
| 2026-10-09 | WebSearch | postoperative pulmonary complications India prospective study incidence cost rupees hospital stay tertiary care 2022 2023 2024 | Medium: Indian incidence, no rupee cost |
| 2026-10-09 | WebSearch | Indian patent smart incentive spirometer sensor IoT "incentive spirometer" India patent application | High: Tidal US patents; no Indian product |
| 2026-10-09 | WebSearch | InSee Tidal Medical Technologies incentive spirometer tracker price cost per patient hospital | Medium: no price; IEEE article (IR ToF) |
| 2026-10-09 | WebSearch | flow-oriented versus volume-oriented incentive spirometer randomized trial India patients | High: Mangalore RCT |
| 2026-10-09 | WebSearch | PM-JAY Ayushman Bharat most common surgical procedures claimed top specialities general surgery orthopaedics cardiology | High |
| 2026-10-09 | YouTube (yt-dlp) | ytsearch6: incentive spirometer kaise use kare hindi | Medium: 3-ball devices dominate |

## Round 3 plan (9 Oct 2026)
1. COMMS: TRAI TCCCPR Third Amendment text; SMS DLT; Twilio WhatsApp fee; Plivo/Exotel India price + KYC.
2. INDLOC: demographics by surgery; caregiver/living arrangements (LASI); vision/hearing/literacy; naming and format conventions.
3. TECH: VL53L1X datasheet accuracy; camera tracking of IS; open-source projects.
4. REG: CDSCO MDSW guidance + class of spirometers; DPDP Rules 2025 text.
5. VOICE: Bulbul latency, voices for elderly, Bhashini terms. 6. BIZ: PM-JAY HBP rates; India complication cost; hospital RPM models. 7. COMP: Indian/PCT patents; Indian respiratory startups. 8. JUDGE section.
(A previous round-3 agent was stopped before logging anything; its DPDP reading was redone here.)

| date | channel | query | useful? |
|---|---|---|---|
| 2026-10-09 | curl + pdftotext | TRAI Regulation_18092026.pdf (Jina returned empty) | High: primary text read |
| 2026-10-09 | WebSearch | DLT registration SMS India sender ID header template approval time cost entity registration Jio Vilpower 2026 | High: steps/timelines; fee conflicting |
| 2026-10-09 | WebSearch | Twilio WhatsApp pricing India per message fee Twilio markup 2026 | Medium: led to Twilio page |
| 2026-10-09 | Jina Reader | twilio.com/en-us/whatsapp/pricing; developer.exotel.com dlt-guide | High |
| 2026-10-09 | Jina Reader | plivo.com/voice/pricing/in; support.plivo.com India requirements | High |
| 2026-10-09 | WebSearch | Exotel account KYC verification documents how many days activation virtual number outbound calls per minute rate | High: KYC; no official rate |
| 2026-10-09 | Jina Reader | developer.exotel.com kyc-verification | High |
| 2026-10-09 | Europe PMC | (CABG OR "coronary artery bypass") AND (India OR Indian) AND "mean age" 2018–2026 | Low: noisy |
| 2026-10-09 | WebSearch | Indian patients undergoing CABG mean age male percentage diabetes multicentre registry India study | Medium: single-centre snippets |
| 2026-10-09 | Jina Reader | amrita.edu 4,024-CABG publication page | Low: abstract without numbers |
| 2026-10-09 | Europe PMC | DOI:10.1007/s12055-014-0318-5 | None (not indexed) |
| 2026-10-09 | Europe PMC | "total knee arthroplasty" India "mean age" female multicentre/registry 2019–2026 | High |
| 2026-10-09 | Europe PMC | TITLE "coronary artery bypass" India AFF "mean age" 2017–2026 | Medium |
| 2026-10-09 | Europe PMC | TITLE cholecystectomy India "mean age" female 2019–2026; "post-tuberculosis lung disease" India age | High |
| 2026-10-09 | WebSearch | LASI wave 1 India older adults living arrangements living alone with children spouse percentage caregiver daughter-in-law | High: led to LASI factsheet |
| 2026-10-09 | curl + pdftotext | VL53L1X datasheet (st.com blocked; Pololu mirror) | High |
| 2026-10-09 | GitHub (gh) | search repos "incentive spirometer"; "spirometer computer vision ball" | Medium / none |
| 2026-10-09 | Europe PMC | "incentive spirometer" AND (camera OR smartphone OR "computer vision" OR video OR sensor) 2019–2026 | High |
| 2026-10-09 | WebSearch | DPDP Rules 2025 notified November 2025 phased implementation 18 months consent manager data breach 72 hours health data exemptions Fourth Schedule healthcare | High |
| 2026-10-09 | WebSearch | meity.gov.in DPDP Rules 2025 gazette notification PDF G.S.R. 846(E) | High: primary PDF link |
| 2026-10-09 | WebSearch | CDSCO guidance document medical device software 2026 SaMD wellness software excluded risk classification final guidance | High |
| 2026-10-09 | WebSearch | CDSCO classification list respiratory devices "incentive spirometer" risk class A OR B notification anaesthesiology pulmonology | Medium: IS not listed |
| 2026-10-09 | WebSearch | Sarvam Bulbul v3 latency milliseconds time to first audio benchmark streaming TTS | Medium: vendor claim only |
| 2026-10-09 | Europe PMC | synthetic speech / TTS older adults speech rate intelligibility | None |
| 2026-10-09 | WebSearch | Bhashini ULCA API access startups free registration terms TTS ASR inference API key Dhruva | Low: third-party only |
| 2026-10-09 | WebSearch | PM-JAY HBP 2022 package rate CABG rupees coronary artery bypass graft package price Ayushman Bharat cholecystectomy package rate | High: led to HBP 2022 sheet |
| 2026-10-09 | WebSearch | India hospital cost postoperative pneumonia OR pulmonary complication rupees additional cost per patient study tertiary hospital readmission cost INR | Low: VAP proxy only |
| 2026-10-09 | Europe PMC | ventilator-associated pneumonia attributable cost India 2015 | Medium |
| 2026-10-09 | WebSearch | Indian hospital post-discharge remote patient monitoring program subscription fee rupees Apollo OR Narayana OR Manipal OR Medanta home care monitoring 2025 | Medium: models, no current prices |
| 2026-10-09 | WebSearch | patents.google.com IN incentive spirometer sensor monitoring device Indian patent application 202 | Low: US only |
| 2026-10-09 | Google Patents xhr | q=("incentive spirometer")&country=IN; q=spirometer&country=IN; q=spirometer + incentive/exerciser/lung &country=IN; q=spirometer&assignee=Tidal | Medium: found Tidal PCT |
| 2026-10-09 | WebSearch | Indian startup pulmonary rehabilitation digital app COPD home monitoring India 2025 2026 funding respiratory healthtech | High: Respira Health |

## Round 4 plan (9 Oct 2026)
1. TECH: Romsons Breazer 2500 internals; VL53L1X inside a tube (ROI, wall reflections).
2. REG: CDSCO MDSW guidance PDF itself; incentive-spirometer class.
3. COMMS: TRAI Third Amendment Gazette date; commentary on health reminder calls.
4. BIZ: rupee cost of complications / bed-days; PM-JAY current rates; home-care price anchors; unit economics.
5. COMP: Indian post-op / respiratory RPM startups (InPASS needs CAPTCHA, left to user). 6. VIS: post-TB / COPD rehab demand; NTEP guidance. 7. JUDGE: 10 more questions.
(A previous round-4 agent was stopped before logging anything; no ledger rows after #134 were found.)

| date | channel | query | useful? |
|---|---|---|---|
| 2026-10-09 | WebSearch | Romsons Breazer 2500 incentive spirometer dimensions piston cylinder diameter specifications | None: no specs anywhere |
| 2026-10-09 | WebSearch | VL53L1X inside tube pipe wall reflection ROI narrow field of view crosstalk measurement | High: ST forum threads |
| 2026-10-09 | WebSearch | TRAI TCCCPR (Third Amendment) Regulations 2026 gazette published date comes into force | Medium: PR 119 found; Gazette date not found |
| 2026-10-09 | WebSearch | CDSCO medical device software guidance July 2026 PDF wellness software classification annexure | High: primary PDF link |
| 2026-10-09 | curl + pdftotext | CDSCO MDSW guidance PDF | High |
| 2026-10-09 | YouTube (yt-dlp) | ytsearch8: Romsons Breazer 2500 | None (titles only) |
| 2026-10-09 | WebSearch | "Breazer" Romsons volumetric exerciser amazon.in product dimensions cm | None |
| 2026-10-09 | WebSearch | romsons.com breazer volumetric respiratory exerciser 4000 2500 5000 product catalogue | Low: retail only |
| 2026-10-09 | curl + pdftotext | TRAI PR_No119of2026.pdf | High |
| 2026-10-09 | WebSearch | TRAI third amendment 2026 TCCCPR A2P calls "service" calls hospitals healthcare reminders analysis law firm October 2026 | Medium: Exotel comments |
| 2026-10-09 | WebSearch | India cost of postoperative pulmonary complications rupees per patient hospital stay study INR | Low: no rupee PPC cost exists |
| 2026-10-09 | WebSearch | Portea home nursing visit price per day rupees 2026 OR Apollo HomeCare nursing charges per day post-surgery care | Low: old snippets only |
| 2026-10-09 | WebSearch | National Health System Cost Database India cost per ICU bed day ward bed day rupees tertiary hospital PGIMER | High: CHSI ₹2,307/bed-day |
| 2026-10-09 | Europe PMC | ABSTRACT "2307" bed-day India; ICU "bed day" India cost trauma 2016–2026 | High: PMIDs 37857541, 38953191 |
| 2026-10-09 | WebSearch | PM-JAY HBP 2025 revised package rates increase CABG cholecystectomy NHA rationalisation 2025 2026 | Low: HBP 2022 still latest found |
| 2026-10-09 | WebSearch | Indian startup post-surgery remote patient monitoring home recovery app hospitals 2025 2026 Inc42 OR YourStory respiratory | Medium |
| 2026-10-09 | WebSearch | NTEP post-TB care guidance document India 2024 post-tuberculosis lung disease pulmonary rehabilitation follow-up | High |
| 2026-10-09 | WebSearch | pulmonary rehabilitation availability India COPD patients percentage access centres Lung India 2023 2024 survey | Medium: Pune survey |
| 2026-10-09 | Europe PMC | "pulmonary rehabilitation" Pune survey/needs 2022–2026 | High |
| 2026-10-09 | WebSearch | VL53L1X module price India robu.in OR robocraze rupees ESP32-C3 price India | Medium (snippets) |
| 2026-10-09 | WebSearch | VL53L1X ROI 4x4 SPAD field of view degrees 16x16 27 degrees user manual UM2356 SetROI | Medium: 4x4 ≈ 15° |
| 2026-10-09 | Europe PMC | "incentive spirometer(s)" AND (accuracy OR bench OR calibration OR "inspired volume") | None new |
| 2026-10-09 | WebSearch | CDSCO classification "incentive spirometer" OR "respiratory exerciser" OR "lung exerciser" risk class A notified medical device list | Low: no Indian entry; US Class II |
| 2026-10-09 | WebSearch | "Third Amendment" TCCCPR 2026 notified gazette "September 2026" effective "October 2026" A2P declaration deadline | None |
