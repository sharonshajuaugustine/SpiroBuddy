# SpiroBuddy 2.0 – what you need to set up (founder steps)

There are **three things to do**, about 10 minutes in total. The app works without any of them (with fake data, the manual prescription path and the demo database). Each step switches on a little more.

| Step | What it switches on | Without it |
|---|---|---|
| 1. Gemini key | The AI reads sample prescriptions and suggests a title, type and date for uploaded papers. It also writes the short family and nurse summaries when there is no Anthropic key. | Staff type the prescription lines next to the photo (the "manual path"). Summaries use fixed template text. |
| 2. Supabase paste | The live site keeps its data in your Supabase database, and uploaded papers go to private Supabase storage. | The live site uses a temporary demo database. It resets when Render restarts, and a red "Database update needed" banner shows for the admin. |
| 3. Say "push" | The live site (spirobuddy.onrender.com) gets the new version. | The live site keeps showing the old version. |

---

## 1. Gemini key (free tier is enough)

1. Open **aistudio.google.com** and sign in with a Google account.
2. Click **Get API key**, then **Create API key**.
3. Click **Copy**.
4. **On your computer:** open the file `.env` in the SpiroBuddy folder (Notepad is fine). Find the line `GEMINI_API_KEY=` and paste the key right after the `=`, with no spaces. Save the file.
   - If the line isn't there, add a new line: `GEMINI_API_KEY=` and then your key.
5. **On Render:** open **dashboard.render.com**, then the **spirobuddy** service, then **Environment**.
6. Click **Add environment variable**. Name: `GEMINI_API_KEY`. Value: paste the key. Click **Save changes**. Render restarts the site by itself (about 2 minutes).

**Why the free tier is fine:** the demo only ever sends the **sample prescriptions** (fake, watermarked) to Gemini. The app also limits itself to 300 AI calls a day and 20 per visitor per hour, so the free quota can't run out during judging.

**Model:** the app uses `gemini-3.1-flash-lite`, as you asked. To switch later, add `GEMINI_MODEL` on Render with another model name, for example `gemini-3.8-flash`. No code change is needed.

**Never** paste the key into chat, into a file that goes to GitHub, or anywhere else. `.env` is never uploaded.

## 2. Supabase (one paste)

1. Open **supabase.com/dashboard** and open the **spirobuddy** project.
2. In the left menu, click **SQL Editor**, then **New query**.
3. On your computer, open `supabase/schema_v2.sql` in the SpiroBuddy folder. Select everything (Ctrl+A) and copy it (Ctrl+C).
4. Paste it into the Supabase query box (Ctrl+V) and click **Run**.
5. You should see **"Success. No rows returned"**. Running it twice is safe: it only adds things and never deletes data.
6. Wait about a minute, or restart the Render service (**Manual Deploy → Restart service**), so the site sees the new tables.
7. Log in to the live site as the demo admin (accounts below), open **Demo controls**, and click **Reset demo data**.

You don't need to create a storage bucket. The app creates its private `documents` bucket by itself.

## 3. Say "push"

When the build session asks **"Push now?"**, answer **push** at a time when nobody is looking at the live site. Each push restarts the live site for about 2 minutes.

After the push:
1. Open **https://spirobuddy.onrender.com/api/health** and wait until it shows `"ok": true`. The first visit after a quiet spell can take up to a minute, because the free Render plan sleeps.
2. Open **https://spirobuddy.onrender.com/login.html** and click **Try as Doctor**.
3. Open **Demo controls** and click **Prepare for recording**.

---

## Demo accounts (all fake – reset every night)

| Who | Email | Password |
|---|---|---|
| Hospital admin | `admin@demo-general.example` | `demo-admin-2026` |
| Dr. Meera Nair (surgeon) | `meera.nair@demo-general.example` | `demo-doctor-2026` |
| Dr. Kabir Rao | `kabir.rao@demo-general.example` | `demo-doctor-2026` |
| Sister Anjali (nurse) | `anjali@demo-general.example` | `demo-nurse-2026` |
| Nurse Thomas Mathew (limited access) | `thomas@demo-general.example` | `demo-nurse-2026` |
| Second hospital admin (for the "separate hospitals" check) | `admin@demo-riverside.example` | `demo-riverside-2026` |

- **Doctor join code** (for the sign-up page): `DEMO-2026`
- **Unused nurse access key** (for the redeem page): `DEMO-NURSE-KEY-0001`
- **Patient app** (Ravi, the demo patient): `/app.html?id=1`

These accounts exist only in demo mode. They are fictional, and the login page shows them on purpose.

## Optional keys (leave blank unless you already have them)

| Key | Switches on |
|---|---|
| `ANTHROPIC_API_KEY` | Claude writes the summaries first; Gemini is then the backup |
| `SARVAM_API_KEY` | Indian-language voice for new phrases (otherwise recorded clips or the phone's own voice) |
| `TWILIO_*`, `EXOTEL_*`, `SARVAM_AGENT_*` | Real WhatsApp messages and calls, to the team's own phones only (otherwise everything shows in the on-screen phone simulators) |
| `ALLOW_TRAINING=1` | Lets the admin record labelled breaths and retrain the model (off by default) |
| `SHOW_API_DOCS=1` | Shows the developer API pages at `/docs` (off by default) |
