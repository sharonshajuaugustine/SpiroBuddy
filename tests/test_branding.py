"""Branding lite: each hospital's own app name + logo inside the patient app (docs/plan/12 section 2).

Admin of a hospital saves a name, a short name, an accent colour and a logo; the patients (and
staff) of THAT hospital read it; nobody else does. Fixed things (the "with SpiroBuddy" line, the
safety messages, the status labels) cannot be changed through the API.
"""
import io
import re
from pathlib import Path

import pytest

from backend.app import branding

ROOT = Path(__file__).resolve().parents[1]
DOCTOR = "meera.nair@demo-general.example"
NURSE = "anjali@demo-general.example"
RIVER_ADMIN = "admin@demo-riverside.example"
WRITE = "/api/admin/branding"
GOOD = {"display_name": "Test Care", "short_name": "TestCare", "accent": "#1b5e9e"}


def _png(size=(64, 64), colour=(200, 40, 40)) -> bytes:
    from PIL import Image
    buf = io.BytesIO()
    Image.new("RGB", size, colour).save(buf, "PNG")
    return buf.getvalue()


def _reset_branding(hospital_id: int) -> None:
    """Back to 'nothing saved' for a test that needs the defaults."""
    from backend.app import authz
    branding.clear_logo(hospital_id)
    st = authz.ident()
    rows = st.select("hospitals", [("id", "eq", hospital_id)], columns="settings", limit=1)
    s = dict(rows[0].get("settings") or {})
    s.pop("branding", None)
    st.update("hospitals", [("id", "eq", hospital_id)], {"settings": s})


@pytest.fixture(scope="module", autouse=True)
def _restore_demo_after_this_file(client):
    """The demo data (and both demo hospitals' seeded branding) is put back when this file is done."""
    yield
    client.post("/api/demo/reset")


@pytest.fixture()
def clean(client):
    """The demo admin's client. Each test sets the branding it needs itself."""
    return client


# ----------------------------------------------------------------------------- defaults

def test_defaults_when_nothing_is_saved(clean, patient_client):
    _reset_branding(1)
    got = patient_client(1).get("/api/me/branding")
    assert got.status_code == 200, got.text
    b = got.json()
    assert b["display_name"].startswith("Dawnlight General Hospital")
    assert b["accent"] == branding.DEFAULT_ACCENT
    assert b["logo_url"] is None
    assert b["powered_by"] == "with SpiroBuddy"
    # and no logo bytes either
    assert patient_client(1).get("/api/me/branding/logo").status_code == 404


def test_seed_gives_both_demo_hospitals_a_name_and_a_logo(client, patient_client, riverside_patient):
    client.post("/api/demo/reset")
    a = patient_client(1).get("/api/me/branding").json()
    b = patient_client(riverside_patient).get("/api/me/branding").json()
    assert a["display_name"] and b["display_name"] and a["display_name"] != b["display_name"]
    assert a["logo_url"] and b["logo_url"]
    logo = patient_client(1).get("/api/me/branding/logo")
    assert logo.status_code == 200 and logo.headers["content-type"] == "image/png"
    assert logo.content.startswith(b"\x89PNG")


# ----------------------------------------------------------------------------- admin saves, patient sees

def test_admin_saves_and_the_patient_of_that_hospital_sees_it(clean, patient_client):
    r = clean.put(WRITE, json=GOOD)
    assert r.status_code == 200, r.text
    assert r.json()["display_name"] == "Test Care"
    seen = patient_client(1).get("/api/me/branding").json()
    assert seen["display_name"] == "Test Care"
    assert seen["short_name"] == "TestCare"
    assert seen["accent"] == "#1b5e9e"
    assert seen["powered_by"] == "with SpiroBuddy"
    # a staff member of the same hospital reads it on the staff route
    nurse = clean.get("/api/branding/mine").json()
    assert nurse["display_name"] == "Test Care"


def test_get_admin_branding_has_limits_and_what_is_fixed(clean):
    r = clean.get(WRITE)
    assert r.status_code == 200, r.text
    j = r.json()
    assert j["limits"]["logo_max_bytes"] == 512 * 1024
    assert any("with SpiroBuddy" in line for line in j["fixed"])
    assert j["defaults"]["accent"] == branding.DEFAULT_ACCENT


def test_other_hospitals_people_never_see_it(clean, login_as, patient_client, riverside_patient):
    clean.put(WRITE, json={"display_name": "Only Ours Care", "short_name": "Ours",
                           "accent": "#0b6e8a"})
    # the patient and the admin of the OTHER hospital
    other_patient = patient_client(riverside_patient).get("/api/me/branding").json()
    assert other_patient["display_name"] != "Only Ours Care"
    other_admin = login_as(RIVER_ADMIN)
    assert other_admin.get("/api/branding/mine").json()["display_name"] != "Only Ours Care"
    assert other_admin.get(WRITE).json()["display_name"] != "Only Ours Care"
    # ... and a save by the other admin changes only the other hospital
    r = other_admin.put(WRITE, json={"display_name": "River Test Care"})
    assert r.status_code == 200, r.text
    assert patient_client(1).get("/api/me/branding").json()["display_name"] == "Only Ours Care"
    assert patient_client(riverside_patient).get("/api/me/branding").json()["display_name"] == "River Test Care"


def test_a_partial_save_keeps_the_other_fields(clean, patient_client):
    clean.put(WRITE, json=GOOD)
    clean.put(WRITE, json={"accent": "#8e3b5f"})
    b = patient_client(1).get("/api/me/branding").json()
    assert b["display_name"] == "Test Care" and b["accent"] == "#8e3b5f"


# ----------------------------------------------------------------------------- who may save

def test_doctor_and_nurse_cannot_save(clean, login_as):
    for email in (DOCTOR, NURSE):
        c = login_as(email)
        assert c.put(WRITE, json=GOOD).status_code == 403, email
        assert c.get(WRITE).status_code == 403, email
        assert c.post(WRITE + "/logo", files={"file": ("a.png", _png(), "image/png")}).status_code == 403
        assert c.delete(WRITE + "/logo").status_code == 403
    # ... but they may READ their own hospital's branding (they work in it)
    assert login_as(DOCTOR).get("/api/branding/mine").status_code == 200


def test_a_patient_cannot_save(clean, patient_client):
    p = patient_client(1)
    assert p.put(WRITE, json=GOOD).status_code in (401, 403)
    assert p.post(WRITE + "/logo", files={"file": ("a.png", _png(), "image/png")}).status_code in (401, 403)
    assert p.delete(WRITE + "/logo").status_code in (401, 403)


def test_staff_read_the_staff_path_and_patients_the_me_path(clean, login_as, patient_client):
    """The middleware gives /api/me/* to patient sessions only, so staff have their own read path."""
    staff = login_as(NURSE)
    assert staff.get("/api/me/branding").status_code == 401
    assert staff.get("/api/branding/mine").status_code == 200
    assert staff.get("/api/branding/mine").json()["powered_by"] == "with SpiroBuddy"
    patient = patient_client(1)
    assert patient.get("/api/me/branding").status_code == 200
    assert patient.get("/api/branding/mine").status_code == 401


def test_nobody_logged_in_cannot_read_or_save(anon):
    assert anon.put(WRITE, json=GOOD).status_code == 401
    assert anon.get(WRITE).status_code == 401
    assert anon.get("/api/me/branding").status_code == 401
    assert anon.get("/api/branding/mine").status_code == 401
    assert anon.get("/api/me/branding/logo").status_code == 401


# ----------------------------------------------------------------------------- bad values

@pytest.mark.parametrize("accent", ["red", "#12", "#gggggg", "0b6e8a", "#0b6e8a00", "", None, 7])
def test_a_bad_colour_is_refused(clean, accent):
    r = clean.put(WRITE, json={"accent": accent})
    assert r.status_code == 400, r.text


@pytest.mark.parametrize("accent,word", [
    ("#ffffff", "white"),            # fades into the light screen
    ("#fafafa", "white"),
    ("#000000", "black"),            # fades into the dark screen
    ("#050505", "black"),
    ("#808080", "read"),             # neither white nor dark writing is clear on mid-grey
])
def test_a_low_contrast_colour_is_refused_with_a_plain_message(clean, accent, word):
    r = clean.put(WRITE, json={"accent": accent})
    assert r.status_code == 400, r.text
    assert word in r.json().get("detail", r.text).lower()


def test_strong_colours_in_both_themes_are_accepted(clean):
    for ok in ("#0b6e8a", "#1b5e9e", "#8e3b5f", "#b3261e", "#2e7d32"):
        assert clean.put(WRITE, json={"accent": ok}).status_code == 200, ok


def test_contrast_helper_numbers():
    assert branding.contrast("#000000", "#ffffff") == pytest.approx(21.0, rel=0.01)
    assert branding.check_accent("#1B5E9E")[0] == "#1b5e9e"
    with pytest.raises(ValueError):
        branding.check_accent("#ffffff")


@pytest.mark.parametrize("body", [
    {"display_name": ""}, {"display_name": "A"}, {"display_name": "x" * 41},
    {"short_name": "x"}, {"short_name": "y" * 15}, {"display_name": "<b>Hi</b>"},
    {"display_name": 5}, {"short_name": None},
])
def test_bad_names_are_refused(clean, body):
    assert clean.put(WRITE, json=body).status_code == 400, body


def test_the_fixed_line_and_other_settings_cannot_be_changed(clean, patient_client):
    for body in ({"powered_by": "by Someone Else"}, {"logo_path": "brand/x.png"},
                 {"safety_message": "x"}, {"status_labels": {}}):
        r = clean.put(WRITE, json=body)
        assert r.status_code == 400, body
    clean.put(WRITE, json=GOOD)
    assert patient_client(1).get("/api/me/branding").json()["powered_by"] == "with SpiroBuddy"
    assert branding.POWERED_BY == "with SpiroBuddy"


def test_the_other_hospital_settings_survive_a_save(clean):
    from backend.app import authz
    before = authz.hospital_settings(1)
    clean.put(WRITE, json=GOOD)
    after = authz.hospital_settings(1)
    for k, v in before.items():
        if k != "branding":
            assert after[k] == v, k


# ----------------------------------------------------------------------------- logo upload

def _upload(c, data, name="logo.png", mime="image/png"):
    return c.post(WRITE + "/logo", files={"file": (name, data, mime)})


def test_a_png_logo_is_accepted_and_served_to_the_own_hospital_only(clean, patient_client, login_as,
                                                                    riverside_patient):
    r = _upload(clean, _png((900, 300)))
    assert r.status_code == 200, r.text
    assert r.json()["logo_url"]
    mine = patient_client(1).get("/api/me/branding/logo")
    assert mine.status_code == 200 and mine.headers["content-type"] == "image/png"
    from PIL import Image
    img = Image.open(io.BytesIO(mine.content))
    assert max(img.size) <= 512                      # scaled down
    # staff of the same hospital get the same bytes on the staff route
    assert login_as(NURSE).get("/api/branding/mine/logo").content == mine.content
    # the other hospital's patient and admin get THEIR logo (or none), never ours
    theirs = patient_client(riverside_patient).get("/api/me/branding/logo")
    assert theirs.status_code in (200, 404)
    if theirs.status_code == 200:
        assert theirs.content != mine.content
    other = login_as(RIVER_ADMIN).get("/api/branding/mine/logo")
    assert other.status_code in (200, 404)
    if other.status_code == 200:
        assert other.content != mine.content


def test_jpeg_and_webp_are_accepted(clean):
    from PIL import Image
    for fmt, mime in (("JPEG", "image/jpeg"), ("WEBP", "image/webp")):
        buf = io.BytesIO()
        Image.new("RGB", (80, 80), (10, 90, 140)).save(buf, fmt)
        assert _upload(clean, buf.getvalue(), "l." + fmt.lower(), mime).status_code == 200, fmt


def test_svg_and_other_files_are_refused(clean):
    svg = b'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"><script>alert(1)</script></svg>'
    assert _upload(clean, svg, "logo.svg", "image/svg+xml").status_code == 400
    assert _upload(clean, svg, "logo.png", "image/png").status_code == 400       # SVG renamed
    assert _upload(clean, b"%PDF-1.4\n%%EOF", "a.pdf", "application/pdf").status_code == 400
    assert _upload(clean, b"<html><script>1</script></html>", "a.png", "image/png").status_code == 400
    assert _upload(clean, b"plain text", "a.txt", "text/plain").status_code == 400
    assert _upload(clean, b"", "a.png", "image/png").status_code == 400


def test_a_big_upload_is_refused(clean):
    big = _png((1600, 1600))
    from PIL import Image
    import os
    buf = io.BytesIO()
    Image.frombytes("RGB", (900, 900), os.urandom(900 * 900 * 3)).save(buf, "PNG")     # noise: ~2 MB
    assert len(buf.getvalue()) > branding.MAX_LOGO_BYTES
    r = _upload(clean, buf.getvalue())
    assert r.status_code == 400 and "512" in r.text
    assert big  # (a plain large picture compresses well and is scaled down instead)


def test_a_picture_with_too_many_pixels_is_refused_before_it_is_decoded(clean):
    from PIL import Image
    buf = io.BytesIO()
    Image.new("L", (4000, 4000), 7).save(buf, "PNG")        # a few KB of file, 16 million pixels
    assert len(buf.getvalue()) < branding.MAX_LOGO_BYTES
    r = _upload(clean, buf.getvalue(), "wide.png", "image/png")
    assert r.status_code == 400 and "too large" in r.text


def test_logo_refusals_talk_about_logos_not_photos_or_pdfs(clean):
    for data, name, mime in ((b"%PDF-1.4\n%%EOF", "a.pdf", "application/pdf"),
                             (b"plain text", "a.txt", "text/plain"),
                             (b"\x89PNG\r\n\x1a\n" + b"junk" * 50, "a.png", "image/png")):
        r = _upload(clean, data, name, mime)
        assert r.status_code == 400
        assert "photo" not in r.text.lower() and "pdf" not in r.text.lower(), r.text


def test_a_logo_has_no_metadata_after_upload(clean, patient_client):
    from PIL import Image
    img = Image.new("RGB", (64, 64), (30, 30, 30))
    exif = Image.Exif()
    exif[0x010E] = "SECRET-DESCRIPTION"
    buf = io.BytesIO()
    img.save(buf, "JPEG", exif=exif)
    assert b"SECRET-DESCRIPTION" in buf.getvalue()
    assert _upload(clean, buf.getvalue(), "l.jpg", "image/jpeg").status_code == 200
    got = patient_client(1).get("/api/me/branding/logo").content
    assert b"SECRET-DESCRIPTION" not in got


def test_removing_the_logo(clean, patient_client):
    _upload(clean, _png())
    r = clean.delete(WRITE + "/logo")
    assert r.status_code == 200 and r.json()["logo_url"] is None
    assert patient_client(1).get("/api/me/branding/logo").status_code == 404


def test_a_new_logo_changes_the_logo_address(clean):
    a = _upload(clean, _png(colour=(1, 2, 3))).json()["logo_url"]
    b = _upload(clean, _png(colour=(200, 100, 3))).json()["logo_url"]
    assert a and b and a != b


# ----------------------------------------------------------------------------- audit

def test_every_write_leaves_an_audit_row(clean):
    from backend.app import authz

    def rows(action):
        return [r for r in authz.ident().select("audit_events", [("action", "eq", action)])
                if r.get("hospital_id") == 1]
    n_up, n_logo, n_rm = (len(rows(a)) for a in ("branding.update", "branding.logo_upload",
                                                  "branding.logo_remove"))
    assert clean.put(WRITE, json=GOOD).status_code == 200
    assert _upload(clean, _png()).status_code == 200
    assert clean.delete(WRITE + "/logo").status_code == 200
    assert len(rows("branding.update")) == n_up + 1
    assert len(rows("branding.logo_upload")) == n_logo + 1
    assert len(rows("branding.logo_remove")) == n_rm + 1
    last = rows("branding.update")[-1]
    assert last["actor_role"] == "admin" and last["detail"]["display_name"] == "Test Care"


# ----------------------------------------------------------------------------- pages

PAGES = ["web/branding.html", "web/js/branding-admin.js", "web/js/branding.js", "web/css/branding.css"]
BANNED = ["approved", "compliant", "certified", "validated", "real-time monitoring",
          "prevents pneumonia", "reduces readmission", "abdm-integrated", "works with any spirometer",
          "accurately", "clinically proven", "guarantee", "first", "cure", "no such software exists",
          "used during covid"]
MONEY = ["price", "pricing", "payment", "invoice", "billing", "insurance", "rupee", "₹", "refund",
         "subscription", "checkout", "discount"]


def _text(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_the_pages_exist_and_say_nothing_banned_or_about_money():
    for rel in PAGES:
        low = _text(rel).lower()
        for word in BANNED:
            assert not re.search(r"\b" + re.escape(word), low), f"{rel}: banned word {word!r}"
        for word in MONEY:
            assert word not in low, f"{rel}: money word {word!r}"
    for rel in ("backend/app/branding.py", "backend/app/routes_admin.py", "backend/app/seed_branding.py"):
        low = _text(rel).lower()
        for word in MONEY + ["secure ", "safe "]:
            assert word not in low.replace("unsafe", ""), f"{rel}: {word!r}"


def test_the_admin_page_has_the_badge_and_the_fixed_line_note():
    html = _text("web/branding.html")
    assert 'data-feature="hospital.branding"' in html
    assert "with SpiroBuddy" in html
    low = html.lower()
    assert "safety messages" in low and "status labels" in low
    assert 'src="js/icons.js"' in html and 'src="js/api.js"' in html and 'src="js/ui.js"' in html
    assert "Live" not in html          # badges come only from the registry


def test_the_staff_page_list_knows_the_new_page():
    assert "'/branding.html'" in _text("web/js/api.js")


def test_the_patient_pages_load_the_brand_strip_and_nothing_else_changed_much():
    for rel in ("web/app.html", "web/meds.html"):
        html = _text(rel)
        assert 'id="brand-slot"' in html, rel
        assert html.count("js/branding.js") == 1, rel          # ONE script tag, nothing else added


def test_branding_js_fails_silently_and_only_paints_the_strip():
    js = _text("web/js/branding.js")
    assert "/api/me/branding" in js and "catch" in js
    css = _text("web/css/branding.css")
    # the accent is a custom property used on the strip only
    assert "--brand-accent" in css
    for forbidden in (".btn", "button", ".chip", ".alert", ".banner", "--red", "--amber", "--green"):
        assert forbidden not in css, forbidden


def test_the_admin_page_is_served_and_the_scripts_load(client):
    for path in ("/branding.html", "/js/branding.js", "/js/branding-admin.js", "/css/branding.css"):
        assert client.get(path).status_code == 200, path


def test_the_feature_badge_is_in_the_registry(client):
    feats = client.get("/api/features").json()
    items = feats.get("features", feats) if isinstance(feats, dict) else feats
    found = next((f for f in items if f.get("key") == "hospital.branding"), None)
    assert found is not None
    assert found.get("status") in ("planned", "in_development", "simulated", "live")
