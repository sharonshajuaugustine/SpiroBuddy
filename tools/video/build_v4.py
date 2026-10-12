"""Motion-graphics build (v4): card graphics for Part 1, the recorded live run in care order with click rings,
highlight boxes, end-of-shot zoom, a journey bar, the call cropped to the simulated phone with English subtitles,
a status recap, and a teleprompter copy.
Usage: python build_v4.py <work_dir> <rec_dir> <narration_md> <spec_json> <assets_dir> <out_dir> [only=part1|part2|all]"""
import json, re, shutil, subprocess, sys, textwrap, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = pathlib.Path(__file__).parent; sys.path.insert(0, str(HERE))
import runinfo
try: import gfx_v4
except ImportError: gfx_v4 = None            # only Part 1 and the close need the card graphics

WORK, REC, NARR, SPECF, ASSETS, OUTD = (pathlib.Path(a) for a in sys.argv[1:7])
ONLY = sys.argv[7] if len(sys.argv) > 7 else 'all'
G = WORK / 'gfx4'; G.mkdir(parents=True, exist_ok=True)
FF, FP = shutil.which('ffmpeg'), shutil.which('ffprobe')
W, H, FPS = 1920, 1080, 30
NAVY, NAVY2, CARD = (10, 21, 38), (16, 34, 60), (22, 42, 72)
TEAL, TEAL2, WHITE, DIM, AMBER = (18, 140, 160), (64, 196, 214), (255, 255, 255), (150, 170, 195), (246, 170, 40)
FD = 'C:/Windows/Fonts/'
def F(size, w='r'): return ImageFont.truetype(FD + {'r': 'segoeui.ttf', 'b': 'segoeuib.ttf', 's': 'seguisb.ttf', 'l': 'segoeuil.ttf'}[w], size)
ENC = ['-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', str(FPS)]
WIDE = (142, 98, 1636, 920)                     # Part 1 inset (16:9)
DW = (166, 124, 1588, 894)                      # demo inset (16:9), lower to leave a row for the journey bar
PH_H = 874; PH_W = 2 * round(412 * PH_H / 860 / 2); PH_X, PH_Y = 1196, 124
FADE = 0.10

run = runinfo.load(REC)
M, EVS, DELTA, VID, SIZE, INFO = run['M'], run['events'], run['delta'], run['videos'], run['size'], run['info']
SPEC = json.load(open(SPECF, encoding='utf-8'))
FIRST = INFO.get('name', 'Patient').split()[0]
if not INFO.get('missed'):                    # the count spoken in the call is also written on the nurse's card
    mm = re.search(r'missed (\d+) sessions', (INFO.get('alert_text') or '') + (INFO.get('call_screen') or ''))
    INFO['missed'] = int(mm.group(1)) if mm else None
def EV1(name, ctx=None): return next(e for e in EVS if e['name'] == name and (ctx is None or e['ctx'] == ctx))

def ff(args, cwd=G):
    r = subprocess.run([FF, '-v', 'error', '-y'] + [str(a) for a in args], cwd=cwd, capture_output=True, text=True)
    if r.returncode: raise SystemExit('ffmpeg failed: ' + ' '.join(map(str, args))[:900] + '\n' + r.stderr[-1800:])

# ------------------------------------------------------------------ drawing helpers
def tsize(d, text, font):
    b = d.textbbox((0, 0), text, font=font); return b[2] - b[0], b[3] - b[1]
D0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))

def pill(text, font, fill, fg=WHITE, padx=22, pady=10, outline=None, radius=None):
    tw, th = tsize(D0, text, font)
    w, h = tw + 2 * padx, th + 2 * pady + 6
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius or h // 2, fill=fill, outline=outline, width=2 if outline else 0)
    d.text((padx, pady - 2), text, font=font, fill=fg)
    return im

def fit(text, w, size, weight='b', min_size=18):
    while size > min_size and tsize(D0, text, F(size, weight))[0] > w: size -= 2
    return F(size, weight)

def wrap_px(text, font, w):
    out = []
    for para in text.split('\n'):
        cur = ''
        for word in para.split():
            trial = (cur + ' ' + word).strip()
            if tsize(D0, trial, font)[0] <= w or not cur: cur = trial
            else: out.append(cur); cur = word
        out.append(cur)
    return out

def gradient(c2=NAVY2):
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    for y in range(H):
        a = y / H; d.line([(0, y), (W, y)], fill=tuple(int(NAVY[i] * (1 - a) + c2[i] * a) for i in range(3)))
    return im

def journey_row(im, steps, cur):
    d = ImageDraw.Draw(im); f = F(21, 's'); fb = F(21, 'b'); gap = 54
    ws = [tsize(D0, s, fb)[0] + 26 for s in steps]; total = sum(ws) + gap * (len(steps) - 1); x = (W - total) // 2; y = 91
    for i, s in enumerate(steps):
        col = TEAL2 if i < cur else (AMBER if i == cur else (92, 112, 140))
        d.ellipse((x, y + 7, x + 14, y + 21), fill=col if i <= cur else None, outline=col, width=2)
        d.text((x + 24, y), s, font=fb if i == cur else f, fill=WHITE if i == cur else (TEAL2 if i < cur else (120, 138, 164)))
        x += ws[i]
        if i < len(steps) - 1:
            d.line([(x + 8, y + 14), (x + gap - 10, y + 14)], fill=TEAL2 if i < cur else (70, 90, 120), width=2); x += gap

def background(kind='wide', tracker=None, caption=None, tag=None, phone_text=None, part=1, journey=None, step=0,
               phone_size=None, phone_label="Patient's phone"):
    im = gradient(); d = ImageDraw.Draw(im)
    d.line([(0, 84), (W, 84)], fill=(40, 62, 92), width=2)
    if tracker is not None:
        roles = ['Doctor', 'Patient', 'Admin', 'Nurse']; f = F(24, 's')
        pills = [pill(r, f, TEAL if r == tracker else (0, 0, 0, 0), fg=WHITE if r == tracker else DIM,
                      outline=None if r == tracker else (70, 95, 130), padx=18, pady=6) for r in roles]
        total = sum(p.width for p in pills) + 34 * (len(pills) - 1); x = W - 40 - total
        for i, p in enumerate(pills):
            im.paste(p, (x, 20), p); x += p.width
            if i < len(pills) - 1: d.text((x + 9, 22), '›', font=F(28, 'b'), fill=DIM); x += 34
    else:
        t_ = 'Aarogya Saathi  ·  SpiroBuddy'; d.text((W - 40 - tsize(d, t_, F(24, 's'))[0], 26), t_, font=F(24, 's'), fill=DIM)
    if journey: journey_row(im, journey, step)
    if kind == 'wide':
        x, y, w, h = DW if part == 2 else WIDE
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
        ds.rounded_rectangle((x - 6, y - 2, x + w + 6, y + h + 14), radius=18, fill=(0, 0, 0, 150))
        sh = sh.filter(ImageFilter.GaussianBlur(12)); im.paste(sh, (0, 0), sh)
        d.rounded_rectangle((x - 5, y - 5, x + w + 4, y + h + 4), radius=12, fill=(36, 58, 90))
        right = 'Live site  ·  spirobuddy.onrender.com  ·  fictional patients' if part == 2 else 'Dolphin Tank India  ·  Social Impact Hackathon 2026'
        d.text((W - 40 - tsize(d, right, F(21))[0], 1040), right, font=F(21), fill=DIM)
        cx = x
        if tag:
            p = pill(tag, F(22, 'b'), AMBER, fg=(30, 20, 0), padx=14, pady=4, radius=8); im.paste(p, (cx, 1032), p); cx += p.width + 14
        if caption: d.text((cx, 1031), caption, font=fit(caption, W - 40 - tsize(d, right, F(21))[0] - cx - 30, 28, 's'), fill=WHITE)
    elif kind == 'phone':
        pw, ph = phone_size or (PH_W, PH_H); x = PH_X - (pw - PH_W) // 2; y = PH_Y
        d.rounded_rectangle((x - 14, y - 14, x + pw + 14, y + ph + 14), radius=38, fill=(30, 42, 60), outline=(70, 92, 124), width=3)
        d.text((x + pw // 2 - tsize(d, phone_label, F(21, 's'))[0] // 2, y + ph + 20), phone_label, font=F(21, 's'), fill=DIM)
        title, desc = phone_text; ty = 250
        for line in wrap_px(title, F(56, 'b'), 900):
            d.text((160, ty), line, font=F(56, 'b'), fill=WHITE); ty += 72
        ty += 18
        for line in wrap_px(desc, F(32, 'l'), 900):
            d.text((160, ty), line, font=F(32, 'l'), fill=(205, 218, 235)); ty += 46
        if tag:
            p = pill(tag, F(24, 'b'), AMBER, fg=(30, 20, 0), padx=16, pady=6, radius=10); im.paste(p, (160, ty + 26), p); ty += 26 + p.height
        im.info['text_bottom'] = ty
        d.text((160, 1040), 'Live site  ·  spirobuddy.onrender.com  ·  fictional patients', font=F(21), fill=DIM)
    return im

def chapter_png(text, sub=None):
    f1, f2 = F(25, 'b'), F(25, 's')
    a = pill(text, f1, TEAL, padx=20, pady=8)
    if not sub: return a
    sw, _ = tsize(D0, sub, f2)
    im = Image.new('RGBA', (a.width + 18 + sw + 10, a.height), (0, 0, 0, 0)); im.paste(a, (0, 0), a)
    ImageDraw.Draw(im).text((a.width + 18, 8), sub, font=f2, fill=WHITE)
    return im

def subtitle_png(text, maxw=1400, size=30):
    f = F(size, 's'); lines = [l for para in text.split('\n') for l in wrap_px(para, f, maxw - 48)]
    ws = [tsize(D0, l, f)[0] for l in lines]; w = max(ws) + 48; lh = int(size * 1.5); h = lh * len(lines) + 28
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=14, fill=(0, 0, 0, 215))
    for i, l in enumerate(lines): d.text((24, 12 + lh * i), l, font=f, fill=WHITE)
    return im

def ring_png():
    s = 240; im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((14, 14, s - 14, s - 14), fill=AMBER + (46,), outline=AMBER + (255,), width=16)
    d.ellipse((6, 6, s - 6, s - 6), outline=(255, 255, 255, 190), width=5)
    return im

def box_png(w, h):
    w, h = int(w) + 20, int(h) + 20; im = Image.new('RGBA', (w + 24, h + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 12, w + 11, h + 11), radius=14, outline=AMBER + (150,), width=12)
    im = im.filter(ImageFilter.GaussianBlur(5)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 12, w + 11, h + 11), radius=14, outline=AMBER + (255,), width=5)
    return im

def spot_png(size, box):
    """Dim everything except one box (content pixels)."""
    im = Image.new('RGBA', size, (6, 14, 28, 165)); d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, radius=18, fill=(0, 0, 0, 0)); return im

def save(im, name): im.save(G / name); return name

# ------------------------------------------------------------------ narration timing -> cue times
md = NARR.read_text(encoding='utf-8')
BLOCKS = []
for sec in re.split(r'\n(?=### |## Part 3)', md):
    h = sec.split('\n', 1)[0]; tm = re.search(r'(\d):(\d\d)–(\d):(\d\d)', h)
    body = ' '.join(l[1:].strip() for l in sec.split('\n') if l.startswith('>')).replace('★', '').strip()
    if tm and body:
        BLOCKS.append(dict(a=int(tm.group(1)) * 60 + int(tm.group(2)), b=int(tm.group(3)) * 60 + int(tm.group(4)), text=re.sub(r'\s+', ' ', body), head=h))
def sec(s): m_, s_ = s.split(':'); return int(m_) * 60 + int(s_)
def block_at(t0): return next(b for b in BLOCKS if b['a'] == t0)
def cue(t0, phrase):
    b = block_at(t0); words = b['text'].split(); low = b['text'].lower()
    i = low.find(phrase.lower())
    if i < 0: raise SystemExit(f'cue not found in block {t0}: {phrase!r}')
    n = len(low[:i].split()); return b['a'] + (b['b'] - b['a']) * n / len(words)

# ------------------------------------------------------------------ segment renderers
SEGS = []; IDX = [0]; CLOCK = [0.0, 0]          # ideal seconds so far, frames written so far
def out_name(): IDX[0] += 1; return f'v4_{IDX[0]:03d}.mp4'
def frames_for(dur):
    """Whole frames for this segment, carrying the rounding error forward so the video never drifts from the script's times."""
    CLOCK[0] += dur; n = max(round(CLOCK[0] * FPS) - CLOCK[1], 1); CLOCK[1] += n; return n

def compose(content, dur, bg_name, label=None, anim=True, content_xy=(WIDE[0], WIDE[1]), extras=(), fade=FADE):
    """content: mp4 of exact content size (or None); overlays: bg, content, chapter label, extras=[(png, x, y, t1, t2)]"""
    nfr = frames_for(dur); dur = nfr / FPS
    out = out_name(); inputs = ['-loop', '1', '-t', f'{dur + 0.2:.3f}', '-i', bg_name]; k = 1; last = '0:v'; fc = []
    if content:
        inputs += ['-i', content]
        fc.append(f"[1:v]tpad=stop_mode=clone:stop_duration=1,format=yuva420p,fade=in:st=0:d={fade}:alpha=1,fade=out:st={max(dur - fade, 0):.3f}:d={fade}:alpha=1[c]")
        fc.append(f"[0:v][c]overlay={content_xy[0]}:{content_xy[1]}:shortest=1[v0]"); last = 'v0'; k = 2
    if label:
        inputs += ['-loop', '1', '-t', f'{dur:.3f}', '-i', label]
        xexp = "'if(lt(t,0.4),-w+(w+40)*(1-pow(1-t/0.4,3)),40)'" if anim else '40'
        fc.append(f"[{last}][{k}:v]overlay=x={xexp}:y=18:shortest=1[v{k}]"); last = f'v{k}'; k += 1
    for png, x, y, t1, t2 in extras:
        inputs += ['-loop', '1', '-t', f'{dur + 0.2:.3f}', '-i', png]
        fc.append(f"[{k}:v]format=rgba,fade=in:st={t1:.2f}:d=0.3:alpha=1[e{k}]")
        fc.append(f"[{last}][e{k}]overlay=x={x}:y={y}:enable='between(t,{t1:.2f},{t2:.2f})'[v{k}]"); last = f'v{k}'; k += 1
    if not fc: fc.append('[0:v]null[v0]'); last = 'v0'
    ff(inputs + ['-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-frames:v', nfr] + ENC + [out])
    SEGS.append((out, dur))

def layered(dur, layers, label=None, anim=True, bg='plain_bg.png', slide=30, fade_out=None):
    """layers: [(png full-frame RGBA, t_in)] each fades in and rises into place at its time."""
    nfr = frames_for(dur); dur = nfr / FPS
    out = out_name(); inputs = ['-loop', '1', '-t', f'{dur + 0.2:.3f}', '-i', bg]; fc = []; last = '0:v'; k = 1
    if label:
        inputs += ['-loop', '1', '-t', f'{dur + 0.2:.3f}', '-i', label]
        xexp = "'if(lt(t,0.4),-w+(w+40)*(1-pow(1-t/0.4,3)),40)'" if anim else '40'
        fc.append(f"[{last}][{k}:v]overlay=x={xexp}:y=18:shortest=1[b{k}]"); last = f'b{k}'; k += 1
    for name, t1 in layers:
        t1 = min(max(t1, 0.1), max(dur - 0.6, 0.1))
        inputs += ['-loop', '1', '-t', f'{dur + 0.2:.3f}', '-i', name]
        fc.append(f"[{k}:v]format=rgba,fade=in:st={t1:.2f}:d=0.4:alpha=1[l{k}]")
        fc.append(f"[{last}][l{k}]overlay=x=0:y='if(lt(t,{t1:.2f}+0.4),{slide}*(1-(t-{t1:.2f})/0.4),0)'[b{k}]"); last = f'b{k}'; k += 1
    if fade_out: fc.append(f"[{last}]fade=out:st={dur - fade_out:.2f}:d={fade_out}:color=0x0a1526[fo]"); last = 'fo'
    if not fc: fc.append('[0:v]null[fo]'); last = 'fo'
    ff(inputs + ['-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-frames:v', nfr] + ENC + [out])
    SEGS.append((out, dur))

def kenburns(img_path, dur, size, z1=1.0, z2=1.04):
    out = out_name(); n = int(round(dur * FPS)); w, h = size
    ff(['-i', img_path, '-vf',
        f"scale={w * 2}:{h * 2}:flags=lanczos,zoompan=z='{z1}+({z2}-{z1})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={w}x{h}:fps={FPS},format=yuv420p",
        '-frames:v', n] + ENC + [out])
    return out

def still_zoom(img_path, dur, size, cx, cy, z):
    """Ease-in punch toward (cx,cy) (fractions) up to zoom z, then hold."""
    out = out_name(); n = max(int(round(dur * FPS)), 1); w, h = size; ramp = max(int(n * 0.5), 1)
    e = f"(3*pow(min(on/{ramp},1),2)-2*pow(min(on/{ramp},1),3))"
    ff(['-i', img_path, '-vf',
        f"scale={w * 2}:{h * 2}:flags=lanczos,zoompan=z='1+({z}-1)*{e}':"
        f"x='max(0,min(iw-iw/zoom,{cx}*iw-iw/zoom/2))':y='max(0,min(ih-ih/zoom,{cy}*ih-ih/zoom/2))':d={n}:s={w}x{h}:fps={FPS},format=yuv420p",
        '-frames:v', n] + ENC + [out])
    return out

# ------------------------------------------------------------------ Part 1 graphics
save(gradient(), 'plain_bg.png')
class _Img(dict):                               # any other name resolves to <assets>/<name>.png (e.g. the trust-page crops)
    def __missing__(self, k):
        p = ASSETS / f'{k}.png'
        if not p.exists(): raise SystemExit(f'image asset missing: {p}')
        return p
IMG = _Img({'slide7': ASSETS / 'slide7.png', 'slide8': ASSETS / 'slide8.png', 'arch_device': ASSETS / 'arch_device.png',
            'arch': REC / 'arch.png' if (REC / 'arch.png').exists() else ASSETS / 'arch.png'})

def title_card(g, dur, label):
    bg = gradient((14, 60, 80)); save(bg, 'title_bg.png'); layers = []
    def layer(name, fn, t1):
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(im), im); layers.append((save(im, name), t1))
    layer('t_name.png', lambda d, im: d.text((150, 330), g.get('name', 'Aarogya Saathi'), font=F(118, 'b'), fill=WHITE), 0.1)
    def tagl(d, im):
        d.text((156, 490), g.get('line1', ''), font=fit(g.get('line1', ''), 900, 46, 'l'), fill=(210, 225, 240))
        d.text((156, 550), g.get('line2', ''), font=fit(g.get('line2', ''), 900, 46, 's'), fill=TEAL2)
    layer('t_tag.png', tagl, 0.4)
    def pills(d, im):
        p1 = pill(g.get('pill1', ''), F(28, 's'), TEAL, padx=22, pady=10); im.paste(p1, (156, 660), p1)
        p2 = pill(g.get('pill2', ''), F(28, 's'), (0, 0, 0, 0), outline=(110, 140, 175), padx=22, pady=10); im.paste(p2, (156 + p1.width + 18, 660), p2)
        d.text((158, 760), g.get('team', ''), font=F(30), fill=DIM)
    layer('t_pills.png', pills, 0.7)
    layer('t_foot.png', lambda d, im: d.text((158, 980), g.get('foot', ''), font=F(24), fill=DIM), 0.9)
    # right side: the patient's own screen from this recording (medicines page in Hindi)
    e = EV1('meds_hindi', 'pat'); shot = 'title_phone.png'
    ff(['-ss', f"{e['t'] - DELTA['pat'] + 2.0:.2f}", '-i', VID['pat'], '-frames:v', 1, shot])
    ph = Image.open(G / shot).convert('RGB'); ph = ph.resize((364, round(ph.height * 364 / ph.width)), Image.LANCZOS)
    vis = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dv = ImageDraw.Draw(vis); px, py = 1330, 150
    dv.rounded_rectangle((px - 14, py - 14, px + ph.width + 14, py + ph.height + 14), radius=40, fill=(30, 42, 60, 255), outline=(70, 92, 124, 255), width=3)
    msk = Image.new('L', ph.size, 0); ImageDraw.Draw(msk).rounded_rectangle((0, 0, ph.width - 1, ph.height - 1), radius=26, fill=255)
    vis.paste(ph, (px, py), msk)
    cap = 'Patient app  ·  sample patient  ·  recorded on the live site'; dv.text((px + ph.width // 2 - tsize(D0, cap, F(20))[0] // 2, py + ph.height + 26), cap, font=F(20), fill=DIM + (255,))
    layers.append((save(vis, 't_vis.png'), 0.25))
    layered(dur, layers, bg='title_bg.png', slide=24, fade_out=0.25)

def stat_layers(g, prefix):
    out = []
    head = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(head).text((150, 150), g['head'], font=fit(g['head'], 1600, 60), fill=WHITE)
    out.append((save(head, f'{prefix}_head.png'), None))
    n = len(g['cards']); cw = (1620 - 40 * (n - 1)) // n
    for i, c in enumerate(g['cards']):
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); x = 150 + i * (cw + 40); y = 290
        dd.rounded_rectangle((x, y, x + cw, y + 560), radius=26, fill=CARD + (255,), outline=(52, 82, 120), width=2)
        dd.text((x + 40, y + 44), c['big'], font=fit(c['big'], cw - 80, 104), fill=AMBER if i == n - 1 else TEAL2)
        ty = y + 210
        for line in wrap_px(c['text'], F(36, 's'), cw - 80)[:4]: dd.text((x + 42, ty), line, font=F(36, 's'), fill=WHITE); ty += 48
        sy = y + 560 - 36
        src = wrap_px(c['source'], F(23), cw - 80)[:4]
        for line in reversed(src): sy -= 32; dd.text((x + 42, sy), line, font=F(23), fill=DIM)
        out.append((save(im, f'{prefix}_card{i}.png'), c.get('cue')))
    if g.get('footer'):
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); fy = 884
        for line in wrap_px(g['footer'], F(30, 's'), 1600)[:2]: dd.text((152, fy), line, font=F(30, 's'), fill=(225, 234, 245)); fy += 42
        out.append((save(im, f'{prefix}_foot.png'), g.get('footer_cue')))
    return out

def image_seg(g, dur, label, anim):
    img = IMG[g['img']]; size = (WIDE[2], WIDE[3]); z = g.get('zoom')
    c = still_zoom(str(img), dur, size, *z) if z else kenburns(str(img), dur, size)
    bg = save(background('wide', part=1), f'bg_img_{IDX[0]}.png'); extras = []
    if g.get('tag'):
        p = pill(g['tag'], F(26, 'b'), AMBER, fg=(30, 20, 0), padx=18, pady=8, radius=10); nm = save(p, f'imgtag_{IDX[0]}.png')
        extras.append((nm, WIDE[0] + 26, WIDE[1] + WIDE[3] - p.height - 26, 0.15, dur))
    compose(c, dur, bg, label, anim, (WIDE[0], WIDE[1]), extras)

def graphic_seg(g, dur, t_start, t0, label, anim, prefix):
    """Render one Part 1 graphic for dur seconds. t_start = absolute time it starts; t0 = its block's start (for cues)."""
    rel = lambda ph, dflt: (max(cue(t0, ph) - t_start, 0.1) if ph else dflt)
    kind = g['type']
    if kind == 'title': title_card(g, dur, label)
    elif kind == 'image': image_seg(g, dur, label, anim)
    elif kind == 'stats':
        ls = stat_layers(g, prefix); layered(dur, [(n, rel(c, 0.15 + 0.25 * i)) for i, (n, c) in enumerate(ls)], label, anim)
    else:
        ls = gfx_v4.render_layers(g, str(G), prefix)
        layered(dur, [(l['png'], rel(l.get('cue'), 0.15 + 0.3 * i)) for i, l in enumerate(ls)], label, anim)

def part1():
    for bi, blk in enumerate(SPEC['part1']):
        t0, t1 = sec(blk['start']), sec(blk['end']); gs = blk['graphics']
        starts = [t0] + [cue(t0, g['cue']) if g.get('cue') else None for g in gs[1:]]
        for i in range(1, len(starts)):                       # a graphic without a cue shares the remaining time evenly
            if starts[i] is None: starts[i] = starts[i - 1] + (t1 - starts[i - 1]) / (len(gs) - i + 1)
        if gs[0]['type'] == 'title' and len(gs) > 1: starts[1] = max(starts[1], min(t0 + 4.2, t1 - 1))   # give the title time to be read
        ends = starts[1:] + [t1]
        for i, g in enumerate(gs):
            lab = save(chapter_png(blk['chip']), f'chip_p1_{bi}.png') if blk.get('chip') and g['type'] != 'title' else None
            first_labelled = next((j for j, x in enumerate(gs) if x['type'] != 'title'), 0)
            graphic_seg(g, ends[i] - starts[i], starts[i], t0, lab, i == first_labelled, f'p1_{bi}_{i}')

# ------------------------------------------------------------------ Part 2: the recorded live run
RING = save(ring_png(), 'ring.png')
HOLD = {'s1_module': 1.0, 's3_needs_review': 2.2, 's3_dialog': 1.5, 's5a_login': 1.8, 's7a_device': 3.0, 's8b_request_card': 1.3}
FINAL = {'s9b_nurse': None, 's9a_call': None, 's3_prescribe': None}     # None = no end zoom / end box (the crop or the final screen already shows it)
MID_ONLY = {'s5a_login', 's7a_device', 's10_branding'}                   # their named focus is a mid-shot moment, not the end state
HOLD['s10_branding'] = 2.8

def shot_plan(key):
    """Per-shot cut, crop and layout decisions, all derived from the recorder's log."""
    m = M[key]; ctx = m['ctx']; vw, vh = SIZE[ctx]; o = dict(a=m['a'], b=m['b'], ctx=ctx, crop=(0, 0, vw, vh), phone=ctx.startswith('pat'), phone_size=None)
    if key == 's9a_call':                                   # crop to the simulated phone, from the moment it rings
        e = next(x for x in EVS if x['name'] == 'focus' and x.get('scene') == 's9a_phone')
        o['a'] = EV1('ringing', 'doc')['t'] + 0.35
        top = 46                                            # the page's sticky header covers the first rows of the simulated phone
        x, y, w = e['x'], max(e['y'], top), e['w']; h = min(e['y'] + e['h'], vh) - y
        o['crop'] = (round(x), round(y), 2 * round(w / 2), 2 * round(h / 2)); o['phone'] = True
        o['phone_size'] = (2 * round(PH_H * w / h / 2), PH_H)
    if key == 's7b_breathing':                              # frame the coach itself (the hourly grid below it is not part of this scene)
        o['crop'] = (0, 0, vw, 690); o['phone_size'] = (PH_W, 2 * round(PH_W * 690 / vw / 2))
    if key == 's9b_nurse':                                  # crop to the patient's alert card
        e = next(x for x in EVS if x['name'] == 'focus' and x.get('scene') == 's9b_nurse')
        w = min(vw, e['w'] + 90); h = w * 9 / 16; x = min(max(e['x'] - 45, 0), vw - w); y = min(max(e['y'] + e['h'] / 2 - h * 0.42, 0), vh - h)
        o['crop'] = (round(x), round(y), 2 * round(w / 2), 2 * round(h / 2))
    return o

def shot_seg(sh, out_len, label, anim, scene, extras_fn=None):
    key = sh['key']; o = shot_plan(key); ctx = o['ctx']; d = DELTA[ctx]; phone = o['phone']
    size = (o['phone_size'] or (PH_W, PH_H)) if phone else (DW[2], DW[3])
    cx0, cy0, cw, ch = o['crop']; sx, sy = size[0] / cw, size[1] / ch
    a_cut = o['a'] + 0.05; raw = o['b'] - a_cut - 0.12
    evs = [e for e in EVS if e['ctx'] == ctx and a_cut <= e['t'] <= o['b']]
    final_scene = FINAL.get(key, key)
    fin = next((e for e in reversed(evs) if e['name'] == 'focus' and e.get('scene') == final_scene), None) if final_scene else None
    z = 1.0
    if key in MID_ONLY: fin = None
    if fin and not phone:
        z = min(1.6, min(cw / (fin['w'] + 260), ch / (fin['h'] + 200)))
    zd = min(1.8, out_len * 0.3) if z >= 1.15 else 0
    play = out_len - zd; f = play / raw
    tt = lambda t_: (t_ - a_cut) * f                         # logged time -> time inside this cut
    inputs = ['-ss', f'{a_cut - d:.3f}', '-t', f'{raw:.3f}', '-i', VID[ctx]]
    fc = [f"[0:v]crop={cw}:{ch}:{cx0}:{cy0},setpts={f:.5f}*(PTS-STARTPTS),scale={size[0]}:{size[1]}:flags=lanczos,fps={FPS},format=yuv420p[c0]"]; last = 'c0'; k = 1
    def overlay_png(name, x, y, t1, t2, fade_in=0.15):
        nonlocal last, k
        inputs.extend(['-loop', '1', '-t', f'{play:.3f}', '-i', name])
        fc.append(f"[{k}:v]format=rgba,fade=in:st={t1:.2f}:d={fade_in}:alpha=1[o{k}]")
        fc.append(f"[{last}][o{k}]overlay=x={x}:y={y}:enable='between(t,{t1:.2f},{t2:.2f})':shortest=1[c{k}]"); last = f'c{k}'; k += 1
    if key == 's7a_device':                                 # spotlight on the device panel (the rest of the page is dimmed)
        pe = next((e for e in evs if e['name'] == 'focus' and e.get('scene') == 's7a_panel'), None)
        if pe:
            bx = ((pe['x'] - cx0) * sx - 8, (pe['y'] - cy0) * sy - 8, (pe['x'] + pe['w'] - cx0) * sx + 8, min((pe['y'] + pe['h'] - cy0) * sy + 8, size[1]))
            overlay_png(save(spot_png(size, bx), f'spot_{key}.png'), 0, 0, 0.25, play, 0.4)
    for e in evs:                                           # highlight boxes on the things the narration points at
        if e['name'] != 'focus': continue
        hold = HOLD.get(e.get('scene'))
        if e is fin and zd == 0: hold = o['b'] - e['t']
        if not hold: continue
        bw, bh = e['w'] * sx, e['h'] * sy
        nm = save(box_png(bw, bh), f"box_{key}_{e.get('scene')}.png")
        overlay_png(nm, f"{(e['x'] - cx0) * sx - 22:.0f}", f"{(e['y'] - cy0) * sy - 22:.0f}", max(tt(e['t']), 0.05), min(tt(e['t'] + hold), play))
    for e in evs:                                           # a ring on every click
        if e['name'] != 'click': continue
        x, y = (e['x'] - cx0) * sx, (e['y'] - cy0) * sy
        if not (0 <= x <= size[0] and 0 <= y <= size[1]): continue
        t1 = max(tt(e['t']) - 0.05, 0.0); dur_r = 0.55
        inputs.extend(['-loop', '1', '-t', f'{play:.3f}', '-i', RING])
        grow = f"(64+110*min(max((t-{t1:.2f})/{dur_r},0),1))"
        fc.append(f"[{k}:v]format=rgba,scale=w='2*trunc({grow}/2)':h='2*trunc({grow}/2)':eval=frame,fade=in:st={t1:.2f}:d=0.06:alpha=1,fade=out:st={t1 + 0.33:.2f}:d=0.22:alpha=1[r{k}]")
        fc.append(f"[{last}][r{k}]overlay=x='{x:.0f}-w/2':y='{y:.0f}-h/2':enable='between(t,{t1:.2f},{t1 + dur_r:.2f})':shortest=1[c{k}]"); last = f'c{k}'; k += 1
    cut = out_name()
    ff(inputs + ['-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-t', f'{play:.3f}'] + ENC + [cut])
    parts = [cut]
    if zd:
        still = f'still_{key}.png'; ff(['-sseof', '-0.07', '-i', cut, '-frames:v', 1, still])
        parts.append(still_zoom(still, zd, size, (fin['x'] + fin['w'] / 2 - cx0) / cw, (fin['y'] + fin['h'] / 2 - cy0) / ch, z))
    if len(parts) > 1:
        lst = f'list_{key}.txt'; (G / lst).write_text(''.join(f"file '{p}'\n" for p in parts), encoding='utf-8')
        content = out_name(); ff(['-f', 'concat', '-safe', 0, '-i', lst, '-c', 'copy', content])
    else: content = cut
    jr = SPEC['demo'].get('journey'); step = scene.get('journey_step', 0)
    if phone:
        text = (sh.get('phone_title') or scene['sub'], sh.get('phone_desc') or sh.get('caption') or '')
        lab_ = f"{FIRST}'s phone (simulated)  ·  no real call" if key == 's9a_call' else "Patient's phone"
        bgim = background('phone', tracker=sh['tracker'], tag=sh.get('tag'), phone_text=text, part=2, journey=jr, step=step, phone_size=o['phone_size'], phone_label=lab_)
        bg = save(bgim, f'bg_{key}.png'); xy = (PH_X - (size[0] - PH_W) // 2, PH_Y)
        text_bottom = bgim.info.get('text_bottom', 600)
    else:
        bg = save(background('wide', tracker=sh['tracker'], caption=sh.get('caption'), tag=sh.get('tag'), part=2, journey=jr, step=step), f'bg_{key}.png')
        xy = (DW[0], DW[1]); text_bottom = 0
    extras = extras_fn(dict(tt=tt, play=play, out_len=out_len, xy=xy, size=size, text_bottom=text_bottom)) if extras_fn else []
    compose(content, out_len, bg, label, anim, xy, extras)

def call_extras(c):
    subs = SPEC['demo']['call_subs']; names = ['ai_line_1', 'ai_line_2', 'ai_line_3']; out = []
    ts = [max(c['tt'](EV1(n, 'doc')['t']), 0.1) for n in names] + [c['out_len']]
    for i, s in enumerate(subs[:3]):
        s = s.replace('{missed}', str(INFO.get('missed') or 'several')).replace('Kamala', FIRST)
        p = subtitle_png(s, maxw=940, size=29); nm = save(p, f'sub_call_{i}.png')
        out.append((nm, 160, max(c['text_bottom'] + 40, 600), ts[i], ts[i + 1]))
    return out

def nurse_extras(c):
    s = SPEC['demo'].get('nurse_sub')
    if not s: return []
    p = subtitle_png(s.replace('Kamala', FIRST), maxw=1300, size=30); nm = save(p, 'sub_nurse.png')
    t1 = max(c['tt'](EV1('own_words', 'staff')['t']), 0.2)
    return [(nm, (W - p.width) // 2, c['xy'][1] + c['size'][1] - p.height - 26, t1, c['out_len'])]

def first_extras(c):
    """Shown once: the screens say SpiroBuddy because the prototype runs under its module name."""
    p = pill('The prototype runs under its module name, SpiroBuddy', F(24, 's'), (0, 0, 0, 200), padx=18, pady=8, radius=10); nm = save(p, 'note_name.png')
    return [(nm, c['xy'][0] + c['size'][0] - p.width - 22, c['xy'][1] + c['size'][1] - p.height - 22, 0.4, min(5.0, c['out_len']))]

def part2():
    for si, sc in enumerate(SPEC['demo']['scenes']):
        t0, t1 = sec(sc['start']), sec(sc['end']); shots = sc['shots']
        plans = [shot_plan(s['key']) for s in shots]; raws = [p['b'] - p['a'] - 0.17 for p in plans]
        FIXED = {'s7a_device': 4.0}                         # long enough to read the device panel (it would get ~2 s by share)
        fixed = {i: FIXED[s['key']] for i, s in enumerate(shots) if s['key'] in FIXED and len(shots) > 1}
        scale = (t1 - t0 - sum(fixed.values())) / sum(r for i, r in enumerate(raws) if i not in fixed)
        if any(s['key'] == 's10_branding' for s in shots): sc = dict(sc, journey_step=len(SPEC['demo']['journey']))   # after the journey: every step done
        lab = save(chapter_png(SPEC['demo']['chip'], sc['sub']), f'lab_scene_{si}.png')
        for i, (s, r) in enumerate(zip(shots, raws)):
            fn = call_extras if s['key'] == 's9a_call' else nurse_extras if s['key'] == 's9b_nurse' else first_extras if (si, i) == (0, 0) else None
            shot_seg(s, fixed.get(i, r * scale), lab, i == 0, sc, fn)

# ------------------------------------------------------------------ Part 3: status recap, then the link and team
def outro():
    o = SPEC['outro']; t0, t1 = sec(o['start']), sec(o['end']); dur = t1 - t0
    d2 = min(3.2, dur * 0.25); d1 = dur - d2; TAIL = 2.0      # recap while the close is spoken, then the link and team (held 2 s after the last word)
    g = o['graphics'][0]
    ls = gfx_v4.render_layers(g, str(G), 'outro')
    rel = lambda ph, dflt: (min(max(cue(t0, ph) - t0, 0.1), d1 - 0.8) if ph else dflt)
    layered(d1, [(l['png'], rel(l.get('cue'), 0.15 + 0.35 * i_)) for i_, l in enumerate(ls)], None, False)
    bg = gradient((14, 60, 80)); save(bg, 'outro_bg.png'); layers = []
    def L(name, fn, t_):
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(ImageDraw.Draw(im), im); layers.append((save(im, name), t_))
    L('o1.png', lambda d, im: (d.text((150, 250), 'See it on the live site', font=F(44, 's'), fill=DIM), d.text((150, 312), o.get('link', 'spirobuddy.onrender.com'), font=F(96, 'b'), fill=WHITE)), 0.1)
    def statuses(d, im):
        x = 152
        for t_, c_ in (('Live', (34, 160, 90)), ('Simulated', AMBER), ('In development', (120, 140, 220)), ('Planned', (110, 120, 140))):
            p = pill(t_, F(26, 's'), c_, fg=WHITE if t_ != 'Simulated' else (30, 20, 0), padx=18, pady=6); im.paste(p, (x, 480), p); x += p.width + 14
        d.text((152, 548), 'Every feature on our status list carries one of these labels.', font=F(30), fill=(205, 218, 235))
        d.text((152, 596), 'Fictional patients only  ·  Device not built yet', font=F(30), fill=(205, 218, 235))
    L('o2.png', statuses, 0.5)
    team = o.get('team', 'Team GuGu GaGa'); head, _, rest = team.partition('·')
    L('o3.png', lambda d, im: (d.text((150, 730), head.strip(), font=F(56, 'b'), fill=TEAL2), d.text((152, 815), rest.strip(), font=F(40, 's'), fill=WHITE)), 0.9)
    L('o4.png', lambda d, im: d.text((152, 985), 'Aarogya Saathi, with the SpiroBuddy breathing coach  ·  Dolphin Tank India Social Impact Hackathon 2026', font=F(24), fill=DIM), 1.2)
    layered(d2 + TAIL, layers, bg='outro_bg.png', slide=24)

# ================================================================== THE TIMELINE
if ONLY in ('all', 'part1'): part1()
if ONLY in ('all', 'part2'): part2()
if ONLY == 'all': outro()

(G / 'list_all.txt').write_text(''.join(f"file '{f}'\n" for f, _ in SEGS), encoding='utf-8')
OUTD.mkdir(parents=True, exist_ok=True)
suffix = '' if ONLY == 'all' else f'_{ONLY}'
clean = OUTD / f'Aarogya_Saathi_video_SILENT{suffix}.mp4'
ff(['-f', 'concat', '-safe', 0, '-i', 'list_all.txt', '-c', 'copy', '-movflags', '+faststart', clean])
print('segments', len(SEGS), 'planned total', round(sum(d for _, d in SEGS), 2))
json.dump([dict(file=f, dur=round(d, 3)) for f, d in SEGS], open(G / 'segments.json', 'w'), indent=1)

if ONLY == 'all':
    draws = ["drawtext=fontfile=fb.ttf:text='%{pts\\:hms}':fontsize=40:fontcolor=yellow:box=1:boxcolor=black@0.8:boxborderw=12:x=40:y=100",
             "drawtext=fontfile=fb.ttf:text='TELEPROMPTER COPY - do not upload':fontsize=30:fontcolor=white:box=1:boxcolor=0xb00020@0.9:boxborderw=12:x=w-text_w-40:y=100"]
    shutil.copy(FD + 'segoeuib.ttf', G / 'fb.ttf'); n = 0
    for b in BLOCKS:
        sents = re.split(r'(?<=[.!?;:])\s+', b['text']); chunks, cur = [], ''
        for s_ in sents:
            if len(cur) + len(s_) > 140 and cur: chunks.append(cur); cur = s_
            else: cur = (cur + ' ' + s_).strip()
        if cur: chunks.append(cur)
        words = [len(c.split()) for c in chunks]; tot = sum(words); t = b['a']
        for c, w in zip(chunks, words):
            dd = (b['b'] - b['a']) * w / tot
            (G / f'tp{n}.txt').write_text('\n'.join(textwrap.wrap(c, 60)), encoding='utf-8')
            draws.append(f"drawtext=fontfile=fb.ttf:textfile=tp{n}.txt:fontsize=40:line_spacing=10:fontcolor=white:box=1:"
                         f"boxcolor=black@0.88:boxborderw=22:x=(w-text_w)/2:y=h-text_h-90:enable='between(t,{t:.2f},{t + dd:.2f})'"); n += 1; t += dd
    (G / 'tp_filter.txt').write_text(','.join(draws), encoding='utf-8')
    tele = OUTD / 'Aarogya_Saathi_video_TELEPROMPTER.mp4'
    ff(['-i', clean, '-/vf', 'tp_filter.txt'] + ENC + ['-movflags', '+faststart', tele])
for pth in ([clean] + ([tele] if ONLY == 'all' else [])):
    r = subprocess.run([FP, '-v', 'error', '-show_entries', 'format=duration,size', '-of', 'csv=p=0', str(pth)], capture_output=True, text=True)
    print(pth.name, r.stdout.strip())
