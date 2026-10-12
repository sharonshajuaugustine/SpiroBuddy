"""Join the team's recorded voice with the silent video.
Usage: python mux_voice.py <silent.mp4> <voice audio file> <out.mp4> [lead_seconds=0.25]
- finds the first speech (silencedetect), trims everything before it minus a small lead,
- evens out loudness (EBU R128, -16 LUFS), cuts audio to the video length,
- reports duration and size and fails loudly if over 6:00 or 100 MB."""
import re, shutil, subprocess, sys

video, voice, out = sys.argv[1:4]
lead = float(sys.argv[4]) if len(sys.argv) > 4 else 0.25
FF, FP = shutil.which('ffmpeg'), shutil.which('ffprobe')

r = subprocess.run([FF, '-hide_banner', '-i', voice, '-af', 'silencedetect=noise=-35dB:d=0.4', '-f', 'null', '-'],
                   capture_output=True, text=True)
ends = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', r.stderr)]
starts = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', r.stderr)]
first_speech = ends[0] if starts and starts[0] < 0.05 and ends else 0.0
trim = max(first_speech - lead, 0.0)
print(f'first speech at {first_speech:.2f}s in the recording; trimming {trim:.2f}s')

vdur = float(subprocess.run([FP, '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video],
                            capture_output=True, text=True).stdout)
subprocess.run([FF, '-v', 'error', '-y', '-i', video, '-ss', f'{trim:.3f}', '-i', voice,
                '-filter_complex', f'[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=0:{vdur:.3f}[a]',
                '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000',
                '-movflags', '+faststart', '-t', f'{vdur:.3f}', out], check=True)
d = subprocess.run([FP, '-v', 'error', '-show_entries', 'format=duration,size', '-of', 'csv=p=0', out],
                   capture_output=True, text=True).stdout.strip().split(',')
dur, size = float(d[0]), int(d[1])
print(f'OUTPUT {out}: {int(dur // 60)}:{dur % 60:05.2f} long, {size / 1e6:.1f} MB')
assert dur < 360, 'TOO LONG: must be under 6:00'
assert size < 100e6, 'TOO BIG: must be under 100 MB'
print('OK: under 6:00 and under 100 MB')
