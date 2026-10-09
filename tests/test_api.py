"""CONTRACT D smoke tests: every endpoint answers sensibly with no keys (docs/ARCHITECTURE.md §6)."""
from ml import synth

LABELS = {"good", "too_fast", "too_shallow", "no_hold"}


def test_health(client):
    h = client.get("/api/health").json()
    assert h["ok"] is True
    assert h["data_backend"] == "demo" and h["demo_mode"] is True
    assert h["llm_enabled"] is False and h["whatsapp_enabled"] is False


def test_patients_list_has_all_colours(fresh):
    pts = fresh.get("/api/patients").json()
    assert len(pts) >= 6
    assert pts[0]["id"] == 1 or any(p["id"] == 1 for p in pts)
    assert {"red", "yellow", "green"} <= {p["status"] for p in pts}
    for p in pts:
        for key in ("name", "age", "surgery", "language", "target_ml", "done_today", "due_today"):
            assert key in p


def test_patient_detail_and_update(fresh):
    d = fresh.get("/api/patients/1").json()
    assert d["name"].startswith("Ravi")
    assert len(d["history"]) == 7
    assert all(s["status"] in {"done", "missed", "pending", "upcoming"} for s in d["today"])
    assert fresh.put("/api/patients/1", json={"target_ml": 2200}).json()["target_ml"] == 2200
    fresh.put("/api/patients/1", json={"target_ml": 2000})


def test_unknown_patient_is_json_404(client):
    r = client.get("/api/patients/999")
    assert r.status_code == 404 and "error" in r.json()


def test_classify_good_and_fast(client):
    _, good = synth.make_breath("good")
    r = client.post("/api/classify", json=good).json()
    assert r["label"] in LABELS and r["source"] in {"model", "rules"}
    fast = dict(good, max_rise_ml_s=2500, mean_rise_ml_s=1800)
    assert client.post("/api/classify", json=fast).json()["label"] == "too_fast"


def test_post_session_ticks_a_slot(fresh):
    breaths = []
    for i in range(10):
        _, f = synth.make_breath("good")
        breaths.append({"t": i * 15_000, "features": f})
    r = fresh.post("/api/sessions", json={"patient_id": 1, "started_at": "2026-10-09T10:00:00+05:30",
                                          "breaths": breaths})
    assert r.status_code == 200
    body = r.json()
    assert body["slot_status"] == "done" and 8 <= body["slot_hour"] <= 21


def test_demo_simulate_miss_reset(fresh):
    sim = fresh.post("/api/demo/simulate/1", json={"quality": "mixed"}).json()
    assert len(sim["breaths"]) == 10
    assert all(b["label"] in LABELS for b in sim["breaths"])
    agree = sum(b["label"] == b["intended"] for b in sim["breaths"])
    assert agree >= 6, f"model agreed only {agree}/10"
    miss = fresh.post("/api/demo/miss/2").json()
    assert miss["ok"] is True
    assert fresh.post("/api/demo/simulate/1", json={"quality": "awful"}).status_code == 400
    assert fresh.post("/api/demo/reset").json()["ok"] is True


def test_sessions_list(fresh):
    fresh.post("/api/demo/simulate/1", json={"quality": "good"})
    rows = fresh.get("/api/patients/1/sessions?limit=5").json()
    assert rows and {"good", "too_fast", "too_shallow", "no_hold"} <= set(rows[0]["label_counts"])


def test_summary_falls_back_to_template(client):
    for lang in ("en", "hi"):
        r = client.post("/api/summary/1", json={"language": lang}).json()
        assert r["source"] == "template" and len(r["text"]) > 20


def test_whatsapp_is_dry_run_without_keys(client):
    r = client.post("/api/whatsapp/1", json={"kind": "summary", "to": "family"}).json()
    assert r["dry_run"] is True and r["sent"] is False and r["text"]
    assert client.get("/api/messages").status_code == 200


def test_model_info(client):
    m = client.get("/api/model").json()
    assert "model_loaded" in m


def test_unknown_api_path_is_json_404(client):
    r = client.get("/api/nope")
    assert r.status_code == 404 and "error" in r.json()


def test_static_pages_served(client):
    for path in ("/", "/patient.html", "/demo.html", "/collect.html", "/guardian.html", "/showcase/"):
        assert client.get(path).status_code == 200, path
