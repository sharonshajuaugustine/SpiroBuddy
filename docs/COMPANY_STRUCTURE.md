# Company structure: the company needed to maintain and run SpiroBuddy

**Written:** Sun 11 Oct 2026 · **Answers:** the founder's ask of 11 Oct ("create a company structure, which will be needed to maintain and run this company") · **Confidence:** medium for the legal steps and duties (they come from the repo's legal research, much of it still marked "not confirmed" there); **low** for every headcount (the repo holds no staffing plan).

**How to read this file**
- **plan 00 / 03 / 05 / 06 / 11** = files in `docs/plan/`. **B3-x, B4-x** = `docs/research/business/03_…` and `04_…`. **FA** = `docs/FUTURE_ARCHITECTURE.md`. **SCALING** = `docs/SCALING_AND_COST.md`. Full list in section 11.
- Every number is a fact with its repo source, or is labelled **estimate**, **assumption** or **target**. "Derived" = our arithmetic on repo numbers. "Ours" = this file's own guess. Where the repo has no basis: "not yet costed" or "founder to fill".
- Status words: **Live**, **Simulated**, **In development**, **Planned**. Only Stage 0 is Live. Every company, hire, licence and routine below is Planned. The hospital and patients in the demo are fictional.
- Roles are titles only. No person or firm is named: the team's names are not in the repo (plan 00 §F). This is a plan, not legal advice. Where a choice is needed, confirm with a company secretary (a licensed company-law professional) or a chartered accountant (CA).

> ## 1. Answer in 10 lines
> 1. **Today (Live):** a small founder team does everything. **No company is registered** (plan 06 Gate 1 #10: "Not started"). Team size, names and college: founder to fill (plan 00 §F).
> 2. **Legal shell (Planned):** a private limited company, the usual choice for a team that wants grants and investors (plan 06 L-14). Register it when a grant is about to be released or a hospital wants a contract. Apply for DPIIT recognition (Startup India's "recognised startup" status) the same month (B3-15).
> 3. **Before that, for ₹0:** a founders' agreement that assigns all inventions and code to the future company, and the college's and hackathon's ownership terms in writing (plan 06 Gate 0 #1–4).
> 4. **Nine functions** keep the service running: clinical and patient safety; regulatory and quality; product and engineering; device operations; hospital success; support; data protection and security; sales and partnerships; finance, legal and people (section 4).
> 5. **Stage 1 Pilot needs no employees** (assumption). The founders hold six hats that the repo's legal checklists already name. Paid by the job: company secretary or CA, lawyer, regulatory consultant, insurance broker. Plus one clinical adviser from outside the pilot hospital.
> 6. **Hires start at Stage 2** (10 hospitals): quality and regulatory lead, a backend engineer who shares on-call, hospital success lead, support and device coordinator, clinical lead (section 9). About 23 employees at Stage 3 (assumption, ours).
> 7. **Care decisions never sit with us.** The nurse and doctor decide (B4-15). Patients contact their nurse, not SpiroBuddy. Our helpdesk serves hospital staff.
> 8. **Duties that need a named owner:** the quality system (the written rules for how a device company designs, builds and supports its product); adverse events (harm to a patient), complaints and recall (report within 15 days: plan 06 L-17); human oversight of the AI (the 2023 AI guideline of ICMR, the Indian Council of Medical Research: plan 11 §H); the data-breach clock (6 hours and 72 hours: FA §8.5); a grievance officer for privacy requests (FA §3.7).
> 9. **People cost:** salaries are not yet costed anywhere in the repo (plan 03 header). Sourced so far: CA ₹12,000–50,000 a year and early legal papers ₹20,000–1,00,000 (estimates, plan 03 §C3); support time ₹25 an episode (assumption, plan 03 §3).
> 10. **Do now:** (a) sign the founders' agreement, (b) put one name against each hat, (c) find one clinical adviser and one company secretary or CA.

## 2. The legal shell

### 2a. Which kind of company, and when
| Question | What the repo says | Source |
|---|---|---|
| Which form? | **Private limited company:** at least 2 shareholders and 2 directors; can issue shares and share options; has the most yearly filings. An LLP (limited liability partnership) is cheaper to run but cannot issue shares, so investors and several grants expect a private limited company. The founders choose: confirm with a company secretary | plan 06 L-14; B3-15 |
| When? | Stay unregistered through early grant applications. Register when a grant is about to be released, a hospital wants a contract, or just before the prototype test licence (it needs a legal entity) | B3-15; plan 06 L-14; B4 §10 step 2 |
| Who can sign? | Every founder who signs must be 18 or older. At least one director must have lived in India 182 days or more in the year | plan 06 L-14 |
| Set-up cost | ₹7,000–25,000 all-in (**estimate**, 2026 vendor guides, grade C; depends on the state) | plan 03 §C3 |

### 2b. Registrations that follow
| When | What | Cost and time | Source |
|---|---|---|---|
| Month of incorporation | DPIIT recognition; Udyam (micro-enterprise) registration | ₹0 | B3-15; plan 06 Gate 1 #11 |
| Before prototypes go to a hospital | Test licence for prototype units (Form MD-12 → MD-13) | ₹500 per device; 30 days; valid 3 years | B4 "Answer" line 3; plan 06 Gate 1 #13 |
| Before a paid pilot (money changing hands counts as a sale) | Manufacturing licence, or a **loan licence** through a manufacturing partner that already holds one; GST (goods and services tax) registration; trademark filing | ₹5,000 per site + ₹500 per device; 45 days (Class A) or about 140 days (Class B). Trademark ₹4,500 per class (snippet) | B4 §10 steps 13, 18; plan 06 Gate 2 #24, #26, #28 |
| As headcount grows | Shops and Establishments registration from employee 1 in most states; state insurance at 10 workers; provident fund at 20 | to confirm (general knowledge in the repo) | plan 06 L-23 |

### 2c. Founders' agreement, and who owns the inventions
- **Founders' agreement** (practice, not a statute): roles, shareholding, vesting (shares earned over time; commonly 4 years with a 1-year wait), what happens when a founder leaves, decision rules, and **written assignment of all IP (inventions, code, designs) to the company** by every founder and contractor (plan 06 L-14).
- **Student work:** read the college IP policy and the hackathon terms, and get both in writing. Status: not started (plan 06 Gate 0 #1–2). Which college: founder to fill (plan 00 §F).
- **Helpers:** an unpaid volunteer who writes code owns that code unless they assign it. Every contributor signs a one-page assignment (plan 06 L-23, Gate 0 #4).
- **Protect the business** with IP assignment and confidentiality, not a non-compete: Indian courts refuse to enforce a non-compete after someone leaves (plan 06 L-23). Keep new hardware details unpublished until a patent or design decision is made (plan 06 Gate 0 #5).

### 2d. The incubator (for example an AIC)
"AIC" is read here as Atal Incubation Centre, a government-backed incubator programme (same reading as SCALING §7; founder to confirm). The repo holds **no terms** for the team's own incubator.

| What incubators usually give (B3-12) | What they usually ask (B3-12) |
|---|---|
| Lab access; help with IP and regulatory paperwork; links to hospitals and medtech companies; grant-application mentoring; a letter of intent to incubate | Enrol in their programme and pass selection. Some take a stake: 3% in one state scheme, or a convertible note (a loan that turns into shares) in one accelerator scheme (snippets, grade C). **No incubator's standard fee or equity terms were found in public** |

- Ask ours three things **in writing**: the monthly fee, the equity taken, and which hospital will actually let us test (B3-12).
- For its servers, use the fill-in table in SCALING §7d and the 10 conditions in §7b. Read the incubation agreement for any clause on IP or equity before signing (ours; confirm with the lawyer).

## 3. The organisation at each stage
Stage names are the ones in SCALING §4. **Only Stage 0 is Live; Stages 1–4 are Planned.** All headcounts are **assumptions (ours)** for the founder to correct.

| Stage | Active patients at once | Monthly running cost (units lent, no salaries, estimate) | Cost to us per 14-day episode (lent, estimate) | Legal gate to pass (plan 06; mapping ours) | Who runs it |
|---|---|---|---|---|---|
| **0 Demo** (today, Live) | 7 fictional | ₹0 hosting | n/a | Gate 0 | Founder team; size: founder to fill |
| **1 Pilot** (1 hospital) | 25–50 | ₹32,000–59,000 | ≈ ₹670 | Gate 1: before any real patient | Same founders in 6 named hats; 0 employees |
| **2 Multi-hospital** (10 hospitals) | about 250 | ₹2.8–3.8 lakh | ≈ ₹500–540 (derived) | Gates 2 and 3: before a paid pilot, before selling | Founders + about 5 employees |
| **3 Multi-hospital** (about 100 hospitals) | 2,500–5,000 | ₹25.8–30.2 lakh (at 2,500) | ≈ ₹470–490 | Gate 4: at scale | A team per function; about 23 employees |
| **4 National** (state or national programme) | 100,000+ | technology only: about ₹50–60 lakh; the rest not yet costed | ≈ ₹450 (derived) | Gate 4, plus tender terms | not yet costed |

Sources: SCALING §4; plan 03 §2.2, §3; FA §1.1, §11. If the hospital owns the units, the monthly figure is ₹12,000–40,000 / ₹0.8–1.8 lakh / ₹6.0–10.5 lakh. Planned price: about ₹1,000 an episode (estimate).

### 3a. Who holds each role
**F** = founder hat · **E** = employee · **A** = part-time adviser · **O** = outside firm · **H** = the hospital's own staff (not ours) · **–** = not needed yet

| Role | St. 0 | St. 1 | St. 2 | St. 3 | St. 4 |
|---|---|---|---|---|---|
| Team lead / chief executive (grants, contracts, money) | F | F | F | F | F |
| Product owner (intended use, claims wording, labels) | F | F | F | F | E |
| Software lead (hospital software, patient app, AI and breath model, data safeguards) | F | F | F + 1 E | F + team | team |
| Hardware lead (unit, firmware, bench tests) | F (Simulated only) | F | F | F + E | team |
| Quality owner (quality system, licence file, complaints) | – | F | E | E + 1 | team |
| Clinical adviser, later clinical lead | – | A | A, then E | E + A panel | team |
| Hospital investigator, ethics committee, ward nurses | – | H | H | H | H |
| Device operations (stock, repair, cleaning supplies, courier) | – | F | E (shared) | team | regional |
| Hospital success (onboarding, training, connecting) | – | F | E | team or distributors | programme office |
| Support desk for hospital staff | – | F | E (shared) | 3 E | second line only |
| Data protection and security owner | F | F | F + O | E | team |
| On-call engineer | – | F, in turn | rota | rota | day and night |
| Sales and partnerships | F | F | F | E | team |
| Finance, legal and people | F | F + O | F + O | E + O | team |
| Outside firms: company secretary or CA, lawyer, regulatory consultant, insurance broker. From Stage 2 also a licensed contract manufacturer, an accredited test lab and a security tester | – | O | O | O | O |

### 3b. The trees
```
STAGE 0 – Demo (Live)
Founder team  (size and names: founder to fill – plan 00 §F)
├─ Team lead ...... pitch, form, interviews
├─ Software ....... hospital software, patient app, AI coach – Live, fictional patients
└─ Hardware ....... 3D model and simulator only; no hardware today (plan 00 item 12)
   Held by nobody yet: quality owner, clinical adviser, company secretary
STAGE 1 – Pilot, 1 hospital (Planned; 0 employees – assumption)
Founders  (same people, six named hats)
├─ Team lead ...... company, grants, pilot agreement, insurance quote
├─ Product owner .. intended use, banned claims, consent script
├─ Hardware lead .. pilot units, risk file, bench safety check
├─ Software lead .. India-hosted data, breach plan, access log, releases
├─ Quality owner .. starts the quality system; complaint and incident log
└─ Operations ..... unit log (out, back, condition), cleaning supplies, weekly visit
   Paid by the job: company secretary or CA · lawyer · regulatory consultant · insurance broker
   Adviser: one clinical adviser from OUTSIDE the pilot hospital
   Hospital's own: investigator, ethics committee, ward nurses, biomedical engineer, infection-control nurse
STAGE 2 – Multi-hospital, 10 hospitals (Planned; about 5 employees – assumption)
Chief executive (founder) ─ sales, partnerships, money
├─ Quality and regulatory lead (E, hire 1) ─ quality system, licence file, complaints, recall
├─ Clinical lead (A, later E, hire 5) ───── alert rules, coach wording, safety review
├─ Technology lead (founder) ─ with hardware and firmware (founder) and data protection (founder hat)
│   └─ Backend engineer (E, hire 2) ─ shares the on-call rota (FA §14)
├─ Hospital success lead (E, hire 3) ─ onboarding, training, connecting to hospital software
└─ Support and device coordinator (E, hire 4) ─ helpdesk for nurses, unit stock, repairs
   Outside: licensed contract manufacturer · test lab · security tester · company secretary or CA · lawyer · regulatory consultant
STAGE 3 – Multi-hospital, about 100 hospitals (Planned; about 23 employees = the sum below – assumption)
Chief executive (founder)
├─ Clinical and patient safety ... clinical lead (1) + part-time adviser panel
├─ Regulatory and quality ........ lead + 1
├─ Product and engineering ....... technology lead (founder) + software 3, AI model 1, hardware and firmware 1
├─ Device operations ............. lead + 2 technicians; contract manufacturer outside
├─ Hospital success .............. lead + 4 regional staff, or distributors (plan 03 §3, note 4)
├─ Support desk .................. 3  (derived: 5,000 episodes × 5 min ≈ 417 hours a month ≈ 2.5 people)
├─ Data protection and security .. 1 · Sales and partnerships .. 2
└─ Finance, legal and people ..... 1 + company secretary, CA and lawyer outside
STAGE 4 – National (Planned; shape only, headcount not yet costed)
Same nine functions, plus a programme office per contract (plan 06 Gate 4 #41), on-call day and night (FA §14),
and regional unit depots or a maker or distributor channel (plan 05 E-20). Support becomes second line:
200,000 episodes a month × 5 min would need about 100 people (derived), so the programme's own staff
would take nurses' day-to-day questions (ours).
```
Stage 1 hats and owners: B4 §10 steps 1–11; plan 06 Gates 0–1; plan 05 E-3 steps 3–5; plan 03 §C4. Support sizing: 5 minutes an episode is a repo assumption (B3-6, used in plan 03 §3); 170 working hours a month per person is ours.

## 4. Functions, and what each one owns
| Function | Owns | Notes and limits | Source |
|---|---|---|---|
| **Clinical and patient safety** | Alert rules and thresholds; red-flag word lists; coach wording; review of every safety incident; the "nurse only, no AI" option | Never owns care decisions: those stay with the nurse and doctor. The coach stays on "how to do the exercise" | B4-15; B3-16; plan 11 H-1 #1 |
| **Regulatory and quality** | Quality system (the rule book for how a device company designs, builds, changes and supports products); risk file; test licence and device licence; change control over the frozen "device baseline"; complaints, adverse events and recall; review of every public claim | Device class (A-measuring or B): to confirm with CDSCO (India's device regulator) or a consultant | FA §10; B4-5; plan 06 Gate 2 #25, Gate 3 #31–32 |
| **Product and engineering** | Hospital software; patient app; AI coach and breath model; firmware; hardware design; releases and their records; model, rules and firmware version stamped on every breath and alert | Keeps the regulated core separate from messaging and family features, so a wording change does not reopen the device change process | FA §10, §13 #5, #9 |
| **Device operations** | Build through a licensed contract manufacturer; serial number and firmware version on every unit; stock, repair, retire, lost units; cleaning procedure and supplies; courier for units not returned | In the lent model the **nurse or technician at the hospital** does return → clean and check (20-second self-test) → wipe, on one screen. Planned design, not built | DEVICE_LIFECYCLE §5.1; B4-5; B4 §10 step 13; plan 03 §C4 |
| **Hospital success** | The 13-step buying journey; onboarding and nurse training; weekly pilot summary; yearly usage report for renewal; **connecting to the hospital's own software** | See [`INTEROPERABILITY.md`](INTEROPERABILITY.md): four levels of connection (§4), moving a hospital in (§6) and out (§7). From meeting a hospital to being paid: 9–15 months (**estimate**) | plan 05 E-3 |
| **Support** | Helpdesk for nurses and hospital admins. A support engineer can open a patient record only by typing a reason; access lasts 60 minutes and the hospital admin is told at once | **Patients contact their nurse, not us.** Urgent words get the fixed "contact your nurse / call 112" message. Helpdesk hours: founder to fill (to be written into the service agreement, plan 06 Gate 2 #27) | FA §2.4; project rule |
| **Data protection and security** | Duties in the data agreement with each hospital: access logs kept 1 year, breach notice, help with patients' requests (see, correct, erase, withdraw), deletion or return at the end; the breach runbook (a one-page what-to-do sheet); key rotation; outside security tests | In a pilot the hospital decides why data is used; we process it for the hospital | B4-16; FA §3.7, §8.5 #5, §9.1 |
| **Sales and partnerships** | Hospital champions, rehab chains, makers and distributors, grants, the incubator | Written rule: no payments or gifts to individual clinicians | plan 05 E-20; B3-16; plan 06 Gate 1 #22 |
| **Finance, legal and people** | Books, tax and company filings; contracts (pilot agreement, unit-loan terms, data agreement, service agreement); insurance; hiring letters with IP assignment; harassment-prevention policy from day one | Mostly outside firms until Stage 3 | plan 06 L-14, L-23, Gate 1 #18; B4-19 |

## 5. Roles a rule or guideline requires someone to hold
| Role | Why | Repo source | From | Confirmed? |
|---|---|---|---|---|
| Two directors, one resident in India | Companies Act 2013 (minimum for a private limited company; s.149(3)) | plan 06 L-14 | The day the company is registered | To confirm with the company secretary |
| Auditor (outside firm) | Appointed within 30 days; a private limited company is audited every year whatever its size | plan 06 L-14; B3-15 | Same | To confirm (snippets) |
| Sponsor of the study | Medical Devices Rules 2017 (MDR), rules 51 and 53, if the pilot counts as a clinical investigation | plan 06 Gate 1 #16–17; plan 11 §H | Stage 1 | Rule cited in the repo. **Who** is sponsor (us or the hospital): to confirm with the consultant |
| Principal investigator, and a registered ethics committee | MDR rule 50; ICMR 2017 guidelines | plan 06 Gate 1 #15; B4 §10 step 8; plan 11 H-2 #2 | Stage 1 | Yes. These are the hospital's people, not ours |
| Named people accountable for the AI; a human always supervising it | ICMR 2023 AI guideline §1.5 and its 17-item checklist. A guideline, not a law | plan 11 H-1 #2, #6; H-2 #7 | Stage 1 | Guideline text read; how it applies to us is our reading. If the prescription reader (Planned) is built, a named nurse or pharmacist at the hospital signs off each prescription it reads (plan 11 H-1 #2) |
| Quality owner | MDR Fifth Schedule (quality system) | B4-5; B4 §10 steps 12, 19, 24; plan 06 Gate 2 #25 | A hat at Stage 1; a job before a paid pilot | Yes. The title "management representative" used by ISO 13485 (the international quality-system standard for device makers): **to confirm** (not in the repo research) |
| Owner of adverse events, complaints and recall | MDR rule 26(ii): tell the licensing authority within 15 days; rule 89: recall; rule 53(v): 14 days inside a permitted investigation | plan 06 L-17, Gate 3 #31 | Stage 1 (study events); Stage 2 (licence holder) | Yes (rule text read). In a study, serious events also go to the ethics committee within 24 hours (plan 11 H-2 #12); whether the investigator or we report: to confirm |
| Breach-response owner | CERT-In (India's cyber-incident agency) within 6 hours; affected people and the Data Protection Board within 72 hours; the hospital "without delay" | FA §8.5 #5; B4-16; plan 06 Gate 1 #19 | Stage 1 | In the repo ledger. The Board had no members as of Aug 2026 (B4-13) |
| Grievance officer (privacy contact named in every notice) | DPDP Act 2023 (India's data protection law); main duties start 13 May 2027 | FA §3.7; B4-13 | Stage 1–2 | **To confirm:** FA marks the reply period "(?)", and in a pilot the hospital, not us, decides how data is used (B4-16). A data protection officer is needed only by a "significant data fiduciary" named by the Government; no list was found (B4-13) |
| Internal Committee for harassment complaints | POSH Act 2013: compulsory at 10 or more workers | plan 06 L-23 | When headcount reaches 10 | To confirm |
| Named clinical adviser | Not a legal post. A nurse or physiotherapist must agree the alert rules; an ethics committee asks for the team's credentials | B3-16; plan 11 H-1 #6; plan 03 §C4 | Stage 1 | Plan, not a rule |

## 6. How decisions and safety problems travel

### 6a. Who decides what
| Decision | Who decides | Who can stop it |
|---|---|---|
| A patient's care: targets, what to do about an alert | The nurse or doctor at the hospital. Never SpiroBuddy (B4-15) | – |
| Alert rules, red-flag words, coach wording | Clinical adviser or lead, with the product owner | Quality owner |
| A release that changes the device baseline (FA §10) | Technology lead ships; quality owner signs | Quality owner. Once licensed, major changes need the regulator's approval beforehand (plan 06 L-17) |
| Any claim in an advert, video or pitch | Team lead | Quality owner (B4-20) |
| Money: spending, price, grants, hiring | Chief executive, under the decision rules in the founders' agreement; the board once a company exists | Board |
| Pausing a hospital, or a recall | Quality owner and chief executive | Either one alone may pause (ours) |

### 6b. A safety incident
```
Patient feels unwell ──► fixed message: contact your nurse / call 112   (the AI never diagnoses)
Nurse or doctor ─────► treats the patient (the hospital's duty), then tells our helpdesk
Helpdesk ────────────► logs it the same day ──► quality owner + clinical adviser
Clinical adviser ────► is it serious? were the unit or the software involved?
Quality owner ───────► tells the founders the same day ──► pause, fix or recall
Reports outside, where required:
  · during a study: ethics committee within 24 hours (plan 11 H-2 #12); CDSCO within 14 days if it is a permitted investigation (plan 06 L-17)
  · once licensed: licensing authority within 15 days, including any recall (plan 06 L-17)
  · the hospital: both ways, as the pilot agreement sets out (B4-19, key clauses)
```
- **Data breach:** contain → assess → CERT-In within 6 hours → affected people and the Data Protection Board within 72 hours → the hospital, under the contract → a written review (FA §8.5 #5).
- **System fault:** one-page runbooks for alert path down, message provider down, database down, bad release and AI vendor down (FA §8.5; Planned, not yet written). If the alert path fails, the fallback is a printed phone list at the nurse desk.

### 6c. Who is on call
- **Stage 0:** nobody (fictional patients only). **Stage 1:** founders, in turn (assumption, ours). **Stages 2–3:** a rota, from the day hospital 2 signs (FA §14). **Stage 4:** day and night (FA §14).
- **Target (FA §8.3):** an urgent alert not on the nurse's screen in 60 seconds, or not acknowledged in 10 minutes, pages the on-call person and rings the ward's nurse desk. The on-call person looks after the system and never advises on a patient.

## 7. The routines that keep it running
All Planned. A routine marked * has a cadence that is ours (assumption): the repo names the task but not how often.

| How often | Routine | Owner | Source |
|---|---|---|---|
| Weekly | Review every "break-glass" access (staff opening a record outside their scope) | Data protection owner | FA §2.4 |
| Weekly | Nurses label a small random sample of breaths, from consenting patients only | Clinical lead + hospital | FA §6.4 |
| Weekly | Release review*: what shipped, what it touched, roll back if needed. Open complaints list* | Technology lead + quality owner | FA §8.5 #4 |
| Weekly | Pilot summary to the hospital; unit log (out, back, condition) | Hospital success | plan 05 E-3 step 5 |
| Monthly | Audit-log sample*: who looked at what. Privacy-request tracker*: nothing waiting past its deadline (deadline to confirm: FA recalls 90 days, marked "(?)") | Data protection owner; grievance officer | FA §13 #6, §3.7; B4-16 |
| Monthly | Model performance review*: daily drift figures (drift = the model's inputs or answers slowly shifting); labels against nurses' corrections. A new model runs unseen beside the live one for 4 weeks or more before any switch | AI owner + clinical lead | FA §6.3; plan 11 H-1 #5 |
| Monthly | Usage report per hospital (it becomes the renewal case); books and tax filings | Hospital success; finance | plan 05 E-3; plan 06 L-14 |
| Quarterly | Test restore of the backup, written up. Rotate the systems' keys and passwords | Technology lead | FA §3.4, §9.1 |
| Quarterly | Quality-system review*: complaints, incidents, changes, suppliers | Quality owner + founders | FA §10 |
| Yearly | Device-recall drill*: pick a serial range, find every unit and every patient it was lent to, and time it | Quality owner + device operations | plan 06 Gate 3 #31; DEVICE_LIFECYCLE §5.1 |
| Yearly | Outside security test, later an audit by a government-empanelled auditor. Publish a short audit of AI performance and errors | Data protection owner; AI owner | plan 03 Stage D; plan 06 Gate 4 #42; plan 11 H-2 #13 |
| Yearly | Company filings (annual meeting, accounts, annual return, director identity check); marketing-code self-declaration and claims review; insurance renewal. Every 5 years: licence retention fee, ₹5,000 + ₹500 | Company secretary or CA; quality owner; finance | plan 06 L-14, Gate 3 #32; B4-19; B4 §10 step 19 |

## 8. What it costs to run: the people side
Servers, messaging, AI and units: see [`SCALING_AND_COST.md`](SCALING_AND_COST.md) §4 and plan 03 §3. **No file in the repo costs salaries** (plan 03 header: the team's time is "the largest real cost, and it is unpaid"). So founders' time and every salary is "not yet costed". The four lines below are **already inside** the monthly totals in section 3; do not add them twice.

| People-side line (a month) | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Basis |
|---|---|---|---|---|---|
| Human support, 5 min an episode | ₹1,250 | ₹12,500 | ₹1,25,000 | not yet costed | plan 03 §3 (**assumption**, B3-6) = ₹25 an episode (derived) |
| Cleaning | ₹1,000 | ₹10,000 | ₹1,00,000 | not yet costed | plan 03 §3 (**assumption**, B3-6) |
| Field visits and travel | ₹3,000–10,000 | ₹30,000–1,00,000 | ₹2–5 lakh | not yet costed | plan 03 §3 (**estimate**) |
| Company overheads (CA, domain, stores, insurance) | ₹1,100–5,400 | ₹2,000–5,800 | ₹50,000–1,50,000 | not yet costed | plan 03 §3 (**estimate**) |

| Outside help | Cost | When | Basis |
|---|---|---|---|
| CA: yearly filings | ₹12,000–50,000 a year | From registration | plan 03 §C3 (**estimate**, grade C) |
| Lawyer: founders' agreement, pilot agreement, unit-loan terms, data agreement | ₹20,000–1,00,000 once | Stage 1 | plan 03 §C3 (**estimate**, quote needed) |
| Regulatory consultant | ₹0–65,000 once for a written answer on device class and study permission (₹0 = MedTech Mitra, a no-fee route for putting questions to CDSCO); ₹50,000–3,00,000 once for the licence | Stage 1; Stage 2 | plan 03 §C3, Stage D (**estimates**, quotes needed) |
| Quality system and technical file | ₹1–5 lakh once | Stage 2 | plan 03 Stage D (**estimate**, quote needed) |
| Outside security test | ₹40,000–3,50,000, then yearly | Stage 2 | plan 03 Stage D (**estimate**, grade C) |
| Clinical adviser | ₹0, or quote needed if paid | Stage 1 | plan 03 §C4. Never pay a clinician at the pilot hospital |

**What this says:** plan 03 §3 finds that one hospital never pays for itself, and that at about ₹1,000 an episode the lent model earns more than it costs from about 10 hospitals, **before salaries**. So Stage 2 hires would have to be funded by grants (B3-16: ₹20–60 lakh at 12–24 months, team estimate; "we will apply", not "we will get").

## 9. Hiring order and triggers
Each hire follows an event, not a date. Until then the role stays a founder hat. Triggers 1–2 follow the repo; 3–5 are ours. Before any hire: a letter covering pay, hours, confidentiality and IP assignment, and a one-page harassment-prevention policy (plan 06 L-23).

| # | Role | Trigger | Why then | Source |
|---|---|---|---|---|
| 1 | Quality and regulatory lead | The founders decide to charge a hospital | Charging is a sale: it needs a licence and a quality system, and the quality system takes months | B4 §10 steps 12–13; plan 06 Gate 2 #24–25 |
| 2 | Backend engineer who shares on-call | Hospital 2 signs | Hospital-by-hospital data separation, a rehearsal copy and an on-call rota all start here | FA §14 |
| 3 | Hospital success lead | Hospital 3 signs | Travel reaches ₹30,000–1,00,000 a month at 10 hospitals (estimate); each new hospital is a 13-step journey | plan 03 §3; plan 05 E-3 |
| 4 | Support and device coordinator | About 500 episodes a month (≈ 42 support hours, derived) or about 300 units in the field | Founders can no longer answer nurses and track units as a side task | plan 03 §3 (30 units a hospital) |
| 5 | Clinical lead (the adviser joins the staff) | The licence file is being written, or a second use begins | Clinical evaluation, usability tests and alert rules need a daily owner | FA §10; plan 05 E-20 |

## 10. Today against the plan
| Area | Today (11 Oct 2026) | Gap |
|---|---|---|
| Company | None registered (plan 06 Gate 1 #10) | None yet: the advice is to wait (B3-15) |
| Team | A founder team. Names, size, college and state are not in the repo (plan 00 §F) | Founder to fill; no hat has a name |
| Founders' agreement, IP assignment, college and hackathon ownership terms | Not started (plan 06 Gate 0 #1–4) | Do now; ₹0 |
| Product | Software: Live, fictional patients. Unit: Simulated; no hardware today (plan 00 item 12) | A real unit (plan 03 Stages A–B) |
| Clinical adviser | None recorded. No user interviews done as of 10 Oct evening (plan 00 item 28) | Find one |
| Quality owner and quality system | Not started (plan 06 Gate 2 #25) | Name the hat now |
| Company secretary or CA, lawyer, regulatory consultant | None engaged | plan 06 lists questions for an opening paid hour with each |

**Three things to do now**
1. **Sign a founders' agreement with IP assignment**, and get the college's and the hackathon's ownership terms in writing. Cost: ₹0 (plan 06 Gate 0 #1–4).
2. **Put one name against each hat** in the Stage 1 tree, including the quality owner and the person who receives safety reports. One person may hold several hats.
3. **Find two outside people:** a nurse or physiotherapist, not from a future pilot hospital, to agree the alert rules (B3-16); and a company secretary or CA for the questions in plan 06 (its question lists for each adviser). In the same week, ask the incubator its three questions in writing (B3-12).

## 11. Sources
All are files in this repo; no web page was opened. Many legal items are marked "NOT CONFIRMED" in their source file (plan 06 L-14, L-23; B3-15 costs; B3-16) and are repeated here with that caution.
- `docs/research/business/03_scale_funding_unit_economics.md`: B3-12, B3-15, B3-16, "First 90 days" (B3-6 only as quoted in plan 03 §3) · `04_legal_and_regulatory.md`: "Answer in 10 lines", B4-5, B4-13, B4-16, B4-19, section 10
- `docs/plan/00_FOUNDER_NOTES.md`: items 12, 28; §F · `03_COSTS_AND_BUDGET.md`: header, §C3, §C4, Stage D, §3 · `05_EXPANSION_AND_CUSTOMERS.md`: E-3, E-20 · `06_LEGAL_DEEP_DIVE.md`: L-14, L-17, L-23; "Master legal checklist", Gates 0–4 · `11_HOME_RECOVERY_COMPANION.md`: section H
- `docs/FUTURE_ARCHITECTURE.md`: §2.4, §3.4, §3.7, §6.3, §6.4, §8.3, §8.5, §9.1, §10, §13, §14 · `docs/DEVICE_LIFECYCLE.md`: §5.1 · `docs/SCALING_AND_COST.md`: §4, §7 · `docs/INTEROPERABILITY.md`: §4, §6, §7
