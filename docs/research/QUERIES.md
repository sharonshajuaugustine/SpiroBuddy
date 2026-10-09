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

## Round 5 plan (9 Oct 2026, task Q-24)
1. REG: CDSCO respiratory list (2021) and Jan 2025 self-notified list: is "incentive spirometer" named, which class; Romsons registration for the Breazer.
2. BIZ: Indian 30-day readmission after CABG / abdominal / joint replacement. 3. BIZ: 2025–26 home-care prices (Portea, Apollo, Max@Home, Tata 1mg).
4. ADH: Indian IS adherence at home / after discharge. 5. VIS: post-TB sizing (TB completions, lung impairment). 6. INDLOC: voice/IVR evidence for older Indians. 7. JUDGE: 5+ new questions.

| date | channel | query | useful? |
|---|---|---|---|
| 2026-10-09 | WebSearch | CDSCO notification respiratory devices risk classification 2021 list "spirometer" class A B incentive | Low: consultancy pages only |
| 2026-10-09 | WebSearch | 30-day readmission rate after cardiac surgery CABG India study tertiary hospital | Medium: meta-analysis (international) |
| 2026-10-09 | WebSearch | India TB Report 2025 number of patients successfully treated treatment success rate notified 2024 | Medium: 90% success (news) |
| 2026-10-09 | WebSearch | elderly India IVR voice-based health intervention older adults usability study mHealth | Low: no Indian study |
| 2026-10-09 | WebSearch | CDSCO "self notified" class A medical devices list January 2025 respiratory devices PDF MED-16014 | Medium: Morulaa list |
| 2026-10-09 | WebSearch | Romsons Scientific CDSCO manufacturing licence MD-5 respiratory exerciser Breazer registration | None: no licence data |
| 2026-10-09 | Jina | Morulaa Class A self-notified list (grep spiro/exerciser) | Medium: "Pulmonary exerciser" only |
| 2026-10-09 | Europe PMC | TITLE readmission AND India AND (surgery OR CABG OR arthroplasty OR laparotomy) 2015–2026 | Low |
| 2026-10-09 | Europe PMC | ABSTRACT readmission AND AFF:India AND 30-day AND surgery 2016–2026 | High: Amrita protocol, Ludhiana TKA, Tata caregiver pilot |
| 2026-10-09 | WebSearch | Portea post-operative care at home price nursing attendant per visit 2025 | None |
| 2026-10-09 | WebSearch | incentive spirometer adherence after discharge India patients home compliance study physiotherapy | Low: no home data |
| 2026-10-09 | WebSearch | India TB Report 2026 MoHFW released patients notified 2025 treatment completed lakh | Low: no 2026 report |
| 2026-10-09 | WebSearch (pib.gov.in) | pib.gov.in TB Mukt Bharat 2025 notified TB cases treatment success rate Ni-kshay press release | High: PIB Mar 2026 PDF |
| 2026-10-09 | Europe PMC | post-tuberculosis lung disease India prevalence/spirometry 2019–2026 | Medium: Mullana |
| 2026-10-09 | Europe PMC | "incentive spirometry/spirometer" AND AFF:India AND (adherence OR compliance OR knowledge OR practice) 2015–2026 | Medium: Chennai practice study |
| 2026-10-09 | WebSearch | "Max@Home" OR "Apollo HomeCare" nursing care at home charges per day rupees 2025 2026 | Low |
| 2026-10-09 | WebSearch | India hospital remote patient monitoring post-discharge program price per month rupees subscription 2025 | None |
| 2026-10-09 | WebSearch (portea.com) | portea nursing attendant physiotherapy at home price ₹ | Low (old snippets) |
| 2026-10-09 | Europe PMC | (IVR OR "voice call" OR "voice message" OR "voice-based") AND India AND (elderly OR older adults OR low literacy …) 2016–2026 | Medium: Virtual Baithak protocol |
| 2026-10-09 | Europe PMC | TITLE:"99DOTS" AND (accuracy OR adherence OR acceptability) AND (review OR cohort …) | None (non-India) |
| 2026-10-09 | Europe PMC | 99DOTS AND India AND (urine OR accuracy OR sensitivity) | High: DAT systematic review |
| 2026-10-09 | WebSearch (cdsco.gov.in) | cdsco.gov.in pdf "Respiratory" risk classification medical devices 2021 "Intended use" "Risk Class" annexure | High: Class A non-measuring list PDF |
| 2026-10-09 | curl + pdftotext | CDSCO Class A (non-sterile, non-measuring) list – grep "incentive" | High: item 496 |
| 2026-10-09 | Europe PMC | (readmission OR rehospitalization) AND (CABG OR cardiac surgery) AND India 2012–2026 | None (no Indian rate) |
| 2026-10-09 | Europe PMC | post-TB obstructive/restrictive spirometry systematic review 2019–2026 | Medium: Madurai |

## Round 6 plan (10 Oct 2026, capped at ~15 sources)
1. BIZ: an Indian 30-day readmission rate after CABG or major abdominal surgery (pulmonary causes if any).
2. ADH: Indian post-discharge incentive-spirometer adherence (CTRI, Indian journals).
3. INDLOC/VOICE: Kilkari / mMitra evaluations; LASI phone ownership and use among 60+.
4. VIS: pulmonary share of TB in India; RBIPMT 2024 post-TB rehab guidance PDF.
5. BIZ (only if budget remains): published home-physio / home-nursing prices.

| date | channel | query | useful? |
|---|---|---|---|
| 2026-10-10 | Europe PMC | (readmission OR readmitted OR rehospitalisation) AND (India OR Indian) AND (CABG OR "cardiac surgery" OR laparotomy OR "abdominal surgery" OR gastrointestinal OR pancreaticoduodenectomy OR esophagectomy) 2014–2026 | High: SGPGI Whipple, CMC ICU recidivism, I-INFUSE (4.7%) |
| 2026-10-10 | WebSearch | "readmission" after off-pump CABG Indian patients 30 days rate "India" cohort Indian Heart Journal OR "Indian J Thorac" | None (no Indian CABG rate) |
| 2026-10-10 | WebSearch | ctri.nic.in incentive spirometer trial home discharge | None (CTRI not indexed; only #5 again) |
| 2026-10-10 | Europe PMC | "incentive spirometr*" AND (CTRI OR "Clinical Trials Registry-India") 2016–2026 | None (0 hits) |
| 2026-10-10 | Europe PMC | (spirometer OR spirometry OR "breathing exercise*") AND (CTRI OR "Clinical Trials Registry") AND India AND (home OR discharge) AND (adherence OR compliance) 2016–2026 | Medium: Thar Desert tele-rehab, rural peer-led PR (no IS data) |
| 2026-10-10 | WebSearch | LASI older adults India mobile phone ownership percent aged 60 "mobile phone" use study | Low (snippets: DAHLIA 50%) |
| 2026-10-10 | Europe PMC | (LASI) AND ("mobile phone" OR "internet use" OR digital OR ICT) 2020–2026 | None |
| 2026-10-10 | Europe PMC | TITLE:(mobile phone OR smartphone OR internet use OR digital divide/literacy) AND India AND (elderly OR older adults) 2020–2026 | None useful |
| 2026-10-10 | curl + pdftotext | LASI Wave 1 India Report 2020 – grep "mobile phone", "telephone" | High: 87% households own a mobile; 28.6% of 60+ have difficulty making phone calls |
| 2026-10-10 | Europe PMC | (Kilkari OR mMitra) 2018–2026 | High: Kilkari exposure + RCT |
| 2026-10-10 | Jina | ntep.in/node/6610 and book/export/html/6610 – grep spirometer/breathing/home | High: incentive spirometer listed in RBIPMT 2024 breathing exercises |
| 2026-10-10 | WebSearch | India TB Report 2024 notified pulmonary extrapulmonary percentage of total notified TB patients | Medium: WHO pages |
| 2026-10-10 | WebSearch | "India TB Report" extrapulmonary TB share of notifications "per cent" pulmonary 2023 OR 2024 tbcindia.mohfw.gov.in pdf | Low (India TB Report PDF not found) |
| 2026-10-10 | WebFetch | WHO GTB 2025 case notifications – India / SEAR extrapulmonary share | Medium: India EPTB ">20%" |
| 2026-10-10 | WebSearch | physiotherapy at home per session charges ₹ 2026 Apollo HomeCare OR Portea OR "Max@Home" OR "Care24" price | Low (aggregator snippet only) |
| 2026-10-10 | Jina | apollohomecare.com/physiotherapy-at-home – grep ₹/price | Low: packages incl. "Chest Physiotherapy", no prices |

## Round 7 plan (10 Oct 2026, capped at ~12 sources; person-only gaps skipped: calipers, CTRI, InPASS, TRAI Gazette)
1. BIZ: Indian 30-day readmission after CABG / cardiac surgery (stop after ~4 sources).
2. REG: Romsons Breazer CDSCO registration; which MDR 2017 rule would class a *measuring* clip-on.
3. INDLOC/VOICE: personal phone ownership 60+; WhatsApp/voice-note use by older Indians; mMitra listening data.
4. VIS: India pulmonary vs extrapulmonary TB split.

| date | channel | query | useful? |
|---|---|---|---|
| 2026-10-10 | Europe PMC | (readmission OR readmitted OR "re-admission" OR rehospitali*) AND ("coronary artery bypass" OR CABG OR "valve replacement" OR "open heart") AND (India OR Indian OR Kerala OR Chennai OR Delhi OR Vellore OR Trivandrum) 2010–2026 | Low: 1,410 hits, no Indian 30-day rate in top 40 |
| 2026-10-10 | Europe PMC full text | PMC11473761, PMC12138072 – grep readmi/pneumonia | None (no 30-day rate) |
| 2026-10-10 | WebSearch | "30-day readmission" cardiac surgery Indian tertiary centre study post-operative pulmonary complications readmitted India 2022 2023 2024 | None (only paediatric 2018 + non-Indian) |
| 2026-10-10 | Europe PMC | JOURNAL (IJTCVS OR Ann Card Anaesth OR Indian Heart J) AND (readmission OR readmitted OR rehospitalization) AND (CABG OR "coronary artery bypass" OR "cardiac surgery") 2012–2026 | Low: no Indian 30-day rate; gap closed for agents |
| 2026-10-10 | WebSearch | Romsons Scientific & Surgical Industries CDSCO registration certificate Class A medical device Agra incentive spirometer | None |
| 2026-10-10 | WebSearch | GeM incentive spirometer volumetric 5000 ml bid specification CDSCO registration required | None (GeM bids not indexed) |
| 2026-10-10 | WebSearch | Medical Devices Rules 2017 First Schedule Part I classification rules "active device" "intended for diagnosis" "accessory" cdsco.gov.in pdf | High: link to primary MDR PDF |
| 2026-10-10 | curl + pdftotext | MDR 2017 PDF – grep accessor / active diagnostic / monitoring / software | High: F-REG-6 |
| 2026-10-10 | WebSearch | NSS 78th round Comprehensive Annual Modular Survey 2022-23 mobile phone use by age group 60 years and above percentage persons owning mobile phone | None |
| 2026-10-10 | Europe PMC | ("own a mobile phone" OR "mobile phone ownership" OR "personal mobile phone" OR "WhatsApp use") AND (older adults OR elderly OR aged 60 OR geriatric) AND India 2019–2026 | Medium: Telangana 45+ smartphone figures |
| 2026-10-10 | WebSearch | mMitra ARMMAN voice call listenership percentage of calls listened "more than 30 seconds" engagement drop-off study | Medium: Kilkari listenership preprint (no mMitra-specific figure) |
| 2026-10-10 | WebSearch | India TB Report 2025 "extra-pulmonary" notified 2024 per cent "pulmonary" TB patients notified tbcindia | Low (report PDF still not found) |
| 2026-10-10 | curl (WHO TME CSV) | WHO notifications dataset, India 2019–2024: new_labconf, new_clindx, new_ep, ret_rel_* | High: F-VIS-7 (EP 26.0% in 2024) |
| 2026-10-10 | WebSearch | older adults India WhatsApp use voice messages survey senior citizens 60+ percent use WhatsApp 2023 2024 study | None (small studies, snippets only) |

## Round 8 plan (10 Oct 2026, capped at ~10 sources): is sending health updates on WhatsApp allowed?
1. Meta policy: Business Messaging Policy health / sensitive-data / prohibited lines.
2. Opt-in, template categories (utility vs marketing), 24-hour window.
3. Cloud API data handling: processor role, retention, India local storage.
4. Indian precedent (government or hospital on WhatsApp Business).
5. Indian rules (TPG 2020, DPDP, SPDI) – reuse ledger items where possible.
Also: added FUTURE_ARCHITECTURE W1–W16 to the ledger (#191–#206) without opening them.

| date | channel | query | useful? |
|---|---|---|---|
| 2026-10-10 | Jina | business.whatsapp.com/policy – grep health/medical/sensitive/opt-in/template | High: F-COMMS-14 |
| 2026-10-10 | Jina | developers.facebook.com/docs/whatsapp/updates-to-pricing/new-template-guidelines | None (Page Not Found) |
| 2026-10-10 | WebSearch | developers.facebook.com WhatsApp template categorization utility "appointment" marketing guidelines | High: found the .md doc URL |
| 2026-10-10 | curl | template-categorization.md – grep utility/health/appointment/recategor | High: F-COMMS-15 |
| 2026-10-10 | WebSearch | WhatsApp Cloud API data privacy security "data processor" messages stored 30 days data localization developers.facebook.com | High: found Meta page |
| 2026-10-10 | curl | data-privacy-and-security.md, local-storage.md, registration.md – grep processor/30 days/region/India | High: F-REG-7 (India "IN" supported) |
| 2026-10-10 | curl | getting-opt-in.md | High: F-COMMS-16 |
| 2026-10-10 | WebSearch | Telemedicine Practice Guidelines 2020 Board of Governors MCI pdf WhatsApp "Facebook Messenger" text based | Medium: PDF URLs (all blocked) |
| 2026-10-10 | curl / Jina / WebFetch | TPG PDF at covid19dashboard.mohfw.gov.in, nmcn.in, mohfw.gov.in, vikaspedia | None (blocked / empty) |
| 2026-10-10 | WebSearch | "Telemedicine Practice Guidelines" text "WhatsApp" "Facebook Messenger" "chat" "Mobile App" RMP section 3 technology "Text / Chat based" | Medium: secondary summaries quote WhatsApp line (F-REG-8) |
| 2026-10-10 | WebSearch | PIB MyGov Corona Helpdesk WhatsApp chatbot 9013151515 launched vaccination certificate download WhatsApp | Medium: F-INDLOC-10 (news snippets) |
