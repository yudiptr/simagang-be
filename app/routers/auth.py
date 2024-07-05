from fastapi import APIRouter, Request, Response, status
import json
from app.schema.user_profile import UserProfileSchema
from app.schema.user_account import UserAccountSchema
from marshmallow import ValidationError
from app.controllers.user import UserController

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/register")
async def register(request: Request):
    body = await request.body()
    json_data = body.decode('utf-8')
    data = json.loads(json_data)

    
    try : 
        validated_data = UserAccountSchema().load(data)
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
    res = await UserController().register_user(validated_data)
    return res

@auth_router.post("/login")
async def login(request: Request):
    body = await request.body()
    json_data = body.decode('utf-8')
    data = json.loads(json_data)

    
    try : 
        validated_data = UserAccountSchema().load(data)
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

    res = await UserController().login_user(validated_data)
    return res

@auth_router.post("/profile")
async def profile(request: Request):
    body = await request.body()
    json_data = body.decode('utf-8')
    data = json.loads(json_data)
    
    try : 
        validated_data = UserProfileSchema().load(data)
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
    

    print(validated_data)

