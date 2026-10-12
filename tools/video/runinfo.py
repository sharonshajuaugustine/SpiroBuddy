"""Load a recorder run.json and line its logged times up with each video's own clock.
The recorder flashes each page from black to white at a logged time; the first big picture change in the video is that flash.
delta[ctx] = logged time - video time, so video_time = logged_time - delta[ctx].
Command line: python runinfo.py <rec_dir> [sheet.png]  -> prints the offsets and (optionally) a contact sheet of every shot's last frame."""
import json, re, shutil, subprocess, sys, pathlib

FF = shutil.which('ffmpeg')

def flash_time(video):
    r = subprocess.run([FF, '-v', 'info', '-t', '4', '-i', video, '-vf', "select='gt(scene,0.5)',metadata=print", '-an', '-f', 'null', '-'],
                       capture_output=True, text=True)
    m = re.search(r'pts_time:([\d.]+)', r.stderr)
    if not m: raise SystemExit('no sync flash found in ' + video)
    return float(m.group(1))

def load(rec_dir):
    rec = pathlib.Path(rec_dir); run = json.load(open(rec / 'run.json', encoding='utf-8'))
    run['delta'] = {c: round(run['sync'][c] - flash_time(v), 3) for c, v in run['videos'].items()}
    run['M'] = {m['scene']: m for m in run['marks']}
    return run

def vt(run, ctx, t): return t - run['delta'][ctx]

if __name__ == '__main__':
    run = load(sys.argv[1]); print('delta', run['delta'])
    for m in run['marks']: print(f"{m['scene']:14s} {m['ctx']:5s} a={m['a']:7.2f} b={m['b']:7.2f} len={m['b'] - m['a']:5.2f} {'OK' if m['ok'] else 'FAILED'}")
    if len(sys.argv) > 2:
        here = pathlib.Path(__file__).parent
        for kind, cols, cw in (('wide', 3, 640), ('phone', 6, 320)):
            specs = [f"{run['videos'][m['ctx']]}@{vt(run, m['ctx'], m['b']) - 0.2:.2f}:{m['scene']}" for m in run['marks'] if (m['ctx'] == 'pat') == (kind == 'phone')]
            out = sys.argv[2].replace('.png', f'_{kind}.png')
            subprocess.run([sys.executable, str(here / 'sheet.py'), out, str(cols), str(cw)] + specs, check=True)
