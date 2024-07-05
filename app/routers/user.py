from fastapi import APIRouter, status, Response, Request
from app.utils.decorators import login_required
from app.schema.user_profile import UserProfileSchema
from marshmallow import ValidationError
import json
from app.controllers.user import UserController

user_router = APIRouter(prefix="/user")


@user_router.post("/profile")
@login_required(
    token_types=["USER"],
    return_validation_data=True
)
async def update_profile(request: Request, validation_data: dict = None):
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
    
    res = await UserController().update_profile(data, validation_data)    
    return res