import json
from fastapi import APIRouter, Response, Request, status
from marshmallow import ValidationError
from app.controllers.interns import InternController
from app.schema.add_new_division import AddNewDivision
from app.schema.set_intern_quota import SetInternQuota


intern_router = APIRouter(prefix='/intern')

@intern_router.get('/division')
async def get_intern_division():
    res = await InternController().get_divsion()
    return res

@intern_router.get('/quota')
async def get_intern_quota():
    res = await InternController().get_quota()
    return res

@intern_router.post('/quota')
async def set_intern_quota(request: Request):
    body = await request.body()
    json_data = body.decode('utf-8')
    data = json.loads(json_data)
    
    try : 
        req = SetInternQuota().load(data)
    except ValidationError as e :
        res = dict(
            message = "Validation error",
            errors = e.messages
        )
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="application/json",
            content=json.dumps(res)
        )
    res = await InternController().set_quota(req)
    return res


@intern_router.post('/division')
async def add_division(request: Request):
    body = await request.body()
    json_data = body.decode('utf-8')
    data = json.loads(json_data)
    
    try : 
        req = AddNewDivision().load(data)
    except ValidationError as e :
        res = dict(
            message = "Validation error",
            errors = e.messages
        )
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="application/json",
            content=json.dumps(res)
        )
    
    res = await InternController().add_division(req)
    return res