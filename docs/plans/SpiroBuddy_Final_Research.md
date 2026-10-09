# SpiroBuddy – Final Research Check

*Researched 9 October 2026. Every claim below links to its source. "Unverified" means we could not confirm it.*

---

## 1. Biggest finding: a clip-on smart spirometer already exists in the US

**InSee by Tidal Medical Technologies**
- A plastic box that **attaches to the base** of one specific US spirometer (Vyaire AirLife, 2500 and 4000 mL).
- Records breath attempts above 250 mL, successful attempts and the best volume, and **sends reminders**.
- **FDA history:** Emergency Use Authorization for COVID-19 patients (July 2021), then an FDA clearance letter dated **21 August 2025** (K241152, Class II).
- Approved for use **in hospitals only**, with one spirometer model only.
- The company's claimed accuracy is 97%, in its own press release (not independently checked).

**What this means:** we can't say "first clip-on smart spirometer". Using InSee as proof that the idea works makes the pitch stronger, not weaker.

**New positioning:**
> "In the US, InSee proved that a clip-on tracker works, and the FDA cleared it in 2025. But it fits one American spirometer, works only in hospitals and speaks only English. SpiroBuddy brings the same idea to India: it fits the Romsons spirometers Indian hospitals hand out, works **at home**, coaches in **10 Indian languages**, and updates families on **WhatsApp**."

| | InSee (US) | SpiroBuddy |
|---|---|---|
| Fits | One US model (AirLife) | Indian models (start with Romsons Breazer) |
| Where | Hospital only | Home, after discharge |
| Feedback | Counts attempts, reminders | Live AI voice coach + breath-quality AI |
| Language | English | Hindi, Tamil, Bengali and more |
| Family/nurse updates | Hospital system | WhatsApp |
| Regulatory | FDA-cleared | Prototype (hackathon) |

---

## 2. Claims from the other AI's report: checked

| Claim | Verdict | Notes |
|---|---|---|
| The 58% vs 28% study is Eltorai et al., *JAMA Surgery* 2019 | ✅ **True** | CABG (heart bypass) patients, one US hospital, 145 analysed. |
| The reminder also "cut atelectasis" (lung collapse) | ⚠️ **Only a small effect** | The X-ray lung-collapse scores differed by about 0.3 on a 10-point scale. Don't make it a headline. Say "improved adherence, with signs of fewer lung problems." |
| InSee holds an FDA EUA, not a 510(k) | ⚠️ **Out of date** | EUA in 2021, then a regular FDA clearance letter in August 2025. |
| InSee mounts at the bottom of the spirometer | ✅ **True** | Per the FDA letter. |
| Romsons Breazer costs ₹340–450 | ⚠️ **Roughly** | Online prices range from about ₹217 to ₹855; Medikabazaar lists ₹477. Say "under ₹500". |
| VL53L1X can narrow its view to 15° | ✅ **True** | Documented by ST (the chip maker). The VL53L0X is fixed at about 25°. |
| Shining the laser through clear plastic causes errors | ✅ **True** | ST calls this "crosstalk". Fix: no window (open slot), or a thin window very close to the sensor, kept clean. |
| Web Bluetooth avoids needing an app | ⚠️ **Not on iPhone** | Works in Chrome on Android and laptops. Safari on iPhone still doesn't support it, as far as we could find. |
| `emlearn` can put the model on the ESP32 | ✅ **True** | Converts a scikit-learn model to C code. The best-tested ESP32 route is emlearn-micropython. |
| Preventing one complication saves ₹50,000–2,50,000 | ❌ **No Indian source found** | Don't use this number. See section 3 for numbers that do have sources. |
| Reusable cap costs under ₹55 per patient | ❌ **Unsourced** | It's a calculation, not a fact. If you use it, show the maths. |
| CDSCO Class A device | ✅ **True for the plain spirometer** | The plain spirometer is CDSCO Class A (lowest risk, not diagnostic). Our measuring clip-on will need its own registration and licence. See section 6. |

---

## 3. Numbers you can safely put on slides

**Problem size (Indian studies)**
- Lung complications after surgery in Indian hospitals: **about 3% to 30%**, depending on the surgery and the study.
- Apollo Hospital, Chennai (330 patients): **9.4% overall**, about **14% after upper-abdominal surgery**, and **over 55% after chest surgery**.
- Udaipur study: patients with chest complications stayed **21.7 days vs 12.5 days** in hospital, and **8.5 vs 1.4 days in ICU**.

**Proof that tracking and reminders work**
- *JAMA Surgery* 2019: hourly reminder → **58% vs 28%** adherence.
- Penn Airalux study (2025, 30 patients, no comparison group): patients with a digital spirometer and reminders did about **15 sessions a day** and used it in about **7.6 hours a day**.

**International cost (only if needed)**
- Australia/New Zealand (1,473 patients): a lung complication added about **A$29,000** in hospital costs and about **9 extra days**.

---

## 4. Technical decisions confirmed

1. **Sensor:** use the **VL53L1X** (adjustable view down to 15°) rather than the VL53L0X. Test both if you have them.
2. **Mounting:** no plastic between the laser and the disc, or a thin window pressed against the sensor. Try a base mount too, since InSee uses one.
3. **Connection:** Bluetooth to an Android phone or laptop in Chrome. **Keep Wi-Fi as a backup.** On iPhone, use the dashboard and WhatsApp side only.
4. **Own AI model on the chip:** train in scikit-learn and convert with `emlearn`. Test on your exact ESP32 board early (day 4).
5. **Breath state machine:** split readings into separate breaths: waiting → breathing in → holding → falling. This is needed before the model can label breaths.
6. **Voice:** **Sarvam Bulbul v3**. It covers Hindi, Bengali, Tamil, Telugu, Gujarati, Kannada, Malayalam, Marathi, Punjabi, Odia and Indian English, and has a free tier. The company claims a first response in under 250 ms. Still pre-record the live during-breath phrases so they play instantly.

---

## 5. Hackathon itself

- We couldn't find an event called exactly "Social Impact Hackathon 2026".
- The closest match is **Hack for a Social Cause 2026** (Ministry of Youth Affairs, VBYLD, registration on the MY Bharat portal). Healthcare & Well-being is one of its themes. Teams are students aged 18–29, at most 3 members, one team per institution.
- ⚠️ A third-party site lists its **deadline as 15 October 2026, 6 days from today**. Check the official portal now.
- No official judging rubric was found. Read the "Competition Guidelines" attached to the official circular.

---

## 6. Regulation (India): what to say if asked

- India's regulator (CDSCO) classes devices A (lowest risk) to D (highest). The plain spirometer is CDSCO Class A (lowest risk, not diagnostic). Our measuring clip-on will need its own registration and licence.
- CDSCO finalised guidance for **medical device software in July 2026**. General **wellness** apps are excluded, and what the maker says the product is for decides whether software counts as a medical device.
- **Safe answer for judges:** "Today it's an exercise coach and tracker, not a diagnostic. The plain spirometer is CDSCO Class A; our measuring clip-on will need its own registration and licence before launch."

---

## 7. Changes to make in the plan

1. Replace "no one has done this" with the InSee comparison in section 1.
2. Design the cap to fit the **Romsons Breazer** first.
3. Switch the sensor to the **VL53L1X**.
4. Bluetooth first, Wi-Fi backup, and a note that iPhone isn't supported.
5. Add the breath state machine to day 3–4 of the build.
6. Use only the sourced numbers in section 3. Drop ₹50,000–2,50,000.
7. Confirm the hackathon's name, deadline and rubric today.

---

## Sources
- Eltorai et al., JAMA Surgery 2019: https://jamanetwork.com/journals/jamasurgery/article-abstract/2730077 · full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC6583822
- InSee FDA letter, Aug 2025 (K241152): https://www.accessdata.fda.gov/cdrh_docs/pdf24/K241152.pdf
- InSee EUA press release, 2021: https://www.prnewswire.com/news-releases/tidal-medical-technologies-receives-fda-emergency-use-authorization-eua-for-the-use-of-insee-for-tracking-of-incentive-spirometers-usage-in-treatment-of-respiratory-conditions-in-covid-19-patients-301333527.html
- Penn Airalux trial results: https://clinicaltrials.gov/study/NCT06629454 · AATS abstract: https://www.aats.org/resources/abstract.pdf?abstract=3136448
- Romsons Breazer prices: https://www.medikabazaar.com/products/romsons-breazer-2500-volumetric-lung-exerciser-mbpgmrsmmssrre15739 · https://www.medikabazaar.com/physiotherapy-rehabilitation-medical-aids/physiotherapy-rehabilitation/exerciser/brand-20282.html
- Indian PPC studies: https://www.ijsurgery.com/index.php/isj/article/view/3176 (Udaipur numbers, Int Surg J 2018;5:3057–65; corrected link) · https://doaj.org/article/8ce7474ddd114cdbb332bb5c0d16b782 · https://pmc.ncbi.nlm.nih.gov/articles/PMC12535847/
- PPC hospital costs (Australia/NZ): https://world.physio/congress-proceeding/impact-postoperative-pulmonary-complications-hospital-costs-and-length-stay
- VL53L1X field of view (ST UM2555): https://st.com/resource/en/user_manual/um2555-vl53l1x-ultra-lite-driver-multiple-zone-implementation-stmicroelectronics.pdf
- ST cover-window guidelines (AN5231): https://www.st.com/resource/en/application_note/an5231-cover-glass-guidelines-for-the-singlezone-timeofflight-sensor-stmicroelectronics.pdf
- emlearn: https://pypi.org/project/emlearn/0.6.0/ · https://emlearn-micropython.readthedocs.io/en/stable/getting_started_device.html
- Sarvam text-to-speech: https://docs.sarvam.ai/api-reference-docs/text-to-speech/api/overview
- CDSCO software guidance (2026): https://www.emergobyul.com/news/india-cdsco-finalizes-guidance-medical-device-software · classification portal: https://www.india-briefing.com/news/india-medical-device-licensing-classification-portal-42416.html
- Hack for a Social Cause 2026: https://mybharat.gov.in/pages/hack_social · https://www.sadakath.ac.in/newscircular.php?id=13 · https://www.startupgrantsindia.com/hacksocial-2026
