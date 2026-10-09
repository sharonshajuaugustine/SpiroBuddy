#!/usr/bin/env bash
# Render single frames of a video for checking: sample_frames.sh <id> <frame> [<frame> ...]
# Writes tools/render/_frames/<id>/f_NNNNN.jpg. Needs render_server.py running on :8765.
id=$1; shift
for f in "$@"; do
  P=$(mktemp -d)
  "/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --use-angle=d3d11 --ignore-gpu-blocklist --enable-webgl \
    --window-size=1920,1080 --hide-scrollbars --no-first-run --force-device-scale-factor=1 --user-data-dir="$P" \
    "http://localhost:8765/showcase/?render=$id&from=$f&to=$((f+1))" >/dev/null 2>&1 &
  pid=$!
  for i in $(seq 1 40); do sleep 0.5; [ -f "$(dirname "$0")/_frames/$id/$(printf 'f_%05d.jpg' $f)" ] && break; done
  sleep 0.3; kill $pid 2>/dev/null; wait $pid 2>/dev/null; rm -rf "$P"
  echo "frame $f done"
done
