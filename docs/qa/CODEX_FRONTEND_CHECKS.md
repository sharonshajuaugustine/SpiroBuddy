# Frontend syntax checks

Date: 2026-10-12. Latest read-only sweep after consent, login and navbar changes.

Checked **40 JavaScript sources**: 35 standalone files under `web/` and 5 inline JavaScript blocks across `web/app.html`, `web/register.html`, `web/patient-login.html`, `web/prescription-print.html`, and `web/login.html`.

Result: **40 passed; 0 failed**.

## Commands and method

Bundled Node executable: `C:/Users/USER/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe`.

Every standalone file was checked with `node --check <absolute source path>`. Python standard-library `HTMLParser` extracted eligible inline JavaScript/module blocks to ignored `.build/frontend-syntax/`; each was checked with `node --check <extracted .js/.mjs path>`. Scripts with external `src` were excluded from inline extraction and local JavaScript files were covered by the full standalone sweep. No vendor files were skipped.

Per-file results: `.build/frontend-syntax/results.json`.

## Navigation review

- New root navigation targets `doctor-day.html` and `appointments.html` exist. Both legacy entries set `initialHidden: true`; nav rendering applies the HTML `hidden` attribute before identity resolves.
- Authenticated visibility permits My day only for doctors; Appointments permits admin/doctor and nurses with `manage_appointments`. Hospital-shell Appointments now targets the existing `/appointments.html`.
- The doctor-day navigation key is `doctor-day`. Shared navigation compares page keys for `aria-current` and does not require a separately registered page key for booting; matching the boot key controls highlighting, not route authorization.
- Login fallback derives the destination from the authenticated `SB.auth.me()` role, selects `/doctor-day.html` for doctors and preserves the existing validated same-origin `?next` destination. It does not trust the clicked demo login role.

These are static findings. Role enforcement remains the server's responsibility; syntax checks do not establish successful browser behavior or server integration.

## Failures

None.

No application files or tests were edited. The physical root AGENTS.md was absent; supplied session instructions were followed. Concurrent edits may supersede this snapshot.
