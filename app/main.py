from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Depends, Form
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


app = FastAPI()

s3 = boto3.client(
    's3',
    aws_access_key_id = Config.AWS_ACCESS_KEY,
    aws_secret_access_key = Config.AWS_SECRET_KEY
)

bucket_name = str(Config.AWS_BUCKET_NAME)

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(intern_router)

def handle_file_uploads(files: InternFiles):
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            raise HTTPException(status_code=404, detail="Bucket does not exist")
        else:
            raise HTTPException(status_code=500, detail="Error checking bucket")

    try:
        for key, file in files.dict().items():
            s3.upload_fileobj(file.file, bucket_name, file.filename)

        return True
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.post("/test-aws")
async def test_upload(
    division_id: int = Form(..., description="Division ID"),
    files: InternFiles = Depends()
):
    
    for attr_name, attr_value in files.__dict__.items():
        file_size = len(attr_value.file.read())

        if attr_name == "photo":
            if attr_value.content_type != FileTypes.PNG.value:
                raise HTTPException(status_code=400, detail=f"File {attr_name} must be PNG format")
        else:
            if attr_value.content_type != FileTypes.PDF.value:
                raise HTTPException(status_code=400, detail=f"File {attr_name} must be PDF format")
        if file_size > (3 * 1024 * 1024):  # 3MB limit
            raise HTTPException(status_code=400, detail=f"File {attr_name} exceeds 3MB limit")


    # Validate file types and upload files to S3
    if not handle_file_uploads(files):
        raise HTTPException(status_code=500, detail="Failed to upload files to S3")

    return JSONResponse(content={
        "message": "Files uploaded successfully",
        "division_id": division_id,
        "cv_filename": files.cv.filename,
        "cover_letter_filename": files.cover_letter.filename,
        "student_card_filename": files.student_card.filename,
        "photo_filename": files.photo.filename,
        "proposal_filename": files.proposal.filename,
    })

@app.get('/test-download-aws')
async def test_download():
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': 'interface.htm'
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