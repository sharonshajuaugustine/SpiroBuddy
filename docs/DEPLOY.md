# Put SpiroBuddy online (Supabase + Render)

**In short:** make a free Supabase project and paste one file into it, then make a free Render Blueprint from the GitHub repo and paste two values. About 20 minutes. Nothing else.

Think of it like a shop: **Render** is the shop front people walk into (the website), and **Supabase** is the stock room behind it (the database). Only the shop staff (our server) has the stock-room key. Visitors' browsers never get it.

You don't need any of this for the laptop demo: `scripts\run.ps1` works with no accounts.

---

## Before you start (one check)
The code Render uses is the **`main` branch on GitHub**: https://github.com/sharonshajuaugustine/SpiroBuddy
Make sure the latest work has been pushed there (ask Claude: "commit and push to GitHub"). Render builds whatever is on GitHub, not what is on the laptop.

---

## Part 1 – Supabase (the database)

1. Go to https://supabase.com and click **Start your project**. Choose **Continue with GitHub**.
2. Click **New project**.
   1. **Name:** `spirobuddy`
   2. **Database password:** click **Generate a password**. Save it in a note (the app doesn't need it).
   3. **Region:** **South Asia (Mumbai)**. If it isn't offered, pick **Singapore**.
   4. Click **Create new project**. Wait 1–2 minutes until the dashboard appears.
3. In the left sidebar click **SQL Editor**. Then click **New query** (or the **+** tab).
4. On the laptop, open `supabase\schema.sql` with Notepad. Press **Ctrl+A**, then **Ctrl+C**.
5. Click in the Supabase editor, press **Ctrl+V**, then click **Run** (bottom right).
   - You should see **"Success. No rows returned"**.
   - If Supabase warns about "destructive operations", click **Run this query**. (The file only creates tables. It never deletes anything.)
6. You do **not** need `supabase/seed.sql`. The server fills in the 7 fake patients and a week of history by itself the first time it starts. (Running seed.sql anyway is harmless.)
7. Copy the two values Render needs. Keep them in a private note.
   1. **Project URL:** click **Project Settings** (gear icon, bottom left) → **Data API**. Copy the **URL**. It looks like `https://abcdefghijk.supabase.co`.
   2. **Secret key:** **Project Settings** → **API Keys**.
      - If you see a **Secret keys** section: click **Reveal** / copy on the key that starts with `sb_secret_`. (If there is none yet, click **Create new secret key**.)
      - If you only see **Legacy API keys**: copy the **service_role** key (a long text starting with `eyJ`).
      - Both kinds work. Do **not** use the "publishable" or "anon" key: it can't see the tables, on purpose.
8. **Never** paste the secret key into a chat, a screenshot, GitHub or the website code. It goes only into Render (Part 2) and the laptop's `.env` file.

---

## Part 2 – Render (the website)

1. Go to https://render.com and click **Get Started**. Choose **GitHub** and allow access.
2. In the Render dashboard click **New** (top right) → **Blueprint**.
3. Find **SpiroBuddy** in the list and click **Connect**.
   - Not listed? Click **Configure GitHub** (or "Connect account"), choose **Only select repositories** → **SpiroBuddy** → **Save**, then go back to step 2.
4. On the next page:
   1. **Blueprint Name:** `spirobuddy`
   2. **Branch:** `main`
   3. Render reads `render.yaml` and shows one web service, **spirobuddy**, and a list of values to fill in.
5. Fill in only these two:
   - `SUPABASE_URL` → the Project URL from Part 1, step 7.1
   - `SUPABASE_SERVICE_ROLE_KEY` → the secret key from Part 1, step 7.2
   - **Leave all the others empty.** Every one of them is optional (see "Optional keys" below).
6. Click **Deploy Blueprint** (it may say **Apply**). The first build takes about 5–8 minutes. You can watch it under **Logs**.
7. When the service shows **Live** (green), click its link at the top. It looks like `https://spirobuddy.onrender.com` (Render may add letters, e.g. `spirobuddy-x1y2.onrender.com`).

---

## Part 3 – Check it works

1. Open `https://YOUR-APP.onrender.com/api/health`.
2. You want to see **`"data_backend":"supabase"`** and **`"data_note":"supabase connected"`**.
3. Open `https://YOUR-APP.onrender.com/` for the nurse dashboard. You should see 7 patients in green, yellow and red.
4. Optional: in Supabase click **Table Editor → patients**. The same 7 fake patients are there.
5. Also try `/showcase/` (3D showroom) and `/demo.html` (demo controls).

### If it says `"data_backend":"demo"` instead
The website still works, but on temporary data that disappears on every restart. Read `data_note` on the same page – it says why:

| `data_note` says | What to do |
|---|---|
| `... SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY missing` | A value is empty. Add it (steps below). |
| `Supabase unreachable (... 401 ...)` or `Invalid API key` | Wrong key. Copy the **secret** / **service_role** key again – not the anon/publishable one. |
| `... table guardians: HTTP 404 ... run supabase/schema.sql` | The tables aren't there. Do Part 1, steps 3–5 again. |
| `... Name or service not known` / `ConnectError` | The URL is wrong. It must look exactly like `https://abcdefghijk.supabase.co` (no `/rest/v1`, no spaces). |
| Supabase project **paused** | Free projects pause after a week without use. In Supabase click **Restore project**, wait 2 minutes, then restart Render (below). |

**To fix a value on Render:**
1. Render dashboard → click **spirobuddy** → **Environment** (left menu).
2. Click **Edit**, fix `SUPABASE_URL` or `SUPABASE_SERVICE_ROLE_KEY`, click **Save, rebuild, and deploy** (or **Save and deploy**).
3. Wait until it's **Live**, then open `/api/health` again.

---

## Good to know
- **The free Render plan sleeps** after 15 minutes without visitors. The first visit after that takes up to a minute. **Open the site 5 minutes before you present.**
- **Data is safe in Supabase.** Render's own disk is wiped on every restart and deploy, but all patients, sessions, messages, alerts and guardians live in Supabase.
- **Demo data refreshes itself.** If the newest data is more than a day old, the server wipes the demo tables and creates fresh fake history timed to today. The **Reset demo data** button (`/demo.html`) does the same on purpose. Collected training breaths (`breaths_labelled`) are never wiped.
- **Every `git push` to `main` redeploys** automatically.
- Things that **don't** survive a Render restart (small, not demo-critical):
  - Voice settings chosen per patient (speaker, pace) go back to the patient's own language and the default voice.
  - A model re-trained with the **Train model** button (`/collect.html`) goes back to the one built during deploy. Press **Train model** again (on the free plan it can take a few minutes) – the collected breaths are read back from Supabase first, so none are lost.
  - Cached voice audio and translations are simply re-made when needed.
- Render's web address is filled in automatically as `PUBLIC_BASE_URL`, so Twilio/Sarvam call-backs work without extra setup.

---

## Optional keys (add any time)
None of these are needed. Without them the app uses its offline fallbacks (template text, recorded/browser voice, "would send" messages, calls ringing in the on-screen phone simulator).

To add one later: Render → **spirobuddy** → **Environment** → **Edit** → fill the value (or **Add Environment Variable** if it isn't listed) → **Save, rebuild, and deploy**.

| Key | What it turns on | Where to get it |
|---|---|---|
| `ANTHROPIC_API_KEY` | AI-written daily summaries and call scripts | console.anthropic.com → API Keys |
| `SARVAM_API_KEY` | Natural voice in 11 Indian languages, speech-to-text, translation | dashboard.sarvam.ai → API Keys |
| `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` | Real WhatsApp messages (sandbox) and calls | console.twilio.com (front page) |
| `TWILIO_VOICE_FROM` | Caller number for real Twilio calls | Twilio → Phone Numbers |
| `DEMO_FAMILY_WHATSAPP`, `DEMO_NURSE_WHATSAPP` | Where real WhatsApp demo messages go. Team phones only, like `whatsapp:+9198xxxxxxxx` | your team |
| `DEMO_PATIENT_PHONE`, `DEMO_GUARDIAN_PHONE`, `DEMO_NURSE_PHONE`, `NURSE_DESK_PHONE` | Where real demo calls go. Team phones only, like `+9198xxxxxxxx` | your team |
| `SARVAM_AGENT_*`, `SARVAM_ORG_ID`, `SARVAM_WORKSPACE_ID`, `SARVAM_CONNECTION_ID` | AI check-in phone call (Sarvam voice agent) | see `docs/COMMS.md` section 5 |
| `EXOTEL_*` | Indian caller ID for calls (needs a registered Indian business) | Exotel dashboard |

`SARVAM_WEBHOOK_SECRET` is generated by Render automatically. Real messages and calls only ever go to the team's own `DEMO_*` phones, never to the fake patients.

---

## Try Supabase from the laptop first (optional)
1. Open the file `.env` in the project folder with Notepad.
2. Set these lines and save:
   ```
   DATA_BACKEND=supabase
   SUPABASE_URL=https://abcdefghijk.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=sb_secret_...your key...
   ```
3. Run `powershell -ExecutionPolicy Bypass -File scripts\run.ps1`.
4. Open http://localhost:8000/api/health. It should say `"data_backend":"supabase"`.
5. To force fresh demo data into Supabase from the laptop: `.venv\Scripts\python.exe -m backend.app.seed --target supabase --force`

Only fake patients. Never put real health data in this demo.
