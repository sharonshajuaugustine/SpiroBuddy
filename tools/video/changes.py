"""List the moments when a recording's picture changes (frame-difference score), to line up logged event times with video times.
Usage: python changes.py <video> <from_s> <to_s> [threshold=0.004]   -> prints 'video_time score' for frames whose difference from the previous frame exceeds the threshold."""
import subprocess, sys, shutil, re
vid, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); thr = float(sys.argv[4]) if len(sys.argv) > 4 else 0.004
r = subprocess.run([shutil.which('ffmpeg'), '-v', 'info', '-ss', f'{a}', '-t', f'{b - a}', '-i', vid, '-vf',
                    f"select='gt(scene,{thr})',metadata=print", '-an', '-f', 'null', '-'], capture_output=True, text=True)
out = []; cur = None
for line in r.stderr.splitlines():
    m = re.search(r'pts_time:([\d.]+)', line)
    if m: cur = float(m.group(1))
    m = re.search(r'lavfi\.scene_score=([\d.]+)', line)
    if m and cur is not None: out.append((round(a + cur, 2), float(m.group(1))))
print(' '.join(f'{t:.2f}({s:.3f})' for t, s in out))
