"""Weekly progress card as a PNG (Pillow), in SpiroBuddy colours, English + Hindi.

Easy to forward to relatives on WhatsApp. Hindi needs a Devanagari font (Nirmala UI on Windows,
Noto Sans Devanagari on Linux). Pillow wheels on Windows have no complex-script shaper (raqm),
so the Hindi lines use words without conjuncts and we re-order the short-i vowel sign ourselves.
If no Devanagari font exists (e.g. a bare Linux server), the card is English-only.
"""
from __future__ import annotations

import io
import os
from datetime import date
from functools import lru_cache

from .common import first_name, lang_of
from .progress import progress

# Same tokens as web/css/styles.css (light theme)
C = {"bg": "#f4f6f9", "surface": "#ffffff", "border": "#dbe1e8", "text": "#13202e",
     "text2": "#4a5868", "text3": "#6b7888", "brand": "#0b6e8a", "brand_soft": "#e3f2f6",
     "green": "#1d7a3a", "green_dot": "#2e9d4e", "green_soft": "#e7f6ec", "yellow": "#a15c00",
     "yellow_dot": "#f0a020", "red": "#c62828", "mint": "#7fe0c8"}

W = H = 1080

LATIN = {
    "regular": [r"C:\Windows\Fonts\segoeui.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/dejavu/DejaVuSans.ttf", "/usr/share/fonts/TTF/DejaVuSans.ttf"],
    "bold": [r"C:\Windows\Fonts\segoeuib.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"],
}
DEVA = {
    "regular": [r"C:\Windows\Fonts\Nirmala.ttc", r"C:\Windows\Fonts\Nirmala.ttf",
                "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
                "/usr/share/fonts/noto/NotoSansDevanagari-Regular.ttf",
                "/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf"],
    "bold": [r"C:\Windows\Fonts\Nirmala.ttc|1", r"C:\Windows\Fonts\NirmalaB.ttf",
             "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
             "/usr/share/fonts/noto/NotoSansDevanagari-Bold.ttf"],
}


@lru_cache(maxsize=64)
def _font(kind: str, weight: str, size: int):
    from PIL import ImageFont
    for entry in (DEVA if kind == "deva" else LATIN)[weight]:
        path, _, idx = entry.partition("|")
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size, index=int(idx or 0))
            except OSError:
                continue
    if kind == "deva":
        return None
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def hindi_ok() -> bool:
    return _font("deva", "regular", 20) is not None


def _has_raqm() -> bool:
    try:
        from PIL import features
        return bool(features.check("raqm"))
    except Exception:
        return False


_CONS = set(chr(c) for c in range(0x0915, 0x093A)) | set(chr(c) for c in range(0x0958, 0x0960))
_HALANT, _I = "\u094d", "\u093f"


def deva_visual(s: str) -> str:
    """Basic-layout fix: move the short-i sign (ि) in front of its consonant cluster."""
    if _has_raqm():
        return s
    out: list[str] = []
    for ch in s:
        if ch == _I:
            j = len(out)
            # walk back over nukta + consonant (+ halant consonant)*
            if j and out[j - 1] == "\u093c":
                j -= 1
            if j and out[j - 1] in _CONS:
                j -= 1
                while j >= 2 and out[j - 1] == _HALANT and out[j - 2] in _CONS:
                    j -= 2
            out.insert(j, ch)
        else:
            out.append(ch)
    return "".join(out)


def _is_deva(s: str) -> bool:
    return any("\u0900" <= ch <= "\u097f" for ch in s)


def _text(draw, xy, s, size, color, weight="regular", anchor="la"):
    """Draw mixed text: Devanagari runs with the Devanagari font, the rest with the Latin font."""
    if not _is_deva(s):
        draw.text(xy, s, font=_font("latin", weight, size), fill=color, anchor=anchor)
        return draw.textlength(s, font=_font("latin", weight, size))
    dfont = _font("deva", weight, size) or _font("deva", "regular", size)
    lfont = _font("latin", weight, size)
    runs, cur, cur_deva = [], "", None
    for ch in s:
        d = "\u0900" <= ch <= "\u097f" or (ch == " " and cur_deva)
        if cur_deva is None or d == cur_deva:
            cur += ch
            cur_deva = d if cur_deva is None else cur_deva
        else:
            runs.append((cur, cur_deva))
            cur, cur_deva = ch, d
    if cur:
        runs.append((cur, cur_deva))
    total = sum(draw.textlength(deva_visual(r) if d else r, font=dfont if d else lfont)
                for r, d in runs)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    elif anchor[0] == "r":
        x -= total
    va = "l" + anchor[1]
    for r, d in runs:
        txt = deva_visual(r) if d else r
        f = dfont if d else lfont
        draw.text((x, y), txt, font=f, fill=color, anchor=va)
        x += draw.textlength(txt, font=f)
    return total


def render_card(pid: int, lang: str = "hi") -> bytes | None:
    from PIL import Image, ImageDraw
    pr = progress(pid)
    if not pr:
        return None
    lang = lang_of(lang, "en")
    hi = lang == "hi" and hindi_ok()
    p = pr["patient"]
    fn = first_name(p["name"])
    img = Image.new("RGB", (W, H), C["bg"])
    d = ImageDraw.Draw(img)

    # header band
    d.rectangle([0, 0, W, 190], fill=C["brand"])
    d.rounded_rectangle([56, 52, 136, 132], radius=20, fill="#ffffff")
    d.rounded_rectangle([82, 66, 100, 120], radius=9, fill=C["brand_soft"])
    d.rounded_rectangle([82, 88, 100, 120], radius=9, fill=C["brand"])
    for yy in (78, 100):
        d.line([(108, yy), (118, yy), (124, yy + 6)], fill=C["mint"], width=5)
    _text(d, (160, 58), "SpiroBuddy", 54, "#ffffff", "bold")
    _text(d, (162, 128), "Weekly breathing progress" + ("  ·  पिछले 7 दिन" if hi else ""), 30,
          "#d8eef5")

    # name + dates
    week = pr["week"]
    try:
        d0, d1 = date.fromisoformat(week[0]["date"]), date.fromisoformat(week[-1]["date"])
        rng = f"{d0.day} {d0.strftime('%b')} – {d1.day} {d1.strftime('%b %Y')}"
    except Exception:
        rng = ""
    _text(d, (56, 230), f"{p['name']}", 60, C["text"], "bold")
    _text(d, (58, 312), rng + (f"  ·  recovery day {_pod(p)}" if _pod(p) else ""), 30, C["text2"])

    # stat tiles
    tiles = [
        (f"{pr['week_sessions']}", "sessions done", "सेशन पूरे" if hi else "", C["green"], C["green_soft"]),
        (f"{int(pr['week_best']):,} mL", "biggest breath", "सबसे बड़ी साँस" if hi else "", C["brand"], C["brand_soft"]),
        (f"{pr['streak']} days", "good days in a row", f"लगातार {pr['streak']} दिन" if hi else "",
         C["yellow"], "#fff5e0"),
    ]
    tw, gap, ty = (W - 112 - 2 * 24) // 3, 24, 370
    for i, (num, lbl, hil, col, soft) in enumerate(tiles):
        x = 56 + i * (tw + gap)
        d.rounded_rectangle([x, ty, x + tw, ty + 170], radius=22, fill=soft)
        _text(d, (x + 26, ty + 22), num, 50, col, "bold")
        _text(d, (x + 28, ty + 90), lbl, 26, C["text2"])
        if hil:
            _text(d, (x + 28, ty + 124), hil, 26, C["text2"])

    # chart
    cx0, cy0, cx1, cy1 = 56, 580, W - 56, 920
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=22, fill=C["surface"], outline=C["border"], width=2)
    target = float(p.get("target_ml") or 2000)
    vmax = max([target * 1.1] + [h.get("best_ml") or 0 for h in week]) or 1
    px0, px1, py0, py1 = cx0 + 40, cx1 - 30, cy0 + 100, cy1 - 70
    _text(d, (cx0 + 30, cy0 + 16), "Best breath each day (mL)" + ("  ·  हर दिन की सबसे बड़ी साँस" if hi else ""),
          26, C["text2"], "bold")
    ty_ = py1 - (target / vmax) * (py1 - py0)
    x = px0
    while x < px1:
        d.line([(x, ty_), (min(x + 16, px1), ty_)], fill=C["red"], width=3)
        x += 28
    _text(d, (px1, ty_ - 8), f"target {int(target):,}", 22, C["red"], "regular", "rd")
    n = len(week) or 1
    slot = (px1 - px0) / n
    for i, h in enumerate(week):
        v = float(h.get("best_ml") or 0)
        bx = px0 + i * slot + slot * 0.2
        bw = slot * 0.6
        top = py1 - (v / vmax) * (py1 - py0)
        col = C["brand"] if v >= 0.8 * target else C["yellow_dot"]
        if v > 0:
            d.rounded_rectangle([bx, top, bx + bw, py1], radius=10, fill=col)
            _text(d, (bx + bw / 2, top - 6), f"{int(v):,}", 20, C["text2"], "regular", "md")
        try:
            dd = date.fromisoformat(h["date"])
            lbl = "Today" if i == n - 1 else dd.strftime("%a")
        except Exception:
            lbl = ""
        _text(d, (bx + bw / 2, py1 + 14), lbl, 24, C["text"], "bold", "ma")
        cnt = f"{h.get('sessions_done', 0)} done"
        cw = d.textlength(cnt, font=_font("latin", "regular", 20))
        dx = bx + bw / 2 - cw / 2 - 4
        d.ellipse([dx - 10, py1 + 50, dx, py1 + 60], fill=C["green_dot"])
        _text(d, (bx + bw / 2 + 4, py1 + 42), cnt, 20, C["green"], "regular", "ma")

    # footer message
    if hi:
        msg = f"शाबाश {fn} जी! हर घंटे धीरे-धीरे गहरी साँस लेते रहिए।"
    else:
        msg = f"Great effort, {fn} ji! Keep breathing slowly and deeply every hour."
    _text(d, (W / 2, 968), msg, 32, C["text"], "bold", "ma")
    _text(d, (W / 2, 1024), "SpiroBuddy coaches and summarises – it does not diagnose. Emergency: 112",
          22, C["text3"], "regular", "ma")
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def _pod(p: dict) -> int | None:
    try:
        from .common import now
        return (now().date() - date.fromisoformat(str(p.get("surgery_date"))[:10])).days
    except Exception:
        return None


def caption(pid: int, lang: str) -> str:
    pr = progress(pid)
    if not pr:
        return ""
    p = pr["patient"]
    fn = first_name(p["name"])
    if lang == "hi":
        return (f"📊 {fn} जी का हफ़्ता: {pr['week_sessions']} सेशन पूरे, सबसे बड़ी साँस "
                f"{int(pr['week_best']):,} mL (लक्ष्य {p['target_ml']:,} mL)। "
                + (f"लगातार {pr['streak']} अच्छे दिन 🔥 " if pr["streak"] else "")
                + "उनका हौसला बढ़ाते रहिए 💛")
    return (f"📊 {fn}'s week: {pr['week_sessions']} sessions done, biggest breath "
            f"{int(pr['week_best']):,} mL (target {p['target_ml']:,} mL). "
            + (f"{pr['streak']} good days in a row 🔥 " if pr["streak"] else "")
            + "Keep cheering them on 💛")
