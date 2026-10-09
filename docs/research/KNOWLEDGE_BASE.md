# SpiroBuddy research knowledge base

Kept by the research agent; saved by the lead for round 1. Grades: **A** = peer-reviewed study, guideline or regulator data · **B** = reputable organisation, major news or company official page · **C** = retailer, blog or press release. Ledger numbers (#n) point to `SOURCES_LEDGER.md`. Last updated: 9 Oct 2026, round 3 (about 30 more reads; see "Round 3 additions" and "JUDGE" at the end; Claim check, risks and open gaps updated in place).

## VOICE – Indian voice AI (Sarvam AI first)

### F-VOICE-1: Sarvam gives ₹100 of free credits at signup, and the credits never expire
- Detail: the ₹100 works across all Sarvam APIs. After that it's pay as you go (₹1 = 1 credit), with no monthly fee and no expiry. When credits run out, API calls return errors.
- Source: Sarvam docs, Credits & Rate Limits – https://docs.sarvam.ai/api/getting-started/ratelimits.md (#55); Sarvam API Pricing – https://www.sarvam.ai/api-pricing (#53) – B
- Use: the demo can run on the free credits. Keep the browser-voice fallback for when they run out.
- Caveat: company pages; terms can change.

### F-VOICE-2: Text-to-speech costs ₹3 per 1,000 characters; speech-to-text ₹30 per hour
- Detail:
  - Text-to-speech: ₹3.00 per 1,000 characters.
  - Speech-to-text: ₹30 per hour, or ₹45 with speaker separation.
  - Translation: ₹0.005 per character.
  - Sarvam 105B chat model: ₹29.28 input / ₹73.20 output per 1M tokens.
  - Our maths: a 200-character coaching message costs about ₹0.60, and ₹100 buys about 33,000 characters of speech.
- Source: #53 – B
- Use: "Voice coaching in 11 languages costs paise per message."

### F-VOICE-3: Bulbul v4 Flash is the newest model; Bulbul v3 is the default and covers 11 languages
- Detail:
  - `bulbul:v4-flash` has 222 voices, but they cover only Hindi, English, Hindi-English mix, Bengali, Gujarati, Kannada, Marathi, Punjabi, Tamil and Telugu. No Malayalam or Odia.
  - `bulbul:v3` is the default. It has 30+ voices (Shubh, Priya, Ritu, Kavya, Anand, Roopa…) and covers Hindi, Bengali, Tamil, Telugu, Gujarati, Kannada, Malayalam, Marathi, Punjabi, Odia and Indian English.
  - Speed can be set from 0.5x to 2.0x. Requests can be up to 2,500 characters. The Starter plan allows 30 requests per minute on v3.
- Source: https://docs.sarvam.ai/api/getting-started/models/bulbul.md (#54); TTS overview (#17) – B
- Build notes: use v3 for Malayalam and Odia. Pick a calm voice, not the v4 advertising-style default `shubh_enhi_ads`. Use mp3 or wav, because `opus` output currently errors.
- Caveat: our "under 250 ms" claim is not checked.

### F-VOICE-4: Audio made with credits, including the free ₹100, can be used commercially
- Detail: voice cloning needs the voice owner's consent.
- Source: https://docs.sarvam.ai/api/getting-started/commercial-licensing.md (#56) – B
- Caveat: the EULA and terms on health use are not read yet.

### F-VOICE-5: "Saarika" speech-to-text is deprecated; use "Saaras"
- Detail: the whole platform claims 22 Indian languages. Text-to-speech and voice agents cover 11.
- Source: https://docs.sarvam.ai/llms.txt (#57) – B

### F-VOICE-6: Sarvam Voice Agents handle phone calls in 11 languages, with guides for Twilio and Exotel
- Detail:
  - Handles mixed-language speech, inbound and outbound calls, your own telephony or a Sarvam number.
  - "Appointment booking and reminders" is a listed use case.
  - WhatsApp voice agents are enterprise-only.
  - The Twilio guide is about 80 lines of Python (Twilio Media Streams + Pipecat + Sarvam).
- Source: https://docs.sarvam.ai/conversations/overview.md (#59); https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio.md (#58) – B
- Caveat: per-minute price is not checked.

## COMMS – calls and WhatsApp in India

### F-COMMS-1: Twilio calls to India need a non-Indian caller ID; voice OTP calls are banned; consent is required
- Detail:
  - Outbound calls show an international caller ID (for example +1…).
  - Many short calls can trigger carrier blocks.
  - Indian toll-free numbers can only receive calls, not make them.
  - Calls without consent count as unsolicited commercial communication (UCC) under TRAI, and the account can be blocked.
- Source: Twilio India Voice Guidelines (dated 8 Oct 2026) – https://www.twilio.com/en-us/guidelines/in/voice (#60) – B
- Use: demo calls work with a foreign caller ID. A real product needs an Indian provider such as Exotel or Plivo, and must record consent.

### F-COMMS-2: WhatsApp in India (from 1 Oct 2026): utility ₹0.115 per message, marketing ₹0.8631
- Detail:
  - Meta charges per message, for business-sent messages only.
  - Authentication and service messages are also ₹0.115.
  - Starting a conversation needs an approved template.
  - Free-form messages are allowed within 24 hours of the user writing, and replies in that window are free.
  - Each business number gets 1,000 free service messages a month.
- Source: https://developers.facebook.com/docs/whatsapp/pricing (#61); INR rate card (#62) – B
- Use: "A family update costs about 12 paise." 14 reminders a day costs about ₹1.6 per patient per day.
- Caveat: promotional wording gets billed as marketing, at about 7x. Twilio's own fee is not checked.

## CLIN – clinical evidence

### F-CLIN-1: About 1 in 10 surgical patients gets a lung complication (10.4% of 9,864)
- Detail: LAS VEGAS study, 146 hospitals, 29 countries. Rates: 7.0% in low-risk patients and 19.2% in higher-risk patients.
- Source: *Eur J Anaesthesiol* 2017;34:492–507 – https://pmc.ncbi.nlm.nih.gov/articles/PMC5502122 (#35) – A
- Caveat: mostly European hospitals.

### F-CLIN-2: 30-day death rate: 19.5% with a lung complication vs 0.5% without
- Detail: ARISCAT study, 2,464 patients, Catalonia.
- Source: Canet et al., *Anesthesiology* 2010 (#36) – A
- Caveat: shows a link, not proof of cause; single source.

### F-CLIN-3: Cochrane 2014: no proof that incentive spirometry prevents complications after upper-abdominal surgery
- Detail: 12 randomised trials, 1,834 people. Risk ratio 0.59 (95% CI 0.30–1.18). Evidence quality low. **Adherence was never recorded.**
- Source: CD006058, PMID 24510642 (#39) – A
- Use: on the honest-limits slide. SpiroBuddy produces the missing adherence data.

### F-CLIN-4: AARC 2011 guideline: don't rely on incentive spirometry alone
- Detail: combine it with deep breathing, coughing, walking and pain control. A volume-oriented device is suggested.
- Source: Restrepo et al., *Respir Care* 2011;56:1600–4 (#42) – A
- Use: present SpiroBuddy as part of a nurse-led care bundle.

### F-CLIN-5: Standard technique: slow breath in, hold 3–5 s, about 10 breaths every 1–2 waking hours
- Source: MedlinePlus 2025 (#44); Cleveland Clinic 2026, which says hold ≥5 s (#45) – B
- Use: justifies our scoring. Let nurses raise the hold target to 5 s.

## ADH – adherence

### F-ADH-1: Hourly reminder doubled the share of waking hours with use (58% vs 28%)
- Detail:
  - Randomised trial, Rhode Island, 145 heart-bypass (CABG) patients analysed.
  - Breaths per day: 35 vs 17. Final X-ray (atelectasis) score: 1.5 vs 1.8, P=.04.
  - Non-elective patients needed less non-invasive breathing support (19% vs 37%).
- Source: Eltorai et al., *JAMA Surgery* 2019 – https://pmc.ncbi.nlm.nih.gov/articles/PMC6583822 (#2) – A
- Caveat: counts hours, not patients. One hospital. The author filed a patent on the reminder device.

### F-ADH-2: 86% of 1,681 US nurses and respiratory therapists say adherence is poor
- Detail: reasons given: patients forget (83.5%), use it ineffectively (74.4%), or don't use it often enough (70.7%).
- Source: *Respir Care* 2018;63:532–7 (#48) – A

### F-ADH-3: Penn's Airalux trial: 14.7 sessions a day; more use was linked to shorter stays
- Detail: 30 patients, no control group.
- Source: NCT06629454 (#5); AATS abstract (#6); Penn listing (#34) – A/B

### F-ADH-4: Hyderabad: 26 of 100 cancer-surgery patients couldn't use the spirometer correctly
- Detail: main reasons: didn't understand the instructions, too little practice, limited family support.
- Source: *Anesth Essays Res* 2018 – https://pmc.ncbi.nlm.nih.gov/articles/PMC6020596 (#47) – A
- Use: **Indian evidence** for a voice coach in their language, technique AI and family involvement.

### F-ADH-5 (against us): Korea's Go-breath (hourly alarm 9 am–9 pm + nurse dashboard, 42 patients) showed no significant benefit
- Detail: P=.22, but 38 of 42 patients found it useful. Use was self-reported, with no sensor.
- Source: *JMIR mHealth uHealth* 2019;7:e12204 (#52) – A

## COMP – competitors and prior art

### F-COMP-1: InSee
- Detail:
  - FDA 510(k) K241152, cleared 21 Aug 2025, Class II, code BWF.
  - Made by Tidal Medical. Fits only the AirLife 2500/4000. Hospital use, prescription only.
  - Mounts at the base. Reminder intervals: 10–120 min. Its predicate is K781838, a 1978 Bard device.
- Source: FDA database (#31); FDA letter (#3) – A

### F-COMP-2: Prior-art list
- InSee, SpiroTimer, Airalux, the Michigan optical add-on, Go-breath.
- Seen only in search results: NCT03686631, TryBreath NCT07528222, QUT "ISy".
- No Indian product found yet.

### F-COMP-3: Airalux is a whole new spirometer, not a clip-on
- Source: #34 – B

### F-COMP-4: Michigan optical clip-on (2023)
- Detail: piston tracking 99% accurate, volume within 7.5%, breath classification 100% sensitivity / 99% specificity.
- Source: Burns et al., *JMIR Biomed Eng* 2023;8:e46653 (#50) – A
- Use: shows our approach is technically sound. It is also the closest prior art.

## INDIA

### F-INDIA-1: About 356 major surgeries per 100,000 people (2019); about 4.9 million a year
- Detail: unmet need of about 49 million procedures. Growing about 4% a year.
- Source: Int J Surg 2024 – https://pmc.ncbi.nlm.nih.gov/articles/PMC10942208 (#63) – A
- Caveat: the data source (HMIS) misses much of the private sector, so this is an undercount.

### F-INDIA-3: Romsons Breazer 2500: MRP about ₹1,067; online prices about ₹146–₹960
- Source: #7, #8 – C

### F-INDIA-4: Romsons SH 6082 is a 3-ball flow-type device (MRP ₹688)
- Detail: our disc sensor can't read it.
- Source: #33 – C

---
# Round 2 additions (9 Oct 2026)

## INDIA (round 2)

### F-INDIA-5: Only 41% of older Indians own a smartphone, and just 13% use the internet or social media
- Detail: HelpAge India report "Understanding Inter-generational Dynamics & Perceptions on Ageing" (released 14 Jun 2025). 71% of elders use basic phones, 41% own a smartphone, 13% use the internet or social media, and 5% use online services such as banking or health apps. 88% of communication between generations is still face to face.
- Source: Deccan Herald, 14 Jun 2025, reporting the HelpAge India report – https://www.deccanherald.com/india/karnataka/bengaluru/88-seniors-offline-helpage-urges-action-3585484 (#65) – Grade B
- Use in pitch/build: **send WhatsApp updates to a family member (the caregiver), not only to the patient**. The bedside device and voice coach must work for a patient with no smartphone.
- Caveat: news report of an NGO survey. Sample size, age cut-off and method not seen. Single source. City surveys show higher ownership (e.g. 65% in one Tribune-reported city survey, not opened).

### F-INDIA-6: India has 886 million active internet users (2024); 57% prefer content in Indian languages
- Detail: IAMAI–Kantar "Internet in India 2024" (ICUBE survey, 90,000+ households): 886 M active users (+8% a year), 488 M rural vs 397 M urban, and women are 47% of rural users. 57% prefer regional-language content. Of the 41% still offline, 13% cite the lack of local-language content.
- Source: Business Today, 16 Jan 2025 – https://www.businesstoday.in/amp/technology/news/story/indias-internet-revolution-key-insights-from-kantar-and-iamai-report-461043-2025-01-16 (#64) – Grade B
- Use in pitch: "Most Indian internet users prefer their own language, so our coach speaks it."
- Caveat: secondary report. No age split found.

### F-INDIA-7: India has 2.60 registered nursing personnel per 1,000 people, below the WHO benchmark of 3, and far fewer in the north and east
- Detail: Health Minister's Rajya Sabha reply, 21 Jul 2026: 46.02 lakh registered nursing personnel (31 Dec 2025), i.e. 2.60 per 1,000. Registered nurses and midwives alone: 34.88 lakh (2.45 per 1,000). Kerala has 10.47 per 1,000 and Karnataka 7.69, while many northern and eastern states lag far behind. The earlier Lok Sabha figure (Mar 2025) was 2.20 per 1,000.
- Source: The South First, 24 Jul 2026, quoting the Rajya Sabha reply – https://thesouthfirst.com/health/south-india-leads-indias-nursing-workforce-as-national-ratio-remains-below-who-benchmark/ (#67) – Grade B (the primary Sansad PDF timed out, #66)
- Use in pitch: "India has fewer nurses than WHO recommends, and they can't watch every patient's breathing exercises at home. SpiroBuddy shows them who needs a call."
- Caveat: registered ≠ working (migration abroad). **Ward-level nurse-to-patient ratios were not found.**

### F-INDIA-8: Hindi is the mother tongue of only 43.6% of Indians (Census 2011)
- Detail: Hindi 43.63%, Bengali 8.03%, Marathi 6.86%, Telugu 6.70%, Tamil 5.70%, Malayalam 2.88%. The 22 scheduled languages cover 96.72% of mother tongues. 13 languages are each the mother tongue of over 1 crore people.
- Source: Factly, 29 Jun 2018, citing Census 2011 Statement 5 – https://factly.in/a-major-dravidian-language-is-now-the-mother-tongue-of-only-18-9-indians-down-from-23-in-1971 (#69) – Grade B. Also seen on Scroll (#68), whose numbers were in charts.
- Use in pitch: "A Hindi-plus-English app misses more than half of India. Sarvam's 11 languages cover the large majority." (The six languages above add up to 73.8%. Don't claim a higher total until the other five are checked.)
- Caveat: census data is from 2011 and counts mother tongue only, not second languages.

### F-INDIA-9: Heart bypass (CABG), angioplasty, hip fracture fixation and knee replacement are among the top procedures under Ayushman Bharat PM-JAY
- Detail: Lok Sabha reply (Jul 2019): the top 5 PM-JAY procedures were angioplasty (PTCA), haemodialysis, high-risk delivery, cataract and CABG. NHA (Aug 2021): 2 crore hospital admissions. Top specialities were general medicine, general surgery, infectious diseases, obstetrics and gynaecology, medical oncology and orthopaedics.
- Source: The Quint, 27 Jul 2019 – https://www.thequint.com/fit/medical-procedures-performed-under-ayushman-bharat (#91) – B; The Tribune, 19 Aug 2021 – https://www.tribuneindia.com/news/nation/indian-poor-seek-2-crore-hospital-admissions-under-ayushman-bharat-most-in-general-medicine-general-surgery-299041 (#90) – B
- Use in INDLOC/demo data: realistic demo patients include post-CABG (same population as the Eltorai trial), upper-abdominal / general surgery, hip-fracture fixation and knee replacement in older adults.
- Caveat: 2019–2021 data. The ranking measure varies by source.

### F-INDIA-10 (weak, Grade C): India's most-watched Hindi spirometer videos show 3-ball "Respirometer/Triflo" devices
- Detail: YouTube search "incentive spirometer kaise use kare hindi" (9 Oct 2026). Top results: Dr Lokendra Gaud "Respirometer" (~295k views), Prof. Dr Deepak Kumar Capri (~419k), a Triflow pulmonary-rehab video by Dr Ankush (~2.48M views).
- Source: YouTube search via yt-dlp (#92) – Grade C
- Use: suggests home patients in India commonly have 3-ball flow devices. This supports building a 3-ball mode (e.g. camera-based ball tracking) on the roadmap.
- Caveat: view counts are not market share. Titles only; subtitles not read.

## COMMS (round 2)

### F-COMMS-3: TRAI's 2026 rule change names robocalls and AI-voice calls ("A2P calls"). Service calls to existing customers don't need explicit consent, but "ongoing use" calls need consent that lasts only 7 days
- Detail: Plivo's India regulations page summarises the TCCCPR (Third Amendment) Regulations 2026 (TRAI notification PDF dated 18 Sep 2026, not yet read):
  - **A2P call:** a call that software places without a human dialling, including robocalls and AI-generated voices.
  - **Service call:** a call about a product or service the customer already has. It needs no explicit consent.
  - **Ongoing-use calls:** a call that supports the customer's ongoing use of a service counts as a service call only after explicit consent. That consent lasts **7 days** (renewable).
  - **Transactional call:** within 30 minutes of a customer-initiated transaction.
  - **Number series:** 140 series = promotional only. Landline-style numbers (022, 080…) = service and transactional only. 1600/160 series = banking, insurance and finance companies only.
  - **Who can call domestically:** only India-registered businesses with KYC can rent Indian numbers and make domestic calls. A foreign business must call internationally and shows a foreign caller ID.
  - Cold calling is prohibited.
- Source: Plivo docs, "India Calling Regulations" – https://www.plivo.com/docs/voice/concepts/india-calling.md (#71) – Grade B
- Use in build/pitch: hourly reminder calls to a hospital's own discharged patient most likely count as **service calls**. Record digital consent at discharge and renew it, and call from an Indian landline-series number via an Indian provider. For the demo, say "would call", or call a team phone.
- Caveat: vendor summary. **The TRAI regulation text itself must be read next round** (https://www.trai.gov.in/sites/default/files/2026-09/Regulation_18092026.pdf).

### F-COMMS-4: TRAI's "1600" trusted-call series is only for banks, insurers, pension funds and government. "140" is for promotions, which DND can block
- Detail: TRAI clarification of 10 Jul 2026. Calls from 1600 numbers can't be tagged, blocked or filtered. 140-series callers must register with telecom operators, and people's DND choices block them.
- Source: SCC Online, 18 Jul 2026 – https://www.scconline.com/blog/post/2026/07/18/trai-clarifies-1600-and-140-series-number-framework/ (#70) – Grade B
- Use: a private health startup can't use the trusted 1600 series. It needs regular service numbers plus consent. A government hospital partner (government-to-citizen calls) could.
- Caveat: legal-news summary of a TRAI press note.

### F-COMMS-5: Twilio trial limits: 30 days, at most 5 verified numbers, calls and SMS only within your sign-up country, and Twilio's own WhatsApp templates only
- Detail: free units: 100 SMS, 100 WhatsApp, 75 voice minutes. Calls and messages go only to verified numbers (max 5, shared across products). SMS and voice are restricted to the sign-up country. WhatsApp allows only pre-defined templates, with no custom templates on trial. Some TwiML verbs are blocked on trial.
- Source: Twilio docs, "Twilio trial account" – https://www.twilio.com/docs/usage/trials (#74); "Get started with your free trial" (#73) – Grade B
- Use in build: **demo risk**. If the account was signed up with an Indian number, trial voice is limited to India. But Twilio says calls to India must come from a non-Indian number (F-COMMS-1), which may conflict. **Test one call to a verified team phone today.** Have the "would call" fallback ready.
- Caveat: the interaction of these two rules is not documented. Test it.

### F-COMMS-6: Twilio WhatsApp sandbox: each phone must send "join <code>", the session lasts 3 days, and free-form text works only within 24 hours of the user's last message
- Detail: one shared number (+1 415 523 8886, Twilio logo). Max one message every 3 seconds. Business-initiated messages must use Twilio's pre-approved templates (e.g. "Appointment Reminders"); custom templates aren't possible. Sending "join" opens a 24-hour window for free-form messages. It may be restricted for some countries.
- Source: Twilio docs, "Twilio Sandbox for WhatsApp" – https://www.twilio.com/docs/whatsapp/sandbox (#29, re-opened to fact-check the plan) – Grade B
- Use in build: our plan's "send join again on demo morning" is **CONFIRMED and essential**. It both re-joins and opens the 24-hour window for our free-form AI summary. Space messages ≥3 s apart.

### F-COMMS-7: Exotel's pricing page shows no public per-minute prices
- Source: https://exotel.com/pricing/ (#72) – nothing useful (prices not in page text)

## VOICE (round 2)

### F-VOICE-7: Saaras v4 is now Sarvam's default speech-to-text model, covering 22 Indian languages plus English, with auto language detection and support for 8 kHz phone audio
- Detail: five output modes (transcribe, translate to English, verbatim, transliterate, code-mixed). REST takes ≤30 s per request; batch up to 2 h per file; WebSocket streaming. v4 adds "keyterm prompting" (up to 50 custom words, e.g. "spirometer", drug names) on REST and batch only.
- Source: Sarvam docs, Saaras – https://docs.sarvam.ai/api/getting-started/models/saaras.md (#75) – Grade B
- Use in build: for patient Q&A, keep clips under 30 s or use streaming. Add "spirometer", "SpiroBuddy" and similar as keyterms.
- Caveat: no latency figure found.

### F-VOICE-8: Sarvam's terms forbid AI medical advice unless a qualified professional reviews it, and require telling users it's AI
- Detail: Terms of Service effective 29 Jul 2026. Users must not use the service to give tailored medical advice without professional review and clear AI disclosure. They must not automate high-stakes medical decisions without human review. Outputs are "not medical advice". Customers must tell users they are dealing with AI, and human oversight is required.
- Source: Sarvam Terms of Service – https://www.sarvam.ai/terms-of-service (#78) – Grade B
- Use: our rules already fit: coaching and summaries only, fixed red-flag message, nurse-agreed rules, nurse approves targets. **Add an "AI voice coach" disclosure on screen and in the first spoken line.**

### F-VOICE-9: Sarvam voice-agent per-minute pricing is not published in the docs
- Detail: the docs pricing page lists LLM, TTS and STT rates, and per-minute dubbing rates (₹40/min Starter). There are no Voice Agents per-minute prices in the docs index.
- Source: https://docs.sarvam.ai/api/getting-started/pricing.md (#77); https://docs.sarvam.ai/conversations/llms.txt (#76) – Grade B
- Caveat: still a gap. Ask Sarvam sales or check the dashboard.

### F-VOICE-10: A free, offline alternative exists: AI4Bharat Indic-TTS (MIT licence, 13 Indian languages)
- Detail: IIT Madras / AI4Bharat. FastPitch + HiFi-GAN models for Assamese, Bengali, Bodo, Gujarati, Hindi, Kannada, Malayalam, Manipuri, Marathi, Odia, Rajasthani, Tamil and Telugu (ICASSP 2023). The models are also published on the government Bhashini platform. 408 GitHub stars; last pushed Nov 2024.
- Source: GitHub AI4Bharat/Indic-TTS (README) – https://github.com/AI4Bharat/Indic-TTS (#79) – Grade B
- Use in build/pitch: a **no-internet, no-cost fallback** to pre-generate clips, and an answer to "what if Sarvam disappears?".
- Caveat: needs a GPU or patience to run. Not tested. Repo not actively updated.

## CLIN (round 2)

### F-CLIN-6: 2024 lung-cancer review: incentive spirometry helps **as part of a breathing-exercise bundle** (fewer complications, shorter stays), but its effect on its own can't be separated
- Detail: 9 RCTs, 1,209 patients, searched to Nov 2023. IS combined with other breathing therapy reduced PPCs, improved lung function, shortened hospital stay and lowered breathlessness scores. There was no gain in 6-minute walk distance or quality of life.
- Source: Liang Y et al., *BMC Pulm Med* 2024, PMID 38360672 – via Europe PMC (#80) – Grade A
- Use in pitch: supports "IS works best as part of the nurse's bundle", which is exactly how SpiroBuddy is positioned.
- Caveat: includes Chinese-language trials, and the IS effect is mixed with other therapies.

### F-CLIN-7 (against us): 2024 cardiac-surgery review: incentive spirometry was **not better** than standard respiratory care
- Detail: 21 RCTs + 1 quasi-RCT, 1,677 participants. No advantage in lung complications or clinical outcomes. IS was worse on blood oxygen (PaO2 −4.48). Flow-type IS was better on vital-capacity recovery. The authors say IS shouldn't be widely recommended until better trials exist.
- Source: Silva HVC et al., *Braz J Cardiovasc Surg* 2024, PMID 38629953 – via Europe PMC (#81) – Grade A
- Use: Q&A honesty. The comparison is IS vs other active breathing care, not IS vs nothing. Our answer: we support whatever exercise the nurse prescribes, and we make adherence visible.

### F-CLIN-8: Indian studies: lung complications are common and deadly. Udaipur: 21.7 vs 12.5 days in hospital, and 28% of patients with a complication died. Puducherry (JIPMER): 34% after GI surgery
- Detail: Udaipur (Int Surg J 2018;5:3057–65): case-control study, emergency abdominal surgery. PPC incidence 2.9%. Total stay 21.7 vs 12.5 days, ICU stay 8.5 vs 1.4 days. **28% of patients with a lung complication died.** The authors recommend early mobilisation and deep breathing. JIPMER Puducherry (Int Surg J 2020;7:93–7): 100 GI-surgery patients, PPC incidence 34% (pleural effusion 44%, pneumonia 26.5%). Lower education status was linked to more complications.
- Source: https://www.ijsurgery.com/index.php/isj/article/download/3176/2303/11735 (#83) – A; https://www.ijsurgery.com/index.php/isj/article/download/4636/3454/20290 (#82) – A
- Use in pitch: confirms the plan's Udaipur numbers and adds Indian mortality ("28% of patients who got a lung complication didn't survive"). The education link supports simple voice coaching in the patient's language.
- Caveat: small single-centre studies, lower-tier journal. **Note: the plans cite ijsurgery article 2439 for Udaipur, but these numbers are in article 3176.** The 2439 link was not re-opened. Search results mention a Pune study (29/150 PPC, 11 died in 30 days) whose source wasn't confirmed, so don't use it.

### F-CLIN-9: An Indian RCT (Mangalore, 2016) used both flow (3-ball) and volume devices after open abdominal surgery. Both were safe and helped lung function recover; the volume device gave better walking-test gains
- Detail: 50 patients (37 men). Lung function dropped on days 1–3 and recovered by days 4–5 in both groups. The volume group improved more on 6-minute walk distance. No adverse events.
- Source: Kumar AS et al., *J Clin Diagn Res* 2016, PMID 26894090 (PMC4740618) – via Europe PMC (#89) – Grade A
- Use: Indian evidence supporting the volume-type device that SpiroBuddy reads (alongside AARC recommendation 6).
- Caveat: small, short follow-up, no PPC outcomes.

## COMP (round 2)

### F-COMP-5: InSee measures the piston with an **infrared time-of-flight sensor**, the same principle as our VL53L1X, and was built at a university lab in 2020
- Detail: Built by Prof. Farid Farahmand's lab at Sonoma State University. Infrared time-of-flight readings of the piston are converted to volume. It records failed attempts, the best volume and the time to reach a volume. A red blinking light reminds the patient and turns off only after a breath reaches the target. Data goes over Wi-Fi.
- Source: IEEE Spectrum (The Institute), 16 Jun 2020 – https://spectrum.ieee.org/infrared-device-helps-monitor-covid19-patients-breathing-therapy (#88) – Grade B
- Use in pitch: **never claim the laser-sensing idea as ours**. Our differences are the breath-*technique* AI (speed and hold quality, not just volume), the voice coach in Indian languages, home use, WhatsApp, and fitting Indian devices. InSee's FDA clearance is validation that ToF sensing on a piston works.

### F-COMP-6: Tidal Medical (InSee) holds active US patents on portable monitoring of incentive spirometry, with expiry around 2038
- Detail: US10610129B1 (filed 30 Oct 2018, granted 7 Apr 2020; inventors Farid and Foad Farahmand; assigned to Tidal Medical Technologies, Dec 2021). Claims cover a portable device that senses inspired volume in an IS, compares it with a target, counts successes and displays the result. Continuations: US11832930B2, US12053272B2, US20240049983A1. Anticipated expiry 30 Oct 2038.
- Source: Google Patents US10610129B1 (#86) – Grade A (patent record; legal status is Google's assumption)
- Use: patents are national, so US patents don't apply in India unless an Indian family member exists (**not checked**). A judge may ask about IP. Answer: "We know the US patents. Our India-first design adds technique AI and multilingual coaching. We'd run a freedom-to-operate check before any US launch."
- Caveat: we are not lawyers. The Indian filing search is a gap. US7998085 (an IS with "simulated humanlike voices") also exists, so voice prompts on an IS aren't new (#87 failed to load, title seen in search only).

### F-COMP-7: No public InSee price was found. No Indian smart incentive spirometer was found
- Detail: Indian digital *diagnostic* spirometers exist (Alveofit, Pune; SpiroPRO by Briota, Hyderabad, seen in search snippets only), but they measure lung function and are not incentive-spirometer coaches. One search found no Indian IS-tracker product or patent.
- Source: search snippets (not opened) – Grade C
- Use: careful wording: "we found no Indian product that tracks incentive-spirometer exercise at home".
- Caveat: absence of evidence. The Indian patent office search wasn't done.

## Claim check
| # | Our claim | Verdict | Use this wording |
|---|---|---|---|
| C1 | Hourly reminder: 58% vs 28% adherence | NEEDS WORDING CHANGE | "In a randomised trial of 145 heart-bypass patients, an hourly reminder doubled the share of waking hours in which patients did their breathing exercise: 58% vs 28% (Eltorai, *JAMA Surgery* 2019)." |
| C2 | It reduced atelectasis | CONFIRMED (small effect) | "slightly less lung collapse on X-ray" |
| C3 | InSee was FDA-cleared in 2025 | CONFIRMED | K241152, 21 Aug 2025 |
| C4 | Penn Airalux trial | CONFIRMED | 14.7 sessions a day, 30 patients, no control group |
| C5 | Airalux is iPhone-only | WEAK | "an iPhone/iPad app in the trial" |
| C6–C7 | Romsons under ₹500 / ₹300 | NEEDS WORDING CHANGE | "sold online for about ₹200–₹1,000" |
| C8 | InSee is English-only | UNVERIFIED | "designed for US hospitals" |
| C9–C10 | Sarvam covers 10 languages; under 250 ms | 11 languages CONFIRMED (Bulbul v3); speed not checked | "11 Indian languages" |
| C11 | Udaipur study: 21.7 vs 12.5 days in hospital, 8.5 vs 1.4 days in ICU (Plan §1, Final Research §3) | CONFIRMED, wrong link | Numbers confirmed in Int Surg J 2018;5:3057–65 (ijsurgery article 3176). The plans link article 2439. Fix the link. Can add: "28% of patients with these complications died." |
| C12 | Twilio sandbox: each phone sends "join <code>"; resend on demo morning (Plan §10.2) | CONFIRMED | Sandbox sessions expire after 3 days. "join" also opens the 24-hour window needed for free-form messages. |
| C13 | Plan §11.3: India "Digital Personal Data Protection Act, 2023"; consent | CONSISTENT | TRAI's 2026 rules also say telecom consent doesn't replace DPDP duties (F-COMMS-3). |
| C10 (round 3 update) | Sarvam speaks in "under 250 ms" | VENDOR CLAIM ONLY | Only Sarvam's marketing claims under 250 ms to the first audio over WebSocket; no independent test found (F-VOICE-11). Say "fast enough for live coaching", or measure it ourselves on demo day. Pre-generated clips make this irrelevant. |
| C15 | Plans: phone reminder calls by AI as part of the product | NEEDS WORDING CHANGE | TRAI's 2026 text (F-COMMS-8): AI calls are "A2P calls"; they must be declared in advance from an Indian registered caller ID, and "ongoing use" calls need consent renewed every 7 days. Say: "calls are an escalation step via an Indian telephony partner, with recorded consent; the demo uses a browser phone." |
| C16 | Plan test targets: volume within ±100 mL; readings wobble less than ±5 mm | PLAUSIBLE ONLY WITH CALIBRATION | The datasheet says typical error ±20 mm but good repeatability (F-TECH-1). ±5 mm wobble is realistic with averaging; ±100 mL needs a per-device 2–3 point calibration at the printed marks. Report the measured number, not the target. |
| C17 | Plans: "CDSCO class unconfirmed; wellness apps excluded" | CONFIRMED, MORE DETAIL | Guidance is function-based (F-REG-1). Diagnostic and monitoring spirometers are Class B; no incentive-spirometer row found (F-REG-2). Keep the answer "exercise coach; we'll get a formal ruling". |
| C18 | Plan §11.3/§790: "We follow the DPDP Act principles" | CONFIRMED, ADD SPECIFICS | Rules notified Nov 2025; main duties from about May 2027 (F-REG-3). Add: itemised notice read aloud, one-word withdrawal, access logs, 72-hour breach report, and the patient's own consent (an adult child isn't a legal guardian). |
| C14 | Plan/REQUIREMENTS imply our laser sensing is new | NEEDS WORDING CHANGE | InSee already uses infrared time-of-flight on the piston (F-COMP-5). Say: "like InSee, we read the disc with a laser sensor; unlike InSee, our AI judges breathing *technique* and coaches in Indian languages at home." |
| C19 (round 4) | PITCH_FACTS #25: "ongoing-use reminders need consent renewed every 7 days" | NEEDS WORDING CHANGE | Only type (ii) "ongoing use" service calls need 7-day consent (F-COMMS-8). TRAI's press release adds a *separate* 7-day window for commercial messages after a customer's written inquiry (F-COMMS-12). Say: "some reminder calls need consent the patient renews weekly". |
| C20 (round 4) | "Spirometers for monitoring are Class B; wellness tools are outside" | CONFIRMED FROM PRIMARY TEXT | CDSCO PDF (F-REG-4): wellness software must not mention any disease; software that *alerts* about a condition is not wellness. Standalone software that only *informs* clinical management of a *serious* condition sits in Class A in Table 2. |
| C21 (round 4) | "No Indian complication-cost figure exists" (PITCH_FACTS never-say list) | UPDATE | Still no direct rupee cost of a post-surgery lung complication. We now have Indian cost anchors: ₹2,307 per ward bed-day (CHSI, F-BIZ-4) and ₹25,927 per ICU bed-day (PGIMER 2024, F-BIZ-5). Use them as "what a day costs", not as "what we save". |
| C22 (round 4) | Plans: piston mL can be computed from the cylinder size | WRONG APPROACH | No Romsons drawing exists publicly (F-TECH-4). Calibrate against the printed marks on each spirometer model instead. |
| C23 (round 5) | Plans (Complete Plan §633, Final Research §47/§89): "We couldn't confirm the CDSCO class for incentive spirometers" | WRONG (now answered) | CDSCO's Class A (non-sterile, non-measuring) list names "Incentive spirometer" (item 496) and says it is not a diagnostic (F-REG-5). Say: "The plastic spirometer is Class A, the lowest risk. Our measuring clip-on will need its own registration, probably Class A measuring or Class B." |
| C24 (round 5) | Judge answers J8/J17: "we'll get an official ruling first" | NEEDS WORDING CHANGE | Keep the ruling step, but lead with the fact: the base device is already Class A (F-REG-5); measuring and alerts take us out of the non-measuring exemption (F-REG-4). |
| C25 (round 5) | Implied: SpiroBuddy reduces readmissions | NOT SUPPORTED | Only an international CABG baseline exists (12.9%, F-BIZ-8); no Indian figure; knee-replacement readmission is ~1% in Ludhiana. Say "we'll measure readmissions in a pilot". |
| C26 (round 5) | J22 / pitch: "TB survivors are a large next market" | CONFIRMED (rough) | ~26 lakh notified a year, 90% success (PIB 2026); 59% lung impairment at completion in Madurai (F-VIS-4). Say "lakhs of people a year", labelled as our estimate. |
| C27 (round 6) | F-VIS-4 caveat / pitch: "No guideline names incentive spirometry for post-TB rehab" | WRONG (now answered) | The RBIPMT 2024 pulmonary-rehab guidance on ntep.in lists the incentive spirometer among breathing exercises (F-VIS-5). Say: "India's own TB rehab guidance (RBIPMT 2024, draft) includes the incentive spirometer", and add "in supervised sessions". |
| C28 (round 6) | F-BIZ-8 / J27: "No Indian 30-day readmission figure" | NEEDS WORDING CHANGE | For major abdominal (GI cancer) surgery there is one: 4.7% in 30 Indian centres (F-BIZ-10); about 5% after Whipple. For CABG there is still none. Say: "about 1 in 20 after major abdominal surgery in India; for bypass, about 1 in 8 worldwide". |
| C29 (round 6) | Post-TB sizing "about 23 lakh finish treatment, roughly half impaired" (F-VIS-4 team estimate) | NEEDS WORDING CHANGE | Over 20% of India's TB is outside the lungs (WHO, F-VIS-6). Use "fewer than about 19 lakh finish treatment for lung TB each year (our estimate)", still "lakhs of people a year". |

## Contradictions & risks
1. Cochrane 2014 found no proof incentive spirometry works, and AARC advises against using it alone. Our answer: the trials never recorded adherence, and we measure it. **Never say "prevents pneumonia".**
2. Go-breath (Korea), an hourly alarm with a nurse dashboard, showed no significant effect. It is also prior art for our 8:00–21:00 schedule.
3. Prior art is crowded (InSee, SpiroTimer, Michigan, Airalux, Go-breath, a 1978 Bard device). Our edge: Indian devices, home use, Indian languages, WhatsApp and technique AI.
4. Many Indian patients get 3-ball flow devices, which our disc sensor can't read.
5. Twilio calls to India show a foreign caller ID, so elderly patients may not answer. A real product needs Indian telephony.
6. WhatsApp templates that sound promotional are billed as marketing (about 7x more).
7. The author of the 58% trial filed a patent on the reminder device.
8. **(Round 2)** A 2024 cardiac-surgery meta-analysis (22 trials) found IS **not better** than standard breathing care (F-CLIN-7). The 2024 lung-cancer review found benefit only as part of a bundle (F-CLIN-6). Keep the line "supports the nurse's exercise plan".
9. **(Round 2)** Our sensing principle (infrared time-of-flight on the piston) is the same as InSee's (F-COMP-5), and Tidal holds active US patents until about 2038 (F-COMP-6). India isn't covered unless an Indian filing exists (unchecked). Don't present the sensor as our innovation.
10. **(Round 2)** Twilio trial accounts are limited to the sign-up country and 5 verified numbers, while Twilio says calls to India must come from a non-Indian number. The demo voice call may simply fail, so test it today (F-COMMS-5).
11. **(Round 2)** Automated reminder calls in India fall under TRAI's 2026 "A2P call" rules: consent records, Indian registered business, Indian service-number series. A hackathon team can't do this, so present calling as "roadmap via an Indian telephony partner" (F-COMMS-3/4).
12. **(Round 2)** Only 41% of older Indians own a smartphone (F-INDIA-5). An app-only patient experience would exclude most of our users. The device + voice + family WhatsApp design answers this. Say so.
13. **(Round 2)** Popular Hindi videos show 3-ball devices (F-INDIA-10, weak). The volume-device focus is evidence-backed (AARC rec. 6; Mangalore RCT, F-CLIN-9), but many home patients may have the 3-ball type.
14. **(Round 3)** The VL53L1X's typical error is ±20 mm out of the box, and its 27° beam may hit the tube wall (F-TECH-1). Without calibration and a narrowed sensing area, the live demo could show wrong volumes. Test against the printed marks before the pitch.
15. **(Round 3)** TRAI's A2P rules (F-COMMS-8) start about mid-October/November 2026, right around the hackathon. Any live robocall to a real Indian phone from an undeclared caller ID would technically be spam. Call only a team member's own phone, with consent, or use the browser phone.
16. **(Round 3)** Once SpiroBuddy alerts nurses about a patient's breathing, it probably becomes medical device software (F-REG-1/2), likely Class B. "Wellness" only holds if we stay with exercise coaching and adherence.
17. **(Round 3)** WhatsApp health bots in India lose most users: 18% completion overall in one pilot (F-COMP-9, self-reported). Don't promise sustained engagement through WhatsApp alone.
18. **(Round 3)** Voice pacing feedback ("slow down / speed up") already exists in hobby projects (F-COMP-10), and Tidal's PCT text also covers sound-based sensing and voice switches (F-COMP-8). Our novelty is the combination for Indian homes, not any single feature.
19. **(Round 3)** The only Indian complication-cost number we have is a proxy (VAP in an ICU, F-BIZ-2). Don't present it as the cost of a post-surgery lung complication.
20. **(Round 3)** Inconsistent finding IDs: the imported section reuses F-VOICE-7 to 9 and F-COMP-7. Cite those as "(imported)".
21. **(Round 4)** CDSCO's own text says software that *alerts* about a condition is **not** wellness (F-REG-4). The nurse-alert feature therefore probably makes SpiroBuddy medical device software. Keep the demo wording "exercise reminders and adherence summary for the care team".
22. **(Round 4)** Inside a 5–7 cm wide cylinder the sensor's full 27° beam reaches the walls by about 10–15 cm of distance. Wall echoes make readings too short (F-TECH-3). Use the smallest sensing window (4x4, about 15°) and test at the top of the piston's travel.
23. **(Round 4)** The Romsons Breazer's inner size and mL-per-mm are not published anywhere we could find (F-TECH-4). Without a hands-on measurement, any volume we show is a guess.
24. **(Round 4)** TRAI's Gazette date is still unknown. If it was published around 18 Sep 2026, the main rules start about 18 Oct 2026 and the A2P declaration rule about 17 Nov 2026, so they may be in force on hackathon day (F-COMMS-12).
25. **(Round 4)** Our rupee cost numbers come from different hospitals and years (a trauma ICU, a multi-state costing study). They are anchors, not a savings claim (F-BIZ-4, F-BIZ-5).

26. **(Round 5)** The CDSCO exemption covers only *non-measuring* incentive spirometers (F-REG-5). Adding our sensor makes it a measuring device, so we must not say "no licence needed". Plan for registration and a licence.
27. **(Round 5)** An Indian group (Amrita, Kochi) is already running an RCT of an LLM nurse chatbot after CABG (F-COMP-12). Don't say "first AI follow-up for Indian surgery patients".
28. **(Round 5)** Digital adherence tools in TB showed only a modest, low-certainty effect (F-ADH-8), and the Indian caregiver-WhatsApp pilot changed visits, not complications (F-ADH-7). Don't promise clinical outcomes; promise visibility and earlier escalation.
29. **(Round 5)** Knee-replacement readmission in India can be ~1% (F-BIZ-8). A "readmission savings" story for knee patients would fall apart; use CABG and abdominal surgery for that argument.
30. **(Round 5)** We still have no evidence that older Indians prefer voice or IVR (F-INDLOC-5). The voice-first case rests on literacy and vision data only.
31. **(Round 6)** Indian 30-day readmission after major abdominal surgery is low (4.7% in 30 cancer centres, F-BIZ-10), and none of the Indian papers names lung problems as a cause. A readmission-savings story for abdominal surgery in India is weak; lead with length of stay and adherence instead.
32. **(Round 6)** 29% of over-60s (35% of older women) have difficulty making a phone call (LASI, F-INDLOC-7). A design that asks the patient to dial, type or navigate menus will fail for many; keep the patient's part to "answer and listen" or "breathe into the device".
33. **(Round 6)** Kilkari, India's biggest voice-message programme, had **no effect on its main outcome** in an RCT, and only half of calls are answered on the first try (F-INDLOC-6). Voice reminders alone are not enough; don't present "AI calls" as the thing that changes behaviour.
34. **(Round 6)** The RBIPMT guidance that names the incentive spirometer is a **draft** for **supervised centre** rehab, not home use (F-VIS-5). Don't say "the TB programme recommends SpiroBuddy at home".
35. **(Round 7)** Under India's device law, an accessory is classed **on its own**, and a battery device that supplies monitoring information is an "active diagnostic medical device"; if it is for monitoring a vital body process it is **Class B** (F-REG-6). So the clip-on probably can't borrow the spirometer's low-risk Class A status. Say "we expect Class B; we'd confirm with CDSCO", never "it's just an accessory, no approval needed".
36. **(Round 7)** Kilkari reach figures conflict: one paper says 99.5% are reached by the 9th call (F-INDLOC-6), a later ARMMAN/Google preprint says about 23% are **not** reached despite 9 attempts (F-INDLOC-9). Different cohorts and definitions. Quote "half answer the first call" and "retries matter", not a single reach rate.

## Open gaps (priority order, after round 7)
1. **TECH (hands-on, team):** caliper measurements of the Breazer 2500 and a 4x4-window bench test inside the tube (the web has nothing).
2. **REG (person):** Romsons Chapter IIIB registration for the Breazer (read the box label, or search cdscomdonline.gov.in). Two more web searches in round 7 found nothing; GeM bids aren't indexed. For our own class, the law points to Class B (F-REG-6); confirm with a CDSCO pre-submission query or a regulatory consultant.
3. **BIZ: Indian 30-day readmission after CABG — stop web searching.** Rounds 5, 6 and 7 (four Europe PMC searches incl. a journal-filtered one on IJTCVS / Ann Card Anaesth / Indian Heart J, plus web searches, ~8 papers checked) found none. Use the global 12.9% (F-BIZ-8) and the Indian abdominal 4.7% (F-BIZ-10), or ask a cardiac surgeon for their unit's figure.
4. **COMMS (person):** TRAI Third Amendment Gazette date; "human-assisted" call exclusion (search our local copy of #106).
5. **ADH (person):** CTRI search by hand for Indian post-discharge incentive-spirometer trials; otherwise accept "no Indian home data exists; our pilot would create it".
6. **INDLOC/VOICE:** personal (not household) phone ownership for 60+ still not found on the web (NSS 78th round tables not indexed; LASI Wave 2 not yet found). A person could open MoSPI's NSS 78th round "Multiple Indicator Survey" report tables by hand. No usable data on WhatsApp voice-note use by older Indians (only small, non-representative studies). mMitra-specific listening data still not found (the ARMMAN preprint read was about Kilkari).
7. **VIS:** the India TB Report's own table (to cross-check the WHO-data split, F-VIS-7); whether RBIPMT guidance has a final version.

## Open gaps (priority order, after round 6; kept for history)
1. **TECH (hands-on, team):** caliper measurements of the Breazer 2500 and a 4x4-window bench test inside the tube (the web has nothing).
2. **REG:** Romsons Chapter IIIB registration for the Breazer (needs a person on cdscomdonline.gov.in or the box label); CDSCO class for a *measuring* incentive-spirometer accessory.
3. **COMMS:** TRAI Third Amendment Gazette date; whether "human-assisted" calls are excluded (search our local copy of #106).
4. **ADH:** Indian incentive-spirometer use **after discharge** is still missing after 3 rounds. Only a person can search CTRI (ctri.nic.in → Search trials → "incentive spirometer", "spirometry", "breathing exercise"); or try the WHO ICTRP portal by hand. Otherwise accept the gap and say "no Indian home data exists; our pilot would create it".
5. **BIZ:** Indian 30-day readmission after **CABG** (still none; try Indian J Thorac Cardiovasc Surg conference abstracts, SCTIMST/AIIMS cohorts, or ask a cardiac surgeon). Home-physio price: stop web searching; get a phone quote.
6. **INDLOC/VOICE:** mMitra (ARMMAN) call-pickup and listening data; WhatsApp voice-note use among older Indians; a personal (not household) phone-ownership figure for 60+ (LASI Wave 2 when published, or NSS 78th round "mobile phone use" tables).
7. **VIS:** the exact India pulmonary vs extrapulmonary split (India TB Report 2024/2025 PDF table, by hand on tbcindia.mohfw.gov.in); check whether the RBIPMT guidance has a final (non-draft) version.

## Open gaps (priority order, after round 5; kept for history)
1. **TECH (hands-on, team):** caliper measurements of the Breazer 2500 and a 4x4-window bench test inside the tube (unchanged from round 4; the web has nothing).
2. **REG:** does Romsons hold a Chapter IIIB registration for the Breazer? Needs a person on the CDSCO registration portal (cdscomdonline.gov.in) or a look at the box label. Also: which class does CDSCO give a *measuring* incentive-spirometer accessory (ask via the classification portal / a regulatory consultant).
3. **COMMS:** TRAI Third Amendment Gazette date and whether "human-assisted" calls are excluded (search our local copy of #106).
4. **COMP:** InPASS search (CAPTCHA, needs a person): "incentive spirometer", "spirometer", "respiratory exerciser"; applicant "Tidal". Check Amrita's Smart CABGuard results when published.
5. **ADH/CLIN:** still no Indian data on spirometer use *after discharge*; try CTRI (ctri.nic.in) for trials on home breathing exercise or post-discharge physiotherapy adherence; any Indian family-involved breathing-exercise trial.
6. **BIZ:** an Indian 30-day readmission rate after CABG or major abdominal surgery (try Indian J Thorac Cardiovasc Surg full texts, AIIMS/SCTIMST cohorts); a current official home-physio price (call or app quote).
7. **VOICE/INDLOC:** Indian evidence on voice or IVR use by older adults (Kilkari/mMitra reach data, LASI phone-use tables); WhatsApp voice-note use among older Indians.
8. **VIS:** RBIPMT July 2024 pulmonary-rehab guidance PDF (ntep.in/node/6610, not yet opened); share of pulmonary vs extrapulmonary TB in notifications to tighten the post-TB estimate.

## Open gaps (priority order, after round 4; kept for history)
1. **TECH (hands-on, needs the team, not the web):** with calipers, measure the Breazer 2500's inner cylinder diameter, piston travel from 0 to 2500 mL and the mm between printed marks; check whether the floor under the piston is open. Bench-test the VL53L1X at 4x4 sensing window inside the tube at the top of travel. The web has no drawing (F-TECH-4).
2. **COMMS:** exact Gazette date of the TRAI Third Amendment (try egazette.gov.in by hand); whether the final text excludes "human-assisted" calls (search our local copy of #106 for "human"); a telecom lawyer's view on type (i) vs type (ii) for post-discharge reminders.
3. **COMP:** InPASS (Indian patent office) search needs a CAPTCHA, so a person must do it: iprsearch.ipindia.gov.in → Patent Search → title/abstract "incentive spirometer", "spirometer", "respiratory exerciser"; applicant "Tidal".
4. **REG:** CDSCO respiratory notification (6 Aug 2021) and the Jan 2025 "Class A self-notified" list: is "incentive spirometer" or "respiratory exerciser" named? Does Romsons hold a CDSCO registration for the Breazer?
5. **BIZ:** 30-day readmission rate after major surgery in India; current Portea / Apollo HomeCare price pages; any HBP revision after 2022.
6. **VOICE:** listen to Bulbul v3 voices with older listeners; measure our own latency; Bhashini terms.
7. **CLIN:** Indian home IS adherence after discharge; any trial of family-involved breathing exercise.
8. **VIS:** RBIPMT July 2024 pulmonary-rehab guidance PDF (ntep.in/node/6610); yearly number of people completing TB treatment (Ni-kshay / India TB Report) to size the post-TB market.

## Open gaps (priority order, after round 3; kept for history)
1. **TECH:** mL per mm of piston travel for the Romsons Breazer 2500 and the AirLife-type devices (measure with calipers or find the product drawing); tube inner diameter vs the 27° beam; any published VL53L1X-in-tube test.
2. **COMMS:** the exact Gazette date of TRAI's Third Amendment (to fix the start dates); whether TRAI or a law firm has said post-discharge health reminders are type (i) or type (ii) service calls; the DLT fee on an operator's own page; Meta Cloud API direct (no BSP fee) for India, re-check.
3. **BIZ:** the rupee cost of a post-surgery lung complication or an extra ward/ICU day in India (try the CHSI costing study / PGIMER unit costs); the current HBP version (2023+) rates for CABG and cholecystectomy; per-patient prices of Indian post-discharge programmes.
4. **REG:** open the CDSCO MDSW guidance PDF itself (classification matrix, wellness wording); search CDSCO's classification portal for "incentive spirometer" / "lung exerciser"; whether a registered nurse-alert function makes it Class B.
5. **COMP:** InPASS search (Indian patent office) for incentive-spirometer, respiratory-exerciser and Tidal filings; Indian smart-IS or physio startups (Inc42, YourStory); Zorgers–Clinitouch details.
6. **VOICE:** listen to the Bulbul v3 voices with older listeners (pooja, ishita, priya); measure our own latency; Bhashini official terms (bhashini.gov.in) and the Sansad answer on Bhashini usage.
7. **INDLOC:** Indian lobectomy demographics; a source for phone ownership among caregivers; check the F-INDLOC-4 conventions with an Indian team member; Kerala/Tamil Nadu-specific elderly smartphone or WhatsApp data.
8. **CLIN:** India-specific IS adherence after discharge (home), beyond Hyderabad; any trial of family-involved breathing exercise.

## Open gaps (after round 2; kept for history)
1. **COMMS:** read the TRAI TCCCPR Third Amendment 2026 text (trai.gov.in/sites/default/files/2026-09/Regulation_18092026.pdf) on A2P/AI calls and consent; DLT registration for SMS; Twilio's WhatsApp fee for India; Exotel/Plivo per-minute prices (try Plivo's pricing page); test whether a Twilio trial can call a verified Indian number.
2. **INDLOC:** realistic demo data: typical ages and sex for CABG / abdominal / hip patients in India; common names by region; caregiver patterns (who looks after a discharged elder: spouse, son, daughter-in-law; children abroad); hospital types (government medical college vs private chain); DD/MM/YYYY and lakh formatting; ward nurse-to-patient ratios.
3. **TECH:** VL53L1X accuracy and repeatability at 5–25 cm (ST datasheet); a camera-based 3-ball tracking idea; accuracy of volumetric IS scale markings.
4. **REG:** CDSCO class for an IS accessory and software; DPDP Act consent for health data; the "wellness" exclusion in the July 2026 software guidance.
5. **VOICE:** Sarvam voice-agent per-minute price; Bulbul latency; which voices sound warm for elderly listeners (listen to the Voices page); Bhashini API access terms.
6. **BIZ:** cost of a lung complication in India (still no rupee figure found); PM-JAY package rates for CABG and abdominal surgery as a cost anchor; hospital remote-monitoring business models.
7. **COMP:** Indian patent search (ipindiaservices) for IS tracker filings and any Tidal Medical Indian family; InSee price (contact only).
8. **INDIA:** a LASI national figure for mobile phone ownership among people over 60 (not found in the factsheet snippet); WhatsApp use among caregivers.
9. JUDGE: compile likely questions with evidence-backed answers.


## Imported: Sarvam calls & InSee feasibility (separate chat, 9 Oct 2026)
Full report: `docs/research/SARVAM_CALLS_AND_INSEE_FEASIBILITY.md` (ledger #93–#105). Key points:
- **F-VOICE-7:** Sarvam Voice Agents cost **₹3.50/min** (launch price), which includes numbers, simulation and analytics. The ₹100 signup credit covers about 28 min if it can be applied to Voice Agents (not confirmed). Renting a number may need KYC. – #99, #55 – B
- **F-VOICE-8:** keypad entry (DTMF) is still "planned" in Sarvam's runtime docs, so the demo should use **spoken answers**, not "press 1/2/3". Call transfer goes to **one** number or SIP address per transfer. No simultaneous ring-group found. Outbound webhooks and call variables exist (Aug 2026). – #94, #97, #98 – B
- **F-VOICE-9:** "emotion" is only **post-call sentiment from the transcript** (Call Analytics). There is no validated reading of feelings from tone of voice, so label it "possible distress – review call" and require the nurse to confirm. – #104, #105 – B
- **F-COMP-7:** InSee performance study: 30 subjects, 240 data points, 100% agreement with blinded physicians (95% CI 98.5–100%). Size about 6.24 × 3.34 × 1.14 in, 4.2 oz, 1,200 mAh, USB-C. **No public price, no verified India distributor.** It is offered as a free hospital trial. It proves measurement accuracy, **not** better patient outcomes. – #101–#103 – A/B
- Decisions: the browser phone is the guaranteed demo route; a real Sarvam call goes only to one pre-consented presenter phone if a number is active; the webhook is normalised to `{provider, status, outcome, reason_category, patient_words, neutral_note, red_flag, callback_requested, transcript_reference}`; red-flag rules are deterministic and run outside the LLM.

---
# Round 3 additions (9 Oct 2026)

About 30 reads (ledger #106–#134). Note: the imported Sarvam/InSee section above reuses IDs F-VOICE-7 to 9 and F-COMP-7. To avoid more clashes, round 3 starts at F-VOICE-11 and F-COMP-8. When citing the older duplicates, add "(imported)".

## COMMS (round 3)

### F-COMMS-8: TRAI's 2026 rule text confirms that AI-voice calls and robocalls are "A2P calls" and must be declared in advance. Health reminders to your own patient can count as "service calls", but some kinds need consent that lasts only 7 days
- Detail (primary text, read in full):
  - **A2P call:** a call started by software without a human dialling. This includes robocalls and pre-recorded or artificial (AI) voices.
  - **Service call, type (i):** information about a product or service the customer already has. It isn't promotional and **needs no explicit consent**.
  - **Service call, type (ii):** a call that supports the customer's *ongoing use* of a service. It needs **explicit consent, valid for 7 days**, which the customer can renew 7 days at a time. The consent must be recorded in the operators' Consent Register.
  - **New rule 4:** every sender must **declare A2P calling in advance** to its telecom operator, with the caller-ID ranges it will use. An undeclared A2P call counts as spam (UCC).
  - The receiving operator may charge up to **5 paise per minute** for A2P calls.
  - **Health** is one of the categories customers can block or unblock. "BLOCK PROMO" never blocks service or transactional calls.
  - Consent under TRAI does **not** replace duties under the DPDP Act (Explanation 3).
  - Timing: the rules apply 30 days after publication in the Gazette, the A2P-declaration rule after 60 days, and some items after 90 days. The PDF is dated 18 Sep 2026, so expect about **mid-to-late October 2026** and **mid-to-late November 2026** (exact Gazette date not seen).
- Source: TRAI, TCCCPR (Third Amendment) Regulations 2026 – https://www.trai.gov.in/sites/default/files/2026-09/Regulation_18092026.pdf (#106) – **A**
- Use in pitch/build: our reminder call is most defensibly a **service call from the hospital to its own discharged patient**. To be safe under either reading, record digital consent at discharge **and** build a weekly renewal ("Shall we keep calling you? Say yes"). Calls must come from a declared caller ID registered to an Indian business, through an Indian operator. For the demo, use the browser phone only.
- Caveat: the PDF is a scan, read through OCR. Whether post-discharge reminders are type (i) or type (ii) is our reading, not a ruling. Ask a telecom lawyer before launch.

### F-COMMS-9: SMS in India needs DLT registration by an Indian company. It takes about 1–3 weeks end to end, and every message must match a pre-approved template
- Detail:
  - Steps:
    1. Register the business (the "entity") on one operator portal (Jio, Airtel or ViLPower).
    2. Register a 6-letter sender ID (the "header").
    3. Register each message text as a template with `{#var#}` placeholders.
  - Documents: company PAN (not a personal PAN), Certificate of Incorporation, GST certificate, authorisation letter and ID proof.
  - Quoted times: entity 3–7 business days; header 1–3 days; each template 1–3 days; sync across portals 5–7 days.
  - Fee: unclear. Vendor guides quote about ₹5,900 on some portals; another says registration is free. Not confirmed on an operator's own page.
- Source: Exotel DLT guide – https://developer.exotel.com/docs/sms-support/dlt-guide (#108) – B; fee from vendor search snippets – C
- Use: **no SMS in the hackathon.** WhatsApp, the device beep and browser voice are enough. An SMS fallback for feature phones goes on the roadmap, once we have a registered company.

### F-COMMS-10: Twilio adds $0.005 to every WhatsApp message, sent or received, on top of Meta's fee
- Detail: Twilio charges $0.005 per message, inbound or outbound, and passes Meta's per-template fee through. Failed messages cost $0.001. Meta's fee for an Indian utility message is ₹0.115 (F-COMMS-2), so Twilio's own fee is several times bigger than Meta's.
- Source: Twilio WhatsApp pricing – https://www.twilio.com/en-us/whatsapp/pricing (#107) – B
- Use in pitch: "About 12 paise per update at Meta's rate. In production we'd connect directly to Meta's Cloud API or use an Indian partner, to avoid the middleman's fee." (We did **not** re-check this round that the Cloud API has no extra fee.)
- Caveat: the page's calculator defaulted to another country. The $0.005 fee is stated for all countries.

### F-COMMS-11: Phone calls in India are cheap but need paperwork: Plivo charges ₹0.38/min and ₹200/month per number, Exotel's ID check (KYC) takes 1–3 business days, and both need a business registered in India
- Detail:
  - Plivo India prices:
    - domestic calls ₹0.38/min, both ways, billed in **30-second steps**
    - calls from a browser (WebRTC) ₹0.25/min
    - Indian number ₹200/month
    - multilingual text-to-speech free; speech recognition ₹1.70 per 15 seconds
    - $10 of free credits
  - Plivo's rules:
    - Only businesses registered in India, with KYC done, can rent Indian numbers and make domestic calls.
    - Both ends of the call must stay in India ("media anchoring"), or the call fails.
    - Landline-style numbers are for service and transactional calls only. 140-series numbers are for promotions only. 160-series numbers are for banks, insurers and other finance firms only.
  - Exotel:
    - KYC needs business documents: Certificate of Incorporation or GST certificate, business PAN, and the signatory's ID.
    - Review takes 1–3 business days (up to 5).
    - Outbound calls are blocked until KYC is done. Trial accounts can only call verified numbers.
    - No public per-minute price.
  - Our maths: a 2-minute AI reminder call costs about ₹0.76 for the phone line (Plivo) + ₹7.00 for the Sarvam Voice Agent (₹3.50/min, imported F-VOICE-7) ≈ **₹8 per call**. A WhatsApp utility message costs ₹0.115, about 70 times less.
- Source: https://www.plivo.com/voice/pricing/in/ (#109); Plivo India requirements (#110); Exotel KYC (#111) – B
- Use: in the pitch, say "WhatsApp first; calls only when a patient misses sessions or has no smartphone". This is also our answer on cost.
- Caveat: our team has no Indian company yet, so an Indian caller ID isn't possible before the hackathon.

## INDLOC (round 3) – realistic Indian demo data

### F-INDLOC-1: Indian heart-bypass (CABG) patients are mostly men (about 87–89%), usually in their late 50s or early 60s, and often have diabetes
- Detail:
  - Robotic CABG at one Indian hospital, 2019–2023: 195 patients, 88.7% men, mean age 61.3 (IJTCVS 2024).
  - From search snippets (not opened):
    - 1,000 planned CABG patients: mean age 59.7, 88.4% men.
    - *Indian Heart Journal* 2018: 1,559 patients, 87% men, 40% with known diabetes.
  - A Kochi series of 4,024 CABG patients (Amrita, 2014) exists, but its numbers weren't visible.
- Source: Europe PMC, PMID 38125327 (#114) – A; snippets – C; #112 – B
- Use (demo data): the CABG demo patient is a man aged 55–66 with diabetes, e.g. a 62-year-old retired bank officer from Kerala.
- Caveat: single-hospital data. No national registry found.

### F-INDLOC-2: Knee-replacement patients are mostly women (about 60–65%), with a mean age of about 62. Gallbladder-surgery patients are mostly women in their 40s. People with lung damage after TB average about 50, slightly more often men
- Detail:
  - Knee replacement:
    - 604 Indian patients: mean age 61.7, 65% women (J ISAKOS 2026).
    - Robotic surgery at several centres: mean age 62.9, 60.5% women (J Exp Orthop 2026).
  - Keyhole gallbladder removal (laparoscopic cholecystectomy):
    - 215 patients: mean age 42.7, 81% women.
    - A government-hospital series: mean age 44.8, 98% women.
    - Complicated cases: mean age 49.9, 58% women.
  - Lung damage after TB: 150 survivors, mean age 50.3, 55% men (*Indian J Tuberc* 2026).
- Source: Europe PMC searches (#113, #115) – A
- Use (demo data):
  - knee-replacement patient: a woman of about 60–68
  - gallbladder patient: a woman of about 40–50
  - post-TB patient: a man of about 45–55 from a lower-income family
  - Ages for lung-surgery (lobectomy) patients: not found.
- Caveat: single studies, not national averages.

### F-INDLOC-3: Most older Indians live with their children, most older women can't read, and over a third have low vision. So the design must be voice-first, with big text and the family in the loop
- Detail (LASI Wave 1, people aged 60+):
  - Living arrangements:
    - alone: 5.7% (women 9.0%)
    - with spouse and children: 40.6%
    - with children and others: 27.6% (women 42.7%)
    - So about **two in three live with their children.**
  - Reading:
    - **can read and write: 39.6%**
    - men 56.6%, **women 24.2%**, rural 30%
  - Daily tasks:
    - 48% have trouble with at least one everyday task, such as making a phone call or taking medicines.
    - 24.8% need someone to help them.
  - Eyes and ears:
    - 55.3% report an eye or vision problem.
    - **37.1% had low vision when tested.**
    - 9.6% report hearing problems, but only 0.7% use a hearing aid.
  - Lungs:
    - 8.3% report a diagnosed chronic lung disease.
    - 9.2% showed a blocked-airway (obstructive) pattern on testing.
- Source: LASI Wave 1 India factsheet, IIPS/MoHFW – https://www.iipsindia.ac.in/sites/default/files/other_files/LASI_W1_Elderly_India.pdf (#117) – **A**
- Use in pitch: "Three in four older Indian women can't read, and over a third of older people have low vision. So SpiroBuddy speaks, and a family member gets the WhatsApp update."
- Use in build:
  - large fonts and icons
  - a voice version of every screen
  - the caregiver as the default WhatsApp recipient
  - nothing on the device that needs reading
- Caveat: the survey was done in 2017–18.

### F-INDLOC-4 (team guidance, not a cited source): conventions for demo data and wording
- These are cultural and formatting conventions, not research findings. Ask an Indian team member to check them.
  - **Names by region (fake patients):**
    - Kerala: Thomas Varghese, Sreedevi Nair, Abdul Rasheed, Mariamma Joseph
    - Tamil Nadu: Murugan Subramanian, Lakshmi Ammal, Fathima Beevi
    - North: Ramesh Kumar Sharma, Sunita Devi
    - West: Suresh Patil, Meena Shah
    - East: Subrata Das
  - **Respectful address:**
    - Hindi speakers: name + "ji" (Sharma ji), or "Mataji/Pitaji" for elders.
    - Tamil: "Amma/Appa" (mother/father), "Paati/Thatha" (grandmother/grandfather).
    - Malayalam: "Amma/Achan" (mother/father); "Ammachi/Appachan" (grandparents, common among Christians); "Chechi/Chettan" (elder sister/brother). Patients often call nurses "Sister" or "Chechi".
    - Don't call an elder by first name alone.
  - **Formats:**
    - dates: DD/MM/YYYY
    - times: 12-hour clock, Indian time ("6:30 pm")
    - money: ₹1,62,400 (lakh grouping); show "₹", not "INR", to patients
    - phone numbers: +91 and 10 digits; mobile numbers start with 6–9
  - **Hospitals in the demo:** use made-up names, e.g. "Govt. Medical College Hospital, Kozhikode" for a public hospital, or "a private multispeciality hospital in Chennai". Never use a real hospital's brand.
  - **When to send messages:**
    - Default quiet hours 9 pm–7 am, which the family can change.
    - Allow pausing for fasting days, festivals and funerals.
    - No cheerful emojis on red-flag messages.
  - **Caregivers:** usually a spouse, son, daughter or daughter-in-law living in the same home (F-INDLOC-3). Sometimes a child lives abroad, so allow two WhatsApp contacts in different time zones.

## TECH (round 3)

### F-TECH-1: The VL53L1X laser sensor gives very steady readings but isn't exact out of the box: typical error ±20 mm, nothing closer than 4 cm, and a 27° beam. Each unit must be calibrated against the spirometer's printed scale
- Detail (ST datasheet, Rev 3):
  - **Minimum distance: 4 cm.** Closer than that, readings aren't accurate.
  - Overall error ("ranging error", which combines accuracy and repeatability) is typically **±20 mm** in the dark and **±25 mm** in ambient light. Test settings: long-distance mode, 100 ms per reading.
  - **Repeatability** (how much repeated readings vary) is much better: about 1%, down to 0.15% with longer readings.
  - Each reading can take 20 ms (short-distance mode only) up to 1,000 ms. The sensor can read up to 50 times a second.
  - The beam spreads at about **27°**. Our own geometry: the beam is about 2.4 cm wide at 5 cm, 9.6 cm at 20 cm and 12 cm at 25 cm. That's probably wider than the spirometer tube, so reflections off the tube wall are a risk. The sensing area can be narrowed in software.
  - The sensor needs offset and crosstalk calibration, especially behind a cover window.
- Source: ST VL53L1X datasheet DocID031281 Rev 3 – copy at https://www.pololu.com/file/0J1506/vl53l1x.pdf (#118) – B
- Use in build (**URGENT**):
  - Use short-distance mode with 20–33 ms per reading (30–50 readings a second). That's fast enough for the under-100 ms loop.
  - Narrow the sensing area as far as you can while it still sees the disc.
  - Keep the black foam ring (already in the plan).
  - Calibrate each spirometer at 2–3 of its printed marks.
  - Average a few readings at the top of each breath.
  - Our "±100 mL" target is reachable only through this calibration. The datasheet accuracy alone won't get there.
- Caveat: how many mL one mm of piston travel means on the Breazer 2500 is still unknown (gap). The datasheet tests used flat grey or white targets, not a small coloured disc inside a plastic tube.

### F-TECH-2: Tracking a spirometer with a camera has only been shown as a feasibility demo, and digital readings can differ from the printed scale by ±500 mL
- Detail:
  - Turkey 2025: a tablet camera tracked the volume marker of a standard spirometer in real time. The AI models were trained on **scripted** data and reported 100% accuracy. Feasibility only; no testing on patients. (*Healthcare* 2025;13:2693)
  - Thailand 2026: a digital incentive spirometer was compared with a volume-type device in 150 people aged 7–80.
    - The two agreed well overall (ICC 0.87), and the average difference was 49 mL.
    - But single readings could differ by **−469 to +567 mL** (95% limits of agreement). Reading a volume scale by eye is itself imprecise. (*Biosensors* 2026)
  - Thailand 2025 trial: the same digital spirometer vs a 3-ball Triflo after open-heart surgery, 32 patients. No difference in lung function or breathing-muscle strength.
  - We found no open-source camera tracker for 3-ball devices on GitHub (#119).
- Source: Europe PMC abstracts (#120) – A
- Use:
  - A camera mode for 3-ball devices stays on the **roadmap**: "shown feasible, not yet validated".
  - Answer on accuracy: "We calibrate to the printed marks. Even reading these scales by eye varies by hundreds of mL. We count good breaths; we don't claim lab-grade volume."
- Caveat: small studies.

## REG (round 3)

### F-REG-1: CDSCO's final software guidance (21 July 2026) decides by what the software does. Wellness, education and plain data-transfer software are not medical devices. Real-time patient monitoring, or numbers used for clinical decisions, are. Software that drives a device gets that device's class
- Detail:
  - Document no. CDSCO/MD/GD/MDSW/01/2026 (circular dated 21 Jul 2026). It drops the separate "SaMD" and "SiMD" labels and uses one category, "medical device software" (MDSW).
  - **Not a medical device:**
    - software only for general wellness, fitness, education or training
    - software that only transfers, stores, formats or communicates data
  - **A medical device:** software with a medical purpose. This includes "real-time patient monitoring" and measuring body readings that feed clinical decisions.
  - **Class:**
    - Software that drives or influences hardware gets **the same class as that hardware**.
    - Stand-alone software is classed by how much its information matters to care decisions and how serious the condition is.
  - **AI software** must document:
    - its training data
    - risks of bias, drift and hallucination
    - it may also need **testing on Indian patients**
- Source: analysis by law firm Nishith Desai Associates – https://nishithdesai.com/research-and-articles/hotline/pharma-healthcare-update/from-code-to-compliance-decoding-indias-medical-device-software-guidance-15623 (#123) – B (the CDSCO PDF itself was not opened)
- Use in the hackathon: describe SpiroBuddy as "an exercise coach and adherence tracker for a spirometer the nurse has already prescribed. It doesn't diagnose and doesn't measure lung function." The nurse dashboard flags missed sessions, not a patient getting worse.
- Caveat: once we alert nurses about a patient's breathing, we are probably a medical device (see F-REG-2).

### F-REG-2: CDSCO lists diagnostic and monitoring spirometers as Class B. We didn't find incentive spirometers in the respiratory or anaesthesiology lists
- Detail:
  - Respiratory list:
    - "Diagnostic Spirometer": Class B
    - "Monitoring Spirometer" (measures each breath's volume, or volume per minute, to check how well a patient is breathing): Class B
  - Anaesthesiology list: includes a peak flow meter.
  - No "incentive spirometer" or "lung exerciser" row in either list.
- Source: copies of CDSCO notifications on consultancy site Morulaa – #124, #125 – B
- Use (honest answer): "If we market it as monitoring breathing, it probably sits next to monitoring spirometers in Class B (low-to-moderate risk). As an exercise coach, it may count as wellness. We'll ask CDSCO's classification portal before launch."
- Caveat: consultancy copies, not the CDSCO PDFs. Other device lists weren't checked.

### F-REG-3: India's data protection rules (DPDP Rules 2025, primary text): most duties start around May 2027. From then we need a plain-language notice listing each piece of data, easy withdrawal, encryption, access logs kept for a year, and breach reports within 72 hours
- Detail:
  - Notified 13–14 Nov 2025 (G.S.R. 846(E)).
  - When the rules start:
    - Rules 1, 2 and 17–21 apply now.
    - Rule 4 (consent managers) applies after one year, about Nov 2026.
    - Rules 3, 5–16 and 22–23 apply after **18 months, about May 2027**.
  - **Notice (rule 3):**
    - must stand on its own, in clear and plain language
    - must list **each item** of data collected and each purpose
    - must give a way to withdraw consent **as easily as it was given**
  - **Security (rule 6):**
    - encryption or masking, access control, **access logs** and backups
    - logs kept for **one year**
  - **Data breaches (rule 7):**
    - tell each affected person without delay
    - tell the Data Protection Board within **72 hours**
  - **Guardians (rule 11):** a "lawful guardian" is one appointed by a court or a designated authority. An adult son or daughter isn't automatically one. So the elderly patient must consent personally; the family member is a contact the patient chooses.
  - Clinics and hospitals don't need a parent's consent to use a child's data for health care (Fourth Schedule). This doesn't affect adult patients.
- Source: DPDP Rules 2025, MeitY Gazette PDF – https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf (#122) – **A**; KPMG summary (#121) – B
- Use in build (**India-fit QA**):
  - Consent screen in the patient's language, read aloud.
  - It lists each data item: name, phone, surgery type, breath counts, voice replies.
  - One tap or one word ("stop") withdraws consent.
  - The patient chooses which family number gets updates.
  - The demo uses fake patients only.
- Caveat: unlike some older Indian rules, the DPDP Act has no special "health data" category. All personal data gets the same basic protection.

## VOICE (round 3)

### F-VOICE-11: Sarvam's own guide says wellness content should be "relaxed" (pace 0.8–0.9) and "warm" (temperature 0.7–0.8). It names recommended voices for each language, and says streaming is faster than one-shot requests
- Detail:
  - Recommended Bulbul v3 voices (female / male):

    | Language | Female | Male |
    |---|---|---|
    | Hindi | priya, suhani | shubh, ashutosh |
    | Tamil | ishita, ritu | ratan, rohan |
    | Malayalam | pooja | shubh |
    | Telugu | neha, priya | shubh, ratan |
    | Kannada | neha, ishita | shubh, ratan |
    | Bengali | roopa, suhani | rehan |
    | Marathi | priya, ritu | ratan |
    | Gujarati | priya, ritu | ratan |
    | Punjabi | roopa, suhani | mani |
    | Odia | ritu, pooja | shubh |
    | English | ishita | ratan |

  - Avoid "varun", a dramatic character voice. Bulbul v3 has **no pitch or loudness control**.
  - Speed:
    - A one-shot request (REST) returns the whole clip at once, so there's more delay.
    - Streaming (WebSocket or HTTP) is faster.
    - Phone calls use the `mulaw` format at 8 kHz.
  - Latency: Sarvam's marketing claims under 250 ms before the first audio arrives over WebSocket (search snippets only, not opened – C). No independent test found.
- Source: Bulbul v3 best practices – https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/bulbul-v3-best-practices.md (#126) – B
- Use in build (**URGENT, voice**):
  - Elderly preset: **pace 0.85, temperature 0.7**.
  - Female voice by default: pooja for Malayalam, ishita for Tamil, priya for Hindi. Offer a male voice too.
  - Generate the fixed coaching lines in advance (one-shot requests are fine for those). Use streaming only for live answers.
  - With LASI (F-INDLOC-3) in mind: repeat the key number, keep sentences short, and show the same words in large text.
- Caveat: we haven't listened to the voices. Let one older listener per language choose.

### F-VOICE-12: Bhashini sign-up and an API key seem free for developers, but we found no official terms or usage limits
- Detail: third-party guides describe signing up on the Bhashini dashboard, getting an API key from "My Profile", and using the Dhruva endpoint. We found no official page on startup usage limits or commercial-use terms.
- Source: search snippets only – C
- Use: keep AI4Bharat Indic-TTS (F-VOICE-10) and the browser's built-in voices as the offline fallback. Mention Bhashini only as "a government option we'd evaluate".

## BIZ (round 3)

### F-BIZ-1: Ayushman Bharat pays a fixed bundle per operation: CABG ₹1,62,400 (10-day stay), gallbladder removal ₹31,100, lung-lobe removal ₹32,900, knee replacement ₹36,400 + ₹60,500 for the implant
- Detail:
  - Source list: the HBP 2022 rate list (general ward, base "Tier3 (Z)" column), as adopted by Nagaland's state scheme.
  - Packages are "bundled and all inclusive". So extra days or complications within the package are paid by the hospital.
  - Expected hospital stays:

    | Operation | Expected stay |
    |---|---|
    | CABG | 10 days |
    | Gallbladder removal | 6 days |
    | Lung-lobe removal | 5 days |
    | Knee replacement | 5 days |

- Source: HBP 2022 list, Nagaland State Health Agency – https://cmhis.nagaland.gov.in/storage/pageFiles/381.pdf (#128) – **A** (government document)
- Use in pitch: "Under Ayushman Bharat a hospital gets about ₹1.6 lakh for a bypass, whatever happens. Every extra day caused by a lung complication comes out of that. A few hundred rupees of coaching per patient is a small price to protect it."
- Caveat: one state's copy. Rates differ by city tier and state, and the list may have been revised since 2022.

### F-BIZ-2 (proxy): in an ICU in north India, pneumonia on a ventilator added about US$5,200 per patient and doubled the hospital stay (21 vs 11 days)
- Detail: 95 of 250 ventilated patients got ventilator-associated pneumonia (VAP). Hospital costs were $6,251 for them vs $2,599 for the others (2015).
- Source: J Infect Public Health 2015, PMID 25444392 (#129) – A
- Use: only as a stand-in for "lung complications are expensive in India too". It is **not** the cost of a lung complication after surgery, so don't present it as one.
- Caveat: ICU patients on ventilators, 2015 dollars. We still haven't found the rupee cost of a lung complication after surgery in India.

### F-BIZ-3: Indian hospital chains already pay for monitoring patients at home after surgery: Manipal and ConnectedLife (2022) for knee replacement, angioplasty and bypass patients
- Detail:
  - Remote monitoring with Fitbit watches, with reminders for medicines and physiotherapy and alerts when vital signs look abnormal. Manipal reported "improved" adherence, without numbers.
  - During COVID: Max Healthcare's 15-day remote-monitoring package cost from ₹333/day (search snippet, C).
- Source: Healthcare IT News, Mar 2022 – #130 – B
- Use: the business model is **hospital-paid (B2B)**: a post-discharge programme, bundled into the surgery package or charged as a small fee at discharge. SpiroBuddy adds the missing piece: the lung exercises.
- Caveat: no prices or results published.

## COMP (round 3)

### F-COMP-8: Tidal Medical's international (PCT) patent application has lapsed and shows no Indian filing. Google Patents finds no Indian patent for an incentive-spirometer tracker
- Detail:
  - WO2022204480A1 (priority date 26 Mar 2021), "Systems and methods for monitoring of incentive spirometry".
    - Status: **Ceased**. It never entered the European phase, and the only country listed is WO (international).
    - Its text covers measuring the piston's travel time with light **or sound**, and even voice-activated switches.
  - A Google Patents search for Indian spirometer filings returned only 2 old, unrelated families.
- Source: Google Patents – #132 – A (patent record; the legal status is Google's assumption); #131 – C
- Use (judge answer): "Tidal's US patents don't extend to India. As far as public databases show, their international application lapsed without an Indian filing."
- Caveat: Google's coverage of Indian patents is incomplete. **The Indian patent office database (InPASS) wasn't searched.** This isn't legal advice.

### F-COMP-9: Respira Health runs lung rehab over WhatsApp in India. Only 18% of people who signed up finished a short programme, but 30% of those referred by a hospital did
- Detail:
  - Founded in 2025, incubated by AIM (Ambitious Impact).
  - A WhatsApp chatbot (built on Turn.io) plus physiotherapists working online, in English and Hindi. An 8-week rehab programme for COPD.
  - First test:
    - 140+ breathless people signed up.
    - 12–13% of adults aged 40–64 and 65+ who saw the ads clicked them.
    - 18% finished overall: about 30% of hospital referrals vs 14% of people recruited through online ads.
- Source: the founders' post on the EA Forum – #133 – C (self-reported)
- Use:
  1. Not a competitor for post-surgery spirometry, but proof that older Indians use WhatsApp health bots.
  2. **Enrol patients at discharge through the nurse**, not through ads.
  3. Expect people to drop off. The device's beep and voice work even if nobody opens WhatsApp.
- Caveat: self-reported numbers, not peer-reviewed.

### F-COMP-10: Hobby projects already give spoken "slow down / speed up" feedback on a spirometer
- Detail:
  - d-eniz/incentive-spirometer-voice: an Arduino with an ultrasonic sensor. Its voice says "Safe speed", "Slow down" or "Speed up".
  - shaoyuancc/spiro-android: an app built for a clinical study of spirometer adherence.
  - Each has 0–1 GitHub stars.
- Source: GitHub (#119) – C
- Use: don't claim spoken pace feedback as new. What's new in our design is the combination: coaching in Indian languages, AI that checks technique, and the nurse-and-family loop for Indian homes.

## VIS (round 3)

### F-VIS-1: An Indian study at 5 centres ran lung rehab at home for TB survivors, with phone follow-up. 246 of 260 completed 12 weeks, and walking distance, quality of life and lung function improved
- Detail:
  - A physiotherapist taught the exercises once in the clinic. Patients then continued at home, with phone follow-up for 12 weeks.
  - Improvements: 6-minute walking distance, balance, muscle strength, quality of life (SGRQ) and lung function (FEV1/FVC).
  - The authors suggest adding this rehab to India's National TB Elimination Programme.
- Source: Sinha et al., *Indian J Med Res* 2025, PMID 40844105 (#116) – A
- Use (roadmap slide): "Lung rehab at home after TB has been shown to work in India. SpiroBuddy's coach and nurse dashboard can be the remote follow-up layer."
- Caveat: a before-and-after study with no comparison group. Participants were selected because they attended well.

## JUDGE – 15 tough questions with short answers

| # | Question | Short answer | Evidence |
|---|---|---|---|
| J1 | "Does incentive spirometry even work?" | "On its own, the evidence is weak. As part of a nurse-led bundle of breathing care, it helps. The trials never checked whether patients actually did the exercise. We make that visible." | F-CLIN-3, F-CLIN-6, F-CLIN-7, F-CLIN-4 |
| J2 | "What proof is there that reminders help?" | "In a randomised trial of 145 bypass patients, hourly reminders doubled the share of waking hours with exercise (58% vs 28%) and breaths per day (35 vs 17)." | F-ADH-1 |
| J3 | "InSee already exists and is FDA-cleared. Why you?" | "InSee proves laser tracking works in US hospitals. It fits one US spirometer and is for hospital use only. We add home use, Indian devices, technique AI, coaching in Indian languages and WhatsApp for the family." | F-COMP-1, F-COMP-5, F-COMP-7 (imported) |
| J4 | "Aren't you infringing Tidal's patents?" | "Patents are national. Their US patents don't cover India, and public databases show their international application lapsed without an Indian filing. We'd do a formal check before any US launch." | F-COMP-6, F-COMP-8 |
| J5 | "How accurate is the sensor?" | "Out of the box the chip is accurate to about ±2 cm. But its readings are very steady, so we calibrate it to each spirometer's printed marks. Even reading the scale by eye varies by hundreds of mL. We coach good breaths; we don't claim lab-grade volume." | F-TECH-1, F-TECH-2 |
| J6 | "Most Indian patients get the 3-ball type. Then what?" | "True for many home patients. The US guideline suggests the volume type, and an Indian trial found it better for walking recovery. A camera mode for 3-ball devices is on the roadmap; it has been shown feasible but not yet tested on patients." | F-INDIA-10, F-CLIN-4, F-CLIN-9, F-TECH-2 |
| J7 | "Old patients don't use smartphones." | "Right: only 41% own one, and 3 in 4 older women can't read. That's why the device speaks and the WhatsApp update goes to a family member. Two in three older Indians live with their children." | F-INDIA-5, F-INDLOC-3 |
| J8 | "Is it a medical device? What about CDSCO?" | "Today it's an exercise coach and adherence tracker. CDSCO's July 2026 guidance decides by what software does. If we marketed it as monitoring breathing, it would probably sit near monitoring spirometers (Class B). We'll get an official ruling first." | F-REG-1, F-REG-2 |
| J9 | "Data privacy?" | "The demo uses fake patients. For launch, we follow the DPDP Rules: a notice in the patient's language that lists each piece of data and is read aloud, one-word withdrawal, encryption and access logs, and breach reports within 72 hours. The patient consents, not the son." | F-REG-3 |
| J10 | "Can you legally robocall patients in India?" | "Under TRAI's 2026 rules, AI calls are 'A2P calls'. They must be declared in advance and come from an Indian registered number, and some reminder calls need consent renewed every week. So calls are our escalation step through an Indian partner. WhatsApp and the device work today." | F-COMMS-8, F-COMMS-11 |
| J11 | "What does it cost, and who pays?" | "The parts cost a few hundred rupees, a WhatsApp update about 12 paise, and the voice a few paise per message. The hospital pays: Ayushman Bharat pays a flat ₹1.6 lakh for a bypass, so avoiding extra days protects its margin. Indian hospital chains already buy post-surgery monitoring." | F-COMMS-2, F-VOICE-2, F-BIZ-1, F-BIZ-3 |
| J12 | "Won't the AI end up giving medical advice?" | "No. It only coaches and summarises, and says it's an AI. Red-flag words trigger a fixed 'call your nurse or 112' message, and a nurse reviews every flag. Sarvam's terms require this too." | F-VOICE-8 |
| J13 | "Why will patients keep using it? WhatsApp bots lose most users." | "True: an Indian WhatsApp rehab bot saw 18% completion overall, but 30% when hospitals referred patients. We enrol patients at discharge through the nurse, and the device beeps and speaks even if nobody opens WhatsApp." | F-COMP-9, F-ADH-1 |
| J14 | "A Korean app with hourly alarms showed no benefit." | "Go-breath relied on patients reporting their own use, with no sensor. We record every breath automatically, as the successful US trial did." | F-ADH-5, F-ADH-1 |
| J15 | "Is India's problem big enough?" | "Public records alone show about 49 lakh major operations a year (an undercount). Roughly 1 in 10 surgical patients gets a lung complication, and in one Indian study 28% of those patients died. India also has fewer nurses than WHO recommends." | F-INDIA-1, F-CLIN-1, F-CLIN-8, F-INDIA-7 |

# Round 4 additions (9 Oct 2026)

## REG (round 4)

### F-REG-4: CDSCO's software guidance (primary text): wellness software must not mention any disease, and software that alerts about a condition is never wellness. Standalone software that only informs care of a serious condition is Class A
- Detail (read in the PDF itself, Doc No. CDSCO/MD/GD/MDSW/01/2026, 62 pages):
  - **Scope:** the guidance excludes software meant only for general wellness, a healthy lifestyle, or tracking body measures for fitness, *as long as* it has no medical purpose.
  - **Wellness rules:** a wellness claim may talk about keeping up or improving general health, but it **must not refer to any disease, disorder or condition**. Software that measures or reports body values for screening, diagnosis, **monitoring, alerting** or managing a condition is **not** wellness.
  - **Hardware link:** software that drives or influences a hardware medical device gets the **same class as that device**. Apps that control a device over Bluetooth or Wi-Fi count as medical devices.
  - **Table 2, standalone software:** class depends on how serious the condition is and what the software does. *Serious* condition: treat/diagnose = C, drive clinical management = B, **inform clinical management = A**. *Critical*: D / C / B. *Non-serious*: B / A / A.
  - **Licensing:** only Class A devices that are **non-sterile and non-measuring** skip the licence and just register. A device that measures needs a licence.
  - The guidance itself is "for public awareness", not law. Its date isn't printed on the pages we read; secondary sources say 21 July 2026.
- Source: CDSCO, Guidance Document on Medical Device Software under MDR-2017 – https://www.cdsco.gov.in/opencms/export/sites/CDSCO_WEB/Pdf-documents/Guidance-document-on-Medical-Device-Software-under-MDR-2017.pdf (#135) – **A**
- Use in pitch: two honest routes. (1) **Wellness mode:** "a breathing-exercise coach" with no disease named on the box or in the app. (2) **Care-team mode** (nurse summary and alerts): medical device software. If it only *informs* the nurse about recovery after surgery (serious, not critical), Table 2 points to **Class A**, but because it measures volume it still needs a licence, not just registration.
- Caveat: our reading, not a ruling. In the US, incentive spirometers themselves are Class II (21 CFR 868.5690, search snippet only). We still haven't found an Indian class for incentive spirometers (F-REG-2).

## TECH (round 4)

### F-TECH-3: A laser sensor inside a tube picks up echoes off the walls, which make readings too short. Fix: shrink the sensing window to 4x4 (about 15° instead of 27°), use dull dark walls, and keep a clear target
- Detail:
  - In ST's own forum, users and ST staff say that once the beam touches the side walls, light bounces back early and the sensor **under-reads**. Advice: matte black inner walls; the VL53L1X (unlike older chips) can turn off the outer light detectors to **narrow its view**.
  - Several forum posts quoting ST's manual: full array (16x16) ≈ 27°, 8x8 ≈ 20°, **4x4 ≈ 15° (the minimum)**. The window is set with VL53L1X_SetROI(dev, X, Y), sizes 4–16. A smaller window also lowers the maximum range, which doesn't matter at our 4–20 cm.
  - Team geometry (our maths, not a source): at 15 cm the full 27° cone is about **7 cm wide**; at 4x4 (15°) it's about **4 cm wide**. So in a 5–7 cm cylinder only the narrowed window stays off the walls at the top of travel.
- Source: ST Community, "VL53L1X in a tube.. Tips and tricks?" – https://community.st.com/imaging-sensors-49/vl53l1x-in-a-tube-tips-and-tricks-20936 (#136) – **C** (forum, includes ST staff); ROI figures from forum snippets (#149) – **C**
- Use in build: firmware sets ROI 4x4 (centred); mount the sensor on the cylinder axis; put a matte-white dot on the piston top as the target; calibrate at 3 printed marks. Use in pitch: "we narrowed the laser to fit inside the tube".
- Caveat: forum evidence. No published test of a VL53L1X inside an incentive spirometer exists. Our own bench test is the real proof.

### F-TECH-4: The Romsons Breazer 2500's inner size and mL per mm of piston travel are not published anywhere we could find, so each model must be calibrated against its printed scale
- Detail: retailer pages (1mg, Medikabazaar, Truemeds), the supplier listing (HSN code 90192090 only), and YouTube titles give no drawing, inner diameter or mL-per-mm value. Team reasoning (not a source): volumetric spirometer scales are set by the maker, not by simple cylinder geometry, so **don't calculate mL from the diameter**. Map distance to the printed marks (for example 500, 1500 and 2500 mL) instead.
- Source: #137, #138 and search results (#149) – **C**; absence of evidence
- Use in build: a calibration table per spirometer model (distance in mm → mL), filled by hand on hackathon day with calipers and the printed marks.
- Caveat: whether the floor under the piston is open remains unknown. Look at a real unit.

## COMMS (round 4)

### F-COMMS-12: TRAI's own press release (18 Sep 2026) confirms the A2P rules and adds three things: a termination charge of up to 5 paise a minute, a 7-day window after a customer's written inquiry, and a ban on spam apps blanket-tagging official number series
- Detail:
  - A2P call = a call started by software or an automated platform without a human dialling, including robocalls and pre-recorded or artificial voices. **Every sender must pre-declare A2P use and its caller IDs**; undeclared A2P calls count as spam.
  - The receiving operator may charge up to **₹0.05 a minute** for A2P calls; official 140/1600 series are exempt.
  - Commercial messages may follow a customer's **written or digital inquiry for 7 days only**. This is separate from the type (ii) service-call consent in F-COMMS-8.
  - **Call-management apps** (such as caller-ID apps) may not blanket-block or tag the official 140xx, 1600xx and 1601xx series as spam. Users can still block calls on their own phones.
  - Operators' AI flags a sender when 5 or more of its numbers are flagged within 10 days. Then come KYC re-checks, possible barring and disconnection. Complaint-based action now starts at 3 complaints in 10 days, if the AI has also flagged the number.
  - Timeline: draft 13 Mar 2026, comments until 19 Apr / 4 May, open house 3 Jun, issued 18 Sep 2026. **The Gazette date is still not found.**
- Source: TRAI Press Release No. 119/2026 – https://www.trai.gov.in/sites/default/files/2026-09/PR_No119of2026.pdf (#139) – **A**
- Use in pitch: "Our calls would be declared A2P calls from a hospital's registered number. WhatsApp and the device do the daily work."
- Caveat: press release summary. Legal detail is in the regulation (#106).

### F-COMMS-13: Exotel asked TRAI to exempt "human-assisted" calls (an app connects a live person, for example a healthcare teleconsultation) from the A2P rules. We don't yet know if the final rules accepted this
- Detail: in its April 2026 comments, Exotel proposed that a call with a live human agent actively taking part should not count as an A2P call. Its examples included healthcare teleconsultation and click-to-call. It argued the A2P burden should fall on automated, pre-recorded calls.
- Source: Exotel comments on the draft TCCCPR Third Amendment – https://www.trai.gov.in/sites/default/files/2026-04/Exotel_TRAI_TCCCPR_Comments_v2.pdf (#140) – **B**
- Use in build: design the escalation as **nurse clicks "Call patient" → the phone line connects nurse and patient**, a human call, rather than an AI robocall. This is the safest design under either outcome.
- Caveat: an industry wish, not the final rule. Check #106 for "human".

## BIZ (round 4)

### F-BIZ-4: A hospital bed-day in India costs about ₹2,307 on average, and a surgical procedure about ₹10,686 (national costing study, 57 hospitals in 11 states)
- Detail: the Cost of Health Services in India (CHSI) study covered 11 public tertiary hospitals, 27 district hospitals and 16 private hospitals. Its mean cost was ₹2,307 per inpatient bed-day and ₹10,686 per procedure. Teaching hospitals cost more per bed-day. The study is used to set PM-JAY payment weights.
- Source: "Refining the provider payment system of India's government-funded health insurance programme", *BMJ Open* 2023, PMID 37857541 (#141) – **A**
- Use in pitch: "Every extra day in a ward costs an Indian hospital about ₹2,300. In PM-JAY's fixed bundle, that comes out of the hospital's margin."
- Caveat: provider cost, not price. Data from before 2023.

### F-BIZ-5: At PGIMER Chandigarh, an ICU bed-day cost the health system ₹25,927, and a patient with ventilator pneumonia cost ₹5.44 lakh vs ₹2.07 lakh without it (2021–22)
- Detail: trauma ICU, 494 admissions. Ventilator pneumonia (VAP) affected 9.7% of ventilated patients. Average stay was 21 days with VAP vs 8.2 without.
- Source: "Ventilator-associated pneumonia – What price does the public health system pay?", *Lung India* 2024, PMID 38953191 (#142) – **A**
- Use in pitch (illustrative, label it so): the Udaipur study's patients with lung complications spent about 7 more ICU days (F-CLIN-8). At PGIMER's ICU cost, that's about **₹1.8 lakh** of extra ICU cost per complicated patient. Say "up to about ₹2 lakh", and say it is a back-of-envelope figure.
- Caveat: VAP ≠ post-surgery lung complication. Trauma ICU at a teaching hospital. Combining two studies is our own calculation.

### F-BIZ-6 (weak, Grade C): Home-care price anchors: Apollo HomeCare launched home nursing at about ₹2,000–3,600 a day; Portea's home ICU was about ₹6,500–12,000 a day (2018); Tricog's post-discharge monitoring runs at least 6 months
- Source: search snippets (#149, not opened) and the Tricog news reprint, 2023 (#145) – **C**
- Use: shows families and hospitals already pay thousands of rupees a day for home care, so a few hundred rupees per recovery episode is small.
- Caveat: old and undated prices. Check the current price pages.

### F-BIZ-7 (team estimate, not a source): unit economics sketch
- Parts (Indian retail, snippets #149): VL53L1X module ₹399–₹859, ESP32-C3 board ₹299, plus battery, buzzer/speaker and case, roughly ₹300–500. **About ₹1,000–1,700 per clip-on at hobby prices**, less in volume.
- Reusable: one clip-on serves about 10+ patients after cleaning, so roughly ₹100–170 of hardware per patient.
- Running cost for a 14-day recovery: WhatsApp 3 updates a day × ₹0.115 ≈ **₹5**; voice coaching ≈ ₹0.6 a message, or **₹0** with pre-made clips (F-VOICE-1); cloud costs negligible.
- Price idea: **₹500–1,000 per patient episode, paid by the hospital.** That is less than half of one ward bed-day (₹2,307, F-BIZ-4) and a small fraction of one ICU day (₹25,927, F-BIZ-5).
- Caveat: our own estimate. Not validated with any hospital.

## COMP (round 4)

### F-COMP-11: Indian home-monitoring players exist (Zorgers + Clinitouch for COPD at home, Tricog after discharge, Dozee in hospital beds), but none tracks incentive-spirometer exercise
- Detail: Mohali's Zorgers partnered with UK firm Clinitouch (Spirit Health) to bring remote monitoring to COPD and lung patients at home in India; Clinitouch's patients average **77 years old** worldwide, and an offline mode was planned for early 2025 (article updated Nov 2024). Tricog monitored patients discharged after heart failure or surgery with two Bengaluru hospitals, for at least 6 months (2023). Dozee monitors heart and breathing in hospital beds (snippet).
- Source: Digital Health News (#144) – **B**; Tricog news reprint (#145) – **C**
- Use in pitch: "Home monitoring after discharge is a real Indian market. Nobody measures whether the patient actually does the breathing exercise."
- Caveat: no prices or outcomes published.

## VIS (round 4)

### F-VIS-2: India's TB programme (NTEP) says every patient completing TB treatment should be checked for post-TB lung disease, and lists home-based activity and inspiratory muscle training in rehab
- Detail: Standard 1: evaluate everyone completing treatment (chest X-ray, lung function, 6-minute walk, symptoms, quality of life). Standard 2: rehab indications (breathlessness, poor exercise capacity, COPD or bronchiectasis, a hospital stay in the past year). Standard 3: rehab must include supervised exercise, education and **home-based activity plans**; core parts include inspiratory muscle training and airway clearance. A separate RBIPMT/Central TB Division guidance on pulmonary rehab for TB (July 2024) exists (snippet only).
- Source: NTEP, Clinical Standards for Post-TB Lung Disease (Annexure 2) – https://ntep.in/node/6657 (#146) – **A**
- Use in pitch (roadmap): "After surgery today; next, India's TB survivors. The national TB programme already asks for home-based lung rehab."
- Caveat: an incentive spirometer isn't named. Inspiratory training uses other devices. Undated page.

### F-VIS-3: In Pune, 87% of 370 people with chronic lung disease wanted pulmonary rehab, and 84% liked a web-based programme at home (70% a paper manual)
- Detail: outpatient survey at a multi-speciality hospital, mean age 56. 80% of 207 doctors and physios thought rehab works, but many didn't know how to refer.
- Source: *Chronic Respiratory Disease* 2024, PMID 39075037 (#147) – **A**
- Use in pitch: demand for home-based breathing programmes in India.
- Caveat: one city, a hospital outpatient sample, stated preference only.

## JUDGE – round 4 additions (J16–J25)

| # | Question | Short answer | Evidence |
|---|---|---|---|
| J16 | "What does a lung complication cost an Indian hospital?" | "A ward day costs about ₹2,300 and an ICU day about ₹26,000 at a public teaching hospital. Patients with these complications spend about a week more in ICU, so roughly up to ₹2 lakh each. That's our rough estimate from two Indian studies." | F-BIZ-4, F-BIZ-5, F-CLIN-8 |
| J17 | "Your nurse alerts make this a medical device, don't they?" | "Yes, probably. CDSCO says alerting software isn't wellness. Software that only informs the nurse about a serious but not critical condition points to Class A, and because it measures, it needs a licence. We'd apply before launch; the hackathon build is a coach." | F-REG-4 |
| J18 | "Can a laser even work inside a plastic tube?" | "Wall echoes are a known problem. We narrow the sensor's view from 27° to about 15°, aim it down the middle, and calibrate on the printed marks. We'll show the live reading against the scale." | F-TECH-3, F-TECH-1 |
| J19 | "How do you turn millimetres into millilitres?" | "We don't use geometry. We read the distance at the device's own printed marks and map between them, once per spirometer model." | F-TECH-4 |
| J20 | "Won't patients ignore calls marked as spam?" | "That's why calls are only the backup. Daily coaching happens on the device and WhatsApp. TRAI now bars caller-ID apps from blanket-tagging official commercial series, and a hospital's declared number is the right channel." | F-COMMS-12, F-COMMS-13 |
| J21 | "Who else does home monitoring in India?" | "Zorgers with Clinitouch for COPD, Tricog after discharge, Dozee in hospital. None checks whether patients do their breathing exercise, or how well." | F-COMP-11 |
| J22 | "Is this just for surgery?" | "Surgery first. Next is TB survivors: NTEP asks for every patient finishing treatment to be checked, with home-based rehab. An Indian trial completed 246 of 260 patients at home." | F-VIS-2, F-VIS-1 |
| J23 | "What are your unit economics?" | "About ₹1,000–1,700 of parts for a reusable clip-on, so roughly ₹150 a patient over 10 uses, plus about ₹5 of WhatsApp per recovery. We'd charge the hospital ₹500–1,000 per patient, less than half a ward day." | F-BIZ-7, F-BIZ-4 |
| J24 | "After TRAI's new rules, can you still call patients?" | "Yes, if done right: an Indian registered sender, declared A2P caller IDs, and consent recorded at discharge. Our escalation is a nurse-to-patient call, so a human is on the line." | F-COMMS-8, F-COMMS-12, F-COMMS-13 |
| J25 | "Do Indian patients even want home programmes?" | "In Pune, 87% of chronic lung patients wanted rehab and 84% liked a home-based digital programme. Hospital-referred users of a WhatsApp rehab bot finished more often." | F-VIS-3, F-COMP-9 |

# Round 5 additions (9 Oct 2026)

## REG (round 5)

### F-REG-5: CDSCO's own Class A list names "Incentive spirometer" (item 496) as a low-risk, non-sterile, non-measuring device that "is not a diagnostic device". Such devices only need a simple registration, not a licence
- Detail: CDSCO list F. No. MED-16014(12)/1/2024-eoffice-Part(2), "Risk classification list of Class A (non-sterile and non-measuring) medical devices" (about 1,069 items; news reports date it to 3 Nov 2025). Item 496 describes a hand-held mechanical breathing-muscle exerciser that encourages deep breaths after surgery to prevent lung collapse. Item 810, "Pulmonary exerciser" (breathing-muscle trainers), is on the same list. The note on page 1 says these devices are exempt from Chapters IV, V, VII, VIII and XI of the Medical Devices Rules 2017 (the licensing chapters), provided the maker or importer registers them under Chapter IIIB. A consultancy copy of the January 2025 "Class A self-notified" list also includes "Pulmonary exerciser" (#432) but not "incentive spirometer".
- Source: CDSCO PDF "Risk based classification list of Class A (non-sterile and non-measuring) medical device" – https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadPublic_NoticesFiles/Risk%20based%20classification%20list%20of%20Class%20A(non-sterile%20and%20non-measuring)%20medical%20device.pdf (ledger #150) – Grade A. Supporting: Morulaa Class A self-notified page (#151) – Grade B.
- Use in pitch: answers "is the spirometer itself regulated?" The plastic spirometer is in the lowest-risk class and isn't a diagnostic. SpiroBuddy clips onto a device CDSCO already treats as low-risk.
- Caveat: the exemption is for **non-measuring** devices. Our clip-on measures volume and alerts nurses, so SpiroBuddy itself is very likely **not** covered by this exemption. Under the July 2026 software guidance (F-REG-1, F-REG-4), it would probably be Class A *measuring* or Class B and need a licence. We did not find whether Romsons has registered the Breazer under Chapter IIIB (the CDSCO registration portal can't be searched from here).

## BIZ (round 5)

### F-BIZ-8: About 1 in 8 heart-bypass (CABG) patients worldwide is readmitted within 30 days (12.9%), and lung problems are among the main causes. We found no Indian 30-day figure for CABG. After knee replacement in Ludhiana it was only 1.1%
- Detail: Meta-analysis of 53 studies, 8.9 million CABG patients (to June 2020): pooled 30-day readmission 12.9% (95% CI 11.3–14.4%). Causes: infection/sepsis, irregular heartbeat, heart failure, **respiratory complications (1–20% of readmissions)** and fluid around the lung (0.4–22.5%). Most readmissions were for non-cardiac causes. An Indian 2026 trial protocol (Amrita, Kochi) puts it at 10–20%, "particularly in LMICs". Knee replacement, Fortis Ludhiana, 609 patients 2017–22: 1.1% readmitted at 30 days, 1.8% at 90 days; unplanned visits 2.6% at 30 days.
- Source: Shawon et al., *J Cardiothorac Surg* 2021, PMID 34112216, doi 10.1186/s13019-021-01556-1, alias PMC8194115 (ledger #152) – Grade A. Ludhiana: *World J Orthop* 2024, PMID 39165878 (#153) – Grade A (single centre). Amrita protocol: #154.
- Use in pitch: bypass patients are the strongest readmission story; knee patients are not. For knee patients, talk about recovery and adherence, not readmissions.
- Caveat: the 12.9% is mostly US/Western data. No Indian CABG readmission number was found (two Europe PMC searches). Don't claim SpiroBuddy reduces readmissions; say "we'll measure it in a pilot".

### F-BIZ-9 (weak, Grade C/B): Home-care price anchors, 2026: the big providers don't publish prices; older figures and directories suggest a home physio visit from about ₹500 and a home attendant at ₹1,800–3,200 a shift
- Detail: Max@Home's Delhi "cost" page and Portea's Bangalore physiotherapy page (both opened Oct 2026) show no rupee prices ("depends on needs"). Search snippets only (not opened): an old Portea landing page (©2022) priced 12/24-hour trained attendants at ₹1,800–3,200 by city; Portea page metadata shows physiotherapy "from ₹499"; a 2026 elder-care directory gives ₹24,000–40,000/month for a 12-hour qualified nurse in Chennai and ₹12,000–18,000/month for a Delhi attendant.
- Source: Max@Home (#155), Portea (#156) – Grade B (no price found); snippets (#160) – Grade C.
- Use in pitch: "One home physiotherapy visit costs about what we'd charge for a whole two-week recovery (₹500–1,000)." Label as approximate.
- Caveat: no current, official, published price. Don't put a specific Portea price on a slide.

## COMP (round 5)

### F-COMP-12: An Indian hospital is already testing an AI nurse chatbot after heart bypass: Amrita's "Smart CABGuard" (Kochi), with an LLM and a single-lead ECG. It requires a smartphone and doesn't track breathing exercise
- Detail: *JMIR Research Protocols* 2026: a nurse-led clinical decision-support chatbot (fine-tuned Mistral-7B with a risk score and explainable AI) plus continuous single-lead ECG from Amrita's own device, to predict and prevent complications and 30-day readmission after isolated CABG. Phase III is an open-label RCT; adults with **smartphone access** only. Usability target ≥80%.
- Source: *JMIR Res Protoc* 2026, PMID 42550966, doi 10.2196/103717 (ledger #154) – Grade A (protocol, no results yet).
- Use in pitch: proves Indian hospitals want AI-assisted, nurse-led follow-up after surgery. We are complementary: breathing-exercise tracking, voice for patients without smartphones, family WhatsApp. A possible partner, not just a competitor.
- Caveat: it's a protocol; no outcomes yet. Judges from Kerala may know it.

## ADH (round 5)

### F-ADH-6: In a Chennai hospital, only 6% of 60 post-surgery patients used their spirometer adequately on day 1 after surgery; 54% did it inadequately. By day 3, with teaching, 72% did it adequately
- Detail: Descriptive study, general-surgery inpatients, flow-type (ball) incentive spirometer, Saveetha (Chennai), 2024. Day 1: 6% adequate, 40% moderately adequate, 54% inadequate. Day 2: 40% adequate. Day 3: 72% adequate. No link to age, sex or education.
- Source: *J Pharm Bioallied Sci* 2024, PMID 39346353, doi 10.4103/jpbs.jpbs_565_24 (ledger #157) – Grade A (small, descriptive).
- Use in pitch: technique is poor right when it matters most (day 1), and it improves with coaching. That's what our technique feedback does at home, when the nurse isn't there.
- Caveat: in hospital, not at home; 60 patients; scoring tool not described in the abstract. We still have **no Indian data on spirometer use after discharge** (searched twice).

### F-ADH-7: An Indian randomised pilot that supported family caregivers (Hindi website, booklet and a moderated WhatsApp group) after cancer surgery halved unplanned follow-up visits and lowered caregiver burden
- Detail: Tata Memorial Centre unit, Muzaffarpur (Bihar), 75 oral-cancer surgery patients and their main caregivers. Intervention vs standard care: unplanned follow-ups 1.23 vs 2.64 (mean); caregiver burden (Zarit) 12.3 vs 17.5 (p=0.021). 30-day complications and swallowing recovery were the same in both arms.
- Source: *Indian J Cancer* 2026, PMID 42301659, doi 10.4103/ijc.ijc_109_25 (ledger #158) – Grade A (pilot RCT, small).
- Use in pitch: evidence from rural India that bringing the family in through WhatsApp reduces unplanned hospital trips and family stress. Supports the guardian WhatsApp update.
- Caveat: different surgery; no difference in complications. Say "fewer unplanned visits", not "fewer complications".

### F-ADH-8: Across 76 TB studies (86,586 people), digital adherence tools gave a modest, uncertain boost to treatment success (OR 1.14). Smartphone apps did better (OR 2.17), and digital tools made side-effects get reported more often (OR 1.57)
- Detail: Systematic review to March 2024: SMS (18 studies), feature-phone (8), 99DOTS pill sleeves with calls (6), video-observed therapy (18), apps (7), digital pillboxes (21). Treatment success in RCTs OR 1.14 (0.99–1.30, very low certainty). Apps OR 2.17 (1.07–4.4, 3 RCTs, low certainty). Adverse-event reporting in RCTs OR 1.57 (1.25–1.97, moderate certainty).
- Source: *BMC Infect Dis* 2025, PMID 41087928, doi 10.1186/s12879-025-11503-3 (ledger #159) – Grade A.
- Use in pitch: honest answer to "do digital reminders work?": on their own, modestly. What digital follow-up reliably does is bring problems to the care team earlier, which is our nurse-alert design.
- Caveat: TB medicines, not breathing exercise. Low certainty overall.

## VIS (round 5)

### F-VIS-4: Post-TB market size: India notified about 26 lakh TB patients in 2024 and 90% are treated successfully. In Madurai, 59% of patients finishing treatment had impaired lung function, mostly the "stiff lung" (restrictive) type
- Detail: PIB (24 Mar 2026): treatment success under TB Mukt Bharat 90% (global 88%); 28 lakh+ diagnosed since Dec 2024. PIB also states 25.5 lakh (2023) and 26.07 lakh (2024) notified, the highest ever (search snippet). Madurai NTEP centres, 132 adults at treatment completion: lung function impairment 59% (95% CI 51–67%), restrictive pattern 55%. Mullana (Haryana) hospital study, 150 TB survivors: 48% restrictive and 34% mixed on spirometry; mean age 50.
- **Team estimate (not a source):** about 26 lakh × 90% ≈ 23 lakh people finish TB treatment each year. If roughly half have lung impairment, that's on the order of 10 lakh people a year who could need breathing rehab.
- Source: PIB "India Speeding Towards TB Elimination", 24 Mar 2026 (ledger #161) – Grade A. Madurai: *Cureus* 2026, PMID 41873289, doi 10.7759/cureus.103941 (#162) – Grade A (single district). Mullana: *Indian J Tuberc* 2025, PMID 42031463 (#163) – Grade A (hospital sample, likely sicker patients).
- Use in pitch: "the next market after surgery may be bigger than surgery". Deep-breathing exercise suits stiff (restrictive) lungs.
- Caveat: the 26 lakh includes TB outside the lungs; 59% is one district. Say "lakhs of people a year", not an exact figure. No guideline names incentive spirometry for post-TB rehab (NTEP lists breathing exercise and inspiratory muscle training, F-VIS-2).

## INDLOC (round 5)

### F-INDLOC-5: We found no peer-reviewed Indian study of voice or IVR health tools for older adults. A PGIMER trial (381 rural adults aged 60+) is testing IVR now and calls such evidence "scarce". A UK WhatsApp AI coach saw 28% of chats sent as voice notes
- Detail: PGIMER Chandigarh "Virtual Baithak" RCT protocol: 3 arms (IVR + nurse-moderated group calls, IVR only, usual care), weekly for 3 months, rural adults ≥60; outcomes: digital health literacy, technology acceptance. UK ophthalmology pilot E.M.M.A (WhatsApp AI coach, 83 users, 446 chats): 28% of chats were audio; 88% of 66 respondents satisfied; 9% reported mild-to-moderate anxiety.
- Source: *BMJ Open* 2026, PMID 41922061 (ledger #164) – Grade A (protocol). *Indian J Ophthalmol* 2026, PMID 41884918 (#165) – Grade A (pilot, UK).
- Use in pitch: voice-first for older Indians is justified by literacy and vision data (F-INDLOC-3), not by a voice trial. Say "voice-first because 3 in 4 older women can't read", and accept WhatsApp voice notes.
- Caveat: absence of evidence. Don't claim "proven that elderly Indians prefer voice".

## JUDGE – round 5 additions (J26–J31)
| # | Question | Short answer | Evidence |
|---|---|---|---|
| J26 | "Is an incentive spirometer even a regulated device in India?" | "Yes, at the lowest level. CDSCO lists it as Class A, non-sterile and non-measuring, and says it isn't a diagnostic. Because our clip-on measures and alerts, we expect to need our own registration and licence, probably Class A measuring or Class B. We'll apply before selling." | F-REG-5, F-REG-4 |
| J27 | "Will you cut readmissions?" | "We don't claim that yet. Worldwide, about 1 in 8 bypass patients is readmitted within a month, and lung problems are one of the main causes. Our pilot would measure it. For knee replacement, readmissions are already low, so there we help recovery, not readmissions." | F-BIZ-8 |
| J28 | "Amrita already has an AI chatbot for bypass patients. Why you?" | "It shows hospitals want this. Smart CABGuard watches the heart and needs a smartphone. We check the breathing exercise and work by voice for patients without one. We'd plug in alongside it." | F-COMP-12 |
| J29 | "Does putting the family on WhatsApp actually help?" | "An Indian pilot at a Tata Memorial unit supported caregivers via WhatsApp. Unplanned follow-up visits halved and family stress fell. And two in three older Indians live with their children." | F-ADH-7, F-INDLOC-3 |
| J30 | "Digital reminders for TB barely worked. Why would yours?" | "Right: on average they help only modestly. Two differences: our sensor records each breath, so there's no self-reporting, and digital follow-up reliably brings problems to the nurse earlier, which is what our alerts do." | F-ADH-8, F-ADH-1 |
| J31 | "How big can this get?" | "Surgery first. Then TB survivors: about 23 lakh people finish TB treatment each year, and in one Tamil Nadu district 59% of them still had impaired lungs. That's our rough estimate, but it's lakhs of people a year." | F-VIS-4, F-VIS-2 |

# Round 6 additions (10 Oct 2026)

## BIZ (round 6)

### F-BIZ-10: Indian readmission numbers after major abdominal surgery are found, and they are modest: 4.7% within 30 days after major GI cancer surgery (30 centres) and about 5% after Whipple surgery. Still no Indian 30-day figure after CABG
- Detail: **I-INFUSE** (Tata Memorial–led, 810 patients, 30 Indian cancer centres, 3 months, CTRI-registered): 30-day readmission 38/810 = **4.7%**; serious complications (Clavien-Dindo grade 3 or higher) 7.9%; mean stay 9.3 days. Causes of readmission not reported. **SGPGIMS Lucknow**, 997 Whipple (pancreaticoduodenectomy) patients 1989–2021: 10.3% ever readmitted; 53 of 997 (about **5.3%**) within 30 days, half of those within 7 days; top cause intra-abdominal fluid collection, not the lungs. **CMC Vellore**, 1,711 cardiac-surgery patients: 3.1% had to go back to the ICU before discharge; **lung complications after surgery were an independent risk factor**; those patients stayed 17.6 vs 7.6 days and 7.4% died (vs 1.4% overall).
- Source: *Indian J Anaesth* 2026, PMID 41788757 (ledger #170) – Grade A. *Cureus* 2024, PMID 39176340 (#168) – Grade A (single centre, 32 years of data). *Ann Card Anaesth* 2024, PMID 39365131 (#169) – Grade A (single centre; ICU readmission, not 30-day hospital readmission).
- Use in pitch: honest Indian anchor: "in 30 Indian cancer centres, about 1 in 20 major abdominal-surgery patients was back within a month". The CMC data supports "a lung complication after heart surgery is linked to going back to ICU, and those patients stay more than twice as long".
- Caveat: none of these names lung problems as a cause of 30-day readmission. An Indian 30-day readmission rate after CABG is **still not found** (searched in rounds 5 and 6). The lower Indian figures may partly reflect patients readmitted at other hospitals and not counted.

### F-BIZ-11 (weak): Apollo HomeCare sells home physiotherapy packages (7, 14 and 30 days) and a "Chest Physiotherapy" package, but publishes no prices
- Detail: Apollo's page lists the packages with "Enquire Now" only. An unnamed Delhi aggregator page (snippet, not opened) claims ₹700–2,000 per home visit.
- Source: Apollo HomeCare (ledger #178) – Grade B (that the packages exist); snippet (#179) – Grade C (price).
- Use in pitch: a big Indian chain already sells **chest physiotherapy at home**, so there is a paying market for home breathing care. Keep the price as "roughly ₹500–2,000 a visit (approximate)".
- Caveat: still no official published rupee price from Portea, Apollo or Max@Home (searched in rounds 4, 5 and 6). Stop searching the web; get a phone quote if a number is needed.

## ADH (round 6)

### F-ADH-9: Home breathing rehab by phone works in rural India: in the Thar Desert, 76% of older COPD patients were still exercising after 8 weeks of Hindi video rehab sent over social media, and 58% a year later
- Detail: Jodhpur, 45 COPD patients (mean age 64, 87% men), Hindi rehab videos sent to smartphones via social media for 8 weeks. Usability score 81.5/100; breathlessness, quality of life and walking test improved. 75.5% exercising at 8 weeks, 58% at 1 year; the authors call it feasible "even in low-literacy populations". A second rural study (peer-led community rehab, 30 patients, median age 57.5): 70% attended at least 12 of 16 sessions; walking distance rose from 263 to 320 m.
- Source: *Lung India* 2025, PMID 40296389 (ledger #171) – Grade A (feasibility, no control group). *J Glob Health* 2025, PMID 40340958 (#172) – Grade A (feasibility).
- Use in pitch: older, rural, low-literacy Indians do keep up home breathing exercise when guided by phone in Hindi. Supports the voice + WhatsApp design.
- Caveat: COPD rehab, not incentive spirometry after surgery; adherence self-reported; small. **We still have no Indian data on incentive-spirometer use after discharge.** CTRI can't be keyword-searched from here, and Europe PMC finds no CTRI-registered incentive-spirometer trial (0 hits).

## INDLOC / VOICE (round 6)

### F-INDLOC-6: India's government voice-call programme (Kilkari) reaches people only with retries: 50% answer the first call, 76% by the third, 99.5% by the ninth. Once answered, about half listen to most of the message
- Detail: Kilkari (MoHFW with BBC Media Action) sends recorded health calls to over 10 million subscribers, about 1.2 million calls a day. Of answered calls, 48% were heard for at least half their length and 43% for at least three-quarters. Its RCT (5,095 pregnant women, Madhya Pradesh) found 65% listened to at least half the content, but **no effect on the main outcome** (exclusive breastfeeding) and only small gains elsewhere (modern contraception up 3.7 points, immunisation up 2.8 points), largest among the poorest.
- Source: *BMJ Glob Health* 2021, PMID 34312148 (ledger #173) – Grade A. *BMJ Glob Health* 2022, PMID 35835477 (#174) – Grade A (RCT).
- Use in pitch: (1) design rule: retry a reminder call up to 3 times and send a WhatsApp backup; (2) honest framing: one-way voice messages alone change behaviour only a little, which is why we add a sensor, live feedback and a nurse.
- Caveat: young mothers, not older patients. mMitra was not checked this round.

### F-INDLOC-7: Most Indian homes have a mobile phone (87% of households), but 29% of people aged 60+ have difficulty making a phone call: 35% of older women and 38% of those who never went to school
- Detail: LASI Wave 1 (2017–18), India Report: the mobile phone is the most common household durable, 87% of households (94% urban, 84% rural). Table 11.9, aged 60+ (n = 31,336): difficulty "making telephone calls" 28.6% overall; rural 32.8%, urban 18.2%; men 21.5%, women 34.8%; no schooling 37.7%; widowed 38.0%; living alone 35.4%.
- Source: LASI Wave 1 India Report 2020, IIPS / MoHFW (ledger #175) – Grade A. (The household figure is quoted from the report text, because the table layout came out garbled in the PDF text.)
- Use in pitch: "the phone is in the house, but 1 in 3 older women struggles to use it". So the patient only has to answer or listen, never dial or type; the family member gets the WhatsApp.
- Caveat: 2017–18 data; household ownership, not personal ownership. This report gives no personal mobile-phone ownership figure for 60+.

## VIS (round 6)

### F-VIS-5: India's 2024 RBIPMT guidance for TB pulmonary rehabilitation explicitly lists the incentive spirometer as one of the breathing exercises
- Detail: "Guidance Document on Pulmonary Rehabilitation for People affected with Tuberculosis", Rajan Babu Institute of Pulmonary Medicine and TB (RBIPMT), Delhi, July 2024, published on the national TB portal ntep.in (marked "Draft" and "live document"). Breathing exercises listed: pursed-lip breathing, deep diaphragmatic breathing, **incentive spirometer**, postural drainage positions, huffing/coughing. Programme: 6–12 weeks, 3 supervised sessions a week, groups of 5, at DR-TB centres; in-patients may come back after discharge to complete 3 months. The essential equipment list includes a spirometer; an inspiratory muscle trainer is "desirable".
- Source: RBIPMT / NTEP, ntep.in/node/6610 (ledger #176) – Grade A (official guidance, draft).
- Use in pitch: answers "does any Indian TB guidance use your device?" Yes: incentive spirometry is in India's own post-TB rehab guidance. Strengthens the TB-survivor roadmap (F-VIS-2, F-VIS-4).
- Caveat: a draft from one institute, written for **supervised centre sessions**, not home use. It gives no incentive-spirometer dose.

### F-VIS-6: WHO says India's share of extrapulmonary TB is above 20%, so under 80% of notified TB is in the lungs
- Detail: WHO Global TB Report 2025: worldwide, 84% of new and recurrent notified cases were pulmonary and 16% extrapulmonary (2024); South-East Asia Region 25% extrapulmonary; India is named among countries with a "particularly high (>20%)" extrapulmonary share. The exact India split is not on this page.
- Source: WHO Global TB Report 2025, section 2.1 (ledger #177) – Grade A.
- Use in pitch: tightens the post-TB estimate in F-VIS-4. **Team estimate (not a source):** about 26 lakh notified × under 80% pulmonary × 90% success ≈ fewer than about 19 lakh people a year finishing treatment for lung TB. Still "lakhs of people a year".
- Caveat: the exact Indian pulmonary percentage needs the India TB Report table (the PDF was not found by search).

## JUDGE – round 6 additions (J32–J35)
| # | Question | Short answer | Evidence |
|---|---|---|---|
| J32 | "What's the readmission rate in India?" | "In 30 Indian cancer centres, about 1 in 20 major abdominal-surgery patients was back within a month (4.7%). For bypass we found no Indian number; worldwide it's about 1 in 8. We'd measure it in our pilot." | F-BIZ-10, F-BIZ-8 |
| J33 | "Will older people even pick up a phone call?" | "The government's Kilkari service shows half pick up on the first try and three in four by the third. And 29% of over-60s find making a call hard. So we retry, the patient only has to listen, and the family gets WhatsApp." | F-INDLOC-6, F-INDLOC-7 |
| J34 | "Is incentive spirometry used for TB survivors in India?" | "Yes. The 2024 RBIPMT pulmonary-rehab guidance on the national TB portal lists the incentive spirometer among the breathing exercises." | F-VIS-5 |
| J35 | "Do older rural patients keep up home exercise?" | "In the Thar Desert, 76% of older COPD patients were still exercising after 8 weeks of phone-guided Hindi rehab, and 58% after a year." | F-ADH-9 |

# Round 7 additions (10 Oct 2026)

## REG (round 7)

### F-REG-6: India's device law classes an accessory on its own, not by the device it clips onto. A battery-powered device that supplies monitoring information is an "active diagnostic medical device", which is Class B if it monitors a vital body process, and Class A only if no such rule applies
- Detail (read in the primary text, Medical Devices Rules 2017, consolidated CDSCO copy, First Schedule Part I):
  - **Basic principle (ii):** if devices are used together, each is classified separately; "Accessories are classified in their own right". **Principle (iii):** software that drives or influences a device falls in that device's class.
  - **Rule 2(c):** an "active diagnostic medical device" is any active device that supplies information for detecting, diagnosing or **monitoring** a physiological condition or state of health. **Rule 2(d):** "active" means it runs on electricity or another energy source other than the body or gravity.
  - **Para (xiii)(a)(3):** an active diagnostic device is **Class B** if it is for direct diagnosis or **monitoring of vital physiological processes**. **(xiii)(c)(1):** **Class C** if it monitors vital parameters where a change could put the patient in immediate danger (the rule names respiration as an example).
  - **Para (xiv):** any other active device not covered by (xii) or (xiii) is **Class A**.
  - Romsons' registration status: two more searches (CDSCO, GeM) found nothing (gap remains; needs a person).
- **Team reading (not a ruling):** SpiroBuddy's clip-on is battery-powered, measures inhaled volume and alerts a nurse, so it is very likely an active diagnostic device. If CDSCO sees breathing-exercise volume as "monitoring a vital physiological process", it is **Class B**; if it is seen as exercise tracking only, it could fall to **Class A** under (xiv). It should **not** be Class C, as long as we never claim real-time danger monitoring. This matches F-REG-2 (CDSCO lists "monitoring spirometer" as Class B) and F-REG-4 (software that alerts about a condition is not wellness).
- Source: Medical Devices Rules 2017 (consolidated, 211 pages), CDSCO – https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2022/m_device/Medical%20Devices%20Rules%2C%202017.pdf (ledger #183) – Grade A (primary law).
- Use in pitch: J36 below. Shows the team knows the exact rule and has planned for it.
- Caveat: our own reading of the rules; CDSCO decides. Avoid words like "real-time monitoring", "detects deterioration" or "prevents pneumonia" in product claims, which push the class up.

## VIS (round 7)

### F-VIS-7: India's exact TB split from WHO's official notification data: in 2024, 26% of new and relapse TB cases notified in India were outside the lungs, so about 74% (about 18.5 lakh people) had lung TB
- Detail: WHO notification dataset, India, 2024: new + relapse cases 24,98,584. Pulmonary (lab-confirmed + clinically diagnosed, new + relapse) 18,49,397; extrapulmonary (new + relapse) 6,49,187 = **26.0%**. Extrapulmonary share by year: 2019 22.2%, 2020 29.2%, 2021 24.5%, 2022 24.8%, 2023 24.7%, 2024 26.0%. Pulmonary lab-confirmed new cases 2024: 10,90,789.
- **Team estimate (not a source):** about 18.5 lakh lung-TB cases × 90% treatment success (F-VIS-4) ≈ **about 16–17 lakh people a year finish treatment for lung TB**. If roughly half have lasting lung impairment (Madurai 59%), that is several lakh people a year who could use breathing rehab.
- Source: WHO Global TB Programme notifications dataset (CSV), https://extranet.who.int/tme/generateCSV.asp?ds=notifications (ledger #187) – Grade A (official data reported by India to WHO). Consistent with F-VIS-6 (WHO says India's extrapulmonary share is ">20%").
- Use in pitch: replaces the "under 80%" guess in F-VIS-6 with a real number: "about 3 in 4 TB patients in India have it in the lungs, about 18 lakh a year".
- Caveat: the 24.99 lakh (new + relapse) is lower than PIB's 26.07 lakh total notified (PIB counts all notified, incl. other retreatment). We computed the split ourselves from WHO's columns; the India TB Report table itself was not found (single source).

## INDLOC / VOICE (round 7)

### F-INDLOC-8: Among people aged 45+ at Telangana health centres, only about 1 in 5 rural and 1 in 3 urban had a smartphone; only 20% had good digital health literacy
- Detail: 318 adults aged 45 or over visiting rural and urban primary health centres, Hyderabad area, March 2023. Smartphones: urban 36.5%, rural 19.5%. Basic ("standard analogue") phones: urban 45.9%, rural 38.4%. Good eHealth literacy: 20.4% (rural 20.1%, urban 20.8%). Owning a mobile phone, education and recent computer use predicted better digital literacy.
- Source: *Med J Armed Forces India* 2024, PMID 38799990, doi 10.1016/j.mjafi.2023.09.006 (ledger #184) – Grade A (single district, clinic sample).
- Use in pitch: "Among older patients at Telangana health centres, only 1 in 5 rural patients had a smartphone." Supports a design where the patient needs no smartphone (voice call + clip-on), and the family member gets the WhatsApp.
- Caveat: ages 45+, not 60+; one region; clinic attenders. Still **no national personal-ownership figure for 60+** (NSS 78th round tables not reachable by search). DAHLIA (rural Karnataka, #179 snippet) found 50% own any mobile phone.

### F-INDLOC-9: In India's Kilkari voice programme, about 23% of women were never reached even after 9 call attempts over 4 days; morning slots had the best pickup; listening dipped around festivals, and listening (not just pickup) is the better success measure
- Detail: ARMMAN / Google Research analysis of Kilkari call logs (arXiv preprint, Nov 2023). Each message gets up to 9 attempts over 4 days. "Engagement" = listening for more than 30 seconds of a roughly 90-second message. Beneficiaries were grouped by pickup and engagement; some picked up often but listened little (a family member may answer). One low-pickup group had only about 20% technically successful calls (network failures). After 6 weeks with no listening, people are dropped. Listening fell around New Year, likely around major festivals too. Kilkari has reached over 3 crore women, 30 lakh active.
- Source: "Analyzing and Predicting Low-Listenership Trends in a Large-Scale Mobile Health Program", arXiv 2311.07139, 2023 (ledger #186) – Grade B (preprint, not peer-reviewed).
- Use in pitch / build: design rules for our reminder calls: retry at different times, prefer morning slots, count a call as done only if the patient listened (or breathed into the device), not just if someone picked up, and pause or soften reminders on festival days.
- Caveat: young mothers, not older patients. Conflicts with F-INDLOC-6's "99.5% reached by the 9th call" (different cohort and measure; see Contradictions 36). mMitra-specific data not found.

## BIZ (round 7) – null result

### F-BIZ-12 (null): Three rounds of searching found no published Indian 30-day hospital readmission rate after CABG
- Detail: Round 7 checked a 618-patient CABG cohort (septuagenarians), the COHOS hybrid-vs-CABG study (Indian Heart J 2025; readmission given only as a hazard ratio over 3.6 years), an Amrita off-pump CABG cohort (2014–19; mortality only; notes that off-pump is "the default" in India) and a journal-filtered search of the three main Indian cardiac journals. None reports a 30-day readmission rate. Indian cohorts usually report in-hospital and mid-term mortality, not readmission.
- Source: ledger #180, #181, #188, #189 – Grade A (papers), null result.
- Use in pitch: if asked, say "Indian bypass centres don't publish 30-day readmission rates; that gap is itself a reason for remote follow-up. Our pilot would measure it." Use the global 12.9% (F-BIZ-8) as the reference.
- Caveat: absence of published evidence, not proof that the rate is low.

## JUDGE – round 7 additions (J36–J38)
| # | Question | Short answer | Evidence |
|---|---|---|---|
| J36 | "Isn't your clip-on just an accessory to a Class A device?" | "No. Indian law classes an accessory on its own. Because ours is battery-powered and gives monitoring information, we expect Class B, and we'll confirm with CDSCO before selling. The demo is a prototype, not a medical device on sale." | F-REG-6, F-REG-5 |
| J37 | "How many TB survivors are we talking about?" | "In 2024 India notified about 18.5 lakh lung-TB cases (74% of new and relapse cases, WHO data). With 90% treated successfully, that's roughly 16–17 lakh people a year finishing treatment; studies find about half still have weak lungs." | F-VIS-7, F-VIS-4 |
| J38 | "What's the 30-day readmission rate after bypass in India?" | "Indian centres don't publish it; we searched three rounds. Worldwide it's about 1 in 8. Measuring it is part of our pilot." | F-BIZ-12, F-BIZ-8 |

## Round 8 additions – Is sending health updates on WhatsApp allowed? (10 Oct 2026)

Context: family updates may go through WaBI (the team's own Indian WhatsApp Business platform, Coyot AI) or straight through Meta's WhatsApp Cloud API. Both follow the same Meta rules below. Sources are Meta's own policy and developer pages (grade B under our rubric because they are a company's official pages, but they are *the* rules for WhatsApp).

### F-COMMS-14: WhatsApp's Business Messaging Policy does not ban health messages. It bans them only where local law requires "heightened" systems for health data. It also requires opt-in, honouring opt-outs, and no sensitive ID numbers in chats
- Detail (read 10 Oct 2026; the page shows no date; Meta's opt-in page says the policy was updated in Nov 2024):
  - Section 3 (Protect data): "Don't use WhatsApp for telemedicine or to send or request any health related information" – but only **if** applicable regulations forbid sending such information to systems that don't meet heightened requirements for health data. So the test is local law, not a blanket ban.
  - Section 3 also: the business must secure all notices and consents, keep a **published privacy policy**, and must not ask people to share **personal ID card numbers** or other sensitive identifiers (so: never ask for Aadhaar or ABHA numbers in the chat).
  - Section 2: you may contact someone only if (a) they gave you their number and (b) you got **opt-in permission** to receive messages from you. Business-started chats must use an **approved Message Template**. Free-form replies are allowed only inside the **24-hour customer service window**, which restarts each time the user writes.
  - Section 1: you must honour every request to stop or opt out, made on or off WhatsApp.
  - Section 4: "Medical and healthcare products" (and prescription drugs) are restricted for **buying, selling or promoting**. That is about commerce, not care updates. SpiroBuddy's messages sell nothing.
  - Regulated verticals can't be messaged about on the free WhatsApp Business **App**; we use the Business **Platform** (API) anyway.
- Source: WhatsApp Business Messaging Policy – https://business.whatsapp.com/policy (ledger #207) – Grade B (Meta's official policy; primary for Meta's own rules).
- Use in pitch: J-WA below.
- Caveat: we did not open the separate Meta Commerce Policy (we use no catalogue or payments, so it should not apply). Meta can change the policy without notice.

### F-COMMS-15: A patient's own care update should fit Meta's "utility" category if it is plain and non-promotional. Meta gives no health-specific template rule; if it judges a utility template to be marketing, it now approves it as marketing (about 7× the price)
- Detail:
  - **Utility** needs both: (1) **non-promotional**, and (2) either **specific to or requested by the user** (their order, account, services) **or essential/critical** to the user (e.g. safety).
  - Utility examples include **"Account Alerts or Updates"** (time-sensitive updates about a service the user signed up for, with no upselling or renewals) and opt-in confirmation messages. Health appears only in public-service examples (a vaccine-drive notice, a health emergency).
  - **Team reading (not a Meta ruling):** "Today Amma did 6 of 10 breathing sessions; best 1,500 mL. Reply STOP to end updates." is specific to a service the family opted into, so it should be utility. Words like "upgrade", "offer" or "book a home visit" would make it marketing.
  - Since **9 April 2025**, a template filed as utility that Meta thinks is marketing is **approved as marketing**; a review can be requested within 60 days. Businesses that abuse categories lose utility templates for **7 days (30 days if repeated)**, and since 16 April 2025 without the usual 1-day notice.
  - Templates mixing utility and marketing count as marketing. Meta says its examples are only illustrative.
  - We found **no health-specific review rule** for templates in Meta's docs.
- Source: Template categorization – https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization.md (ledger #209) – Grade B. Prices: F-COMMS-2 (#61, #62).
- Use in build: keep each family template short and factual, one purpose each, no links to buy anything; a separate opt-in confirmation template.
- Caveat: Meta categorises each template case by case; the final category is only known after submission.

### F-COMMS-16: Opt-in can be collected on paper, in person, by IVR call, SMS or a website; it must name the business and say clearly that the person is opting in
- Detail: Meta's opt-in page (citing the Nov 2024 policy update) says opt-in can be general rather than WhatsApp-specific, as long as local law is followed. Requirements: state clearly that the person is opting in, give the **business's name**, comply with law. Supported methods include **in person or on paper**, an IVR phone flow, SMS and a website. Tips: separate opt-in per message category, clear opt-out, watch the quality rating.
- Source: Get opt-in for WhatsApp – https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in.md (ledger #213) – Grade B.
- Use in build: at discharge the nurse records the patient's consent to share (the patient picks the family number); then the **family member** gets a utility "confirm you want updates from <Hospital> about <patient first name>" message and replies YES. That covers Meta's opt-in (family member) and DPDP consent (patient, F-REG-3).
- Caveat: the opt-in must name the sender actually shown on WhatsApp (the hospital's verified business, or SpiroBuddy's). Decide whose name the number carries.

### F-REG-7: On Cloud API, Meta acts as a data processor for the business, keeps message content at most 30 days (encrypted at rest), doesn't use it for ads automatically, and can keep message data at rest **in India** ("IN") if the number is registered with local storage
- Detail:
  - Meta "acts as a data processor/service provider on behalf of the business" where the law uses those terms, and uses messages only on the business's instructions.
  - Message content: **maximum 30 days** retention (for retries etc.), **encrypted at rest**. User identifiers are deleted within 30 days of a message's last status update.
  - Cloud API **decrypts** incoming messages and forwards them to the business (it manages the keys for the business). So messages are encrypted in transit, but Meta's servers see the content; don't call it end-to-end between family and hospital.
  - Not used automatically to target ads.
  - Default: processed in Meta data centres worldwide. **Local storage** option: per phone number, set at registration (`data_localization_region`). The supported list includes **India (IN)** (also AU, ID, JP, SG, KR, DE, CH, GB, BR, BH, ZA, AE, CA). Meta names **healthcare** as a typical reason to use it.
  - With local storage on Cloud API, content may sit in Meta data centres abroad for **up to 60 minutes** while being processed ("data-in-use"), then is deleted outside the chosen country and kept only inside it. Turning it on for an already-registered number means deregister + re-register (usually under 5 minutes, no re-verification).
  - Meta says Cloud API customers must meet their own data-protection obligations; sub-processors are listed in the WhatsApp Business Data Processing Terms / Meta Hosting Terms for Cloud API (not opened).
- **DPDP mapping (team reading, not legal advice):** hospital = data fiduciary; SpiroBuddy/WaBI = data processor under a written contract; Meta = sub-processor. DPDP Act s. 16 lets the government restrict transfers to named countries (#196, not opened this round); we did not check whether any such list has been notified (gap).
- Source: Data Privacy & Security (#210), Local storage (#211), Registration API (#212) – developers.facebook.com – Grade B.
- Use in pitch / architecture: "For real hospitals we register the number with India local storage, so message content rests in India; our own database is in Mumbai."
- Caveat: "data never leaves India" would be false (up to 60 minutes of processing abroad; contact-book data is outside local storage). Whether WaBI's number setup supports `data_localization_region` must be checked in WaBI.

### F-REG-8: We found no Indian rule that forbids health updates over WhatsApp. India's 2020 Telemedicine Practice Guidelines reportedly list WhatsApp as an allowed text tool; the DPDP Act treats health data like other personal data and asks for consent, notice and security
- Detail:
  - **Telemedicine Practice Guidelines 2020** (Board of Governors in supersession of MCI, with NITI Aayog, March 2020): several summaries quote the guidelines as listing "Chat Platforms like WhatsApp, Facebook Messenger" among tools a doctor may use, with the same core principles whatever the tool. **We could not open the primary PDF** (government copies blocked or broken: #214–#217), so this rests on secondary summaries only (#218). The guidelines govern doctors' consultations; SpiroBuddy's family updates are not consultations and give no advice or prescriptions.
  - **DPDP Act 2023 / Rules 2025:** no special "health data" category (F-REG-3); needs a plain notice, consent that can be withdrawn as easily as given, reasonable security, and breach reports (72 hours to the Board). Most duties start about **May 2027**.
  - **IT Act SPDI Rules 2011** treat health information as "sensitive personal data" needing written consent. Our understanding is that the DPDP Act removes IT Act s. 43A (the basis of the SPDI Rules) once its provisions take effect; **not verified from primary text this round (?)**. Until then, get written (digital) consent from the patient, which we do anyway.
  - Meta's health clause (F-COMMS-14) only applies if Indian law requires "heightened" systems for health data. We found no such Indian rule.
- Source: TPG summaries (#218, grade C as read); DPDP Rules (#122, A); DPDP Act (#196, A, not opened); F-REG-3.
- Use in pitch: J-WA.
- Caveat: absence of a ban is not a licence. A hospital's own IT policy or a state rule may be stricter; a lawyer should confirm before the first real patient.

### F-INDLOC-10: Indian government precedent: the MyGov Corona Helpdesk ran on WhatsApp from March 2020, reached about 4.1 crore users, and from August 2021 let people download vaccine certificates (about 32 lakh in the first weeks) and book vaccine slots
- Detail: WhatsApp number +91 90131 51515; certificate download via OTP (Aug 2021), slot booking (24 Aug 2021); tech partners Haptik and Turn.io. Shows the Government of India itself sent personal health documents (vaccination certificates) over the WhatsApp Business Platform.
- Source: news reports, Aug 2021 (Business Today, The Tribune, ETV Bharat, BusinessWorld) – search snippets only (#218) – Grade B (several major outlets agree; pages not opened).
- Use in pitch: one line in J-WA.
- Caveat: 2021, a public-health emergency; current status not checked. **No Indian hospital example (Apollo, AIIMS) was verified this round** (gap).

### Risks found (round 8)
- **R-WA-1: Two consents, not one.** The family member must opt in on WhatsApp (Meta), and the patient must consent to their data being shared with that family member (DPDP). Never message a family number on the nurse's word alone.
- **R-WA-2: Template drift to marketing.** One promotional phrase can turn a utility template into marketing (≈7× the price) or, if repeated, cost all utility templates for 7–30 days.
- **R-WA-3: "End-to-end encrypted" is not accurate for Cloud API.** Meta decrypts on our behalf. Say "encrypted in transit and at rest".
- **R-WA-4: Free-form AI replies only inside 24 hours.** Outside the window, only approved templates. The AI-written evening summary must go into an approved template's variables, not be sent as free text.
- **R-WA-5: Don't collect IDs in chat.** No Aadhaar or ABHA numbers over WhatsApp (policy section 3).

## JUDGE – round 8 addition (J-WA)
| # | Question | Short answer | Evidence |
|---|---|---|---|
| J-WA | "How is sending health updates on WhatsApp allowed?" | "WhatsApp's business rules allow health messages unless local law demands special health-data systems, and we found no Indian rule that does; the Government's own MyGov helpdesk sent vaccine certificates on WhatsApp. We only message a family member who has opted in, after the patient has consented, using Meta-approved, non-promotional 'utility' templates, and anyone can reply STOP. The messages are progress updates, never a diagnosis, and any worrying reply goes to a nurse. For real hospitals, Meta acts as our data processor, deletes message content within 30 days, and can keep it stored in India." | F-COMMS-14, F-COMMS-15, F-COMMS-16, F-REG-7, F-REG-8, F-INDLOC-10 |

## Open gaps (after round 8, WhatsApp only; the round 7 list still stands)
1. Primary text of the Telemedicine Practice Guidelines 2020 (all government PDF copies blocked this round). Needs a person to download it in a browser.
2. An Indian **hospital** (Apollo, AIIMS, Narayana, a state health department) using the WhatsApp Business API for patient or family updates, from an official page.
3. DPDP Act s. 44 / IT Act s. 43A status, and whether any s. 16 restricted-country list has been notified (open the Act text, #196).
4. Whether WaBI supports `data_localization_region: IN` when registering numbers, and whose business name the sender shows.
5. Meta Commerce Policy and WhatsApp Business Data Processing Terms (sub-processor list) – not opened; low priority.

## Round 9 – WaBI vs Meta Cloud API (10 Oct 2026)

**Privacy note:** this repo is public. Part of this round used the team's own private WaBI material. Only the conclusions are kept here; request formats, internal prices and hosting details were removed on purpose. Ask the WaBI team for the developer guide.

**Short answer:** yes, our server can send WhatsApp messages through WaBI by itself with an API key. WaBI is Coyot AI's own product and it *is* Meta's Cloud API underneath, so "WaBI or Meta direct" is really "use the layer we already built, or write that layer again inside SpiroBuddy". For the demo, keep the Twilio sandbox that is already coded. For the pilot, use WaBI with the hospital's own WhatsApp number, after the fixes listed below.

**Which WaBI? (identification: high confidence)** WaBI = **Coyot WaBI**, made by **Coyot AI** (coyot.ai). The coyot.ai home page calls it "an existing Coyot AI product". It is not one of the well-known Indian providers (Wati, Interakt, Gupshup, AiSensy) and web search finds nothing about it. An unrelated iPhone app also called "Wabi" is **not** this product.

**Evidence labels:** **[INTERNAL]** = the team's own private WaBI documents and code (not public). **[MARKETING]** = a public marketing or legal page. **[DOCS, Meta]** = developers.facebook.com. **[NOT CONFIRMED]** = could not confirm. **Nothing was test-sent this round.**

### F-COMMS-17: WaBI has a real server API: an API key, a call to send a template, a call to send a free-form reply, and signed webhooks for incoming replies
- Detail **[INTERNAL]**: keys are created by an owner or admin inside WaBI's settings. A server can send an approved template (business-started message) or a free-form text (only inside WhatsApp's 24-hour window, and only if that person has already messaged us), and can check a send. Incoming replies, delivery status and opt-outs arrive at our server as signed webhooks. Sends are once-only (a repeat does not send twice) and an opted-out contact is never sent a template.
- Detail **[MARKETING, coyot.ai + WaBI terms/privacy pages]**: described only as a dashboard (bulk campaigns, shared team inbox, contacts, delivery/read insights). It connects to Meta's Cloud API as a registered Tech Provider, the customer connects their own WhatsApp Business Account, and **Meta bills the customer directly** for messages. The public pages do not mention the API.
- Source: ledger #219, #221, #222 – Grade B (company's own material, not a published spec).
- Use in build: a WaBI sender would sit beside the Twilio one in `backend/app/whatsapp.py`; replies ("STOP", "status", 1/2/3) would arrive on a new webhook route.
- Caveat – limits that matter for SpiroBuddy **[INTERNAL]**:
  - Only **text** and **templates without a media header**. No image (the weekly progress card), no voice note, no free-form buttons.
  - A person who types **STOP** is opted out inside WaBI. Our own consent record must be updated from the opt-out event too.
  - Hosting is **not in India yet**, and India local storage of message data is **[NOT CONFIRMED]**.

### F-COMMS-18: WaBI onboarding and price: the slow parts are Meta's (business verification, payment method, display name, template review), not WaBI's
- Detail **[INTERNAL]**: connecting a new number needs a phone number not already on WhatsApp, a Meta Business Portfolio, Meta **business verification** (days, not hours), a payment method on the WhatsApp account and a display name Meta accepts. Coyot AI's own number is already connected and verified.
- **Per-message price:** WaBI adds none. Meta charges the WhatsApp account directly (utility template in India ₹0.115, F-COMMS-2). WaBI's own subscription price is not published.
- Detail **[NOT CONFIRMED]**: any sandbox or test number inside WaBI; public pricing; uptime promise.
- Source: #221, #222 – Grade B.

### F-COMMS-19: Meta's Cloud API used directly: free test number at once, one REST call to send, webhooks for replies, templates reviewed within about 24 hours
- Detail **[DOCS, Meta]**:
  - Getting started needs only a Facebook account and developer registration. Creating the app gives a **test business phone number automatically** and a **temporary access token**; you add a "To" number and send.
  - **Send (templates and free-form use the same call):** `POST https://graph.facebook.com/v25.0/<PHONE_NUMBER_ID>/messages` with header `Authorization: Bearer <token>` and `"messaging_product": "whatsapp"`.
  - **Free-form messages** only within 24 hours of the user's last message; otherwise an approved template.
  - **Replies and delivery status** arrive as webhooks (JSON) on our URL; needs the `whatsapp_business_messaging` permission.
  - **Long-lived token** for a server: a System User token (if we send only from our own account). Sending from **another** business's account (a hospital's) needs a Tech Provider's "business token", which means Meta business verification + App Review.
  - **Template review:** "can take up to 24 hours"; appeal decisions also within 24 hours.
- Detail **[NOT CONFIRMED in the pages read]**: the commonly quoted limit of 5 recipient numbers on the test number; how long the temporary token lasts; Meta's own stated time for business verification.
- Source: Meta for Developers – get-started (#224), send-messages (#225), webhooks overview (#226), template review (#227), Become a Tech Provider (#228), phone numbers (#229), access tokens (#230) – Grade B. Price: F-COMMS-2.
- Caveat: none of this is written in SpiroBuddy yet. It would be a new sender, a new webhook reader, token handling and a consent/opt-out layer, which is what WaBI already has.

### Comparison (for the build decision)

| | **WaBI** (Coyot AI's own) | **Meta Cloud API direct** | **Twilio WhatsApp sandbox** (already coded) |
|---|---|---|---|
| Server can send with a key? | Yes [INTERNAL] | Yes: Bearer token [DOCS] | Yes: account SID + token (COMMS.md §4, F-COMMS-6) |
| Send template / free-form | Both; text only, no images or voice notes | Both; all message types | Free-form in the sandbox; Twilio's own templates only |
| Replies ("STOP", "status") | Signed webhook | Webhook from Meta | Webhook, already wired (`/api/comms/webhooks/whatsapp`) |
| Sender the family sees | Indian number, "Coyot AI" today; the hospital's name once the hospital connects its own number | Meta test number for a demo; own number later | Twilio's shared US number |
| Work left in SpiroBuddy | New sender + new webhook route (small) | New sender, webhook, tokens, consent layer (larger) | **None** |
| Ready for a demo in a few hours? | **Probably**, with a small adapter. Untested. | **Possible** with the test number, but more new code on demo eve | **Yes, about 15 minutes**; each phone must send the join code, again on demo morning (expires after 3 days) |
| Right for a hospital pilot? | **Yes, with fixes** (below) | Yes, but we would rebuild what WaBI has | **No** (sandbox, shared foreign number, no own templates) |
| Cost | Meta's fee only (utility ₹0.115) | Meta's fee only | Meta's fee + Twilio $0.005 per message (F-COMMS-10) |

### Recommendation
- **Demo: keep the Twilio sandbox plus the built-in phone simulators.** It is the only path that needs no new code the night before. A WaBI adapter is a nice extra only if a real test send works first.
- **Pilot: WaBI, with the hospital's own verified WhatsApp number,** so families see the hospital's name. It is Meta's Cloud API anyway (same price, same rules, F-COMMS-14 to 16, F-REG-7); consent, STOP handling, send-once safety and signed webhooks already exist; the team controls the code. **Before the first real patient:** (1) host WaBI in India; (2) register pilot numbers with India local storage (F-REG-7); (3) add image / voice-note / button sends if the pilot needs the progress card.
- If WaBI cannot meet (1) and (2) in time, fall back to Meta Cloud API direct on the hospital's own account.

### Risks found (round 9)
- **R-WA-6: Using Coyot AI's live number for patient-family messages.** Its existing chatbots may answer a family member's reply, the sender shows "Coyot AI" (not a hospital), and a family STOP opts that person out of Coyot AI's own messages. For a demo, use a separate number if one exists, or accept this knowingly.
- **R-WA-7: WaBI's API is documented only privately.** A future session without access must ask the WaBI team for the developer guide.
- **R-WA-8: Free-form messages need the person to write first.** Otherwise only an approved template works, and review can take up to 24 hours. Submit SpiroBuddy's utility templates early if WaBI will be shown live.

### Still uncertain (round 9)
1. A live end-to-end send through WaBI (nobody has tested it for SpiroBuddy).
2. Whether WaBI supports India local storage at number registration (open gap 4 from round 8: **still open**).
3. Whether a separate, bot-free number exists in WaBI for the demo.
4. Meta's recipient limit on test numbers and the temporary token's lifetime (not on the pages read).
