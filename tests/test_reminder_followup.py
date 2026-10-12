"""Medication follow-ups survive midnight and patient demographic edits."""
from datetime import timedelta

from backend.app import service
from backend.app.config import now_local
from backend.app.meds import service as meds, reminders


def _alerts():
    return service.store().select('alerts', [('patient_id', 'eq', 1), ('kind', 'eq', 'missed_dose')])


def test_yesterday_report_resolves_existing_followup(fresh, monkeypatch):
    yesterday = now_local().replace(hour=12, minute=0, second=0, microsecond=0)
    monkeypatch.setattr(meds, 'now_local', lambda: yesterday)
    reminders.tick(force=True)
    old = _alerts()
    assert old
    missed = [d for d in meds.today_doses(1) if d['status'] == 'missed']
    assert missed
    monkeypatch.setattr(meds, 'now_local', lambda: yesterday + timedelta(hours=13))
    for dose in missed:
        meds.report_dose(dose['id'], 'patient', 1)
    reminders.tick(force=True)
    assert all(service.store().select('alerts', [('id', 'eq', a['id'])])[0]['status'] == 'resolved' for a in old)


def test_name_change_and_staff_resolution_do_not_duplicate(fresh, monkeypatch):
    stamp = now_local().replace(hour=12, minute=0, second=0, microsecond=0)
    monkeypatch.setattr(meds, 'now_local', lambda: stamp)
    reminders.tick(force=True)
    old = _alerts()
    assert old
    service.store().update('patients', [('id', 'eq', 1)], {'name': 'Updated sample name'})
    reminders.tick(force=True)
    assert {a['id'] for a in _alerts()} == {a['id'] for a in old}
    service.store().update('alerts', [('id', 'eq', old[0]['id'])], {'status': 'resolved'})
    reminders.tick(force=True)
    assert {a['id'] for a in _alerts()} == {a['id'] for a in old}
    assert service.store().select('alerts', [('id', 'eq', old[0]['id'])])[0]['status'] == 'resolved'


def test_legacy_named_alert_and_paused_patient_remain_safe(fresh, monkeypatch):
    stamp = now_local().replace(hour=12, minute=0, second=0, microsecond=0)
    monkeypatch.setattr(meds, 'now_local', lambda: stamp)
    reminders.tick(force=True)
    alert = _alerts()[0]
    due = next(d['due_at'] for d in meds.today_doses(1) if d['status'] == 'missed')
    from backend.app.config import parse_dt
    legacy = 'Old name: medicine follow-up at ' + parse_dt(due).strftime('%d %b %I:%M %p')
    service.store().update('alerts', [('id', 'eq', alert['id'])], {'title': legacy})
    service.store().update('patients', [('id', 'eq', 1)], {'name': 'Changed name'})
    reminders.tick(force=True)
    assert len(_alerts()) == 1
    service.store().update('patients', [('id', 'eq', 1)], {'programme_status': 'paused'})
    reminders.tick(force=True)
    assert _alerts()[0]['status'] == 'open'
