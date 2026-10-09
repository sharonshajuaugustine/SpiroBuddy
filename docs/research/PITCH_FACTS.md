# Pitch facts (slide-ready)

Rewritten at the end of each round. Only A/B-graded facts unless labelled. Finding IDs (F-…) and ledger numbers (#) point to KNOWLEDGE_BASE.md and SOURCES_LEDGER.md. **Round 4, 9 Oct 2026.** Judge Q&A: see the "JUDGE" table at the end of KNOWLEDGE_BASE.md.

## The problem
1. **About 1 in 10 adults having surgery gets a lung complication** (10.4% of 9,864 patients, 146 hospitals, 29 countries). LAS VEGAS, *Eur J Anaesthesiol* 2017. **A**. F-CLIN-1
2. **When a lung complication happens, about 1 in 5 patients dies within 30 days: 19.5% vs 0.5% without one** (2,464 patients, Spain). Canet et al., *Anesthesiology* 2010. **A**. This shows a link, not proof of cause. F-CLIN-2
3. **In India too: in a Udaipur study, patients with lung complications stayed 21.7 days in hospital instead of 12.5 and 8.5 days in ICU instead of 1.4, and 28% of them died.** *Int Surg J* 2018. **A** (small, single centre). F-CLIN-8
4. **86% of US nurses and respiratory therapists say patients don't use their spirometer as they should. The top reason: patients forget (83.5%).** Eltorai et al., *Respir Care* 2018, 1,681 respondents. **A**. F-ADH-2
5. **In India, 1 in 4 cancer-surgery patients in Hyderabad couldn't do the exercise correctly, mostly because they didn't understand the instructions or lacked family support.** *Anesth Essays Res* 2018, 100 patients. **A** (small study). F-ADH-4

## Why India needs a different design
6. **Three in four older Indian women can't read (literacy 24%), and over a third of older Indians have low vision (37%).** So SpiroBuddy speaks. LASI Wave 1 (government survey). **A**. F-INDLOC-3
7. **Two in three older Indians live with their children; only about 6% live alone.** So the WhatsApp update goes to the family. LASI Wave 1. **A**. F-INDLOC-3
8. **Only 41% of older Indians own a smartphone.** HelpAge India 2025 (via Deccan Herald). **B**, single source. F-INDIA-5
9. **Hindi is the mother tongue of only 43.6% of Indians**, and 57% of Indian internet users prefer their own language. Census 2011; IAMAI–Kantar 2024. **B**. F-INDIA-8, F-INDIA-6
10. **India has 2.6 registered nursing staff per 1,000 people, below the WHO benchmark of 3.** Rajya Sabha reply, July 2026. **B**. F-INDIA-7

## Proof that tracking and reminders help
11. **An hourly reminder doubled the share of waking hours in which patients did their breathing exercise: 58% vs 28%** (randomised trial, 145 heart-bypass patients, USA). Eltorai et al., *JAMA Surgery* 2019. **A**. F-ADH-1. *Say "hours", not "patients".*
12. **The same trial: breaths per day doubled (35 vs 17), with slightly less lung collapse on X-ray.** **A**. F-ADH-1
13. **A 2024 review of 9 trials (1,209 lung-cancer patients): spirometry used as part of a breathing-exercise bundle cut lung complications and shortened hospital stays.** *BMC Pulm Med* 2024. **A**. F-CLIN-6
14. **Home lung rehab with phone follow-up works in India: 246 of 260 TB survivors at 5 centres completed 12 weeks, with better walking distance and quality of life.** *Indian J Med Res* 2025. **A** (no comparison group). F-VIS-1

## The idea is proven, but not for India
15. **The FDA cleared InSee, a clip-on spirometer tracker, on 21 August 2025 (K241152). It reads the piston with an infrared sensor (like ours), fits only one US spirometer and is cleared for hospital use only.** FDA database; IEEE Spectrum 2020. **A/B**. F-COMP-1, F-COMP-5
16. **Positioning line:** "InSee proved laser tracking of a spirometer works in US hospitals. SpiroBuddy adds what India needs: AI that checks *how* you breathe, a voice coach in Indian languages, home use, and WhatsApp updates for the family."

## How the exercise should be done (justifies our scoring)
17. **Standard instructions: breathe in slowly, hold 3–5 seconds, about 10 breaths every waking hour.** MedlinePlus 2025 and Cleveland Clinic 2026. **B**, two sources agree. F-CLIN-5
18. **The US guideline suggests a volume-type device (what SpiroBuddy reads), used together with deep breathing, coughing, walking and pain control.** An Indian trial (Mangalore 2016) found the volume type gave better walking-test gains. AARC 2011; *J Clin Diagn Res* 2016. **A**. F-CLIN-4, F-CLIN-9

## Money and who pays
19. **Ayushman Bharat pays hospitals a flat ₹1,62,400 for a bypass (CABG), with a 10-day stay built in. Any extra days from a complication come out of the hospital's pocket.** HBP 2022 rate list (state copy). **A**. F-BIZ-1
20. **Indian chains already pay for home monitoring after surgery** (Manipal + ConnectedLife, 2022, for bypass and knee replacement patients). **B**. F-BIZ-3
21. **A WhatsApp update costs about 12 paise (₹0.115, Meta's India utility rate). An AI phone call costs about ₹8 for 2 minutes, roughly 70 times more.** So: WhatsApp first, calls only to escalate. Meta rate card; Plivo + Sarvam prices (our maths). **B**. F-COMMS-2, F-COMMS-11
22. **Voice in 11 Indian languages: Sarvam at ₹3 per 1,000 characters (about 60 paise per coaching message), with ₹100 free credits. A free offline backup (AI4Bharat Indic-TTS, MIT licence) also exists.** **B**. F-VOICE-1–3, F-VOICE-10

23a. **What a hospital day costs in India: about ₹2,307 per ward bed-day on average (57 hospitals, 11 states) and ₹25,927 per ICU bed-day at PGIMER.** CHSI, *BMJ Open* 2023; *Lung India* 2024. **A**. F-BIZ-4, F-BIZ-5. *Back-of-envelope only:* a week of extra ICU from a lung complication ≈ up to ₹2 lakh. Label it as our estimate.
23b. **Unit economics (team estimate): about ₹1,000–1,700 of parts per reusable clip-on (≈ ₹150 a patient over 10 uses) and about ₹5 of WhatsApp per 14-day recovery. Price idea: ₹500–1,000 per patient, less than half of one ward day.** F-BIZ-7 (not a source).
23c. **Demand beyond surgery: NTEP asks for every patient finishing TB treatment to be checked for post-TB lung disease, with home-based rehab plans; in Pune, 87% of 370 lung patients wanted rehab and 84% liked a home digital programme.** NTEP standards; *Chron Respir Dis* 2024. **A**. F-VIS-2, F-VIS-3

## Honest limits (say them before judges ask)
23. **The evidence that incentive spirometry alone prevents complications is weak** (Cochrane 2014; a 2024 cardiac-surgery review found it no better than standard breathing care). **But those trials rarely recorded whether patients actually did the exercise. SpiroBuddy makes that visible.** **A**. F-CLIN-3, F-CLIN-7
24. **It's an exercise coach and tracker, not a diagnostic.** CDSCO's 2026 software guidance (primary text): wellness software may not name any disease, and software that monitors or **alerts** about a condition is a medical device. Standalone software that only *informs* care of a serious condition is Class A in its table, but a measuring device still needs a licence. **A**. F-REG-4, F-REG-1, F-REG-2
25. **Calls: TRAI's 2026 rules treat AI voice calls as "A2P calls". They need advance declaration, an Indian registered caller ID and, for some reminder calls, consent the patient renews weekly.** So calls are an escalation step: the nurse clicks "call" and a human talks to the patient. WhatsApp and the device do the daily work. **A**. F-COMMS-8, F-COMMS-12, F-COMMS-13
26. **Accuracy: the sensor chip is ±2 cm out of the box but very steady, so we calibrate it to each spirometer's printed marks and narrow its view (27° → about 15°) so tube walls don't confuse it. Even eye-reading of these scales varies by hundreds of mL.** ST datasheet; ST forum; Thai study 2026. **A/B/C**. F-TECH-1, F-TECH-2, F-TECH-3

Never say: "prevents pneumonia", "first in the world", "laser sensing is our invention", "diagnoses", "₹X saved per patient" (we have day-cost anchors, not a measured saving), "CDSCO-approved", "no regulation applies".
