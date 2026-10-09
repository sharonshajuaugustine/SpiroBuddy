"""Tiny local server for rendering the showroom videos (stdlib only).

Serves web/ at http://localhost:8765/ and accepts:
  POST /frame/<id>/<n>   JPEG frame n of video <id>  -> tools/render/_frames/<id>/f_00000.jpg
  POST /done/<id>        JSON {frames, fps, beeps:[{t,f,d}]} -> ffmpeg -> web/showcase/videos/<id>.mp4
  POST /fail/<id>        error text from the page
  POST /reset/<id>       clear the status of <id> before a new run
  POST /glb              binary GLB -> hardware/3d/spirobuddy_setup.glb
  POST /log              text, printed to the console
  GET  /status/<id>      JSON {state, frames, msg}

Run:  .venv\\Scripts\\python.exe tools\\render\\render_server.py [--port 8765]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "web"
FRAMES = Path(__file__).resolve().parent / "_frames"
VIDEOS = WEB / "showcase" / "videos"
GLB = ROOT / "hardware" / "3d" / "spirobuddy_setup.glb"

STATUS: dict[str, dict] = {}
LOCK = threading.Lock()


def set_status(vid: str, **kw) -> None:
    with LOCK:
        STATUS.setdefault(vid, {"state": "idle", "frames": 0, "msg": ""}).update(kw)


def encode(vid: str, info: dict) -> None:
    """Frames -> H.264 MP4 (yuv420p, 30 fps) with optional synthesised beeps."""
    fps = int(info.get("fps", 30))
    frames_dir = FRAMES / vid
    VIDEOS.mkdir(parents=True, exist_ok=True)
    out = VIDEOS / f"{vid}.mp4"
    duration = float(info.get("duration") or info.get("frames", 0) / fps)
    beeps = info.get("beeps") or []
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-framerate", str(fps), "-i", str(frames_dir / "f_%05d.jpg")]
    if beeps:
        # one sine source per beep, delayed to its time, mixed onto a silent bed
        filt, labels = [], []
        cmd += ["-f", "lavfi", "-t", f"{duration:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
        for i, b in enumerate(beeps):
            d = float(b.get("d", 0.15))
            cmd += ["-f", "lavfi", "-t", f"{d:.3f}", "-i", f"sine=frequency={float(b['f']):.0f}:sample_rate=48000"]
            ms = int(max(0.0, float(b["t"])) * 1000)
            filt.append(f"[{i + 2}:a]volume=1.6,afade=t=in:d=0.01,afade=t=out:st={max(0.0, d - 0.04):.3f}:d=0.04,"
                        f"aformat=channel_layouts=stereo,adelay={ms}|{ms}[b{i}]")
            labels.append(f"[b{i}]")
        filt.append(f"[1:a]{''.join(labels)}amix=inputs={len(labels) + 1}:normalize=0:duration=first[aout]")
        cmd += ["-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[aout]", "-c:a", "aac", "-b:a", "128k"]
    cmd += ["-vf", "scale=in_range=full:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-color_range", "tv", "-r", str(fps),
            "-movflags", "+faststart", "-shortest" if beeps else "-an", str(out)]
    set_status(vid, state="encoding")
    print(f"[render] encoding {vid}: {info.get('frames')} frames", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 and beeps:
        print(f"[render] audio mux failed, retrying without sound:\n{r.stderr[-800:]}", flush=True)
        r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-framerate", str(fps), "-i", str(frames_dir / "f_%05d.jpg"),
                            "-vf", "scale=in_range=full:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-color_range", "tv", "-r", str(fps), "-movflags", "+faststart", str(out)],
                           capture_output=True, text=True)
    if r.returncode == 0:
        set_status(vid, state="done", msg=str(out))
        print(f"[render] wrote {out} ({out.stat().st_size / 1e6:.1f} MB)", flush=True)
    else:
        set_status(vid, state="error", msg=r.stderr[-2000:])
        print(f"[render] ffmpeg failed for {vid}:\n{r.stderr[-2000:]}", flush=True)


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):  # keep the console quiet (frames are many)
        if "/frame/" not in (self.path or "") and "/status/" not in (self.path or ""):
            sys.stderr.write("[http] " + (fmt % args) + "\n")

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> bytes:
        n = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(n) if n else b""

    def do_GET(self):
        if self.path.startswith("/status/"):
            vid = self.path.split("/")[2]
            with LOCK:
                return self._json(STATUS.get(vid, {"state": "idle", "frames": 0, "msg": ""}))
        return super().do_GET()

    def do_POST(self):
        parts = [p for p in self.path.split("?")[0].split("/") if p]
        data = self._body()
        if len(parts) == 3 and parts[0] == "frame":
            vid, n = parts[1], int(parts[2])
            d = FRAMES / vid
            d.mkdir(parents=True, exist_ok=True)
            (d / f"f_{n:05d}.jpg").write_bytes(data)
            set_status(vid, state="rendering", frames=n + 1)
            return self._json({"ok": True})
        if len(parts) == 2 and parts[0] == "done":
            vid = parts[1]
            info = json.loads(data or b"{}")
            set_status(vid, state="encoding")
            threading.Thread(target=encode, args=(vid, info), daemon=True).start()
            return self._json({"ok": True})
        if len(parts) == 2 and parts[0] == "reset":
            with LOCK:
                STATUS[parts[1]] = {"state": "idle", "frames": 0, "msg": ""}
            return self._json({"ok": True})
        if len(parts) == 2 and parts[0] == "fail":
            set_status(parts[1], state="error", msg=data.decode(errors="replace"))
            print(f"[render] page error for {parts[1]}: {data.decode(errors='replace')}", flush=True)
            return self._json({"ok": True})
        if parts == ["glb"]:
            GLB.parent.mkdir(parents=True, exist_ok=True)
            GLB.write_bytes(data)
            print(f"[render] wrote {GLB} ({len(data) / 1e6:.2f} MB)", flush=True)
            return self._json({"ok": True})
        if parts == ["log"]:
            print("[page] " + data.decode(errors="replace"), flush=True)
            return self._json({"ok": True})
        return self._json({"error": "not found"}, 404)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        print("[render] WARNING: ffmpeg not found on PATH – videos cannot be encoded", flush=True)
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), partial(Handler, directory=str(WEB)))
    print(f"[render] serving {WEB} at http://localhost:{a.port}/  (showroom: /showcase/)", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
