"""Make the pre-recorded voice clip library with Sarvam TTS.

    .venv\\Scripts\\python.exe tools\\voice\\make_clips.py                 # all 11 languages
    .venv\\Scripts\\python.exe tools\\voice\\make_clips.py --lang hi ta    # some languages
    .venv\\Scripts\\python.exe tools\\voice\\make_clips.py --force         # re-make existing clips

Writes web/audio/<lang>/<cue>.mp3 for every cue in backend/app/voice_cues.py, plus
web/audio/cues.json (all cue texts – the browser uses it to speak cues even with no server).
Without SARVAM_API_KEY it only writes cues.json and says so. Sarvam's Starter plan allows
30 bulbul:v3 requests per minute, so the script paces itself (about 12 minutes for all ~340).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.app import voice  # noqa: E402
from backend.app.voice_cues import CUE_ORDER, LANG_ORDER, all_cues, cue_text  # noqa: E402

AUDIO_DIR = ROOT / "web" / "audio"
MIN_GAP_S = 2.1          # 30 requests/min on Starter for bulbul:v3


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", nargs="*", default=LANG_ORDER, help="language codes, e.g. hi ta or")
    ap.add_argument("--cues", nargs="*", default=CUE_ORDER, help="cue ids (default: all)")
    ap.add_argument("--force", action="store_true", help="re-make clips that already exist")
    args = ap.parse_args()

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    (AUDIO_DIR / "cues.json").write_text(json.dumps(all_cues(), ensure_ascii=False, indent=1),
                                         encoding="utf-8")
    print(f"Wrote {AUDIO_DIR / 'cues.json'} ({len(CUE_ORDER)} cues x {len(LANG_ORDER)} languages)")

    langs = [voice.norm_lang(x) for x in args.lang]
    bad = [a for a, b in zip(args.lang, langs) if not b]
    if bad:
        print(f"Unknown language(s): {bad}. Use: {' '.join(LANG_ORDER)}")
        return 2
    if not voice.enabled():
        print("No SARVAM_API_KEY in .env - no clips made. The website still speaks every cue with "
              "the browser's own voice. Add the key (docs/VOICE.md) and run this again.")
        return 0

    made = skipped = failed = 0
    total = len(langs) * len(args.cues)
    last_call = 0.0
    print(f"Model {voice.tts_model()}, pace {voice.default_pace()}, {total} clips to check.")
    for lg in langs:
        out_dir = AUDIO_DIR / lg
        out_dir.mkdir(parents=True, exist_ok=True)
        for cue in args.cues:
            text = cue_text(cue, lg)
            dest = out_dir / f"{cue}.mp3"
            if not text:
                print(f"  ? unknown cue {cue}")
                failed += 1
                continue
            if dest.exists() and not args.force:
                skipped += 1
                continue
            key = voice.cache_key(text, lg, voice.speaker_for(lg), voice.default_pace(), "mp3")
            if not (voice.TTS_CACHE_DIR / f"{key}.mp3").exists():   # needs an API call: pace it
                wait = MIN_GAP_S - (time.time() - last_call)
                if wait > 0:
                    time.sleep(wait)
                last_call = time.time()
            path = voice.tts(text, lg, fmt="mp3")
            if path:
                shutil.copyfile(path, dest)
                made += 1
                print(f"  ok {lg}/{cue}.mp3  {text[:50]}", flush=True)
            else:
                failed += 1
                print(f"  FAILED {lg}/{cue}  (see the warning above)", flush=True)
                if failed >= 5 and made == 0:
                    print("Stopping: the first 5 clips all failed (check the key and credits).")
                    break
        else:
            continue
        break
    print(f"\nDone: {made} clips made, {skipped} already there, {failed} failed "
          f"(of {total}). Files are in {AUDIO_DIR}.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
