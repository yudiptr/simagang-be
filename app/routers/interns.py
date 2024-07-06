from fastapi import APIRouter, Response, Request
from app.controllers.interns import InternController
intern_router = APIRouter(prefix='/intern')

@intern_router.get('/division')
async def get_intern_division():
    res = await InternController().get_divsion()
    return res

@intern_router.get('/quota')
async def get_intern_quota():
    res = await InternController().get_quota()
    return res