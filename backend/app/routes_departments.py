"""Department and hospital operational views; admin role only."""
from fastapi import APIRouter, Body, HTTPException
from . import authz
from .department_ops import service as ops

router = APIRouter(tags=['department operations'])


@router.get('/api/department-ops')
def board():
    return ops.snapshot(authz.require_staff('admin'))


@router.post('/api/department-ops/beds')
def create_bed(body: dict = Body(...)):
    return ops.mutate(authz.require_staff('admin'), 'create', body)


@router.post('/api/department-ops/beds/{bed_id}/{action}')
def operate_bed(bed_id: str, action: str, body: dict = Body(...)):
    actor = authz.require_staff('admin')
    if action not in ('admit', 'transfer', 'discharge', 'ready', 'clean'):
        raise HTTPException(400, 'Unknown bed operation')
    return ops.mutate(actor, action, body, bed_id)
