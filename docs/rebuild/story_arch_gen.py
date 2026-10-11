"""Redraws the architecture picture. Run after a feature status changes:
    .venv/Scripts/python.exe docs/rebuild/story_arch_gen.py
It rewrites docs/hackathon/architecture_v2.svg and, in web/architecture.html, the inline copy and the box table.
Builds the standalone docs/hackathon/architecture_v2.svg and the inline copy from one box list. Statuses are read from features.py."""
import json
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from backend.app import features  # noqa: E402

W = {"live": "Live", "simulated": "Simulated", "in_development": "In development", "planned": "Planned"}

# (id, x, y, w, h, [title lines], key, description)
BOXES = []
def col(x, w, ys, items, h=48):
    for y, it in zip(ys, items):
        BOXES.append((x, y, w, h, *it))

YS = [74, 136, 198, 260, 322]
col(20, 210, YS, [
    (["Patient app"], "app.patient", "Large text, voice and no typing: breathing coach, medicines, visits and papers."),
    (["Family page"], "family.page", "A private link. With the patient's consent: today's ticks."),
    (["Hospital software"], "chart.tabs", "Doctor, nurse and admin: the triage list, the patient chart, prescriptions and visits."),
    (["Public story site"], "public.landing", "This site: landing, impact, trust, vision and architecture."),
    (["3D twin and showroom"], "twin.public", "A 3D model of the device that breathes on its own simulator."),
])
col(290, 220, YS, [
    (["Logins, permissions, audit"], "auth.staff_login", "Staff logins, patient links, who may see which patient, and the audit writer."),
    (["Safety rules"], "safety.red_flags", "Danger words get one fixed message. Medicine questions go to a person."),
    (["Breath model and coach"], "coach.classifier", "Labels and scores each breath. Fixed rules are the backup."),
    (["Prescription and doses"], "rx.patient_phone", "Holds the doctor's prescription and builds the patient's medicine schedule."),
    (["Comms simulators"], "comms.whatsapp", "WhatsApp and phone-call previews, and the escalation ladder."),
])
col(575, 210, YS, [
    (["Database"], "tenancy.hospitals", "Supabase (Postgres), or a local SQLite file on a laptop. Every row carries its hospital."),
    (["File storage"], "docs.vault", "Papers and prescription files, checked and cleaned, kept under random names."),
    (["Audit log"], "audit.log", "Who looked at or changed what, and when."),
    (["AI register"], "ai.register", "Every AI call as a reference with no content, plus the reviewer's decision."),
    (["Row security"], "db.rls_per_hospital", "The database itself keeping hospitals apart."),
])
col(830, 150, YS, [
    (["Gemini"], "rx.ai_read", "Optional drafts from sample documents. A person confirms every line."),
    (["Anthropic"], "ai.summary", "Daily summary text. A fixed template is the backup."),
    (["Sarvam voice"], "coach.voice", "Spoken coaching. Recorded clips and browser speech are the backups."),
    (["WhatsApp and calls"], "comms.whatsapp_real_send", "Twilio and Exotel. Real sending is not switched on."),
    (["Records network"], "docs.abdm_link", "ABDM link to the patient's health locker."),
])
# bottom-left: device link
for y, it in zip([446, 498, 550], [
    (["Clip-on unit over USB"], "device.usb", "The unit on the spirometer, wired to the phone."),
    (["Bluetooth link"], "device.ble", "Wireless pairing of the unit."),
    (["Breath simulator"], "coach.breath", "Stands in for the unit today."),
]):
    BOXES.append((20, y, 320, 40, *it))
# bottom-right: prescription path
for x, it in zip([392, 546, 700, 854], [
    (["Doctor types it", "in the hospital app"], "rx.manual", "No AI involved. This route always works."),
    (["Shows on the", "patient's phone"], "rx.patient_phone", "The doctor writes it; the patient sees every medicine at once."),
    (["Shown at the", "pharmacy counter"], "rx.pharmacy_screen", "A clear screen for the chemist instead of paper. Not yet tested with a real pharmacy."),
    (["Chemist scans", "a QR to check"], "rx.verify_qr", "Opens the hospital's copy to compare. No login; sample patients only."),
]):
    BOXES.append((x, 478, 130, 64, *it))

ZONES = [
    (10, 44, 240, 338, "BROWSER APPS (NO INSTALL)"),
    (275, 44, 250, 338, "SERVER (FASTAPI, ONE WEB SERVICE)"),
    (560, 44, 240, 338, "STORE"),
    (815, 44, 175, 338, "OUTSIDE SERVICES"),
    (10, 410, 340, 196, "AT HOME: THE DEVICE LINK"),
    (372, 410, 618, 196, "THE PRESCRIPTION PATH, DOCTOR TO CHEMIST"),
]

def status_of(key):
    f = features.get(key)
    assert f, key
    return f["status"]

def box_svg(b, standalone=False):
    x, y, w, h, lines, key, desc = b
    st = status_of(key)
    word = W[st]
    cx = x + w / 2
    n = len(lines)
    ty = y + (18 if n == 1 and h <= 48 else 20 if h == 40 else 22)
    if h == 40:
        ty = y + 17
    tspans = ""
    for i, ln in enumerate(lines):
        tspans += f'<text class="t" x="{cx}" y="{ty + i * 15}" text-anchor="middle">{escape(ln)}</text>'
    sy = y + h - 9
    name = features.get(key)["name"]
    return (f'<g class="box s-{st}" data-key="{key}" role="img" aria-label="{escape(" ".join(lines))}: {word}">'
            f'<title>{escape(name)}: {word}. {escape(desc)}</title>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>{tspans}'
            f'<text class="st" x="{cx}" y="{sy}" text-anchor="middle">{word}</text></g>')

def zones_svg():
    out = []
    for x, y, w, h, t in ZONES:
        out.append(f'<rect class="zone" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>'
                   f'<text class="zone-t" x="{x + 12}" y="{y + 20}">{escape(t)}</text>')
    return "".join(out)

def arrows_svg():
    a = []
    def line(d, dashed=False, label=None, lx=0, ly=0, anchor="middle"):
        a.append(f'<path class="link{" dashed" if dashed else ""}" d="{d}" marker-end="url(#ah)"/>')
        if label:
            a.append(f'<text class="lk" x="{lx}" y="{ly}" text-anchor="{anchor}">{escape(label)}</text>')
    line("M240 200 L273 200", label="HTTPS", lx=257, ly=190)
    line("M525 200 L558 200", label="reads, writes", lx=541, ly=190)
    # outside services bus over the top
    line("M400 44 L400 24 L902 24 L902 42", dashed=True, label="calls out, each with an offline backup", lx=650, ly=18)
    # device link up to the patient app
    line("M125 410 L125 384", dashed=True, label="breath readings", lx=135, ly=399, anchor="start")
    # prescription path
    for x1 in (522, 676, 830):
        line(f"M{x1} 510 L{x1 + 22} 510")
    # server <-> prescription path (doctor types it through the hospital app)
    return "".join(a)

DEFS = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
        '<path class="arrow" d="M0 0 L10 5 L0 10 z"/></marker></defs>')

def legend_svg(y=616):
    items = [("live", "Live"), ("simulated", "Simulated"), ("in_development", "In development"), ("planned", "Planned")]
    out = []
    x = 12
    for st, word in items:
        out.append(f'<g class="box s-{st}"><rect x="{x}" y="{y}" width="26" height="16" rx="4"/></g>'
                   f'<text class="lk" x="{x + 34}" y="{y + 12}" style="font-size:12px">{word}</text>')
        x += 34 + len(word) * 7 + 26
    return "".join(out)

def body(standalone):
    parts = [DEFS, zones_svg(), arrows_svg()]
    parts += [box_svg(b, standalone) for b in BOXES]
    if standalone:
        parts.append(legend_svg())
    return "".join(parts)

STYLE = """
.box rect{fill:#f8fafb;stroke:#c3ccd5;stroke-width:1.5}
.box.s-live rect{fill:#e8f5ec;stroke:#2e9d4e}
.box.s-simulated rect{fill:#e4f1f5;stroke:#0b6e8a}
.box.s-in_development rect{fill:#eef2f5;stroke:#5b6878;stroke-width:2}
.box.s-planned rect{fill:#ffffff;stroke:#c3ccd5;stroke-dasharray:6 4}
.box .t{fill:#101c27;font-size:13px;font-weight:650}
.box .st{fill:#445263;font-size:11px;font-weight:700}
.zone{fill:none;stroke:#c3ccd5;stroke-width:1;stroke-dasharray:3 4}
.zone-t{fill:#5b6878;font-size:11px;font-weight:700;letter-spacing:.04em}
.link{stroke:#5b6878;stroke-width:1.6;fill:none}.link.dashed{stroke-dasharray:5 4}
.arrow{fill:#5b6878}.lk{fill:#5b6878;font-size:10.5px}
@media (prefers-color-scheme:dark){
.bg{fill:#0d1319}
.box rect{fill:#1a2430;stroke:#3a4a5c}
.box.s-live rect{fill:#13301d;stroke:#4cc06d}
.box.s-simulated rect{fill:#12303d;stroke:#3fb4d4}
.box.s-in_development rect{fill:#202c39;stroke:#95a2b0}
.box.s-planned rect{fill:#151d26;stroke:#3a4a5c}
.box .t{fill:#e8eef4}.box .st{fill:#b4c0cc}
.zone{stroke:#283544}.zone-t,.lk{fill:#95a2b0}.link{stroke:#95a2b0}.arrow{fill:#95a2b0}
.title-t{fill:#e8eef4}}
.bg{fill:#f4f6f8}.title-t{fill:#101c27;font-size:18px;font-weight:700}
"""

def standalone_svg():
    inner = body(True)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 646" width="1000" height="646" '
            f'font-family="Segoe UI, Nirmala UI, Noto Sans, Arial, sans-serif" role="img" aria-labelledby="t d">\n'
            f'<title id="t">SpiroBuddy 2.0 architecture</title>\n'
            f'<desc id="d">Browser apps (patient app, family page, hospital software, public site, 3D twin) talk to one FastAPI web service, '
            f'which reads and writes the store (database, file storage, audit log, AI register) and calls outside services (Gemini, Anthropic, Sarvam, WhatsApp and calls, a records network), each with an offline backup. '
            f'The device link (USB in development, Bluetooth planned, a simulator in the demo) feeds the patient app. '
            f'The prescription path runs from the doctor to the patient\'s phone to the pharmacy counter. Every box carries its status word. Fake patients only. '
            f'Statuses as of the date this file was generated, from backend/app/features.py.</desc>\n'
            f'<style>{STYLE}</style>\n<rect class="bg" width="1000" height="646"/>\n{inner}\n</svg>\n')

def inline_svg():
    return (f'<svg class="arch-svg" viewBox="0 0 1000 620" role="group" aria-label="SpiroBuddy system diagram. The same boxes are listed below as a table." xmlns="http://www.w3.org/2000/svg">'
            f'{body(False)}</svg>')

def table_rows():
    rows = []
    for x, y, w, h, lines, key, desc in BOXES:
        rows.append(f'<tr><th scope="row" data-label="Box">{escape(" ".join(lines))}</th>'
                    f'<td data-label="What it does">{escape(desc)}</td>'
                    f'<td data-label="Status"><span data-feature="{key}"></span></td></tr>')
    return "\n".join(rows)

if __name__ == "__main__":
    (ROOT / "docs" / "hackathon" / "architecture_v2.svg").write_text(standalone_svg(), encoding="utf-8")
    page = ROOT / "web" / "architecture.html"
    html = page.read_text(encoding="utf-8")
    html = re.sub(r"<!--SVG-->.*?<!--/SVG-->", lambda m: "<!--SVG-->" + inline_svg() + "<!--/SVG-->", html, flags=re.S)
    html = re.sub(r"<!--ROWS-->.*?<!--/ROWS-->", lambda m: "<!--ROWS-->\n" + table_rows() + "\n<!--/ROWS-->", html, flags=re.S)
    page.write_text(html, encoding="utf-8")
    print("boxes", len(BOXES), {k: status_of(b[5]) for k, b in enumerate(BOXES)} if False else "")
