"""SpiroBuddy 2.0 logins and permissions (Contract E, docs/REBUILD_PLAN.md §3.3-§3.5, spec §6):
login, lockout, expiry, logout, password change, CSRF, hidden docs, training off, doctor signup,
nurse keys (create, redeem, scope, revoke, expire, max uses), patient-app sessions, the
permission matrix, the demo rules and "no secret ever reaches the audit log".

Fictional accounts only (backend/app/seed_auth.py). No network, no real services.
"""
import json

import pytest

ADMIN = "admin@demo-general.example"
MEERA = "meera.nair@demo-general.example"      # patients 1, 2, 4, 6
KABIR = "kabir.rao@demo-general.example"       # patients 3, 5, 7
ANJALI = "anjali@demo-general.example"         # nurse: all of Dr. Meera's patients, every permission
THOMAS = "thomas@demo-general.example"         # nurse: patients 3 and 5, view + acknowledge alerts
RIVERSIDE = "admin@demo-riverside.example"
NEW_PASSWORD = "a-brand-new-pass-77"


@pytest.fixture(autouse=True)
def _no_rate_limit_left_over():
    from backend.app import ratelimit
    ratelimit.reset()
    yield
    ratelimit.reset()


@pytest.fixture(scope="module", autouse=True)
def _leave_the_demo_data_clean(client):
    yield
    assert client.post("/api/demo/reset").status_code == 200


def _ist():
    from backend.app import authz
    return authz.ident()


def _ids(c):
    r = c.get("/api/patients")
    assert r.status_code == 200, r.text
    return [p["id"] for p in r.json()]


def _login(c, email, password):
    return c.post("/api/auth/login", json={"email": email, "password": password})


def _new_key(doctor, **body):
    body = {"label": "Test key", "scope": "patients", "patient_ids": [1, 2], "permissions": ["view"], **body}
    r = doctor.post("/api/keys", json=body)
    assert r.status_code == 200, r.text
    return r.json()


def _redeem(c, key, email="nurse.test@demo-general.example", password="nurse-test-pass-1", name="Nurse Test (fake)"):
    return c.post("/api/auth/redeem", json={"key": key, "name": name, "email": email, "password": password})


# ----------------------------------------------------------------------------- login

def test_anonymous_gets_401_json_on_the_nurse_api_and_public_routes_stay_open(anon):
    for url in ("/api/patients", "/api/patients/1", "/api/messages", "/api/model", "/api/comms/care/1",
                "/api/comms/alerts", "/api/keys", "/api/nope"):
        r = anon.get(url)
        assert r.status_code == 401 and r.json() == {"error": "login needed", "status": 401}, url
    assert anon.put("/api/patients/1", json={"target_ml": 2100}).status_code == 401
    assert anon.post("/api/demo/reset").status_code == 401
    assert anon.post("/api/collect", json={"label": "good"}).status_code == 401
    for url in ("/api/health", "/api/voice/status", "/api/comms/guardian/ravi-amit-demo", "/api/comms/card/1.png"):
        assert anon.get(url).status_code == 200, url
    assert anon.get("/api/auth/me").json() == {"authenticated": False}
    assert anon.get("/index.html").status_code == 200


def test_login_ok_wrong_and_me(anon):
    assert _login(anon, MEERA, "not-the-password").status_code == 401
    assert _login(anon, "nobody@demo-general.example", "whatever-123").json()["error"] == "wrong email or password"
    assert _login(anon, MEERA, "").status_code == 400
    assert anon.post("/api/auth/login", json=["x"]).status_code == 422
    r = _login(anon, "  Meera.Nair@Demo-General.example ", "demo-doctor-2026")      # emails are lower-cased
    assert r.status_code == 200, r.text
    me = r.json()["me"]
    assert me["authenticated"] and me["kind"] == "staff" and me["role"] == "doctor" and me["id"] == 2
    assert me["hospital"] == {"id": 1, "name": "Dawnlight General Hospital"} and me["demo_mode"] is True
    cookie = r.headers["set-cookie"].lower()
    assert "sb_staff=" in cookie and "httponly" in cookie and "samesite=lax" in cookie and "path=/" in cookie
    assert "secure" not in cookie and "max-age=43200" in cookie                    # plain http in tests; 12 hours
    assert anon.get("/api/auth/me").json()["email"] == MEERA
    assert _ids(anon) == [1, 2, 4, 6]
    # only the hash of the cookie is stored
    from backend.app import authz
    token = anon.cookies.get("sb_staff")
    rows = _ist().select("auth_sessions", [("token_hash", "eq", authz.hash_token(token))])
    assert len(rows) == 1 and rows[0]["kind"] == "staff" and rows[0]["staff_id"] == 2
    assert token not in json.dumps(_ist().select("auth_sessions"))
    assert _ist().select("staff", [("id", "eq", 2)])[0]["last_login_at"]


def test_cookie_is_secure_behind_https(anon):
    r = anon.post("/api/auth/login", json={"email": MEERA, "password": "demo-doctor-2026"},
                  headers={"X-Forwarded-Proto": "https"})
    assert r.status_code == 200 and "secure" in r.headers["set-cookie"].lower()


def test_lockout_after_ten_wrong_tries_then_locked_even_with_the_right_password(fresh, anon):
    for i in range(10):
        assert _login(anon, KABIR, f"wrong-{i}").status_code == 401, i
    r = _login(anon, KABIR, "wrong-again")
    assert r.status_code == 429 and "15 minutes" in r.json()["error"]
    assert _login(anon, KABIR, "demo-doctor-2026").status_code == 429          # locked: even the right one
    row = _ist().select("staff", [("id", "eq", 3)])[0]
    assert row["locked_until"] and row["failed_logins"] >= 10
    # another address can't get in either while the account is locked
    from backend.app import ratelimit
    ratelimit.reset()
    assert _login(anon, KABIR, "demo-doctor-2026").status_code == 429
    # an unknown email is limited the same way (per IP + email)
    for i in range(10):
        assert _login(anon, "ghost@demo-general.example", f"wrong-{i}").status_code == 401
    assert _login(anon, "ghost@demo-general.example", "x").status_code == 429
    # other accounts are not affected, and a demo reset unlocks the demo account
    assert _login(anon, MEERA, "demo-doctor-2026").status_code == 200
    assert fresh.post("/api/demo/reset").status_code == 200
    ratelimit.reset()
    assert _login(anon, KABIR, "demo-doctor-2026").status_code == 200


def test_expired_and_revoked_sessions_stop_working(login_as):
    from backend.app import authz
    from backend.app.config import iso, now_local
    from datetime import timedelta
    c = login_as(MEERA)
    assert c.get("/api/patients").status_code == 200
    h = authz.hash_token(c.cookies.get("sb_staff"))
    _ist().update("auth_sessions", [("token_hash", "eq", h)], {"expires_at": iso(now_local() - timedelta(minutes=1))})
    assert c.get("/api/patients").status_code == 401
    assert c.get("/api/auth/me").json() == {"authenticated": False}
    c = login_as(MEERA)
    h = authz.hash_token(c.cookies.get("sb_staff"))
    _ist().update("auth_sessions", [("token_hash", "eq", h)], {"revoked_at": iso(now_local())})
    assert c.get("/api/patients").status_code == 401
    # a made-up cookie is just "not logged in"
    c.cookies.set("sb_staff", "x" * 43)
    assert c.get("/api/patients").status_code == 401


def test_logout_ends_the_session(login_as):
    c = login_as(MEERA)
    token = c.cookies.get("sb_staff")
    r = c.post("/api/auth/logout")
    assert r.status_code == 200 and r.json() == {"ok": True}
    assert c.get("/api/patients").status_code == 401
    c.cookies.set("sb_staff", token)                 # the old cookie value is dead on the server too
    assert c.get("/api/patients").status_code == 401
    assert c.post("/api/auth/logout").status_code == 200       # logging out twice is fine


def test_disabled_and_pending_staff_cannot_log_in_or_keep_a_session(fresh, login_as, anon):
    c = login_as(THOMAS)
    assert c.get("/api/patients").status_code == 200
    _ist().update("staff", [("id", "eq", 5)], {"status": "disabled"})
    assert c.get("/api/patients").status_code == 401                             # at the very next request
    r = _login(anon, THOMAS, "demo-nurse-2026")
    assert r.status_code == 403 and "switched off" in r.json()["error"]
    _ist().update("staff", [("id", "eq", 5)], {"status": "pending"})
    r = _login(anon, THOMAS, "demo-nurse-2026")
    assert r.status_code == 403 and "approval" in r.json()["error"]
    assert _login(anon, THOMAS, "wrong").status_code == 401                      # the status is not leaked
    assert fresh.post("/api/demo/reset").status_code == 200                      # demo accounts come back active
    assert _login(anon, THOMAS, "demo-nurse-2026").status_code == 200


def test_password_change_needs_the_old_password(fresh, login_as, anon):
    c = login_as(THOMAS)
    other = login_as(THOMAS)                                                     # a second device
    assert c.post("/api/auth/password", json={"old_password": "wrong-old-one", "new_password": NEW_PASSWORD}).status_code == 403
    assert c.post("/api/auth/password", json={"new_password": NEW_PASSWORD}).status_code == 400
    assert c.post("/api/auth/password", json={"old_password": "demo-nurse-2026", "new_password": "short"}).status_code == 400
    assert anon.post("/api/auth/password", json={"old_password": "a", "new_password": NEW_PASSWORD}).status_code == 401
    r = c.post("/api/auth/password", json={"old_password": "demo-nurse-2026", "new_password": NEW_PASSWORD})
    assert r.status_code == 200 and r.json() == {"ok": True}
    assert c.get("/api/patients").status_code == 200                             # this device stays logged in
    assert other.get("/api/patients").status_code == 401                         # the other one is logged out
    assert _login(anon, THOMAS, "demo-nurse-2026").status_code == 401
    assert _login(anon, THOMAS, NEW_PASSWORD).status_code == 200
    assert _ist().select("staff", [("id", "eq", 5)])[0]["password_hash"].startswith("$argon2")
    # the demo reset puts the demo password back (the login page shows it)
    assert fresh.post("/api/demo/reset").status_code == 200
    assert _login(anon, THOMAS, "demo-nurse-2026").status_code == 200


def test_sessions_survive_a_demo_reset_but_demo_made_staff_do_not(fresh, login_as, anon):
    doctor = login_as(MEERA)
    r = anon.post("/api/auth/signup", json={"join_code": "DEMO-2026", "name": "Dr. Temp (fake)",
                                            "email": "temp.doc@demo-general.example", "password": "temp-doc-pass-1"})
    assert r.status_code == 200
    assert fresh.post("/api/demo/reset").status_code == 200
    assert _ids(fresh) == [1, 2, 3, 4, 5, 6, 7]                # the admin is still logged in
    assert _ids(doctor) == [1, 2, 4, 6]                        # and so is the doctor
    assert _login(anon, "temp.doc@demo-general.example", "temp-doc-pass-1").status_code == 401
    assert sorted(s["id"] for s in _ist().select("staff", columns="id")) == [1, 2, 3, 4, 5, 50]


# ----------------------------------------------------------------------------- middleware rules

def test_csrf_header_is_needed_for_every_write_except_webhooks(login_as):
    c = login_as(ADMIN)
    del c.headers["X-SB"]
    for method, url in (("PUT", "/api/patients/1"), ("POST", "/api/demo/reset"), ("POST", "/api/auth/logout"),
                        ("POST", "/api/auth/login"), ("POST", "/api/comms/guardian/ravi-amit-demo/cheer"),
                        ("DELETE", "/api/comms/guardians/1")):
        r = c.request(method, url, json={})
        assert r.status_code == 403 and r.json() == {"error": "missing X-SB header", "status": 403}, url
    assert c.get("/api/patients").status_code == 200                              # reads don't need it
    r = c.post("/api/comms/webhooks/whatsapp", data={"From": "whatsapp:+910000000000", "Body": "hello"})
    assert "X-SB" not in r.text and r.status_code != 401                          # webhooks keep their own checks
    c.headers["X-SB"] = "1"
    assert c.put("/api/patients/1", json={}).status_code == 200


def test_api_docs_are_hidden(client, anon):
    for c in (client, anon):
        for url in ("/docs", "/redoc", "/openapi.json"):
            assert c.get(url).status_code == 404, url


def test_security_headers_on_every_response(client, anon):
    for c, url in ((client, "/api/health"), (client, "/api/patients"), (anon, "/api/patients"), (client, "/index.html"),
                   (client, "/api/nope"), (anon, "/no-such-page.html")):
        h = c.get(url).headers
        assert h["x-content-type-options"] == "nosniff" and h["referrer-policy"] == "same-origin", url
        assert h["x-frame-options"] == "DENY", url
    # the 3D showroom is shown inside a frame by our own pages
    assert client.get("/showcase/").headers["x-frame-options"] == "SAMEORIGIN"


def test_training_is_off_unless_admin_and_allow_training(client, login_as, monkeypatch):
    body = {"person": "t", "label": "good", "samples": [], "features": {"peak_ml": 1800}}
    doctor = login_as(MEERA)
    assert doctor.post("/api/collect", json=body).status_code == 403            # a doctor never
    assert doctor.post("/api/train").status_code == 403
    assert login_as(ANJALI).post("/api/collect", json=body).status_code == 403
    assert client.post("/api/collect", json=body).status_code == 200            # admin + ALLOW_TRAINING=1 (conftest)
    monkeypatch.setenv("ALLOW_TRAINING", "0")
    for c in (client, doctor):
        r = c.post("/api/collect", json=body)
        assert r.status_code == 403 and "training is switched off" in r.json()["error"]
        assert c.post("/api/train").status_code == 403
    monkeypatch.delenv("ALLOW_TRAINING")
    assert client.post("/api/collect", json=body).status_code == 403            # off is the default


def test_demo_controls_are_for_admin_and_doctors_of_the_demo_hospital(fresh, login_as, monkeypatch):
    meera, anjali, riverside = login_as(MEERA), login_as(ANJALI), login_as(RIVERSIDE)
    assert meera.post("/api/demo/simulate/1", json={"breaths": 2}).status_code == 200
    assert meera.post("/api/demo/simulate/3", json={"breaths": 2}).status_code == 404     # Dr. Kabir's patient
    assert anjali.post("/api/demo/simulate/1", json={"breaths": 2}).status_code == 403    # nurses: no demo controls
    assert anjali.post("/api/demo/reset").status_code == 403
    assert anjali.post("/api/comms/demo/ladder/1", json={}).status_code == 403
    assert riverside.post("/api/demo/reset").status_code == 403                           # another hospital can't wipe the demo
    assert riverside.post("/api/demo/simulate/1", json={}).status_code == 404
    assert meera.post("/api/demo/reset").status_code == 200
    monkeypatch.setenv("DEMO_MODE", "0")
    r = meera.post("/api/demo/simulate/1", json={"breaths": 2})
    assert r.status_code == 403 and "DEMO_MODE" in r.json()["error"]
    assert fresh.post("/api/demo/reset").status_code == 403


def test_other_hospital_gets_404_everywhere(fresh, login_as, riverside_patient):
    riverside = login_as(RIVERSIDE)
    assert _ids(riverside) == [100]
    assert riverside.get("/api/patients/100").json()["name"] == "Kiran Joseph"
    assert riverside.get("/api/messages").json() == [] and riverside.get("/api/keys").json() == []
    alert = fresh.get("/api/comms/alerts?status=all&limit=1").json()[0]["id"]
    guardian = fresh.get("/api/comms/care/1").json()["guardians"][0]["id"]
    for method, url in (("GET", "/api/patients/1"), ("PUT", "/api/patients/1"), ("GET", "/api/patients/1/sessions"),
                        ("POST", "/api/summary/1"), ("POST", "/api/whatsapp/1"), ("GET", "/api/comms/care/1"),
                        ("GET", "/api/comms/patient/1"), ("GET", "/api/comms/timeline/1"), ("GET", "/api/voice/prefs/1"),
                        ("POST", f"/api/comms/alerts/{alert}/ack"), ("PUT", f"/api/comms/guardians/{guardian}"),
                        ("DELETE", f"/api/comms/guardians/{guardian}"), ("POST", "/api/keys/1/revoke"),
                        ("POST", "/api/keys/5/revoke")):
        r = riverside.request(method, url, json={"target_ml": 2100})
        assert r.status_code == 404, f"{method} {url}: {r.status_code} {r.text[:120]}"
    assert riverside.post("/api/sessions", json={"patient_id": 1, "breaths": []}).status_code == 404
    assert fresh.get("/api/patients/1").json()["target_ml"] == 2000                 # nothing was changed
    # and the other way round: Demo General can't see Riverside's patient
    assert 100 not in _ids(fresh) and fresh.get("/api/patients/100").status_code == 404
    assert login_as(MEERA).get("/api/patients/100").status_code == 404
    assert fresh.post("/api/demo/simulate/100", json={}).status_code == 404


def test_the_path_check_covers_every_router_not_only_main(client):
    """FastAPI keeps an included router as one nested entry: the middleware must open it up,
    or the patient check silently skips /api/comms/*, /api/voice/* and every 2.0 router."""
    from backend.app import main
    assert not main.SKIPPED_MODULES, main.SKIPPED_MODULES
    assert len(main.api_route_table()) > 80
    for method, path, params in (("GET", "/api/patients/1", {"pid": "1"}), ("GET", "/api/comms/care/1", {"pid": "1"}),
                                 ("PUT", "/api/voice/prefs/2", {"pid": "2"}), ("POST", "/api/keys/5/revoke", {"key_id": "5"}),
                                 ("POST", "/api/comms/cheers/9/played", {"cid": "9"}), ("GET", "/api/comms/card/3.png", {"pid": "3"}),
                                 ("POST", "/api/comms/escalations/5/stop", {"rid": "5"}), ("DELETE", "/api/comms/guardians/4", {"gid": "4"})):
        assert main._path_params(path, method) == params, path
    assert main._path_params("/api/comms/alerts/7/ack", "POST")["aid"] == "7"
    assert main._path_params("/api/comms/alerts/counts", "GET") == {} and main._path_params("/api/nope", "GET") == {}


def test_odd_ids_still_get_the_old_clean_answers(client):
    assert client.get("/api/patients/abc").status_code == 422
    assert client.get("/api/patients/999999").json() == {"error": "patient 999999 not found", "status": 404}
    assert client.get("/api/patients/99999999999999999999999").status_code in (400, 404)
    assert client.delete("/api/patients/1").status_code == 405
    assert client.get("/api/comms/calls/999999").status_code == 404
    assert client.post("/api/comms/alerts/abc/ack", json={}).status_code == 422


# ----------------------------------------------------------------------------- signup

def test_doctor_signup_with_the_join_code(fresh, anon, monkeypatch):
    body = {"join_code": "demo 2026", "name": "Dr. Asha Verma (fake)", "email": "Asha.Verma@demo-general.example",
            "password": "asha-pass-12345", "department": "General Surgery", "specialty": "Surgeon", "reg_no_display": "DEMO-0001"}
    assert anon.post("/api/auth/signup", json={**body, "join_code": "WRONG-CODE"}).status_code == 400
    assert anon.post("/api/auth/signup", json={**body, "password": "short"}).status_code == 400
    assert anon.post("/api/auth/signup", json={**body, "email": "not-an-email"}).status_code == 400
    assert anon.post("/api/auth/signup", json={**body, "name": ""}).status_code == 400
    r = anon.post("/api/auth/signup", json=body)
    assert r.status_code == 200 and r.json() == {"ok": True, "status": "active"}      # DEMO_MODE: no waiting
    assert anon.post("/api/auth/signup", json=body).status_code == 400                # the email is taken
    row = _ist().select("staff", [("email", "eq", "asha.verma@demo-general.example")])[0]
    assert row["role"] == "doctor" and row["hospital_id"] == 1 and row["password_hash"].startswith("$argon2")
    assert _login(anon, "asha.verma@demo-general.example", "asha-pass-12345").status_code == 200
    assert _ids(anon) == [] and anon.get("/api/patients/1").status_code == 404        # a new doctor has no patients yet
    assert anon.post("/api/keys", json={"label": "x", "scope": "patients", "patient_ids": [1], "permissions": ["view"]}).status_code == 400
    # outside demo mode the hospital admin has to approve first
    monkeypatch.setenv("DEMO_MODE", "0")
    other = {**body, "email": "wait.ing@demo-general.example"}
    assert anon.post("/api/auth/signup", json=other).json() == {"ok": True, "status": "pending"}
    r = _login(anon, "wait.ing@demo-general.example", "asha-pass-12345")
    assert r.status_code == 403 and "approval" in r.json()["error"]
    # the other hospital's code makes a doctor of the other hospital
    r = anon.post("/api/auth/signup", json={**body, "join_code": "RIVERSIDE-2026", "email": "river.doc@demo-riverside.example"})
    assert r.status_code == 200
    assert _ist().select("staff", [("email", "eq", "river.doc@demo-riverside.example")])[0]["hospital_id"] == 2


# ----------------------------------------------------------------------------- nurse keys

def test_doctor_creates_a_key_shown_once_and_stored_hashed(fresh, login_as):
    from backend.app import authz
    meera = login_as(MEERA)
    k = _new_key(meera, permissions=["manage_appointments"], expires_days=7, max_uses=2)
    plain = k["key"]
    assert len(plain) >= 20 and k["key_hint"] == plain[-4:] and k["status"] == "active" and k["uses"] == 0
    assert k["permissions"] == ["view", "manage_appointments"]                   # a key always lets you view
    assert k["doctor"] == {"id": 2, "name": "Dr. Meera Nair"} and k["patient_ids"] == [1, 2] and k["max_uses"] == 2
    listed = meera.get("/api/keys").json()
    assert plain not in json.dumps(listed) and all("key" not in x and "key_hash" not in x for x in listed)
    assert k["id"] in [x["id"] for x in listed]
    row = _ist().select("access_keys", [("id", "eq", k["id"])])[0]
    assert row["key_hash"] == authz.hash_token(plain) and plain not in json.dumps(row)
    # a doctor sees only their own keys; the admin sees every key in the hospital
    assert {x["doctor"]["id"] for x in meera.get("/api/keys").json()} == {2}
    assert {x["id"] for x in fresh.get("/api/keys").json()} >= {1, 2, 3, 4, 5, k["id"]}
    by_id = {x["id"]: x for x in fresh.get("/api/keys").json()}
    assert by_id[1]["status"] == "active" and by_id[1]["grants"] == [{"staff_id": 4, "name": "Sister Anjali"}]
    assert by_id[3]["status"] == "revoked" and by_id[4]["status"] == "expired"
    # only doctors create keys, only for their own patients, only known permissions
    assert fresh.post("/api/keys", json={"label": "x", "scope": "all", "permissions": ["view"]}).status_code == 403
    assert login_as(ANJALI).post("/api/keys", json={"label": "x", "scope": "all", "permissions": ["view"]}).status_code == 403
    assert login_as(ANJALI).get("/api/keys").status_code == 403
    for bad in ({"patient_ids": [3]}, {"patient_ids": [1, 999]}, {"patient_ids": []}, {"patient_ids": "1"}, {"permissions": ["fly"]},
                {"permissions": []}, {"scope": "everything"}, {"expires_days": 0}, {"max_uses": 500}, {"max_uses": "2"}):
        r = meera.post("/api/keys", json={"label": "x", "scope": "patients", "patient_ids": [1], "permissions": ["view"], **bad})
        assert r.status_code == 400, bad


def test_nurse_redeems_a_key_and_sees_only_its_scope(fresh, login_as, anon):
    meera = login_as(MEERA)
    k = _new_key(meera)                                   # patients 1 and 2, view only
    r = _redeem(anon, k["key"])
    assert r.status_code == 200, r.text
    me = r.json()["me"]
    assert me["role"] == "nurse" and me["permissions_summary"] == ["view"] and me["patients_count"] == 2
    assert _ids(anon) == [1, 2]                           # exactly the scoped patients
    assert anon.get("/api/patients/1").status_code == 200
    for pid in (4, 6, 3):                                 # Dr. Meera's other patients and Dr. Kabir's: not there
        assert anon.get(f"/api/patients/{pid}").status_code == 404
    assert {m["patient_id"] for m in anon.get("/api/messages?limit=200").json()} <= {1, 2}
    # view only: the care plan can't be changed, but the chart can be read
    r = anon.put("/api/patients/1", json={"target_ml": 2100})
    assert r.status_code == 403 and "permission" in r.json()["error"]
    assert anon.put("/api/patients/1", json={"language": "ta"}).status_code == 403
    assert anon.post("/api/whatsapp/1", json={}).status_code == 403
    assert anon.get("/api/patients/1").json()["target_ml"] == 2000
    assert anon.post("/api/summary/1", json={}).status_code == 200
    # the key is used up (max_uses 1): nobody else can redeem it
    assert meera.get("/api/keys").json()[0]["status"] == "used_up"
    r = _redeem(_fresh_anon(), k["key"], email="second.nurse@demo-general.example")
    assert r.status_code == 400 and "already been used" in r.json()["error"]
    # logging in again later works with the email and password chosen at redeem
    again = _fresh_anon()
    assert _login(again, "nurse.test@demo-general.example", "nurse-test-pass-1").status_code == 200
    assert _ids(again) == [1, 2]


def _fresh_anon():
    from fastapi.testclient import TestClient
    from backend.app.main import app
    c = TestClient(app, headers={"X-SB": "1"})
    c.cookies.clear()
    return c


def test_revoking_or_expiring_a_key_ends_access_at_the_next_request(fresh, login_as):
    from backend.app.config import iso, now_local
    from datetime import timedelta
    meera, kabir = login_as(MEERA), login_as(KABIR)
    k = _new_key(meera, permissions=["view", "update_care_plan"])
    nurse = _fresh_anon()
    assert _redeem(nurse, k["key"]).status_code == 200
    assert nurse.put("/api/patients/1", json={"target_ml": 2100}).status_code == 200      # has "update care plan"
    assert kabir.post(f"/api/keys/{k['id']}/revoke").status_code == 404                   # not Dr. Kabir's key
    assert login_as(ANJALI).post(f"/api/keys/{k['id']}/revoke").status_code == 403        # nurses don't revoke
    r = meera.post(f"/api/keys/{k['id']}/revoke")
    assert r.status_code == 200 and r.json()["status"] == "revoked" and r.json()["revoked_at"]
    assert nurse.get("/api/patients/1").status_code == 404                                # the very next request
    assert nurse.put("/api/patients/1", json={"target_ml": 2200}).status_code == 404
    assert _ids(nurse) == []
    assert _redeem(_fresh_anon(), k["key"], email="late.nurse@demo-general.example").status_code == 400
    # the admin can revoke any key in the hospital
    k2 = _new_key(kabir, patient_ids=[3])
    assert fresh.post(f"/api/keys/{k2['id']}/revoke").json()["status"] == "revoked"
    assert fresh.post("/api/keys/999999/revoke").status_code == 404
    # an expired key can't be redeemed, and access ends when a redeemed key expires
    k3 = _new_key(meera, max_uses=2)
    nurse3 = _fresh_anon()
    assert _redeem(nurse3, k3["key"], email="third.nurse@demo-general.example").status_code == 200
    assert _ids(nurse3) == [1, 2]
    _ist().update("access_keys", [("id", "eq", k3["id"])], {"expires_at": iso(now_local() - timedelta(minutes=1))})
    assert _ids(nurse3) == [] and nurse3.get("/api/patients/1").status_code == 404
    r = _redeem(_fresh_anon(), k3["key"], email="fourth.nurse@demo-general.example")
    assert r.status_code == 400 and "expired" in r.json()["error"]
    assert meera.get("/api/keys").json()[0]["status"] == "expired"


def test_max_uses_and_wrong_keys(fresh, login_as):
    k = _new_key(login_as(MEERA), max_uses=2)
    assert _redeem(_fresh_anon(), k["key"], email="n1@demo-general.example").status_code == 200
    assert _redeem(_fresh_anon(), k["key"], email="n2@demo-general.example").status_code == 200
    r = _redeem(_fresh_anon(), k["key"], email="n3@demo-general.example")
    assert r.status_code == 400 and "already been used" in r.json()["error"]
    assert _ist().select("access_keys", [("id", "eq", k["id"])])[0]["uses"] == 2
    assert _ist().select("staff", [("email", "eq", "n3@demo-general.example")]) == []     # no account was made
    r = _redeem(_fresh_anon(), "not-a-real-key")
    assert r.status_code == 400 and "not right" in r.json()["error"]
    assert _fresh_anon().post("/api/auth/redeem", json={"name": "x"}).status_code == 400
    k2 = _new_key(login_as(MEERA))
    assert _redeem(_fresh_anon(), k2["key"], password="short").status_code == 400
    assert _redeem(_fresh_anon(), k2["key"], email=MEERA, password="demo-doctor-2026").status_code == 400   # not a nurse account
    assert _ist().select("access_keys", [("id", "eq", k2["id"])])[0]["uses"] == 0


def test_demo_key_and_adding_a_key_to_a_logged_in_nurse(fresh, login_as):
    from backend.app import seed_auth
    nurse = _fresh_anon()
    r = _redeem(nurse, seed_auth.DEMO_NURSE_KEY, email="demo.redeem@demo-general.example")
    assert r.status_code == 200 and _ids(nurse) == [1, 2]
    assert set(r.json()["me"]["permissions_summary"]) == {"view", "confirm_prescriptions", "manage_appointments"}
    # Nurse Thomas (patients 3 and 5) is logged in and redeems one more key: both scopes add up
    thomas = login_as(THOMAS)
    assert _ids(thomas) == [3, 5]
    k = _new_key(login_as(MEERA), patient_ids=[4], permissions=["view", "update_care_plan"])
    r = thomas.post("/api/auth/redeem", json={"key": k["key"]})
    assert r.status_code == 200 and r.json()["me"]["id"] == 5
    assert _ids(thomas) == [3, 4, 5]
    assert thomas.put("/api/patients/4", json={"target_ml": 2100}).status_code == 200     # this key allows it
    assert thomas.put("/api/patients/3", json={"target_ml": 2100}).status_code == 403     # his first key doesn't
    assert len(_ist().select("key_grants", [("staff_id", "eq", 5)])) == 2


def test_seeded_nurses_have_the_planned_scope(fresh, login_as):
    anjali, thomas = login_as(ANJALI), login_as(THOMAS)
    assert _ids(anjali) == [1, 2, 4, 6] and _ids(thomas) == [3, 5]
    assert anjali.put("/api/patients/2", json={"target_ml": 2400}).status_code == 200
    assert thomas.put("/api/patients/3", json={"target_ml": 2400}).status_code == 403
    assert thomas.get("/api/patients/7").status_code == 404                     # Dr. Kabir's, but not in the key
    me = thomas.get("/api/auth/me").json()
    assert me["permissions_summary"] == ["view", "acknowledge_alerts"] and me["grants"][0]["patient_ids"] == [3, 5]


# ----------------------------------------------------------------------------- patient app session

def test_patient_session_sees_only_itself(fresh, patient_client, monkeypatch):
    from backend.app import authz
    p = patient_client(1)
    assert "sb_patient" in p.cookies and "sb_staff" not in p.cookies
    assert p.get("/api/auth/me").json() == {"authenticated": True, "kind": "patient", "patient_id": 1,
                                            "name": "Ravi Kumar", "language": "hi"}
    assert p.get("/api/patients/1").status_code == 200
    assert p.get("/api/patients/2").status_code == 404
    assert p.get("/api/patients").status_code == 401                             # the list is for staff
    assert p.get("/api/patients/1/sessions").status_code == 401
    assert p.put("/api/patients/1", json={"target_ml": 900}).status_code == 401
    assert p.get("/api/comms/care/1").status_code == 401 and p.get("/api/keys").status_code == 401
    assert p.post("/api/demo/reset").status_code == 401
    assert p.post("/api/sessions", json={"patient_id": 1, "breaths": []}).status_code == 400  # own scope, invalid empty exercise
    assert p.post("/api/sessions", json={"patient_id": 2, "breaths": []}).status_code == 404
    assert p.get("/api/voice/prefs/1").status_code == 200 and p.get("/api/voice/prefs/2").status_code == 404
    assert p.post("/api/comms/demo/red-flag/2", json={}).status_code == 404       # own id only
    # the same link again reuses the session; the cookie lasts 30 days
    n = len(_ist().select("auth_sessions", [("kind", "eq", "patient"), ("patient_id", "eq", 1)]))
    assert p.post("/api/me/session", json={"patient_id": 1}).status_code == 200
    assert len(_ist().select("auth_sessions", [("kind", "eq", "patient"), ("patient_id", "eq", 1)])) == n
    r = _fresh_anon().post("/api/me/session", json={"patient_id": 3})
    assert "max-age=2592000" in r.headers["set-cookie"].lower() and "httponly" in r.headers["set-cookie"].lower()
    assert r.json() == {"ok": True, "patient_id": 3, "name": r.json()["name"], "language": r.json()["language"]}
    for bad, code in (({"patient_id": 999999}, 404), ({"patient_id": "abc"}, 400), ({}, 400), ({"token": ""}, 400),
                      ({"token": "no-such-token"}, 400), ({"patient_id": [1]}, 400)):
        assert _fresh_anon().post("/api/me/session", json=bad).status_code == code, bad
    # a personal link token (stored hashed) works too
    from backend.app import service
    service.store().update("patients", [("id", "eq", 2)], {"app_token_hash": authz.hash_token("link-token-for-priya-0001")})
    t = _fresh_anon()
    assert t.post("/api/me/session", json={"token": "link-token-for-priya-0001"}).json()["patient_id"] == 2
    assert t.get("/api/patients/2").status_code == 200 and t.get("/api/patients/1").status_code == 404
    # logout ends it
    assert t.post("/api/auth/logout").status_code == 200 and t.get("/api/patients/2").status_code == 401
    # outside demo mode the id shortcut is closed (a personal link is needed)
    monkeypatch.setenv("DEMO_MODE", "0")
    assert _fresh_anon().post("/api/me/session", json={"patient_id": 1}).status_code == 403


def test_doctor_tab_and_patient_app_in_the_same_browser(fresh, login_as):
    c = login_as(THOMAS)                                  # nurse for patients 3 and 5
    assert c.post("/api/me/session", json={"patient_id": 1}).status_code == 200     # + Ravi's patient app
    assert c.get("/api/auth/me").json()["kind"] == "staff"                          # the staff login wins
    assert _ids(c) == [3, 5]
    assert c.post("/api/sessions", json={"patient_id": 1, "breaths": []}).status_code == 400   # own scope, invalid empty exercise
    assert c.get("/api/patients/1").status_code == 200                              # as the patient
    assert c.get("/api/patients/2").status_code == 404
    assert c.put("/api/patients/1", json={"target_ml": 900}).status_code == 404     # staff-only: the nurse can't see Ravi


# ----------------------------------------------------------------------------- the matrix (authz)

def _actor(email):
    from backend.app import authz
    return authz.staff_actor(_ist().select("staff", [("email", "eq", email)])[0])


def test_permission_matrix(fresh):
    from backend.app import authz, service
    admin, meera, anjali, thomas, riverside = (_actor(e) for e in (ADMIN, MEERA, ANJALI, THOMAS, RIVERSIDE))
    ravi = authz.patient_actor(service.get_patient_row(1))
    can = authz.can
    assert set(authz.RESOURCE_PARAMS) == {"pid", "rx", "item", "dose", "appt", "doc", "note_id", "aid", "rid", "cid", "gid",
                                           "staff_id", "doctor_id", "key_id", "device_id"}
    # see the patient list and chart
    assert authz.visible_patient_ids(admin) == {1, 2, 3, 4, 5, 6, 7} and authz.visible_patient_ids(meera) == {1, 2, 4, 6}
    assert authz.visible_patient_ids(anjali) == {1, 2, 4, 6} and authz.visible_patient_ids(thomas) == {3, 5}
    assert authz.visible_patient_ids(ravi) == {1} and authz.visible_patient_ids(riverside) == set()
    assert authz.visible_patient_ids(None) == set()
    # edit patient details, care plan, targets
    for a, pid, ok in ((admin, 3, True), (meera, 1, True), (meera, 3, False), (anjali, 1, True), (thomas, 3, False), (ravi, 1, False)):
        assert can(a, "careplan.edit", pid) is ok and can(a, "patient.edit", pid) is ok, (a.name, pid)
    # prescriptions: doctors; the admin never; a nurse may only approve, with the permission and the hospital setting
    assert all(can(meera, x, 1) for x in ("rx.create", "rx.approve", "rx.upload"))
    assert not any(can(admin, x, 1) for x in ("rx.create", "rx.approve", "rx.upload", "dose.report"))
    assert can(anjali, "rx.approve", 1) and not can(anjali, "rx.create", 1) and not can(thomas, "rx.approve", 3)
    assert can(ravi, "rx.upload", 1) and not can(ravi, "rx.approve", 1) and not can(ravi, "rx.upload", 2)
    _ist().update("hospitals", [("id", "eq", 1)], {"settings": {"rx_confirm_by": "doctor_only"}})
    assert not can(_actor(ANJALI), "rx.approve", 1) and can(_actor(MEERA), "rx.approve", 1)
    assert authz.hospital_settings(1)["rx_confirm_by"] == "doctor_only" and authz.hospital_settings(1)["grace_minutes"] == 60
    _ist().update("hospitals", [("id", "eq", 1)], {"settings": {}})
    # report a dose
    assert can(meera, "dose.report", 1) and can(anjali, "dose.report", 1) and can(thomas, "dose.report", 3) and can(ravi, "dose.report", 1)
    # appointments
    assert can(admin, "appt.manage", 1) and can(meera, "appt.manage", 1) and can(anjali, "appt.manage", 1)
    assert not can(thomas, "appt.manage", 3) and can(ravi, "appt.request", 1) and not can(ravi, "appt.manage", 1)
    # documents
    assert can(admin, "doc.upload", 1) and can(meera, "doc.upload", 1) and can(anjali, "doc.upload", 1)
    assert not can(thomas, "doc.upload", 3) and can(thomas, "doc.view", 3) and can(ravi, "doc.upload", 1) and can(ravi, "doc.view", 1)
    # alerts
    assert can(thomas, "alerts.ack", 3) and not can(thomas, "alerts.ack", 7) and can(anjali, "alerts.ack", 2)
    # keys, staff, governance, demo
    assert can(meera, "keys.create") and not can(admin, "keys.create") and not can(anjali, "keys.create")
    assert can(admin, "keys.revoke") and can(meera, "keys.revoke") and not can(anjali, "keys.revoke")
    assert can(admin, "admin.manage") and not can(meera, "admin.manage") and not can(anjali, "admin.manage")
    assert can(admin, "governance.read") and can(meera, "governance.read") and can(thomas, "governance.read") and not can(ravi, "governance.read")
    assert can(admin, "demo.control") and can(meera, "demo.control") and not can(anjali, "demo.control") and not can(ravi, "demo.control")
    # other hospitals: never
    assert not any(can(riverside, a, 1) for a in authz.ACTIONS) and not can(None, "patient.view", 1)
    assert authz.patient_permissions(riverside, 1) == set() and authz.patient_permissions(meera, 3) == set()
    # defaults of the hospital settings (spec §8.3)
    s = authz.hospital_settings(1)
    assert s == {"grace_minutes": 60, "quiet_hours": "21:00-07:00", "rx_confirm_by": "doctor_or_permitted_nurse",
                 "routine": {"wake": "07:00", "breakfast": "08:00", "lunch": "13:00", "dinner": "20:00", "bed": "22:00"},
                 "ai_enabled": True, "ai_handwriting": False, "reminder_channels": ["app"], "alert_thresholds": {}}
    assert authz.hospital_settings(424242)["grace_minutes"] == 60
    # programme status
    assert authz.reminders_allowed({"programme_status": "active"}) and authz.reminders_allowed({})
    assert not any(authz.reminders_allowed({"programme_status": x}) for x in ("paused", "stopped", "deceased"))


def test_require_answers_401_404_403(fresh):
    from fastapi import HTTPException
    from backend.app import authz

    def code(actor, action, pid=None):
        tokens = authz.set_actor(actor)
        try:
            authz.require(action, pid)
            return 200
        except HTTPException as e:
            return e.status_code
        finally:
            authz.reset_actor(tokens)
    thomas = _actor(THOMAS)
    assert code(None, "patient.view", 1) == 401
    assert code(thomas, "patient.view", 3) == 200 and code(thomas, "patient.view", 1) == 404
    assert code(thomas, "patient.view", 999999) == 404 and code(thomas, "patient.view", "abc") == 404
    assert code(thomas, "careplan.edit", 3) == 403 and code(thomas, "keys.create") == 403
    assert authz.current_actor() is None
    tokens = authz.set_actor(thomas)
    try:
        assert authz.require_staff().id == 5 and authz.require_staff("nurse", "doctor").role == "nurse"
        with pytest.raises(HTTPException) as e:
            authz.require_staff("admin")
        assert e.value.status_code == 403
    finally:
        authz.reset_actor(tokens)
    with pytest.raises(HTTPException) as e:
        authz.require_staff()
    assert e.value.status_code == 401


def test_path_parameter_owners(fresh):
    from backend.app import authz, service
    st = service.store()
    alert = st.select("alerts", limit=1)[0]
    guardian = st.select("guardians", [("patient_id", "eq", 1)], limit=1)[0]
    assert authz.resolve_param_owner("pid", "5") == ("patient", 5)
    assert authz.resolve_param_owner("aid", str(alert["id"])) == ("patient", alert["patient_id"])
    assert authz.resolve_param_owner("gid", guardian["id"]) == ("patient", 1)
    assert authz.resolve_param_owner("staff_id", "50") == ("hospital", 2) and authz.resolve_param_owner("doctor_id", 2) == ("hospital", 1)
    assert authz.resolve_param_owner("key_id", 5) == ("hospital", 1)
    for name in ("rx", "item", "dose", "appt", "doc", "note_id", "rid", "cid", "device_id", "aid"):
        assert authz.resolve_param_owner(name, "999999") is None, name
    assert authz.resolve_param_owner("pid", "9" * 30) is None
    for bad in ("abc", "1.5", "1e3", ""):
        with pytest.raises(ValueError):
            authz.resolve_param_owner("pid", bad)
    meera, riverside = _actor(MEERA), _actor(RIVERSIDE)
    assert authz.owner_visible(meera, ("patient", 1)) and not authz.owner_visible(meera, ("patient", 3))
    assert authz.owner_visible(meera, ("hospital", 1)) and not authz.owner_visible(riverside, ("hospital", 1))
    assert not authz.owner_visible(meera, None) and not authz.owner_visible(None, ("patient", 1))
    # a prescription line belongs to its prescription's patient
    rx = st.insert("prescriptions", [{"hospital_id": 1, "patient_id": 3, "status": "draft"}])[0]
    item = st.insert("prescription_items", [{"hospital_id": 1, "prescription_id": rx["id"], "drug_name": "Test (fake)"}])[0]
    try:
        assert authz.resolve_param_owner("rx", rx["id"]) == ("patient", 3)
        assert authz.resolve_param_owner("item", item["id"]) == ("patient", 3)
    finally:
        st.delete("prescription_items", [("id", "eq", item["id"])])
        st.delete("prescriptions", [("id", "eq", rx["id"])])


def test_rate_limit_buckets():
    from backend.app import ratelimit
    assert all(ratelimit.allow("t", "a", 3, 60) for _ in range(3))
    assert not ratelimit.allow("t", "a", 3, 60) and not ratelimit.peek("t", "a", 3, 60)
    assert ratelimit.allow("t", "b", 3, 60) and ratelimit.peek("t", "b", 3, 60)          # another key is separate
    assert ratelimit.allow("t", "a", 3, 0)                                               # the window has passed
    ratelimit.reset("t", "a")
    assert ratelimit.allow("t", "a", 1, 60) and not ratelimit.allow("t", "a", 1, 60)
    ratelimit.reset("t")
    assert ratelimit.allow("t", "a", 1, 60)
    ratelimit.reset()
    assert ratelimit.allow("t", "a", 1, 60)


# ----------------------------------------------------------------------------- audit

def test_audit_log_has_the_events_and_never_a_secret(fresh, login_as):
    from backend.app import audit, authz
    start = max([r["id"] for r in _ist().select("audit_events", columns="id")] or [0])
    secrets_seen = ["demo-doctor-2026", "demo-nurse-2026", "demo-admin-2026", "totally-wrong-pass", NEW_PASSWORD,
                    "audit-nurse-pass-1", "audit-doc-pass-12"]
    meera = login_as(MEERA)
    secrets_seen.append(meera.cookies.get("sb_staff"))
    assert _login(_fresh_anon(), MEERA, "totally-wrong-pass").status_code == 401
    assert meera.get("/api/patients/1").status_code == 200                              # a chart view
    assert meera.put("/api/patients/1", json={"target_ml": 2100, "family_phone": "+910000000000"}).status_code == 200
    k = _new_key(meera)
    secrets_seen.append(k["key"])
    nurse = _fresh_anon()
    assert _redeem(nurse, k["key"], email="audit.nurse@demo-general.example", password="audit-nurse-pass-1").status_code == 200
    secrets_seen.append(nurse.cookies.get("sb_staff"))
    assert _redeem(_fresh_anon(), "wrong-key-value-123", email="x@demo-general.example").status_code == 400
    secrets_seen.append("wrong-key-value-123")
    assert nurse.post("/api/auth/password", json={"old_password": "audit-nurse-pass-1", "new_password": NEW_PASSWORD}).status_code == 200
    assert meera.post(f"/api/keys/{k['id']}/revoke").status_code == 200
    assert _fresh_anon().post("/api/auth/signup", json={"join_code": "DEMO-2026", "name": "Dr. Audit (fake)",
                                                       "email": "audit.doc@demo-general.example", "password": "audit-doc-pass-12"}).status_code == 200
    secrets_seen.append("DEMO-2026")
    patient = _fresh_anon()
    assert patient.post("/api/me/session", json={"patient_id": 1}).status_code == 200
    secrets_seen.append(patient.cookies.get("sb_patient"))
    assert patient.get("/api/patients/1").status_code == 200                            # not a staff chart view
    assert meera.post("/api/auth/logout").status_code == 200
    rows = [r for r in _ist().select("audit_events", order="id") if r["id"] > start]
    actions = [r["action"] for r in rows]
    for a in ("auth.login", "auth.login_failed", "patient.view", "patient.update", "key.create", "key.redeem", "key.redeem_failed",
              "auth.password_change", "key.revoke", "auth.signup", "auth.patient_session", "auth.logout"):
        assert a in actions, a
    assert actions.count("patient.view") == 1                                            # once per chart view, staff only
    view = next(r for r in rows if r["action"] == "patient.view")
    assert view["actor_type"] == "staff" and view["actor_id"] == 2 and view["actor_role"] == "doctor" and view["patient_id"] == 1
    assert view["hospital_id"] == 1 and view["resource_type"] == "patient" and view["resource_id"] == "1"
    assert view["ip"] and len(view["request_id"]) == 32 and view["at"]
    login_row = next(r for r in rows if r["action"] == "auth.login")
    assert login_row["detail"]["hospital_id"] == 1 and login_row["patient_id"] is None   # staff without a patient
    dump = json.dumps(rows)
    for s in secrets_seen:
        assert s and s not in dump, f"a secret reached the audit log: {s[:6]}..."
    # the writer blanks anything that looks like a secret, and never raises
    audit.write("test.event", "thing", 1, detail={"password": "p@ss", "new_token": "tok", "key": "k", "nested": {"join_code": "J"},
                                                  "note": "fine"}, actor=_actor(ADMIN))
    d = _ist().select("audit_events", [("action", "eq", "test.event")])[-1]["detail"]
    assert d["password"] == d["new_token"] == d["key"] == d["nested"]["join_code"] == "[hidden]" and d["note"] == "fine"
    audit.write("test.event", "thing", detail={"x": object()}, actor=None)               # odd values: no error
    assert authz.current_actor() is None
    # reading it back: newest first, by hospital, with filters
    events = audit.list_events(1, {"action": "patient.view"}, limit=5)
    assert events and all(e["action"] == "patient.view" and e["hospital_id"] == 1 for e in events)
    assert all(e["hospital_id"] == 2 for e in audit.list_events(2, {}))             # never another hospital's rows
    assert all(e["patient_id"] == 1 for e in audit.list_events(1, {"patient_id": 1}))
    assert audit.list_events(1, {"patient_ids": {3}, "action": "patient.view"}) == []
