# SpiroBuddy 2.0 redesign – build state (resume from here)

**How to resume:** when the founder says "continue the redesign" (or similar), follow **§R** of the spec `docs/private/ULTRACODE_BUILD_PROMPT.md` (a local file, not on GitHub):
1. Check the time.
2. Read this file.
3. Check the lock.
4. Check git, worktrees and branches; recover leftover work.
5. Do the **Next action**.

**Never restart from Phase 0 and never redo a `done` step.** Trust git over this file if they disagree, then fix this file.

**Deadline:** submission Mon 12 Oct 2026, 11:00 AM IST · **build freeze 03:00 IST Mon** · checkpoints in spec §1.

**Status words:** `todo` · `doing (<session>, <IST time>)` · `done (<commit>)` · `blocked (<why>)` · `dropped (<why>)`. Add rows for new sub-steps, but never rename IDs.

---

## Now

- **Next action (for the NEXT session, on a fresh account – the founder has 4 more):** P0 is live (557857d) and docs were pushed after it. **IN PARALLEL FROM THE START: the pitch deck** from the organisers' template `DTI_SIH_Pitch Deck_Template.pptx` (repo folder, not committed; founder gave it at 00:45 IST) – one agent with the pptx skill, rules in CLAUDE.md 'Deck'; output a new file such as `docs/hackathon/SpiroBuddy_DTI_Pitch.pptx`; the founder checks it before submitting. **FIRST builder (founder, 00:20 IST): build the patient login with hospital registration number + PIN – brief: `docs/rebuild/REGNO_PIN_BRIEF.md`** (needs one more Supabase paste from the founder). **SECOND: branding lite** – each hospital's name + logo inside the patient app after login, admin 'App branding' card (plan: `docs/plan/12_HOSPITAL_ONBOARDING_AND_BRANDING.md` §6; founder ask 00:35). Then run **wave 2**, 2 builders + 1 checker at a time (founder's rule), builders on Sonnet. Reuse the prompts in `docs/rebuild/wave1_workflow.js` (COMMON rules + the VERIFY function):
  1. **Checker first:** verify-and-fix tonight's pages – story site (`/`, impact, trust, vision, architecture) and the digital prescription (`prescribe.html`, `meds.html`, `rx.html`) at 375/1440 px, light/dark, real clicks (the wave 1 checkers were stopped for usage before they reported).
  2. **Builder – medicine reminder:** a big "time for your medicine" card on Ravi's main screen (`app.html`) with Hindi voice + "I took it" (reported, never "taken"), using `backend/app/meds/service.py` (`today_doses`, `report_dose`); plus the missed-dose alert to the nurse (`doses.missed_alert`: after `grace_minutes`, an amber `missed_dose` alert in the comms alerts table; family notice only with consent). Flip `doses.reminders` / `doses.missed_alert` only when they work.
  3. **Builder – visit request (appointments lite):** Ravi taps "I want to see the doctor" → the doctor confirms a time on Ravi's staff page → Ravi sees it confirmed (Contract I subset; `appt.booking`).
  4. **Builder – public 3D twin page** `/twin.html` from the WIP `web/js/twin-model.js` (B8 brief in PHASE2_BRIEFS.md; `/showcase/` must keep working), then embed it on the landing hero.
  Then the full suite, the founder's "push?", push, live check, and the founder resets the demo. **Freeze 03:00 IST.**
- **Open founder questions (ask, don't assume):** (a) the founder asked "where is the SpiroBuddy part?" about the landing page – offer to make the spirometer the headline again ("Every breath, coached and counted") with the prescription as pillar 2; (b) **the deck: WAIT for the founder's Dolphin Tank slide template – do not make slides before it arrives** (PITCH_PLAN has only notes: slide 4b + the DTI logo/footer checklist); (c) the device is **not built yet** (founder, 00:00) – keep `device.*` In development, breaths Simulated; (d) the README disclosure sentence is the founder's to write; (e) the live demo reset after the 23:40 push (founder to do: log in as Doctor → `/demo.html` → Reset demo data).
- **Founder's wider vision (Mon 12 Oct ~00:15 IST) – ask the founder whether to build it in wave 2 before the other builders:** SpiroBuddy is for every hospital and clinic. Doctors and departments have their own logins; doctors type prescriptions; each patient's medicines are saved under their **hospital registration number**; the patient logs in with that number to see all their medicines; clinics without numbers get one from the app; nothing to do with money. Build suggestion: patient login = registration number + a 4–6 digit PIN printed on the discharge slip (an OTP needs a paid SMS service, so Simulated in the demo); a `registration_no` on each patient (additive column = a new Supabase paste for the founder); department accounts on top of the staff `department` field. Pitch: never say "no such software exists" (hospital-chain apps and ABHA health-locker apps exist); say "any hospital or clinic, elderly-first, in their language, shown at the pharmacy counter".
- **COVID source check (00:15):** no official Indian guideline found that recommends incentive spirometers for COVID (an NDMA May 2021 mention appears only in a market report, unverified). Safe line: incentive spirometry has been studied for post-COVID lung recovery (e.g. a 2024 randomised trial, 60 patients, PMC11182030); post-COVID lung rehab = a Planned segment. Never say SpiroBuddy was used in COVID.
- **Score estimate given to the founder (00:00):** about 70/100 on the Dolphin Tank criteria; biggest lifts = showing the prescription in video/deck (done in the plans: Shot 12b, slide 4b), a working prototype, the reminder loop.
- **Usage (Pro plan, 5-hour window resets 03:30 IST):** 75% used at 23:31 IST. The two verify agents were stopped at 23:32 to keep enough for the push; the lead checked the prescription path in the browser instead (patient app → My medicines in Hindi → pharmacy card → QR → public check says "Current"). A local DB made before the seed hook shows no medicines until **Reset demo data**.
- **Time note:** earlier entries in this session said 23:12 and 23:45; the real IST times were about 22:45 and 23:00 (the shell clock was read as UTC).
- **Founder decisions, Sun 11 Oct 22:55–23:05 IST (override the spec where they differ):**
  1. **Story site first**, then medicines. The account is a small Pro plan: at most about 4–6 agents until 03:30, so 2 builders + 2 verifiers.
  2. **Landing page at `/`; the nurse dashboard moves to `/dashboard.html`;** update the recording notes in `DEMO_VIDEO_SHOTLIST.md` ("Before you record", tab 5 and shot 9) to the new address and a "log in as Doctor" step.
  3. **Medicines = the doctor's prescription on the patient's phone, shown at the pharmacy counter, no paper.** It is **not** "AI reads a prescription photo" ("any AI could do that – that's not the app"). The doctor types the prescription in the hospital software → the patient sees every medicine on the phone → a "show at the pharmacy" screen with a QR the chemist can scan to check it. AI photo reading is at most a side helper (left In development); patient photo upload is Planned. Spec §8.7's Gemini pipeline is no longer the headline.
- **Honesty pass on `features.py` (23:10):** every feature that is not built yet now says In development (31 keys + 7 public pages), and a new test fails if a Live or Simulated badge points at a page that does not exist. Builders flip their own keys back only when the feature works. New keys: `rx.patient_phone`, `rx.pharmacy_screen`, `rx.verify_qr`.
- **Lock (active session):** none – session 7469796e (Pro plan) ended on purpose at about 00:05 IST Mon 12 Oct, with its usage nearly used up. The next session takes the lock. The previous session dd50472b's workflows ended at about 22:26 on its usage limit; no other session is running (checked).
- **Last heartbeat:** Sun 11 Oct 23:33 IST.
- **Schedule risk:** P0 was due 22:30 and Phase 2 is only starting now. Rule: ship only finished screens; everything else keeps its In development badge.
- **Last good commit before the redesign:** `4c78e46`
- **Live site** (https://spirobuddy.onrender.com): old version, not redeployed by the redesign yet

**Founder config** (tick when done; never ask again for a ticked item):
- [ ] Gemini API key added to `.env` (local)
- [ ] Gemini API key added on Render → Environment
- [x] `supabase/schema_v2.sql` pasted into the Supabase SQL Editor and run (founder, Sun 11 Oct about 23:15 IST: result "setval 1000", no error)
- [x] Push approved for P0 (founder, Sun 11 Oct about 23:35 IST: "yes, push when tests pass")
- [ ] Push approved for P1
- [ ] AIC server facts given (the fill-in table in `docs/SCALING_AND_COST.md` section 7d) – asked 11 Oct 18:20

---

## Steps

### Phase 0 – Map
| ID | Step | Pri | Status | Commit | Notes |
|---|---|---|---|---|---|
| P0-0.1 | Start-up check, lock, baseline full test suite (background) | P0 | done (e56411e) | e56411e | Baseline re-run 11 Oct 16:15 IST: 420 passed, 14 xfailed (9 min) |
| P0-0.2 | `docs/REBUILD_PLAN.md`: file ownership, risks, P0/P1/P2 list | P0 | done | e56411e+ | |
| P0-0.3 | Contracts E–K written into `docs/ARCHITECTURE.md` + PROGRESS note | P0 | done | e56411e | Must be done before Phase 2 |
| P0-0.4 | Gemini model + SDK version chosen from Google's docs, recorded in PROGRESS | P0 | done | e56411e+ | `gemini-3.1-flash-lite` (founder's choice), google-genai 2.29.0 |

### Phase 1 – Foundations (one builder, sequential)
| ID | Step | Pri | Status | Commit | Notes |
|---|---|---|---|---|---|
| P1-1.1 | Config + env names (`.env.example`, `render.yaml`, `config.py`), `ALLOW_TRAINING`, `SHOW_API_DOCS` | P0 | done (a02ed99) | a02ed99 | Recovered on resume; tests green |
| P1-1.2 | `supabase/schema_v2.sql` (additive) + SQLite tables + store additions + "v2 tables missing" fallback | P0 | done (a02ed99) | a02ed99 | Recovered on resume; test_store_v2 + test_supabase_store + test_api = 57 passed |
| P1-1.3 | `authz.py`, middleware policy, auth endpoints, sessions, CSRF header in `api.js` | P0 | done (bdcf467) | bdcf467, f1385ce, 1e5f193 | auth agent; the api.js CSRF header is in WIP 8ebc65d (the kit agent finishes it) |
| P1-1.4 | Audit writer, `ai_events`, `features.py` + `GET /api/features` | P0 | done (4b1c899) | bdcf467, 4b1c899 | audit = auth agent; features + ai_events = platform agent |
| P1-1.5 | Gemini wrapper (limits, fallback, logging) + storage wrapper (Supabase bucket auto-create + local) | P0 | done (4b1c899) | 4b1c899 | platform agent |
| P1-1.6 | Seed v2 (both demo hospitals, staff, keys, prescriptions, doses, visits, documents, devices) + `tools/demo/make_samples.py` | P0 | partly done: hospitals, staff, keys (bdcf467); demo prescription seeded by builder B; visits, documents, devices dropped with their features | f7310d1 (samples) | Sample files done (f7310d1); seed v2 = seed2 agent |
| P1-1.7 | `conftest.py` under auth; old suite green; new auth, role and isolation tests | P0 | done (02d913f) | bdcf467, f1ecdc7, 02d913f | Full suite 23:00: 648 passed, 1 order-dependent failure fixed in f1ecdc7. Comms isolation + tests/test_isolation.py in 02d913f. Left (P1): `POST /api/voice/stt` form patient_id not checked |
| P1-1.8 | Phase 1 verify (2 skeptics) + commit | P0 | dropped (usage; replaced by a browser check 22:50: login, dashboard and patient app work under auth) | | |

### Phase 2 – Features (builders own disjoint files; the lead applies `docs/rebuild/<builder>_integration.md`)
| ID | Builder / item | Pri | Status | Commit | Notes |
|---|---|---|---|---|---|
| P2-B1a | Login, signup (join code), nurse key redeem pages | P0 | todo | | |
| P2-B1b | Hospital shell, role-aware home, staff, settings, join code, keys pages | P0 | todo | | |
| P2-B1c | Demo controls page (new buttons + "Prepare for recording") | P0 | todo | | |
| P2-B1d | Governance: consents overview + AI register (P0); audit viewer + pilot checklist (P1) | P0/P1 | todo | | |
| P2-B2a | Triage list + patient chart header + tabs (Overview, Breathing, Medicines, Visits, Papers, Care team & consent, Notes, Timeline, Device) | P0 | todo | | |
| P2-B2b | Enrol wizard + printable patient handout with QR | P0 | todo | | |
| P2-B2c | Prescription review screen (photo + lines, unclear in amber, confirm all → approve, warnings) | P0 | todo | | |
| P2-RX | **Digital prescription (founder, 23:00):** doctor types it → patient phone → pharmacy-counter screen + QR check | P0 | done (90f0bc3) | 5b0aecd, 90f0bc3, c7fe3f4 | Replaces B3's photo pipeline as the headline |
| P2-B3a | Normaliser (`backend/app/meds/normalise.py`) + full table tests | P0 | todo | | |
| P2-B3b | Prescription pipeline: typed / doctor upload / patient upload / manual; approve, stop, version | P0 | todo | | No dose events before approval (test) |
| P2-B3c | Dose events, grace → missed → `missed_dose` alert, family notice with consent | P0 | todo | | |
| P2-B3d | Medicine reminders in the phone and WhatsApp simulators; Web Push; offline "I took it" queue | P1 | todo | | |
| P2-B4a | Availability, slots, no double booking, request → confirm/propose/decline, attended/no-show | P0 | todo | | |
| P2-B4b | Visit reminders (in-app P0; simulators P1) | P0/P1 | todo | | |
| P2-B5a | Document vault: upload validation, re-encode, permission-checked file fetch, visibility flags, AI type/title/date suggestion | P0 | todo | | |
| P2-B6a | Patient app: Now card, Today list, 4 tabs, Help, medicine due card with voice, visit request, papers by camera (en + hi) | P0 | todo | | |
| P2-B6b | Patient app strings in ta + ml; new voice clips if a Sarvam key exists | P1 | todo | | |
| P2-B6c | Family page additions (medicine ticks, next visit, shared papers) | P1 | todo | | |
| P2-B7a | Landing page | P0 | done (b0d2f4e) |  |  |
| P2-B7b | Impact page (who, how many, funnel, calculator, live metrics, SDG) + `GET /api/impact` | P0 | done (b0d2f4e) |  | Numbers copied exactly from PITCH_PLAN · WIP `routes_public.py` (GET /api/impact, not registered) is in 8ebc65d |
| P2-B7c | Trust (ICMR) page | P0 | done (b0d2f4e) |  |  |
| P2-B7d | Vision (startup) page + architecture page + `docs/hackathon/architecture_v2.svg` | P0 | done (b0d2f4e) |  | Add the sections "Scale and cost" and "Works beside your hospital's software" (founder ask F-5) |
| P2-B8a | `twin-model.js` refactor (showcase still works) + public `/twin.html` | P0 | todo |  | WIP `web/js/twin-model.js` (792 lines, not loaded by any page yet) is in 8ebc65d |
| P2-B8b | Live twin in the hospital (`/api/live`, replay from `session_curves`) | P0 | todo |  | Never "real-time monitoring" |
| P2-B8c | Fleet twin: server-backed devices page with lifecycle, actions, telemetry | P1 | todo |  |  |
| P2-X1 | Itemised consent v2, enforced in code (family, AI) | P0 | todo | | |
| P2-X2 | Planned-feature cards in context (from `features.py`) | P1 | todo | | |
| P2-X3 | Interoperability (Contract L): FHIR R4 export per patient, CSV / FHIR patient import with a dry run, whole-hospital export; plus the printable discharge plan | P0-lite (raised by the founder, 11 Oct) | todo |  | Build after Phase 1 is verified. Admin only, audited; imported prescriptions are never created as approved. Brief: end of PHASE2_BRIEFS.md |
| P2-X4 | Security extras: CSP, hash-chained audit, multilingual "never diagnose" filter | P1 | todo | | |
| P2-X5 | Nightly demo auto-reset at 04:00 IST | P1 | todo | | |
| P2-X6 | Data-rights requests; hospital self-registration | P2 | todo | | |

### Founder asks – Sun 11 Oct, 17:50 IST (scaling, cost, AIC servers, migration, company)
| ID | Step | Pri | Status | Commit | Notes |
|---|---|---|---|---|---|
| F-1 | `docs/SCALING_AND_COST.md`: load model, scaling stages, cost per stage and per patient episode, "Are the AIC servers enough?" | P0 | done (c8ccac7) | c8ccac7 | The AIC specification is not in the repo: the document answers by use and gives a fill-in table |
| F-2 | `docs/INTEROPERABILITY.md` + Contract L in ARCHITECTURE.md: SpiroBuddy sits beside the hospital's own software; data in, data out, moving hosts | P0 | done (2340b3f) | 2340b3f | The code is P2-X3 |
| F-3 | `docs/COMPANY_STRUCTURE.md`: legal shell, organisation by stage, required roles, routines, hiring order | P0 | done (628cdef) | 628cdef | No invented people or salaries |
| F-4 | Scaling and cost said in the demo video (shot 14) and in the pitch plan | P0 | todo (the integrator died on the usage limit; the video lines are in SCALING_AND_COST.md §9) | | The founder's ask overrides the spec's "do not edit the shot list". Only shots 14–15 and the totals change; the video stays at or under 5:55 |
| F-5 | Public Vision page: sections "Scale and cost" and "Works beside your hospital's software" | P0 | done (b0d2f4e) | | Part of B7d |
| F-6 | AIC server facts from the founder | P0 | blocked (waiting on the founder) | | Processor, memory, disk, graphics card, internet line, uptime, who looks after it |

### Phase 3 – Integration
| ID | Step | Pri | Status | Commit | Notes |
|---|---|---|---|---|---|
| P3-3.1 | Full test suite green (background, once) | P0 | done (745 passed, 14 xfailed, 23:44 IST) | | |
| P3-3.2 | Demo path click-through at 375 px and 1440 px, light and dark, hi + en, with and without a Gemini key | P0 | todo | | |
| P3-3.3 | Copy pass (never-say lists), label pass (registry), language pass | P0 | todo | | |
| P3-3.4 | Performance after a cold start; three.js only on twin pages | P1 | todo | | |

### Phase 4 – Docs and deploy
| ID | Step | Pri | Status | Commit | Notes |
|---|---|---|---|---|---|
| P4-4.1 | Update REQUIREMENTS, ARCHITECTURE, FEATURE_STATUS (generated), PROGRESS, HANDOFF (merge) | P0 | todo | | |
| P4-4.2 | `README.md` for judges, with the founder's disclosure placeholder (verdict A1) | P0 | todo | | Do not write the disclosure yourself |
| P4-4.3 | `docs/SETUP_STEPS.md` (Gemini key, Supabase paste, Render) | P0 | done (draft; re-check in Phase 4) | d0879ba | |
| P4-4.4 | `docs/hackathon/DEMO_PATH.md` (about 2:30, timed) + `docs/hackathon/VIDEO_PAGE_MAP.md` | P0 | todo | | |
| P4-4.5 | Founder config done (see the checkboxes above) | P0 | todo | | |
| P4-4.6 | Push P0 (founder OK) → live check → demo reset | P0 | done except the demo reset (557857d, 23:40 IST) | | |
| P4-4.7 | P1 work, verified and pushed (founder OK) | P1 | todo | | |
| P4-4.8 | FREEZE at 03:00 IST: lock none, final session log | P0 | todo | | |

---

## Session log (newest first)

- **Sun 11 Oct 23:15 – Mon 12 Oct 00:05 IST – session 7469796e (cont.):** wave 1 built story site (b0d2f4e) and digital prescription (5b0aecd, 90f0bc3); integration c7fe3f4; full suite 745 passed; **pushed P0 to main (557857d), live check all 200, Supabase v2 tables in**. README for judges (5008d46). Video Shot 12b + pitch slide 4b + DTI checklist (7e5e4a1, founder request). Founder: device not built; wait for the slide template. Usage nearly spent: lock released, wave 2 planned above for a fresh account.

- **Sun 11 Oct 2026, 22:35–23:15 IST – Opus 5.5 ultracode session 7469796e (Pro plan):** both 18:18 workflows had ended on the usage limit at about 22:26 (auth, kit, three founder docs committed; platform left uncommitted; isolation, seed v2, verify, skeptic and integrator never ran). Recovered and committed the platform work (4b1c899, 99 tests green). Browser check: staff login, the old dashboard and the patient app work under auth. Founder decisions recorded above (story site first; landing at `/`; medicines = digital prescription, not AI photo reading). Honesty pass on `features.py`. Launched wave 1 (2 builders + 2 verify-and-fix agents).

- **Sun 11 Oct 2026, 17:50–18:20 IST – Opus 5.5 ultracode session dd50472b (coyotaidev), resumed after the usage limit:** the 16:25 Phase 1 workflow and the 16:50 early wave both died at about 16:35 on the account's session limit (1 of 10 agents had finished: samples). Recovered the leftovers (see "Recovered work"): the data step was complete and green, so P1-1.1 and P1-1.2 are done. Took the founder's new asks (scaling and cost in the docs and the video, AIC servers, hospital migration, company structure): rows F-1 to F-6, and P2-X3 raised. Launched two smaller workflows (2 builders + 1 writer at a time). Next: mark rows from git when they finish, then Phase 2, two builders at a time.
- **Sun 11 Oct 2026, 16:05–16:25 IST – Opus 5.5 ultracode session (coyotaidev):** start-up check done, lock taken, baseline 420 passed / 14 xfailed. Phase 0 done (plan, contracts E–K, model `gemini-3.1-flash-lite` by founder's choice). Launching the Phase 1 workflow. Next: Phase 1 rows.
- **Sun 11 Oct 2026, ~4:30 pm IST – planning session:** wrote the spec and seeded this file. No build work yet. Next: P0-0.1.

## Recovered work

- **11 Oct 17:55 – uncommitted files left by the interrupted workflows (sessions a3646362 and b9fe4b50):**
  - `a02ed99` – the data step (config, env, `schema_v2.sql`, store, `tests/test_store_v2.py`): complete, 57 tests green. Committed as done.
  - `0c9b54a` – docs from the video-planning session: the rewritten 5½-minute shot list, `docs/hackathon/architecture.svg` and `.png`, HANDOFF notes, `docs/private/` added to `.gitignore`. Committed as they were.
  - `8ebc65d` – **WIP, unfinished:** the front-end kit (`api.js`, `ui.js`, `styles.css` section 8, `login.html`), B7's `backend/app/routes_public.py`, B8's `web/js/twin-model.js`. Committed on `master` so nothing is lost (not pushed, not wired in). The kit agent finishes the kit; B7 and B8 continue from their files.
  - The worktree `C:/Users/USER/.codex/worktrees/e2df/SpiroBuddy` (branch `codex/sarvam-insee-research`) belongs to another tool. Left alone.
