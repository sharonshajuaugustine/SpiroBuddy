# Public story site (P2-B7a-d, F-5) - integration notes for the lead

Written by builder A on Sun 11 Oct 2026, night. Plain words, short.

## What is done

- **Landing `/`** (`web/index.html`) replaces the placeholder. Order: hero, the two things that go home with the patient, the problem (sourced), three illustrative personas, how it works, what is inside, trust strip, status legend, two big buttons, footer.
  - The founder's framing leads: the hospital (doctor and nurse) stays connected to the patient at home. Pillar 1 is proof the breathing exercise was done (the spirometer stays the hero). Pillar 2 is the doctor's prescription on the patient's phone, shown at the pharmacy counter, no paper. Badges `rx.manual`, `rx.patient_phone`, `rx.pharmacy_screen`, `rx.verify_qr` come from the registry, so they say In development until you flip them.
  - Nothing pitches AI reading a prescription photo. The line on the page is "nothing has to be decoded from a photo".
  - Hero is `/showcase/videos/hero.mp4` (muted, loop, playsinline). It starts only when the visitor has not asked for less motion, and only while it is on screen. With reduced motion the page shows a still frame and a Play button. Link "Open the 3D showroom" goes to `/showcase/`. No iframe, no `/twin.html`.
  - Buttons: "Open the patient app (demo)" goes to `/app.html?id=1`; "Hospital login (demo credentials shown)" goes to `/login.html?next=/dashboard.html`.
- **`/impact.html`**: segments with statuses (B1-5, E-7 to E-10), counted inputs and the market range (B1-8, B1-10: about 24.5 to 147 crore, estimate), the six-step adoption and retention funnel (tagged "Shot list · shot 13 · assumptions"), the calculator (six sliders, outputs all labelled Estimate, formula and fixed assumptions shown), live numbers from `GET /api/impact`, SDG 3 table.
- **`/trust.html`**: the rule table (ICMR 2017, ICMR AI 2023, DPDP 2023, Telemedicine 2020) with registry badges, the ten safe-medication rules, live AI audit numbers (from `/api/impact`, so no login), the disclaimer and the Gemini sentence word for word, the 14-step pilot checklist with the "Demo hospital example" note.
- **`/vision.html`**: problem, solution and the three tiers, business model in words (labelled estimates), the Kerala beachhead (B1-13), roadmap 0-3, 3-12 and 12-24 months, hard to copy and honest risks, what we ask mentors for, **Scale and cost** (stage cards, only Stage 0 is running; the three video lines), **Works beside your hospital's software** (short answer and the four levels), and the **Drug-interaction checks - deliberately not built** section.
- **`/architecture.html`** with an inline SVG. Boxes are coloured by the registry status in the browser, with the status word inside. A table below lists every box. The same picture is saved as `docs/hackathon/architecture_v2.svg` (the old `architecture.svg` is untouched).
- **`GET /api/impact`** (`backend/app/routes_public.py`, Contract K): public, never errors (any missing table or store gives zeros), the same numbers for every viewer (it reads the store directly, not the logged-in list), 15-second cache, includes `ai_drafts`, `ai_lines_edited_pct`, `ai_rejected_pct`.
- Shared files I wrote: `web/css/public.css`, `web/js/public-shell.js` (header, footer, theme button, legend), `public-home.js`, `public-impact.js`, `public-trust.js`, `public-arch.js`, `web/data/impact.json`, `web/data/trust.json`.

## Feature keys to flip

All eight are finished and shown on the pages. Flip them to `live` in `backend/app/features.py`:

`public.landing`, `public.impact`, `impact.calculator`, `impact.metrics`, `public.trust`, `public.vision`, `public.architecture`, `segment.post_surgery`.

Notes for the flip:
- `impact.metrics` is live only because `/api/impact` works; the tiles show "No data yet" when a table has no rows (for example doses, until the medicines work lands).
- `segment.post_surgery` is the focus segment card on `/impact.html`.
- `public.landing` has no badge on its own page; the existing test that a Live badge needs its page is satisfied (`web/index.html` exists).
- After you flip keys, the file `docs/hackathon/architecture_v2.svg` still shows the old words (the web page fixes itself in the browser). Redraw it with `.venv/Scripts/python.exe docs/rebuild/story_arch_gen.py` (the script is a new file of mine; it also refreshes the inline copy in `web/architecture.html`). `tests/test_public.py` only warns when the file is out of date, it does not fail.

## Things you may want to change in files I do not own

1. **`backend/app/features.py`, optional new keys.** Some plain-text statuses on `/vision.html` have no registry key, so they are written as text, never as a badge: Stage 0 to 4 (scale), Level 0 and Level 2 (connection levels). If you want badges there, add `scale.stage0` (live), `scale.stages_1_4` (planned), `interop.csv` (in development), `interop.live_feed` (planned) and tell me or swap the text for `data-feature` spans.
2. **`backend/app/main.py`**: nothing needed. `/api/impact` is already in `PUBLIC_PREFIXES`; `routes_public` loads on its own now. The public pages never redirect to login (`api.js` lists staff pages only).
3. **Possible links once the digital prescription pages are final** (builder B: `web/meds.html`, `web/rx.html`): add "See the patient's medicine screen (demo)" to the pillar 2 card on `web/index.html`. I did not link them because they were still changing while I worked.
4. **`tests/test_platform.py`**: its never-say check covers only the registry notes, so nothing to change. If you add a site-wide grep, note that `/trust.html` holds one sentence word for word from the spec: "Designed to follow these guidelines. Not reviewed or approved by ICMR, an ethics committee or CDSCO." It names a banned word only to deny it. My own test removes that single sentence before it scans.

## Honest limits

- The calculator and funnel use the founder's shot-13 numbers and my own simple arithmetic (shown on the page under "How these are worked out"). They are estimates, not results.
- Statuses of Stage 0 to 4 and Level 0 to 3 come from `docs/SCALING_AND_COST.md` and `docs/INTEROPERABILITY.md` as written on 11 Oct; nothing in those docs was re-checked against code, except Level 1 and Level 3, which use the registry keys `fhir.export` and `docs.abdm_link`.
- Source IDs such as `PITCH_FACTS #5` and `B1-10` point to files in this repo; I copied the figures from those files and did not re-open the outside papers.
- The hero video shows a "Romsons Breazer" caption that is baked into the existing `hero.mp4`. I did not edit the video.
- I wrote no new patient-side translations, so there is nothing for a native speaker to check.
