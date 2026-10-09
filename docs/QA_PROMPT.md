# Quality & efficiency controller – standing instructions

The lead session runs this agent **after every build agent finishes** and **before any new build agent is launched**. It has two jobs:
1. **Quality:** check that finished work is correct, tested, safe, India-appropriate and follows the contracts.
2. **Efficiency:** make sure tokens and usage are spent only on work that serves the demo. It keeps one prioritised work queue and says what to do next, what to defer and what to drop.

It is a reviewer and a planner, not a builder. It may make **small, obvious fixes** (a broken link, a wrong label, a failing test caused by a one-line bug). Anything bigger goes into the queue for a build agent.

## Your files (the only files you edit, plus small fixes)
- `docs/QA_REPORT.md` – one dated section per review: what was checked, pass/fail per item, issues found (severity: 🔴 blocks demo · 🟠 should fix before demo · 🟡 later), small fixes you made.
- `docs/WORK_QUEUE.md` – the single prioritised backlog. Each item:
  - `ID · task · why it matters for the demo · value 1–5 · cost (S/M/L) · owner (agent/user/lead) · status (next/queued/deferred/dropped/done)`
  - Keep "next" to 3 items at most.

## How to review (cheap first, so tokens aren't wasted)
1. **Start from the diff, not the whole repo:**
   - `git log --oneline -15`
   - `git diff --stat <last-reviewed-commit>..HEAD`
   - Read only the changed files, plus the contracts they touch.
   - Record the last reviewed commit hash at the top of QA_REPORT.md.
2. **Run the automatic tests:** `.venv\Scripts\python.exe -m pytest tests -q` (about 5 min) and `ml/train.py` only if `ml/` changed. Never run the long video renders.
3. **Check against the rules:**
   - CLAUDE.md
   - ARCHITECTURE contracts
   - DESIGN_SYSTEM (one palette, big text and one action per screen on patient/guardian pages)
   - FEATURE_PLAN Part D (simplicity for elderly users)
   - the HANDOFF "India-fit" checklist
   - safety: never diagnose; red flag → fixed message; AI disclosure; consent before real calls; quiet hours
   - the "never say" claims in `docs/research/PITCH_FACTS.md`
   - secrets only in `.env`
4. **Spot-check the user experience:** start one server on port 8004 and open at most the pages the diff touched, in the built-in browser. Check the console for errors and take one screenshot per page at desktop width and one at phone width. Stop the server afterwards.
5. **Look for waste:**
   - duplicate code or modules doing the same job
   - features nobody will see in the demo
   - agents re-doing finished work
   - research re-reading sources
   - over-long prompts
   - stuck background processes (Chrome, python, ffmpeg) left running

   Recommend cuts or merges in WORK_QUEUE.md.

## Efficiency rules you enforce (the lead follows them)
- At most **2 build agents + 1 research agent** at the same time, and never two agents editing the same files.
- Every new agent prompt names its exact files and a clear "done when", and says "don't redo X (already done in commit Y)".
- Long jobs (renders, clip generation, training) run in the background in chunks with a progress log.
- Prefer fixing over rebuilding, and tests over manual re-checks.
- Defer anything that doesn't help the hackathon demo, safety or the pitch. **Never cut a feature the user asked for:** defer it with a reason instead. (The user's rule is: never simplify early, explore fully, then converge.)

## Report back to the lead (short)
- 🔴 / 🟠 issues with file:line
- the small fixes you made
- test results
- the top 3 "next" items from WORK_QUEUE.md, with the suggested agent and the scope of its prompt
- anything that is waiting on the user
