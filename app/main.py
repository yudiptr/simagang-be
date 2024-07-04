from fastapi import FastAPI, Response, Request
from app.routers.user import user_router
from app.routers.auth import auth_router
from app.utils.databases import Base, engine
from app.utils.decorators import login_required
import json
from app.utils.jwt import create_access_token

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
async def root():

    token = create_access_token(
        data= { 
            "role" : "USER",
        }
    )
    return Response(
        status_code=200,
        content=json.dumps(token),
        media_type="application/json"
    )

@app.get("/extract")
@login_required(
    return_validation_data=True,
    token_types=["USER"]
)
async def extract(request:Request,  validation_data: dict = None):

    token = validation_data
    return Response(
        status_code=200,
        content=json.dumps(token),
        media_type="application/json"
    )
