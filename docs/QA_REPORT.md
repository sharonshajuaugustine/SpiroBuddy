# QA report – quality & efficiency controller

**Last reviewed commit:** `f91b58f` (Review 2, 10 Oct 2026) + the doc fixes listed in Review 2 (not committed). Review 1 was `23d8b0b`.
Severity: 🔴 blocks the demo · 🟠 fix before the demo · 🟡 later.

---

## Review 1 – baseline (9 Oct 2026, ~23:45 IST)

**Scope:** whole project, cheaply (git log, file lists, targeted reads, browser spot-check on port 8004). Code had not changed since `a3f7a76` (61 tests passed); only docs changed in `23d8b0b`.

### Verdict
The demo story works end to end in dry-run mode. No 🔴 blockers. Five 🟠 items, mostly India-fit and one safety seam in the old WhatsApp summary path.

### What was checked

| Area | Result | Notes |
|---|---|---|
| Dashboard `/` | ✅ pass | Live update, alerts inbox, chips, red/amber/green with "why" lines. No console errors. |
| Demo panel: simulate good / 2 missed / send summary | ✅ pass | Activity log: "slot 21:00 done, avg 7.8/10", "2 slots marked missed", "would send". |
| Escalation ladder (fast-forward) | ✅ pass | Beep → patient WhatsApp → call → guardian WhatsApp + call → nurse alert. AI disclosure in every message. |
| Replay webhook (pain + red flag) | ✅ pass | Neutral nurse note, patient's own words stored separately, fixed 112 message, red-flag ladder bypasses quiet hours. |
| Phone simulator keypad / conversational | ⚪ not clicked by hand | Covered by tests (`test_comms.py`); ladder shows calls ringing in the simulator. Person check still needed (TEST_PLAN L2). |
| WhatsApp simulator | ✅ renders | Hindi quick replies (✅ हो गया / ⏰ 15 मिनट बाद / 📞 मुझे कॉल करें). Typed replies not clicked. |
| Patient page | ✅ pass | Slots, 7-day chart, template summary in Hindi, "DRY RUN – would send" clearly shown, check-in notes, care-team actions. |
| Guardian page (375 px) | ✅ after fix | Giant status, Call Papa, cheer, ticks, quiet hours. Some text was 13–17 px → fixed to 20 px (see fixes). |
| Collect page | ✅ loads | Simulator running, no console errors. |
| 3D showroom `/showcase/` | ✅ loads | Renders; two stray `console.log` lines from showcase.js. Videos not replayed (checked earlier by lead + 3D agent). |
| Phone width 375 px | ✅ after fix | Dashboard alert tabs overflowed by 53 px → fixed. Patient, demo, collect, showcase: no overflow. |
| Never diagnose | ✅ pass | LLM + call-script prompts forbid diagnosis; trend flag worded as "observation, not a diagnosis"; footers say "does not diagnose". |
| Red flag → fixed message | ✅ pass | Same 112 text in 11 languages (voice_cues) and in comms. |
| AI disclosure | ✅ mostly | Calls start "automated care assistant"; comms WhatsApp adds a footer. ❌ The old `/api/whatsapp/{pid}` summary path has no disclosure (see 🟠-3). |
| Consent before real calls + 7-day renewal | ✅ pass | `calls.py:240` skips calls with no consent; `calls.py:251` blocks real calls if consent > 7 days. Weekly renewal message exists. |
| Quiet hours | ✅ pass | Per-guardian quiet hours; demo ladder says "quiet hours ignored for the demo" when the box is off; red flag always overrides. |
| Secrets | ✅ pass | `git grep` for key patterns: nothing. `.env` is git-ignored; only `.env.example` is tracked. |
| "Never say" claims | ✅ pass | None in web/, backend/, showcase captions or render tools. |
| Palette | ✅ pass | Only `#0b6e8a` / `#7fe0c8` hard-coded (logo SVG); everything else uses tokens. |
| Same words for the same cue | ✅ after fix | collect.html said "SLOWER!" → now "⚠ Slower…". |
| Oversized files | ✅ ok | Tracked total 38.7 MB: videos 32.6 MB (expected), GLB 3.9 MB, model.joblib 0.8 MB. DB, caches and frames are ignored. |
| Stray processes | ⚠ report | A uvicorn on **port 8003** (PIDs 43052 / 41828, the comms agent's test server) is still running. Safe to stop. Chrome processes belong to the user – not touched. |

### Issues

🟠 **1. Dates and times show in US format.** Every `toLocale…([])` call used the browser's locale, so the dashboard showed "Friday, October 9, 2026" and "Oct 8 08:05 PM". → **Fixed** (all web pages now use `en-IN`: "Friday, 9 October 2026", "11:42 pm", lakh grouping for numbers). Still open: hour slots show 24-hour "08:00–21:00" and guardian ticks "8 … 21" (HANDOFF asks for 12-hour) – queued Q-05.

🟠 **2. Browser cache hid code changes.** Static files had no `Cache-Control`, so after an edit the browser kept the old JS even on Ctrl+Shift+R. This can make a fixed bug "come back" during rehearsal. → **Fixed** in `backend/app/main.py:47` (`Cache-Control: no-cache` on non-API files; still cheap 304s via ETag).

🟠 **3. The old WhatsApp summary path skips consent, the AI disclosure and the footer.** `backend/app/main.py:236` (`/api/whatsapp/{pid}`, used by "Send summary" on the demo panel and patient page) calls `whatsapp.send()` directly, not `comms/messages.send()`. Text is just "SpiroBuddy - Ravi: …". With real Twilio keys, a family member who said STOP would still get it. → Queued Q-01 (route it through `messages.send` + the consent check).

🟠 **4. Event status "warn" was labelled "NO ANSWER" everywhere.** Red flags, trend flags and check-in results all showed a "NO ANSWER" chip in the live comms feed (`web/js/comms.js:113`). Wrong in front of judges. → **Fixed**: shows "⚠ needs a look", and "no answer" only when the event really is a no-answer.

🟠 **5. Guardian page below the 20 px / 64 px rule.** Header subtitle (the "automated updates" notice) 12.8 px, language buttons 16.8 px / 56 px tall, hour ticks 14.4 px, footer 14.4 px, quiet-hour buttons 17.6 px. → **Fixed** in `web/css/styles.css:503–534` (all 20 px, language buttons 64 px).

🟡 6. **"▲ Improving" next to "Needs a call".** Abdul and Mohan (0 of 14 done) show "TREND ▲ Improving" because the trend is the 3-day best-breath volume (`backend/app/service.py:114–119`) and ignores today's misses. Confusing on screen. → Q-06 (label it "Volume (3 days)" or blank when today has no sessions).

🟡 7. **Priya shows "On track" with an open red-flag alert.** Status colour comes only from sessions; an open red-flag alert doesn't turn the card red. Defensible (alerts inbox is separate) but a judge may ask. → Q-06.

🟡 8. **Two red-flag lists.** `backend/app/voice.py` `RED_FLAG_WORDS` (11 languages) and `backend/app/comms/messages.py:202` `RED_FLAG_RE` (en/hi/ta + romanised). They are OR-ed together everywhere, so nothing is missed, but a new word must be added in two places. → Q-10 (merge after the demo).

🟡 9. **Two WhatsApp senders.** `backend/app/whatsapp.py` (summary/missed) and `backend/app/comms/messages.py` (everything else, which calls `whatsapp.send` underneath). Fixing 🟠-3 removes most of the duplication.

🟡 10. **Voice preset differs from the research checklist.** Default pace 0.9 (`backend/app/voice.py:90`, `.env.example:18`) vs 0.85; no `temperature` 0.7; English/Tamil default speaker is "ishita", Hindi "priya", Malayalam "pooja" ✓. → Q-07.

🟡 11. **Demo patients don't match the India-fit list.** No woman 60–68 after knee replacement and no man ~50 in post-TB rehab; Lakshmi (72, hip) is close. No Malayalam-speaking patient although Malayalam is a showcase language. → Q-08.

🟡 12. **Wording: "clip-on" vs "base unit".** CLAUDE.md/REQUIREMENTS say "clip-on unit"; the 3D model and videos show a base the spirometer stands on. Pick one word for the pitch. → Q-12.

🟡 13. **Stale docs.** `docs/HANDOFF.md` still says "5 subagents started"; PROGRESS.md has no entries for 3D, comms, tests or research rounds 2–3. A fresh session would be misled. → Q-02 (lead).

🟡 14. **Replay sample label names Ravi even when replayed for another patient** ("Ravi: mild pain…" on Arjun's timeline). Cosmetic. → Q-11.

### Small fixes made in this review (not committed)
1. `web/js/*.js`, `web/*.html` (10 files): `toLocale…([])` → `toLocale…('en-IN')`; `toLocaleString()` → `toLocaleString('en-IN')`.
2. `web/js/comms.js:113–117`: "warn" chip label → "⚠ needs a look" (or "no answer" when the event says so).
3. `backend/app/main.py:47–54`: middleware adds `Cache-Control: no-cache` for non-`/api` paths.
4. `web/css/styles.css:159`: `.seg` gets `max-width:100%; overflow-x:auto` (dashboard tabs no longer push the page wider than a phone).
5. `web/css/styles.css:503–534`: guardian header, language buttons, ticks, choices and footer at 20 px; language buttons 64 px.
6. `web/collect.html:40` + `docs/TEST_PLAN.md:66`: "SLOWER!" → "⚠ Slower…".
7. (After research round 4, lead's request) `firmware/spirobuddy_serial/spirobuddy_serial.ino:29`: `VL53L1X_ROI_SIZE` default 8 → 4 (4×4 centred, centre 199 unchanged); `docs/HARDWARE.md:194,225` updated, matte target added. Not compiled (no toolchain/hardware); a constant change only.

Round 4 items folded into WORK_QUEUE as Q-22 (done), Q-23 calibration table, Q-24 CDSCO "care-team mode" wording, Q-25 human-call-first wording, Q-26 capped research round 5, Q-27 deferred research; hands-on checks added to "Waiting on the user" (7, 10, 11). Quick grep: no disease/complication names in patient- or guardian-facing text (guardian page, voice cues, WhatsApp, call scripts).

### Tests
`pytest tests -q` re-run after the fixes (backend file changed): **61 passed in 4 min 30 s.** ML not re-trained (`ml/` unchanged).

### Waste found
- Port-8003 test server left running by the comms agent.
- Leftover `console.log` in `web/showcase/showcase.js` (harmless).
- `.claude/launch.json` has an uncommitted reformat + a "comms-test-8003" entry: fine to commit or drop; add "qa-8004" only if useful.
- No agent is re-doing finished work. The research ledger has 142 entries and the round-3 gaps don't repeat round-2 sources.

---

## Review 2 – Q-01, Q-03, research round 5 (10 Oct 2026, ~01:10 IST, HEAD `f91b58f`)

**Scope:** diff `23d8b0b..f91b58f` (code: `main.py`, `comms/messages.py`, `voice.py`, `seed.py`, `seed_comms.py`, `supabase/seed.sql`, `llm.py`, web time labels), live API check on port 8010 (server stopped afterwards; no stray servers on 8000/8003/8004/8010). Web agent's in-progress Q-06/Q-23 files (`ui.js`, `service.py`, `index.html` cards) not reviewed.

### Verdict
Q-01 and Q-03 meet their "done when". No 🔴. One 🟠 (wording in the pitch plans, fixed). New 🟡s queued.

| Check | Result | Notes |
|---|---|---|
| Q-01 summary goes through comms sender | ✅ | `main.py:246–257` → `messages.care_update_recipient` + `send_care_update`. Live: Ravi's family summary in Hindi with "स्वचालित देखभाल सहायक" disclosure + footer; nurse "missed" alert works (staff, not covered by family STOP). |
| Q-01 STOP blocks + test | ✅ | `tests/test_comms.py::test_whatsapp_summary_endpoint_respects_consent_and_discloses`; blocked → `sent:false, dry_run:false, blocked, error`, nothing logged as sent. |
| CONTRACT D shape | ✅ (doc updated) | Returns `{sent, dry_run, text, to_role}` (+ `blocked`, `blocked_reason`, `error` when blocked). ARCHITECTURE row still said `{sent, dry_run, text}` → **fixed** (additive, UI unaffected). |
| Q-03 12-hour times | ✅ | Dashboard "slots 8 am–9 pm" via `hourRange`, patient page "8 am–9 pm", guardian ticks 12-hour (`guardian.html:99`); API keeps 24-hour numbers. |
| Q-03 demo patients | ✅ | After **Reset demo data**: Abdul 63 CABG (red), Lakshmi 66 knee (yellow), Priya 44 cholecystectomy, Mohan 50 post-TB (red), **Sreedevi Nair 54, Malayalam** (green, husband Gopakumar `ml`, daughter in Dubai with quiet hours). Ids 1–7 kept; `seed.sql` matches. All fictional. |
| Q-03 voice preset | ✅ not guessed | Pace 0.85, temperature 0.7 (clamped 0.01–1.0, sent only to bulbul v3/v4-flash, part of the cache key). Cited: `docs/VOICE.md:28` from docs.sarvam.ai TTS convert page + KNOWLEDGE_BASE F-VOICE-11 (Sarvam's "warm 0.7–0.8"). `/api/voice/status` shows both. |
| Disease names kept out of family text | ✅ | `llm._prompt` no longer sends the operation; `_DIAGNOSIS_WORDS` adds tuberculosis/TB/cancer. Call script (nurse-facing) still gets the surgery – fine. |
| "Never say" grep (web, backend, docs excl. research) | ✅ | "FDA" appears only as facts about InSee (competitor) and in the never-say lists. No "reduces readmissions", "first AI", "no licence needed", "prevents pneumonia" (except the never-say table), "clinically proven". |
| CDSCO wording (round 5 URGENT) | 🟠 → fixed | Plans said "We couldn't confirm the class". |
| Endpoints smoke | ✅ | health, patients, patient detail, simulate, messages, model, comms/status, voice/status, sessions; pages `/`, patient, guardian, demo, collect, showcase all 200. Server log: no errors. |
| Tests | ⚪ not re-run | No code changed in this review; lead reports 62 passed at `f91b58f`. Web agent's files are mid-edit, so a run now would test their WIP. |

### Issues
🟡 15. **Malayalam family gets English.** Sreedevi's husband (`ml`) receives the summary, disclosure and footer in English, because comms has no Malayalam text (`comms/common.py:32` maps `ml` → `en` on purpose – better than Hindi). Malayalam is a showcase language → Q-28.
🟡 16. **"0 of 0 sessions today" before 8 am.** A summary sent at night reads oddly; also "SpiroBuddy - Ravi Kumar:" repeats the brand after the disclosure line → Q-29.
🟡 17. **Q-01/Q-03 had no PROGRESS line and HANDOFF wasn't refreshed** in `f91b58f`. PROGRESS line added now; HANDOFF → Q-30 (lead, at next commit).

### Small fixes made (not committed)
1. `docs/plans/SpiroBuddy_Complete_Plan.md:633,635,791` and `docs/plans/SpiroBuddy_Final_Research.md:47,89,91`: "couldn't confirm the class / get a ruling" → "The plain spirometer is CDSCO Class A (lowest risk, not diagnostic). Our measuring clip-on will need its own registration and licence." (judge answers aligned).
2. `docs/ARCHITECTURE.md` CONTRACT D `/api/whatsapp/{id}` row: real response shape + consent note.
3. `docs/PROGRESS.md`: Q-01/Q-03 line + Review 2 line.
4. `docs/WORK_QUEUE.md`: Q-01, Q-02, Q-03, Q-05, Q-07, Q-08, Q-24, Q-26 done; new Q-28–Q-30; new "Next".

### Waste
None found: no duplicate work, no stray servers. Q-01 also removed most of 🟡-9 (two senders) – `whatsapp.py` is now only the transport plus `missed_text`.
