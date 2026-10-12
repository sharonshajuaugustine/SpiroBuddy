"""Patient-only optional AI choice with immutable history and no provider calls."""
import pytest
from backend.app import ai_gemini as ai, service
from backend.app.routes_ai_consent import router


@pytest.fixture(autouse=True)
def route_available(client):
    # Production integration is owned by the root agent; isolated test registers
    # only when that integration has not landed yet, before the fallback route.
    from backend.app.main import app
    if not any(getattr(r, 'path', '') == '/api/me/ai-consent' for r in app.routes):
        old = list(app.router.routes)
        app.include_router(router)
        new = [r for r in app.router.routes if r not in old]
        app.router.routes[:] = new + old


def test_patient_choice_history_and_ai_gate(fresh, patient_client, monkeypatch):
    c = patient_client(1)
    service.store().delete('consents', [('patient_id','eq',1)])
    monkeypatch.setattr(ai, 'gemini_enabled', lambda: True)
    ai.reset_limits()
    assert c.get('/api/me/ai-consent').json()['ai_use'] is False
    assert ai.ai_allowed(1,1,None)[0] is False
    first = c.post('/api/me/ai-consent',json={'ai_use':True,'language':'en'})
    assert first.status_code == 200, first.text
    assert ai.ai_allowed(1,1,None)[0] is True
    assert c.post('/api/me/ai-consent',json={'ai_use':False}).status_code == 200
    assert ai.ai_allowed(1,1,None)[0] is False
    rows = service.store().select('consents',[('patient_id','eq',1)],order='id')
    assert len(rows) == 2 and rows[0]['items']['ai_use'] is True
    assert rows[1]['version'] == 2 and rows[1]['items']['ai_use'] is False


def test_other_preferences_and_withdrawal_preserved(fresh, patient_client):
    st = service.store(); st.delete('consents',[('patient_id','eq',1)])
    st.insert('consents',[{'hospital_id':1,'patient_id':1,'version':3,
                         'items':{'family_sharing':False,'care_reminders':True,'ai_use':True}}])
    c = patient_client(1)
    assert c.post('/api/me/ai-consent',json={'ai_use':False}).status_code == 200
    row = st.select('consents',[('patient_id','eq',1)],order='id',desc=True,limit=1)[0]
    assert row['items']['care_reminders'] is True and row['items']['family_sharing'] is False
    st.update('consents',[('id','eq',row['id'])],{'withdrawn_at':'2026-10-12T10:00:00+05:30'})
    assert c.post('/api/me/ai-consent',json={'ai_use':True}).status_code == 409
    assert c.post('/api/me/ai-consent',json={'ai_use':False}).status_code == 200
    assert c.get('/api/me/ai-consent').json()['ai_use'] is False


def test_patient_identity_and_strict_input(fresh, patient_client, anon, login_as):
    assert anon.get('/api/me/ai-consent').status_code == 401
    staff = login_as('meera.nair@demo-general.example')
    assert staff.post('/api/me/ai-consent',json={'ai_use':True}).status_code in (401,403)
    c = patient_client(1)
    for body in ({'ai_use':'true'}, {'ai_use':True,'patient_id':2}, {'ai_use':True,'hospital_id':2}, {'ai_use':True,'language':'xx'}):
        assert c.post('/api/me/ai-consent',json=body).status_code == 400
