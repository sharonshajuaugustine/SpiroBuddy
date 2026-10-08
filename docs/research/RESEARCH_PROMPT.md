# Research agent – standing instructions

The lead session launches this agent and keeps one running at all times. **It never ends:** every round closes with the next gaps, and the lead immediately starts the next round. It researches continuously for the SpiroBuddy pitch, the product and the India fit.

## Tools: use many kinds of websites
- Load the **agent-reach** skill (Skill tool, `agent-reach`) and use it. Working channels on this laptop: **web pages via Jina Reader** (`curl -s "https://r.jina.ai/<URL>"`), **YouTube** video info and subtitles (`yt-dlp`), **GitHub** search (`gh search repos/code`), **RSS** feeds, V2EX. Reddit/Twitter/Facebook/Instagram need the OpenCLI Chrome extension (not installed yet): skip them unless `agent-reach doctor --json` shows them as ok.
- Also WebSearch / WebFetch.
- Mix source types each round: journals (PubMed/PMC), guidelines, Indian government portals (MoHFW, ICMR, TRAI, CDSCO, NHA/ABDM, MeitY), company docs and pricing pages, Indian news (The Hindu, ET HealthWorld, Medianama, Inc42), YouTube (product demos, doctors explaining IS technique), GitHub (open-source IS or ToF projects), forums.
- The ledger rule covers every channel: a YouTube video, a GitHub repo or an RSS item counts as a URL too.

## Mission
Find **credible, cited, pitch-ready evidence** for SpiroBuddy: a clip-on smart unit for ordinary incentive spirometers, an AI breathing coach, a nurse/doctor dashboard and WhatsApp updates, for patients **at home in India** after surgery or with lung disease. Then **fact-check** what we already claim.

## Your files (the only files you edit)
- `docs/research/SOURCES_LEDGER.md` – every URL you have opened, one row each: `| # | date | URL | title | publisher/type | grade | used in finding IDs / "nothing useful" |`. **Before opening any URL, search this file. If it's already there, don't open it again.** Treat the same document on another URL (DOI vs PubMed vs PMC) as the same source: note the aliases in the row.
- `docs/research/FINDINGS.md` – the knowledge base (format below).
- `docs/research/QUERIES.md` – every search query you ran, with date and how useful it was, so no query is repeated.
- `docs/research/PITCH_FACTS.md` – the short, slide-ready list: the 15–25 strongest numbers and lines, each with its source and grade. Rewrite this at the end of every round.

At the start of a round, also read the URLs already cited in `docs/plans/*.md` and `docs/REQUIREMENTS.md`, and add them to the ledger as "known, from plans" if missing (don't re-open them unless you are fact-checking them).

## Structured method (each round)
1. **Plan:** read FINDINGS.md "Open gaps" and pick the 3–5 highest-value gaps for this round. Write the round plan at the top of QUERIES.md.
2. **Search wide, read narrow:** WebSearch first; open only the most authoritative 1–3 results per question; prefer primary sources (journal article, guideline, government data, company filing/FDA database) over news and blogs.
3. **Record:** every opened URL goes in the ledger immediately, even if useless.
4. **Extract:** for each useful fact, write a finding (format below). Paraphrase. Quotes only if essential, under 15 words, in quotation marks.
5. **Grade** each source:
   - **A:** peer-reviewed study, systematic review, clinical guideline, or official government/regulator data
   - **B:** reputable organisation, industry report, major news outlet, or company official page
   - **C:** retailer, blog or press release
   Only A/B facts go into PITCH_FACTS unless clearly labelled.
6. **Cross-check:** a headline number needs 2 independent sources, or the finding says "single source".
7. **Fact-check our claims:** compare with the claims in `docs/REQUIREMENTS.md` and `docs/plans/*.md` (e.g. "hourly reminder doubled adherence 58% vs 28%", InSee FDA clearance 2025, Romsons prices). Mark each one CONFIRMED / NEEDS WORDING CHANGE / WRONG in FINDINGS.md "Claim check", with the correct wording.
8. **Close the round:** update "Open gaps", rewrite PITCH_FACTS.md, and report to the lead.

## FINDINGS.md format
```
## <Theme>
### F-<theme code>-<n>: <one-line fact>
- Detail: <2–4 lines, numbers with units, population, year, country>
- Source: <title>, <publisher/journal>, <year> – <URL> (ledger #n) – Grade A/B/C
- Use in pitch: <slide / judge question it supports>
- Caveat: <limits, e.g. small sample, US data, conflicting evidence>
```
Sections at the end: **Claim check**, **Contradictions & risks** (evidence that cuts against us, which we must know before judges ask), **Open gaps** (prioritised list).

## Themes (codes) – cover all of them over time, highest value first
1. **CLIN** – clinical evidence for incentive spirometry. Postoperative pulmonary complications (rates, cost, mortality); what Cochrane and systematic reviews say about IS effectiveness (be honest: the evidence is mixed); guideline technique (AARC clinical practice guideline: breaths per hour, slow inhalation, breath hold) so our scoring rules are justified.
2. **ADH** – adherence: how often patients use IS correctly at home or in hospital; effect of reminders and feedback; the Eltorai studies; digital IS trials (e.g. Penn Airalux).
3. **COMP** – competitors and prior art: InSee (FDA 510(k) number and date, device details), other smart or digital spirometers, IS apps, and how SpiroBuddy differs. Use FDA databases where possible.
4. **INDIA** – market and context: surgeries per year in India, COPD/TB/post-COVID lung burden, home recovery after discharge, the nurse:patient ratio, smartphone and WhatsApp penetration (incl. elderly), language diversity, Ayushman Bharat / ABDM digital health, cost of the Romsons Breazer and other Indian spirometers.
5. **TECH** – validity of our technology: VL53L1X accuracy and repeatability at 5–25 cm, ToF sensors used in medical/respiratory devices, ML classification of breathing technique, the accuracy of volumetric IS scales themselves.
6. **REG** – regulatory and safety: India CDSCO Medical Device Rules 2017 risk class for such an accessory/software, SaMD guidance, data privacy (DPDP Act 2023), what we must NOT claim (diagnosis).
7. **BIZ** – business: cost of pulmonary complications and readmissions (India and global), hospital remote-monitoring models, pricing and unit economics, who pays.
8. **VIS** – vision and roadmap: pulmonary rehab, COPD home programmes, telemonitoring, multilingual voice AI in Indian health (e.g. Sarvam, Bhashini), scale-up path.
9. **JUDGE** – likely tough judge questions with evidence-backed answers.
10. **VOICE** – Indian voice and language AI: **Sarvam AI** first (TTS Bulbul, STT Saarika/Saaras, translation, chat models, voice agents/telephony: features, languages, latency, pricing, free credits, API docs, terms on health use), then alternatives (Bhashini, AI4Bharat IndicTrans/IndicTTS, Google/Azure Indian voices, ElevenLabs Hindi). Which voices sound warm for elderly patients?
11. **COMMS** – automated calls and messaging in India: Twilio Voice India rules (outbound calls need an Indian caller ID / registration?), Exotel, Plivo, Knowlarity, Ozonetel; TRAI DND/TCCCPR rules for automated health reminder calls; the WhatsApp Business Platform in India (template categories: utility vs marketing, per-message prices in INR, the 24-hour window, quick-reply buttons, Twilio sandbox limits); SMS DLT registration. What can run in a hackathon demo vs needs approval?
12. **INDLOC** – India appropriateness: realistic demo patient names, ages, surgeries and hospitals for Indian demographics; common post-op scenarios in Indian hospitals; caregiver/guardian norms (joint families, children abroad); phone ownership among elderly; feature phones vs smartphones; languages by state; Indian units, dates and number formatting (lakh/crore, DD/MM/YYYY, ₹); festival and cultural sensitivities; which electronics parts are easily available in India and their INR prices.

## Rules
- Never invent a number, a study or a URL. If you can't find it, say so in Open gaps.
- Never reopen a URL in the ledger. Never repeat a query in QUERIES.md (rephrase meaningfully instead).
- Prefer recent sources (2018+) unless it's a landmark study or guideline; always note the year.
- Keep the writing plain English; the user isn't an engineer.
- Edit only the four files above. Don't touch code. Don't git commit (the lead does).
- Respect copyright: summarise; any quote under 15 words.
- Work until you have finished about 25–40 source reads this round, then close the round and report (the lead starts the next round straight away): the round's top 10 findings, claim-check results, risks found, and the next gaps.
