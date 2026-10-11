"""2.0 hospital isolation for the comms routes (alerts, escalations, events, calls, care plan,
guardians): staff of one hospital never see or act on another hospital's patients."""
from __future__ import annotations

C = "/api/comms"
RIVERSIDE_ADMIN = "admin@demo-riverside.example"


def _demo_city_alert(client) -> dict:
    """A red-flag alert for patient 1 (Dawnlight General Hospital)."""
    r = client.post(f"{C}/demo/red-flag/1", json={})
    assert r.status_code == 200, r.text
    rows = client.get(f"{C}/alerts?status=active&patient_id=1").json()
    assert rows, "the demo red flag should raise an alert"
    return rows[0]


def test_other_hospital_sees_no_alerts_events_or_calls(client, login_as):
    alert = _demo_city_alert(client)
    other = login_as(RIVERSIDE_ADMIN)
    assert all(a.get("patient_id") != 1 for a in other.get(f"{C}/alerts?status=active").json())
    assert other.get(f"{C}/alerts?status=active&patient_id=1").json() == []
    counts = other.get(f"{C}/alerts/counts").json()
    assert "1" not in counts["by_patient"] and counts["open"] == 0
    assert all(e.get("patient_id") != 1 for e in other.get(f"{C}/events").json())
    assert all(c.get("patient_id") != 1 for c in other.get(f"{C}/calls").json())
    assert all(r.get("patient_id") != 1 for r in other.get(f"{C}/escalations").json())
    # the home hospital still sees it
    assert any(a["id"] == alert["id"] for a in client.get(f"{C}/alerts?status=active").json())


def test_other_hospital_cannot_act_on_a_patient_it_cannot_see(client, login_as):
    alert = _demo_city_alert(client)
    other = login_as(RIVERSIDE_ADMIN)
    assert other.post(f"{C}/alerts/{alert['id']}/ack", json={"by": "x"}).status_code == 404
    assert other.put(f"{C}/care/1", json={}).status_code == 404
    assert other.post(f"{C}/guardians", json={"patient_id": 1, "name": "X"}).status_code == 404
    assert other.post(f"{C}/wa/reply", json={"patient_id": 1, "text": "status"}).status_code == 404
    # the alert is untouched
    a = [x for x in client.get(f"{C}/alerts?status=active").json() if x["id"] == alert["id"]][0]
    assert a["status"] == alert["status"]


def test_home_hospital_can_still_acknowledge(client):
    alert = _demo_city_alert(client)
    r = client.post(f"{C}/alerts/{alert['id']}/ack", json={"by": "Sister Anjali"})
    assert r.status_code == 200, r.text
