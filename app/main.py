from fastapi import FastAPI, Response, Request
from app.routers.user import user_router
from app.routers.auth import auth_router
from app.utils.databases import Base, engine
from app.utils.decorators import login_required
import json
from app.utils.jwt import create_access_token
from app.utils.databases import session_scope
from app.models.intern_quota import InternQuota
from app.models.intern_division import InternDivision
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(auth_router)
