"""Render the showroom videos to MP4 with headless Chrome + ffmpeg.

Usage (from the project folder):
  .venv\\Scripts\\python.exe tools\\render\\render_videos.py              # all 4 videos + the GLB
  .venv\\Scripts\\python.exe tools\\render\\render_videos.py hero exploded # only some
  options: --keep-frames  --swiftshader (force CPU rendering)  --port 8765
           --from N --to M (render only frames N..M-1, for quick checks; no MP4 is made unless the
           whole video is rendered)

Output: web/showcase/videos/<id>.mp4 (1920x1080, 30 fps, H.264, yuv420p) and hardware/3d/spirobuddy_setup.glb.
Needs internet once for the Three.js CDN and Google Fonts.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FRAMES = HERE / "_frames"
ALL = ["tour", "hero", "breath-types", "exploded"]
CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
]
GPU_FLAGS = ["--use-angle=d3d11", "--ignore-gpu-blocklist", "--enable-gpu-rasterization", "--enable-webgl"]
CPU_FLAGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--enable-webgl"]


def chrome_path() -> str:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    found = shutil.which("chrome") or shutil.which("chrome.exe")
    if found:
        return found
    sys.exit("Chrome not found. Install Google Chrome or edit CHROME_CANDIDATES.")


def get(url: str, timeout=3.0):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()


def status(port: int, vid: str) -> dict:
    try:
        return json.loads(get(f"http://localhost:{port}/status/{vid}"))
    except Exception:
        return {"state": "unknown", "frames": 0}


def start_server(port: int):
    try:
        get(f"http://localhost:{port}/showcase/")
        print(f"[render] using the server already running on port {port}")
        return None
    except Exception:
        pass
    p = subprocess.Popen([sys.executable, str(HERE / "render_server.py"), "--port", str(port)], cwd=str(ROOT))
    for _ in range(50):
        time.sleep(0.2)
        try:
            get(f"http://localhost:{port}/showcase/")
            return p
        except Exception:
            continue
    p.kill()
    sys.exit("render server did not start")


def run_one(vid: str, port: int, gpu: bool, glb: bool, rng: tuple[int | None, int | None], expect: int | None, resume: bool = False) -> bool:
    if not resume:
        shutil.rmtree(FRAMES / vid, ignore_errors=True)
    urllib.request.urlopen(urllib.request.Request(f"http://localhost:{port}/reset/{vid}", data=b"", method="POST"), timeout=5).read()
    q = f"render={vid}" + ("&glb=1" if glb else "")
    if rng[0] is not None:
        q += f"&from={rng[0]}"
    if rng[1] is not None:
        q += f"&to={rng[1]}"
    url = f"http://localhost:{port}/showcase/?{q}"
    prof = tempfile.mkdtemp(prefix="sb_chrome_")
    cmd = [chrome_path(), "--headless=new", *(GPU_FLAGS if gpu else CPU_FLAGS), "--window-size=1920,1080", "--hide-scrollbars",
           "--mute-audio", "--no-first-run", "--no-default-browser-check", "--disable-background-timer-throttling",
           "--disable-renderer-backgrounding", "--disable-backgrounding-occluded-windows", "--force-device-scale-factor=1",
           f"--user-data-dir={prof}", url]
    print(f"[render] {vid}: Chrome ({'GPU d3d11' if gpu else 'SwiftShader CPU'}) -> {url}")
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    t0, last_n, last_change = time.time(), -1, time.time()
    ok = False
    try:
        while True:
            time.sleep(1.0)
            s = status(port, vid)
            n = s.get("frames", 0)
            if n != last_n:
                last_n, last_change = n, time.time()
                el = time.time() - t0
                if expect:
                    print(f"\r[render] {vid}: frame {n}/{expect}  ({n / max(el, 1e-3):.1f} fps, {el:.0f}s)   ", end="", flush=True)
            if s.get("state") == "done":
                print(f"\n[render] {vid}: done -> {s.get('msg')}")
                ok = True
                break
            if s.get("state") == "error":
                print(f"\n[render] {vid}: ERROR {s.get('msg', '')[:600]}")
                break
            if rng[1] is not None and n >= rng[1]:
                print(f"\n[render] {vid}: partial frames written to {FRAMES / vid}")
                ok = True
                break
            if time.time() - last_change > (90 if n <= 0 else 60):
                print(f"\n[render] {vid}: no progress for a while (state={s.get('state')}) – giving up on this run")
                break
            if proc.poll() is not None and s.get("state") not in ("encoding",):
                print(f"\n[render] {vid}: Chrome exited early")
                break
    finally:
        proc.kill()
        try:
            proc.wait(10)
        except Exception:
            pass
        shutil.rmtree(prof, ignore_errors=True)
    return ok


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", default=ALL)
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--keep-frames", action="store_true")
    ap.add_argument("--swiftshader", action="store_true")
    ap.add_argument("--from", dest="frm", type=int)
    ap.add_argument("--to", type=int)
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found on PATH")
    durations = {"tour": 92, "hero": 20, "breath-types": 35, "exploded": 15}
    srv = start_server(a.port)
    results = {}
    try:
        for i, vid in enumerate(a.ids):
            expect = durations.get(vid, 0) * 30
            glb = i == 0 and a.frm is None
            ok = run_one(vid, a.port, not a.swiftshader, glb, (a.frm, a.to), expect)
            for attempt in range(3):  # resume on the GPU from the first missing frame
                if ok or a.swiftshader or a.frm is not None:
                    break
                have = 0
                while (FRAMES / vid / f"f_{have:05d}.jpg").exists():
                    have += 1
                print(f"[render] {vid}: resuming on GPU from frame {have} (attempt {attempt + 1})")
                ok = run_one(vid, a.port, True, False, (have, None), expect, resume=True)
            if not ok and not a.swiftshader:
                print(f"[render] {vid}: retrying with SwiftShader (CPU)")
                ok = run_one(vid, a.port, False, glb, (a.frm, a.to), expect)
            if ok and a.frm is None:  # wait for ffmpeg
                for _ in range(600):
                    s = status(a.port, vid)
                    if s.get("state") in ("done", "error"):
                        break
                    time.sleep(1)
            results[vid] = ok
            if ok and not a.keep_frames and a.frm is None:
                shutil.rmtree(FRAMES / vid, ignore_errors=True)
    finally:
        if srv:
            srv.terminate()
    for vid, ok in results.items():
        out = ROOT / "web" / "showcase" / "videos" / f"{vid}.mp4"
        print(f"  {vid:13s} {'OK  ' if ok else 'FAIL'} {out if out.exists() else ''}")


if __name__ == "__main__":
    main()
