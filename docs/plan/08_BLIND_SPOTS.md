# Blind spots – what nobody has considered yet

**Written:** 10 Oct 2026, night · **Method:** walked through a real day as each person who touches SpiroBuddy, then removed everything already listed in `00_FOUNDER_NOTES.md`, `01`–`06`, `BUSINESS_BRIEF.md`, `HANDOFF.md` and `REQUIREMENTS.md`. Where an existing gap is close, it is cited (for example **G-32**) instead of repeated.

**How to read the tables**
- **Likely / Bad:** H = high, M = medium, L = low. Team judgement, not measured.
- **When:** **Sub** = matters before the hackathon submission (Mon 12 Oct, 11:00 IST) · **Pilot** = before any real patient · **Later** = at scale or when selling.
- **Basis:** a repo file, a web search snippet (not opened, grade C), or **"our reasoning"** (an idea nobody has checked).
- Nothing here is medical, legal or insurance advice.

---

## Answer in 12 lines

1. **35 new blind spots. 8 matter before tomorrow's submission; most of the rest block the first real patient.**
2. **Biggest one: nobody owns a patient's alerts after discharge.** Ward nurses look after in-patients. Once Ravi goes home, no shift is responsible, especially nights and Sundays (BS-12).
3. **The system treats "no data" as "did not exercise".** A flat phone or an expired data pack in a village would send a "missed 3 sessions" alert to the family (BS-3).
4. **Nothing stops the messages if a patient is readmitted or dies.** The code has no "pause" or "end" state. Messages to a grieving family would be the worst possible news story (BS-10).
5. **Anyone can breathe into the unit.** A son, a grandchild or a visitor turns the dashboard green. The data shows the exercise was done on the unit, not by the patient (BS-2).
6. **The commonest beginner mistake, blowing out instead of breathing in, is not handled.** The coach would just say "too shallow" (BS-1).
7. **Money: private insurers list the spirometer as "not payable" (insurer copies of the IRDAI list, snippets).** PM-JAY patients cannot be charged extra (state scheme page, snippet). So the hospital pays our fee itself and gets nothing back from insurance (BS-22, BS-23).
8. **Supplying the spirometer with the unit (advised in 05) makes us a seller of someone else's medical device.** That needs the MD-42 seller registration, which 06 marks "not applicable yet" (BS-21).
9. **Reminder calls from an unknown number look like spam or a scam to an elderly patient.** Real scammers can also copy our messages ("pay your unit deposit by UPI") (BS-6, BS-7).
10. **Pitch risks for tomorrow:** the name "Spiro" makes judges think of a lung-function test. The "95.8%" accuracy comes from simulated breaths. The team must be able to explain AI-written code in their own words (BS-17, BS-28, BS-29).
11. **Team risk for tomorrow:** the live site, database and keep-alive job all hang on one person's accounts. Judges may open the link days after 12 Oct, when free services may have paused (BS-31, BS-32).
12. **Cheapest wins:** one "I'm resting" button, a "not synced" status, an "end/pause episode" switch, and one line on every message: "We never ask for money or OTP". Each is a day's work or less, and none needs hardware.

---

## Already covered elsewhere (not repeated)

Hearing loss **G-14** · low vision **G-15** · non-readers **G-18** · missing language **G-19** · power cuts **G-25** · no smartphone or shared phone **G-26** · women and phones **G-27** · patients with no family **G-24** · alert overload for nurses **G-7** · false reassurance from a green tick **G-12** · family pressure **G-113** · staff measured **G-117** · helpline **G-30** · unit returns, including when a patient moves or dies **G-32** · infection control **risk 18**, **G-33** · biomedical intake **G-36** · no login **G-41** · free hosting and database pause **G-46** · time zones **G-52** · hospital IT links **G-56** · single vendor **G-60** · AI-written code ownership **G-87** · hackathon and college IP **G-88**, **G-89** · deposits **G-103** · camera-only rival **risk 10**, **E-18** · team dispersal **risk 6** · telecom caller-ID rules **risk 22**, `KNOWLEDGE_BASE.md` item 15 · personal criminal liability **L-17**.

---

## 1. The patient

*A day: wakes in pain on day 3 after a heart operation, dozes after lunch on painkillers, lives in a two-room house with five people, has a ₹199 prepaid data pack, and goes to his daughter's town after a week.*

| ID | Blind spot | Who it hurts | Likely | Bad | Cheapest test or fix | When | Basis |
|---|---|---|---|---|---|---|---|
| BS-1 | **Blowing out instead of breathing in.** It is the classic first-time mistake with an incentive spirometer. The disc does not rise, so our coach only says "too shallow" and the patient tries harder the wrong way | Patient; nurse sees false "poor technique" | H | M | Rule: session started + no rise for ~8 s → spoken "Breathe IN slowly, like sipping through a straw. Do not blow." One new clip per language. Test on 5 relatives with the simulator | Pilot (nice in demo) | Our reasoning; detector in `web/js/breath.js` has no such state |
| BS-2 | **Someone else does the breaths, or two people share the unit.** A son clears the alert, a grandchild plays with it, or a husband and wife who both had surgery use one unit | Nurse misled; the whole adherence claim; the AI training data | M | H | Flag any session far above the patient's own best (a fit adult pulls much more than a 68-year-old after surgery). Say "exercise recorded on this unit", never "patient did". Ask in the pilot exit interview | Pilot | Our reasoning |
| BS-3 | **No data is treated as a missed exercise.** Phone flat, Bluetooth off, data pack expired after discharge. The ladder counts missed slots only (`backend/app/comms/escalation.py`, `trailing_missed`) and goes on to the family and the nurse. 02 (M-16) separates "unit not seen" on the nurse screen, but not in the ladder | Patient blamed; family scared; nurse calls for nothing | H | M | A third slot status, "not synced", which never goes to the family. First ladder step for it is one question: "Did you do your breathing? Press 1 for yes." Check whether the hospital will top up a data pack | Pilot | Repo code + our reasoning |
| BS-4 | **Day-time sleep.** Patients sleep a lot after surgery and on painkillers. Hospital leaflets say "every hour *while awake*". Our schedule is fixed at 14 slots, 8 am–9 pm (`FEATURE_STATUS.md`), so a nap becomes "missed" and a call wakes him | Patient's rest; trust in the product | H | M | One big "I'm resting – remind me in an hour" button and voice word. Do not count rest hours as missed | Pilot | Repo + our reasoning |
| BS-5 | **The cough is missing.** Standard teaching pairs the deep breaths with a cough while hugging a pillow over the wound. Our coach counts breaths only | Patient (phlegm stays); clinical credibility | M | M | Ask the clinical lead (**G-9**) whether to add a "now cough, holding a pillow" step after each set; one clip | Pilot | Our reasoning (general nursing practice, not checked) |
| BS-6 | **Reminder calls look like spam.** An automated call from an unknown number gets a "spam" tag in caller-ID apps, or is ignored. Many older people are taught never to trust calls about health or money | Reminder ladder stops working | H | M | Call from the hospital's known number, or save our number in the patient's contacts at discharge, with the patient's phone in hand. Test: call 5 relatives cold and count who answers | Pilot | Our reasoning; legal side in risk 22 |
| BS-7 | **Scammers copy us.** Fake "SpiroBuddy" messages: "your unit deposit is due, pay by UPI", "share the OTP to update your device". Recent surgery and phone numbers leak from many sources | Patient's money; our name | M | H | One fixed line on every message, card and call: "SpiroBuddy and your hospital never ask for money, OTP or bank details." No such line exists in the code today (searched) | Pilot | Repo search + our reasoning |
| BS-8 | **The voice is loud in a shared space.** A small home or a general ward: 8 am prompts wake others, and "too shallow, try again" tells the neighbours. 20 units beeping on a ward is noise | Patient's dignity; other patients; nurses | M | L | A "quiet mode": lights, big screen, low volume, no spoken scores. A "ward mode" with no beeps | Pilot | Our reasoning |
| BS-9 | **The patient moves after discharge** to a son's or daughter's home in another town or state. Network, language of the family, and which hospital answers all change. **G-32** covers getting the unit back, not the care | Patient; return of unit; data jurisdiction | M | M | Ask at discharge "Where will you stay for the next two weeks?" and record it. Decide: the first hospital stays responsible | Pilot | Our reasoning |

## 2. The family member or guardian

*A day: a daughter in Dubai, 1.5 hours behind India, checks WhatsApp at work, sees "Papa missed 3 sessions", and calls the ward four times.*

| ID | Blind spot | Who it hurts | Likely | Bad | Cheapest test or fix | When | Basis |
|---|---|---|---|---|---|---|---|
| BS-10 | **Messages do not stop if the patient is readmitted or dies.** The backend has no "paused", "readmitted", "ended" or "deceased" state (searched `backend/app`). The ladder would keep calling and keep telling the family "missed sessions" | Grieving family; hospital; our reputation | L–M | H | "Pause or end episode" switch with a reason. The ladder checks it before every send. After 48 h with no data and no answer: nurse only, never family | Pilot | Repo search |
| BS-11 | **Worried families call the ward.** The product creates incoming calls. A family abroad sees red and rings the nurses' station at odd hours. **G-30** (helpline) is for patients, not families | Ward nurses; families | H | M | Every family message ends with what to do and who to call (not the ward), plus a "request a call-back" button with the hours written on it | Pilot | Our reasoning |

## 3. The ward nurse

*A day: 30 patients, a hand-over at 8 am and 8 pm, three other devices already alarming, a personal phone in her pocket.*

| ID | Blind spot | Who it hurts | Likely | Bad | Cheapest test or fix | When | Basis |
|---|---|---|---|---|---|---|---|
| BS-12 | **Nobody owns discharged patients.** A ward nurse cares for in-patients. After discharge, home patients belong to no shift, and nights, Sundays and festivals have nobody. **G-38** names a pilot coordinator, not who reads alerts. The patient may think he is watched 24×7 | Patient (false sense of safety); nurse; hospital | H | H | Before the pilot, write one paragraph: who reads alerts, which hours, what they do. Put the hours on every patient message: "Your nurse checks this 9 am–5 pm, Mon–Sat. Emergency: call 112." | Pilot | Our reasoning |
| BS-13 | **No shift hand-over view.** An alert seen at 7:50 pm is lost at 8 pm. With no login (**G-41**), nobody knows who saw what | Nurses; patients | M | M | A "since last shift" list, printable on one page | Pilot | Our reasoning |
| BS-14 | **Nurses use personal phones and WhatsApp.** Patient names and alerts land on private phones; hospital IT may ban it; data leaves when a nurse leaves | Patient privacy; hospital | M | M | Nurse alerts carry no name or diagnosis, only a link to the dashboard | Pilot | Our reasoning |

## 4. The doctor or physiotherapist

| ID | Blind spot | Who it hurts | Likely | Bad | Cheapest test or fix | When | Basis |
|---|---|---|---|---|---|---|---|
| BS-15 | **The champion may lose work.** 05 names the physiotherapy head as the way in. A home coach could cut billable physio visits, or look like it replaces them | Our champion; the sale | M | M | Make the physio the owner: they set the target and get the report. Ask directly in interviews: "Would this take visits away from your department?" | Pilot | Our reasoning; 05 line 1 |
| BS-16 | **Doctors will not log in.** They want one line in the follow-up visit, not a dashboard | Adoption | H | L | A one-page printable summary for the follow-up visit. It is also the paper backup | Pilot | Our reasoning |
| BS-17 | **"Spiro" means a lung-function test to most doctors and judges.** They will ask "how accurate is it compared to a PFT?" It may also push a regulator toward reading it as a diagnostic device | Pitch; licence class | H | M | Always open with "incentive spirometer – a breathing exerciser"; never show lung-test numbers like FEV1 | **Sub** | Our reasoning |

## 5. The hospital (admin, purchase, biomedical, infection control, IT, legal)

*Purchase, biomedical, infection control and IT are covered in **G-36**, **risk 18**, **G-47**, **G-53**, **G-56**, and 05 E-3. New points:*

| ID | Blind spot | Who it hurts | Likely | Bad | Cheapest test or fix | When | Basis |
|---|---|---|---|---|---|---|---|
| BS-18 | **Getting the data creates a duty to act.** Once an alert reaches the hospital, its lawyer may fear blame if nobody acts on it at night. They may say no, or ask us to staff it | The sale; legal risk | M | H | Pilot agreement states the monitoring hours, "not an emergency service", alerts are advisory, and patients are told to call 112. Ask the hospital's legal team early | Pilot | Our reasoning; 06 L-17 covers *our* liability, not the hospital's fear |
| BS-19 | **The hospital's own marketing makes claims we cannot.** A press release saying "AI device prevents lung infection" still carries our name. Under consumer law we are the "product manufacturer" (06 L-17) | Us (advertising law); trust | M | M | A clause: public statements about the product need our OK. Give them a wording sheet using the "say / do not say" list in 06 | Pilot | 06 + our reasoning |
| BS-20 | **"Put our logo on it."** A hospital wants its own brand and voice. Device labels still need the maker's name, and our brand disappears for patients | Brand; labelling | M | L | Rule: "Hospital X, with SpiroBuddy". The maker's label stays on the unit | Later | Our reasoning |
| BS-21 | **Supplying the spirometer makes us a device seller.** 05 (lines 3–4) says to supply the spirometer with the unit. Anyone who sells, stocks or distributes a medical device needs an MD-42 registration (02 business file, B2-10a). 06 marks MD-42 "not applicable yet" | Us (regulatory) | M | M | Let the hospital buy the spirometer from its usual supplier, or ask the consultant. Fix the line in 06 | Pilot | `02_sales_and_go_to_market.md` B2-10a; `06` row 33; search snippets |

## 6. The payer

| ID | Blind spot | Who it hurts | Likely | Bad | Cheapest test or fix | When | Basis |
|---|---|---|---|---|---|---|---|
| BS-22 | **Private insurers list the spirometer as "not payable".** Insurer and TPA copies of the IRDAI non-payable list include "spirometre" (marked "device not payable"). If the hospital puts our fee on an insured patient's bill, the claim is likely cut and the patient pays at discharge, angry | Patient; hospital billing | H | M | Do not bill it as a separate "spirometer" line. Price it into the hospital's own costs. Ask one hospital's insurance desk | Pilot | Web search snippets (insurer/TPA PDFs, not opened) |
| BS-23 | **PM-JAY patients cannot be charged extra.** The package covers 15 days after discharge (PIB fact sheet, snippet), and a state scheme page says hospitals may charge nothing beyond the package. 05 says to lead with package patients. So the hospital pays our fee out of the package margin. Upside: our 14-day episode sits inside that 15-day window | Our price | H | M | Check the rule in the official PM-JAY guidelines. Ask a hospital's PM-JAY desk: "Could a ₹500 post-discharge item fit in the package?" | Pilot | Web search snippets; 05 line 21 |
| BS-24 | **CSR money usually goes through a registered NGO or trust, not a startup.** The brief says "donor or CSR money for government hospitals". There is no plan for who receives it | Funding plan | M | M | Partner with the hospital's trust or an NGO; ask one CSR head how they would fund it | Later | Our reasoning (rule not checked this round) |

## 7. Competitors and substitutes

| ID | Blind spot | Who it hurts | Likely | Bad | Cheapest test or fix | When | Basis |
|---|---|---|---|---|---|---|---|
| BS-25 | **The real rival is a free paper tally chart plus a nurse's phone call.** Judges and buyers will ask "why not a ₹10 sheet?" | Pitch; sale | H | M | Answer: we record *how* each breath was done (speed, depth, hold), not only *that* it was done. Add a paper-chart arm to assumption test J-8 | **Sub** (answer) · Pilot (test) | Our reasoning; 04 J-8 |
| BS-26 | **Hospitals' own post-discharge call teams.** Big chains already phone patients after discharge. They could add one question: "Are you doing your breathing?" | Sale | M | M | Ask in interviews: "Who calls patients after discharge today?" | Pilot | Our reasoning |
| BS-27 | **Breathing trainers and home lung-test devices with phone apps are not mapped.** Buyers may lump them in with us or spend the "smart breathing" budget on them | Positioning | M | L | A one-hour desk scan after the hackathon; one comparison table | Later | Our reasoning (not checked) |

## 8. The investor, the grant reviewer and the hackathon judge

| ID | Blind spot | Who it hurts | Likely | Bad | Cheapest test or fix | When | Basis |
|---|---|---|---|---|---|---|---|
| BS-28 | **"95.8%" is accuracy on simulated breaths** (`HANDOFF.md`). A judge who spots this will doubt everything else | Credibility | H | M | Say "trained on simulated breaths; accuracy on real breaths not measured yet; simple rules run as a backup" | **Sub** | Repo |
| BS-29 | **The team must explain AI-written code in its own words.** Most of the code was written with an AI tool (**G-87** covers ownership, not understanding). A live "how does your classifier work?" can sink the pitch | Pitch; investor trust | M | H | Each member owns one part (sensor, breath detection, model, alerts, money) and rehearses a 60-second explanation tonight | **Sub** | Our reasoning |
| BS-30 | **"Where exactly is the AI?"** Judges dislike "AI" as a sticker. Today: a breath classifier, a three-sentence summary writer, and a voice service | Pitch | M | M | Name the three AI parts plainly, and say alerts come from fixed rules on purpose (safety) | **Sub** | `REQUIREMENTS.md` §5 |

## 9. The team

| ID | Blind spot | Who it hurts | Likely | Bad | Cheapest test or fix | When | Basis |
|---|---|---|---|---|---|---|---|
| BS-31 | **One person holds everything.** GitHub, Render, Supabase, the keep-alive job and the voice key sit on one person's accounts. The founder also records the video and does the voice-over. One illness on Sunday means no submission | Submission; pilot | M | H | Add a second admin on each service. Keep a private list (not in the repo) of where each login lives. A second person rehearses the submission steps | **Sub** | `HANDOFF.md`, `00_FOUNDER_NOTES.md` #27; **G-60** covers vendors, not people |
| BS-32 | **Judges may open the link days after 12 Oct.** The free database pauses after a quiet week (**G-46**), keys can expire, and an auto-deploy on a late push can break the live site | Judging | M | H | Freeze `main` after submission (no pushes until results). Check the link daily until results. Keep a recorded video as the fallback | **Sub** | Repo + our reasoning |

## 10. Edge cases

| ID | Blind spot | Who it hurts | Likely | Bad | Cheapest test or fix | When | Basis |
|---|---|---|---|---|---|---|---|
| BS-33 | **Police, court or insurer asks for our logs** after a death or a dispute. There is no process and no named person, and logs on free plans may be gone | Us; hospital | L | H | One-page rule: send the request to the hospital (it decides how the data is used); keep everything; call the lawyer. Set a log-keeping period (**G-54**) | Pilot | Our reasoning |
| BS-34 | **A media story, good or bad.** Good: a reporter writes "students' device prevents pneumonia" after a win, which is a claim we must not make (B4-20). Bad: "AI keeps calling dead man's family" (BS-10). No spokesperson, no approved paragraph | Reputation; legal | M | M | Write a 5-line press note now, using only allowed wording. Name one spokesperson | **Sub** (if we win) · Pilot | 06 "say / do not say"; our reasoning |
| BS-35 | **A lent hub phone is lost or stolen while signed in.** It can show patient data and send family messages. No "cut off this phone" button exists | Patient privacy | L | M | A "revoke" button on the Units screen that kills the phone's token | Pilot | `DEVICE_LIFECYCLE.md` (token per unit) + our reasoning |

---

## Top 15 new blind spots, ranked

Ranked by how likely × how bad, with anything that hits tomorrow pulled up.

| # | ID | Blind spot | Likely / Bad | When | Cheapest fix |
|---|---|---|---|---|---|
| 1 | BS-12 | Nobody owns discharged patients' alerts; patients may think they are watched 24×7 | H / H | Pilot | Written monitoring hours on every message; a named reader |
| 2 | BS-10 | Messages continue after readmission or death; no pause/end state in code | L–M / H | Pilot | "Pause / end episode" switch checked before every send |
| 3 | BS-3 | "No data" counted as "missed"; the family is alarmed by a flat phone | H / M | Pilot | A "not synced" status that never goes to family |
| 4 | BS-31 | One person holds every account and the voice-over | M / H | **Sub** | Second admin; a second person rehearses the submission |
| 5 | BS-32 | Live link may break while judges are still looking | M / H | **Sub** | Freeze `main`; check daily; video fallback |
| 6 | BS-28 | "95.8%" is simulated accuracy | H / M | **Sub** | Say so plainly |
| 7 | BS-29 | Team cannot explain AI-written code | M / H | **Sub** | One owner per part, 60-second rehearsal |
| 8 | BS-17 | "Spiro" heard as a lung-function test | H / M | **Sub** | Say "incentive spirometer – breathing exerciser" first |
| 9 | BS-2 | Anyone can do the breaths; the data proves the unit was used, not who used it | M / H | Pilot | Flag sessions far above the patient's own best; careful wording |
| 10 | BS-23 | PM-JAY: hospital cannot pass our fee on | H / M | Pilot | Ask a PM-JAY desk; price inside the package |
| 11 | BS-22 | Insurers treat the spirometer as non-payable | H / M | Pilot | Do not bill it as a separate line |
| 12 | BS-18 | Hospital fears a duty to act on alerts | M / H | Pilot | "Not an emergency service" and stated hours in the agreement |
| 13 | BS-7 | Scammers copy our reminders | M / H | Pilot | "We never ask for money or OTP" on everything |
| 14 | BS-1 | Blowing out instead of in is not detected | H / M | Pilot | No-rise rule + "sip, don't blow" clip |
| 15 | BS-4 | Day-time naps become "missed"; a call wakes a recovering patient | H / M | Pilot | "I'm resting" button |

Just outside the top 15: BS-25 (paper chart is the real rival, needed as a pitch answer tomorrow), BS-6 (spam-looking calls), BS-11 (families calling the ward), BS-21 (MD-42 if we supply the spirometer).

---

## What to add to the pitch tomorrow (max 5 lines)

1. "SpiroBuddy is a coach for the incentive spirometer, the breathing exerciser given after surgery. It is not a lung-function test."
2. "Our breath model is trained on simulated breaths. Its accuracy on real patients is not measured yet, and simple rules run as a backup."
3. "A paper tally sheet counts sessions. We also record how each breath is done (speed, depth and hold), and testing whether that helps is our first study question."
4. "Before any real patient, we will add: stated nurse hours on every message, a 'not synced' state kept apart from 'missed', and one switch that stops all messages if a patient is readmitted."
5. "For government-scheme patients the hospital cannot bill extra, so our price has to fit inside its package. That is a question for our first interviews."

---

## Web searches and URLs

No web page was opened. Three web searches were run; only the search-result summaries were read (grade C, "snippet only"). None of these URLs is in `docs/research/SOURCES_LEDGER.md` as a page we read.

1. IRDAI non-payable list (BS-22). Result URLs: https://www.iitg.ac.in/medical/IRDANonpayale.pdf · https://www.icicilombard.com/docs/default-source/other-documents/sc-annexure---non-payable-list.pdf · https://uatintegrations.paramounttpa.com/paramounttpa/Home/Download/IRDA%20NON%20PAYABLE%20LIST%20-%20Year%20-%202013-14.pdf · https://bajajgeneralinsurance.com/download-documents/health-insurance/PRODUCT-WISE-SPECIFIC-LIST-OF-EXCLUDED-ITEMS.pdf · https://rahejaqbe.com/uploads/images/health-claim/pdf/List_of_Non_payable_Items_Health_Products.pdf
2. PM-JAY post-discharge window and no extra charges (BS-23). Result URLs: https://static.pib.gov.in/WriteReadData/specificdocs/documents/2024/sep/doc2024923400001.pdf · https://biswass.bihar.gov.in/pages/Scheme_coverage.aspx · https://vikaspedia.in/health/nrhm/national-health-mission/ayushman-bharat%E2%80%93pm-jan-arogya-yojana
3. MD-42 seller registration (BS-21). Result URLs: https://corpseed.com/knowledge-centre/medical-device-wholesalers-traders-and-retailers-registration-cdsco-form-md-42 · https://www.agileregulatory.com/blogs/medical-device-distributor-license-in-india-registration-process (this agreed with the repo's own B2-10a, so the only new finding is the link to 05's "supply the spirometer" advice)
