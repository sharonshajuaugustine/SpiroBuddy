# 03 – Costs and budget: what it costs to get SpiroBuddy out, stage by stage

**Written:** 10 Oct 2026 · **Answers:** founder notes items 7 and 15 (`docs/plan/00_FOUNDER_NOTES.md` §A-7, §C-15) · **Confidence overall:** medium for parts and official fees, **low** for adviser, insurance, testing and quality-system costs (no quotes exist yet).

**How to read this file**
- Every number names where it came from: a file and section in this repo, or a search result from this round (list at the end).
- **Grades:** **A** = primary source (official page, law, the vendor's own price page read by us or an earlier agent). **B** = secondary source opened by an earlier agent (vendor page, law-firm note). **C** = search snippet or a team estimate written in an earlier file. **Est.** = our own reasoned estimate in this file, with the reasoning shown. **Quote needed** = no price was found anywhere; the estimate next to it is a placeholder, not a price.
- **Money:** ₹96 = US$1, the rate in `02_MOBILE_APP_AND_BLUETOOTH.md` (header). `FUTURE_ARCHITECTURE.md` §11 used ₹88, so its dollar figures are about 9% higher here.
- **GST** (India's goods and services tax) is 18% on electronic parts (`01_HARDWARE_REVIEW.md` §H-9). Until the company is GST-registered it cannot claim that tax back, so pilot hardware is costed **with** GST.
- **Not included anywhere:** salaries and the team's own time. Today that is the largest real cost, and it is unpaid (`04_GAPS_AND_RISKS.md`, "Hand to the costs file", last row).
- Indian number format: ₹1,00,000 = 1 lakh; ₹1,00,00,000 = 1 crore. Fake patients only.

---

## Answer in 12 lines

1. **(a) Bench test** (one test unit on a real spirometer, on a desk): **about ₹8,000–13,000.**
2. **(b) Working demo with Bluetooth** (2–3 battery units talking to an Android phone): **about ₹12,000–52,000 in total**, including the bench test. The low end assumes the team uses its own phones.
3. **(c) A 30-patient, 3-month pilot at one hospital: about ₹2.1–12.4 lakh for the pilot stage itself; a realistic middle is about ₹5.5 lakh.** Including (a) and (b): **about ₹2.2–12.9 lakh.**
4. **(d) First paid sale** (licence, quality system, safety tests, security test, trademark, insurance): **another ₹4–20 lakh**, mostly estimates. **Cumulative: about ₹6–33 lakh**, plus the stock of units you sell.
5. The pilot range is wide because of five yes/no items: **CDSCO permission (₹0 at a government-funded hospital, ₹1,00,000 at a private one), the ethics committee fee (₹10,000–88,500), study insurance, the lawyer, and whether we buy phones for patients.**
6. **The device now costs about ₹2,500 a unit before GST (₹2,700–2,950 with GST), not ₹1,500.** That one change moves every earlier business figure.
7. **A lent 14-day episode now costs us about ₹670 in a pilot and about ₹470 at scale** (was ₹505 and ₹318).
8. **"Device + software for ₹200": no.** A sold device loses about ₹2,750 a unit at ₹200. A lent device loses about ₹270 an episode at scale. **₹200 works only as a software fee per patient on units the hospital owns, and only at scale** (we keep about ₹125).
9. **App stores: Android ₹2,400 once. Apple ₹9,500 every year – skip it until a hospital asks.**
10. **Running one hospital on the lend model costs about ₹32,000–59,000 a month**, of which about ₹19,000 is device wear and loss. At ₹500 an episode that hospital brings in about ₹25,000. **Charge ₹1,000 an episode, or let the hospital own the units.**
11. **One NIDHI-PRAYAS grant (up to ₹10 lakh) covers a realistic pilot** (`docs/research/business/03_scale_funding_unit_economics.md` §B3-7).
12. **About half the money in this file has no real price yet.** The five quotes that matter most: study insurance, a regulatory consultant, the ethics committee fee at the chosen hospital, a lawyer for the pilot papers, and an accredited lab for safety tests.

---

## 1. Stage-by-stage budget

Columns: **Item | One-off or monthly | ₹ low | ₹ high | Source / grade | Notes.** Totals are rounded.

### Stage A – Bench test (answers "does the sensor read the piston?")

| Item | One-off or monthly | ₹ low | ₹ high | Source / grade | Notes |
|---|---|---|---|---|---|
| 2 Romsons Breazer 2500 spirometers | One-off | 400 | 2,000 | `01_HARDWARE_REVIEW.md` §H-11 row 1 (RESEARCH_REPORT §4.1) / C | One to keep whole, one to cut |
| Digital caliper | One-off | 500 | 1,000 | §H-11 row 2 / C | Needed to measure the spirometer base |
| Electronics: XIAO ESP32-C3, XIAO nRF52840, 2 × VL53L1X, VL53L4CX, LIS3DH | One-off | 6,046 | 6,046 | §H-11 rows 3–7, ₹5,124 + 18% GST / B (Evelta shop prices) | Shop prices, not quotes |
| Small parts: LiPo cell, wires, breadboard, black foam and tape, beeper | One-off | 500 | 1,500 | §H-11 row 8 "not sourced" / **Est.** | A 1,000 mAh cell was seen at about ₹237 each (2-pack ₹474, Amazon deal page, snippet, C) |
| 3D-printed test stand | One-off | 300 | 1,600 | `03_scale…` §B3-3 (₹3–8 a gram, 100–200 g) / C | ₹0 if a college printer is free |
| Delivery | One-off | 0 | 500 | **Est.** | |
| Microamp meter, calibration syringe | – | 0 | 0 | §H-11 row 9; §H-8 | Borrow from the college lab and a hospital lung-function lab |
| **Stage A total** | | **≈ 7,750** | **≈ 12,650** | | **Say ₹8,000–13,000** |

### Stage B – Working demo with Bluetooth (2–3 battery units + Android phone)

Builds on Stage A (the bench parts become demo unit no. 1).

| Item | One-off or monthly | ₹ low | ₹ high | Source / grade | Notes |
|---|---|---|---|---|---|
| Extra pilot-design units (nRF52840 + sensor + motion chip + cell + small parts) | One-off | 2,700 (1 unit) | 8,850 (3 units) | `01_HARDWARE_REVIEW.md` §H-9(b): ₹2,700–2,950 each with GST / B + C | ₹2,000 of each unit is sourced; ₹300–500 is the repo's own estimate |
| Spare LiPo cells | One-off | 474 | 474 | Amazon 2-pack snippet / C | Must be BIS-marked for patients (`06_LEGAL_DEEP_DIVE.md` §L-4); this one is not confirmed |
| Printed cases | One-off | 600 | 4,800 | §B3-3 / C | 2–3 cases at ₹300–1,600 |
| Android test phones | One-off | 0 | 20,000 | `02_MOBILE_APP_AND_BLUETOOTH.md` §M-36 phase 0 / **Est.** | ₹0 if the team's own phones are used |
| Bluetooth sniffer (nRF52840 dongle) | One-off | 0 | 2,900 | §M-35 / C | Nice to have; skip at first |
| Google Play developer account | One-off | 0 | 2,400 | §M-21, US$25 / A | Not needed for a demo: install the app file directly |
| Hosting | Monthly | 0 | 0 | today's free plans | Fine for a demo with fake data only |
| **Stage B increment** | | **≈ 3,800** | **≈ 39,400** | | |
| **Cumulative A + B** | | **≈ 12,000** | **≈ 52,000** | | |

### Stage C – Pilot: 30 patients, one hospital, 3 months running (plus about 1 month of set-up)

**Assumptions (Est.):** each patient uses a unit for one 14-day episode. "Low" lends each unit to several patients: about 12 in use at once + 20% spares = **15 units**. "High" gives every patient a fresh unit: 30 + 20% = **36 units**. Hosting is paid for 4 months. 30 episodes of 14 days ≈ **15 patient-months** of messaging and AI use.

#### C1. Hardware

| Item | One-off or monthly | ₹ low | ₹ high | Source / grade | Notes |
|---|---|---|---|---|---|
| Pilot units (15 or 36, including 20% spares) | One-off | 40,500 | 1,06,200 | §H-9(b) ₹2,700–2,950 with GST; spares per `04_GAPS…` G-31 / B + C | The biggest hardware line |
| Small circuit-board run + hand assembly set-up | One-off | 5,000 | 20,000 | `03_scale…` §B3-2: ₹799 for 5 boards (B); assembly set-up ₹3,000–15,000 (C) | Replaces loose wires; makes units repeatable |
| Calibration / test jig | One-off | 0 | 5,000 | **Est.** | A printed block of known heights for the "function check" between patients |
| Spirometer for each patient (single-patient item) | One-off | 4,400 | 32,000 | `05_EXPANSION…` line 19: ₹146–1,067 each (#7, #8) / B | ₹0 if the ward already stocks volume-type spirometers. The offer should include it |
| Hub phones for patients with no smartphone | One-off | 0 | 60,000 | `DEVICE_LIFECYCLE.md` §options row 4: ₹5,400–6,000 each / C | High = 10 phones. Low = patients' own phones or the hospital lends |
| Data SIMs for hub phones | Monthly | 0 | 9,000 (3 months) | **Quote needed.** Est. ₹300 a month × 10 | |
| More test phones (the hub model + the common brands) | One-off | 10,000 | 80,000 | §M-34, §M-36 phase 1 / C (snippet prices) | Low = one more phone; high = the full 8–10 phone matrix |
| **C1 subtotal** | | **≈ 59,900** | **≈ 3,12,200** | | |

#### C2. Software and running costs

| Item | One-off or monthly | ₹ low | ₹ high | Source / grade | Notes |
|---|---|---|---|---|---|
| Paid hosting in India with backups (4 months) | Monthly | 22,000 (₹5,500 a month) | 84,000 (₹21,000 a month) | High: `FUTURE_ARCHITECTURE.md` §11 pilot tier, US$220 a month / C. Low: Supabase Pro US$25 (`04_GAPS…` hand list, W1, B) + a small Mumbai app server, **Est.** | Free plans are not allowed with real patients (`04_GAPS…` G-46 to G-48). High includes point-in-time recovery (from US$100 a month) and monitoring |
| WhatsApp updates | Per patient-month | 150 | 750 | §11: ₹10 a patient-month; Meta utility rate ₹0.115 a message (#61) / B | +₹40 a patient-month if sent through Twilio (#107) |
| AI phone calls + a phone number | Monthly | 800 | 1,400 | §11: ₹36 a patient-month; Plivo ₹0.38 a minute + ₹200 a month per number (#109) / B | |
| Voice (text to speech) | Per patient-month | 0 | 270 | §11: ₹0–18 / B (#53) | ₹0 with pre-recorded clips |
| AI summaries (Claude) | Per patient-month | 0 | 255 | §11: ₹17 / B | ₹0 if the template fallback is used |
| Domain, email, privacy-policy page | One-off + yearly | 1,000 | 5,000 | **Quote needed.** Est. | Stores need a privacy page (§M-24) |
| Google Play account | One-off | 2,400 | 2,400 | §M-21 / A | For the "managed private app" or closed test (§M-23) |
| D-U-N-S company number | One-off | 0 | 10,000 | §M-21: free from D&B; up to ₹10,000 through a consultant / A + C | Only for an organisation store account |
| Apple developer account | Yearly | 0 | 0 | §M-25 | Deferred: Android first |
| **C2 subtotal** | | **≈ 26,400** | **≈ 1,04,000** | | |

#### C3. Company, legal and ethics (Gate 1 in `06_LEGAL_DEEP_DIVE.md`, "Master legal checklist")

| Item | One-off or monthly | ₹ low | ₹ high | Source / grade | Notes |
|---|---|---|---|---|---|
| Incorporate a private limited company (digital signatures, name, stamp duty, professional fee) | One-off | 7,000 | 25,000 | 2026 guides seen this round: all-in ₹7,000–25,000 / C. `03_scale…` §B3-15 said ₹8,000–20,000 + fees / C | Stamp duty depends on the state. Needed before the test licence (§L-14) |
| DPIIT recognition, Udyam registration | One-off | 0 | 0 | `06_LEGAL…` Gate 1 #11 / A | |
| Chartered accountant: first-year filings | Yearly | 12,000 | 50,000 | packages seen this round ₹11,999–50,000 a year / C | Late filing costs ₹100 a day per form (`04_GAPS…` hand list, C) |
| Bookkeeping | Yearly | 0 | 30,000 | ₹10,000–30,000 a year seen this round / C | Low = a founder does it in free software |
| Lawyer: founders' agreement with IP assignment, pilot agreement, unit-loan terms, data-processing agreement | One-off | 20,000 | 1,00,000 | **Quote needed.** Est.: 4–5 documents, template-based at a small firm vs custom drafting | `06_LEGAL…` Gate 0 #3, Gate 1 #18 |
| Regulatory consultant: written answer on device class and "CDSCO permission or not" | One-off | 0 | 65,000 | Hourly rates for India work US$110–340 (one consultancy's guide, snippet, C) → 1–2 hours. **Quote needed** for a written opinion | Low = MedTech Mitra, which states no fee (`05_icmr…` §B5 MedTech Mitra / A) |
| Test licence for prototypes (Form MD-13) | One-off | 7,500 | 18,000 | `06_LEGAL…` Gate 1 #13: ₹500 per device / A | 15 or 36 units |
| CDSCO permission for the study (Form MD-22) | One-off | 0 | 1,00,000 | `06_LEGAL…` §L-1: ₹1,00,000; nil if a government-run or government-funded hospital sponsors / A | Plan for it (Reading A in §L-1) |
| Trial registration (CTRI) | One-off | 0 | 0 | `05_icmr…` CTRI finding / A | |
| Ethics committee review fee | One-off | 10,000 | 88,500 | Fee lists seen this round: JSS Mysore ₹10,000 (external academic) to ₹75,000 + GST (private-sponsored); CHARUSAT ₹50,000 / C | Varies by hospital. Ask the chosen hospital |
| Study insurance (no-fault compensation cover) | One-off | 25,000 | 1,00,000 | **Quote needed.** No Indian premium published (`04_legal…` §B4-19; this round's search found policy wordings, no prices). Est.: small study, 30 people, about 4 months | Ethics committees usually ask for it. The pilot cannot start without it (G-93) |
| Radio approval (WPC) | One-off | 0 | 10,000 | `06_LEGAL…` §L-2: ₹0 if an approved module is used unchanged; ₹10,000 per model otherwise / A | Confirm the XIAO board's module has an approval |
| **C3 subtotal** | | **≈ 81,500** | **≈ 5,86,500** | | |

#### C4. Operations

| Item | One-off or monthly | ₹ low | ₹ high | Source / grade | Notes |
|---|---|---|---|---|---|
| Printing: quick-start cards, leaflets, asset tags, "cleaned on" tags, consent forms | One-off | 3,000 | 10,000 | **Quote needed.** Est. | `04_GAPS…` G-29, G-33, G-78 |
| Translation and clinical check of voice lines and leaflets (1–2 languages) | One-off | 0 | 20,000 | **Quote needed.** Est. | Low = team + volunteer clinician |
| Cleaning supplies (detergent, 70% alcohol wipes, gloves, bags) | One-off | 500 | 2,000 | **Est.** Protocol in `06_sell_vs_share.md` §B6-11 | |
| Team travel to the hospital (3 months) | Monthly | 10,000 | 40,000 | **Est.** | Depends on distance |
| Courier for units not returned at follow-up | Per unit | 0 | 4,800 | `06_sell_vs_share.md` §B6-17: ₹80 a shipment (team assumption) / C | 30 × 2 trips |
| Training video for nurses | One-off | 0 | 0 | `04_GAPS…` hand list: team time | |
| Clinical adviser | – | 0 | 0 | **Quote needed** if paid | **Never pay clinicians at the pilot hospital** (`06_LEGAL…` Gate 1 #22). An outside adviser may be paid under a written contract |
| **C4 subtotal** | | **≈ 13,500** | **≈ 76,800** | | |

#### C5. Pilot total

| | ₹ low | ₹ middle (Est.) | ₹ high |
|---|---|---|---|
| C1 Hardware | 59,900 | 1,57,000 | 3,12,200 |
| C2 Software and running | 26,400 | 54,000 | 1,04,000 |
| C3 Company, legal, ethics | 81,500 | 2,27,000 | 5,86,500 |
| C4 Operations | 13,500 | 44,000 | 76,800 |
| Contingency 15% (Est.) | 27,200 | 72,000 | 1,62,000 |
| **Pilot stage total** | **≈ 2.1 lakh** | **≈ 5.5 lakh** | **≈ 12.4 lakh** |
| **Including Stages A and B** | **≈ 2.2 lakh** | **≈ 5.8 lakh** | **≈ 12.9 lakh** |

**The middle case** assumes 24 units, 5 hub phones, a government-funded teaching hospital as sponsor (so no CDSCO fee), an ethics fee of ₹40,000, insurance at ₹50,000, a lawyer at ₹50,000 and a consultant at ₹25,000.

**Where the money goes:** legal, ethics and insurance are about 40–50% of the pilot. Hardware is about 25–30%. Hosting and AI together are under 15%. **Messaging, voice and AI for 30 patients cost under ₹3,000 in total.**

### Stage D – First paid sale (Gates 2 and 3 in `06_LEGAL_DEEP_DIVE.md`)

A sale is not lawful before a manufacturing licence (`BUSINESS_BRIEF.md`, "We cannot sell yet").

| Item | One-off or monthly | ₹ low | ₹ high | Source / grade | Notes |
|---|---|---|---|---|---|
| Manufacturing licence (state, Form MD-5) | One-off | 5,500 | 5,500 | `06_LEGAL…` Gate 2 #24: ₹5,000 + ₹500 / A | 45 days to about 5 months |
| Quality system and technical file | One-off | 1,00,000 | 5,00,000 | **Quote needed.** Est. (consultant help + documents). `06_LEGAL…` Gate 2 #25 "n/f" | Certification audit later: quote needed |
| Electrical safety and radio-interference tests at an accredited lab (IS 13450 / IEC 60601) | One-off | 1,00,000 | 5,00,000 | **Quote needed.** Est. AMTZ lists these labs with no prices (`03_scale…` §B3-5) | Ask AMTZ or a college lab first |
| Packaging, drop and transport tests; lithium transport paperwork | One-off | 20,000 | 1,00,000 | **Quote needed.** Est. (`04_GAPS…` G-80) | Cell supplier should give the UN 38.3 test summary free |
| Security test of the web app (VAPT) | One-off, then yearly | 40,000 | 3,50,000 | `04_GAPS…` hand list / C | Hospitals will ask before a contract |
| Regulatory consultant for the licence | One-off | 50,000 | 3,00,000 | **Quote needed.** Est. | |
| Trademark SPIROBUDDY, 3–4 classes | One-off | 13,500 | 18,000 | `06_LEGAL…` §L-11: ₹4,500 per class for startups / C | Free search first |
| Design registration of the case | One-off | 1,000 | 1,000 | `06_LEGAL…` Gate 3 #36 / C | File before the final case is shown publicly |
| GST registration | One-off | 0 | 0 | `06_LEGAL…` §L-15 / C | Compulsory from the first rupee for sales to another state |
| Product liability + cyber insurance | Yearly | 50,000 | 1,00,000 | Cyber ₹1 crore cover ≈ ₹50,000 a year (`04_legal…` §B4-19, 2023 press, C); product liability **quote needed** | |
| Labels and instructions with the licence number | One-off | 5,000 | 20,000 | **Est.** | `06_LEGAL…` Gate 3 #30 |
| Apple developer account (only if a hospital needs iPhone) | Yearly | 0 | 9,500 | `02_MOBILE…` §M-22 / A | |
| D-U-N-S for public store listing as an organisation | One-off | 0 | 10,000 | §M-21 / A + C | |
| **Stage D total (before stock)** | | **≈ 4.1 lakh** | **≈ 19.6 lakh** | | Mostly estimates |
| Stock: 50 units for the first sale | One-off | 1,35,000 | 1,47,500 | §H-9(b) | Paid back by the sale. Not in the total |
| **Cumulative A + B + C + D** | | **≈ 6.3 lakh** | **≈ 32.5 lakh** | | |

**Not needed for a first sale:** an injection mould (₹3–7 lakh, `03_scale…` §B3-4, pays back only above about 1,000 units), an iPhone app, ISO certification, a 1,000-unit build.

---

## 2. Unit economics, redone with the new unit cost

**What changed:** the earlier files used a ₹1,500 unit (`03_scale…` §B3-6; `06_sell_vs_share.md` §B6-1). The hardware review prices a real pilot unit (Bluetooth, battery, motion sensor, case) at **₹2,300–2,500 before GST** and says to use **about ₹2,500** (`01_HARDWARE_REVIEW.md` §H-9, "Does the repo's ₹1,000–1,700 hold?"). A cheaper volume price "cannot be stated honestly" until four quotes exist (sensor chip, battery, board, case). Below, ₹2,500 is the base. ₹1,000 and ₹600 are **what-if** cases, not prices.

All other lines use the same method as §B3-6 so the old and new tables can be compared. Server costs are converted at ₹96.

### 2.1 How many patients one unit serves

| Limit | What it gives | Source / grade |
|---|---|---|
| Loss or not returned | At 5% lost per episode, a unit lasts about 20 episodes on average. At 10%: 10. At 20%: 5 | `06_sell_vs_share.md` §B6-16 (foreign return data, much worse than 5%) / B; 5% is an assumption |
| Calendar | 14 days in use + 2–4 days for cleaning and waiting ≈ **18–20 episodes a year at most** | **Est.** |
| Battery | A 1,000–1,200 mAh cell lasts about 40 days per charge (`01_HARDWARE…` §H-4), so about one charge per episode. Battery wear is not the limit in the first year | Est. from §H-4; cycle life not sourced |
| Wear from alcohol wipes, drops | Unknown. The pilot must measure it | `04_GAPS…` G-79 |

**Base case: 10 patients per unit (about 6 months of use). Ceiling: 20 (about one year).**

### 2.2 Lent model: cost to us per 14-day episode

| Cost line (₹ per episode) | Pilot (~50 active) | Scale (~5,000 active) | Source |
|---|---|---|---|
| Device share: ₹2,500 ÷ 10 patients | 250 | 250 | §H-9; reuse assumption |
| Loss and breakage: 5% of a unit per episode | 125 | 125 | §B3-6 method (was ₹75) |
| Cleaning and check | 20 | 20 | §B3-6 (assumption) |
| WhatsApp | 5 | 5 | §B3-6; `FUTURE_ARCHITECTURE.md` §11 |
| Voice | 9 | 5 | same |
| AI phone calls (about 2) | 18 | 18 | same |
| AI summaries | 8 | 4 | same |
| Server share (half a patient-month) | 213 | 18 | §11 at ₹96 (was 195 and 16 at ₹88) |
| Human support (about 5 minutes) | 25 | 25 | §B3-6 (assumption) |
| **Total, ₹2,500 unit, 10 patients** | **≈ 673** | **≈ 470** | was ≈ 505 and ≈ 318 |
| Same, 20 patients per unit | ≈ 548 | ≈ 345 | was ≈ 430 and ≈ 243 |
| What-if ₹1,000 unit, 10 patients | ≈ 448 | ≈ 245 | needs quotes |
| What-if ₹600 unit, 20 patients, 2% loss, no AI calls | ≈ 300 | ≈ 119 | the §B6-5 "everything goes right" case |
| **Add if we supply the spirometer** | +146 to +1,067 | +146 to +1,067 | `05_EXPANSION…` line 19 |

### 2.3 What we keep per episode (lent, ₹2,500 unit, 10 patients, before GST)

| Price per episode | Pilot | Scale | Scale, 20 patients per unit |
|---|---|---|---|
| ₹200 | −473 | **−270** | −145 |
| ₹500 | −173 | **+30 (6%)** (was +182) | +155 |
| ₹1,000 | +327 | **+530 (53%)** (was +682) | +655 |

**Patients needed before one unit pays for itself** (unit cost ÷ (price − every other cost, including loss)): at scale **9 at ₹500** (was 5) and **4 at ₹1,000** (was 2). ₹200 never pays it back.

If 18% GST must come out of the price (a per-episode fee may be taxed as a service: `06_LEGAL…` §L-15), take about 15% off each price first.

### 2.4 Sold model: cost of one sold unit

| Line | ₹ (scale) | ₹ (pilot size) | Source |
|---|---|---|---|
| Parts | 2,500 | 2,500 | §H-9 (was 1,500) |
| Assembly and test | 150 | 150 | §B6-1 (assumption) |
| Box, printed instructions, cable | 80 | 80 | §B6-1 (assumption) |
| Warranty reserve, 5% | 137 | 137 | §B6-1 method |
| Software for one episode, pre-paid | 75 | 270 | §2.2 without device, loss and cleaning |
| **Total** | **≈ 2,940** | **≈ 3,140** | was ≈ 1,880 and ≈ 2,065 |

| Shelf price needed (incl. 5% device GST, `06_sell_vs_share.md` §B6-2) | Earlier | **Now** |
|---|---|---|
| Break even, sold direct | ≈ 1,970 | **≈ 3,090** |
| Break even, through shops at a 70% trade margin | ≈ 3,350 | **≈ 5,250** |
| Keep 30%, direct | ≈ 2,820 | **≈ 4,410** |
| Keep 30%, through shops | ≈ 4,790 | **≈ 7,500** |

For comparison, an Omron blood-pressure monitor sells for about ₹1,850–2,330 (§B6-7). **At today's unit cost, selling to families is not a business.**

### 2.5 Hospital owns the unit, pays us a per-patient software fee

Our cost per patient = messaging, voice, calls, summaries, server and support only.

| | Pilot size | Scale |
|---|---|---|
| Our cost per patient | ≈ 278 | ≈ 75 |
| Keep at ₹200 a patient | −78 | **+125 (63%)** |
| Keep at ₹500 a patient | +222 | +425 |

The hospital pays for the unit once: about ₹2,700–2,950 now (or less at volume). Over 10 patients that adds about ₹290 a patient to the hospital's cost.

### 2.6 The straight answer on ₹200

- **Device + software sold for ₹200: no.** After 5% GST, ₹200 leaves ₹190. The parts alone cost about ₹2,500. We would lose about ₹2,750 on every unit.
- **Device lent + software for ₹200 an episode: no, not now.** It costs us about ₹470 an episode at scale and about ₹670 in a pilot. It only works if the unit falls to about ₹600, lasts 20 patients, only 2% are lost and there are no AI phone calls. Then it costs about ₹119 and we keep about ₹80. None of those four things is proven.
- **Software only, ₹200 per patient, on a unit the hospital bought: yes, at scale.** We keep about ₹125. In a small pilot it loses about ₹80 a patient, because a few patients share the whole server bill.
- **What to say:** "₹200 a patient is our software price once the hospital owns the units." Never "device plus software for ₹200."

---

## 3. Monthly running costs: one hospital, 10 hospitals, 100 hospitals

**Assumptions (Est.):** one hospital = 50 episodes a month ≈ 25 patients active at any time, with about 30 units (25 + 20% spares, about ₹75,000 of units). Lent model at ₹2,500 a unit, 10 patients per unit, 5% loss. **No salaries.** Hosting at the §11 pilot tier up to about 10 hospitals; between the pilot and "multi" tiers at 100 (Est.).

| Monthly cost line (₹) | 1 hospital | 10 hospitals | 100 hospitals | Source |
|---|---|---|---|---|
| Hosting, backups, monitoring | 5,500–21,000 | 21,000–40,000 | 1,00,000–1,80,000 | §11 at ₹96 / C; Est. |
| WhatsApp, calls, voice, AI | 1,600–2,000 | 16,000–20,000 | 1,25,000–1,90,000 | §11: ₹65–80 per active patient-month (₹50–75 at volume) |
| Human support (5 min an episode) | 1,250 | 12,500 | 1,25,000 | §B3-6 assumption |
| Cleaning | 1,000 | 10,000 | 1,00,000 | §B3-6 assumption |
| Device wear and loss (lend model only) | 18,750 | 1,87,500 | 18,75,000 | §2.2: ₹375 an episode |
| Company overheads (CA, domain, stores, insurance spread monthly) | 1,100–5,400 | 2,000–5,800 | 50,000–1,50,000 | §C3, §D; Est. |
| Field visits and travel | 3,000–10,000 | 30,000–1,00,000 | 2,00,000–5,00,000 | Est. |
| **Total, lend model** | **≈ 32,000–59,000** | **≈ 2.8–3.8 lakh** | **≈ 25.8–30.2 lakh** | |
| **Total, hospital owns units (no device or cleaning lines)** | **≈ 12,000–40,000** | **≈ 0.8–1.8 lakh** | **≈ 6.0–10.5 lakh** | |
| Income at ₹500 an episode (lend) | 25,000 | 2.5 lakh | 25 lakh | |
| Income at ₹1,000 an episode (lend) | 50,000 | 5 lakh | 50 lakh | |
| Income at ₹200 a patient (software only) | 10,000 | 1 lakh | 10 lakh | |

**What this says:**
1. **One hospital never pays for itself.** The fixed costs (hosting, travel) are too large for 50 patients a month.
2. **At ₹500 an episode, the lend model loses money even at 100 hospitals** with a ₹2,500 unit. At ₹1,000 it makes money from about 10 hospitals.
3. **The device line is the elephant.** At 100 hospitals it is about ₹19 lakh a month. A ₹1,000 unit would cut it to about ₹7.5 lakh. The four volume quotes in §H-9(c) decide the business.
4. **The software-only model is thin at ₹200** until travel per hospital falls (distributors, the spirometer maker as the channel: `06_sell_vs_share.md` §B6-19).
5. Capital tied up in units under the lend model: about ₹75,000 per hospital, **about ₹75 lakh at 100 hospitals.** Grants or hospital deposits must fund this.

---

## 4. What is sourced and what is a guess

| Number | Value | Grade |
|---|---|---|
| Electronics prices (XIAO boards, sensors, motion chip) | ₹225–1,759 each | B (Evelta shop pages, `01_HARDWARE…` H10–H20) |
| Pilot unit | ₹2,300–2,500 before GST | B for ₹2,000 of it; C (repo estimate) for ₹300–500 |
| Volume unit price (1,000+) | unknown | **Quote needed** (4 quotes) |
| 1,000 mAh LiPo cell | about ₹237 | C (deal page, not BIS-confirmed) |
| Spirometer | ₹146–1,067 | B |
| Google Play fee | US$25 once | A |
| Apple fee | US$99 a year | A |
| Test licence | ₹500 a device | A |
| CDSCO study permission | ₹1,00,000 or nil | A |
| Manufacturing licence | ₹5,000 + ₹500 | A |
| WPC radio approval | ₹0 or ₹10,000 | A |
| CTRI registration | ₹0 | A |
| WhatsApp utility message | ₹0.115 | B |
| Phone calls | ₹0.38 a minute + ₹200 a month | B |
| Database plan, backup add-on | US$25 a month; from US$100 a month | B |
| Total hosting per tier | ₹21,000 / ₹1.78 lakh / ₹7.7 lakh a month | C (team estimate in §11) |
| Company incorporation | ₹7,000–25,000 | C |
| CA yearly compliance | ₹12,000–50,000 | C |
| Ethics committee fee | ₹10,000–88,500 | C (two colleges' fee lists) |
| Trademark | ₹4,500 a class | C |
| VAPT | ₹40,000–3,50,000 | C |
| Regulatory consultant | US$110–340 an hour | C (one consultancy's guide) |
| Cyber insurance | ≈ ₹50,000 a year for ₹1 crore | C (2023, not medtech) |
| Study insurance | Est. ₹25,000–1,00,000 | **Quote needed** |
| Lawyer for pilot papers | Est. ₹20,000–1,00,000 | **Quote needed** |
| Quality system and technical file | Est. ₹1–5 lakh | **Quote needed** |
| Safety and radio-interference tests | Est. ₹1–5 lakh | **Quote needed** |
| Packaging and transport tests | Est. ₹20,000–1,00,000 | **Quote needed** |
| Regulatory consultant for the licence | Est. ₹50,000–3,00,000 | **Quote needed** |
| Product liability insurance | Est. | **Quote needed** |
| Printing, translation, domain, SIM data, travel | Est. | **Quote needed** |
| Reuses per unit, loss rate, cleaning time, support time | 10 / 5% / – / 5 min | Assumptions. The pilot must measure them |

---

## 5. Cheapest honest path

### Skip or defer (saves money, costs no safety)
1. **iPhone app and the Apple fee** (₹9,500 a year + a Mac or cloud builds). Android only until a hospital asks (`02_MOBILE…` §M-25).
2. **Public store listing.** Use the managed private app or a closed test (§M-23). Play account ₹2,400 only.
3. **The full test-phone matrix** (₹70,000–1,00,000). Buy the hub model and one Xiaomi and one Samsung. Borrow the rest from friends for test days.
4. **Hub phones.** Ask the hospital to lend phones, or enrol patients who have one, and record who was excluded (that is a finding in itself).
5. **The bigger hosting tier.** A paid Supabase Pro plan and a small Mumbai server are enough for 30 patients. Add point-in-time recovery when there is more than one hospital.
6. **AI phone calls and paid voice.** WhatsApp + pre-recorded clips + the template fallback do the job. Saves about ₹1,000 in the pilot and, more importantly, about ₹18 an episode later.
7. **One unit per patient.** Reuse units with the cleaning protocol: 15 units instead of 36 saves about ₹65,000.
8. **The sniffer, speaker version, mould, VL53L4CD import, trademark, design registration, VAPT, ISO audit.** All wait until after the pilot or until the first sale.
9. **Choose a government-funded teaching hospital as sponsor.** It removes the ₹1,00,000 CDSCO fee (§L-1), and such hospitals tend to charge lower ethics fees.
10. **Free help first:** MedTech Mitra for the regulatory question; an incubator for legal templates; the college lab for meters and printers.

### Do not skip (safety and legal gates)
1. **Written regulatory view before the first patient** (MedTech Mitra or a consultant). (Gate 1 #12)
2. **Company + test licence for every unit used on patients.** (Gate 1 #10, #13)
3. **Ethics committee approval, consent forms, and CDSCO permission if the answer to #1 says so.** (Gate 1 #15, #16)
4. **Study insurance or a compensation arrangement.** (Gate 1 #21)
5. **Paid hosting in India with a tested backup** before any real patient data. (`04_GAPS…` G-46 to G-48; Gate 1 #19)
6. **BIS-marked, protected lithium cells** and a sealed case. (§L-4; §H-4)
7. **Founders' agreement with IP assignment, and the college's IP policy in writing.** Cheap now, very expensive later. (Gate 0 #1–4)
8. **20% spare units**, so a dead unit never ends a patient's programme. (G-31)
9. **The fixed red-flag message** ("contact your nurse / call 112") works with no internet and no AI. Costs ₹0, must be tested.
10. **No payments or gifts to clinicians at the pilot hospital.** (Gate 1 #22)

---

## 6. Open questions for the founder

1. **Which state is the team in?** It sets stamp duty, the state grants and which hospitals are near (travel cost).
2. **Government-funded or private hospital for the pilot?** This alone swings about ₹1–1.5 lakh (CDSCO fee + ethics fee).
3. **Do we supply the spirometer**, or does the ward already stock volume-type ones? ₹4,400–32,000 for the pilot.
4. **Reuse units between pilot patients, or one per patient?** 15 or 36 units.
5. **Will the hospital lend phones** to patients without a smartphone, or do we buy hub phones?
6. **Are any founders under 18?** A company and contracts need adult signatories (§L-14).
7. **Can the college give free lab space, a 3D printer, a microamp meter and a calibration syringe?**
8. **Has the team applied, or will it apply, to NIDHI-PRAYAS?** Its ₹10 lakh ceiling fits the middle pilot budget.
9. **Who will collect the five key quotes** (insurance broker, consultant, ethics office, lawyer, test lab) and by when?
10. **Is ₹1,000 an episode acceptable to say** in pitches as the year-1 price? At ₹500 the numbers in this file do not work with a ₹2,500 unit.

---

## Sources opened this round

**No pages were opened.** Six web searches were run. The items below were seen **only as search-result summaries (snippets, grade C)**. None of them is in `docs/research/SOURCES_LEDGER.md`. The research agent may add them.

| Search | Results seen (not opened) | Used for |
|---|---|---|
| Private limited company registration cost India 2026 | thenewsminute.com (2026 costs and timelines); agileregulatory.com (registration fees 2026); kanakkupillai.com (cost to register); taxaj.com (2026 cost guide); patronaccounting.com (cost breakdown, 2 Apr 2026); incorpx.io (registration cost) | Incorporation ₹7,000–25,000 |
| Ethics committee review fee, India | jssuni.edu.in (JSS Medical College IEC fee notification); charusat.ac.in (IEC SOP amendment 2, Jan 2022); jcdr.net (2012 editorial, ₹10,000–50,000) | Ethics fee range |
| CDSCO regulatory consultant fees | meddeviceguide.com (consulting hourly rates by region); artixio.com (CDSCO approval cost); agileregulatory.com (CDSCO fees 2026) | Consultant hourly rate |
| Private limited annual compliance packages | qwikfilings.com; patronaccounting.com; businesssetup.in; incorpx.io (annual compliance 2026); legalsuvidha.com | CA and bookkeeping ranges |
| Clinical trial insurance premium India | idfcfirstbank.com (clinical trials wording); sbigeneral.in (no-fault product page and wording); aiims.edu tenders; icmr.gov.in and nimr.icmr.org.in insurance EOIs | Confirms no published premium → quote needed |
| 3.7 V 1,000 mAh LiPo price India | dealsmagnet.com (KP 1,000 mAh 2-pack, ₹474 on Amazon, May 2026); zbotic.in (403450 cell, out of stock); robu.in (no matching single cell) | About ₹237 a cell |

Ledger and earlier-file sources used without re-opening: #7, #8, #53, #61, #107, #109, #191 (via W1), #274, #275, #281; and the source tables in `01_HARDWARE_REVIEW.md`, `02_MOBILE_APP_AND_BLUETOOTH.md`, `04_GAPS_AND_RISKS.md`, `06_LEGAL_DEEP_DIVE.md`, `03_scale_funding_unit_economics.md`, `06_sell_vs_share.md` and `FUTURE_ARCHITECTURE.md` §11.
