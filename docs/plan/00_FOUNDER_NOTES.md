# Founder notes – what was asked for, in the founder's own terms

**Saved:** 10 Oct 2026, evening. **Why this file exists:** the founder asked that everything said in this conversation be written down *before* any planning, so that future research and planning starts from the real requests and not from someone's summary of them. Add to this file; do not rewrite earlier entries.

Each entry: what was said (lightly tidied), then the status on 10 Oct 2026.

---

## A. The product, as the founder now sees it

1. **An Android app that people download, which connects to the device over Bluetooth.**
   Status: not built. Today there is an installable *mobile web app* (`web/app.html`) with no Bluetooth; the device is simulated and the only real link is a USB cable.
2. **"Every time the Bluetooth is on, it connects automatically."** No pairing steps each time.
   Status: not designed in detail. `docs/DEVICE_LIFECYCLE.md` recommends Bluetooth to a phone for the pilot.
3. **"We will need something to detect that the device is turned on. How can that be done? We did not think of that."**
   Status: open question. Nothing in the hardware or firmware handles power state, sleep, wake or "is the unit on?".
4. **Publish in the Play Store and the Apple App Store**, and know what that costs ("that's going to be another extra payment").
   Status: not researched.
5. **Two ways to offer the device:** (a) sold as a complete device; (b) lent and shared between patients. "It should swap the software as well as all the settings when it is configured to another patient."
   Status: researched. `docs/DEVICE_LIFECYCLE.md` (settings live with the patient record; a nurse "assigns" a unit) and `docs/research/business/06_sell_vs_share.md`.
6. **"How does the login work? How is everything connected? Bluetooth, cable? What's the whole process? I don't know."**
   Status: answered in `docs/DEVICE_LIFECYCLE.md`; nothing of it is built (no login, no device list, no assignment record).
7. **Price idea: "Can we give it plus the software for ₹200?"**
   Status: researched. ₹200 cannot cover a sold device or (today) a lent one; it works as a per-patient software fee on a unit the hospital owns, at scale (`06_sell_vs_share.md`).
8. **"How big a client base are we looking at, daily, monthly and yearly?"**
   Status: estimated in `docs/research/business/01_customers_and_market.md`; rests on an unpublished share of operations that use a spirometer.

## B. The hardware

9. **"Go through the hardware again and make sure that is the best we can use right now, and the most compact."**
10. **"We don't want it to break the second time."** Durability matters: it will be handled, carried home, cleaned and re-issued.
11. **"Look into the future scope: after one year, what if better technology arrives? Do a thorough check."**
    Status of 9–11: to be answered in `docs/plan/01_HARDWARE_REVIEW.md`.
12. **The team has no hardware at all today.** The device in every demo is a simulator and a 3D model.
13. **A human figure in the videos** "so it looks realistic": done as a simple outline figure in the tour video (a realistic 3D person was judged not worth it).

## C. The business

14. **"This is supposed to be a startup kind of idea, an MVP."** Research wanted on: how to scale, how to sell, who the customer base is, how sales start, legal topics, and "the connection of our app with ICMR".
    Status: `docs/research/business/` (six files and `BUSINESS_BRIEF.md`). ICMR does not approve apps or devices; there is no connection today.
15. **"How much are we expected to pay to get this out? How much are we expected to spend in the pilot stage?"** Every payment, itemised.
    Status: to be answered in `docs/plan/03_COSTS_AND_BUDGET.md`.
16. **"Who are our customers going to be? Every minute detail."**
    Status: first pass in `01_customers_and_market.md`; to be deepened in `docs/plan/05_EXPANSION_AND_CUSTOMERS.md`.
17. **"How can we expand?"**
    Status: to be answered in `docs/plan/05_EXPANSION_AND_CUSTOMERS.md`.
18. **"How much stuff did we miss? Plan everything, every single detail. If you think we are missing anything, note it and research it."**
    Status: to be answered in `docs/plan/04_GAPS_AND_RISKS.md`.

## D. How the founder wants the work done

19. **Use several sub-agents, one per section, each writing its own detailed MD file.** "Do not worry about the usage. All out."
20. **Meta-prompt:** think first about how to research each topic well, then brief the agents.
21. **Order asked for:** (1) save these notes; (2) check the hardware; (3) then plan everything else.
22. **Standing preferences (from earlier sessions):** plain, short English for a smart non-engineer; lead with the answer; say clearly what is done, what failed and what is waiting; explore fully before narrowing; one design palette; the patient side must be effortless for elderly users; a quality check after each agent; never re-open a web page already in the source ledger.
23. **Private material stays private:** the repo is public; details from the team's private WaBI code must not be published.

## E. The hackathon (context for all of the above)

24. Social Impact Hackathon 2026 (Cloud Counselage × DTI), 10–11 Oct 2026, online. Track: Health & Well-being.
25. **Submission by Sun 11 Oct, 3:00 pm:** pitch deck file (organisers' template), prototype link, demo video file (MP4, under 100 MB, English or Hindi), a ZIP of the code, a one-line description (200 characters), team details. Then a 5-minute pitch.
26. The form asks: "Would you like to convert your idea into a startup?" The founder is treating it as one.
27. **The founder will record the demo video and do the voice-over personally.** Everything needed must be on screen. Shot list: `docs/hackathon/DEMO_VIDEO_SHOTLIST.md`.
28. The organisers expect at least 3 user interviews per team. **None done as of the evening of 10 Oct.** Guide: `docs/hackathon/INTERVIEW_GUIDE.md`.

## F. Still open with the founder (not answered in this conversation)

- The team's names, the leader's email and mobile number, and the college (needed for the form, for grant eligibility and for the "who owns student work" question).
- **Which state the team lives in** (decides the first hospitals and the state grants).
- Whether any nurse, physiotherapist, doctor or patient has been interviewed.
- The organisers' pitch deck template (in their Google Drive; not yet in the repo).
- Whether to show a mock "Units" screen (assign → return → re-assign) in the demo video.
- Whether the Sarvam key has been added on Render (the live site uses pre-recorded clips without it).
