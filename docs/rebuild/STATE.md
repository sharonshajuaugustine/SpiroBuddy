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

- **Next action:** Two workflows are running, started 18:18 IST by session dd50472b (2 builders + 1 writer at a time, because the usage limit was hit at 16:35):
  1. **Phase 1 resume** `wf_5dc9872f-559`: chain A = auth → isolation; chain B = kit finish → platform → seed v2; then 2 verifiers → fixer. Each agent commits its own files as it goes.
  2. **Founder docs** `wf_43635652-07b`: scaling and cost (with the AIC server check) → interoperability and Contract L → company structure → skeptic → integrator (also edits shot 14 of the video shot list, the pitch plan, HANDOFF and the Phase 2 briefs).

  **When they finish:** mark the rows below from `git log`, then run Phase 2 two builders at a time in this order: B2a chart + B1a login pages → B3 medicines → B6a patient app → B7 public site (with the new "Scale and cost" and "Works beside your hospital's software" sections) → B8 twin → X3 interoperability (Contract L) → the rest.

  **If this session died:** workflows cannot be resumed from another session. Check `git log --oneline -25` for the commits named auth, isolation, kit, platform, seed2, scaling, interop, company; re-launch only what is missing. The Phase 1 script (all builder prompts) is at `%TEMP%/claude/C--Users-USER-Desktop-SpiroBuddy/dd50472b-3b16-40c6-b840-72fc648916f7/scratchpad/phase1_resume.js`; the docs script is in `~/.claude/projects/C--Users-USER-Desktop-SpiroBuddy/dd50472b-3b16-40c6-b840-72fc648916f7/workflows/scripts/`.
- **Lock (active session):** Opus 5.5 ultracode session dd50472b (coyotaidev account), re-taken Sun 11 Oct 17:55 IST after the usage limit reset
- **Last heartbeat:** Sun 11 Oct 18:20 IST. The workflows should run until about 19:45 IST. A new session before 20:15 must ask the founder first.
- **Schedule risk:** Phase 1 was due 18:30 and will land at about 19:45. With 2 builders at a time, not every P0 screen will be ready by 22:30. The rule stands: ship only finished screens and hide the rest behind Planned cards.
- **Last good commit before the redesign:** `4c78e46`
- **Live site** (https://spirobuddy.onrender.com): old version, not redeployed by the redesign yet

**Founder config** (tick when done; never ask again for a ticked item):
- [ ] Gemini API key added to `.env` (local)
- [ ] Gemini API key added on Render → Environment
- [ ] `supabase/schema_v2.sql` pasted into the Supabase SQL Editor and run
- [ ] Push approved for P0
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
| P1-1.3 | `authz.py`, middleware policy, auth endpoints, sessions, CSRF header in `api.js` | P0 | doing (dd50472b, wf_5dc9872f-559, 18:18) |  | auth agent; the api.js CSRF header is in WIP 8ebc65d (the kit agent finishes it) |
| P1-1.4 | Audit writer, `ai_events`, `features.py` + `GET /api/features` | P0 | doing (dd50472b, wf_5dc9872f-559, 18:18) |  | audit = auth agent; features + ai_events = platform agent |
| P1-1.5 | Gemini wrapper (limits, fallback, logging) + storage wrapper (Supabase bucket auto-create + local) | P0 | doing (dd50472b, wf_5dc9872f-559, 18:18) |  | platform agent |
| P1-1.6 | Seed v2 (both demo hospitals, staff, keys, prescriptions, doses, visits, documents, devices) + `tools/demo/make_samples.py` | P0 | doing (dd50472b, wf_5dc9872f-559, 18:18) | f7310d1 (samples) | Sample files done (f7310d1); seed v2 = seed2 agent |
| P1-1.7 | `conftest.py` under auth; old suite green; new auth, role and isolation tests | P0 | doing (dd50472b, wf_5dc9872f-559, 18:18) |  | auth + isolation agents |
| P1-1.8 | Phase 1 verify (2 skeptics) + commit | P0 | doing (dd50472b, wf_5dc9872f-559, 18:18) |  | 2 verifiers + fixer; skipped automatically if a builder returns nothing |

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
| P2-B7a | Landing page | P0 | todo |  |  |
| P2-B7b | Impact page (who, how many, funnel, calculator, live metrics, SDG) + `GET /api/impact` | P0 | todo |  | Numbers copied exactly from PITCH_PLAN · WIP `routes_public.py` (GET /api/impact, not registered) is in 8ebc65d |
| P2-B7c | Trust (ICMR) page | P0 | todo |  |  |
| P2-B7d | Vision (startup) page + architecture page + `docs/hackathon/architecture_v2.svg` | P0 | todo |  | Add the sections "Scale and cost" and "Works beside your hospital's software" (founder ask F-5) |
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
| F-1 | `docs/SCALING_AND_COST.md`: load model, scaling stages, cost per stage and per patient episode, "Are the AIC servers enough?" | P0 | doing (dd50472b, wf_43635652-07b, 18:18) | | The AIC specification is not in the repo: the document answers by use and gives a fill-in table |
| F-2 | `docs/INTEROPERABILITY.md` + Contract L in ARCHITECTURE.md: SpiroBuddy sits beside the hospital's own software; data in, data out, moving hosts | P0 | doing (dd50472b, wf_43635652-07b, 18:18) | | The code is P2-X3 |
| F-3 | `docs/COMPANY_STRUCTURE.md`: legal shell, organisation by stage, required roles, routines, hiring order | P0 | doing (dd50472b, wf_43635652-07b, 18:18) | | No invented people or salaries |
| F-4 | Scaling and cost said in the demo video (shot 14) and in the pitch plan | P0 | doing (dd50472b, wf_43635652-07b, 18:18) | | The founder's ask overrides the spec's "do not edit the shot list". Only shots 14–15 and the totals change; the video stays at or under 5:55 |
| F-5 | Public Vision page: sections "Scale and cost" and "Works beside your hospital's software" | P0 | todo | | Part of B7d |
| F-6 | AIC server facts from the founder | P0 | blocked (waiting on the founder) | | Processor, memory, disk, graphics card, internet line, uptime, who looks after it |

### Phase 3 – Integration
| ID | Step | Pri | Status | Commit | Notes |
|---|---|---|---|---|---|
| P3-3.1 | Full test suite green (background, once) | P0 | todo | | |
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
| P4-4.6 | Push P0 (founder OK) → live check → demo reset | P0 | todo | | |
| P4-4.7 | P1 work, verified and pushed (founder OK) | P1 | todo | | |
| P4-4.8 | FREEZE at 03:00 IST: lock none, final session log | P0 | todo | | |

---

## Session log (newest first)

- **Sun 11 Oct 2026, 17:50–18:20 IST – Opus 5.5 ultracode session dd50472b (coyotaidev), resumed after the usage limit:** the 16:25 Phase 1 workflow and the 16:50 early wave both died at about 16:35 on the account's session limit (1 of 10 agents had finished: samples). Recovered the leftovers (see "Recovered work"): the data step was complete and green, so P1-1.1 and P1-1.2 are done. Took the founder's new asks (scaling and cost in the docs and the video, AIC servers, hospital migration, company structure): rows F-1 to F-6, and P2-X3 raised. Launched two smaller workflows (2 builders + 1 writer at a time). Next: mark rows from git when they finish, then Phase 2, two builders at a time.
- **Sun 11 Oct 2026, 16:05–16:25 IST – Opus 5.5 ultracode session (coyotaidev):** start-up check done, lock taken, baseline 420 passed / 14 xfailed. Phase 0 done (plan, contracts E–K, model `gemini-3.1-flash-lite` by founder's choice). Launching the Phase 1 workflow. Next: Phase 1 rows.
- **Sun 11 Oct 2026, ~4:30 pm IST – planning session:** wrote the spec and seeded this file. No build work yet. Next: P0-0.1.

## Recovered work

- **11 Oct 17:55 – uncommitted files left by the interrupted workflows (sessions a3646362 and b9fe4b50):**
  - `a02ed99` – the data step (config, env, `schema_v2.sql`, store, `tests/test_store_v2.py`): complete, 57 tests green. Committed as done.
  - `0c9b54a` – docs from the video-planning session: the rewritten 5½-minute shot list, `docs/hackathon/architecture.svg` and `.png`, HANDOFF notes, `docs/private/` added to `.gitignore`. Committed as they were.
  - `8ebc65d` – **WIP, unfinished:** the front-end kit (`api.js`, `ui.js`, `styles.css` section 8, `login.html`), B7's `backend/app/routes_public.py`, B8's `web/js/twin-model.js`. Committed on `master` so nothing is lost (not pushed, not wired in). The kit agent finishes the kit; B7 and B8 continue from their files.
  - The worktree `C:/Users/USER/.codex/worktrees/e2df/SpiroBuddy` (branch `codex/sarvam-insee-research`) belongs to another tool. Left alone.
