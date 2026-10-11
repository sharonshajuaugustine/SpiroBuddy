"""Demo branding for the two fictional demo hospitals (docs/plan/12 section 2).

ensure(st) adds a branding block (a name, a short name, an accent colour and a small generated
logo: initials on a coloured rounded square) to a demo hospital that has none. ensure(st,
reset=True) puts it back to these values; seed.seed() calls it right after seed_auth.ensure(),
which resets hospital settings, so a demo reset brings the branding back.
Names are made up from the demo hospitals' own fictional names. Never raises.
"""
from __future__ import annotations

import io
import logging

from . import authz, branding

log = logging.getLogger("spirobuddy.seed_branding")

DEMO = {
    1: {"display_name": "Demo General Care", "short_name": "Demo General",
        "accent": "#1b5e9e", "initials": "DG"},
    2: {"display_name": "Riverside Care", "short_name": "Riverside",
        "accent": "#8e3b5f", "initials": "RS"},
}


def make_logo(initials: str, accent: str, size: int = 256) -> bytes:
    """A simple PNG logo: white initials on a rounded square in the accent colour."""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, size - 1, size - 1), radius=size // 5, fill=accent)
    ink = branding.strip_ink(accent)
    font = None
    for name in ("arialbd.ttf", "DejaVuSans-Bold.ttf", "arial.ttf"):
        try:
            font = ImageFont.truetype(name, int(size * 0.42))
            break
        except OSError:
            continue
    if font is None:
        try:
            font = ImageFont.load_default(size=int(size * 0.42))
        except TypeError:
            font = ImageFont.load_default()
    box = d.textbbox((0, 0), initials, font=font)
    x = (size - (box[2] - box[0])) / 2 - box[0]
    y = (size - (box[3] - box[1])) / 2 - box[1]
    d.text((x, y), initials, font=font, fill=ink)
    out = io.BytesIO()
    img.save(out, "PNG", optimize=True)
    return out.getvalue()


def ensure(st, reset: bool = False) -> None:
    """Give each demo hospital its branding (only when it has none, or always with reset=True)."""
    try:
        ist = authz.ident(st)
        for hid, spec in DEMO.items():
            if not ist.select("hospitals", [("id", "eq", hid)], columns="id", limit=1):
                continue
            current = branding.load(hid)
            if current["saved"] and current["logo_path"] and not reset:
                continue
            if current["logo_path"]:
                branding.clear_logo(hid)
            branding.save(hid, {k: spec[k] for k in branding.EDITABLE})
            try:
                branding.set_logo(hid, make_logo(spec["initials"], spec["accent"]), "image/png")
            except Exception as e:             # no Pillow or file storage down: name and colour still work
                log.warning("demo logo for hospital %s not made: %s", hid, e)
    except Exception as e:
        log.warning("branding seed failed: %s", e)
