# Scaling, unit economics and start-up money
**Written:** 10 Oct 2026 · **Sources opened:** 17 (4 of them gave little or nothing; 2 more attempts failed) · **Confidence overall:** medium for grant rules, low for manufacturing prices and investor cheque sizes

How to read this: "S1…S17" are pages opened this round (table at the end). "Snippet only" means a search-result summary that was not opened; it is grade C. "#n" is a row in `docs/research/SOURCES_LEDGER.md`. "Team estimate" means our own number with no source. Nothing here is legal, tax or investment advice; confirm with a chartered accountant, a lawyer and a regulatory consultant before acting.

## Answer in 10 lines
1. **Best first money for a team with no company: NIDHI-PRAYAS** (Department of Science and Technology). Up to ₹10 lakh grant, an individual aged 18+ can apply, the product must be physical, students need a no-objection letter from college. Our base unit qualifies; "app-only" projects do not. (S17)
2. **If the team is based in Kerala: KSUM Idea Grant**, up to ₹3 lakh. You can apply without a company; you must register one before money is released. (S7)
3. **Biggest early grant: BIRAC BIG**, up to ₹50 lakh for 18 months, calls on 1 January and 1 July each year, open about 45 days. The last call found closed 30 Nov 2025. The next expected opening is 1 Jan 2027. (S1, S16)
4. **Order matters.** The Startup India Seed Fund refuses startups that already took more than ₹10 lakh from other government schemes. Taking BIG first may shut that door. (S8)
5. **Per patient episode the device is not the main cost at pilot size; the server bill is.** At 50 patients our cost is about ₹500 an episode. At 5,000 patients it falls to about ₹240–320. (repo figures plus our assumptions)
6. **₹300 an episode loses money or barely breaks even. ₹500 works at scale. ₹1,000 works even in a small pilot.**
7. **Break-even reuses (at 5,000 patients, ₹1,500 device):** 12 at ₹300, 5 at ₹500, 2 at ₹1,000.
8. **Making it:** 10 units by hand; 100 with 3D-printed cases and a small PCB batch; 1,000 with machine-assembled boards; 10,000 with a moulded case. A simple mould in India is roughly ₹3–7 lakh (vendor guide) and only pays back above about a thousand units.
9. **Investors come late in medtech.** Dozee was founded in 2015; its first round on Inc42's tracker is September 2020. Expect grants to carry the first 18–24 months.
10. **A company is needed sooner than it seems:** almost every scheme after the first two needs a private limited company or LLP, and most need DPIIT recognition (the Government's "recognised startup" label).

## Findings

### B3-1: The four production steps, and what changes at each
- Detail (team reasoning, with sourced price points in B3-2 to B3-5):

| Units | How it is made | What changes | Main cost drivers |
|---|---|---|---|
| 10 | Hand-built: bought sensor module + dev board, jumper wires or hand-soldered, 3D-printed stand | Nothing new; this is HARDWARE.md | Retail module prices; our own time |
| 100 | Custom 2-layer PCB, hand or small-batch assembly, 3D-printed case from a print service | First board design; first test jig; first written build steps | PCB setup fee; print cost per gram; rework |
| 1,000 | Machine-assembled boards (PCBA), sensor chip bought in reels not modules, case still printed or from a low-cost mould | A contract manufacturer; incoming inspection; batch records; (for a regulated device) a licensed site and quality system | Component price breaks; assembly setup; test time per unit |
| 10,000 | Injection-moulded case, turnkey contract manufacturer | Mould tooling paid up front; design frozen; safety and radio testing done | Tooling; minimum order quantities; working capital for stock |

- Source: team reasoning from `docs/HARDWARE.md` §1 and the price points below.
- Status: NOT CONFIRMED (no quotes obtained).
- What it means for SpiroBuddy: do not design for moulding yet. The geometry is still unverified (RESEARCH_REPORT §4.7), so anything beyond step 2 is premature.

### B3-2: Indian PCB fabrication has public entry prices; assembly prices are quote-only
- Detail: Lion Circuits (Bengaluru phone code) advertises "5 Boards for Just ₹799, in 5-6 Days" and offers assembly, component sourcing and contract manufacturing, with an instant quote tool. No assembly price is published. PCB Power (Gujarat) also has an online quote tool (snippet only). A retailer's guide gives Indian assembly at a ₹3,000–15,000 one-time setup fee plus ₹200–2,000 a board, and ₹500–1,500 per assembled board for a 20–30 part board at 5–10 pieces (snippet only; the page refused to open).
- Source: S12 Lion Circuits home page – https://lioncircuits.com/ – grade B (vendor's own page, marketing price). Zbotic guide – snippet only – grade C.
- Status: SINGLE SOURCE for the ₹799 figure; NOT CONFIRMED for assembly ranges.
- What it means for SpiroBuddy: a 100-unit board run is a few thousand rupees of fabrication plus setup. The real price needs our own board file uploaded to two vendors.

### B3-3: 3D-printing services in India quote roughly ₹3–8 a gram for PLA plastic
- Detail: marketplace listings range ₹1–10 a gram for FDM printing (the common melted-plastic method); one vendor guide gives ₹3–8 a gram for PLA and ₹5–12 for PETG; 3Ding (Hyderabad) about ₹3–5 a gram. Setup or minimum-order fees are often extra. Year: 2025–26 listings.
- Source: search results (IndiaMART listings, Zbotic guide, 3Ding) – snippet only – grade C.
- Status: NOT CONFIRMED.
- What it means for SpiroBuddy: a base stand of 100–200 g (team estimate; the weight is not designed yet) would cost about ₹300–1,600 printed outside. Buying one printer may be cheaper for 100 units. This is the reason the Plan's "under ₹1,000" target needs moulding.

### B3-4: A simple single-cavity injection mould in India is about US$3,500–8,000
- Detail: Zetwerk's guide (undated, page footer 2026) gives single-cavity tooling in India as US$3,500–8,000 for a simple two-plate tool, US$10,000–25,000 for medium complexity with slides, US$28,000–80,000 for complex tools. At the repo's ₹88 = US$1 that is about ₹3–7 lakh, ₹9–22 lakh and ₹25–70 lakh. Marketplace listings show cheaper mild-steel tools at ₹80,000–2 lakh (snippet only). No per-part price, lead time or prototype-tool price was given.
- Source: S6 Zetwerk – https://www.zetwerk.com/blog/injection-moulding-in-india-complete-guide-to-plastic-part-manufacturing-and-sourcing/ – grade C (vendor marketing). ExportersIndia / IndiaMART listings – snippet only – grade C.
- Status: SINGLE SOURCE.
- What it means for SpiroBuddy: tooling of ₹3–7 lakh spread over 1,000 units adds ₹300–700 a unit; over 10,000 units, ₹30–70. Moulding is a 10,000-unit decision, or a late 1,000-unit one.

### B3-5: Medical device parks exist; AMTZ lists the shared labs a small team needs, with no public prices
- Detail: Andhra Pradesh MedTech Zone (AMTZ, Visakhapatnam) lists a 3D-printing centre (ADDIT), an EMI-EMC and electrical-safety test centre (ELECTRA; these are the tests that show a device does not interfere with other equipment and is electrically safe), an electronics and sensor centre (SILICO), wireless testing (DECIBLE) and a medtech incubator (MEDI VALLEY). No fees are published; contact is info@amtz.in. Telangana's Medical Devices Park at Sultanpur was launched in 2017 and reported 50 companies by Dec 2021 (snippet only). Tamil Nadu's park at Oragadam was approved in 2021 (snippet only). Kerala's MedSpark at the Life Science Park, Thonnakkal (Sree Chitra institute with KSIDC) was announced in 2020 with a testing centre and an incubator planned; its current status was not confirmed (snippet only).
- Source: S13 AMTZ – https://amtz.in/our-centers – grade B. Park news – snippets only – grade C.
- Status: CONFIRMED that the AMTZ centres are listed; NOT CONFIRMED for prices, and for MedSpark being open.
- What it means for SpiroBuddy: parks matter at the 1,000+ stage (testing and a licensed site). No electronics contract manufacturer with a published "small medical batch" price was found.

### B3-6: Unit economics per 14-day patient episode
- Detail: built from repo figures; every input marked A is an assumption of ours.

| Cost line (₹ per episode) | Pilot, ~50 active patients | Scale, ~5,000 active patients | Where the number comes from |
|---|---|---|---|
| Device share: ₹1,500 unit ÷ 10 reuses | 150 | 150 | Unit cost ₹1,000–2,600 is a team estimate (RESEARCH_REPORT §4.6); ₹1,500 and 10 reuses are **A** |
| Cleaning and checks between patients | 20 | 20 | **A** – no source found |
| Patient's own spirometer | 0 | 0 | Hospital or patient already buys it (₹200–1,000, RESEARCH_REPORT §11.4). If we supply it, add that amount |
| WhatsApp | 5 | 5 | RESEARCH_REPORT §8.3 |
| Voice (text to speech) | 9 | 5 | Half of the monthly ₹0–18 / ₹0–10 in FUTURE_ARCHITECTURE §11 |
| AI phone calls (about 2) | 18 | 18 | Half of ₹36 a month, same table; ≈ ₹8 a call (§8.3) |
| AI summaries | 8 | 4 | Half of ₹17 / ₹1–17 a month, same table |
| Server share | 195 | 16 | Half of ₹390 / ₹33 fixed per patient-month, same table |
| Human support (about 5 minutes) | 25 | 25 | **A** |
| Loss and breakage: 5% of units per episode | 75 | 75 | **A** – no return-rate data exists for a lent device like this |
| **Total cost** | **≈ 505** | **≈ 318** | |
| **Same, with 20 reuses** | **≈ 430** | **≈ 243** | |

Contribution margin (price minus the cost above; no salaries, regulatory or sales costs):

| Price per episode | Pilot, 10 reuses | Scale, 10 reuses | Scale, 20 reuses |
|---|---|---|---|
| ₹300 | −₹205 (loss) | −₹18 (loss) | +₹57 (19%) |
| ₹500 | −₹5 (about zero) | +₹182 (36%) | +₹257 (51%) |
| ₹1,000 | +₹495 (50%) | +₹682 (68%) | +₹757 (76%) |

Break-even reuses for a ₹1,500 device (reuses needed before one unit has paid for itself): at scale the non-device cost is ₹168, so **12 reuses at ₹300, 5 at ₹500, 2 at ₹1,000**. At pilot size the non-device cost is ₹355, so ₹300 **never** breaks even, ₹500 needs 11 reuses, ₹1,000 needs 3.

- Source: `docs/research/RESEARCH_REPORT.md` §4.6, §8.3; `docs/FUTURE_ARCHITECTURE.md` §11 (all repo figures are themselves estimates).
- Status: NOT CONFIRMED (a model, not measured).
- What it means for SpiroBuddy: price the pilot at ₹1,000 or run it free on grant money; do not promise ₹300. The two numbers that decide everything are the loss rate and how many patients share the server bill, and neither is known. A 5% loss rate also means a unit survives about 20 episodes on average, so "20 reuses" is a ceiling, not a base case.

### B3-7: NIDHI-PRAYAS – up to ₹10 lakh for a physical prototype, open to individuals
- Detail: run by the Department of Science and Technology through host incubators called PRAYAS Centres. As published by the HTIC MedTech Incubator at IIT Madras: grant up to ₹10 lakh, 18 months; an individual innovator who is an Indian citizen aged 18+ may apply without a company; a team names one lead innovator who receives the funds; students and employees need a no-objection certificate (NOC); a startup applicant must be at most 7 years old with turnover not above ₹25 lakh. Not eligible: pure software or app-only projects, and products past prototype stage. The grantee must join that incubator's pre-incubation or incubation programme and return unused money. That page's deadline is from June 2023; no current call date was found. The official page says "NIDHI PRAYAS 2.0 Program Guidelines", last updated 20 May 2026, but the guideline text could not be read.
- Source: S17 HTIC MedTech Incubator – https://htic.iitm.ac.in/mti/?p=1789 – grade B. S2 DST NIDHI – https://nidhi.dst.gov.in/nidhi-prayas/ – grade A (page gave only the title and date).
- Status: CONFIRMED for the rules (incubator page plus matching summaries from several other centres, snippets); NOT CONFIRMED for current dates and for any change in "2.0".
- What it means for SpiroBuddy: best fit. Pitch the **base unit**, not the app. First step: email two or three PRAYAS Centres and ask when their next call opens.

### B3-8: Kerala Startup Mission (KSUM) – Idea Grant ₹3 lakh without a company, then ₹7 lakh and ₹15 lakh with one
- Detail: Idea Grant: up to ₹3 lakh for prototype, testing and validation; "Innovators based out of Kerala can apply"; technology products only; company registration (private limited, LLP or one-person company) and a KSUM Unique ID are "mandatory only before fund disbursal"; about 50% is paid first, the rest after a progress review; re-apply after 3 months if rejected. Productisation Grant: up to ₹7 lakh (₹12 lakh if women hold the major share); needs an incorporated company and KSUM ID at application; the startup brings 20% margin money; an Idea Grant winner can claim only the ₹4 lakh balance. Scaleup Grant: up to ₹15 lakh, needs ₹10 lakh revenue in 6 months or ₹30 lakh equity raised, 50% margin money (snippet only). No call dates are published on either page.
- Source: S7 – https://startupmission.kerala.gov.in/schemes/idea-grant – grade A. S15 – https://startupmission.kerala.gov.in/schemes/productisation-grant – grade A.
- Status: CONFIRMED for amounts and rules; dates NOT CONFIRMED. Whether a separate student Idea Grant is open now is NOT CONFIRMED (an aggregator shows it closed).
- What it means for SpiroBuddy: only useful if the team is in Kerala. **We do not know from the repo which state the team is in.**

### B3-9: BIRAC BIG – up to ₹50 lakh, twice a year
- Detail: BIRAC is the Department of Biotechnology's funding arm. BIG "provides early-stage funding support of INR 50 Lakhs as grant-in-aid for a period of 18 months". Calls are announced on 1 January and 1 July and stay open about 45 days. The page was updated 1 Oct 2026 and shows no open call. The last call found is Call 25, closed 30 Nov 2025 (which did not follow the 1 January / 1 July pattern, so the pattern is a guide only). BIG partners such as Venture Center, Pune give free help with the application and discounted incubation. Eligibility, from older BIRAC guideline PDFs seen only as search summaries: an Indian-citizen individual may apply but must be incubated; a company or LLP must be at least 51% Indian-owned and young (3 or 5 years, versions differ); proprietorships are not eligible. The newest guideline (November 2025) could not be read.
- Source: S1 BIRAC – https://birac.nic.in/desc_new.php?id=83 – grade A. S16 Venture Center – https://www.venturecenter.co.in/big/ – grade B. BIRAC guideline PDFs – snippet only – grade C (S9 was opened but unreadable).
- Status: CONFIRMED for amount, duration and call pattern; SINGLE SOURCE (snippets) for the individual route; no 2026–27 call date found.
- What it means for SpiroBuddy: realistic at the 3–12 month stage, once there is a working device and a hospital letter. It is a competitive national grant aimed at people who will work on it full time; a student team should expect to need a mentor institution.

### B3-10: Startup India Seed Fund – ₹20 lakh grant, but only for a recognised company, and with a ₹10 lakh trap
- Detail: the DPIIT guidelines say the startup must be DPIIT-recognised and "incorporated not more than 2 years ago", use technology in its core product, have at least 51% Indian promoter shareholding, and must "not have received more than Rs 10 lakh of monetary support under any other Central or State Government scheme" (prizes and lab access do not count). Money: "Up to Rs. 20 Lakhs as grant" for proof of concept, prototype or product trials, plus up to ₹50 lakh as convertible debentures or debt for market entry. Paid through incubators; a startup applies to up to three incubators on the Startup India portal. The scheme was written for 2021–25 with a ₹945 crore corpus (snippet); whether it is still taking applications in late 2026 was **not confirmed** (the portal page did not load).
- Source: S8 DPIIT guidelines – https://www.startupindia.gov.in/content/dam/invest-india/Templates/public/Guidelines%20for%20Startup%20India%20Seed%20Fund%20Scheme.pdf – grade A.
- Status: CONFIRMED for the rules; current status NOT CONFIRMED.
- What it means for SpiroBuddy: NIDHI-PRAYAS (₹10 lakh) keeps this door open; BIG (₹50 lakh) would appear to close it. Plan the order with an incubator.

### B3-11: Other schemes, sorted by fit for a team with no company
- Detail:

| Scheme | Who runs it | Amount | Who can apply | Notes and status |
|---|---|---|---|---|
| MeitY TIDE 2.0 EiR | Electronics and IT ministry, via host incubators | ₹4 lakh for a year (snippet) | Individuals or teams with an ICT idea (snippet) | Many listings closed; ask the host incubator. NOT CONFIRMED |
| MeitY GENESIS EiR | Same | Up to ₹10 lakh (snippet, from host incubator pages) | Individual, full-time UG/PG student, or DPIIT startup under 2 years; **Tier II and III cities only**; must be incubated | NOT CONFIRMED |
| BIRAC SITARE-GYTI | BIRAC with SRISTI | Up to ₹15 lakh, 15 projects a year (snippet) | Students in a Masters or PhD course, with NOC | Call usually Aug–Sep (snippet). The government scheme page failed to load. NOT CONFIRMED |
| BIRAC E-YUVA | BIRAC | Fellowship; amount not confirmed | Undergraduate teams, at an E-YUVA Centre | NOT CONFIRMED |
| ICMR MedTech Mitra | ICMR and CDSCO, guided by NITI Aayog | **No money stated** | "applicant innovator / startup" applies online | Free help with clinical evaluation and regulatory route. Use it at the pilot stage (S14) |
| MeitY SAMRIDH | MeitY Startup Hub, via accelerators | Matching investment up to ₹40 lakh, as equity-type instruments (snippet) | Private limited company with a working product | Not a grant. NOT CONFIRMED |
| Karnataka ELEVATE | Karnataka Government | Up to ₹50 lakh grant (snippet) | Company, firm or LLP registered in Karnataka | 2025 round finished; 22nd call opened Aug 2025 (snippet). NOT CONFIRMED |
| Tamil Nadu TANSEED | StartupTN | ₹10 lakh, or ₹15 lakh for green, rural-impact and women-led; StartupTN takes a 3% stake (snippet) | DPIIT-recognised, registered in Tamil Nadu | TANSEED 8.0 window was Dec 2025 (snippet). NOT CONFIRMED |
| Pfizer INDovation (run by Social Alpha with FITT, IIT Delhi) | Corporate programme | ₹60 lakh grant each to 14 health startups, plus 18 months' incubation (snippet) | Startups | Date of next round not found. NOT CONFIRMED |

- Source: S14 MedTech Mitra – https://medtechmitra.icmr.org.in/about – grade A. All other rows – snippets only – grade C.
- Status: as marked per row.
- What it means for SpiroBuddy: after PRAYAS and a state idea grant, the next rung almost always needs a company in a particular state. Choose where to register with that in mind.
- **Not researched or not found this round:** NIDHI-EIR amount, BIRAC SPARSH current terms, Atal Innovation Mission grants for startups, ICMR extramural schemes, Maharashtra's schemes, Grand Challenges India, Villgro, C-CAMP, SINE and FITT terms.

### B3-12: Incubators – what they give and what they ask
- Detail: HTIC MedTech Incubator (IIT Madras): access to HTIC's R&D centre and other IIT Madras labs, IP and compliance help, links to hospitals and medtech companies; grantees must enrol in its pre-incubation or incubation programme and pass its selection. Venture Center (Pune): free BIG application mentoring, a Letter of Intent to incubate, discounted incubation for BIG winners; fees and equity are not stated on the page. AMTZ MEDI VALLEY: incubation next to test labs; terms not published. StartupTN takes a 3% stake with TANSEED (snippet). SAMRIDH accelerators take equity through a convertible note (snippet). No incubator's standard equity or fee terms were found in public.
- Source: S17, S16, S13; snippets – grade C.
- Status: SINGLE SOURCE each.
- What it means for SpiroBuddy: ask every incubator three things in writing: monthly fee, equity taken, and which hospital will actually let us test.

### B3-13: Seed investors that have backed Indian medtech hardware
- Detail (cheque sizes are from old or third-party profiles; treat as indicative only):

| Investor | Reported cheque | Example companies | Grade |
|---|---|---|---|
| 3one4 Capital (with Prime Venture Partners, YourNest) | First tracked Dozee round US$1.70 million, Sep 2020 | Dozee | B (S11) |
| Indian Angel Network, Villgro, C-CAMP | ₹4 crore seed together, 2021 | Yostra Labs (foot-nerve testing device) | C, snippet |
| Axilor Ventures, pi Ventures, Ankur Capital | pi Ventures ₹2–10 crore; Ankur US$0.5–5 million (fund profiles) | Niramai (breast screening) | C, snippet |
| Blume Ventures, Inventus Capital | Amount undisclosed | Tricog (ECG reading) Series A | C, snippet |
| Endiya Partners | Not found | SigTuple (blood-test AI) | C, snippet |
| IIMA Ventures | Sources disagree: ₹10–25 lakh, ₹20 lakh–1 crore, or US$100–150 thousand | Comofi Medtech | C, snippet |
| HealthQuad | US$1–5 million, early-growth stage | Not seed | C, snippet |

- What they expect before investing: **no public checklist was found.** Our reading from the comparables in B3-14: a working product in real hospitals, some paid use, and a clear regulatory class. This is inference, not a sourced fact.
- Source: S11 Inc42 – https://inc42.com/company/dozee/funding – grade B; the rest snippets – grade C.
- Status: SINGLE SOURCE / NOT CONFIRMED.
- What it means for SpiroBuddy: do not name a fund in the pitch as a likely backer. Say "grants first, impact and health funds after pilot data".

### B3-14: Comparable Indian medtech timelines – years, not months
- Detail:

| Company | Founded | First round found | Later | Regulatory milestone found |
|---|---|---|---|---|
| Dozee (contactless vital-signs monitor) | 2015 | US$1.70 million, 14 Sep 2020 | Series A US$5.91 million, 20 Jul 2021; US$9.51 million, Jan 2022; US$6.00 million, Apr 2023 | US FDA clearance reported Dec 2022 (snippet) |
| Niramai | 2016 | Seed, 23 Apr 2017, amount undisclosed | Series A US$6 million, Feb 2019 | CE mark and ISO 13485, Apr 2021 (snippet) |
| SigTuple | 2015 | Early round not confirmed | US$4 million, Jun 2025 | US FDA clearance, Sep 2023 (snippet) |
| Tricog | 2014 or 2015 (sources differ) | Seed not found | Series A (Blume, Inventus), amount undisclosed | Not found |
| Bempu (newborn temperature band) | 2013 or 2014 | Seed 2014, amount undisclosed; grant backers include Grand Challenges | About US$2.4 million total (one tracker) | Not found |

Dozee very likely had earlier angel or grant money that the tracker does not list; we could not find it. **First-pilot dates and Indian licence dates were not found for any of them.** Sanskritech and InnAccel were not researched.
- Source: S11 – grade B for Dozee rounds; all else snippets – grade C.
- Status: SINGLE SOURCE (Dozee); NOT CONFIRMED (others).
- What it means for SpiroBuddy: even the well-known names took about 1–5 years to a priced round and 5–8 years to a foreign regulatory clearance. A lower-risk device should be faster, but that is our hope, not evidence.

### B3-15: Company setup and DPIIT recognition
- Detail: DPIIT recognition (Startup India's official "recognised startup" status) is open to a private limited company, a registered partnership firm, an LLP (limited liability partnership) or a cooperative society, up to 10 years old, with turnover never above ₹200 crore, not formed by splitting an existing business, and working on an innovative or scalable product. (The page now also has a "deeptech" class: 20 years, ₹300 crore. Older guides say ₹100 crore; the official page is the one to trust.) Benefits listed: self-certification under 6 labour and 3 environment laws; fast-tracked patent examination with an 80% rebate on patent filing fees and government-paid facilitator fees; a 3-year income-tax holiday within the first 10 years (section 80-IAC; private limited companies and LLPs only); listing on GeM (the Government e-Marketplace), exemption from "prior experience / turnover" rules for manufacturing startups with their own Indian facility, and no earnest-money deposit on government tenders.
- An unregistered team **cannot** get DPIIT recognition. It **can** apply to NIDHI-PRAYAS (S17) and the KSUM Idea Grant (S7), and on BIRAC's older documents to BIG as an individual (snippet).
- Private limited vs LLP (vendor guides, snippets only, 2025–26): incorporation typically ₹8,000–20,000 in statutory costs plus professional fees; a private limited company needs a yearly audit whatever its size and can issue shares to investors; an LLP is cheaper to run but cannot issue shares, so equity investors and several grants (SAMRIDH, GENESIS matching) expect a private limited company. No MCA page was opened.
- Source: S5 Startup India – https://www.startupindia.gov.in/content/sih/en/startup-scheme.html – grade A. Cost guides – snippets only – grade C.
- Status: CONFIRMED for DPIIT rules; NOT CONFIRMED for costs.
- What it means for SpiroBuddy: stay unregistered through the first grant applications; register a private limited company when a grant is about to be released or a hospital wants a contract; apply for DPIIT recognition the same month. Our reading only; confirm with a chartered accountant.

### B3-16: Staged roadmap – what must be true to unlock the next money
- Detail (money figures are **team estimates** capped by the scheme ceilings above):

| Stage | Money and source | Rough need | Must be true at the end |
|---|---|---|---|
| 0–3 months | Own pocket, hackathon prize, college lab | Under ₹50,000 (10 hand-built units at ₹1,400–2,600 each, repo estimate) | A real unit reads a real Breazer within ±100 mL (HARDWARE.md §8); one nurse or physiotherapist agrees the alert rules; NOC from college; one PRAYAS Centre contacted |
| 3–12 months | NIDHI-PRAYAS up to ₹10 lakh; KSUM Idea Grant ₹3 lakh if in Kerala; MeitY EiR ₹4–10 lakh as an alternative | ₹5–13 lakh | 50–100 units built; ethics approval and a ~50-patient pilot running in one hospital; company registered; DPIIT recognition; device class confirmed by a consultant; MedTech Mitra application filed |
| 12–24 months | Startup India Seed Fund ₹20 lakh grant **or** BIRAC BIG ₹50 lakh (check the ₹10 lakh rule before choosing); state productisation grant | ₹20–60 lakh | Pilot results written up; quality system started; licensed manufacturing route chosen; first paying hospital at ₹500–1,000 an episode; 1,000-unit build quoted |
| 24–48 months | Seed equity (impact or health funds); SAMRIDH matching; Seed Fund debt up to ₹50 lakh; hospital revenue | ₹1–4 crore (in line with the ₹4 crore Yostra seed, snippet) | Licence in hand; 3–5 hospitals; contribution margin positive per episode; moulded case; second use (lung rehabilitation after TB) tested |

- Source: schemes as cited in B3-7 to B3-11; unit costs from RESEARCH_REPORT §4.6.
- Status: NOT CONFIRMED (a plan, not a fact).
- What it means for SpiroBuddy: this is the honest answer to "would you make it a startup?" – yes, in grant-sized steps, each tied to one proof.

## What to say in the 5-minute pitch (5 bullets max, each with its source)
- "Our first money is a grant, not an investor: NIDHI-PRAYAS gives up to ₹10 lakh to individuals building a physical prototype." (S17)
- "After a pilot, BIRAC's BIG grant is up to ₹50 lakh for 18 months, with calls every January and July." (S1)
- "At ₹500 an episode and a few thousand patients, each episode leaves about ₹180–260 after device, messaging, calls and server costs – our own model, built on estimates." (B3-6)
- "One unit pays for itself after about 5 patients at ₹500." (B3-6, same caveat)
- "Indian medtech takes years: Dozee was founded in 2015 and its Series A was in 2021. We plan in grant-sized steps." (S11)

## What NOT to say (claims that would be wrong or unproven)
- "We are eligible for the Startup India Seed Fund." Not yet: it needs a DPIIT-recognised company, and we could not confirm the scheme is still open.
- "We will get BIG / PRAYAS." These are competitive; say "we will apply".
- "It costs ₹300 a patient." Our model loses money at ₹300 until volumes are large and units survive 12+ reuses.
- "Each unit is reused 20 times." No data; loss and breakage are unknown.
- "The device will cost under ₹1,000." Only plausible with a moulded case at thousands of units; no quote exists.
- "Investors are interested" or naming any fund. No contact has been made.
- "A mould costs ₹1 lakh." Listings vary from ₹80,000 to several lakh; we have no quote.
- Any current call deadline. None was found for late 2026.

## First 90 days: concrete next steps (who does what, rough cost in ₹ where a source gives one)
1. **Team lead:** email three PRAYAS Centres (for example HTIC at IIT Madras, nidhiprayas@htic.iitm.ac.in, and the nearest one to the college) asking for the next call date and whether a student team may apply. Cost: nil.
2. **Team lead:** ask the college for a no-objection certificate, needed by PRAYAS and SITARE. Cost: nil.
3. **Hardware person:** build 2–3 units and do the caliper and accuracy checks in RESEARCH_REPORT §4.7. Cost: about ₹1,400–2,600 a unit (repo estimate).
4. **Hardware person:** design a simple PCB and get instant quotes from two Indian vendors for 100 boards. Entry price point: ₹799 for 5 bare boards (S12).
5. **Anyone:** if in Kerala, watch for the KSUM Idea Grant call (up to ₹3 lakh; contact on the scheme page, S7).
6. **Team lead:** write to a BIG partner (big@venturecenter.co.in, S16) in November to prepare for a possible 1 January 2027 call.
7. **Clinical contact:** get one hospital department to sign a letter of interest; every grant form asks for it.
8. **All:** do not register a company yet unless a grant or hospital requires it; when you do, expect roughly ₹8,000–20,000 plus fees (vendor guides, unconfirmed) and apply for DPIIT recognition at once (S5).
9. **Team lead:** file the free MedTech Mitra form once a prototype report exists (S14).

## Open questions (what you could not find, and who could answer it)
- **Which state is the team in?** It decides the state grants. (The team.)
- Current 2026–27 call dates for BIG, NIDHI-PRAYAS, SITARE-GYTI, TIDE 2.0 and TANSEED. (Each scheme's portal; the PRAYAS Centre; a BIG partner.)
- Whether the Startup India Seed Fund continues after 2025. (seedfund.startupindia.gov.in, opened in a browser; any SISFS incubator.)
- BIG's current rules for individuals and students (November 2025 guidelines could not be read). (BIRAC; Venture Center.)
- What changed in "NIDHI PRAYAS 2.0". (DST guideline PDF, opened by hand.)
- Real quotes: 100 and 1,000 assembled boards, a printed case, a mould, and a contract manufacturer willing to do a small medical batch. (Upload files to Lion Circuits, PCB Power; ask AMTZ and one mould maker.)
- Fees at AMTZ's test labs and incubator; whether Kerala's MedSpark is operating. (info@amtz.in; KSIDC.)
- Incubator fee and equity terms (HTIC, Venture Center, SINE, FITT, C-CAMP, Social Alpha, Villgro). (Ask each in writing.)
- Loss, breakage and cleaning cost for a lent device. (The pilot itself; a hospital biomedical engineer.)
- First-pilot and Indian licence dates for Dozee, Tricog, Niramai, SigTuple, Bempu; anything on Sanskritech and InnAccel. (Founder interviews; company filings.)
- What seed investors require in writing. (A conversation with one health-focused fund or an incubator's investment manager.)
- Official MCA fee schedule and state stamp duty. (A chartered accountant.)

## Sources opened this round
| # | URL | title | publisher | grade | used in |
|---|---|---|---|---|---|
| S1 | https://birac.nic.in/desc_new.php?id=83 | Biotechnology Ignition Grant (BIG) scheme page, updated 1 Oct 2026 | BIRAC (government) | A | B3-9 |
| S2 | https://nidhi.dst.gov.in/nidhi-prayas/ | NIDHI PRAYAS (title and "2.0 guidelines" link only), updated 20 May 2026 | DST (government) | A | B3-7 |
| S3 | https://grants.startupmission.in | Innovation Grant Portal (login page only, nothing usable) | Kerala Startup Mission | A | – |
| S4 | https://seedfund.startupindia.gov.in/about | Seed Fund portal (page did not render, nothing usable) | DPIIT | A | B3-10 (status gap) |
| S5 | https://www.startupindia.gov.in/content/sih/en/startup-scheme.html | DPIIT Recognition: eligibility and benefits | Startup India (government) | A | B3-15 |
| S6 | https://www.zetwerk.com/blog/injection-moulding-in-india-complete-guide-to-plastic-part-manufacturing-and-sourcing/ | Injection moulding in India guide (undated, 2026 footer) | Zetwerk (vendor) | C | B3-4 |
| S7 | https://startupmission.kerala.gov.in/schemes/idea-grant | Idea Grant | Kerala Startup Mission (government) | A | B3-8 |
| S8 | https://www.startupindia.gov.in/content/dam/invest-india/Templates/public/Guidelines%20for%20Startup%20India%20Seed%20Fund%20Scheme.pdf | Guidelines for Startup India Seed Fund Scheme | DPIIT (government) | A | B3-10 |
| S9 | https://www.birac.nic.in/webcontent/1596458927_updated_faq_big_scheme.pdf | BIG FAQ (PDF text could not be extracted) | BIRAC | A | – (B3-9 uses snippets) |
| S10 | https://tbi.nitc.ac.in/wp-content/uploads/2025/06/1.-PRAYASEE_Eligibility_Guidelines-2024-25-Second-Call.pdf | PRAYAS eligibility, NIT Calicut TBI (redirected to a page with no details) | NIT Calicut TBI | B | – |
| S11 | https://inc42.com/company/dozee/funding | Dozee funding rounds | Inc42 | B | B3-13, B3-14 |
| S12 | https://lioncircuits.com/ | Lion Circuits home page (PCB price offer, services) | Lion Circuits (vendor) | B | B3-2 |
| S13 | https://amtz.in/our-centers | AMTZ centres | Andhra Pradesh MedTech Zone | B | B3-5, B3-12 |
| S14 | https://medtechmitra.icmr.org.in/about | About MedTech Mitra | ICMR / CDSCO (government) | A | B3-11 |
| S15 | https://startupmission.kerala.gov.in/schemes/productisation-grant | Productisation Grant | Kerala Startup Mission (government) | A | B3-8 |
| S16 | https://www.venturecenter.co.in/big/ | BIG at Venture Center (Call 25, partner services) | Venture Center, Pune | B | B3-9, B3-12 |
| S17 | https://htic.iitm.ac.in/mti/?p=1789 | NIDHI PRAYAS at HTIC MedTech Incubator | HTIC, IIT Madras | B | B3-7, B3-12 |

Attempts that failed and were not read: https://zbotic.in/pcb-assembly-service-india-jlcpcb-vs-local-fab-cost-guide/ (blocked, HTTP 403) and https://myscheme.gov.in/schemes/sitare-gyti (error page). None of the above URLs were in the ledger before this round.
