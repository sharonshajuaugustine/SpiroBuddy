"""Headless-Chrome page check for SpiroBuddy (QA tool, not part of the product).

Starts its own server on a free port with a throw-away data folder (DEMO_MODE, no keys), logs in
as a role, opens pages at phone and desktop width in light and dark, and reports console errors,
failed requests, sideways scroll at 375 px and a screenshot per view.

    .venv/Scripts/python.exe tools/qa/browser_check.py --role doctor /hospital/patients.html /hospital/patient.html?id=1
    .venv/Scripts/python.exe tools/qa/browser_check.py --role patient:1 /app.html?id=1 --out shots/
    .venv/Scripts/python.exe tools/qa/browser_check.py --base http://127.0.0.1:8000 --role none /

Roles: none | admin | doctor | doctor2 | nurse | nurse2 | riverside | patient:<id>  (accounts: docs/REBUILD_PLAN.md §2).
Needs: pip install playwright (uses the installed Google Chrome via channel="chrome").
In Git Bash, prefix with MSYS_NO_PATHCONV=1 so "/hospital/..." is not turned into a Windows path.
Exit code 1 if any view has console errors, failed same-origin requests or sideways scroll.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = ROOT / ".venv" / "Scripts" / "python.exe"
ACCOUNTS = {
    "admin": ("admin@demo-general.example", "demo-admin-2026"),
    "doctor": ("meera.nair@demo-general.example", "demo-doctor-2026"),
    "doctor2": ("kabir.rao@demo-general.example", "demo-doctor-2026"),
    "nurse": ("anjali@demo-general.example", "demo-nurse-2026"),
    "nurse2": ("thomas@demo-general.example", "demo-nurse-2026"),
    "riverside": ("admin@demo-riverside.example", "demo-riverside-2026"),
}
KEYS_EMPTY = ["ANTHROPIC_API_KEY", "SARVAM_API_KEY", "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN",
              "SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "EXOTEL_API_KEY", "EXOTEL_API_TOKEN",
              "SARVAM_AGENT_ID", "GEMINI_API_KEY"]


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_server(port: int, extra_env: dict | None = None) -> subprocess.Popen:
    env = dict(os.environ)
    env.update({"SPIROBUDDY_DATA_DIR": tempfile.mkdtemp(prefix="sb-qa-"), "DEMO_MODE": "1",
                "DATA_BACKEND": "demo", "DEMO_AUTOPILOT": "0", "COMMS_TICKER": "0"})
    for k in KEYS_EMPTY:
        env[k] = ""
    env.update(extra_env or {})
    proc = subprocess.Popen([str(PY), "-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1",
                             "--port", str(port)], cwd=str(ROOT), env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(120):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/health", timeout=2) as r:
                if json.load(r).get("ok"):
                    return proc
        except Exception:
            time.sleep(0.5)
    proc.kill()
    raise SystemExit("server did not start")


def login(ctx, base: str, role: str) -> None:
    if role in ("none", ""):
        return
    if role.startswith("patient:"):
        r = ctx.request.post(f"{base}/api/me/session", data={"patient_id": int(role.split(":")[1])},
                             headers={"X-SB": "1"})
    else:
        email, pw = ACCOUNTS[role]
        r = ctx.request.post(f"{base}/api/auth/login", data={"email": email, "password": pw},
                             headers={"X-SB": "1"})
    if not r.ok:
        raise SystemExit(f"login as {role} failed: {r.status} {r.text()[:200]}")


def check(base: str, role: str, pages: list[str], out: Path, widths=(375, 1440),
          schemes=("light", "dark"), wait_ms: int = 1500) -> list[dict]:
    from playwright.sync_api import sync_playwright
    results = []
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        for scheme in schemes:
            for w in widths:
                ctx = browser.new_context(viewport={"width": w, "height": 900 if w > 600 else 812},
                                          color_scheme=scheme, device_scale_factor=1)
                login(ctx, base, role)
                for path in pages:
                    page = ctx.new_page()
                    errors, failed = [], []
                    page.on("console", lambda m, e=errors: e.append(f"{m.text} @ {(m.location or {}).get('url', '')}")
                            if m.type == "error" else None)
                    page.on("pageerror", lambda exc, e=errors: e.append(f"pageerror: {exc}"))
                    page.on("requestfailed", lambda req, f=failed: f.append(f"{req.method} {req.url} {req.failure}")
                            if req.url.startswith(base) else None)
                    page.on("response", lambda res, f=failed: f.append(f"{res.status} {res.url}")
                            if res.url.startswith(base) and res.status >= 400 else None)
                    page.goto(base + path, wait_until="load", timeout=30000)
                    page.wait_for_timeout(wait_ms)
                    sideways = page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
                    name = f"{path.strip('/').replace('/', '_').replace('?', '_').replace('=', '-') or 'root'}_{w}_{scheme}.png"
                    page.screenshot(path=str(out / name), full_page=True)
                    results.append({"page": path, "width": w, "scheme": scheme, "final_url": page.url,
                                    "console_errors": errors, "failed_requests": failed,
                                    "sideways_scroll": bool(sideways and w <= 420), "screenshot": str(out / name)})
                    page.close()
                ctx.close()
        browser.close()
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("pages", nargs="+")
    ap.add_argument("--role", default="none")
    ap.add_argument("--base", default="", help="use a running server instead of starting one")
    ap.add_argument("--out", default=str(Path(tempfile.gettempdir()) / "sb-qa-shots"))
    ap.add_argument("--widths", default="375,1440")
    ap.add_argument("--schemes", default="light,dark")
    ap.add_argument("--env", action="append", default=[], help="extra server env NAME=VALUE")
    a = ap.parse_args()
    proc = None
    base = a.base.rstrip("/")
    if not base:
        port = free_port()
        proc = start_server(port, dict(e.split("=", 1) for e in a.env))
        base = f"http://127.0.0.1:{port}"
    try:
        res = check(base, a.role, a.pages, Path(a.out), tuple(int(x) for x in a.widths.split(",")),
                    tuple(a.schemes.split(",")))
    finally:
        if proc:
            proc.kill()
    bad = [r for r in res if r["console_errors"] or r["failed_requests"] or r["sideways_scroll"]]
    print(json.dumps(res, indent=1, ensure_ascii=False))
    print(f"\n{len(res)} views, {len(bad)} with problems", file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
