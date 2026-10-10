-- Keep the Render free-plan web service awake (it sleeps after ~15 minutes with no visitors and
-- then takes minutes to wake). Supabase visits the health page every 5 minutes.
-- Applied to the "spirobuddy" project on 10 Oct 2026. Safe to run again.
-- To stop it:  select cron.unschedule('keep-spirobuddy-awake');
-- To check it: select status, start_time from cron.job_run_details order by start_time desc limit 5;
create extension if not exists pg_cron;
create extension if not exists pg_net;

select cron.unschedule(jobid) from cron.job where jobname = 'keep-spirobuddy-awake';

select cron.schedule(
  'keep-spirobuddy-awake',
  '*/5 * * * *',
  $$select net.http_get(url := 'https://spirobuddy.onrender.com/api/health', timeout_milliseconds := 20000)$$
);
