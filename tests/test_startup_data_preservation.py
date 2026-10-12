"""A deployment never resets a populated persistent or local store."""
import asyncio

import pytest


@pytest.mark.parametrize('backend,count', [('supabase', 12), ('demo', 12), ('demo', 0)])
def test_startup_preserves_existing_data_and_seeds_only_empty_store(monkeypatch, backend, count):
    from backend.app import main, seed_patient_login, storage
    from backend.app.meds import seed_meds

    class FakeStore:
        name = backend
        def count(self, table):
            assert table == 'patients'
            return count

    fake = FakeStore()
    events = []
    monkeypatch.setattr(main.service, 'init_store', lambda: fake)
    monkeypatch.setattr(main, 'demo_mode', lambda: True)
    # Even a stale-history signal must never turn a populated store into a reset.
    monkeypatch.setattr(main.seed, 'needs_seed', lambda *a: True)
    monkeypatch.setattr(main.seed, 'reset', lambda *a: pytest.fail('Startup must not reset stored data'))
    monkeypatch.setattr(main.seed, 'seed', lambda store: events.append(('seed', store)))
    monkeypatch.setattr(main.seed_auth, 'ensure', lambda store: events.append(('accounts', store)))
    monkeypatch.setattr(seed_patient_login, 'ensure',
        lambda store, reset_pin: events.append(('patient_logins', store, reset_pin)))
    monkeypatch.setattr(seed_meds, 'seed', lambda store: events.append(('sample_medicines', store)))
    monkeypatch.setattr(storage, 'ensure_bucket', lambda: None)
    monkeypatch.setattr(main.models_ml, 'load', lambda: None)

    async def restart():
        async with main.lifespan(main.app):
            pass
        async with main.lifespan(main.app):
            pass
    asyncio.run(restart())

    assert [e for e in events if e[0] == 'seed'] == ([('seed', fake)] * 2 if count == 0 else [])
    assert events.count(('accounts', fake)) == 2
    assert events.count(('patient_logins', fake, False)) == 2
    assert events.count(('sample_medicines', fake)) == 2


def test_sample_phone_setup_preserves_registered_pending_phone(fresh, login_as):
    from backend.app import seed_patient_login, service
    doctor = login_as('meera.nair@demo-general.example')
    created = doctor.post('/api/patients', json={'registration_no': 'PHONE-PENDING-1',
        'name': 'Sample pending phone', 'age': 40, 'sex': 'F', 'language': 'en'})
    assert created.status_code == 200, created.text
    pid = created.json()['patient']['id']
    assert service.get_patient_row(pid)['phone'] is None
    service.store().update('patients', [('id', 'eq', 1)], {'phone': None})
    # A reused small id alone must not establish a fictional sample identity.
    service.store().update('patients', [('id', 'eq', 3)], {'name': 'Replacement patient', 'phone': None})
    seed_patient_login.ensure(service.store(), reset_pin=False)
    assert service.get_patient_row(pid)['phone'] is None
    assert service.get_patient_row(3)['phone'] is None
    assert service.get_patient_row(1)['phone'] == '+910000000001'
    assert doctor.get(f'/api/patients/{pid}/login').json()['phone_hint'] == 'Phone number pending'
