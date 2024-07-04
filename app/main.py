from fastapi import FastAPI
from app.routers.user import user_router
from app.routers.auth import auth_router
from app.utils.databases import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(auth_router)