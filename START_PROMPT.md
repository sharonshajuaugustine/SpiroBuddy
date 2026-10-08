# Paste this as the first message in a new Claude Code session opened in this folder

---

You are the senior engineer and lead developer for SpiroBuddy, a hackathon project that starts in under 24 hours. Work autonomously until the MVP demo works, then keep improving. Don't wait for me between steps.

1. Read CLAUDE.md, then docs/HANDOFF.md, docs/PROGRESS.md, docs/REQUIREMENTS.md, docs/ARCHITECTURE.md and docs/ROLES.md. Follow the contracts in ARCHITECTURE.md exactly.
2. Run scripts\setup.ps1 to install the Python packages (in the background if slow).
3. Start 4 subagents in parallel, one per role in docs/ROLES.md: Firmware & Hardware, Backend, ML, Frontend. Give each one a complete, self-contained prompt: its folders, the contracts it must follow, the "done when" test, and an instruction to check library APIs against the web docs instead of guessing. Each must stay inside its own folders.
4. While they work, write scripts\run.ps1 and the remaining shared files.
5. When they finish, act as QA: start the server, test every API endpoint, and walk through the demo story in docs/REQUIREMENTS.md §3 in Simulator mode in the built-in browser. Fix every seam between the parts.
6. After each milestone, update docs/PROGRESS.md and docs/HANDOFF.md and make a git commit. HANDOFF.md must always be enough for a brand-new session on another account to continue.
7. When the MVP passes, do the nice-to-haves in REQUIREMENTS §4 in order, then write docs/DEMO_GUIDE.md: step-by-step instructions for running the demo on hackathon day, including what to do for each hardware option and every backup plan.

I don't know yet which hardware I'll get, so everything must work in Simulator and Camera modes. The app must work without API keys (fallbacks), and tell me exactly which keys to add to .env and how to get them. Explain things to me in plain, simple English, and report clearly what's done, what failed and what's waiting on me.

---

## If a session runs out and you continue on another account
Open a new session in this folder and paste:

> Continue the SpiroBuddy project. Read CLAUDE.md and docs/HANDOFF.md first, then carry on from "Next steps" in HANDOFF.md. Keep updating PROGRESS.md and HANDOFF.md and commit after each milestone.
