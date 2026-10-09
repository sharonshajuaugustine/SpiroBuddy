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

## Open gaps (priority order, after round 3)
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
