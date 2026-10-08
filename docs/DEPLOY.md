# Deploy SpiroBuddy online (Supabase + Render)

**In short:** Supabase keeps the data, Render runs the website. You make two free accounts, paste one file into Supabase, copy two secrets, and let Render build from GitHub. It takes about 20 minutes.

Think of it like a shop: **Render** is the shop front people walk into (the website), and **Supabase** is the stock room behind it (the database). Only the shop staff (our server) has the stock-room key. Customers' browsers never get it.

Nothing here is needed to run the demo on the laptop. `scripts\run.ps1` works with no accounts at all and uses a local demo database.

Legend: **[YOU]** = waiting on you · **[DONE]** = already in the project

---

## What's already done [DONE]
- `supabase/schema.sql` creates the tables. `supabase/seed.sql` adds the 7 fake patients (optional).
- `render.yaml` tells Render how to build and start the app.
- The server fills in 7 days of fake demo history by itself the first time it starts.
- If Supabase is missing or broken, the server still runs on its own temporary demo data.

---

## Part 1 – Supabase (the database) [YOU]

1. Go to https://supabase.com and click **Start your project**. Sign in with GitHub (easiest).
2. Click **New project**.
   - Name: `spirobuddy`
   - Database password: click **Generate a password** and save it somewhere (you won't need it for the app).
   - Region: **Mumbai (ap-south-1)** if offered, otherwise Singapore.
   - Click **Create new project** and wait 1–2 minutes.
3. In the left sidebar click **SQL Editor**, then **New query**.
4. Open `supabase/schema.sql` from this project in Notepad, copy **everything**, paste it into the editor and click **Run**. You should see "Success. No rows returned".
5. (Optional) New query again, paste all of `supabase/seed.sql`, click **Run**.
6. Copy the two values the server needs:
   - **Project URL**: click **Connect** at the top of the page (or **Project Settings → Data API**). It looks like `https://abcdefgh.supabase.co`.
   - **Secret key**: **Project Settings → API Keys**. Copy a **secret** key (starts with `sb_secret_`). If you only see the "Legacy API keys" tab, copy the **service_role** key instead (a long text starting with `eyJ`). Both work.
   - Do **not** use the "publishable" / "anon" key: it can't read the tables (on purpose).
7. Keep both values for Part 3. **Never** paste the secret key into a chat, a screenshot, GitHub or the website code.

**Try it on the laptop first (optional but recommended):**
1. Open the file `.env` in the project folder with Notepad.
2. Set these lines and save:
   ```
   DATA_BACKEND=supabase
   SUPABASE_URL=https://abcdefgh.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=sb_secret_...your key...
   ```
3. Run `powershell -ExecutionPolicy Bypass -File scripts\run.ps1`.
4. Open http://localhost:8000/api/health. It should say `"data_backend":"supabase"`. If it says `"demo"`, read `data_note` on the same page: it says what went wrong.
5. In Supabase, click **Table Editor → patients**: you should see the 7 fake patients.

---

## Part 2 – Put the code on GitHub [YOU, or ask Claude]

1. Go to https://github.com/new. Name it `spirobuddy`, choose **Private**, and click **Create repository**. Don't tick "Add a README".
2. In a terminal in the project folder, paste the two lines GitHub shows under "…or push an existing repository from the command line". They look like this:
   ```
   git remote add origin https://github.com/YOUR-NAME/spirobuddy.git
   git push -u origin master
   ```
3. Check: `.env` must **not** appear on GitHub. It's in `.gitignore`, so it shouldn't.

---

## Part 3 – Render (the website) [YOU]

1. Go to https://render.com and sign up with **GitHub**.
2. Click **New +** → **Blueprint**.
3. Choose your `spirobuddy` repository (click **Configure GitHub** if it's not listed, and give Render access to that repo).
4. Render reads `render.yaml` and shows a service called **spirobuddy**. It asks for the secret values:
   - `SUPABASE_URL` → the Project URL from Part 1
   - `SUPABASE_SERVICE_ROLE_KEY` → the secret key from Part 1
   - `ANTHROPIC_API_KEY` → your Anthropic key, or leave it empty (the app then uses template text)
   - `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` → from the Twilio console, or leave empty (WhatsApp then shows "would send")
   - `DEMO_FAMILY_WHATSAPP`, `DEMO_NURSE_WHATSAPP` → the demo phones, like `whatsapp:+9198xxxxxxxx`, or leave empty
5. Click **Deploy Blueprint**. The first build takes about 3–6 minutes.
6. When it says **Live**, click the link (like `https://spirobuddy.onrender.com`).

**Check it works:**
1. Open `https://YOUR-APP.onrender.com/api/health`.
2. You should see `"ok":true` and `"data_backend":"supabase"`.
   - `"data_backend":"demo"` means Render couldn't reach Supabase. Check the two Supabase values: **Dashboard → spirobuddy → Environment**, fix them, and click **Save, rebuild and deploy**.
3. Open `https://YOUR-APP.onrender.com/` for the dashboard and `/showcase/` for the 3D showroom.

**Good to know**
- The free Render plan goes to sleep after about 15 minutes without visitors. The first visit after that takes up to a minute. **Open the site a few minutes before you present.**
- Without Supabase, Render's disk is wiped on every restart, so the demo data starts fresh each time. That's fine for a demo.
- To add or change a secret later: **Dashboard → spirobuddy → Environment**.
- Every `git push` to the repo redeploys automatically.

---

## Demo data
- The server re-creates the fake demo history when the tables are empty or the data is more than a day old.
- To reset on purpose, use the **Reset demo** button on the demo page (it calls `POST /api/demo/reset`).
- From the laptop: `.venv\Scripts\python.exe -m backend.app.seed --target supabase --force`
- Only fake patients. Never put real health data in this demo.
