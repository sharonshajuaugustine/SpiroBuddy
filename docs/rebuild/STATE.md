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

- **Next action:** P0-0.1 – run the §R2 start-up check, take the lock, start the baseline test run (nobody has started the build yet)
- **Lock (active session):** none
- **Last heartbeat:** –
- **Last good commit before the redesign:** `4c78e46`
- **Live site** (https://spirobuddy.onrender.com): old version, not redeployed by the redesign yet

**Founder config** (tick when done; never ask again for a ticked item):
- [ ] Gemini API key added to `.env` (local)
- [ ] Gemini API key added on Render → Environment
- [ ] `supabase/schema_v2.sql` pasted into the Supabase SQL Editor and run
- [ ] Push approved for P0
- [ ] Push approved for P1

---

## Steps

### Phase 0 – Map
| ID | Step | Pri | Status | Commit | Notes |
|---|---|---|---|---|---|
| P0-0.1 | Start-up check, lock, baseline full test suite (background) | P0 | todo | | Baseline was 420 pass / 14 expected failures (verdict, 11 Oct) |
| P0-0.2 | `docs/REBUILD_PLAN.md`: file ownership, risks, P0/P1/P2 list | P0 | todo | | |
| P0-0.3 | Contracts E–K written into `docs/ARCHITECTURE.md` + PROGRESS note | P0 | todo | | Must be done before Phase 2 |
| P0-0.4 | Gemini model + SDK version chosen from Google's docs, recorded in PROGRESS | P0 | todo | | Stable Flash only, no preview |

### Phase 1 – Foundations (one builder, sequential)
| ID | Step | Pri | Status | Commit | Notes |
|---|---|---|---|---|---|
| P1-1.1 | Config + env names (`.env.example`, `render.yaml`, `config.py`), `ALLOW_TRAINING`, `SHOW_API_DOCS` | P0 | todo | | |
| P1-1.2 | `supabase/schema_v2.sql` (additive) + SQLite tables + store additions + "v2 tables missing" fallback | P0 | todo | | |
| P1-1.3 | `authz.py`, middleware policy, auth endpoints, sessions, CSRF header in `api.js` | P0 | todo | | |
| P1-1.4 | Audit writer, `ai_events`, `features.py` + `GET /api/features` | P0 | todo | | |
| P1-1.5 | Gemini wrapper (limits, fallback, logging) + storage wrapper (Supabase bucket auto-create + local) | P0 | todo | | |
| P1-1.6 | Seed v2 (both demo hospitals, staff, keys, prescriptions, doses, visits, documents, devices) + `tools/demo/make_samples.py` | P0 | todo | | |
| P1-1.7 | `conftest.py` under auth; old suite green; new auth, role and isolation tests | P0 | todo | | |
| P1-1.8 | Phase 1 verify (2 skeptics) + commit | P0 | todo | | |

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
| P2-B7a | Landing page | P0 | todo | | |
| P2-B7b | Impact page (who, how many, funnel, calculator, live metrics, SDG) + `GET /api/impact` | P0 | todo | | Numbers copied exactly from PITCH_PLAN |
| P2-B7c | Trust (ICMR) page | P0 | todo | | |
| P2-B7d | Vision (startup) page + architecture page + `docs/hackathon/architecture_v2.svg` | P0 | todo | | |
| P2-B8a | `twin-model.js` refactor (showcase still works) + public `/twin.html` | P0 | todo | | |
| P2-B8b | Live twin in the hospital (`/api/live`, replay from `session_curves`) | P0 | todo | | Never "real-time monitoring" |
| P2-B8c | Fleet twin: server-backed devices page with lifecycle, actions, telemetry | P1 | todo | | |
| P2-X1 | Itemised consent v2, enforced in code (family, AI) | P0 | todo | | |
| P2-X2 | Planned-feature cards in context (from `features.py`) | P1 | todo | | |
| P2-X3 | FHIR R4 export (basic) + printable discharge plan | P1 | todo | | |
| P2-X4 | Security extras: CSP, hash-chained audit, multilingual "never diagnose" filter | P1 | todo | | |
| P2-X5 | Nightly demo auto-reset at 04:00 IST | P1 | todo | | |
| P2-X6 | Data-rights requests; hospital self-registration | P2 | todo | | |

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
| P4-4.3 | `docs/SETUP_STEPS.md` (Gemini key, Supabase paste, Render) | P0 | todo | | |
| P4-4.4 | `docs/hackathon/DEMO_PATH.md` (about 2:30, timed) + `docs/hackathon/VIDEO_PAGE_MAP.md` | P0 | todo | | |
| P4-4.5 | Founder config done (see the checkboxes above) | P0 | todo | | |
| P4-4.6 | Push P0 (founder OK) → live check → demo reset | P0 | todo | | |
| P4-4.7 | P1 work, verified and pushed (founder OK) | P1 | todo | | |
| P4-4.8 | FREEZE at 03:00 IST: lock none, final session log | P0 | todo | | |

---

## Session log (newest first)

- **Sun 11 Oct 2026, ~4:30 pm IST – planning session:** wrote the spec and seeded this file. No build work yet. Next: P0-0.1.

## Recovered work

- (none yet: list any leftover worktrees, branches, stashes or uncommitted changes found on resume, and what was done with each)
