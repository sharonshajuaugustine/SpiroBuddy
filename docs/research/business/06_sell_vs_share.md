# Sell the device, or lend and share it? Two business models compared
**Written:** 10 Oct 2026 · **Sources opened:** 17 (15 useful, 1 failed to load, 1 had nothing) · **Confidence overall:** medium on tax, hygiene guidance and rental prices; **low** on trade margins, loss rates and anything about what a hospital will actually pay

How to read this: "S1…S17" are pages opened this round (table at the end). "#n" is a row in `docs/research/SOURCES_LEDGER.md`. "B2-…, B3-…, B4-…" are findings in the other files of this folder. **A** after a number means it is our own assumption with no source. "Snippet only" means a search-result summary that was not opened (grade C). Nothing here is legal, tax or medical advice: confirm with a regulatory consultant, a lawyer and a chartered accountant before acting.

Two models:
- **Model A, SELL:** the patient, family or hospital buys the base unit with its software and owns it.
- **Model B, LEND AND SHARE:** we (or the hospital) own the units. A patient borrows one for about 14 days. It is cleaned, checked and given to the next patient.

Out of scope here (another agent covers it): pairing, login and the technical hand-over of a device from one patient to the next.

---

## Answer in 10 lines
1. **₹200 cannot buy a sold device.** After 5% GST, ₹200 leaves about ₹190. Parts alone are ₹1,000–1,700 (team estimate). The loss is ₹800–1,500 a unit before assembly, packing or any shop margin. (B6-1, B6-4)
2. **₹200 per patient for a lent device loses money today** (our cost is about ₹318 at scale, ₹505 in a pilot: B3-6). It works only if four things all become true: unit cost near ₹500, 20 or more reuses, loss at or under 2%, and no AI phone calls. (B6-5)
3. **₹200 per patient for software only, on a unit the hospital bought, does work at scale:** software and support cost about ₹73 a patient, so we keep about ₹127. It does not work at pilot size (about ₹260 a patient, because the server bill is shared by few). (B6-6)
4. **A sold unit needs a shelf price of roughly ₹2,000 direct, and ₹2,800–4,800 through shops,** to cover cost and a normal margin. That is more than an Omron blood-pressure monitor (about ₹1,850–2,330) for something used about two weeks, sitting under a ₹200–1,000 spirometer. (B6-3, B6-7)
5. **Medical devices now carry 5% GST** (headings 9018 and 9019), from 22 Sep 2025. Glucometers and strips too. (B6-2)
6. **Indian families already rent medical equipment with a deposit:** a 5-litre oxygen concentrator is ₹4,000 for 7 days plus a ₹200 cleaning charge and a ₹15,000 refundable deposit at one Bengaluru provider. Deposits are normal and large. (B6-8)
7. **Hygiene rule:** the base unit touches hands only, so it is a "non-critical" item: clean, then wipe with 70% alcohol between patients. The spirometer and mouthpiece are single-patient and are never re-issued. (B6-10, B6-11)
8. **Lent kit does not always come back.** A US government audit found 8,300 loaned video devices unused and not retrieved; UK press figures put returned loan equipment near 57%. Our 5% loss guess in B3-6 is unproven and may be optimistic. (B6-16)
9. **Selling to patients adds duties that lending through a hospital avoids:** shop registration (MD-42) down the chain, retail pack labelling, consumer-law exposure, being the "data fiduciary" (the party legally answerable for the data), and e-waste producer registration. (B6-12 to B6-15)
10. **Recommendation:** pilot = lend, free. Years 1–2 = lend per episode at ₹500–1,000, or let the hospital buy units and pay ₹200 a patient for software. At scale = hospital-owned units plus a ₹200 software fee, with the spirometer maker as the channel. Sell direct to families only when the all-in unit cost is under about ₹650. (B6-19)

---

## Findings

### 1. Price and margin

### B6-1: The cost of one sold unit is about ₹1,900 (range ₹1,400–2,100), on team estimates
- Detail: built from repo figures; every line marked **A** is our assumption.

| Cost line for one SOLD unit (₹) | Middle case | Low-parts case | Where the number comes from |
|---|---|---|---|
| Parts | 1,500 | 1,000 | Team estimate ₹1,000–1,700 (B2-20, RESEARCH_REPORT §8.3); ₹1,500 is the figure B3-6 uses |
| Assembly and test | 150 | 150 | **A** – no quote exists (B3-2) |
| Box, printed instructions, cable | 80 | 80 | **A** |
| Warranty and returns reserve (5% of the above) | 75 | 75 | **A** – Omron gives 2 years on BP monitors (snippet only, C) |
| Software and support for one 14-day episode, pre-paid | 73 | 73 | B3-6 scale column: WhatsApp 5 + voice 5 + AI calls 18 + summaries 4 + server 16 + human support 25 |
| **Total** | **≈ 1,880** | **≈ 1,380** | |

At pilot size the software line is about ₹260, not ₹73 (server share ₹195 instead of ₹16: B3-6), so a sold unit costs about ₹2,065.
- Source: `03_scale_funding_unit_economics.md` B3-6; `02_sales_and_go_to_market.md` B2-20; RESEARCH_REPORT §4.6, §8.3 (all team estimates).
- Status: NOT CONFIRMED (a model; no supplier quote, no measured support time).
- What it means for SpiroBuddy: a one-time price must pre-pay the software. If the family keeps using the coach after 14 days, each further fortnight costs us about ₹73 with no income, unless there is a subscription.

### B6-2: GST on medical devices is 5% since 22 Sep 2025
- Detail: the 56th GST Council meeting (3 Sep 2025) recommended "Reduction of GST from 18% to 5% on various medical apparatus and devices used for medical, surgical, dental or veterinary usage". The 5% list names heading **9018** (instruments and appliances used in medical sciences, "other electro-medical apparatus") and **9019** (which includes "other therapeutic respiration apparatus"), and "Blood glucose monitoring system (Glucometer) and test strips". Goods rates changed "with effect from 22nd September 2025". The plain spirometer is listed by one seller under HSN 9019 20 90 (#138).
- Which heading our unit falls under, and what rate applies to a **per-episode fee** (a service, or a rental of goods) was **not found**. Software and services are commonly taxed at 18%; that is general knowledge, not checked this round.
- Source: S13 GST Council / PIB press release, 3 Sep 2025 – https://gstcouncil.gov.in/sites/default/files/2025-09/press_release_press_information_bureau.pdf – grade A. Ledger #138.
- Status: CONFIRMED for the 5% rate on headings 9018/9019 and the date; NOT CONFIRMED for our classification and for the fee.
- What it means for SpiroBuddy: on a sale, 5% of the shelf price goes to tax. On a per-patient fee, plan for up to 18% until a chartered accountant says otherwise. All "we keep" figures below say which rate they assume.

### B6-3: Shop and distributor margins: no "typical" figure exists; the only hard numbers are a 70% cap and a 75% proposal
- Detail: the price regulator's 2021 order capped the trade margin (the gap between the price to the distributor and the printed maximum retail price, MRP) at **70%** for pulse oximeters, BP monitors, nebulisers, digital thermometers and glucometers, after finding margins of 3% to 709% (B2-17, #255). The Indian makers' association AiMeD asked in Nov 2018 to "cap trade margins to 75% over the import landed price and Indian manufacturers ex-factory price" (S7). Whether the 2021 order is still in force was not confirmed (a secondary summary says it ran "until January 31, 2022 or until further orders", snippet only). Online marketplaces: a logistics blog lists Amazon India referral fees of 5.5% for glucometers and strips, 8.5% for thermometers, 10.5–12% for scales (undated, snippet only, C). A real dealer margin for a low-cost hospital device is still unknown (B2 open question 2).
- Source: ledger #255 (B); S7 BioVoice News, 23 Nov 2018 – https://biovoicenews.com/aimed-terms-demand-of-global-medtech-companies-on-pricing-as-misleading/ – grade B. Amazon fees – snippet only – C.
- Status: CONFIRMED for the 70% cap and the 75% proposal; NOT CONFIRMED for any typical margin.
- What it means for SpiroBuddy: the table below uses two bounds: **direct** (no middleman) and **shop chain at 70%** (the cap, so a worst case). The truth for a pharmacy sale lies between.

### B6-4: Model A table – what we keep on a sold unit
- Detail: shelf price includes 5% GST. Cost per unit ₹1,880 (B6-1). "Online" = marketplace fee 10% of price (**A**, within the 5.5–12% snippet range) plus ₹80 shipping (**A**). "Shop chain" = price to distributor is the ex-tax price ÷ 1.70.

| Buyer pays (shelf price, incl. GST) | After 5% GST | **We keep: direct sale** (hospital or own website, no fee) | **We keep: online marketplace** | **We keep: pharmacy chain at 70% trade margin** |
|---|---|---|---|---|
| ₹200 | 190 | **−1,690** | −1,790 | −1,770 |
| ₹500 | 476 | **−1,400** | −1,530 | −1,600 |
| ₹1,000 | 952 | **−930** | −1,110 | −1,320 |
| ₹1,500 | 1,429 | **−450** | −680 | −1,040 |
| ₹2,500 | 2,381 | **+500 (21%)** | +170 (7%) | −480 |

Break-even shelf price: **about ₹1,970 direct** (1,880 × 1.05) and **about ₹3,350 through shops at a 70% margin** (1,880 × 1.70 × 1.05). To keep 30% for ourselves: about **₹2,820 direct** and **₹4,790 through shops**. With ₹1,000 parts (cost ₹1,380) the direct break-even falls to about ₹1,450.
- Source: arithmetic on B6-1, B6-2, B6-3.
- Status: NOT CONFIRMED (model).
- What it means for SpiroBuddy: **(a) ₹200 for a sold device: no.** ₹190 after tax does not cover even the distance sensor, which retails at ₹399–859 (#149, snippet). A sold unit is a ₹2,000–4,800 product.

### B6-5: Model B table – what we keep per 14-day episode on a lent unit
- Detail: cost per episode from B3-6: ₹505 at pilot size (about 50 active patients), ₹318 at scale (about 5,000), both with a ₹1,500 unit reused 10 times and 5% loss. The fee is shown **before** GST, as in B3-6. The last column shows the effect if the fee the hospital pays includes 18% GST.

| Hospital or patient pays per episode | **We keep: pilot size** | **We keep: at scale** | At scale, if the price includes 18% GST |
|---|---|---|---|
| ₹200 | **−305** | **−118** | −149 |
| ₹500 | −5 | +182 (36%) | +106 |
| ₹1,000 | +495 | +682 (68%) | +530 |
| ₹1,500 | +995 | +1,182 | +953 |
| ₹2,500 | +1,995 | +2,182 | +1,801 |

**(b) ₹200 per episode for a lent device: not on today's numbers.** Of the ₹318, ₹168 is everything except the device share (B3-6). ₹200 leaves ₹32 for the device, which needs 47 reuses of a ₹1,500 unit (1,500 ÷ 32); at 5% loss a unit lasts about 20 episodes on average. **It can work only if all four hold:** unit cost about ₹500 (moulded case, thousands of units: B3-4), 20 reuses, loss 2%, no AI phone calls. Then: device 25 + cleaning 20 + WhatsApp 5 + voice 5 + summaries 4 + server 16 + support 25 + loss 10 = **about ₹110**, leaving about ₹90 of ₹200 (about ₹60 if 18% GST is inside the price).
- Source: B3-6 and the arithmetic above.
- Status: NOT CONFIRMED (model on assumptions).
- What it means for SpiroBuddy: "₹200 per patient" is a fair long-term target for a lent unit, and the wrong promise for year one.

### B6-6: Software only, on a unit the hospital bought – ₹200 a patient works at scale
- Detail: if the hospital owns, cleans and replaces the unit, our cost per patient is software and support only: about **₹73** at scale (B6-1 line 5), **₹55** without AI phone calls, and about **₹260** at pilot size.

| Hospital pays per patient (software only) | We keep at scale | We keep at pilot size |
|---|---|---|
| ₹200 before GST | **+127 (64%)** | −60 |
| ₹200 including 18% GST (₹169 net) | +96 | −91 |
| ₹500 before GST | +427 | +240 |

- **(c) ₹200 for software only: yes at scale, no for the first 50 patients.**
- Source: B3-6 cost lines.
- Status: NOT CONFIRMED (model).
- What it means for SpiroBuddy: this is the form in which the founder's "₹200" idea is honest: "the hospital owns the unit; ₹200 per patient covers the coach, the WhatsApp updates and the dashboard".

### 2. What Indian patients already pay

### B6-7: Prices of comparable home devices bought outright (2024–26 listings)
- Detail:

| Item | What a family pays | Source and grade |
|---|---|---|
| Incentive spirometer (the thing our unit sits under) | ₹200–1,000; Romsons Breazer 2500 MRP about ₹1,067 | RESEARCH_REPORT §11.4; ledger #7, #33; #32 (snippet) |
| Peak-flow meter (Cipla Breathe-o-meter) | MRP about ₹450–565 | Truemeds, 1mg, Medibuddy listings – snippet only – C |
| Pulse oximeter (Dr Trust) | MRP ₹2,500–3,140; street price ₹1,300–1,600 | PharmEasy, price trackers, Nov 2025–Jun 2026 – snippet only – C |
| BP monitor (Omron HEM-7120) | MRP ₹2,330; street ₹1,850–1,900 (Jun–Aug 2026) | Truemeds, Smartprix, Pricee – snippet only – C |
| Nebuliser (Omron NE-C101) | MRP about ₹2,300–2,430 | Truemeds – snippet only – C |
| Glucometer kit (BeatO Curv, sold with 100 strips and 100 lancets) | MRP ₹2,350, selling price ₹1,316; 1-year warranty; made in India | S8 PharmEasy listing (opened) – C |
| Glucometer strips, the repeat purchase (Accu-Chek Active, 50) | MRP ₹1,115, about ₹22 a strip | Truemeds, Cureka – snippet only – C |

- Source: S8 – https://pharmeasy.in/health-care/products/beato-curv-glucometer-kit-with-100-strips-100-lancets-type-c-usb--3136085 – grade C (retailer). Others as marked.
- Status: SINGLE SOURCE each (retail listings; prices move weekly).
- What it means for SpiroBuddy: a family's "normal" price for a home health gadget it keeps for years is ₹1,300–2,400. Ours would be used for about two weeks. The glucometer shows the "razor and blade" pattern (cheap meter, costly strips); **we have no blade**: the spirometer is the consumable and someone else sells it.

### B6-8: Rental prices and deposits for home medical equipment
- Detail:

| Item | Rent | Deposit and extras | Source and grade |
|---|---|---|---|
| Oxygen concentrator, 5 litre (RxDx, Bengaluru) | ₹4,000 for 7 days; ₹7,500 for 15 days | **₹15,000 refundable deposit**; ₹200 sanitisation; transport ₹400 one way within 5 km + ₹25/km; ID proof needed | S3 (opened) – B |
| Oxygen cylinder, 10 litre (same) | ₹2,000 for 7 days; ₹4,000 for 15 days | ₹5,000 deposit; ₹200 sanitisation | S3 – B |
| Hospital bed with rails (same) | ₹3,500 for 30 days | ₹5,000 deposit | S3 – B |
| Mattress (same) | ₹850 for 30 days | ₹2,000 deposit | S3 – B |
| Oxygen concentrator, other cities | ₹3,000–4,500 a month; ₹150 a day in Erode | deposit ₹3,500 on one listing | IndiaMART listings – snippet only – C |
| BiPAP / CPAP (breathing-support machines) | ₹3,500–12,000 a month by type | ₹1,000–5,000 on one Delhi provider; prescription asked for | listings – snippet only – C |
| BiPAP / CPAP, Apollo HomeCare | "From ₹28,000" (sale or rent not stated); set-up, repairs and "Sanitized" badge included in rentals | deposit not stated | S16 (opened) – B |
| Wheelchair (Ahmedabad dealer) | ₹600 a month | ₹4,500 deposit | listing – snippet only – C |
| Physiotherapy equipment | no published rental price found | – | NOT FOUND |

- Source: S3 RxDx – https://rxdx.in/medical-oxygen-on-rent/ – grade B (company page, footer 2026). S16 Apollo HomeCare – https://www.apollohomecare.com/medical-equipment/bipap-cpap/ – grade B.
- Status: SINGLE SOURCE for each price; the pattern (rent + deposit + cleaning charge) is CONFIRMED across several providers.
- What it means for SpiroBuddy: families are used to (1) a refundable deposit that is a large share of the item's value, (2) a separate cleaning charge, and (3) showing ID. A ₹500–1,500 deposit on our unit would be small by these standards. Rentals exist for items that cost tens of thousands of rupees; nobody rents out a ₹1,500 gadget on its own, which is why our rental has to ride inside the hospital's discharge process.

### B6-9: A working Indian "lend through hospitals" scheme: owner keeps title, partner pays deposit and a monthly fee, patients pay nothing
- Detail: OxygenForIndia (a COVID-era non-profit, delivered by HealthCubed) lends equipment on a "fully returnable basis" to hospitals, NGOs and volunteer groups. Terms: initial 2 months, extendable; **refundable deposit ₹15,000 per 5-litre concentrator**, ₹5,000 per cylinder; **₹1,000 a month per concentrator** as an "audit cost reimbursement"; patients get it free; the partner signs an agreement, stores and secures the units, and sends updates every two weeks on use, stock and condition. Page footer is 2022; current status unknown.
- Source: S5 OxygenForIndia – https://oxygenforindia.org/rural.html – grade B.
- Status: SINGLE SOURCE.
- What it means for SpiroBuddy: this is Model B with the hospital as the responsible middle party. Copy three things: the hospital (not the patient) holds the deposit, a fortnightly stock report, and units numbered and signed for.

### 3. Hygiene and reuse between patients

### B6-10: CONFIRMED – shared equipment that touches only intact skin is "non-critical" and needs cleaning plus low-level disinfection; anything touching the mouth is a higher class
- Detail: the **Spaulding classification** sorts patient-care items by what they touch.
  - US CDC: "Noncritical items are those that come in contact with intact skin but not mucous membranes." Examples: "bedpans, blood pressure cuffs, crutches and computers". "Virtually no risk has been documented for transmission of infectious agents to patients through noncritical items", and "most noncritical reusable items may be decontaminated where they are used". Semi-critical items (touching mucous membranes, such as the mouth) include "respiratory therapy and anesthesia equipment" and "minimally require high-level disinfection". (2008 guideline; page dated 28 Nov 2023; **non-Indian**.)
  - India, National Guidelines for Infection Prevention and Control in Healthcare Facilities (National Centre for Disease Control, MoHFW, Jan 2020): contact spread includes "patient-care devices that are shared between patients without cleaning and disinfection". "Non-critical equipment (e.g. blood pressure cuffs) and environmental surfaces … should be routinely cleaned and disinfected." Annex 5, "Procedures for non-critical patient-care items", gives detergent and water, then 70% alcohol "or any other LLD" (low-level disinfectant) for items such as pulse-oximeter probes, otoscope handles and stethoscopes, and "Clean between patients with detergent and water" for wheelchairs. For breathing equipment: "Disposable supplies such as nasal prongs, tubing, masks, ventilator and breathing circuits are for single patient use only", and "Respiratory therapy equipment that touches mucous membranes … should receive high-level disinfection or be sterilized."
  - The Indian guideline says nothing we could find about equipment that goes to a patient's **home** and returns (the word "home" appears only in unrelated places). It does not name the incentive spirometer.
- Source: S1 – https://cdn.who.int/media/docs/default-source/searo/india/antimicrobial-resistance/ipcguidelines-web-sep2020.pdf – grade A (text extracted and read; the Annex 5 table's columns came out jumbled, so item-by-item rows were quoted only where unambiguous). S2 CDC – https://www.cdc.gov/infection-control/hcp/disinfection-sterilization/rational-approach.html – grade A.
- Status: CONFIRMED (two primary sources agree on the classification and the cleaning level).
- What it means for SpiroBuddy: **our reading:** the base unit is non-critical (hands only). The spirometer and mouthpiece are not ours to re-issue. Confirm the classing of the base with the pilot hospital's infection-control nurse.

### B6-11: Incentive spirometers are single-patient devices; no Indian maker's instruction leaflet was found
- Detail: the US FDA device database lists the AirLife Volumetric Incentive Spirometer (4000 mL) with "For Single-Use: Yes", prescription use "Yes", over-the-counter "No", and the description "This is a single-patient device designed for use in a medical facility and in the home." (The same record's generic description also says "reusable", meaning reusable by that one patient.) A maker's manual for the TRIFLO II spirometer carries the caution that single-patient products used on more than one patient create an infection risk (snippet only; the PDF refused to open). UK NHS patient leaflets say the device is single-patient and must not be shared with family (snippets only). **Romsons' own instructions for the Breazer were not found**: retailer pages say "individually packed" and nothing about single-patient use.
- Source: S14 AccessGUDID – https://accessgudid.nlm.nih.gov/devices/10889483570814 – grade A (**US**). S17 TRIFLO II manual – https://www.medicalplus.pt/wp-content/uploads/2025/10/MAN_4717395CE_145-new.pdf – failed to open; snippet only – C.
- Status: CONFIRMED for a US product; NOT CONFIRMED for the Indian products we target.
- What it means for SpiroBuddy: under either model the patient keeps (and throws away) their own spirometer. Only the base unit is ever shared. Ask Romsons for the Breazer's printed instructions before the pilot.

**The cleaning-and-check step between patients (our proposal, built on B6-10; not a published protocol):**
1. Patient returns the base unit **without** the spirometer. Staff wear gloves.
2. Look: cracks, liquid inside, missing serial label → set aside.
3. Clean visible dirt with detergent and water on a cloth (never soak).
4. Wipe every outer surface with 70% alcohol; leave to air-dry.
5. Function check: power on, sensor reads a test height, battery or cable works.
6. Clear the previous patient's link in the software (the other agent's topic).
7. Write date, serial number, name and signature in a log; bag the unit with a "cleaned on" tag.
- **Who signs:** our reading is the ward nurse or physiotherapist who re-issues it, under a procedure approved by the hospital's infection-control committee. No source names a signatory for loaned home devices. NABH and Kayakalp (hospital quality schemes) requirements were **not checked** this round.
- **Design consequences:** smooth, sealed, wipeable case; no fabric or foam; a sensor window that survives alcohol wipes; nothing the patient's breath passes through.
- Market practice: one Indian rental firm bills a ₹200 "sanitisation" charge per rental and another advertises "Sanitized" equipment (S3, S16). B3-6 assumes ₹20 for our small unit; unverified.

### 4. Regulatory and legal differences between the models (extends file 04)

### B6-12: Selling to consumers – no prescription rule was found for low-risk devices; every seller in the chain needs registration
- Detail: we found **no Indian rule** saying a Class A or B device needs a prescription, and none saying it does not. Comparable devices (BP monitors, oximeters, glucometers, the spirometer itself) are sold on Indian pharmacy sites with no prescription step shown (S8; ledger #32, #33). In the **US**, the AirLife spirometer is flagged prescription-only (S14). A 2026 law-firm overview of Indian device rules covers classes, labelling and price control but says nothing on online sale or prescriptions (S9). Anyone who stocks or sells a device needs a Form MD-42 registration (B2-10a); consultancy pages say this includes sellers on online marketplaces (snippets only, C). The same overview says the price regulator sets ceilings only for notified devices and "Prices for non-notified devices remain market determined" (S9).
- Source: S9 Acuity Law, 20 May 2026 – https://acuitylaw.co.in/md/faqs/medical-devices-equipment-market-entry-business-establishment-in-india/ – grade B. S8, S14.
- Status: NOT CONFIRMED (absence of a rule is not proof). 
- What it means for SpiroBuddy: Model A needs our licence **plus** MD-42 at every distributor, pharmacy and online seller. Model B needs our licence and one contract with the hospital. Our reading; confirm with a regulatory consultant.

### B6-13: Pack labelling – a 2025 change makes the Medical Devices Rules the main label rule; retail packs still need the usual price declarations as far as we can tell
- Detail: a law-firm note of 28 Oct 2025 says the Legal Metrology (Packaged Commodities) Amendment Rules 2025 carve "packages containing medical devices" into the Medical Devices Rules 2017 for label declarations, and remove the fixed letter-size rules for them. It does **not** say whether the MRP and consumer-care lines are still required, and gives no notification number. Separately, packages meant for "industrial or institutional consumers" are exempt from the retail-package rules (Rule 3 of the 2011 Rules; snippet only), and a 2024 proposal to narrow that was not confirmed as final.
- Source: S6 IndiaLaw LLP – https://www.indialaw.in/blog/legal-metrology/medical-devices-exit-legal-metrology-labelling-rules/ – grade B.
- Status: SINGLE SOURCE; MRP position NOT CONFIRMED.
- What it means for SpiroBuddy: **our reading:** a unit sold in a box to a family is a retail package (MRP, maker, month and year, consumer-care contact, plus the rule 44 label in B4-5). A unit supplied to a hospital, or lent, is an institutional supply and avoids the retail declarations. Confirm with a Legal Metrology consultant before printing a box.

### B6-14: Liability and data roles shift with the model
- Detail (our reading of sources already in the ledger; nothing new opened):

| Question | Model A – sold to a patient | Model A – sold to a hospital | Model B – lent (we or the hospital own it) |
|---|---|---|---|
| Legal "manufacturer" | Us (or our loan-licence partner, B4-3) | Us | Us |
| Owner | The family | The hospital | Us, or the hospital |
| User | Patient at home, untrained | Patient, issued by a nurse | Patient, issued by a nurse |
| Who the patient can sue as a consumer | **Us directly**, and the shop. Product-liability chapter of the Consumer Protection Act 2019 (B4-18); any written warranty is an "express warranty" | The hospital for its service; us for a defect | Same as the middle column |
| Warranty and returns | We run a consumer warranty and a returns desk | One contract; repairs by exchange | No warranty to the patient; we swap faulty units |
| Data role (DPDP Act, #196) | **We are the data fiduciary**: we decide why the data is used, so notice, consent, grievance and breach duties are ours (main duties from 13 May 2027, B4-13) | Hospital is fiduciary; we are its processor (B4-16) | Same as the middle column |
| Who gives set-up help | Us, by phone, to an elderly user | Ward staff | Ward staff |

- Source: B4-13, B4-16, B4-18; ledger #122, #196, #299.
- Status: NOT CONFIRMED (our reading, not a ruling).
- What it means for SpiroBuddy: selling to patients turns a five-person student team into a consumer-electronics company with a helpline, a warranty and a privacy office. Lending through a hospital keeps one trained adult between us and the patient.

### B6-15: E-waste – "producer" duties attach to offering to sell under our own brand
- Detail: the Central Pollution Control Board's procedure for the E-Waste (Management) Rules 2022 (in force 1 Apr 2023) defines a producer as anyone who "Manufactures and offers to sell electrical and electronic equipment … under its own brand" or offers to sell assembled or imported equipment, "irrespective of the selling technique used such as dealer, retailer, e-retailer". Producers "are required to register themselves on the portal" and get recycling targets; "No entity will carry out any business without registration." A fee applies (schedule in an annexure not read). Medical devices, except implanted and infected products, are in the covered list (snippets only, C). Batteries: no duty if we use another maker's branded cells (B4-12).
- Note: this document cites the Rules as G.S.R. 801(E) of 2 Nov 2022; file 04 recorded G.S.R. 823(E) of 22 Jul 2022 from snippets. The CPCB document is the better source.
- Source: S10 CPCB SOP (Assam Pollution Control Board copy) – https://pcbassam.org/SOP_for_Producers_Ewaste_Rules_2022.pdf – grade A.
- Status: CONFIRMED for the definition and the registration duty; whether **lending without selling** makes us a producer is NOT CONFIRMED.
- What it means for SpiroBuddy: **our reading:** Model A clearly makes us a producer who must register before the first sale. Under Model B we keep title and collect every unit ourselves, which makes end-of-life simple (hand dead units to a registered recycler), but the registration question still needs the CPCB helpdesk.

### 5. Operations

### B6-16: Loaned equipment often does not come back – the only numbers found are foreign and not for our kind of device
- Detail:
  - **US, Veterans Health Administration (audit, 4 Aug 2022):** devices were issued to about 41,000 patients in the first three quarters of fiscal 2021; 51% of patients did not use them for a video visit; "nearly 8,300 unused devices" had not been retrieved (value about US$6.3 million); "a backlog of about 14,800 returned devices was pending refurbishment".
  - **UK, community equipment (press and provider figures, 2012–2019; snippets only, C):** about 2 million of 3.5 million loaned items returned (about 57%); one provider collects 77% and re-uses 91% of what it collects; one hospital trust reported 38% of crutches returned, another 10 pairs in 50.
  - **Canada, Health PEI loan agreement (undated):** kit numbered, staff sign that they gave instructions, patient signs on borrowing and on return, and "may be held financially liable … if equipment is lost or damaged as a result of misuse or tampering".
  - **India:** nothing found.
- Source: S4 VA Office of Inspector General, report 21-02668-182 – https://www.oversight.gov/report/VA/Digital-Divide-Consults-and-Devices-VA-Video-Connect-Appointments – grade A (**US**). S12 Health PEI – https://src.healthpei.ca/sites/src.healthpei.ca/files/RPM/RPM_Equipment_Loan_Agreement.pdf – grade B (**Canada**). UK figures – snippets only – C.
- Status: SINGLE SOURCE (US audit); UK figures NOT CONFIRMED; nothing Indian.
- What it means for SpiroBuddy: B3-6 assumes 5% of units lost per episode. Free loan schemes abroad lose far more. If 20% failed to return, a ₹1,500 unit would last 5 episodes, the device cost alone would be ₹300 an episode and the scale cost about ₹393 (93 of non-device, non-loss cost + 300) instead of ₹318. **Return rate is the number the pilot must measure.** Three cheap protections: tie the return to the follow-up visit, have the hospital hold a deposit, and remind by WhatsApp on day 12.

### B6-17: What each model needs day to day (team reasoning)

| Task | Model A – sell to families | Model B – lend through a hospital |
|---|---|---|
| Stock | Finished, boxed stock at shops or a warehouse; cash tied up before sale | A pool of units per ward: about 1 unit per 1.5–2 patients a month (B2-25) plus spares |
| Delivery | Courier to homes (₹80 **A**) or pharmacy shelf | Handed over at discharge; nothing to ship |
| Set-up for an elderly user | Phone or video help from us; the costliest unknown | Nurse or physiotherapist shows it before discharge (about 5 minutes) |
| Phone support | Consumer helpline in several languages | Hospital first, us second |
| Repairs | Warranty returns by courier | Swap from the spare pool |
| Returns | Refund policy; used units cannot be resold as new | Every unit returns; this is the model |
| Loss and deposits | Not our problem after sale | Our main risk: deposit held by hospital, log by serial number |
| Cleaning and refurbishing | None | Seven-step check each cycle (B6-11); new label, cable or battery when worn |
| End of life | Family disposes; we fund recycling as "producer" (B6-15) | We collect and recycle |
| Money in | Once, up front | Small, repeated; hospital may pay late (B2-4) |
| Data we see | Only if the family opts in | Through the hospital, under contract |

- Source: team reasoning on B2-25, B3-6 and the findings above.
- Status: NOT CONFIRMED.
- What it means for SpiroBuddy: Model A's hard part is people (set-up, helpline, warranty). Model B's hard part is logistics (getting units back clean). A small team can borrow the hospital's people; it cannot borrow a helpline.

### 6. Who chooses which model, and why

### B6-18: Six real examples

| Company or scheme | Model | What they charge | Why it made sense | Source |
|---|---|---|---|---|
| Omron BP monitor (India) | Sell outright, pharmacies and online | About ₹1,850–2,330; 2-year warranty | Used daily for years; one owner; mass volume | snippets – C |
| BeatO (India) | Cheap device, money from repeat sales and a care plan | Kit ₹1,316 with 100 strips (MRP ₹2,350); priced "from Rs 499 to Rs 1499" in older coverage; company profiles describe subscription and product revenue | Diabetes is lifelong, so strips and coaching repeat for years | S8 (opened); profiles – snippets – C |
| Dozee (India) | Began selling to consumers, became a hospital business | Consumer device launched Jul 2019 at ₹8,000; hospitals paid a "yearly subscription fee of INR 10,000" for the dashboard (2020); a 2021 rental of ₹3,999 for 30 days / ₹2,999 for 15 days (snippet) | "Hospitals and nursing homes" became its biggest customers; hospital price today is not public (file 02, answer line 8) | S11 KrASIA, 21 Sep 2020 – B |
| RxDx, Apollo HomeCare (India) | Rent with deposit | Concentrator ₹4,000 a week + ₹15,000 deposit (B6-8) | Costly machine, short need, family can't judge quality | S3, S16 |
| OxygenForIndia (India) | Owner lends through hospitals and NGOs; patients free | Partner pays ₹15,000 deposit + ₹1,000 a month per unit (B6-9) | Donor-funded stock, hospital carries responsibility | S5 |
| US Veterans Health Administration | Health system lends devices free | Nil to patient | Access for poor patients; but half went unused and thousands were not retrieved (B6-16) | S4 (**US**) |

Also in earlier files: Niramai (hospital buys hardware, then pays per screening: B2-15); Tricog and Qure.ai (pay per use: B2-13, B2-14); InSee, the closest US product, is offered to hospitals with a free trial and no public price (#102).
- Status: SINGLE SOURCE each.
- What it means for SpiroBuddy: outright sale wins when the need is lifelong and the buyer is the user. Short, one-off needs are rented or lent. A two-week recovery after surgery is the second kind.

### 7. Hybrid options

| Hybrid | How it works | Arithmetic (team estimates) | Good for | Weak point |
|---|---|---|---|---|
| **H1. Hospital buys units, pays per patient for software** | Unit sold as ward equipment at about ₹2,500 + 5% GST; ₹200 a patient for coach, WhatsApp, dashboard | Unit: 2,500 − 1,805 cost = **+₹695**. Software: 200 − 73 = **+₹127** a patient at scale. Hospital's cost over 20 patients: 2,625 ÷ 20 + 200 = **₹331 a patient**; over 10 patients ₹462 | Private hospitals that prefer owning; us (cash up front, no loss risk) | Needs a purchase approval (B2-19); loses at pilot size |
| H2. Rent-to-own | Per-episode fee; after N paid episodes the unit is the hospital's | At ₹500, the unit's cost is covered after about 5 episodes (B3-6) | Hospitals unsure about buying | Contract complexity |
| H3. Deposit refunded on return | Patient or hospital leaves ₹500–1,500; refunded when the unit comes back clean | A deposit equal to the unit cost removes the loss line (₹75 in B3-6) | Any lending model | A barrier for poor patients; not suitable inside a research pilot without ethics approval |
| H4. CSR-funded units + software subscription | A donor buys the units for a government hospital; a small yearly software fee follows | Same as H1 with the donor paying the unit | Government hospitals (B2-12, B2-18) | Donor cycles; fee must survive after year one |
| H5. Spirometer maker bundles the base | Romsons-type partner sells or lends the base with its spirometer through 1,500+ distributors (B2-21) | We earn a licence fee or ₹200 software fee per activation | Scale without our own sales force | No contact made; they hold the customer |

Status of this table: NOT CONFIRMED (team reasoning).

### 8. Recommendation

### B6-19: Which model, when, and what would make us switch

| Stage | Model | Price | Who owns the unit | Switch when… |
|---|---|---|---|---|
| **Pilot (0–12 months, unlicensed prototype)** | **B – lend, free**, inside an ethics-approved study (no sale is lawful yet: B4) | ₹0 | Us | — Measure: share of units returned, cleaning minutes, reuses per unit, support minutes per patient |
| **Year 1–2 (after the licence)** | **B per episode** for private hospitals; **H1** for a hospital that would rather own; **H4** for government hospitals | ₹500–1,000 an episode, or ₹2,500 a unit + ₹200 a patient | Us, the hospital, or the donor | Move a site from B to H1 if non-return there is above 10% per episode, or if our money tied up in lent units exceeds what we can fund from grants |
| **Scale (thousands of patients a year)** | **H1 as the default**, sold through the spirometer maker or distributors (H5); software ₹200 a patient | ₹200 a patient software; unit at cost-plus | Hospital or distributor | Offer **₹200 lend-and-share** only when unit cost ≤ ₹500, loss ≤ 2% and reuses ≥ 20 (B6-5) |
| **Direct sale to families (Model A)** | Add-on only, not the core | MRP about ₹1,499 | Family | Only when all-in unit cost is under about ₹650 (an MRP of ₹1,499 gives ₹840 to us after 5% GST and a 70% trade margin), a long-term use exists (lung rehabilitation after TB or for chronic lung disease, B1), and we can staff a helpline |

- Source: all findings above.
- Status: NOT CONFIRMED (a recommendation built on a model).
- What it means for SpiroBuddy: keep the pitch line from file 02 ("we lend the unit and charge per patient") and add the honest ₹200 line: "₹200 a patient is our software price once hospitals own the units."

---

## What to say in the 5-minute pitch (5 bullets max, each with its source)
- "A patient needs this for two weeks, so we lend it, like the oxygen concentrators Indian families already rent with a deposit." (B6-8, RxDx Bengaluru price list)
- "The base never touches breath. It is cleaned like a blood-pressure cuff, with a 70% alcohol wipe, under India's 2020 national infection-control guidelines. The spirometer stays with its one patient." (B6-10)
- "Our long-term price is ₹200 a patient for the software, once the hospital owns the units. Our own estimate of the software cost is about ₹73." (B6-6)
- "We do not claim ₹200 buys the device. Parts alone are ₹1,000–1,700 today." (B6-1, team estimate)
- "Medical devices carry 5% GST since 22 September 2025." (B6-2, GST Council press release)

## What NOT to say (claims that would be wrong or unproven)
- "Device plus software for ₹200." Wrong for a sold unit, and a loss for a lent one on today's numbers.
- "Units are reused 10 or 20 times" or "only 5% are lost" as facts. They are assumptions; foreign loan schemes do much worse.
- "Dealer margins are X%." No typical figure exists; 70% is a legal cap on five other devices, not a norm.
- "No prescription is needed" or "it can be sold online like a BP monitor." Not confirmed.
- "The spirometer can be shared after cleaning." It is a single-patient device.
- "Our cleaning procedure is approved" or "meets NABH." No hospital has seen it.
- "GST on our fee is 5%." Only the goods rate is confirmed.
- "Hospitals will pay ₹2,500 for a unit." Nobody has been asked.

## First 90 days: concrete next steps (who does what, rough cost in ₹ where a source gives one)
1. **Team lead:** in every hospital interview ask three questions: would you rather own the units or borrow them; what would you pay per patient; who would clean and sign for returned units. Cost nil.
2. **Hardware lead:** design the case to be wiped: sealed, smooth, no fabric; test 50 wipes with 70% alcohol on the case and the sensor window. Cost: a bottle of isopropyl alcohol.
3. **Clinical contact:** show the seven-step cleaning sheet (B6-11) to one infection-control nurse; get it corrected and signed as a draft. Cost nil.
4. **Team lead:** ask Romsons for the Breazer's printed instructions (single-patient wording). Cost nil.
5. **Business lead:** one chartered-accountant question: GST rate on a per-episode fee and on a software-only fee, and the HSN code for the unit. Cost not sourced.
6. **Business lead:** one question to the CPCB e-waste helpdesk: does lending without selling make us a "producer"? Cost nil.
7. **Pilot protocol (with file 05's steps):** record for every unit: date out, date back, days late, condition, cleaning minutes. These five numbers replace the assumptions in B3-6.
8. **Business lead:** ask two surgical-goods distributors for their real margin on a ₹2,500 hospital item. Cost nil.

## Open questions (what you could not find, and who could answer it)
- Real return rate, cleaning time and reuse count for a lent unit. → The pilot.
- Would a hospital buy units at about ₹2,500, or pay ₹200–1,000 a patient? → Interviews.
- Typical distributor and pharmacy margins on a low-cost device; whether the 2021 trade-margin order still runs. → Two distributors; the NPPA site.
- Is a prescription needed to sell a Class A or B device to a consumer, and are there marketplace rules for devices? → Regulatory consultant; CDSCO.
- Does a retail pack of a medical device still need MRP and consumer-care lines after the 2025 change; is hospital supply "institutional"? → Legal Metrology consultant; the gazette text.
- GST rate on the per-episode fee; HSN code of the base unit. → Chartered accountant.
- Does lending (no sale) trigger e-waste producer registration; the fee. → CPCB helpdesk.
- Romsons' and other Indian makers' instructions on single-patient use. → The makers.
- NABH and Kayakalp wording on shared and loaned equipment; any hospital rule for devices returning from a patient's home. → A hospital quality manager or infection-control nurse.
- Whether a hospital may lawfully take a deposit from a patient for loaned equipment, and under a research study. → Hospital administrator; the ethics committee.
- Current Dozee, BeatO and home-monitoring prices. → Company sales teams.

## Sources opened this round
| # | URL | title | publisher | grade | used in |
|---|---|---|---|---|---|
| S1 | https://cdn.who.int/media/docs/default-source/searo/india/antimicrobial-resistance/ipcguidelines-web-sep2020.pdf | National Guidelines for Infection Prevention and Control in Healthcare Facilities (Jan 2020; text extracted and read) | NCDC / MoHFW, hosted by WHO India | A | B6-10 |
| S2 | https://www.cdc.gov/infection-control/hcp/disinfection-sterilization/rational-approach.html | A Rational Approach to Disinfection and Sterilization (2008 guideline; page 28 Nov 2023) | US CDC | A | B6-10 |
| S3 | https://rxdx.in/medical-oxygen-on-rent/ | Medical oxygen and equipment on rent: price table (footer 2026) | RxDx Healthcare, Bengaluru | B | B6-8, B6-18 |
| S4 | https://www.oversight.gov/report/VA/Digital-Divide-Consults-and-Devices-VA-Video-Connect-Appointments | Digital Divide Consults and Devices for VA Video Connect Appointments, report 21-02668-182 (4 Aug 2022) | US VA Office of Inspector General | A | B6-16, B6-18 |
| S5 | https://oxygenforindia.org/rural.html | OxygenForIndia: equipment lending terms for partners (footer 2022) | OxygenForIndia | B | B6-9, B6-18 |
| S6 | https://www.indialaw.in/blog/legal-metrology/medical-devices-exit-legal-metrology-labelling-rules/ | Medical devices step out of Legal Metrology (Packaged Commodities) shadow (28 Oct 2025) | IndiaLaw LLP | B | B6-13 |
| S7 | https://biovoicenews.com/aimed-terms-demand-of-global-medtech-companies-on-pricing-as-misleading/ | AiMeD on trade-margin caps (23 Nov 2018) | BioVoice News | B | B6-3 |
| S8 | https://pharmeasy.in/health-care/products/beato-curv-glucometer-kit-with-100-strips-100-lancets-type-c-usb--3136085 | BeatO Curv glucometer kit listing | PharmEasy (retailer) | C | B6-7, B6-12, B6-18 |
| S9 | https://acuitylaw.co.in/md/faqs/medical-devices-equipment-market-entry-business-establishment-in-india/ | Medical devices and equipment: market entry in India (20 May 2026) | Acuity Law | B | B6-12 |
| S10 | https://pcbassam.org/SOP_for_Producers_Ewaste_Rules_2022.pdf | SOP for grant of registration to Producers under E-Waste (Management) Rules 2022 (text extracted) | CPCB, copy on Assam Pollution Control Board site | A | B6-15 |
| S11 | https://kr-asia.com/dozee-detects-early-signs-of-deteriorating-health-startup-stories | Dozee detects early signs of deteriorating health (21 Sep 2020) | KrASIA | B | B6-18 |
| S12 | https://src.healthpei.ca/sites/src.healthpei.ca/files/RPM/RPM_Equipment_Loan_Agreement.pdf | Remote Patient Monitoring Equipment Loan Agreement (undated; text extracted) | Health PEI, Canada | B | B6-16 |
| S13 | https://gstcouncil.gov.in/sites/default/files/2025-09/press_release_press_information_bureau.pdf | Recommendations of the 56th GST Council meeting (3 Sep 2025; text extracted) | GST Council / PIB | A | B6-2 |
| S14 | https://accessgudid.nlm.nih.gov/devices/10889483570814 | AirLife Volumetric Incentive Spirometer, device record | US FDA / NLM AccessGUDID | A | B6-11, B6-12 |
| S15 | https://alspl.com/?p=1412 | Company home page (no spirometer text) | Advanced LifeSciences, New Delhi | – | nothing useful |
| S16 | https://www.apollohomecare.com/medical-equipment/bipap-cpap/ | BiPAP / CPAP equipment | Apollo HomeCare | B | B6-8, B6-18 |
| S17 | https://www.medicalplus.pt/wp-content/uploads/2025/10/MAN_4717395CE_145-new.pdf | TRIFLO II incentive spirometer manual | hosted by a Portuguese reseller | – | failed to open (connection refused); snippet used in B6-11, grade C |

**Search snippets only, NOT opened (grade C as used):** IndiaMART and other listings for oxygen concentrator, BiPAP/CPAP, hospital bed and wheelchair rental; Truemeds, 1mg, Medibuddy, Smartprix, Pricee, price-history.in listings (Omron HEM-7120, Omron NE-C101, Dr Trust oximeter, Cipla Breathe-o-meter, Accu-Chek strips); Omron warranty table; BeatO company profiles (Dealroom, YourStory 2019); fitgap and 1mg pages on Dozee home pricing; Shiprocket blog on Amazon India referral fees and Amazon's March 2026 fee announcement; Nishith Desai 2021 wrap on the NPPA trade-margin order; registerkaro, agileregulatory, corpbiz on MD-42 for online sellers; lakshmisri and ssrana on institutional consumers under Legal Metrology; amsshardul, ssrana, greensutra on E-Waste Rules Schedule I; kauveryhospital, taxguru, terra-insight on GST; NHS patient leaflets on single-patient spirometers; thiis.co.uk, onthewight.com and other UK reports on equipment return rates; myprivia and prevounce device-return policies; MSF catalogue entry for incentive spirometers.

None of the opened URLs was in `docs/research/SOURCES_LEDGER.md` before this round (rows 1–321 checked). This agent did not edit the ledger: the lead should add S1–S17 as rows 322–338.
