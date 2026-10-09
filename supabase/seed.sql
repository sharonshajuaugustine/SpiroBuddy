-- SpiroBuddy demo patients (fake people only). OPTIONAL.
--
-- You normally do NOT need this file: when the server starts with DEMO_MODE=1 and finds no
-- recent data, it wipes the demo tables and re-seeds 7 patients with 7 days of history timed
-- to the current hour (Asia/Kolkata). The "Reset demo" button (POST /api/demo/reset) does the
-- same. Or from a laptop with the keys in .env:
--     .venv\Scripts\python.exe -m backend.app.seed --target supabase --force
--
-- This file only inserts the 7 patient rows, so the dashboard has names even before the
-- server has run. The server fills in sessions, breaths and slots on its next start.

insert into public.patients
  (id, name, age, sex, surgery, surgery_date, language, target_ml, hold_target_s, personal_best_ml)
values
  (1, 'Ravi Kumar',    58, 'M', 'Abdominal surgery (open hernia repair)',     current_date - 8, 'hi', 2000, 3, 0),
  (2, 'Priya Sharma',  44, 'F', 'Laparoscopic cholecystectomy (gallbladder)', current_date - 5, 'en', 2500, 3, 0),
  (3, 'Abdul Rahman',  63, 'M', 'Heart bypass surgery (CABG)',                current_date - 9, 'en', 1500, 3, 0),
  (4, 'Lakshmi Iyer',  66, 'F', 'Total knee replacement',                     current_date - 6, 'ta', 1500, 3, 0),
  (5, 'Mohan Das',     50, 'M', 'Lung rehab after TB treatment (post-TB)',    current_date - 7, 'hi', 1750, 3, 0),
  (6, 'Sreedevi Nair', 54, 'F', 'Hysterectomy',                               current_date - 4, 'ml', 2250, 3, 0),
  (7, 'Arjun Reddy',   41, 'M', 'Appendix removal (appendectomy)',            current_date - 3, 'en', 3000, 3, 0)
on conflict (id) do nothing;

-- Keep the id counter past the fixed demo ids.
select setval(pg_get_serial_sequence('public.patients', 'id'),
              greatest((select max(id) from public.patients), 7));
