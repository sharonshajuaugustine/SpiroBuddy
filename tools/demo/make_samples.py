"""Make the synthetic sample prescriptions and discharge summary for the demo.

    .venv\\Scripts\\python.exe tools\\demo\\make_samples.py

Writes into web/samples/:
  rx_ravi_printed.png         clean printed prescription (Ravi Kumar) – matches the seeded approved one
  rx_priya_printed.png        clean printed prescription (Priya Sharma)
  rx_ravi_messy.png           "phone photo" of a prescription with one blurred dose/frequency
  discharge_summary_ravi.png  one-page discharge summary (Ravi Kumar)
  discharge_summary_ravi.pdf  the same page as a PDF
  samples.json                what each file says (the expected transcription), for tests and
                              the no-AI demo fallback

Everything is fictional: hospital, doctor, registration number and patients. Every page carries a
large "SAMPLE – FICTIONAL – NOT FOR CLINICAL USE" watermark and footer. Pillow only, system fonts
only (no downloads), and the output is the same every run on the same machine.
"""
from __future__ import annotations

import json
import math
import random
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "web" / "samples"

W, H = 1240, 1754            # A4 portrait at 150 dpi
DPI = 150
M = 90                       # page margin

WATERMARK = "SAMPLE – FICTIONAL – NOT FOR CLINICAL USE"
HOSPITAL = "Demo General Hospital (fictional)"
HOSPITAL_ADDR = "12 Sample Street, Demo City · Phone 0000 000 000 (fictional)"
DOCTOR = "Dr. Meera Nair (fictional)"
DOCTOR_LINE = f"{DOCTOR} – General Surgery"
DOCTOR_QUAL = "MBBS, MS (General Surgery) · Reg. No. DEMO-0000"

INK = (24, 32, 44)
GREY = (92, 102, 116)
TEAL = (14, 112, 120)
RED = (176, 28, 36)
PAPER = (255, 255, 255)

# ---------------------------------------------------------------- fonts

_REG = ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:/Windows/Fonts/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf",
        "DejaVuSans.ttf", "arial.ttf"]
_BOLD = ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/segoeuib.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "C:/Windows/Fonts/DejaVuSans-Bold.ttf",
         "/Library/Fonts/Arial Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
         "DejaVuSans-Bold.ttf", "arialbd.ttf"]
_cache: dict[tuple[bool, int], ImageFont.FreeTypeFont] = {}


def font(size: int, bold: bool = False):
    """A system TrueType font at `size` px, or Pillow's built-in font as a last resort."""
    key = (bold, size)
    if key not in _cache:
        for path in (_BOLD if bold else _REG) + _REG:
            try:
                _cache[key] = ImageFont.truetype(path, size)
                break
            except OSError:
                continue
        else:
            _cache[key] = ImageFont.load_default(size=size)
    return _cache[key]


def text_w(draw: ImageDraw.ImageDraw, s: str, f) -> int:
    return int(draw.textlength(s, font=f))


def fit_font(draw, s: str, max_w: int, size: int, bold: bool = False, min_size: int = 18):
    """Largest font (from `size` down) that fits `s` in `max_w` px."""
    while size > min_size and text_w(draw, s, font(size, bold)) > max_w:
        size -= 1
    return font(size, bold)


# ---------------------------------------------------------------- page pieces

def new_page() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), PAPER)
    return img, ImageDraw.Draw(img)


def letterhead(d: ImageDraw.ImageDraw) -> int:
    """Hospital + doctor header. Returns the y just below it."""
    d.rounded_rectangle((M, 70, M + 96, 166), radius=18, fill=TEAL)
    f = font(44, True)
    tw = text_w(d, "DG", f)
    d.text((M + 48 - tw // 2, 92), "DG", font=f, fill=PAPER)
    d.text((M + 122, 74), HOSPITAL, font=fit_font(d, HOSPITAL, W - 2 * M - 122, 46, True), fill=TEAL)
    d.text((M + 124, 134), HOSPITAL_ADDR, font=font(22), fill=GREY)
    d.rectangle((M, 190, W - M, 194), fill=TEAL)
    d.text((M, 214), DOCTOR_LINE, font=font(32, True), fill=INK)
    d.text((M, 258), DOCTOR_QUAL, font=font(23), fill=GREY)
    right = "OPD: Mon–Sat, 9 AM – 1 PM"
    d.text((W - M - text_w(d, right, font(23)), 262), right, font=font(23), fill=GREY)
    d.line((M, 304, W - M, 304), fill=(200, 206, 214), width=2)
    return 324


def patient_row(d, y: int, name: str, age_sex: str, date: str, ref: str) -> int:
    f_l, f_v = font(25), font(27, True)
    x = M
    for label, value, width in (("Name: ", name, 520), ("Age/Sex: ", age_sex, 270), ("Date: ", date, 0)):
        d.text((x, y), label, font=f_l, fill=GREY)
        d.text((x + text_w(d, label, f_l), y - 2), value, font=f_v, fill=INK)
        x += width
    d.text((M, y + 46), ref, font=font(23), fill=GREY)
    d.line((M, y + 92, W - M, y + 92), fill=(200, 206, 214), width=2)
    return y + 112


def rx_lines(d, y: int, lines: list[list[str]]) -> tuple[int, list[list[tuple[int, int, int, int]]]]:
    """Draw numbered prescription lines. Each line is a list of segments joined by ' – '.

    Returns the y below the block and, per line, the box of each segment (used to blur one).
    """
    d.text((M, y), "Rx", font=font(66, True), fill=TEAL)
    y += 100
    boxes = []
    x0 = M + 30
    max_w = W - M - x0
    for i, segs in enumerate(lines, 1):
        full = f"{i}. " + " – ".join(segs)
        f = fit_font(d, full, max_w, 31)
        x = x0
        seg_boxes = []
        num = f"{i}. "
        d.text((x, y), num, font=f, fill=INK)
        x += text_w(d, num, f)
        for j, seg in enumerate(segs):
            if j:
                sep = " – "
                d.text((x, y), sep, font=f, fill=INK)
                x += text_w(d, sep, f)
            sw = text_w(d, seg, f)
            d.text((x, y), seg, font=f, fill=INK)
            seg_boxes.append((x, y - 4, x + sw, y + f.size + 10))
            x += sw
        boxes.append(seg_boxes)
        y += 84
    return y, boxes


def signature(d, y: int, who: str, role: str) -> None:
    """A drawn squiggle above a signature line, bottom right."""
    x1, x2 = W - M - 420, W - M
    pts = []
    for k in range(0, 161):
        t = k / 160
        px = x1 + 40 + t * 300
        py = y + 40 - 26 * math.sin(t * math.pi * 5.0) * (1 - 0.6 * t) - 18 * t
        pts.append((px, py))
    d.line(pts, fill=(30, 50, 120), width=4, joint="curve")
    d.line((x1 + 70, y + 64, x1 + 260, y + 52), fill=(30, 50, 120), width=3)
    d.line((x1, y + 90, x2, y + 90), fill=INK, width=2)
    d.text((x1, y + 100), who, font=font(25, True), fill=INK)
    d.text((x1, y + 134), role, font=font(22), fill=GREY)


def footer(d) -> None:
    d.line((M, H - 118, W - M, H - 118), fill=(200, 206, 214), width=2)
    f = font(26, True)
    d.text(((W - text_w(d, WATERMARK, f)) // 2, H - 100), WATERMARK, font=f, fill=RED)
    sub = "Synthetic demo file made for SpiroBuddy. Fictional hospital, doctor and patient."
    fs = font(20)
    d.text(((W - text_w(d, sub, fs)) // 2, H - 62), sub, font=fs, fill=GREY)


def watermark(img: Image.Image) -> Image.Image:
    """Large, semi-transparent diagonal watermark, repeated across the page."""
    side = int(math.hypot(W, H)) + 200
    layer = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = font(68, True)
    tw = text_w(d, WATERMARK, f)
    for k in range(-2, 3):          # the middle row runs corner to corner and fits in full
        yy = side // 2 + k * 470 - f.size // 2
        d.text(((side - tw) // 2, yy), WATERMARK, font=f, fill=(196, 30, 40, 76))
    layer = layer.rotate(45, resample=Image.BICUBIC)     # counter-clockwise: rises left to right
    left, top = (side - W) // 2, (side - H) // 2
    layer = layer.crop((left, top, left + W, top + H))
    base = img.convert("RGBA")
    base.alpha_composite(layer)
    return base.convert("RGB")


def photo_effect(page: Image.Image, seed: int) -> Image.Image:
    """Make a clean page look like a slightly tilted phone photo on a table."""
    rnd = random.Random(seed)
    # warm paper tint and uneven light (brightest near the top left, darker at the far corner)
    glow = Image.radial_gradient("L").resize((int(W * 2.2), int(H * 2.2)), Image.BILINEAR)
    left, top = int(W * 2.2) // 2 - int(W * 0.3), int(H * 2.2) // 2 - int(H * 0.25)
    shade = glow.crop((left, top, left + W, top + H)).point(lambda v: 255 - v // 4)
    tint = Image.new("RGB", (W, H), (248, 243, 230))
    paper = Image.composite(page, tint, Image.new("L", (W, H), 236))
    paper = Image.composite(paper, Image.new("RGB", (W, H), (150, 145, 135)), shade)
    # fine grain (deterministic)
    gw, gh = W // 2, H // 2
    noise = Image.frombytes("L", (gw, gh), rnd.randbytes(gw * gh)).resize((W, H), Image.BILINEAR)
    noise = noise.point(lambda v: 128 + (v - 128) // 6)
    grain = Image.merge("RGB", (noise, noise, noise))
    paper = Image.blend(paper, grain, 0.10)
    paper = paper.filter(ImageFilter.GaussianBlur(0.7))
    # place it, a little smaller and tilted, on a darker table
    small = paper.resize((int(W * 0.92), int(H * 0.92)), Image.LANCZOS)
    table = Image.new("RGB", (W, H), (88, 80, 72))
    tilted = small.rotate(1.6, resample=Image.BICUBIC, expand=True, fillcolor=(0, 0, 0))
    mask = Image.new("L", small.size, 255).rotate(1.6, resample=Image.BICUBIC, expand=True, fillcolor=0)
    table.paste(tilted, ((W - tilted.width) // 2 + 6, (H - tilted.height) // 2 - 4), mask)
    return table


def save_png(img: Image.Image, path: Path, colors: int = 64) -> None:
    """Palette PNG keeps the files small (well under 1.5 MB) and the output repeatable."""
    q = img.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q.save(path, format="PNG", optimize=True)


# ---------------------------------------------------------------- the samples

RAVI_LINES = [
    ["Tab. Pantoprazole 40 mg", "1-0-0", "before breakfast", "x 14 days"],
    ["Tab. Paracetamol 650 mg", "TDS", "after food", "x 5 days"],
    ["Tab. Ondansetron 4 mg", "SOS (if vomiting)"],
]
PRIYA_LINES = [
    ["Tab. Cefuroxime 500 mg", "BD", "after food", "x 5 days"],
    ["Tab. Pantoprazole 40 mg", "OD", "before breakfast", "x 7 days"],
    ["Tab. Paracetamol 500 mg", "SOS (if pain)"],
]
# Line 2's dose/frequency ("1-1-1") is printed, then blurred so nobody can be sure of it.
MESSY_LINES = [
    ["Tab. Cetirizine 10 mg", "0-0-1", "at night", "x 5 days"],
    ["Tab. Metoclopramide 10 mg", "1-1-1", "before food", "x 3 days"],
    ["Tab. Folic acid 5 mg", "1-0-0", "after breakfast", "x 30 days"],
]
MESSY_BLUR = (1, 1)          # (line index, segment index) that gets blurred


def prescription(name: str, age_sex: str, date: str, ref: str, lines: list[list[str]],
                 blur: tuple[int, int] | None = None) -> Image.Image:
    img, d = new_page()
    y = letterhead(d)
    y = patient_row(d, y + 10, name, age_sex, date, ref)
    y, boxes = rx_lines(d, y + 10, lines)
    d.text((M, y + 20), "Next review: as advised, or earlier if needed.", font=font(24), fill=GREY)
    signature(d, 1330, DOCTOR, "Signature – General Surgery")
    footer(d)
    if blur:
        x1, y1, x2, y2 = boxes[blur[0]][blur[1]]
        box = (x1 - 14, y1 - 8, x2 + 14, y2 + 6)
        # strong blur, then darken so it reads as a smudge of ink, not as an empty gap
        region = img.crop(box).filter(ImageFilter.GaussianBlur(7))
        region = region.point(lambda v: max(0, int(255 - (255 - v) * 2.4)))
        img.paste(region, box)
    return watermark(img)


def discharge_summary() -> Image.Image:
    img, d = new_page()
    y = letterhead(d)
    title = "DISCHARGE SUMMARY"
    ft = font(40, True)
    d.text(((W - text_w(d, title, ft)) // 2, y + 6), title, font=ft, fill=INK)
    y += 76
    rows = [
        ("Patient", "Ravi Kumar", "Age/Sex", "58 M"),
        ("IP No.", "DEMO-IP-2001", "Ward", "Surgery ward (demo)"),
        ("Admitted", "02/10/2026", "Operated", "02/10/2026"),
        ("Discharged", "03/10/2026", "Department", "General Surgery"),
    ]
    fl, fv = font(24), font(26, True)
    for a, av, b, bv in rows:
        d.text((M, y), a, font=fl, fill=GREY)
        d.text((M + 170, y - 2), av, font=fv, fill=INK)
        d.text((M + 560, y), b, font=fl, fill=GREY)
        d.text((M + 730, y - 2), bv, font=fv, fill=INK)
        y += 46
    d.text((M, y), "Consultant", font=fl, fill=GREY)
    d.text((M + 170, y - 2), DOCTOR, font=fv, fill=INK)
    y += 46
    d.text((M, y), "Operation", font=fl, fill=GREY)
    d.text((M + 170, y - 2), "Open hernia repair (abdominal surgery)", font=fv, fill=INK)
    y += 60
    d.line((M, y, W - M, y), fill=(200, 206, 214), width=2)
    y += 22

    d.text((M, y), "Advice on discharge", font=font(30, True), fill=TEAL)
    y += 54
    advice = [
        "Incentive spirometer: 10 breaths every hour while awake.",
        "Walk a little several times a day.",
        "Keep the wound clean and dry.",
        "Medicines: as per the separate prescription.",
        "Follow-up: in 1 week, General Surgery OPD (10/10/2026).",
    ]
    fa = font(27)
    for i, line in enumerate(advice, 1):
        d.text((M + 20, y), f"{i}.", font=fa, fill=INK)
        d.text((M + 62, y), line, font=fit_font(d, line, W - 2 * M - 62, 27), fill=INK)
        y += 50
    y += 20
    d.text((M, y), "When to get help", font=font(30, True), fill=TEAL)
    y += 52
    help_lines = ["Contact the hospital, or call 112 in an emergency, if there is",
                  "breathlessness, chest pain, fever or bleeding from the wound."]
    for line in help_lines:
        d.text((M + 20, y), line, font=fa, fill=INK)
        y += 44
    signature(d, 1330, DOCTOR, "Consultant – General Surgery")
    footer(d)
    return watermark(img)


def ln(no, drug, form, strength, qty, unit, freq, food, dur, as_needed=False, instr=None, unclear=None):
    return {"line_no": no, "drug_name": drug, "form": form, "strength": strength,
            "dose_qty": qty, "dose_unit": unit, "frequency_raw": freq, "food_timing_raw": food,
            "duration_raw": dur, "as_needed": as_needed, "instructions_raw": instr,
            "unclear_fields": unclear or []}


DOSE_NOTE = ("dose_qty 1 follows the printed convention: 'Tab.' with a frequency and no number "
             "means one tablet each time.")


def entry(file: str, kind: str, mime: str, title: str, patient: str, date: str, legibility: str,
          description: str, lines: list[dict]) -> dict:
    """One samples.json record. `date` is as printed (dd/mm/yyyy); `doc_date` is ISO."""
    dd, mm, yyyy = date.split("/")
    doc_date = f"{yyyy}-{mm}-{dd}"
    return {
        "file": file, "url": f"/samples/{file}", "kind": kind, "mime": mime, "title": title,
        "patient_name": patient, "description": description,
        # header fields as the AI prompt (RX_PROMPT_V1) returns them
        "doctor_name": DOCTOR, "hospital_name": HOSPITAL, "date": date, "doc_date": doc_date,
        "patient_name_on_paper": patient, "handwritten": False, "legibility": legibility,
        "expected_lines": lines,
        # what the document helper (kind, title, date only) should suggest
        "expected_suggestion": {"kind": kind, "title": title, "doc_date": doc_date},
        "watermark": WATERMARK,
    }


def manifest() -> list[dict]:
    """The expected transcription of every sample. Unclear fields are null and listed, never guessed."""
    png, pdf = "image/png", "application/pdf"
    ds_text = ("One-page fictional discharge summary after an open hernia repair. Advice: incentive "
               "spirometer 10 breaths every hour while awake; follow-up in 1 week. No diagnoses beyond "
               "the operation name and no lab values.")
    ds_title = "Sample discharge summary – Ravi Kumar"
    return [
        entry("rx_ravi_printed.png", "prescription", png, "Sample prescription – Ravi Kumar (printed)",
              "Ravi Kumar", "09/10/2026", "clear",
              "Clean printed prescription. Same three medicines as Ravi's seeded, approved "
              "prescription. " + DOSE_NOTE,
              [ln(1, "Pantoprazole", "Tab.", "40 mg", 1, "tablet", "1-0-0", "before breakfast", "x 14 days"),
               ln(2, "Paracetamol", "Tab.", "650 mg", 1, "tablet", "TDS", "after food", "x 5 days"),
               ln(3, "Ondansetron", "Tab.", "4 mg", 1, "tablet", "SOS", None, None, True, "if vomiting")]),
        entry("rx_priya_printed.png", "prescription", png, "Sample prescription – Priya Sharma (printed)",
              "Priya Sharma", "08/10/2026", "clear",
              "Clean printed prescription for the second demo patient. " + DOSE_NOTE,
              [ln(1, "Cefuroxime", "Tab.", "500 mg", 1, "tablet", "BD", "after food", "x 5 days"),
               ln(2, "Pantoprazole", "Tab.", "40 mg", 1, "tablet", "OD", "before breakfast", "x 7 days"),
               ln(3, "Paracetamol", "Tab.", "500 mg", 1, "tablet", "SOS", None, None, True, "if pain")]),
        entry("rx_ravi_messy.png", "prescription", png,
              "Sample prescription – Ravi Kumar (phone photo, one unclear line)",
              "Ravi Kumar", "10/10/2026", "partly unclear",
              "Patient-uploaded phone photo. Line 2's dose and frequency are blurred, so they are "
              "left blank (null) and listed in unclear_fields – never guessed. The other lines are "
              "clear. " + DOSE_NOTE,
              [ln(1, "Cetirizine", "Tab.", "10 mg", 1, "tablet", "0-0-1", "at night", "x 5 days"),
               ln(2, "Metoclopramide", "Tab.", "10 mg", None, "tablet", None, "before food", "x 3 days",
                  unclear=["dose_qty", "frequency_raw"]),
               ln(3, "Folic acid", "Tab.", "5 mg", 1, "tablet", "1-0-0", "after breakfast", "x 30 days")]),
        entry("discharge_summary_ravi.png", "discharge_summary", png, ds_title, "Ravi Kumar",
              "03/10/2026", "clear", ds_text, []),
        entry("discharge_summary_ravi.pdf", "discharge_summary", pdf, ds_title, "Ravi Kumar",
              "03/10/2026", "clear", ds_text, []),
    ]


def check_manifest(records: list[dict]) -> None:
    """Every clear field in samples.json must be printed on its line; unclear ones sit in the blur."""
    printed = {"rx_ravi_printed.png": RAVI_LINES, "rx_priya_printed.png": PRIYA_LINES,
               "rx_ravi_messy.png": MESSY_LINES}
    for rec in records:
        for line in rec["expected_lines"]:
            segs = printed[rec["file"]][line["line_no"] - 1]
            text = " – ".join(segs)
            for key in ("drug_name", "form", "strength", "frequency_raw", "food_timing_raw",
                        "duration_raw", "instructions_raw"):
                if line[key] is not None:
                    assert line[key] in text, (rec["file"], line["line_no"], key)
                elif key in line["unclear_fields"]:
                    assert rec["file"] == "rx_ravi_messy.png" and (line["line_no"] - 1) == MESSY_BLUR[0]


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    check_manifest(manifest())
    ravi = prescription("Ravi Kumar", "58 M", "09/10/2026", "OP No. DEMO-OP-1001", RAVI_LINES)
    save_png(ravi, OUT_DIR / "rx_ravi_printed.png")
    priya = prescription("Priya Sharma", "44 F", "08/10/2026", "OP No. DEMO-OP-1002", PRIYA_LINES)
    save_png(priya, OUT_DIR / "rx_priya_printed.png")
    messy = prescription("Ravi Kumar", "58 M", "10/10/2026", "OP No. DEMO-OP-1001", MESSY_LINES,
                         blur=MESSY_BLUR)
    save_png(photo_effect(messy, seed=2026), OUT_DIR / "rx_ravi_messy.png", colors=96)
    ds = discharge_summary()
    save_png(ds, OUT_DIR / "discharge_summary_ravi.png")
    fixed = time.strptime("2026-10-03 12:00:00", "%Y-%m-%d %H:%M:%S")   # no "now" -> same bytes each run
    ds.save(OUT_DIR / "discharge_summary_ravi.pdf", format="PDF", resolution=DPI, quality=85,
            title="Sample discharge summary (fictional)", author="SpiroBuddy demo tools",
            subject=WATERMARK, creationDate=fixed, modDate=fixed)
    (OUT_DIR / "samples.json").write_text(json.dumps(manifest(), ensure_ascii=False, indent=1) + "\n",
                                          encoding="utf-8")
    for p in sorted(OUT_DIR.iterdir()):
        print(f"{p.relative_to(ROOT).as_posix():45s} {p.stat().st_size / 1024:8.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
