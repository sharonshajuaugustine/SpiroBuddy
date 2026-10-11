"""B7 - the public story site (landing, impact, trust, vision, architecture) and GET /api/impact.

Checks: every page opens with no login; /api/impact is public, numeric, never errors and gives the same
numbers to every viewer; the never-say words are absent from everything this builder wrote; every number in
the data files carries a source or a label; every status badge key exists in the registry; the founder's
framing is on the landing page; the architecture picture and its inline copy agree.
"""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

PAGES = ["/", "/index.html", "/impact.html", "/trust.html", "/vision.html", "/architecture.html"]
MY_FILES = [
    WEB / "index.html", WEB / "impact.html", WEB / "trust.html", WEB / "vision.html", WEB / "architecture.html",
    WEB / "data" / "impact.json", WEB / "data" / "trust.json", WEB / "css" / "public.css",
    *sorted((WEB / "js").glob("public-*.js")),
    ROOT / "docs" / "hackathon" / "architecture_v2.svg",
    ROOT / "docs" / "rebuild" / "story_integration.md",
]

# The spec requires this sentence word for word on /trust.html. It names a word from the never-say list
# only to deny it, so it is the single sentence taken out before the scan.
DISCLAIMER = "Designed to follow these guidelines. Not reviewed or approved by ICMR, an ethics committee or CDSCO."

NEVER = [
    r"approved", r"compliant", r"certified", r"validated", r"real[- ]time monitoring",
    r"prevents?\s+pneumonia", r"reduces?\s+readmission", r"abdm[- ]integrated", r"works with any spirometer",
    r"accurately", r"clinically proven", r"guarantee", r"\bfirst\b", r"\bcures?\b", r"\btaken\b",
]


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------------------------------- pages


@pytest.mark.parametrize("path", PAGES)
def test_every_public_page_opens_with_no_login(anon, path):
    r = anon.get(path)
    assert r.status_code == 200, path
    assert "text/html" in r.headers["content-type"]
    assert "SpiroBuddy" in r.text
    assert "/js/public-shell.js" in r.text and "/css/public.css" in r.text


@pytest.mark.parametrize("path", ["/data/impact.json", "/data/trust.json", "/css/public.css", "/js/public-shell.js",
                                  "/js/public-home.js", "/js/public-impact.js", "/js/public-trust.js",
                                  "/js/public-arch.js", "/showcase/videos/hero.mp4"])
def test_the_files_the_pages_load_are_served_without_a_login(anon, path):
    assert anon.get(path).status_code == 200, path


def test_data_files_are_valid_json():
    for name in ("impact.json", "trust.json"):
        assert isinstance(json.loads(_text(WEB / "data" / name)), dict)


# --------------------------------------------------------------------------------------- landing


def test_landing_leads_with_the_hospital_to_patient_link_and_the_two_pillars():
    html = _text(WEB / "index.html")
    assert "stays connected to the patient at home" in html and "Every breath, coached and counted." in html
    for key in ("rx.patient_phone", "rx.pharmacy_screen", "rx.verify_qr", "coach.breath", "device.usb"):
        assert f'data-feature="{key}"' in html, key
    assert "no paper is needed" in html.lower()
    assert "pharmacy" in html.lower()
    # the app is not pitched as "AI reads prescription photos"
    assert "rx.ai_read" not in html and "rx.patient_upload" not in html
    assert "reads prescription" not in html.lower() and "decodes" not in html.lower()


def test_landing_links_and_hero_follow_the_founder_overrides():
    html = _text(WEB / "index.html")
    assert 'href="/login.html?next=/dashboard.html"' in html
    assert 'href="/app.html?id=1"' in html
    assert "Open the patient app</a>" in html and "Hospital login (sample logins shown)" in html
    assert "/showcase/videos/hero.mp4" in html and "Open the 3D showroom" in html and 'href="/showcase/"' in html
    assert "<iframe" not in html and "twin.html" not in html          # no twin page tonight
    assert "muted" in html and "playsinline" in html and "loop" in html
    assert "autoplay" not in html.lower()                              # script starts it, unless reduced motion
    assert "prefers-reduced-motion" in _text(WEB / "js" / "public-home.js")
    assert "Illustrative personas" in html


def test_footer_and_header_text():
    js = _text(WEB / "js" / "public-shell.js")
    assert "Sample patients · not a medical device · not for clinical use" in js
    for label in ("Home", "Impact", "Trust", "Vision", "Architecture", "3D showroom", "Hospital login", "Patient app</a>"):
        assert label in js, label
    assert "/twin.html" not in js


# --------------------------------------------------------------------------------------- vision


def test_vision_has_the_required_sections():
    html = _text(WEB / "vision.html")
    assert "Scale and cost" in html
    assert "Works beside your hospital's software" in html
    assert "Drug-interaction checks – deliberately not built (would be clinical decision support)" in html
    assert 'data-feature="rx.interaction_checks"' in html
    for text in ("Stage 0", "Stage 1", "Stage 2", "Stage 3", "Stage 4", "Level 0", "Level 1", "Level 2", "Level 3",
                 "Today one web service and one database run this site, with sample patients.",
                 "Planned growth is staged: one pilot hospital, ten, a hundred, then state programmes.",
                 "Each patient episode should cost five to seven hundred rupees, an estimate; our planned price is about one thousand.",
                 "0-3 months", "3-12 months", "12-24 months", "B1-13"):
        assert text in html, text
    # only Stage 0 is described as running today; Stages 1-4 are Planned
    stage0 = html.split("Stage 0")[1].split("Stage 1")[0]
    assert "Running today" in stage0
    for n in ("1", "2", "3", "4"):
        block = html.split(f"Stage {n} ·")[1].split("</header>")[0]
        assert "Planned" in block, n
        assert "Running today" not in block


# --------------------------------------------------------------------------------------- trust


def test_trust_has_the_verbatim_texts_and_the_demo_note():
    html = _text(WEB / "trust.html")
    assert DISCLAIMER in html
    assert ("In the demo only sample prescriptions are sent to Google's Gemini API. Real-patient use needs ethics "
            "approval, a paid or enterprise data agreement and a data-residency review (Planned).") in html
    assert "None of these steps has been done: a real pilot is Planned." in html
    data = json.loads(_text(WEB / "data" / "trust.json"))
    assert len(data["safe_rules"]) == 10 and len(data["checklist"]) == 14
    names = " ".join(g["name"] for g in data["rule_groups"])
    for word in ("ICMR National Ethical Guidelines 2017", "ICMR Guidelines on AI in health 2023",
                 "Digital Personal Data Protection Act 2023", "Telemedicine Practice Guidelines 2020"):
        assert word in names, word
    for g in data["rule_groups"]:
        assert g["source"]
        for row in g["rows"]:
            assert row["rule"] and row["does"] and row["keys"], row


# --------------------------------------------------------------------------------------- honesty: sources, labels, badges


def test_every_number_in_the_data_files_has_a_source_or_a_label():
    d = json.loads(_text(WEB / "data" / "impact.json"))
    for s in d["segments"]:
        assert s["source"] and s["key"]
    for b in d["buyers"]:
        assert b["source"]
    for c in d["market"]["counted"]:
        assert c["label"] == "counted" and c["source"]
    for s in d["market"]["steps"]:
        assert s["label"] in ("estimate", "assumption") and s["source"]
    funnel = d["funnel"]
    assert funnel["tag"] == "Shot list · shot 13 · assumptions"
    assert len(funnel["steps"]) == 6
    for st in funnel["steps"]:
        assert st["label"] in ("estimate", "assumption", "target")
    assert "A pilot of 30-50 patients measures every step" in funnel["footnote"]
    for s in d["calculator"]["sliders"]:
        assert s["source"] and s["min"] <= s["value"] <= s["max"]
    assert {s["id"] for s in d["calculator"]["sliders"]} == {"hospitals", "eligible", "join", "d7", "d14", "family"}
    for f in d["calculator"]["fixed"]:
        assert f["label"] in ("estimate", "assumption", "target") and f["source"]
    assert d["sdg"][0]["target"] == "3.8" and d["sdg"][0]["main"]
    # the market range the spec quotes
    vals = " ".join(s["low"] + s["mid"] + s["high"] for s in d["market"]["steps"])
    assert "₹24.5 crore" in vals and "₹147 crore" in vals


def test_the_market_and_funnel_numbers_are_copied_exactly():
    d = json.loads(_text(WEB / "data" / "impact.json"))
    funnel = " ".join(s["number"] for s in d["funnel"]["steps"])
    for piece in ("about 50 eligible patients", "40 join (8 in 10)", "24 families opt in (6 in 10 of those who join)",
                  "36 do a home session on day 1 (9 in 10)", "34 on day 3 · 30 on day 7 · 26 on day 14 (85% · 75% · 65%)",
                  "about 58% of due sessions done", "1 pilot hospital in 3 goes on to pay"):
        assert piece in funnel, piece
    assert "about 49 lakh" in json.dumps(d["market"], ensure_ascii=False)


def test_rupee_figures_on_the_vision_page_are_labelled():
    html = _text(WEB / "vision.html")
    blocks = re.split(r"</dd>|</li>|</p>|</td>|</h3>", html)
    bad = [b[-160:].strip() for b in blocks if "₹" in b and not re.search(
        r'lbl estimate|lbl assumption|lbl target|class="src"', b)]
    assert not bad, bad


def test_no_prices_on_the_pages_that_have_no_business_content():
    for name in ("index.html", "trust.html", "architecture.html"):
        assert "₹" not in _text(WEB / name), name
    assert "₹" not in _text(WEB / "data" / "trust.json")


def test_every_status_badge_key_exists_in_the_registry():
    from backend.app import features
    used = set()
    for p in MY_FILES:
        if p.suffix in (".html", ".js"):
            used |= set(re.findall(r"data-feature=[\"']([a-z0-9_]+(?:\.[a-z0-9_]+)+)[\"']", _text(p)))
    imp = json.loads(_text(WEB / "data" / "impact.json"))
    used |= {s["key"] for s in imp["segments"]}
    tr = json.loads(_text(WEB / "data" / "trust.json"))
    for g in tr["rule_groups"]:
        for row in g["rows"]:
            used |= set(row["keys"])
    for pt in tr["gemini_points"]:
        used |= set(pt.get("keys", []))
    svg_keys = set(re.findall(r'data-key="([a-z0-9_.]+)"', _text(WEB / "architecture.html")))
    used |= svg_keys
    assert len(used) > 25
    unknown = sorted(k for k in used if features.get(k) is None)
    assert not unknown, unknown
    # the keys the integration note asks the lead to flip are each shown on a page of this site
    for key in ("public.impact", "impact.calculator", "impact.metrics", "public.trust", "public.vision",
                "public.architecture", "segment.post_surgery"):
        assert key in used, key


def test_no_status_word_is_written_into_a_page_by_hand():
    """Badges and legends come from the registry; the landing, impact, trust and architecture pages carry no
    hand-written 'Live' badge. (Vision's plain stage/level notes are text, never a badge class.)"""
    for name in ("index.html", "impact.html", "trust.html", "architecture.html", "vision.html"):
        html = _text(WEB / name)
        assert not re.search(r'class="fbadge', html), name
    for p in sorted((WEB / "js").glob("public-*.js")):
        assert not re.search(r">\s*Live\s*<", _text(p)), p.name


def test_never_say_words_are_absent():
    bad = []
    for p in MY_FILES:
        if not p.exists():
            continue
        text = _text(p).replace(DISCLAIMER, "")
        for pat in NEVER:
            for m in re.finditer(pat, text, re.I):
                bad.append((p.name, m.group(0), text[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")))
    assert not bad, bad[:10]


def test_features_never_say_regex_also_finds_nothing():
    from backend.app import features
    for p in MY_FILES:
        if p.exists():
            assert not features.NEVER_SAY.search(_text(p).replace(DISCLAIMER, "")), p.name


# --------------------------------------------------------------------------------------- architecture


def test_architecture_svg_is_well_formed_and_matches_the_inline_copy():
    svg = ROOT / "docs" / "hackathon" / "architecture_v2.svg"
    root = ET.fromstring(_text(svg))
    ns = "{http://www.w3.org/2000/svg}"
    boxes = [g for g in root.iter(f"{ns}g") if g.get("data-key")]
    inline = re.findall(r'<g class="box s-(\w+)" data-key="([a-z0-9_.]+)"', _text(WEB / "architecture.html"))
    assert len(boxes) == len(inline) >= 20
    import warnings
    from backend.app import features
    words = set(features.STATUS_LABEL.values())
    for g in boxes:
        key = g.get("data-key")
        assert features.get(key), key
        label = features.STATUS_LABEL[features.get(key)["status"]]
        word = g.get("aria-label").rsplit(": ", 1)[1]
        assert word in words, (key, g.get("aria-label"))
        if word != label:   # a status was flipped after the file was drawn: the page fixes itself, the file does not
            warnings.warn(f"architecture_v2.svg shows {word} for {key}, the registry says {label}: "
                          "run docs/rebuild/story_arch_gen.py to redraw it")
    text = _text(svg)
    for word in ("Clip-on unit over USB", "Bluetooth link", "Gemini", "Anthropic", "Sarvam voice", "WhatsApp and calls",
                 "Database", "File storage", "Comms simulators", "Doctor types it"):
        assert word in text, word
    assert {k for _, k in inline} >= {"device.usb", "device.ble", "coach.breath", "rx.patient_phone", "rx.pharmacy_screen"}
    assert (WEB / "architecture.html").read_text(encoding="utf-8").count("arch-svg") >= 1
    assert (ROOT / "docs" / "hackathon" / "architecture.svg").exists()      # the old picture is untouched


# --------------------------------------------------------------------------------------- GET /api/impact

NUMERIC = ("patients_coached", "sessions_completed", "doses_reported_pct", "follow_ups_kept_pct",
           "families_informed", "ai_lines_edited_pct", "ai_drafts", "ai_rejected_pct")


def test_impact_is_public_numeric_and_labelled(anon):
    from backend.app import routes_public
    routes_public.clear_cache()
    r = anon.get("/api/impact")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["label"] == "sample patients"
    for k in NUMERIC:
        assert isinstance(body[k], (int, float)) and not isinstance(body[k], bool), k
        assert body[k] >= 0
    for k in ("doses_reported_pct", "follow_ups_kept_pct", "ai_lines_edited_pct", "ai_rejected_pct"):
        assert 0 <= body[k] <= 100
    assert "Dawnlight General Hospital" in body["hospital"]
    assert "T" in body["as_of"] and ("+05:30" in body["as_of"])
    # nothing that identifies a person
    flat = json.dumps(body)
    assert "phone" not in flat and "@" not in flat


def test_impact_counts_the_demo_data(client):
    from backend.app import routes_public
    routes_public.clear_cache()
    body = client.get("/api/impact").json()
    assert body["patients_in_programme"] >= 7              # the seeded fake patients
    assert body["sessions_completed"] > 0 and body["patients_coached"] > 0
    assert body["sessions_due_today"] >= 0


def test_impact_is_the_same_for_every_viewer(anon, client, login_as):
    from backend.app import routes_public
    seen = []
    for who in (anon, client, login_as("anjali@demo-general.example"), login_as("admin@demo-riverside.example")):
        routes_public.clear_cache()
        body = who.get("/api/impact").json()
        body.pop("as_of")
        seen.append(body)
    assert all(b == seen[0] for b in seen), seen


def test_impact_never_errors_when_the_store_is_missing(anon, monkeypatch):
    from backend.app import routes_public, service
    routes_public.clear_cache()

    def boom():
        raise RuntimeError("store is down")
    monkeypatch.setattr(service, "store", boom)
    r = anon.get("/api/impact")
    assert r.status_code == 200
    body = r.json()
    assert body["label"] == "sample patients"
    for k in NUMERIC:
        assert body[k] == 0, k
    routes_public.clear_cache()


def test_impact_never_errors_when_a_table_is_missing(anon, monkeypatch):
    from backend.app import routes_public
    routes_public.clear_cache()
    real = routes_public._rows

    def no_v2_tables(table, filters=(), columns="*"):
        if table in ("dose_events", "appointments", "ai_events", "guardians"):
            return []
        return real(table, filters, columns)
    monkeypatch.setattr(routes_public, "_rows", no_v2_tables)
    body = anon.get("/api/impact").json()
    assert body["doses_reported_pct"] == 0 and body["follow_ups_kept_pct"] == 0 and body["families_informed"] == 0
    assert body["sessions_completed"] > 0
    routes_public.clear_cache()


def test_impact_falls_back_to_zeros_if_the_calculation_itself_fails(anon, monkeypatch):
    from backend.app import routes_public
    routes_public.clear_cache()

    def boom():
        raise ValueError("bad row")
    monkeypatch.setattr(routes_public, "compute_impact", boom)
    r = anon.get("/api/impact")
    assert r.status_code == 200 and r.json()["patients_coached"] == 0
    routes_public.clear_cache()


def test_impact_counts_reported_doses_missed_follow_ups_and_ai_review(anon, client, monkeypatch):
    """Percentages come from the rows: 3 reported + 1 missed = 75%; 1 attended + 1 no-show = 50%;
    one consented guardian counts as one family; AI lines edited 1 of 4 = 25%, 1 of 2 drafts rejected."""
    from backend.app import routes_public

    def fake_rows(table, filters=(), columns="*"):
        pat = [{"id": 1, "hospital_id": 1}, {"id": 2, "hospital_id": 1}, {"id": 100, "hospital_id": 2}]
        data = {
            "patients": pat,
            "sessions": [{"patient_id": 1}, {"patient_id": 1}, {"patient_id": 2}, {"patient_id": 100}],
            "dose_events": [{"patient_id": 1, "status": "reported_taken"}] * 3
            + [{"patient_id": 1, "status": "missed"}, {"patient_id": 100, "status": "missed"},
               {"patient_id": 2, "status": "upcoming"}],
            "appointments": [{"patient_id": 1, "status": "attended"}, {"patient_id": 2, "status": "no_show"},
                             {"patient_id": 2, "status": "confirmed"}],
            "guardians": [{"patient_id": 1, "consent": 1}, {"patient_id": 1, "consent": 1},
                          {"patient_id": 2, "consent": 0}],
        }
        return data.get(table, [])
    monkeypatch.setattr(routes_public, "_rows", fake_rows)
    monkeypatch.setattr(routes_public, "_ai_stats", lambda: {
        "drafts": 2, "reviewed": 2, "lines_total": 4, "lines_edited_pct": 25.0, "rejected_pct": 50.0})
    monkeypatch.setattr(routes_public, "_sessions_today", lambda pids: (3, 8))
    routes_public.clear_cache()
    body = anon.get("/api/impact").json()
    assert body["patients_in_programme"] == 2                  # the other hospital's patient never counts
    assert body["patients_coached"] == 2 and body["sessions_completed"] == 3
    assert body["doses_reported_pct"] == 75.0 and body["doses_reported"] == 3 and body["doses_missed"] == 1
    assert body["follow_ups_kept_pct"] == 50.0
    assert body["families_informed"] == 1
    assert body["ai_drafts"] == 2 and body["ai_lines_edited_pct"] == 25.0 and body["ai_rejected_pct"] == 50.0
    assert body["sessions_done_today"] == 3 and body["sessions_due_today"] == 8
    assert body["sessions_done_of_due_pct"] == 37.5
    routes_public.clear_cache()
