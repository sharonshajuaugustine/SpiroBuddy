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

## Contradictions & risks
1. Cochrane 2014 found no proof incentive spirometry works, and AARC advises against using it alone. Our answer: the trials never recorded adherence, and we measure it. **Never say "prevents pneumonia".**
2. Go-breath (Korea), an hourly alarm with a nurse dashboard, showed no significant effect. It is also prior art for our 8:00–21:00 schedule.
3. Prior art is crowded (InSee, SpiroTimer, Michigan, Airalux, Go-breath, a 1978 Bard device). Our edge: Indian devices, home use, Indian languages, WhatsApp and technique AI.
4. Many Indian patients get 3-ball flow devices, which our disc sensor can't read.
5. Twilio calls to India show a foreign caller ID, so elderly patients may not answer. A real product needs Indian telephony.
6. WhatsApp templates that sound promotional are billed as marketing (about 7x more).
7. The author of the 58% trial filed a patent on the reminder device.

## Open gaps (priority order)
1. INDIA: smartphone and WhatsApp use among people over 60 (TRAI, IAMAI, LASI); nurse-to-patient ratio; language census.
2. COMMS: TRAI TCCCPR rules for automated health calls; DLT registration for SMS; Twilio trial and WhatsApp sandbox limits; Twilio's India fees; Exotel/Plivo prices for an Indian caller ID.
3. VOICE: Saaras languages and latency; voice-agent per-minute price; Sarvam terms on health use; alternatives (Bhashini, AI4Bharat); voices that sound warm for elderly patients.
4. CLIN: a newer systematic review (2015+); Indian complication studies; the cost of complications in India.
5. COMP: Indian smart spirometers or patents; InSee's price.
6. Which spirometer type (volume vs 3-ball) Indian hospitals hand out most.
7. TECH, REG, BIZ, INDLOC, JUDGE: not started.
