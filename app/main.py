from datetime import datetime, timezone
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Depends, Form
from app.controllers.interns import InternController
from app.routers.user import user_router
from app.routers.auth import auth_router
from app.routers.interns import intern_router
from app.utils.databases import Base, engine
from app.utils.decorators import login_required
import json
from app.utils.jwt import create_access_token
from app.config import Config
from app.utils.databases import session_scope
from app.models.intern_quota import InternQuota
from app.models.intern_division import InternDivision
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from app.schema.register_intern import InternFiles
from fastapi.responses import JSONResponse
from app.schema.register_intern import FileTypes
from app.utils.boto3 import  bucket_name, s3
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(intern_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://simagang-fe.vercel.app"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/generate-download-link')
async def test_download():
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': 'CV_Yudi Putra Sabri (3).pdf'
            },
            ExpiresIn=600,
        )
        return {"url": url}
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="AWS credentials not found")
    except PartialCredentialsError:
        raise HTTPException(status_code=403, detail="Incomplete AWS credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post('/post-aws')
@login_required(
    token_types=["USER"],
    return_validation_data=True
)
async def test_download(
    request: Request,
    validation_data: dict = None,
    division_id: int = Form(..., description="Division ID"),
    intern_duration: str = Form(..., description="Intern Duration"),
    files: InternFiles = Depends()
):
    res = await InternController().register_intern(
        division_id,
        intern_duration,
        files,
        validation_data
    )
    return res