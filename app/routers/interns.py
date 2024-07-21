from datetime import datetime, timezone
import io
import json
from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, Request, UploadFile, status
from marshmallow import ValidationError
from app.controllers.interns import InternController
from app.schema.add_new_division import AddNewDivision
from app.schema.register_intern import FileTypes, InternFiles
from app.schema.set_intern_quota import SetInternQuota
from app.schema.update_intern_registration import UpdateInternRegistration
from app.utils.decorators import login_required
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from app.utils.boto3 import s3, bucket_name

intern_router = APIRouter(prefix='/intern')

@intern_router.get('/division')
async def get_intern_division():
    res = await InternController().get_divsion()
    return res

@intern_router.get('/quota')
async def get_intern_quota():
    res = await InternController().get_quota()
    return res


@intern_router.get('/registration-list')
@login_required(
    token_types=["Admin"],
)
async def get_registration_list(
    request: Request
):
    res = await InternController().get_list_registration_intern()
    return res

@intern_router.get('/my-registration')
@login_required(
    token_types=["USER"],
    return_validation_data=True
)
async def get_registration_list(
    request: Request,
    validation_data : dict = None
):
    res = await InternController().get_my_applicants(validation_data=validation_data)
    return res

@intern_router.get('/report')
@login_required(
    token_types=["Admin"],
)
async def get_finished_report_list(
    request: Request
):
    res = await InternController().get_list_report_intern()
    return res

@intern_router.post('/final-report')
@login_required(
    token_types=["USER", "Admin"],
    return_validation_data=True
)
async def final_report_intern(
    request: Request,
    validation_data: dict = None,
    start_date: str = Form(..., description="Internship Start Date"),
    end_date: str = Form(..., description="Internship End Date"),
    division_id: int = Form(..., description="Division ID"),
    intern_certificate: UploadFile = File(..., media_type='application/pdf')
):
    

    intern_certificate_content = await intern_certificate.read()
    file_size = len(intern_certificate_content)
    if file_size > (3 * 1024 * 1024):  # 3MB limit
        raise HTTPException(status_code=400, detail="File intern certificate exceeds 3MB limit")

    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            raise HTTPException(status_code=404, detail="Bucket does not exist")
        else:
            raise HTTPException(status_code=500, detail="Error checking bucket")
    
    try:
        start_date = datetime.strptime(start_date, "%d/%m/%Y")
        end_date = datetime.strptime(end_date, "%d/%m/%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use dd/mm/yyyy")

    res = await InternController().report_final_internship(
        validation_data,
        start_date,
        end_date,
        division_id,
        intern_certificate_content,
        intern_certificate
    )
    return res

@intern_router.patch('/accept')
@login_required(
    token_types=["Admin"],
    return_validation_data=True
)
async def accept_intern_registration(
    request: Request,
    validation_data: dict = None
):
    
    body = await request.body()
    json_data = body.decode('utf-8')
    data = json.loads(json_data)
    
    try : 
        req = UpdateInternRegistration().load(data)
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
    
    res = await InternController().accept_intern_registration(
        validation_data,
        req["registration_ids"]
    )
    return res

@intern_router.patch('/reject')
@login_required(
    token_types=["Admin"],
    return_validation_data=True
)
async def reject_intern_registration(
    request: Request,
    validation_data: dict = None
):
    body = await request.body()
    json_data = body.decode('utf-8')
    data = json.loads(json_data)
    
    try : 
        req = UpdateInternRegistration().load(data)
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
    
    res = await InternController().reject_intern_registration(
        validation_data,
        req["registration_ids"]
    )
    return res

@intern_router.post('/register')
@login_required(return_validation_data=True, token_types=["USER"])
async def register_intern(
        request: Request,
        validation_data: dict = None,
        division_id: int = Form(..., description="Division ID"),
        intern_duration: str = Form(..., description="Intern Duration"),
        files: InternFiles = Depends()
    ):


    file_data = {}
    for attr_name, attr_value in files.__dict__.items():
        file_content = await attr_value.read()  # Await the read operation
        file_data[attr_name] = file_content  # Store the file content bytes

        if attr_name == "photo":
            if attr_value.content_type != FileTypes.PNG.value:
                raise HTTPException(status_code=400, detail=f"File {attr_name} must be PNG format")
        else:
            if attr_value.content_type != FileTypes.PDF.value:
                raise HTTPException(status_code=400, detail=f"File {attr_name} must be PDF format")
        
        if len(file_content) > (3 * 1024 * 1024):  # 3MB limit
            raise HTTPException(status_code=400, detail=f"File {attr_name} exceeds 3MB limit")
        
    res = await InternController().register_intern(
        division_id,
        intern_duration,
        file_data,
        validation_data
    )
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