"""Contact sheet of frames from a recording. Usage: python sheet.py <out.png> <cols> <cell_w> <video>@<t>[:label] ...
Each frame is drawn with its label; frames keep their aspect ratio inside a cell of width cell_w."""
import subprocess, sys, shutil, pathlib, tempfile
from PIL import Image, ImageDraw, ImageFont
out, cols, cw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
FF = shutil.which('ffmpeg'); tmp = pathlib.Path(tempfile.mkdtemp()); cells = []
for i, spec in enumerate(sys.argv[4:]):
    vid, rest = spec.rsplit('@', 1); ts, _, label = rest.partition(':')
    f = tmp / f'f{i}.png'
    subprocess.run([FF, '-v', 'error', '-y', '-ss', ts, '-i', vid, '-frames:v', '1', str(f)], check=True)
    im = Image.open(f).convert('RGB'); im = im.resize((cw, round(im.height * cw / im.width)), Image.LANCZOS)
    d = ImageDraw.Draw(im); txt = f'{label or ""} @{ts}s'
    d.rectangle((0, 0, 12 + 11 * len(txt), 30), fill=(0, 0, 0)); d.text((6, 4), txt, font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 20), fill=(255, 230, 0))
    cells.append(im)
ch = max(c.height for c in cells); rows = -(-len(cells) // cols)
sheet = Image.new('RGB', (cols * cw, rows * ch), (20, 20, 20))
for i, c in enumerate(cells): sheet.paste(c, ((i % cols) * cw, (i // cols) * ch))
sheet.save(out); print(out, sheet.size)
