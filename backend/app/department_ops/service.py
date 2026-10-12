"""Hospital-scoped operational records. Never infer admissions from clinical sessions.

RLock + optimistic version protects a single process. JSON state and patient display fields
are two writes with compensation; migrate to transactional normalized tables before scaling.
"""
import copy
import threading
import uuid

from fastapi import HTTPException
from .. import authz, service
from ..config import iso, now_local

LOCK = threading.RLock()


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise HTTPException(400, f"Invalid {label}")
    return value


def hospital(actor):
    rows = service.store().select('hospitals', [('id', 'eq', actor.hospital_id)], limit=1)
    if not rows:
        raise HTTPException(404, 'Hospital not found')
    return rows[0]


def read(actor):
    rows = service.store().select('app_settings', [('key', 'eq', f'department_ops:{actor.hospital_id}')], limit=1)
    return copy.deepcopy(rows[0]['value']) if rows else {'version': 0, 'beds': [], 'history': []}


def save(actor, state):
    stamp = iso(now_local())
    service.store().upsert('app_settings', [{'key': f'department_ops:{actor.hospital_id}',
        'hospital_id': actor.hospital_id, 'value': state, 'created_at': stamp, 'updated_at': stamp}])


def text(body, key, maximum=80):
    v = body.get(key)
    if not isinstance(v, str) or not v.strip() or len(v) > maximum:
        raise HTTPException(400, f'Enter a valid {key}')
    return v.strip()


def patient(actor, pid):
    number(pid, 'patient identifier')
    rows = service.store().select('patients', [('id', 'eq', pid)], limit=1)
    if not rows or (rows[0].get('hospital_id') or authz.LEGACY_HOSPITAL_ID) != actor.hospital_id:
        raise HTTPException(404, 'Patient not found')
    return rows[0]


def mutate(actor, action, body, bed_id=None):
    with LOCK:
        h = hospital(actor)
        old = read(actor)
        if action != 'create' and not any(b['id'] == bed_id for b in old['beds']):
            raise HTTPException(404, 'Bed not found')
        if action in ('admit', 'transfer'):
            patient(actor, body.get('patient_id'))
        version = body.get('version')
        if isinstance(version, bool) or not isinstance(version, int) or version < 0:
            raise HTTPException(400, 'A non-negative version is required')
        if version != old['version']:
            raise HTTPException(409, 'The bed board changed. Refresh before trying again.')
        state = copy.deepcopy(old)
        beds = state['beds']
        bed = next((b for b in beds if b['id'] == bed_id), None)
        p = None
        event = {'action': action, 'at': iso(now_local()), 'actor_id': actor.id, 'actor_name': actor.name}
        if action == 'create':
            department, ward, label = text(body, 'department'), text(body, 'ward'), text(body, 'label', 40)
            if department not in (h.get('departments') or []) or ward not in (h.get('wards') or []):
                raise HTTPException(400, 'Choose a department and ward configured for this hospital')
            if any(b['ward'].casefold() == ward.casefold() and b['label'].casefold() == label.casefold() for b in beds):
                raise HTTPException(409, 'This ward already has a bed with that label')
            if len(beds) >= 1000:
                raise HTTPException(400, 'Prototype bed inventory limit reached')
            bed = {'id': uuid.uuid4().hex, 'department': department, 'ward': ward, 'label': label,
                   'status': 'available', 'patient_id': None}
            beds.append(bed)
        else:
            if bed is None:
                raise HTTPException(404, 'Bed not found')
            if action in ('admit', 'transfer'):
                p = patient(actor, body.get('patient_id'))
                if p.get('programme_status') == 'deceased':
                    raise HTTPException(400, 'This patient cannot be admitted')
                if bed['status'] != 'available':
                    raise HTTPException(409, 'Choose an available bed')
                occupied = next((b for b in beds if b['patient_id'] == p['id']), None)
                if action == 'admit' and occupied:
                    raise HTTPException(409, 'Patient already admitted. Use transfer.')
                if action == 'transfer' and occupied is None:
                    raise HTTPException(409, 'Patient has no active admission to transfer')
                if occupied:
                    event['from_bed_id'] = occupied['id']
                    event['from_department'] = occupied['department']
                    occupied.update(status='cleaning', patient_id=None)
                bed.update(status='occupied', patient_id=p['id'])
            elif action == 'discharge':
                if bed['status'] != 'occupied' or not bed['patient_id']:
                    raise HTTPException(409, 'This bed has no admission to discharge')
                p = patient(actor, bed['patient_id'])
                bed.update(status='cleaning', patient_id=None)
            elif action == 'ready':
                if bed['status'] != 'cleaning':
                    raise HTTPException(409, 'Only a cleaning bed can be marked ready')
                bed['status'] = 'available'
            elif action == 'clean':
                if bed['status'] != 'available':
                    raise HTTPException(409, 'Only an available bed can be marked cleaning')
                bed['status'] = 'cleaning'
            else:
                raise HTTPException(400, 'Unknown bed operation')
        event.update(bed_id=bed['id'], department=bed['department'], ward=bed['ward'], label=bed['label'])
        if p:
            event['patient_id'] = p['id']
        state['history'].append(event)
        state['version'] += 1
        # Scope is rechecked in patient(); compensate patient display write if state save fails.
        if p:
            fields = {'ward': bed['ward'], 'bed': bed['label']} if action != 'discharge' else {'ward': None, 'bed': None}
            scoped = [('id', 'eq', p['id'])]
            if p.get('hospital_id') is not None:
                scoped.append(('hospital_id', 'eq', actor.hospital_id))
            service.store().update('patients', scoped, fields)
        try:
            save(actor, state)
        except Exception:
            if p:
                service.store().update('patients', scoped,
                                       {'ward': p.get('ward'), 'bed': p.get('bed')})
            raise
        return snapshot(actor)


def snapshot(actor):
    with LOCK:
        h, state = hospital(actor), read(actor)
        patients = service.store().select('patients', [('hospital_id', 'eq', actor.hospital_id)],
                    columns='id,name,mrn,primary_doctor_id,ward,bed,surgery')
        doctors = service.store().select('staff', [('hospital_id', 'eq', actor.hospital_id), ('role', 'eq', 'doctor')],
                                       columns='id,name,department')
        names = {d['id']: d['name'] for d in doctors}
        active = {b['patient_id']: b for b in state['beds'] if b['status'] == 'occupied'}
        for p in patients:
            p['doctor'] = names.get(p.get('primary_doctor_id'), 'Not assigned')
            p['admission'] = active.get(p['id'])
        today = iso(now_local())[:10]
        counts = {'current_admissions': len(active), 'occupied': 0, 'available': 0, 'cleaning': 0,
                  'admissions_today': 0, 'discharges_today': 0, 'total_beds': len(state['beds'])}
        departments = {d: {'occupied': 0, 'available': 0, 'cleaning': 0, 'total_beds': 0} for d in h.get('departments') or []}
        for b in state['beds']:
            counts[b['status']] += 1
            total = departments.setdefault(b['department'], {'occupied': 0, 'available': 0, 'cleaning': 0, 'total_beds': 0})
            total[b['status']] += 1
            total['total_beds'] += 1
        for e in state['history']:
            if e['at'][:10] == today:
                if e['action'] == 'admit': counts['admissions_today'] += 1
                if e['action'] == 'discharge': counts['discharges_today'] += 1
        return {**state, 'hospital': {'id': h['id'], 'name': h['name']}, 'departments': departments,
                'actor': {'name': actor.name, 'role': actor.role},
                'wards': h.get('wards') or [], 'patients': patients, 'doctors': doctors, 'counts': counts,
                'notice': 'Admin-operated department prototype. Dedicated department login is Planned.'}
