"""Part 1 card graphics for the version 4 video.

Draws the 'cards' and 'strip' graphics of spec.json as full-frame 1920x1080 RGBA layers with a
transparent background. The build script supplies the navy gradient and fades each layer in.

API
    render_layers(g, out_dir, prefix) -> [{'png': name, 'cue': phrase or None, 'kind': 'head'|'card'|'footer'}, ...]
    preview(g, out_dir, prefix)       -> path of out_dir/preview_<prefix>.png (all layers over the gradient)
    INFO[prefix]                      -> layout facts of the last render (scale, card box, problems)

Command line
    python gfx_v4.py <spec.json> <out_dir>            every cards/strip graphic in part1 and outro
    python gfx_v4.py --stress <out_dir>               the built-in stress test
    python gfx_v4.py <spec.json> <out_dir> --stress   both

Nothing here depends on exact strings: every text is wrapped by pixel width, and the whole card
content shrinks a step at a time until it fits the safe area. Does not import build_v3/build_v4."""
import json, math, pathlib, sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

# ------------------------------------------------------------------ constants copied from build_v3
W, H = 1920, 1080
NAVY, NAVY2, CARD = (10, 21, 38), (16, 34, 60), (22, 42, 72)
TEAL, TEAL2, WHITE, DIM, AMBER = (18, 140, 160), (64, 196, 214), (255, 255, 255), (150, 170, 195), (246, 170, 40)
FD = 'C:/Windows/Fonts/'
_FONTS = {}
def F(size, w='r'):
    key = (int(size), w)
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(FD + {'r': 'segoeui.ttf', 'b': 'segoeuib.ttf', 's': 'seguisb.ttf', 'l': 'segoeuil.ttf'}[w], int(size))
    return _FONTS[key]

D0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
def tsize(d, text, font):
    b = d.textbbox((0, 0), text, font=font); return b[2] - b[0], b[3] - b[1]

def pill(text, font, fill, fg=WHITE, padx=22, pady=10, outline=None, radius=None):
    tw_, th = tsize(D0, text, font)
    w, h = tw_ + 2 * padx, th + 2 * pady + 6
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius or h // 2, fill=fill, outline=outline, width=2 if outline else 0)
    d.text((padx, pady - 2), text, font=font, fill=fg)
    return im

# ------------------------------------------------------------------ layout constants
SX0, SY0, SX1, SY1 = 110, 150, 1810, 1000        # safe area
SAFE_W = SX1 - SX0
ACCENTS = {'teal': (64, 196, 214), 'amber': (246, 170, 40), 'green': (60, 190, 120), 'violet': (140, 150, 235), 'grey': (150, 170, 195)}
SOFT = (176, 194, 217)      # soft blue-grey: sub line and footer
SOFTW = (226, 234, 245)     # soft white: card lines
EDGE = (52, 82, 120)        # card outline
TAG_FG = (30, 20, 0)
GAP_COL = 36                # gap between cards
GAP_HEAD = 34               # heading block -> cards
GAP_FOOT = 30               # cards -> footer
RADIUS = 26
SS = 2                      # supersampling for shapes (Pillow shapes are not anti-aliased)
SHADOW_M = 44               # room around a card for its soft shadow
MERGE_CONTINUATIONS = True  # a card line that only continues the line before it is drawn as the same bullet
# (scale, air): tried in order until the tallest card fits. air = extra breathing room between lines.
LEVELS = [(1.0, 1.0), (1.0, 0.5), (1.0, 0.0)] + [(round(1 - 0.04 * k, 2), 0.0) for k in range(1, 16)]
INFO = {}

# ------------------------------------------------------------------ text helpers
def tw(text, font): return font.getlength(text)

def wrap_px(text, font, w):
    """Greedy wrap by pixel width. Honours '\\n'. A single word wider than w is broken by characters."""
    out = []
    for para in str(text).split('\n'):
        cur = ''
        for word in para.split():
            trial = (cur + ' ' + word).strip()
            if tw(trial, font) <= w: cur = trial; continue
            if cur: out.append(cur)
            while tw(word, font) > w and len(word) > 1:
                k = len(word) - 1
                while k > 1 and tw(word[:k], font) > w: k -= 1
                out.append(word[:k]); word = word[k:]
            cur = word
        if cur or not out: out.append(cur)
    return out

def wrap_balanced(text, font, w):
    """Same number of lines as wrap_px, but with lines of similar length (no lonely last word)."""
    base = wrap_px(text, font, w)
    if len(base) < 2 or '\n' in str(text): return base
    lo, hi, best = int(max(tw(x, font) for x in str(text).split()) or 1), int(w), base
    while lo < hi:
        mid = (lo + hi) // 2; trial = wrap_px(text, font, mid)
        if len(trial) <= len(base): best, hi = trial, mid
        else: lo = mid + 1
    return best

def text_on(layer, x, y, text, font, fill):
    """Draw text with correct straight-alpha edges on a transparent or filled RGBA layer (origin = top-left of the line box)."""
    if not text: return
    bb = font.getbbox(text); w, h = bb[2] - bb[0] + 4, bb[3] - bb[1] + 4
    if w <= 4 or h <= 4: return
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).text((2 - bb[0], 2 - bb[1]), text, font=font, fill=255)
    tile = Image.new('RGBA', (w, h), tuple(fill[:3]) + (255,)); tile.putalpha(m)
    put(layer, tile, int(round(x + bb[0] - 2)), int(round(y + bb[1] - 2)))

def put(layer, im, x, y):
    """alpha-composite im on layer at (x, y), clipped to the frame."""
    x0, y0 = max(x, 0), max(y, 0); x1, y1 = min(x + im.width, layer.width), min(y + im.height, layer.height)
    if x1 <= x0 or y1 <= y0: return
    if (x0, y0, x1, y1) != (x, y, x + im.width, y + im.height): im = im.crop((x0 - x, y0 - y, x1 - x, y1 - y))
    layer.alpha_composite(im, (x0, y0))

class Block:
    """Wrapped lines in one font. y passed to draw() is the top of the capitals of the first line;
    h runs from there to just under the descenders of the last line."""
    def __init__(self, text, size, weight, width, lh=1.28, balance=False, desc=0.22, nowrap=False):
        self.size = int(size); self.font = F(size, weight)
        self.lines = [str(text)] if nowrap else (wrap_balanced if balance else wrap_px)(text, self.font, width)
        b = self.font.getbbox('H'); self.off = b[1]; self.cap = b[3] - b[1]
        self.pitch = int(round(self.size * lh)); self.desc = int(round(self.size * desc))
        self.h = (len(self.lines) - 1) * self.pitch + self.cap + self.desc
        self.w = max(tw(l, self.font) for l in self.lines)
    def draw(self, layer, x, y, fill):
        for i, l in enumerate(self.lines): text_on(layer, x, y - self.off + i * self.pitch, l, self.font, fill)

def merge_lines(lines):
    """Join a line to the one before it when it is clearly the same sentence (the one before ends with a
    comma or semicolon, or this one starts with a small letter and the one before has no end mark)."""
    out = []
    for raw in lines or []:
        s = str(raw).strip()
        if not s: continue
        if MERGE_CONTINUATIONS and out:
            prev = out[-1]
            if prev.endswith((',', ';')) or (s[0].islower() and not prev.endswith(('.', '!', '?', ':'))):
                out[-1] = prev + ' ' + s; continue
        out.append(s)
    return out

# ------------------------------------------------------------------ shape helpers (drawn at SS x, then scaled down)
def _rr_points(x0, y0, x1, y1, r, step=1.5):
    """Points along a rounded rectangle, clockwise from the left end of the top-left corner."""
    pts = []
    def arc(cx, cy, a0, a1):
        n = max(int(abs(a1 - a0) * r / step), 2)
        for i in range(n + 1):
            a = a0 + (a1 - a0) * i / n; pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    def seg(ax, ay, bx, by):
        n = max(int(math.hypot(bx - ax, by - ay) / step), 1)
        for i in range(1, n): pts.append((ax + (bx - ax) * i / n, ay + (by - ay) * i / n))
    arc(x0 + r, y0 + r, math.pi, 1.5 * math.pi); seg(x0 + r, y0, x1 - r, y0)
    arc(x1 - r, y0 + r, 1.5 * math.pi, 2 * math.pi); seg(x1, y0 + r, x1, y1 - r)
    arc(x1 - r, y1 - r, 0, 0.5 * math.pi); seg(x1 - r, y1, x0 + r, y1)
    arc(x0 + r, y1 - r, 0.5 * math.pi, math.pi); seg(x0, y1 - r, x0, y0 + r)
    return pts

def _dashed(d, pts, fill, width, dash, gap):
    """Dashes with round ends along a closed path; the dash count is rounded so the pattern closes cleanly."""
    pts = pts + [pts[0]]; cum = [0.0]
    for a, b in zip(pts, pts[1:]): cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    total = cum[-1]; n = max(int(round(total / (dash + gap))), 1); period = total / n; dl = period * dash / (dash + gap)
    def at(i, s):
        span = cum[i + 1] - cum[i]; t = (s - cum[i]) / span if span else 0
        return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t)
    j = 0; r = width / 2
    for k in range(n):
        s0 = k * period; s1 = s0 + dl
        while j + 1 < len(cum) - 1 and cum[j + 1] < s0: j += 1
        i = j; seg = [at(i, s0)]
        while i + 1 < len(cum) - 1 and cum[i + 1] < s1: i += 1; seg.append(pts[i])
        seg.append(at(i, s1))
        d.line(seg, fill=fill, width=int(width), joint='curve')
        for p in (seg[0], seg[-1]): d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=fill)

_SHAPES = {}
def card_shape(cw, ch, accent, style, radius=RADIUS):
    """A card body with its soft shadow. Returns an RGBA image with SHADOW_M px of room on every side."""
    key = (cw, ch, accent, style, radius)
    if key in _SHAPES: return _SHAPES[key]
    M = SHADOW_M; w, h = cw + 2 * M, ch + 2 * M
    big = Image.new('RGBA', (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    box = (M * SS, M * SS, (M + cw) * SS - 1, (M + ch) * SS - 1)
    if style == 'dashed':
        d.rounded_rectangle(box, radius=radius * SS, fill=CARD + (165,))
        ins = 1.5 * SS
        pts = _rr_points(box[0] + ins, box[1] + ins, box[2] - ins, box[3] - ins, radius * SS - ins)
        _dashed(d, pts, accent + (255,), 3 * SS, 16 * SS, 11 * SS)
        out = big.resize((w, h), Image.LANCZOS)
    else:
        d.rounded_rectangle(box, radius=radius * SS, fill=CARD + (255,), outline=EDGE + (255,), width=2 * SS)
        mask = Image.new('L', big.size, 0); ImageDraw.Draw(mask).rounded_rectangle(box, radius=radius * SS, fill=255)
        band = Image.new('L', big.size, 0); ImageDraw.Draw(band).rectangle((box[0], box[1], box[2], box[1] + 6 * SS - 1), fill=255)
        big.paste(Image.new('RGBA', big.size, accent + (255,)), (0, 0), ImageChops.multiply(mask, band))   # accent strip along the top edge
        body = big.resize((w, h), Image.LANCZOS)
        sh = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((M + 4, M + 14, M + cw - 5, M + ch + 7), radius=radius, fill=(0, 0, 0, 105))
        out = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(13)), body)
    _SHAPES[key] = out
    return out

def tag_pill(text, max_w, size):
    """Small amber label. One line when it fits (the font may drop a few px); otherwise wrapped inside the pill."""
    size = int(size); padx, pady = int(round(size * 0.66)), int(round(size * 0.42)); lines = None
    for s in range(size, max(size - 4, 12) - 1, -1):
        f = F(s, 'b')
        if tw(text, f) + 2 * padx <= max_w: lines = [text]; break
    if lines is None: f = F(max(size - 2, 12), 'b'); lines = wrap_balanced(text, f, max_w - 2 * padx)
    b = f.getbbox('H'); off, cap = b[1], b[3] - b[1]; pitch = int(round(f.size * 1.24))
    w = int(math.ceil(max(tw(l, f) for l in lines))) + 2 * padx; h = (len(lines) - 1) * pitch + cap + 2 * pady
    big = Image.new('RGBA', (w * SS, h * SS), (0, 0, 0, 0))
    ImageDraw.Draw(big).rounded_rectangle((0, 0, w * SS - 1, h * SS - 1), radius=min(10, h // 2) * SS, fill=AMBER + (255,))
    im = big.resize((w, h), Image.LANCZOS)
    for i, l in enumerate(lines): text_on(im, padx, pady - off + i * pitch, l, f, TAG_FG)
    return im

def number_circle(n, dia, fill=TEAL, fg=WHITE):
    big = Image.new('RGBA', (dia * 4, dia * 4), (0, 0, 0, 0))
    ImageDraw.Draw(big).ellipse((0, 0, dia * 4 - 1, dia * 4 - 1), fill=fill + (255,))
    im = big.resize((dia, dia), Image.LANCZOS); f = F(int(dia * 0.52), 'b'); s = str(n); bb = f.getbbox(s)
    text_on(im, dia / 2 - (bb[0] + bb[2]) / 2, dia / 2 - (bb[1] + bb[3]) / 2, s, f, fg)
    return im

def arrow(length, col=TEAL2, th=4, head=12):
    k = 4; w, h = int(length), head * 2 + 4
    big = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0)); d = ImageDraw.Draw(big); cy = h * k // 2
    d.line([(th * k // 2, cy), ((w - head) * k, cy)], fill=col + (255,), width=th * k)
    d.ellipse((0, cy - th * k // 2, th * k, cy + th * k // 2), fill=col + (255,))
    d.polygon([(w * k - 1, cy), ((w - head * 1.35) * k, cy - head * k), ((w - head * 1.35) * k, cy + head * k)], fill=col + (255,))
    return big.resize((w, h), Image.LANCZOS)

# ------------------------------------------------------------------ heading and footer
def _head(g):
    """Heading (58 px bold, drops to 44 before it wraps) plus the optional sub line. Returns (ops, bottom y)."""
    ops = []; y = SY0 + 2
    head = str(g.get('head') or '').strip(); sub = str(g.get('sub') or '').strip()
    if head:
        b = next((Block(head, s, 'b', SAFE_W, 1.16, nowrap=True) for s in range(58, 43, -2) if tw(head, F(s, 'b')) <= SAFE_W), None)
        if b is None: b = Block(head, 46, 'b', SAFE_W, 1.16, balance=True)
        ops.append((b, SX0, y, WHITE)); y += b.h
    if sub:
        if head: y += 14
        b = Block(sub, 30, 'r', SAFE_W, 1.3); ops.append((b, SX0, y, SOFT)); y += b.h
    return ops, y

def _foot(text):
    text = str(text or '').strip()
    return Block(text, 26, 'r', SAFE_W, 1.34) if text else None

def _blank(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def _save(im, out_dir, name): im.save(pathlib.Path(out_dir) / name); return name

# ------------------------------------------------------------------ cards
def _card_style(n, scale, air):
    S = lambda v, lo=0: max(int(round(v * scale)), lo)
    title, line, pad = (40, 30, 40) if n <= 2 else ((38, 30, 36) if n == 3 else (36, 28, 30))
    return dict(pad=S(pad, 16), top=S(pad, 16) + 6, kicker=S(24, 13), big=S(100, 34), title=S(title, 18), line=S(line, 15), tag=S(21, 13),
                g_kicker=S(15, 6) + round(3 * air), g_big=S(16, 6) + round(4 * air), g_title=S(24, 8) + round(10 * air),
                g_item=S(13, 5) + round(9 * air), g_tag=S(26, 10))

def _card_layout(c, cw, st):
    """Place one card's content. Returns the draw ops (y relative to the card top), the tag image and the height needed."""
    acc = ACCENTS.get(c.get('accent'), ACCENTS['teal']); pad = st['pad']; iw = cw - 2 * pad
    ops, bullets = [], []; y = st['top']; gap = 0
    kicker = str(c.get('kicker') or '').strip(); big = str(c.get('big') or '').strip(); title = str(c.get('title') or '').strip()
    if kicker:
        b = Block(kicker.upper(), st['kicker'], 'b', iw, 1.26, desc=0.08); ops.append((b, 0, y, acc)); gap = st['g_kicker']; y += b.h + gap
    if big:
        size = st['big']
        while size > 30 and tw(big, F(size, 'b')) > iw: size -= 2
        b = Block(big, size, 'b', iw, 1.0, desc=0.06, nowrap=tw(big, F(size, 'b')) <= iw)
        ops.append((b, -round(size * 0.035), y, acc)); gap = st['g_big']; y += b.h + gap      # nudge left: big glyphs carry side bearing
    if title:
        b = Block(title, st['title'], 's', iw, 1.2, balance=True); ops.append((b, 0, y, WHITE)); gap = st['g_title']; y += b.h + gap
    indent = int(round(st['line'] * 0.86))
    for item in merge_lines(c.get('lines')):
        b = Block(item, st['line'], 'r', iw - indent, 1.3); ops.append((b, indent, y, SOFTW)); bullets.append((y, b)); gap = st['g_item']; y += b.h + gap
    content_bottom = y - gap
    tag = tag_pill(str(c['tag']).strip(), iw, st['tag']) if str(c.get('tag') or '').strip() else None
    need = content_bottom + (st['g_tag'] + tag.height if tag else 0) + pad
    return dict(ops=ops, bullets=bullets, tag=tag, need=need, acc=acc, pad=pad, iw=iw)

def _draw_card(layer, c, lay, x, y, cw, ch):
    put(layer, card_shape(cw, ch, lay['acc'], 'dashed' if c.get('style') == 'dashed' else 'solid'), x - SHADOW_M, y - SHADOW_M)
    tx = x + lay['pad']
    for b, dx, ry, fill in lay['ops']: b.draw(layer, tx + dx, y + ry, fill)
    for ry, b in lay['bullets']: text_on(layer, tx, y + ry - b.off, '\u2022', b.font, lay['acc'])
    if lay['tag']: put(layer, lay['tag'], tx, y + ch - lay['pad'] - lay['tag'].height)

def _render_cards(g, out_dir, prefix):
    cards = list(g.get('cards') or []); n = max(len(cards), 1)
    head_ops, head_bottom = _head(g); foot = _foot(g.get('footer'))
    top = head_bottom + GAP_HEAD if head_ops else SY0
    bottom = SY1 - foot.h - GAP_FOOT if foot else SY1
    avail = bottom - top; cw = (SAFE_W - GAP_COL * (n - 1)) // n
    for scale, air in LEVELS:
        st = _card_style(n, scale, air); lays = [_card_layout(c, cw, st) for c in cards]
        need = max([l['need'] for l in lays] or [0])
        if need <= avail: break
    fits = need <= avail
    ch = min(max(need, int(avail * 0.60)), avail) if fits else need
    y = top + int((avail - ch) * 0.36) if fits else top
    layers = []
    im = _blank()
    for b, x, yy, fill in head_ops: b.draw(im, x, yy, fill)
    layers.append({'png': _save(im, out_dir, f'{prefix}_g_head.png'), 'cue': None, 'kind': 'head'})
    for i, (c, lay) in enumerate(zip(cards, lays)):
        im = _blank(); x = SX0 + i * (cw + GAP_COL) + ((SAFE_W - (cw * n + GAP_COL * (n - 1))) if i == n - 1 and False else 0)
        _draw_card(im, c, lay, x, y, cw, ch)
        layers.append({'png': _save(im, out_dir, f'{prefix}_g_c{i}.png'), 'cue': c.get('cue') or None, 'kind': 'card'})
    if foot:
        im = _blank(); foot.draw(im, SX0, SY1 - foot.h, SOFT)
        layers.append({'png': _save(im, out_dir, f'{prefix}_g_foot.png'), 'cue': g.get('footer_cue') or None, 'kind': 'footer'})
    INFO[prefix] = dict(type='cards', n=len(cards), scale=scale, air=air, box=(cw, ch), y=y, fits=fits, need=need, avail=avail,
                        fonts=dict(title=st['title'], line=st['line'], kicker=st['kicker']))
    return layers

# ------------------------------------------------------------------ strip
def _strip_style(n, scale):
    S = lambda v, lo=0: max(int(round(v * scale)), lo)
    title, text, pad = (34, 26, 26) if n >= 5 else ((36, 27, 30) if n == 4 else (38, 28, 34))
    return dict(pad=S(pad, 14), top=S(pad, 14) + 6, title=S(title, 18), text=S(text, 15), circle=S(58, 34), g_circle=S(24, 10), g_title=S(16, 6))

def _strip_layout(steps, bw, st):
    iw = bw - 2 * st['pad']; titles = [str(s.get('title') or '').strip() for s in steps]
    size = next((s for s in range(st['title'], max(st['title'] - 8, 16) - 1, -2) if all(tw(t, F(s, 's')) <= iw for t in titles)), None)
    wrap_title = size is None
    if wrap_title: size = max(st['title'] - 4, 16)
    lays = []
    for s, t in zip(steps, titles):
        y = st['top']; ops = []; cy = y; y += st['circle'] + st['g_circle']
        if t:
            b = Block(t, size, 's', iw, 1.2, balance=True, nowrap=not wrap_title); ops.append((b, y, WHITE)); y += b.h + st['g_title']
        txt = str(s.get('text') or '').strip()
        if txt:
            b = Block(txt, st['text'], 'r', iw, 1.32); ops.append((b, y, SOFTW)); y += b.h + st['g_title']
        lays.append(dict(ops=ops, circle_y=cy, need=y - st['g_title'] + st['pad']))
    return lays, size

def _render_strip(g, out_dir, prefix):
    steps = list(g.get('steps') or []); n = max(len(steps), 1)
    head_ops, head_bottom = _head(g); foot = _foot(g.get('footer'))
    top = head_bottom + GAP_HEAD + 6 if head_ops else SY0
    gap = 60 if n >= 5 else 68; bw = (SAFE_W - gap * (n - 1)) // n
    foot_gap = 44; foot_h = foot.h + foot_gap if foot else 0
    avail = SY1 - top - foot_h
    for scale in [1.0] + [round(1 - 0.04 * k, 2) for k in range(1, 16)]:
        st = _strip_style(n, scale); lays, tsize_ = _strip_layout(steps, bw, st)
        need = max([l['need'] for l in lays] or [0])
        if need <= avail: break
    fits = need <= avail
    bh = min(max(need, int(avail * 0.44)), avail) if fits else need
    y = top + int((avail - bh) * 0.30) if fits else top
    layers = []
    im = _blank()
    for b, x, yy, fill in head_ops: b.draw(im, x, yy, fill)
    layers.append({'png': _save(im, out_dir, f'{prefix}_g_head.png'), 'cue': None, 'kind': 'head'})
    arr = arrow(gap - 20) if n > 1 else None
    for i, (s, lay) in enumerate(zip(steps, lays)):
        im = _blank(); x = SX0 + i * (bw + gap)
        if i and arr: put(im, arr, x - gap + 10, y + bh // 2 - arr.height // 2)            # the arrow that leads into this step
        put(im, card_shape(bw, bh, ACCENTS['teal'], 'solid', 22), x - SHADOW_M, y - SHADOW_M)
        put(im, number_circle(i + 1, st['circle']), x + st['pad'], y + lay['circle_y'])
        for b, ry, fill in lay['ops']: b.draw(im, x + st['pad'], y + ry, fill)
        layers.append({'png': _save(im, out_dir, f'{prefix}_g_c{i}.png'), 'cue': s.get('cue') or None, 'kind': 'card'})
    if foot:
        im = _blank(); foot.draw(im, SX0, y + bh + foot_gap, SOFT)                          # the footer sits under the row
        layers.append({'png': _save(im, out_dir, f'{prefix}_g_foot.png'), 'cue': g.get('footer_cue') or None, 'kind': 'footer'})
    INFO[prefix] = dict(type='strip', n=len(steps), scale=scale, air=0.0, box=(bw, bh), y=y, fits=fits, need=need, avail=avail,
                        fonts=dict(title=tsize_, line=st['text'], kicker=0))
    return layers

# ------------------------------------------------------------------ public API
def render_layers(g, out_dir, prefix):
    """Draw ONE graphic of type 'cards' or 'strip' as full-frame 1920x1080 RGBA PNG layers with a transparent
    background (the build script supplies the navy gradient background and fades each layer in). Return the
    layers in order of appearance as a list of dicts: {'png': file name inside out_dir, 'cue': the PHRASE or
    None, 'kind': 'head' | 'card' | 'footer'}. One 'head' layer (heading plus sub line), one layer per card or
    step, and one 'footer' layer when the graphic has a footer."""
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    kind = g.get('type')
    if kind == 'strip': return _render_strip(g, out_dir, prefix)
    if kind == 'cards': return _render_cards(g, out_dir, prefix)
    raise ValueError(f"gfx_v4 draws only 'cards' and 'strip' graphics, not {kind!r}")

def gradient():
    """The same background as build_v3 background(): vertical navy gradient, the top-band line and the brand text."""
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    for y in range(H):
        a = y / H; d.line([(0, y), (W, y)], fill=tuple(int(NAVY[i] * (1 - a) + NAVY2[i] * a) for i in range(3)))
    d.line([(0, 84), (W, 84)], fill=(40, 62, 92), width=2)
    t = 'Aarogya Saathi  \u00b7  SpiroBuddy'; d.text((W - 40 - tsize(d, t, F(24, 's'))[0], 26), t, font=F(24, 's'), fill=DIM)
    return im

def preview(g, out_dir, prefix, chip=None, guides=False):
    """Composite all layers of one graphic over the navy gradient into out_dir/preview_<prefix>.png and return that path.
    chip = optional chapter chip text drawn where the build script puts it; guides = draw the safe area."""
    layers = render_layers(g, out_dir, prefix); out = pathlib.Path(out_dir)
    im = gradient().convert('RGBA'); problems = []
    for l in layers:
        lay = Image.open(out / l['png']).convert('RGBA')
        bb = lay.getchannel('A').point(lambda a: 255 if a > 150 else 0).getbbox()      # solid pixels only; soft shadows may pass the edge
        if bb and (bb[0] < SX0 - 1 or bb[1] < SY0 - 1 or bb[2] > SX1 + 1 or bb[3] > SY1 + 1): problems.append(f"{l['png']} leaves the safe area {bb}")
        im.alpha_composite(lay)
    if chip:
        p = pill(chip, F(25, 'b'), TEAL, padx=20, pady=8); im.alpha_composite(p, (40, 18))
    if guides:
        d = ImageDraw.Draw(im); d.rectangle((SX0, SY0, SX1, SY1), outline=(255, 60, 60)); d.line([(0, 1020), (W, 1020)], fill=(255, 60, 60))
    if not INFO[prefix]['fits']: problems.append(f"content needs {INFO[prefix]['need']} px but only {INFO[prefix]['avail']} px are free")
    INFO[prefix]['problems'] = problems; INFO[prefix]['layers'] = layers
    path = out / f'preview_{prefix}.png'; im.convert('RGB').save(path)
    return str(path)

# ------------------------------------------------------------------ command line
def _fill(n, words):
    """A realistic string of exactly n characters."""
    s = ''
    i = 0
    while len(s) < n: s = (s + ' ' + words[i % len(words)]).strip(); i += 1
    s = s[:n].rstrip()
    return s + 'x' * (n - len(s))

def stress_graphics():
    wd = 'Doctor approved plan reaches the patient phone before discharge and nurses see who needs a call first today'.split()
    acc = ['teal', 'amber', 'green', 'violet']
    full = {'type': 'cards', 'cue': None, 'head': _fill(48, wd), 'sub': _fill(90, wd[3:]),
            'cards': [{'kicker': _fill(34, wd[i:]), 'title': _fill(34, wd[i + 2:]), 'lines': [_fill(46, wd[i + k:]) for k in range(4)],
                       'tag': _fill(34, wd[i + 5:]), 'accent': acc[i], 'style': 'dashed' if i % 2 else 'solid', 'big': ['49 lakh', 'Rs 1,000', '6% - 72%', '1 in 10'][i],
                       'cue': None} for i in range(4)],
            'footer': _fill(110, wd[1:]), 'footer_cue': None}
    two = {'type': 'cards', 'cue': None, 'head': 'Who we design for', 'sub': 'Illustrative personas, not real people.',
           'cards': [{'kicker': 'Patient persona', 'title': 'Kamala, 68', 'lines': ['Home after lung surgery', 'Reads Hindi', 'Needs one clear screen, one action at a time'],
                      'tag': 'Illustrative persona', 'accent': 'teal', 'style': 'solid', 'big': None, 'cue': None},
                     {'kicker': 'Nurse persona', 'title': 'Sister Anjali, ward nurse', 'lines': ['Must know whom to call first, and why', 'Has limited time for repeated coaching'],
                      'tag': None, 'accent': 'violet', 'style': 'solid', 'big': None, 'cue': None}], 'footer': None, 'footer_cue': None}
    dashed = {'type': 'cards', 'cue': None, 'head': 'What a pilot would measure', 'sub': 'Illustrative targets, not results.',
              'cards': [{'kicker': 'Activation', 'title': 'Plan viewed within 48 hours', 'lines': ['of enrolled patients'], 'tag': 'Illustrative target',
                         'accent': 'amber', 'style': 'dashed', 'big': '80%', 'cue': None},
                        {'kicker': 'Day-7 return', 'title': 'Activated patients who return', 'lines': ['of activated patients', 'counted from the app record'], 'tag': 'Illustrative target',
                         'accent': 'green', 'style': 'dashed', 'big': '60%', 'cue': None},
                        {'kicker': 'Proposed price', 'title': 'Per care follow-up episode', 'lines': ['Paid by the hospital'], 'tag': 'Proposed, unvalidated',
                         'accent': 'violet', 'style': 'dashed', 'big': 'Rs 1,000', 'cue': None}],
              'footer': 'Targets are illustrative. Nothing here has been measured.', 'footer_cue': None}
    strip = {'type': 'strip', 'cue': None, 'head': 'One journey, five steps',
             'steps': [{'title': _fill(16, wd[i * 2:]), 'text': _fill(44, wd[i + 1:]), 'cue': None} for i in range(5)], 'footer': _fill(110, wd[2:])}
    strip3 = {'type': 'strip', 'cue': None, 'head': 'Three steps', 'steps': [{'title': t, 'text': x, 'cue': None} for t, x in
              [('In hospital', 'Doctor registers; admin admits to a bed'), ('Discharge', 'Doctor sends medicines and care instructions'), ('At home', 'Kamala reads her plan')]],
              'footer': None}
    wide = json.loads(json.dumps(full)); wide['head'] = 'W' * 40; wide['sub'] = None; wide['footer'] = None
    for c in wide['cards']: c['title'] = 'MMMMMMMMMMMM WWWWWWWWWW MMMMMMMMMM'; c['kicker'] = 'W' * 34; c['tag'] = 'M' * 34
    return [('stress_4max', full, 'STRESS  \u00b7  4 CARDS, EVERY FIELD AT ITS LIMIT'), ('stress_2', two, 'STRESS  \u00b7  2 CARDS'),
            ('stress_3dashed', dashed, 'STRESS  \u00b7  3 DASHED CARDS, BIG NUMBERS'), ('stress_strip5', strip, 'STRESS  \u00b7  5-STEP STRIP WITH FOOTER'),
            ('stress_strip3', strip3, 'STRESS  \u00b7  3-STEP STRIP'), ('stress_4wide', wide, 'STRESS  \u00b7  WIDEST GLYPHS')]

def _report(prefix, path):
    i = INFO[prefix]; f = i['fonts']
    state = 'OK' if not i['problems'] else 'PROBLEM: ' + '; '.join(i['problems'])
    print(f"{prefix:<16} {i['type']:<5} {i['n']} boxes {i['box'][0]}x{i['box'][1]} at y={i['y']}  scale={i['scale']:.2f} air={i['air']:.1f}  "
          f"title {f['title']}px line {f['line']}px  layers={len(i['layers'])}  {state}  ->  {pathlib.Path(path).name}")

def main(argv):
    args = [a for a in argv if not a.startswith('--')]; flags = {a for a in argv if a.startswith('--')}
    if '--stress' in flags and len(args) == 1: spec_path, out_dir = None, args[0]
    elif len(args) == 2: spec_path, out_dir = args
    else: raise SystemExit(__doc__)
    guides = '--guides' in flags; bad = 0
    if spec_path:
        spec = json.load(open(spec_path, encoding='utf-8')); jobs = []
        for bi, blk in enumerate(spec.get('part1', [])):
            jobs += [(f'p1_{bi}_{i}', g, blk.get('chip')) for i, g in enumerate(blk.get('graphics', [])) if g.get('type') in ('cards', 'strip')]
        o = spec.get('outro') or {}
        jobs += [('outro' if i == 0 else f'outro_{i}', g, o.get('chip')) for i, g in enumerate(o.get('graphics', [])) if g.get('type') in ('cards', 'strip')]
        for prefix, g, chip in jobs:
            _report(prefix, preview(g, out_dir, prefix, chip=chip or None, guides=guides)); bad += bool(INFO[prefix]['problems'])
    if '--stress' in flags:
        for prefix, g, chip in stress_graphics():
            _report(prefix, preview(g, out_dir, prefix, chip=chip, guides=guides)); bad += bool(INFO[prefix]['problems'])
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
