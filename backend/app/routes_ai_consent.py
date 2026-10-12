"""Optional patient AI-processing choice; append-only clinical consent versions.

Single-process lock serializes choices in this prototype. Multi-worker deployment
requires a database transaction/version constraint for concurrent writers.
"""
from threading import RLock

from fastapi import APIRouter, Body, HTTPException, Request, Response

from . import audit, authz, service
from .config import demo_mode, iso, now_local

router = APIRouter(tags=['patient-ai-consent'])
_lock = RLock()


def _patient():
    actor = authz.current_actor()
    if actor is None:
        raise HTTPException(401, 'Patient login required')
    if actor.kind != 'patient' or actor.patient_id is None:
        raise HTTPException(403, 'Only the patient can record this choice')
    p = service.get_patient_row(actor.patient_id)
    if not p or p.get('hospital_id') != actor.hospital_id:
        raise HTTPException(404, 'Patient not found')
    return actor


def _latest(actor):
    rows = service.store().select('consents', [('patient_id', 'eq', actor.patient_id)],
                                  order='id', desc=True, limit=1)
    if rows and rows[0].get('hospital_id') != actor.hospital_id:
        raise HTTPException(409, 'Consent record requires hospital review')
    return rows[0] if rows else {}


def _view(row):
    items = row.get('items') or {}
    return {'ai_use': items.get('ai_use') is True and not bool(row.get('withdrawn_at')),
            'recorded': bool(row), 'version': row.get('version'),
            'updated_at': row.get('created_at'), 'demo': demo_mode()}


@router.get('/api/me/ai-consent')
def get_choice(response: Response):
    response.headers['Cache-Control'] = 'no-store'
    actor = _patient()
    with _lock:
        return _view(_latest(actor))


@router.post('/api/me/ai-consent')
def set_choice(request: Request, response: Response, body: dict = Body(...)):
    response.headers['Cache-Control'] = 'no-store'
    actor = _patient()
    if set(body) - {'ai_use', 'language'} or type(body.get('ai_use')) is not bool:
        raise HTTPException(400, 'Send only a boolean ai_use choice and optional language')
    language = body.get('language', 'en')
    if language not in ('en', 'hi', 'ta', 'ml'):
        raise HTTPException(400, 'Unsupported language')
    with _lock:
        old = _latest(actor)
        items = dict(old.get('items') or {})
        items['ai_use'] = body['ai_use']
        # Do not resurrect an earlier withdrawal of the complete clinical consent.
        if old.get('withdrawn_at') and body['ai_use']:
            raise HTTPException(409, 'Your clinical consent was withdrawn. Ask the care team to review it before enabling AI.')
        row = {'hospital_id': actor.hospital_id, 'patient_id': actor.patient_id,
               'version': int(old.get('version') or 0) + 1, 'items': items,
               'method': 'self', 'taken_by': None, 'language': language,
               'read_aloud': False, 'teach_back_ok': None,
               'created_at': iso(now_local()), 'withdrawn_at': old.get('withdrawn_at')}
        service.store().insert('consents', [row])
        audit.write('consent.ai_choice', 'patient', actor.patient_id, patient_id=actor.patient_id,
                    actor=actor, request=request,
                    detail={'ai_use': body['ai_use'], 'version': row['version'], 'method': 'self'})
        return _view(row)
