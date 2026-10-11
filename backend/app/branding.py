"""Each hospital's own name and logo inside the patient app (docs/plan/12 section 2).

The branding lives in hospitals.settings["branding"] (JSON, no schema change):
    {"display_name": "...", "short_name": "...", "logo_path": "<storage key>", "accent": "#rrggbb"}

What a hospital can change: the app name, a short name, an accent colour and a logo.
What it cannot change (fixed in code, never read from the store):
    * the small line "with SpiroBuddy" (POWERED_BY),
    * the safety messages and the status labels of the patient app.
The accent colour is painted on the brand strip at the top of the patient app and nowhere else.

Nothing here talks to the web: routes_admin.py calls load / view / save / set_logo.
"""
from __future__ import annotations

import hashlib
import io
import logging
import re

from . import authz, storage

log = logging.getLogger("spirobuddy.branding")

POWERED_BY = "with SpiroBuddy"              # fixed: no API can change this line
DEFAULT_ACCENT = "#0b6e8a"                  # the SpiroBuddy brand colour (light theme)
STRIP_INK_LIGHT = "#ffffff"                 # text colours the brand strip can use
STRIP_INK_DARK = "#101c27"
NAME_MIN, NAME_MAX = 2, 40
SHORT_MIN, SHORT_MAX = 2, 14
MAX_LOGO_BYTES = 512 * 1024                 # about 512 KB
LOGO_MAX_SIDE = 512
LOGO_MIMES = ("image/png", "image/jpeg", "image/webp")
EDITABLE = ("display_name", "short_name", "accent")
MIN_TEXT_CONTRAST = 4.5                     # text on the strip
MIN_EDGE_CONTRAST = 1.5                     # the strip must not vanish into the page background
PAGE_BG = {"light": "#f4f6f8", "dark": "#0d1319"}     # --bg of the two themes (css/styles.css)

# What a hospital can NOT change (shown on the admin page and returned by the API).
FIXED = [
    "The safety messages (for example the red-flag message and \"this app does not diagnose\").",
    "The status labels and their colours.",
    "The small line \"" + POWERED_BY + "\" under your name.",
]

_HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
_BAD_CHARS = re.compile(r"[\x00-\x1f\x7f<>\"`{}\\]")
_EXT_MIME = {"png": "image/png", "jpg": "image/jpeg", "webp": "image/webp"}


# ----------------------------------------------------------------------------- colours

def _lin(v: int) -> float:
    c = v / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a: str, b: str) -> float:
    """WCAG contrast ratio between two #rrggbb colours (1 to 21)."""
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def strip_ink(accent: str) -> str:
    """The text colour used on the brand strip: white if it reads well, else the dark ink."""
    return STRIP_INK_LIGHT if contrast(STRIP_INK_LIGHT, accent) >= contrast(STRIP_INK_DARK, accent) \
        else STRIP_INK_DARK


def check_accent(accent) -> tuple[str, dict]:
    """-> (normalised #rrggbb, report). Raises ValueError with a plain message when the colour
    is refused. The strip has the accent as its background, in the light and in the dark theme:
      * its text (white or dark ink, whichever reads better) needs 4.5:1;
      * the strip needs 1.5:1 against the page background of each theme, so it does not vanish
        (a near-white colour disappears on the light screen, a near-black one on the dark screen)."""
    if not isinstance(accent, str) or not _HEX.match(accent.strip()):
        raise ValueError("The colour must look like #0b6e8a (a # and six letters or digits).")
    accent = accent.strip().lower()
    ink = strip_ink(accent)
    text = contrast(ink, accent)
    if text < MIN_TEXT_CONTRAST:
        raise ValueError("This colour is too hard to read text on: neither white nor dark writing "
                         f"is clear enough on it (best {text:.1f} to 1, needs {MIN_TEXT_CONTRAST:g}). "
                         "Please pick a darker or a lighter shade.")
    light = contrast(accent, PAGE_BG["light"])
    dark = contrast(accent, PAGE_BG["dark"])
    if light < MIN_EDGE_CONTRAST:
        raise ValueError("This colour is too close to white. On the light screen the name strip "
                         "would fade into the page. Please pick a stronger colour.")
    if dark < MIN_EDGE_CONTRAST:
        raise ValueError("This colour is too close to black. On the dark screen the name strip "
                         "would fade into the page. Please pick a lighter colour.")
    return accent, {"ink": ink, "text_contrast": round(text, 2),
                    "light_contrast": round(light, 2), "dark_contrast": round(dark, 2)}


# ----------------------------------------------------------------------------- text

def _clean_name(value, label: str, lo: int, hi: int) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be text.")
    text = " ".join(value.split())
    if len(text) < lo:
        raise ValueError(f"{label} needs at least {lo} characters.")
    if len(text) > hi:
        raise ValueError(f"{label} can have at most {hi} characters.")
    if _BAD_CHARS.search(text):
        raise ValueError(f"{label} has a character that is not allowed (< > \" ` {{ }} or a backslash).")
    return text


def validate(values: dict) -> dict:
    """Check the fields a hospital may change. Only the keys given are checked and returned.
    Raises ValueError (plain message) at a problem."""
    out: dict = {}
    if "display_name" in values:
        out["display_name"] = _clean_name(values["display_name"], "The app name", NAME_MIN, NAME_MAX)
    if "short_name" in values:
        out["short_name"] = _clean_name(values["short_name"], "The short name", SHORT_MIN, SHORT_MAX)
    if "accent" in values:
        out["accent"] = check_accent(values["accent"])[0]
    return out


# ----------------------------------------------------------------------------- reading

def _hospital(hospital_id) -> dict:
    try:
        rows = authz.ident().select("hospitals", [("id", "eq", hospital_id)],
                                    columns="id,name,settings", limit=1)
    except Exception as e:
        log.warning("branding: could not read hospital %s: %s", hospital_id, e)
        return {}
    return rows[0] if rows else {}


def _stored(row: dict) -> dict:
    s = row.get("settings")
    b = s.get("branding") if isinstance(s, dict) else None
    return b if isinstance(b, dict) else {}


def default_short(name: str) -> str:
    """A short name made from the hospital's name: its opening word, cut to fit."""
    word = (name or "").replace("(", " ").split()
    return (word[0] if word else "Hospital")[:SHORT_MAX]


def load(hospital_id) -> dict:
    """The hospital's branding with defaults filled in. Never raises.
    -> {display_name, short_name, accent, logo_path (key or None), saved (bool), hospital_name}"""
    row = _hospital(hospital_id)
    stored = _stored(row)
    name = (row.get("name") or "SpiroBuddy").strip()
    out = {"hospital_name": name, "saved": bool(stored),
           "display_name": name[:NAME_MAX], "short_name": default_short(name),
           "accent": DEFAULT_ACCENT, "logo_path": None}
    try:
        if isinstance(stored.get("display_name"), str):
            out["display_name"] = validate({"display_name": stored["display_name"]})["display_name"]
        if isinstance(stored.get("short_name"), str):
            out["short_name"] = validate({"short_name": stored["short_name"]})["short_name"]
        if isinstance(stored.get("accent"), str):
            out["accent"] = check_accent(stored["accent"])[0]
    except ValueError:
        pass                                   # a damaged value falls back to the default
    lp = stored.get("logo_path")
    if isinstance(lp, str) and lp:
        out["logo_path"] = lp
    return out


def logo_version(logo_path) -> str | None:
    """A short fingerprint of the logo key, added to the logo address so a new logo shows at once."""
    return hashlib.sha256(logo_path.encode()).hexdigest()[:10] if logo_path else None


def view(hospital_id, logo_base: str) -> dict:
    """What the apps get: {display_name, short_name, accent, accent_ink, logo_url, powered_by}.
    logo_base is the address that serves the logo for this kind of session."""
    b = load(hospital_id)
    v = logo_version(b["logo_path"])
    return {"display_name": b["display_name"], "short_name": b["short_name"],
            "accent": b["accent"], "accent_ink": strip_ink(b["accent"]),
            "logo_url": f"{logo_base}?v={v}" if v else None,
            "powered_by": POWERED_BY}


def admin_view(hospital_id, logo_base: str) -> dict:
    """The view plus what the admin page needs (defaults, limits, what is fixed)."""
    b = load(hospital_id)
    out = view(hospital_id, logo_base)
    out.update({
        "saved": b["saved"], "hospital_name": b["hospital_name"],
        "defaults": {"display_name": b["hospital_name"][:NAME_MAX],
                     "short_name": default_short(b["hospital_name"]), "accent": DEFAULT_ACCENT},
        "limits": {"name_max": NAME_MAX, "short_max": SHORT_MAX, "logo_max_bytes": MAX_LOGO_BYTES,
                   "logo_max_side": LOGO_MAX_SIDE, "logo_types": ["PNG", "JPEG", "WebP"]},
        "fixed": list(FIXED),
        "contrast": check_accent(b["accent"])[1]})
    return out


# ----------------------------------------------------------------------------- writing

def _write(hospital_id, change: dict) -> None:
    """Merge `change` into settings["branding"] and keep every other setting as it is."""
    st = authz.ident()
    rows = st.select("hospitals", [("id", "eq", hospital_id)], columns="settings", limit=1)
    if not rows:
        raise LookupError("hospital not found")
    settings = dict(rows[0].get("settings") or {}) if isinstance(rows[0].get("settings"), dict) else {}
    block = dict(settings.get("branding") or {}) if isinstance(settings.get("branding"), dict) else {}
    for k, v in change.items():
        if v is None:
            block.pop(k, None)
        else:
            block[k] = v
    settings["branding"] = block
    st.update("hospitals", [("id", "eq", hospital_id)], {"settings": settings})


def save(hospital_id, values: dict) -> dict:
    """Validate and store the editable fields. Returns the validated values that were saved."""
    clean = validate({k: v for k, v in values.items() if k in EDITABLE})
    if not clean:
        raise ValueError("Nothing to save.")
    _write(hospital_id, clean)
    return clean


def process_logo(data: bytes, filename: str = "", declared: str | None = None) -> tuple[bytes, str]:
    """-> (clean image bytes, mime). PNG, JPEG or WebP only (SVG, PDF and everything else are
    refused), at most about 512 KB, decoded and re-encoded from the pixels (no metadata) and
    scaled down to at most 512 px. Raises ValueError with a plain message."""
    if not data:
        raise ValueError("The file is empty.")
    if len(data) > MAX_LOGO_BYTES:
        raise ValueError("The logo is larger than 512 KB. Please use a smaller picture.")
    mime, cleaned, _thumb = storage.validate_upload(data, filename or "logo", declared)
    if mime not in LOGO_MIMES:
        raise ValueError("The logo must be a PNG, JPEG or WebP picture.")
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(cleaned))
        img.load()
        if max(img.size) > LOGO_MAX_SIDE:
            img.thumbnail((LOGO_MAX_SIDE, LOGO_MAX_SIDE), Image.LANCZOS)
        out = io.BytesIO()
        if mime == "image/jpeg":
            img.convert("RGB").save(out, "JPEG", quality=88, optimize=True)
        elif mime == "image/webp":
            img.save(out, "WEBP", quality=88)
        else:
            img.save(out, "PNG", optimize=True)
        cleaned = out.getvalue()
    except Exception as e:
        raise ValueError("This picture can't be opened. Please try another file.") from e
    if len(cleaned) > MAX_LOGO_BYTES:
        raise ValueError("The logo is larger than 512 KB. Please use a smaller picture.")
    return cleaned, mime


def set_logo(hospital_id, data: bytes, mime: str) -> str:
    """Store a processed logo, point the branding at it and remove the old one. -> storage key."""
    old = load(hospital_id)["logo_path"]
    key = storage.save(data, mime, prefix="brand")
    _write(hospital_id, {"logo_path": key})
    _forget(old)
    return key


def clear_logo(hospital_id) -> bool:
    old = load(hospital_id)["logo_path"]
    if not old:
        return False
    _write(hospital_id, {"logo_path": None})
    _forget(old)
    return True


def _forget(key) -> None:
    if key:
        try:
            storage.delete(key)
        except Exception as e:                  # a leftover file is harmless
            log.info("branding: old logo not removed: %s", type(e).__name__)


def logo_bytes(hospital_id) -> tuple[bytes, str] | None:
    """(bytes, mime) of this hospital's logo, or None."""
    key = load(hospital_id)["logo_path"]
    if not key:
        return None
    try:
        data = storage.load(key)
    except (FileNotFoundError, ValueError, storage.StorageError):
        return None
    return data, _EXT_MIME.get(key.rsplit(".", 1)[-1], "application/octet-stream")
