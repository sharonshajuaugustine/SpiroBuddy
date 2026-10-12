"""One hospital/patient JSON aggregate. An RLock serializes all state transitions.

Not distributed-safe: production requires transactional rows and database CAS.
Published content is immutable; state/acknowledgement metadata may change.
"""
import copy
import threading
from datetime import date
from fastapi import HTTPException
from .. import service as core
from ..config import iso, now_local

LOCK = threading.RLock()
FIELDS = ('condition_summary','treatment_summary','home_care','warning_signs','follow_up','exercise_instructions')
REQUIRED = ('condition_summary','home_care','follow_up')

def content(body):
    if not isinstance(body,dict):
        raise HTTPException(400,'Content must contain named plain-text fields')
    out = {}
    for field in FIELDS:
        value = body.get(field, '')
        if not isinstance(value, str) or len(value) > 4000:
            raise HTTPException(400, f'{field}: maximum 4,000 plain-text characters')
        out[field] = value  # preserve clinician text exactly
    language = body.get('language', 'en')
    if not isinstance(language,str) or not language.strip() or len(language)>40:
        raise HTTPException(400, 'Enter the document language')
    out['language'] = language
    for field in ('follow_up_date','discharge_date'):
        value = body.get(field) or None
        if value is not None:
            try:
                if not isinstance(value,str) or date.fromisoformat(value).isoformat()!=value:
                    raise ValueError()
            except ValueError:
                raise HTTPException(400, f'{field}: use YYYY-MM-DD')
        out[field] = value
    return out

def read(hid,pid):
    key=f'discharge:v1:{hid}:{pid}'
    rows=core.store().select('app_settings', [('key','eq',key),('hospital_id','eq',hid)],limit=1)
    return copy.deepcopy(rows[0]['value']) if rows else {'revision':0,'versions':[]}

def save(hid,pid,state):
    stamp=iso(now_local())
    core.store().upsert('app_settings',[{'key':f'discharge:v1:{hid}:{pid}','hospital_id':hid,
        'value':state,'created_at':stamp,'updated_at':stamp}])

def current(state):
    return next((v for v in state['versions'] if v['status']=='published'),None)

def transition(hid,pid,actor,action,body,version=None):
    with LOCK:
        state=read(hid,pid)
        revision=body.get('revision')
        if isinstance(revision,bool) or not isinstance(revision,int) or revision!=state['revision']:
            raise HTTPException(409,'This document changed. Reload before saving.')
        v=next((v for v in state['versions'] if v['version']==version),None)
        stamp=iso(now_local())
        if action=='create':
            if len(state['versions'])>=100:
                raise HTTPException(409,'Prototype history limit reached; contact the administrator')
            if any(v['status']=='draft' for v in state['versions']):
                raise HTTPException(409,'Reload the existing draft')
            source=current(state)
            v={'version':len(state['versions'])+1,'status':'draft','content':content(body.get('content',source['content'] if source else {})),
               'author':{'id':actor.id,'name':actor.name},'created_at':stamp,'updated_at':stamp,'acknowledgement':None,
               'replaces_version':source['version'] if source else None}
            state['versions'].append(v)
        else:
            if not v: raise HTTPException(404,'Document version not found')
            if action in ('update','publish'):
                if v['status']!='draft': raise HTTPException(409,'Published content is immutable. Create a replacement draft.')
                if action=='update':
                    v['content']=content(body.get('content',{}))
                    v['last_edited_by']={'id':actor.id,'name':actor.name}
                else:
                    if body.get('confirm') is not True: raise HTTPException(400,'Confirm publication to the patient')
                    if any(not v['content'][f].strip() for f in REQUIRED):
                        raise HTTPException(400,'Condition summary, home care and follow-up are required')
                    old=current(state)
                    if old: old.update(status='superseded',superseded_at=stamp,replaced_by=v['version'])
                    v.update(status='published',published_at=stamp,author={'id':actor.id,'name':actor.name})
            elif action=='withdraw':
                if v['status']!='published': raise HTTPException(409,'Only the current published document can be withdrawn')
                reason=body.get('reason')
                if not isinstance(reason,str) or not reason.strip() or len(reason)>1000:
                    raise HTTPException(400,'Enter a withdrawal reason, maximum 1,000 characters')
                v.update(status='withdrawn',withdrawn_at=stamp,withdrawn_by={'id':actor.id,'name':actor.name},withdrawal_reason=reason)
            elif action=='ack':
                if v['status']!='published': raise HTTPException(409,'The current document changed. Reload your care page.')
                if not v['acknowledgement']:
                    v['acknowledgement']={'patient_id':pid,'at':stamp,'version':version}
            else: raise HTTPException(400,'Unknown transition')
            v['updated_at']=stamp
        state['revision']+=1
        save(hid,pid,state)
        return copy.deepcopy(state),copy.deepcopy(v)
