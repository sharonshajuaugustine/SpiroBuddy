# Competitors and alternatives: who else tracks or replaces the incentive spirometer
**Written:** 10 Oct 2026 · **Sources opened this round:** 25 (19 useful, 5 failed to load or held nothing, 1 was a re-open of known papers through another address) plus about 30 search-result summaries · **Confidence overall:** high on the evidence reviews and on "nobody sells this in India"; medium on product status abroad; **low** on which spirometer type Indian hospitals buy (no real numbers exist)

How to read this: "S1…S25" are pages opened this round (table at the end). "#n" is a row in `docs/research/SOURCES_LEDGER.md`. "F-…" are findings in `KNOWLEDGE_BASE.md`; "B1-…, B2-…, E-…, H-…" are findings in other business and plan files. Grades: **A** = peer-reviewed, regulator, registry or patent record; **B** = reputable organisation or company page; **C** = blog, press-release reprint, retailer or search snippet. Status words: **CONFIRMED** (two independent sources, or one grade-A primary record), **SINGLE SOURCE**, **NOT CONFIRMED** (snippet only or a claim nobody backs up).

Words used below:
- **Volume type** = the spirometer with one disc (piston) that rises to show how much air you breathed in, e.g. Romsons Breazer 2500. Our laser reads this one.
- **Three-ball type** (also "flow type", "Triflo", "respirometer") = three small balls in three tubes that lift if you breathe in fast enough. There is no single height to read, so our laser can't read it.
- **PPC** = post-operative pulmonary complication: pneumonia, collapsed lung areas, and similar lung problems after surgery.

---

## Answer in 10 lines
1. **Nobody sells what we are building.** No product anywhere, and none in India, tracks an ordinary spirometer **at home** and coaches the patient by voice in their language while telling the nurse and the family. (B7-1 to B7-9)
2. **The closest rival is still InSee (US, FDA-cleared 2025).** It fits one US spirometer, it is for hospital use only, it has no public price, and we found no 2026 news of it spreading. (B7-1)
3. **Most "smart incentive spirometers" either stayed in research or changed business.** Airalux is still in a 30-patient trial. ZEPHYRx (a breathing-game company) moved into clinical-trial data and was sold in Aug 2026. Lungy Health promised a medical app "in 2023" and we found no sign it launched. SpiroTimer is not on sale. (B7-2 to B7-6)
4. **The real threat is software with no hardware.** A phone app that "hears" the breath (QUT Inspire, Australia) and a tablet camera that reads the scale (Turkey 2025) both work, **but only on simulated breaths or healthy volunteers.** No product does this for patients yet. (B7-10, B7-11)
5. **Reading the three-ball type is technically easy and not blocked by patents we could find.** A US patent filing that put light sensors on the three ball tubes, including a clip-on version, was **abandoned in 2020**. A Michigan add-on already tracks the flow ball as well as the piston. (B7-7, B7-12)
6. **In India, big companies already ship phone-and-breath apps at scale:** Cipla's free CipAir app screens for asthma from three breaths blown at the phone (Dec 2024), and Lupin's LYFE remote cardiac rehab got CDSCO Class C software approval (2024). Either could add breathing exercise. Neither does today. (B7-14, B7-15)
7. **Evidence, honestly:** the best reviews say incentive spirometry **on its own** does not prevent lung complications better than other breathing care (31 trials, 3,776 adults: risk ratio 1.00). Benefit shows up only in lung-surgery studies and as part of a care bundle. **No major trial measured whether patients actually did the exercise.** (B7-18 to B7-21)
8. **Which spirometer Indian hospitals buy: no real numbers exist.** Every proxy points to the three-ball type being common: cheaper (₹56–145 wholesale against about ₹1,067 MRP for the Breazer), and most listings are three-ball. Indian trials use both types. (B7-23, B7-24)
9. **So what for SpiroBuddy:** position as **"the adherence and coaching layer for breathing exercise, starting with a laser base for the volume spirometer"**, not "a smart spirometer". Threat level today: **low** from hardware rivals, **medium within 2 years** from phone-only apps and from Cipla- or Lupin-sized players. Our defence is the nurse dashboard, voice in Indian languages, the family link, and working for elders with no smartphone. The app must accept breaths from any source (base, phone microphone, phone camera, or "I did it" tap).
10. **To a judge asking "doesn't X already do this?":** "InSee does it in US hospitals for one US spirometer. Phone apps do it in labs with healthy volunteers. Nobody does it at home in India, in Hindi or Tamil, for a patient without a smartphone, with the nurse and the family in the loop. And because the evidence says the exercise only helps when it is actually done as part of the nurse's plan, we measure exactly that."

---

## Competitor table

| Name | Country | What it does | Price | Approval | Status | Source / grade |
|---|---|---|---|---|---|---|
| **InSee** (Tidal Medical) | US | Clip-on base under one US spirometer (AirLife 2500/4000); infrared time-of-flight reads the piston; counts good breaths; blinking-light reminder; Wi-Fi | Not public; free hospital trial offered | FDA 510(k) K241152, Class II, 21 Aug 2025; hospital use, prescription only; earlier COVID EUA 2021 | On sale in US (small); no India presence found | #3, #31, #88, #101–103 (A/B); snippet 2026 (C) |
| **Airalux** (Airalux Medical, Penn spin-out) | US | A whole new digital incentive spirometer with its own screen (no phone needed) plus a clinician dashboard | Not public | None found | Prototype in a 30-patient single-arm trial; won ATS BEAR Cage pitch prize May 2025; grant-funded | #5, #6, #34 (A/B); S11 (B) |
| **ISTracker** (University of Michigan, Burns group) | US | Reusable add-on with light sensors that tracks **both the volume piston and the flow ball** of a common spirometer; breath classifier; game mode | Not public | None (academic) | Research; 2023 accuracy paper, 2026 survey of 105 users | #50 (A); S6 (A) |
| **QUT Inspire** | Australia | **App only, no device**: the phone microphone hears the in-breath and animates a virtual spirometer | Free web app (research) | None | Research: tested on a syringe (2021) and 24 healthy adults vs Triflo II (2022) | S6 (A); snippets (C) |
| **Lungy / Lungy Health** (UCL + studio Pi-a) | UK | Breathing app using phone camera + microphone; medical version claimed it "could potentially replace" plastic incentive spirometers | Wellness app on App Store | Medical version planned as UK Class I; no registration found | **Stalled or dead as a medical product**: promised for 2023, nothing found after 2023 | S14 (C); snippets (C) |
| **ZEPHYRx** | US | Breathing video games on a tablet driven by a Bluetooth MIR Spirobank spirometer, as a post-surgery incentive spirometer | Not public | None for this use | Trial (100 patients, Rochester) status "unknown" since 2022; company re-focused on clinical-trial lung data; **sold Aug 2026** | S15 (A); S22 (B) |
| **SpiroTimer** (Eltorai, Brown Univ.) | US | Reminder and use-counter for an ordinary spirometer; RCT showed more use | Not on sale | None found | Trademark filed 2024 by the inventor as an individual; no company or sales found | #1, #2 (A); snippets (C) |
| **Go-breath** | South Korea | App with hourly alarms and nurse dashboard; use self-reported, no sensor | – | – | Trial only (42 patients, no significant benefit) | #52 (A) |
| **Thai digital incentive spirometer** (Thammasat Univ. + NECTEC) | Thailand | Digital spirometer that shows inspired volume in real time | Not public | Not found | Research: 2025 RCT (32 heart-surgery patients, no better than Triflo); 2026 accuracy study (150 people) | #120 (A); S7 (A, re-open) |
| **Tablet-camera AI spirometry** (Uzun et al.) | Turkey | Tablet camera + AI reads the marker of an ordinary spirometer | – | – | Research only, scripted / simulated data | #120, H3 (A) |
| **"Electronic incentive spirometer"** patent US20180360346A1 | US filing (individual inventors) | Light sensors on each ball tube of a **three-ball** spirometer; a clip-on version for "various triflow" devices; RFID + Wi-Fi | – | – | **Abandoned 2020** (Google's status) | S19 (A) |
| **UCLA incentive spirometry system** (case 2016-288) | US | Adaptor on spirometer tubing; records performance to the patient's phone | – | – | Offered for licensing (page © 2019); no product found | S21 (B) |
| **IIT Guwahati PEEP spirometer** | India | New mechanical spirometer for tracheostomy patients; Bluetooth sensor version "planned" | – | Indian patent reported | Prototype, lab-validated | Snippet only (C) |
| **Bluetooth lung-function meters** (MIR Smart One / Spirobank Smart, CMI SpiroLink) | Italy / US | Measure **breathing out** (FEV1, peak flow) for asthma/COPD; some have "incentive" graphics | About US$88–110 (SpiroLink) | FDA / CE for lung-function testing | On sale; **not** post-surgery breathing trainers | Snippets (C) |
| **Cipla CipAir** (inside Breathefree app) | India | Asthma screening from 3 breaths blown at the phone (sound analysis) | Free | Not stated | Launched Dec 2024, Android | S10 (C) |
| **Lupin LYFE** | India | Remote cardiac rehab: care managers, coaches, wearables, cardiologist protocols | Not public | **CDSCO Class C software (2024)** | On sale; no breathing-exercise module mentioned | S25 (C); snippets (C) |
| **Mediwatch** | India | Daily post-surgery symptom check-ins, green/amber/red alerts, WhatsApp reminders | Not public | None stated | Very small (contact is a personal e-mail; no named hospital) | S13 (C) |
| **Respira Health** | India | WhatsApp COPD rehab with online physios | Free (non-profit) | – | Pilot, 18% completion | #133 (C) |
| **Indian remote-monitoring firms** (Dozee, Tricog, Zorgers + Clinitouch, Manipal + ConnectedLife, Amrita Smart CABGuard) | India | Vital signs in bed or at home; ECG; COPD check-ins; LLM nurse chatbot after bypass | Not public (Dozee home kit ₹3,999/30 days in 2021, snippet) | Various | On sale or in trials; **none tracks breathing exercise** | F-COMP-11, F-COMP-12 (A/B/C) |
| **Digital prehab apps** (Surgery Hero, PrehabM, Fit4Surgery) | UK / Germany / Netherlands | Exercise, nutrition and mental prep before surgery | – | PrehabM CE-marked | Surgery Hero bought by Sword Health Jan 2025 | Snippets only (C) |

---

## Findings

### 1. Smart or connected incentive spirometers and add-ons

### B7-1: InSee is still the only cleared clip-on tracker, and it is narrow
- Detail: FDA 510(k) K241152 (21 Aug 2025), accessory to the AirLife spirometer only, hospital use. A 2021 FDA letter said AirLife makes almost half of the incentive spirometers used in US acute hospitals, which explains why InSee fits only that one. Bench accuracy 97% (FDA EUA document, snippet). No price, no 2026 news, no India distributor.
- Source: #3, #31, #101–#103 (A/B); 2026 search found nothing newer (C)
- Status: **CONFIRMED** (clearance and scope); "no 2026 adoption news" is **NOT CONFIRMED** (absence of evidence).
- So what: InSee proves hospitals and the FDA accept the idea. It leaves home use, other spirometers, languages and family entirely open.

### B7-2: Airalux is a full replacement spirometer, still at trial stage
- Detail: Penn spin-out. Its pitch won the ATS 2025 BEAR Cage prize (US$10,000). Feedback is on the device itself, because the founders see phone pairing as a barrier for post-surgery patients. In a single-arm trial (NCT06629454, 30 patients). Funded by grants (NHLBI and others per a database profile, snippet). No price, no clearance.
- Source: S11 (B); #5, #6, #34 (A/B)
- Status: **CONFIRMED**
- So what: their "no phone needed" lesson matches ours (a base that beeps and speaks on its own). Their weakness: hospitals must buy a new spirometer instead of using the one they already stock.

### B7-3: Michigan's ISTracker reads both the piston and the flow ball, and now has a game mode
- Detail: 2023 paper: light sensors track the volume piston and the flow "bobbin" (the small flow indicator), 99% and 100% accuracy. 2026 *Anesthesiology* paper: 105 patients and staff tried it; 90.5% found it easy, 81% would use the game version, 62.9% preferred it to a plain spirometer; younger people liked the game more. No accuracy or outcome data in 2026.
- Source: #50 (A); S6 (Alrubaie et al., *Anesthesiology* 2026;145:347–58) (A)
- Status: **CONFIRMED**
- So what: closest technical prior art, and proof a flow indicator can be read with cheap light sensors. Academic, US, English, no home or family loop.

### B7-4: ZEPHYRx tried gamified post-surgery spirometry, then changed business and was sold
- Detail: Trial NCT04429009: tablet games driven by a Bluetooth MIR Spirobank, 100 lung-surgery patients planned at Rochester; status "unknown", last update Aug 2022, no results posted. In Aug 2026 a law firm announced ZEPHYRx's sale to an unnamed clinical-research company, describing it as a provider of "respiratory endpoint data capture" for clinical trials.
- Source: S15 (A); S22 (B)
- Status: **CONFIRMED** (both facts); *why* it moved away is **NOT CONFIRMED** (our reading).
- So what: likely lesson: a hospital paying for post-surgery breathing games was a harder sale than pharma paying for trial data. Keep the hospital value case concrete (nurse time saved, B2-11).

### B7-5: Lungy Health promised to replace plastic spirometers with a phone app; it seems to have stalled
- Detail: UCL / Pi-a app using the phone camera and microphone together. Press in 2022–23 said a Class I medical version for asthma, COPD and long COVID was due in 2023, with pilots at the Royal Free Hospital, and that it "could potentially replace" disposable incentive spirometers. We found nothing after 2023: no registration, no published results. The wellness app is still on the App Store.
- Source: S14 (C); UCL and Design Week snippets (C); two UCL pages refused (S12, S16)
- Status: claims **CONFIRMED** (several press items); "stalled" is **NOT CONFIRMED** (absence of evidence).
- So what: the "phone replaces the spirometer" idea has been announced before and not delivered. Still, it shows where the field wants to go.

### B7-6: SpiroTimer, Go-breath and UCLA's system never became products we could find
- Detail: SpiroTimer (the reminder from the 2019 JAMA Surgery trial, F-ADH-1): 52-nurse usability survey; trademark filed Sep 2024 by the inventor personally; no seller found. Go-breath (Korea): no significant benefit (F-ADH-5). UCLA case 2016-288: offered for licensing since about 2019.
- Source: #2, #52 (A); S21 (B); trademark snippet (C)
- Status: **SINGLE SOURCE** each.
- So what (why ideas die here): small single-site studies, no outcome proof, hospitals unwilling to pay for "reminders", and a product tied to one spirometer model. Our counter: lend through the hospital, measure nurse time saved, fit more than one model.

### B7-7: A clip-on sensor for three-ball spirometers was filed as a US patent and abandoned
- Detail: US20180360346A1 (filed 18 Jun 2017, individual inventors): light interrupters on each ball tube count breaths; a two-arm clip-on box fits "various triflow" spirometers; an infrared distance sensor for single-ball devices; RFID + Wi-Fi. Final rejection Nov 2019, abandoned Aug 2020 (Google's status).
- Source: S19 (A); Justia copy refused (S17)
- Status: **SINGLE SOURCE** (one patent record; legal status is Google's assumption).
- So what: (1) a three-ball reader is simple hardware: three light gates. (2) This filing is now public prior art that nobody owns. Not legal advice; a freedom-to-operate check is still needed before selling.

### B7-8: Big spirometer makers have not launched connected incentive spirometers
- Detail: AirLife's product page lists only plain volume spirometers. One market-report site claims BD launched a "wireless incentive spirometer" in Jan 2023; we found no BD press release or product to back it.
- Source: snippets (C)
- Status: **NOT CONFIRMED**
- So what: the makers are not in the race yet. Partner with one (Romsons, see 05 plan) before they build their own.

### B7-9: Bluetooth "spirometers" on sale are lung-function meters, not breathing trainers
- Detail: MIR Smart One / Spirobank Smart and CMI SpiroLink measure a hard **out**-breath (FEV1, peak flow) for asthma and COPD. Some show "incentive" graphics to make the test better. SpiroLink sells for about US$88–110.
- Source: snippets (C)
- Status: **SINGLE SOURCE** per product.
- So what: if a judge says "Bluetooth spirometers already exist", the answer is: they test lung function; they don't coach the slow, deep in-breath after surgery.

### 2. Phone camera, microphone and computer vision

### B7-10: Microphone-only "virtual spirometer" works in the lab, not yet in patients
- Detail: QUT Inspire (Australia). 2021: tested with a 3-litre syringe and recorded sounds, no people. It detected high and medium flows reliably with the phone **5 cm or less** from the mouth; strong flows up to 50 cm. Worked on several phone models. 2022: 24 healthy adults (mean age 39) used both the app and a Triflo II; breath length was similar (7.3 vs 7.5 s); all 24 preferred the app for motivation; but people held the phone **13.6 cm** away on average despite being told to keep it under 5 cm. The authors say patient trials are still needed. It measures breath **duration**, not volume.
- Source: S6 (Baxter et al., *Sensors* 2021; *BMJ Open Respir Res* 2022) (A)
- Status: **CONFIRMED** (two papers, same group)
- So what: this is the most dangerous idea for our hardware, because it needs nothing but a phone. Weak points: no volume, no tested patients, needs a smartphone held close, and noisy wards. It also suggests a cheap **"no device" tier** for us: the phone microphone counts breaths when no base unit is available.

### B7-11: Camera reading of a spirometer: one simulated study, no patient study, nothing for three-ball devices
- Detail: The only camera study (Turkey 2025, tablet on a stand, more than 95% detection, scripted data) is already in our files (H3, F-TECH-2). A broad Europe PMC search this round (60 results, 2018–2026) found no other camera or computer-vision study of incentive spirometers, and none on three-ball devices. A 2016 study used a phone camera on the **chest**, with a spirometer only to calibrate (snippet). A Google Patents search ("incentive spirometer" + camera + image, after 2015, 21 hits, first page read) found no patent claiming a camera that reads the spirometer.
- Source: S5 (A); S20 (C); H3, #120 (A)
- Status: "no patient-tested camera reader exists" **CONFIRMED** within these two searches; it may exist unpublished.
- So what: for three-ball devices a camera only has to see whether each of three coloured balls is up, which is much easier than reading a scale. That makes a phone-camera three-ball mode a realistic two-week student experiment (05, "Open questions"), and an opening nobody has published.

### B7-12: Three-ball devices are readable; nobody has shipped a reader
- Detail: Michigan reads a flow indicator with light sensors (B7-3). The abandoned patent used light gates on three tubes (B7-7). The Thai digital spirometer was tested **against** a Triflo, not on one (B7-1 table).
- Status: **CONFIRMED** (technical feasibility); "nobody ships one" **NOT CONFIRMED**.
- So what: the three-ball gap is a product gap, not a science gap. Whoever builds a cheap three-ball reader for India first has the larger market (E-12).

### B7-13: Phone-based chest or sound sensing is moving fast in general
- Detail: Indian examples: Swaasa (Salcit, Hyderabad) analyses cough sounds for TB and lung disease, 87% agreement with a chest physician in 355 cases (preprint), said to be CDSCO-registered (2023 press, unverified). Cipla's CipAir (B7-14).
- Source: snippets (C)
- Status: **NOT CONFIRMED**
- So what: the phone-as-sensor trend is real in India. Plan for it rather than fight it.

### 3. App-only programmes and Indian companies that could add breathing exercise

### B7-14: Cipla already runs a free phone-and-breath app in India
- Detail: CipAir, inside Cipla's Breathefree app, launched Dec 2024 on Android: the user blows three breaths at the phone; sound analysis gives an asthma risk result in under a minute. Described as "clinically validated" in a multi-centre Indian study, with no numbers given. Cipla also opened a Breathefree lung-health centre with rehab services in Delhi (late 2025, snippet).
- Source: S10 (C); snippets (C)
- Status: **SINGLE SOURCE** (press reprint)
- So what: an Indian giant with a lung brand, doctor reach and a breath-sensing phone app. If anyone in India builds a phone-only breathing coach, Cipla is the most likely. Treat it as a possible partner (pharma patient-support budgets) as much as a threat.

### B7-15: Lupin's LYFE is a CDSCO-approved remote cardiac rehab programme
- Detail: Lupin Digital Health, launched Jan 2023; Class C "Software as a Medical Device" approval from CDSCO, May 2024 (press), after review and an on-site audit. Care managers, coaches, wearables, cardiologist protocols. No breathing-exercise or post-bypass spirometer module mentioned. Reach claims ("700 cardiologists, 280 districts") come from company text in snippets only.
- Source: S25 (C); snippets (C); S23 held nothing
- Status: approval **SINGLE SOURCE**; reach **NOT CONFIRMED**.
- So what: (1) shows CDSCO will license home rehab software, which helps our own regulatory story (04). (2) LYFE serves heart patients after discharge, our first users. Adding "breathing exercise" would be easy for them. Best framed as a partner: our base unit as a data source for their programme.

### B7-16: Small Indian post-surgery monitoring tools exist but don't track exercise
- Detail: Mediwatch: daily symptom check-ins with green/amber/red triage and WhatsApp reminders for Indian hospitals; no named customers; run by an individual. Respira Health (WhatsApp COPD rehab, 18% completion, F-COMP-9). Dozee Pro Ex (2023) extends bed monitoring to home (snippet). ConnectedLife at Manipal, Tricog, Zorgers and Amrita's Smart CABGuard as in F-COMP-11 and F-COMP-12.
- Source: S13 (C); snippets (C); known findings
- Status: **CONFIRMED** that none measures breathing exercise, across all sources read.
- So what: the "after discharge" space is filling up with general check-in tools. Our edge is an objective measure of one exercise that surgeons already prescribe.

### B7-17: Abroad, app-based prehab and post-op rehab is consolidating
- Detail: Surgery Hero (UK digital prehab) was bought by Sword Health in Jan 2025; PrehabM (Germany) is CE-marked; China ran a 136-patient RCT of a home rehab app after lung surgery (lung function recovery 79.3% vs 75.7%, P=.04) and has a 340-patient IoT breathing-training RCT under way (results not yet out).
- Source: S7 (Lv et al., *Int J Surg* 2025) (A); S6 (Hang et al., *Digit Health* 2026, protocol) (A); snippets (C)
- Status: China studies **CONFIRMED**; Surgery Hero sale **NOT CONFIRMED** (database snippet).
- So what: digital post-surgery rehab can show measurable benefit in an RCT (China), and larger health-tech firms are buying in. Useful for the "this is a real category" slide.

### 4. Does incentive spirometry actually work? (the judges' likely hard question)

### B7-18: Largest review: incentive spirometry alone gives little to no reduction in lung complications
- Detail: Sullivan et al., *Respiration* 2021: 31 RCTs, 3,776 adults after heart, chest or upper-abdominal surgery. Spirometry alone vs other chest physiotherapy: 30-day lung complications RR 1.00 (95% CI 0.88–1.13); 30-day death RR 0.73 (0.42–1.25); hospital stay −0.17 days (−0.65 to 0.30). Authors' wording: IS alone "likely results in little to no reduction" in these outcomes.
- Source: S2 (A)
- Status: **CONFIRMED** (agrees with Cochrane 2014, F-CLIN-3, and the 2024 cardiac review, F-CLIN-7)
- So what: never say "spirometry prevents pneumonia". The comparison is against **other active breathing care**, not against nothing.

### B7-19: After lung-cancer surgery, reviews do find a benefit, mostly as part of a bundle
- Detail: Chang et al., *Asian J Surg* 2023: 5 RCTs + 3 cohort studies, 10,322 patients after lung resection: lung complications OR 0.68 (0.51–0.90), pneumonia OR 0.82, stay 1.8 days shorter; more benefit when pre-surgery lung function was below 80%. Liang 2024 (F-CLIN-6): benefit when combined with other breathing therapy.
- Source: S3 (A); #80 (A)
- Status: **CONFIRMED** (two reviews)
- Caveat: most of Chang's patients come from observational studies, which are weaker than trials. Don't quote "32% fewer complications" without that caveat.

### B7-20: No newer review or guideline changes the picture
- Detail: Two Europe PMC searches (2020–2026) found no new surgical review after 2024 (only reviews in sickle-cell disease, COVID, rib fractures and spinal-cord injury). The AARC 2011 guideline is still the latest: don't use spirometry alone; combine it with deep breathing, coughing, walking and pain control; deep breathing exercises give "the same benefit" (F-CLIN-4).
- Source: S1, S4 (A); AARC snippet (C)
- Status: **CONFIRMED** (as of 10 Oct 2026, within these searches)

### B7-21: The gap SpiroBuddy fills: none of these trials measured whether the exercise was done
- Detail: Cochrane 2014 states adherence was not recorded (F-CLIN-3). 86% of US nurses say adherence is poor (F-ADH-2). Hourly reminders doubled use in one RCT (F-ADH-1). Pre-surgery breathing-muscle training (a different device) has stronger evidence for fewer complications (Cochrane 2015 and other reviews, snippets only, C).
- Status: adherence gap **CONFIRMED**; muscle-training evidence **NOT CONFIRMED** this round (snippets).
- So what (judge answer, 3 sentences): "On its own, the spirometer is no better than other breathing exercise. That's why we coach whatever the physio prescribes, including plain deep breathing, and measure it. No trial has ever known whether patients actually did their breaths; we make that visible to the nurse." Also note a future path: our base and coach could track a breathing-muscle trainer, which has better evidence (05 roadmap).

### B7-22: What to stop saying
- Don't say "first smart incentive spirometer" (InSee, Airalux, Michigan exist).
- Don't say "first app to coach incentive spirometry" (QUT Inspire, Go-breath, ZEPHYRx exist).
- Don't say "incentive spirometry prevents pneumonia" (B7-18).
- Safe line: "first home-use, Indian-language breathing coach that measures an ordinary spirometer and loops in the nurse and family, as far as we could find."

### 5. Which spirometers Indian hospitals buy

### B7-23: There is no public market-share figure for spirometer types or brands in India
- Detail: No market report, tender result, import record or survey this round gave a split between three-ball and volume types, or between brands. Indian physiotherapy surveys say over 90% use incentive spirometry around chest surgery but don't ask which type (PMC5107873, already in our files; snippets). Market-report sites give global market sizes from US$185 million to US$1.12 billion, which disagree too much to use. Import data (HS code 9019) sits behind paid Volza/Zauba accounts. No GeM or AIIMS tender naming the type was found.
- Source: S8, S9 (A); many snippets (C)
- Status: **CONFIRMED** that no figure is public.
- Ask: Romsons' sales team, any hospital stores officer, or a GeM search by a registered buyer.

### B7-24: Every proxy points to the three-ball type being common, especially for cost-pressed wards and home use
- Detail:
  - Wholesale listings: three-ball units at ₹56–145 each (IndiaMART, several sellers, snippets) against the Breazer volume type at MRP about ₹1,067 (F-INDIA-3). An earlier count found 23 of 28 IndiaMART listings were three-ball and none volume type (E-12).
  - Romsons, the most visible Indian brand, sells both: the SH-6082 Respirometer (three-ball, 600/900/1,200 mL/s) and the Breazer 2500 (volume).
  - Indian studies use both: JIPMER's ERAS gastrectomy RCT used a **volume** device before surgery; the Mangalore RCTs compared flow and volume (F-CLIN-9); the Chennai adherence study used the flow type (#157); a 2025 Delhi/Kolkata bypass trial did not name the type.
  - Popular Hindi videos mostly show three-ball devices (F-INDIA-10).
- Source: S8, S9 (A); snippets (C); known findings
- Status: "three-ball is common" **SINGLE SOURCE** in kind (trade listings); a share figure is **NOT CONFIRMED**.
- So what: supply the volume spirometer with our unit for now (E-12), and make a three-ball reader the first extension. The phone-camera route (B7-11) may be the cheapest way to do that.

---

## What this means for the pitch (one paragraph)
We are not the first to put electronics on an incentive spirometer, and we should say so before a judge does. Hardware rivals are few, mostly American, hospital-only and stuck at trial stage. The serious medium-term threat is a phone-only app, from a research group or from Cipla or Lupin. Our answer is to be the coaching, nurse and family layer, to accept breaths from any source (our base, a phone microphone or camera, or a manual tap), and to win on elders without smartphones and on Indian languages. The honest evidence line is: "the exercise helps as part of the nurse's bundle when it is actually done; we make sure it is done and prove it."

## Open questions (who can answer)
1. Share of three-ball vs volume spirometers in Indian surgical wards: Romsons sales, a hospital stores officer, a GeM-registered buyer.
2. Is InSee entering India or any Asian market? Ask Tidal Medical directly.
3. Did Lungy Health ever register as a medical device? MHRA public database (not searched).
4. Does Cipla's Breathefree app or Lupin's LYFE plan a post-surgery breathing module? Ask their medical affairs teams; could be a partnership lead.
5. Indian patent office (InPASS) search for spirometer trackers: still not done (F-COMP-8).

---

## Sources opened this round

| # | URL | Title | Publisher / type | Grade | Used in |
|---|---|---|---|---|---|
| S1 | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE:"incentive spirometry" AND (systematic review OR meta-analysis) AND PUB_YEAR:[2020 TO 2026] | Search: IS systematic reviews 2020–2026 (6 hits) | Europe PMC | A | B7-20 |
| S2 | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:34274935%20AND%20SRC:MED&resultType=core&format=json | Sullivan et al., IS after cardiac, thoracic and upper-abdominal surgery, SR/MA, *Respiration* 2021;100:1114–27 (abstract) | Europe PMC | A | B7-18 |
| S3 | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:36437210%20AND%20SRC:MED&resultType=core&format=json | Chang et al., IS after pulmonary resection, SR/MA, *Asian J Surg* 2023;46:3397–404 (abstract) | Europe PMC | A | B7-19 |
| S4 | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=(ABSTRACT:"incentive spirometry" …) AND ("meta-analysis" OR "systematic review") AND PUB_YEAR:[2024 TO 2026] | Search: IS reviews 2024–2026 (6 hits) | Europe PMC | A | B7-20 |
| S5 | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=("incentive spirometer" OR … triflo) AND ("computer vision" OR camera OR smartphone OR microphone OR bluetooth OR sensor) AND PUB_YEAR:[2018 TO 2026] | Search: technology + IS 2018–2026 (60 hits) | Europe PMC | A | B7-11 |
| S6 | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:41996546%20OR%20EXT_ID:35760497%20OR%20EXT_ID:34640793%20OR%20EXT_ID:42183304&resultType=core&format=json | Alrubaie 2026 *Anesthesiology* (ISTracker); Baxter 2022 *BMJ Open Respir Res* and 2021 *Sensors* (QUT Inspire; alias PMC8513019); Hang 2026 *Digit Health* (IoT rehab protocol) | Europe PMC | A | B7-3, B7-10, B7-17 |
| S7 | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40035777%20OR%20EXT_ID:42539818%20OR%20EXT_ID:38905505%20OR%20EXT_ID:42505437&resultType=core&format=json | Pearkao 2025 (Thai lung-exercise game); Subramaniam 2026 (Malaysia, mobile learning after CABG); Lv 2025 *Int J Surg* (POPPER RCT); Yuenyongchaiwat 2026 *Biosensors* (**re-open**, already in #120) | Europe PMC | A | B7-17, table |
| S8 | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=("incentive spirometer" OR "incentive spirometry") AND (AFF:India OR ABSTRACT:India) AND ("flow-oriented" OR … "three ball") | Search: Indian IS studies by device type (16 hits) | Europe PMC | A | B7-23, B7-24 |
| S9 | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:42147401%20OR%20EXT_ID:38738205%20OR%20EXT_ID:41947623%20OR%20EXT_ID:41261614%20OR%20EXT_ID:32739548&resultType=core&format=json | SGPGI 2025, AIIMS 2024 (tracheostomy IS), AIIMS 2026 HIPEC ERAS, Batra/Peerless 2025 CABG RCT, JIPMER 2020 ERAS gastrectomy RCT | Europe PMC | A | B7-24 |
| S10 | https://indiamedtoday.com/cipla-introduces-ai-powered-mobile-application-to-transform-asthma-screening-in-india/ | Cipla introduces AI-powered app for asthma screening (18 Dec 2024) | India Med Today (press reprint) | C | B7-14 |
| S11 | https://www.atsconferencenews.org/pitch-for-incentive-spirometry-device-wins-2025-bear-cage-competition/ | Pitch for incentive spirometry device wins 2025 BEAR Cage (21 May 2025) | American Thoracic Society conference news | B | B7-2 |
| S12 | https://www.ucl.ac.uk/news/2022/nov/smartphone-tech-responds-breathing-could-benefit-asthma-copd-and-long-covid-patients | Smartphone tech that responds to breathing (UCL, Nov 2022) | UCL | – | nothing read (HTTP 403); snippet used in B7-5 |
| S13 | https://mediwatch.in/ | Mediwatch post-surgery patient monitoring | small company / individual | C | B7-16 |
| S14 | https://www.breathinglabs.com/pulmonary-diseases/how-a-new-app-could-help-ten-million-britons-with-long-covid-asthma-and-copd/ | How a new app could help ten million Britons (Lungy Health; date shown "19 March", year likely 2023) | Breathing Labs (news aggregator) | C | B7-5 |
| S15 | https://clinicaltrials.gov/api/v2/studies/NCT04429009 | RCT of ZEPHYRx gamified incentive spirometry vs traditional (Rochester) | ClinicalTrials.gov | A | B7-4 |
| S16 | https://www.ucl.ac.uk/news/headlines/2023/mar/how-new-app-could-help-ten-million-britons-long-covid-asthma-and-copd | UCL news, Mar 2023 (Lungy Health) | UCL | – | nothing read (HTTP 403); same story as S14 |
| S17 | https://patents.justia.com/patent/20180360346 | Electronic incentive spirometer (Justia copy) | Justia | – | nothing read (HTTP 403); read via S19 |
| S18 | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:38875693%20OR%20EXT_ID:40327873%20OR%20EXT_ID:41214067&resultType=core&format=json | Burns 2023, Yuenyongchaiwat 2025, Mera 2025 abstracts | Europe PMC | A | **re-open** of #50 and #120 by another address (should not have been opened); added only: Thai RCT comparator was Triflo; Burns tracks the flow bobbin |
| S19 | https://patents.google.com/patent/US20180360346A1/en | US20180360346A1, Electronic incentive spirometer (abandoned) | Google Patents | A | B7-7, B7-12 |
| S20 | https://patents.google.com/xhr/query?url=q%3D%22incentive%2Bspirometer%22%2Bcamera%2Bimage%26after%3Dpriority%3A20150101 | Google Patents search: "incentive spirometer" camera image, priority after 2015 (21 hits, page 1) | Google Patents | C | B7-11 |
| S21 | https://techtransfer.universityofcalifornia.edu/NCD/31772.html | UCLA incentive spirometry system, case 2016-288 (© 2019) | UC tech transfer | B | B7-6 |
| S22 | https://www.morganlewis.com/news/2026/08/morgan-lewis-advises-zephyrx-in-sale-to-clinical-research-organization | Morgan Lewis advises ZEPHYRx in sale (18 Aug 2026) | Morgan Lewis (law firm) | B | B7-4 |
| S23 | https://www.lupin.com/?p=36537 | Lupin press release (expected LYFE Class C) | Lupin | – | nothing useful (page showed a different news item) |
| S24 | https://www.healthcareitnews.com/news/asia/dozee-bets-indias-growing-home-healthcare-market-new-solution | Dozee bets on India's home healthcare market | Healthcare IT News | – | nothing read (HTTP 403); snippet used in B7-16 |
| S25 | https://indiamedtoday.com/27504-2/ | First chronic condition management platform recognised as Class C SaMD (Lupin LYFE, 3 May 2024) | India Med Today (press reprint) | C | B7-15 |

**Search-result summaries used but NOT opened (grade C):** MIR Smart One / Spirobank Smart pages, CMI SpiroLink listings (US$87.99–109.99); Teleflex India IS page; IndiaMART three-ball listings (₹56–145; one ₹600); hospitalstore.com; Romsons Respirometer listings (healthklin, 1mg, medplusmart); market-report sites (datastring, growthmarketreports, marketresearchintellect, marketreportanalytics: BD "wireless IS" claim); AirLife product page; Bedfont Breathacise; CB Insights / BioSpace / fdanews on InSee; FDA EUA documents (fda.gov/media/150487-9); biobuzz.io, sciencecenter.org, PitchBook and opengrants on Airalux; Justia trademarks (SPIROTIMER, serial 98731904); mdpi Adv Respir Med 88/6 (SpiroTimer survey); Design Week, wepresent, tapsmart, App Store on Lungy; nzdoctor; IIT Guwahati PEEP spirometer (PMC12168515); Swaasa (BioSpectrum, Tata Trusts, medRxiv 2023.10.02.23296452 and 2025.01.27.25321216); Cipla Breathefree centre (biovoicenews, indianpharmapost); Lupin LYFE (BioSpectrum 22532, uniindia VITALYFE); Dozee (BioSpectrum 18565, indianpharmapost Pro Ex, fitgap); Carely; Buddy Healthcare; Surgery Hero (seedtable); PrehabM; Fit4Surgery (PubMed 40043662); IMT reviews (PubMed 26436600, PEDro records, PMC9251477); AARC 2011 guideline pages; respiratorytherapyzone; Indian physiotherapy surveys (bisp-surf PMC5107873 record, Manipal researcher pages); Chilean volume-vs-flow IS study (world.physio); globallinker HS code 90191090; Volza/Zauba pages; UW capstone pages; Reyes 2016 *Sensors* (PMC4813972); USPTO patents 7591789, 7998085, 11045112, 10028675; US12179058B2; Morgan Lewis language variants.
