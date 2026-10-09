# SpiroBuddy research knowledge base

Kept by the research agent; saved by the lead for round 1. Grades: **A** = peer-reviewed study, guideline or regulator data · **B** = reputable organisation, major news or company official page · **C** = retailer, blog or press release. Ledger numbers (#n) point to `SOURCES_LEDGER.md`. Last updated: 9 Oct 2026, round 1 (about 34 reads).

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

## Open gaps (priority order, after round 2)
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
