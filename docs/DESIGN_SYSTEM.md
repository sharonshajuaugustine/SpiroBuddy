# SpiroBuddy design system – one look for everything

Every SpiroBuddy surface uses this: the nurse/doctor website, the demo panel, the 3D showroom and videos, WhatsApp cards, the device light, slides, the guardian page and later the patient app. **Source of truth for the values:** the CSS variables at the top of `web/css/styles.css`. If a value changes, change it there and here together.

**Feel:** clinical and calm. Neutral backgrounds, one brand teal, status colours used sparingly and always with an icon and a word. Crisp type hierarchy, 4/8 spacing, thin borders instead of heavy shadows, tabular numbers.

`web/css/styles.css` is organised in this order: **1 tokens** (light + dark) → **2 base** → **3 layout & app shell** → **4 components** → **5 pages** → **6 print** → **7 UI 2 additions** (guardian page v2, demo-panel tidy – later rules that refine the `.g-*` and `.dcard` pieces; add new work below it).

---

## 1. Tokens

### Colour
| Token | Light | Dark | Used for |
|---|---|---|---|
| `--brand` / `--brand-hover` | `#0b6e8a` / `#095a71` | `#3fb4d4` / `#66c6e0` | Logo, primary buttons, links, selected nav, the device accent, "breathing in" |
| `--brand-ink` | `#ffffff` | `#06202a` | Text on a brand fill |
| `--brand-soft` / `--brand-line` | `#e4f1f5` / `#b5d9e4` | `#12303d` / `#1f5266` | Selected items, info boxes |
| `--bg` | `#f4f6f8` | `#0d1319` | Page |
| `--surface` / `--surface-2` / `--surface-3` | `#fff` / `#f8fafb` / `#eef2f5` | `#151d26` / `#1a2430` / `#202c39` | Cards / insets inside cards / hover, table head |
| `--border` / `--border-strong` | `#e0e5ea` / `#c3ccd5` | `#283544` / `#3a4a5c` | Hairlines / inputs, dashed outlines |
| `--text` / `--text-2` / `--text-3` | `#101c27` / `#445263` / `#5b6878` | `#e8eef4` / `#b4c0cc` / `#95a2b0` | Body / secondary / hints (all ≥ 4.5:1 on `--bg` and `--surface`) |
| `--green` / `--green-dot` / `--green-soft` / `--green-line` | `#1b7035` / `#2e9d4e` / `#e8f5ec` / `#b6dfc2` | `#63d083` / `#4cc06d` / `#13301d` / `#285c38` | On track, good breath, done |
| `--yellow` / `--yellow-dot` / `--yellow-soft` / `--yellow-line` | `#8f5100` / `#e8970f` / `#fff5e1` / `#f0d49a` | `#f3b443` / … | Watch, "Slower…", under 80 % of goal |
| `--red` / `--red-soft` / `--red-line` | `#c62828` / `#fdeded` / `#f2c1c1` | `#ff7b7b` / `#3a1b1e` / `#6b2b30` | Needs a call, missed, red flag |
| `--focus` | `#1a73e8` | `#7ab4ff` | Keyboard focus ring (3 px outline) |
| `--overlay` | 45 % ink | 60 % black | Modal backdrop |

`--yellow` text was darkened from `#a15c00` to `#8f5100` so amber words pass AA on the pale amber background. Dark values switch automatically with `prefers-color-scheme`, or by `data-theme="dark"|"light"` on `<html>` (the moon/sun button stores the choice).

**Meaning is fixed everywhere:** teal = SpiroBuddy / breathing in · green = good / done · amber = slow down / watch · red = a person is needed now. The device LED, the app, WhatsApp cards and the dashboard use the same meaning. Goal lines on charts are neutral (dark dashed), never red.
**Never use colour alone:** always add a word and an icon (✓ On track, ⚠ Watch, ⛔ Needs a call, ⚑ Red flag) – for colour-blind users and for patients who can't see well.

### Type
| Token | Size | Use |
|---|---|---|
| `--fs-xs` | 12 px | Badges, table headers only |
| `--fs-sm` | 13 px | Minimum for reading text (hints, meta) |
| `--fs-md` | 14 px | Table cells, buttons, secondary |
| `--fs-base` | 15 px | Nurse body text |
| `--fs-lg` | 17 px | Card titles (h2) |
| `--fs-xl` | 20 px | **Patient/guardian body minimum** |
| `--fs-2xl` | 24 px | Page titles (h1), KPI numbers |
| `--fs-3xl` | 30 px | Summary-tile numbers |
| `--fs-4xl` | 40 px | Patient main number |

Font: `--font` = Segoe UI / system UI, with Nirmala UI and Noto Sans for Devanagari and Tamil. `--mono` for logs. Numbers use tabular figures (`.tnum`, and built into tiles, KPIs, tables, meters) so live values don't jump.

### Space, shape, elevation, layers, motion, sizes
- **Spacing (4/8 grid):** `--sp-1` 4 · `--sp-2` 8 · `--sp-3` 12 · `--sp-4` 16 · `--sp-5` 20 · `--sp-6` 24 · `--sp-8` 32 · `--sp-12` 48.
- **Radius:** `--r-xs` 4 (tags) · `--r-sm` 6 · `--r-md` 8 (buttons, inputs) · `--r-lg` 12 (cards) · `--r-xl` 16 (modal) · `--r-pill`. Legacy aliases `--radius` = 12, `--radius-sm` = 8 stay for older code.
- **Elevation:** borders first. `--elev-1` (cards, almost flat) · `--elev-2` (hover) · `--elev-3` (popovers, toasts, modal). `--shadow` = `--elev-1`.
- **Layers (z-index):** `--z-sticky` 20 (top bar) · `--z-nav` 25 · `--z-pop` 40 · `--z-modal` 60 · `--z-toast` 80.
- **Motion:** `--dur-fast` 120 ms · `--dur` 200 ms · `--dur-slow` 400 ms · `--ease`. Everything stops under `prefers-reduced-motion: reduce`.
- **Sizes:** `--target` 44 px (nurse site buttons and inputs; `.btn.sm` 36 px only inside dense rows – still above the WCAG 2.2 24 px minimum) · `--target-patient` 64 px · `--top-h` 56 px · `--nav-w` 216 px · `--content-max` 1440 px.

---

## 2. App shell (every nurse page)
`SB.ui.boot(pageKey)` in `web/js/ui.js` builds it; pages only need `<header id="app-header"></header><main>…</main>`.
- **Top bar** `.app-header` – logo + "SpiroBuddy", hospital + ward (`SB.ui.SITE`, demo values), dashed **Demo mode** chip, then on the right: alert bell (`comms.js`), **system status** popover (`details.sys` – data store, ML, AI, WhatsApp, each OK / Fallback / Down with the reason), **clock in IST, 12-hour** ("3:04 pm IST"), theme button.
- **Side nav** `.side-nav` – Ward: Dashboard, Alerts (live count badge), Patients · Tools: Demo panel, Record breaths, 3D showroom. Under 1024 px it becomes a scrolling tab strip under the top bar.
- **Skip link** to `#main`; `main` is focusable.
- **Banners** `.banner.offline` / `.banner.mock` under the bar: "Server offline – showing last data".
- **Page header** `.page-head` = title + `.page-sub` on the left, `.page-actions` on the right. Breadcrumb `.crumbs` on detail pages.

Breakpoints: ≥ 1280 full bar · 1024–1279 ward name hidden · < 1024 nav strip · < 820 triage table becomes cards · < 760 clock and hospital hidden, status shows as a dot · < 420 logo text hidden. No horizontal page scroll at 375 px.

## 3. Components (class names)
| Component | Classes | Usage note |
|---|---|---|
| Card | `.card`, `.card-flush`, `.card-head` (+ `h2`, `.card-sub`, `.spacer`) | Every section is a card. `card-flush` for tables that run edge to edge. |
| Button | `.btn` + `.primary` / `.ghost` / `.good` / `.mixed` / `.danger` (`.poor`), sizes `.sm` / `.lg`; `.icon-btn` | One primary per area. Human call = primary; AI call = plain/secondary. Put an icon first: `${SB.ui.ic('phone')}Call`. `SB.ui.busy(btn, fn)` shows the busy state. |
| Status pill | `.status-pill.status-red/yellow/green`, `.status-flag` | Made by `SB.ui.statusPill(status)` and `SB.ui.redFlagPill()` – icon + word, never colour alone. |
| Chip | `.chip` (+ `.ok/.warn/.bad` with `.dot`), `.chip-demo`, `.chip.soft-warn` | Small facts and counts. |
| Tag | `.tag` (+ `.missed/.summary/.dry/.sent`), `.source-tag(.llm)`, `.lbl-chip.lbl-<label>` | Message kinds, AI vs template, breath labels. |
| Severity | `.sev.sev-red/amber/info`, `.alert-item.sev-*`, `.alert-badge(.red)` | Alerts inbox rows and the bell badge on patient rows. |
| Summary tile | `.tiles` > `.tile` (+ `.tile-red`, `.tile-amber`, `.has`), `.tile-label`, `.tile-num`, `.tile-sub` | Use `<button>` when it filters, `<a>` when it jumps. `aria-pressed` shows the active filter. |
| Meter | `SB.ui.meter(frac, tone, label)` → `.meter.good/.warn/.bad/.brand` | x of y progress (sessions, best vs goal). Always next to the number in words. |
| Table | `table`, `.table-wrap`, `.data-table`, `td.num`; `.triage` for the patient list | Right-align numbers. `.triage` rows turn into cards under 820 px using each cell's `data-label`. |
| Segmented filter | `.seg` > `button[aria-pressed]` (+ `.count`) | Filters with counts. |
| Tabs | `.tabs` > `[role=tab][aria-selected]` | For switching views in one card. |
| Forms | `.field`, `.form-grid`, `.mini-form`, `.input-icon`, `.sm-select` | Labels above inputs; 40 px min height. |
| Toast | `SB.ui.toast(msg, 'good'|'bad', ms)` → `.toasts` > `.toast` | Live updates ("Ravi completed a session"). The container is `role=status aria-live=polite`. |
| Modal | `<dialog class="modal">` with `.modal-head`, `.modal-body`, `.modal-foot` | Use `dialog.showModal()`; backdrop uses `--overlay`. |
| Empty state | `.empty` (+ icon, `<b>` title, sentence, optional button) | "No sessions yet today", "No patients match – Clear filters". |
| Loading | `.skeleton` (shimmer), `.skel-row` | Shown before the first load. |
| Live indicator | `.live` (+ `.stale`), `.live-dot` | "Live · updated 3:04 pm" / red "Offline · last data 3:04 pm". |
| Charts | `SB.charts.weekChart(el, history, goal)`, `SB.charts.qualityBar(el, counts)`, `.chart-legend` | Honest: y-axis from 0, labelled axis, value on every bar, goal line with its value, one measure per chart, plus a hidden data table for screen readers. |
| Timeline / ladder | `.timeline` > `.tl-item`, `.ladder` > `.ladder-step.done/.next/.held/.skipped` | Communications history and escalation steps. |
| Icons | `web/js/icons.js`: `SB.icon(name, {size, label})`, or `<span data-icon="bell"></span>` + `SB.ui.hydrateIcons()` | 24 px grid, 2 px stroke, round ends, `currentColor`. Set: dashboard, bell, users, user, user-check, sliders, cube, activity, wind, phone, eye, search, check, check-circle, x-circle, x, alert-triangle, alert-octagon, flag, info, clock, hourglass, circle, calendar, bed, globe, chevron-*, arrow-* (up, down, right, left), minus, moon, sun, printer, sparkles, message, send, refresh, wifi-off, database, flask, external, hospital, play, stop, skip-forward, heart, volume, flame, star, maximize, image, headphones, music, film, book. `ui.js` loads `icons.js` itself if a page forgot it. |
| Page stack | `.page-stack` | Wraps the sections of a page so every card has the same 16 px gap (demo panel). No inline margins. |
| Shortcut list | `.shortcuts` > `span` > `.kbd` | Keyboard shortcuts in a card (demo panel). |
| Demo patient card | `.dcard` (+ `.red/.yellow/.green`, `.star`), `.dcard-head` (`.name`, chip, status pill), `.btns` (+ `.wide`), `.result` with `.r-good/.r-warn/.r-bad` icon | The three simulate buttons stack icon over words (64 px). Results start with an icon and a word (Sent / Dry run / Failed). |

## 4. Pages
- **Dashboard** (`index.html`): tiles (Patients · Needs a call · Open alerts · Sessions today) → triage list sorted red flag → needs a call → watch → on track, with search, status filter with counts, sort, and per row: status pill(s), name + age/sex/operation/post-op day + reason, today "x of y due" meter, best vs goal meter, 3-day volume trend, last session, Call / View. Whole row opens the patient. Alerts inbox beside the list on wide screens (≥ 1560 px), below it otherwise.
- **Patient** (`patient.html`): header (avatar, name, status, age, operation, post-op day, ward/bed, language, family) with **Call patient** (primary) and **Print**; KPI strip; today's 14 hourly slots (icon + time + word); 7-day best-breath chart; breath-quality breakdown; recent sessions; AI summary; WhatsApp; voice; care circle. Right column: care-team actions (nurse call first, AI check-in call secondary), escalation ladder + communications timeline, messages, goal & settings. One column under 1180 px.
- **Demo panel** (`demo.html`): page header with **Reset demo data** in `.page-actions`; then a `.page-stack` of: shortcuts card, patient cards (`.demo-grid` of `.dcard`), simulators card (`js/phone-sim.js`), message log + 3D showroom/activity, voice check (`js/voice-ui.js`). The phone and WhatsApp simulators keep WhatsApp's own colours and emoji on purpose – they imitate another app.
- **3D showroom** (`showcase/index.html`, `videos.html`, `sources.html`): no app shell (the 3D view needs the whole window), but the same tokens, logo, `.btn`, `.chip`, `.card` and focus ring. Each page carries an **inline copy of the tokens** from section 1 of `styles.css` – change both together. A floating top bar (logo → dashboard, page name, Videos / Sources / Fullscreen) sits over the 3D view. They read the same stored light/dark choice (`localStorage sb_theme`). `sources.html` is generated: edit the template in `tools/render/make_sources_html.py`, then run it.
- **Print** (`@media print`): the patient page prints as an A4 summary – header, KPIs, slots, chart, quality, sessions, AI summary, alerts and messages; the shell, buttons, forms, voice, care circle and ladder are hidden; a printed-at line and the "does not diagnose" footer are added.

## 5. Accessibility rules
WCAG 2.2 AA contrast for all text tokens in both themes · visible 3 px focus ring · everything works by keyboard (skip link, native buttons/links/details) · `aria-live` only on small regions (toasts, alerts list, summary) so screen readers aren't flooded every 2 s · re-renders are skipped while focus is inside a list · `prefers-reduced-motion` stops all animation · 44 px targets on the nurse site · status never by colour alone.

## 6. Patient & guardian surfaces
They import the **same** `web/css/styles.css` and the same tokens – same colours, same meaning, same icons (`web/js/icons.js`). Differences:
- **Type:** body at `--fs-xl` (20 px); nothing on the page under 18 px; the main number at `--fs-4xl` (32–48 px).
- **Targets:** `--target-patient` (64 px) minimum, 72 px for the main action.
- **One action per screen**, plain words in the patient's language, no charts with axes – big ticks (`.g-tick.done/.missed/.pending/.upcoming`, each with an icon, and a word legend `.g-legend` underneath) and one status card (`.g-status.good/.nudge/.call`: round icon badge + a sentence).
- **Buttons:** `.g-btn.call` is the one filled teal (primary) button; `.g-btn.cheer` is teal outline on pale teal; `.g-btn.listen` (also used for Back) is a plain outline. Each has an icon first, then words. Choice lists (`.g-choices`) are outlined rows; the chosen one (`aria-pressed="true"`) turns pale teal with a tick.
- **Icons, not emoji** – same set as the nurse site, through `SB.icon()`; if `icons.js` fails to load, the words still show.
- One column under 480 px; no sideways scroll at 375 px; light and dark follow the phone's setting.
- No app shell, no demo chip, no alerts. Classes: `.g-body`, `.g-wrap`, `.g-top`, `.g-lang`, `.g-card`, `.g-note` (loading / bad link / offline), `.g-status`, `.g-title` (icon + card title), `.g-big` (+ `.sm`), `.g-label` (+ `.center`), `.g-row`, `.g-ticks`, `.g-legend`, `.g-btn.call/.cheer/.listen`, `.g-choices`, `.g-done`, `.g-foot`.

## 7. Voice and tone (all text, voice prompts, WhatsApp, calls)
- Warm, short, respectful. Use "Ravi ji" style address in Hindi. No medical jargon.
- Praise first, then one simple next step.
- **Never diagnose.** Red-flag words get the fixed message: "Please contact your nurse now. If it's an emergency, call 112."
- The same phrase means the same thing everywhere (e.g. always "Slower…" / "धीरे…", never a synonym). On the nurse site: "Needs a call", "Watch", "On track", "Red flag", "Goal".

## 8. Sound
- One short, friendly chime for a good breath; one low double-tone for "slower"; no harsh alarms for patients.
- The voice is a calm, warm voice in the patient's language, from pre-recorded clips, with browser speech or TTS as fallback.

## 9. Icons and illustration
- Line icons with 2 px strokes, rounded ends, in the current text or brand colour (`web/js/icons.js`).
- The 3D model and videos use brand teal for the SpiroBuddy unit's accent and the same status colours for the LED and phone screens.
