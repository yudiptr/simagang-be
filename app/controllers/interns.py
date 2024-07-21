from datetime import datetime, timezone
import io
from typing import Dict, List
from app.choices.intern_registration_status import InternRegistrationStatus
from app.models.intern_finished import InternFinished
from app.models.intern_registration import InternRegistration
from app.schema.intern_registration import InternRegistrationSchema
from app.schema.intern_report import InternReportSchema
from app.schema.register_intern import InternFiles
from app.utils.databases import session_scope
from fastapi import HTTPException, UploadFile, status, Response
from app.models.intern_division import InternDivision
from app.models.intern_quota import InternQuota
import json
from app.schema.intern_division import InternDivisionSchema
import boto3
from app.config import Config
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from app.utils.boto3 import s3, bucket_name
class InternController:

    @staticmethod
    async def report_final_internship(
        validation_data: dict, 
        start_date: datetime,
        end_date: datetime,
        division_id : int,
        intern_byte: bytes,
        intern_certificate: UploadFile
    ):
        try:
            with session_scope() as session :   

                try:
                    current_time = datetime.now(timezone.utc)
                    milliseconds = current_time.strftime("%f")
                    filename = f"{validation_data['sub']}_{milliseconds}_{intern_certificate.filename}"
                    s3.upload_fileobj(io.BytesIO(intern_byte), bucket_name, filename)
                except ClientError as e:
                    raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
                

                new_report: InternFinished = InternFinished(
                    start_date = start_date,
                    end_date = end_date,
                    intern_certification = filename,
                    division_id = division_id,
                    user_account_id = validation_data["sub"]
                )

                session.add(new_report)
                session.commit()

                res = dict(
                        message = "Success report intern",
                        code = status.HTTP_200_OK
                    )
                
                return Response(
                    content=json.dumps(res),
                    media_type="application/json",
                )
           
        except Exception as e:
            res = dict(
                    message = "Failed to report internship due to server",
                    code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    messaga = str(e)
                )

            return Response(
                content=json.dumps(res),
                media_type="application/json",
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    async def get_my_applicants(validation_data: dict):
        try:
            with session_scope() as session:
                my_registration: List[InternRegistration] = session.query(
                    InternRegistration
                ).filter_by(
                    user_account_id = validation_data['sub'],
                ).all()
                
                serialiez_registration = InternRegistrationSchema(many = True).dump(my_registration)

                res = dict(
                        message = "Success get registration list",
                        code = status.HTTP_200_OK,
                        data = serialiez_registration
                    )
                
                return Response(
                    content=json.dumps(res),
                    media_type="application/json",
                    status_code= status.HTTP_200_OK
                )
            

        except Exception as e :
            res = dict(
                    message = "Failed to get list of my registration due to server",
                    code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    messaga = str(e)
                )

            return Response(
                content=json.dumps(res),
                media_type="application/json",
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    async def get_list_registration_intern():
        try:
            with session_scope() as session:
                regist_data: List[InternRegistration] = session.query(
                    InternRegistration
                ).filter_by(
                    status = InternRegistrationStatus.ON_PROCESS
                ).all()


                serialiez_registration = InternRegistrationSchema(many = True).dump(regist_data)
                res = dict(
                        message = "Success get registration list",
                        code = status.HTTP_200_OK,
                        data = serialiez_registration
                    )
                
                return Response(
                    content=json.dumps(res),
                    media_type="application/json",
                    status_code= status.HTTP_200_OK
                )
            

        except Exception as e :
            res = dict(
                    message = "Failed to get list intern registration due to server",
                    code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    messaga = str(e)
                )

            return Response(
                content=json.dumps(res),
                media_type="application/json",
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @staticmethod
    async def get_list_report_intern():
        try:
            with session_scope() as session:
                report_data: List[InternRegistration] = session.query(
                    InternFinished
                ).all()


                serialiez_registration = InternReportSchema(many = True).dump(report_data)
                res = dict(
                        message = "Success get report list",
                        code = status.HTTP_200_OK,
                        data = serialiez_registration
                    )
                
                return Response(
                    content=json.dumps(res),
                    media_type="application/json",
                    status_code= status.HTTP_200_OK
                )
            

        except Exception as e :
            res = dict(
                    message = "Failed to get list intern report due to server",
                    code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    messaga = str(e)
                )

            return Response(
                content=json.dumps(res),
                media_type="application/json",
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @staticmethod
    async def accept_intern_registration(validation_data: dict, registration_ids: List[int]):
        try:
            with session_scope() as session:

                intern_registration_list: List[InternRegistration] = session.query(
                    InternRegistration
                ).filter(
                    InternRegistration.id.in_(registration_ids),
                    InternRegistration.status == InternRegistrationStatus.ON_PROCESS,
                ).all()

                retrieved_ids = {registration.id for registration in intern_registration_list}
                failed_ids = set(registration_ids) - retrieved_ids

                if failed_ids:
                    message = f"Success to accept the registration, but the following IDs were not found or not in ON_PROCESS status: {', '.join(map(str, failed_ids))}"
                else:
                    message = "Success to accept the registration"

                for i in intern_registration_list:
                    i.status = InternRegistrationStatus.ACCEPTED
                    i.updated_with = validation_data["sub"]

                    session.add(i)

                session.commit()
                res = dict(
                        message = message,
                        code = status.HTTP_200_OK,
                    )
                
                return Response(
                    content=json.dumps(res),
                    media_type="application/json",
                    status_code= status.HTTP_200_OK
                )

        except Exception as e :
            res = dict(
                    message = "Failed to accept intern registration due to server",
                    code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    messaga = str(e)
                )

            return Response(
                content=json.dumps(res),
                media_type="application/json",
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @staticmethod
    async def reject_intern_registration(validation_data: dict, registration_ids: List[int]):
        try:
            with session_scope() as session:

                intern_registration_list: List[InternRegistration] = session.query(
                    InternRegistration
                ).filter(
                    InternRegistration.id.in_(registration_ids),
                    InternRegistration.status == InternRegistrationStatus.ON_PROCESS,
                ).all()

                retrieved_ids = {registration.id for registration in intern_registration_list}
                failed_ids = set(registration_ids) - retrieved_ids

                if failed_ids:
                    message = f"Success to reject the registration, but the following IDs were not found or not in ON_PROCESS status: {', '.join(map(str, failed_ids))}"
                else:
                    message = "Success to rejet the registration"

                for i in intern_registration_list:
                    i.status = InternRegistrationStatus.REJECTED
                    i.updated_with = validation_data["sub"]

                    quota_div: InternQuota = session.query(
                        InternQuota
                    ).filter_by(
                        division_id = i.division_id,
                        duration = i.duration
                    ).first()

                    quota_div.quota = quota_div.quota + 1
                    
                    session.add(quota_div)
                    session.add(i)

                session.commit()

                res = dict(
                        message = message,
                        code = status.HTTP_200_OK,
                    )
                
                return Response(
                    content=json.dumps(res),
                    media_type="application/json",
                    status_code= status.HTTP_200_OK
                )

        except Exception as e :
            res = dict(
                    message = "Failed to reject intern registration due to server",
                    code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    messaga = str(e)
                )

            return Response(
                content=json.dumps(res),
                media_type="application/json",
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    async def register_intern(division_id: int, intern_duration: str, files: Dict[str, bytes], validation_data: dict):
        try:
            with session_scope() as session :   
                division: InternDivision = session.query(InternDivision).filter_by(
                    id = division_id
                ).first()

                if not division :
                    res = dict(
                        message = f"The division with id {division_id} not found",
                        code = status.HTTP_400_BAD_REQUEST
                    )
                    return Response(
                        content=json.dumps(res),
                        media_type="application/json",
                        status_code= status.HTTP_400_BAD_REQUEST
                    )
                
                intern_quota: InternQuota = session.query(InternQuota).filter_by(
                    duration = intern_duration,
                    division_id = division_id
                ).first()

                if not intern_quota : 
                    res = dict(
                        message = f"Failed to get quota for division with id {division_id} not found",
                        code = status.HTTP_400_BAD_REQUEST
                    )
                    return Response(
                        content=json.dumps(res),
                        media_type="application/json",
                        status_code= status.HTTP_400_BAD_REQUEST
                    )
                
                if intern_quota.quota <= 0 :
                    res = dict(
                        message = f"Division {division.division_name} with duration {intern_duration} did not has any quota left",
                        code = status.HTTP_400_BAD_REQUEST
                    )
                    return Response(
                        content=json.dumps(res),
                        media_type="application/json",
                        status_code= status.HTTP_400_BAD_REQUEST
                    )
                
                try:
                    s3.head_bucket(Bucket=bucket_name)
                except ClientError as e:
                    error_code = int(e.response['Error']['Code'])
                    if error_code == 404:
                        raise HTTPException(status_code=404, detail="Bucket does not exist")
                    else:
                        raise HTTPException(status_code=500, detail="Error checking bucket")

                
                user_filenames = {}
                try:
                    for key, data in files.items():
                        current_time = datetime.now(timezone.utc)
                        milliseconds = current_time.strftime("%f")
                        filename = f"{validation_data['sub']}_{division.division_name}_{milliseconds}_{key}"

                        s3.upload_fileobj(io.BytesIO(data), bucket_name, filename)
                        user_filenames[key] = filename
                except ClientError as e:
                    raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

                intern_quota.quota = intern_quota.quota - 1
                session.add(intern_quota)

                registration_data = InternRegistration(
                    division_id = division_id,
                    duration = intern_duration,
                    user_account_id = validation_data['sub'],
                    cv = user_filenames['cv'],
                    cover_letter = user_filenames['cover_letter'],
                    student_card = user_filenames['student_card'],
                    photo = user_filenames['photo'],
                    proposal = user_filenames['proposal']
                )

                session.add(registration_data)
                session.commit()
                
                res = dict(
                        message = "Success register intern",
                        code = status.HTTP_200_OK
                    )
                
                return Response(
                    content=json.dumps(res),
                    media_type="application/json",
                )

                   
        except Exception as e:
            res = dict(
                    message = "Failed to register intern due to server",
                    code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    messaga = str(e)
                )

            return Response(
                content=json.dumps(res),
                media_type="application/json",
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @staticmethod
    async def set_quota(req:dict):
        try:
            with session_scope() as session:
                
                division = session.query(InternDivision).filter_by(
                    id = req["division_id"]
                ).first()

                if not division :
                    res = dict(
                        message = f"Division with id {req["division_id"]} is not found",
                        code = status.HTTP_400_BAD_REQUEST
                    )
                
                    return Response(
                        content=json.dumps(res),
                        media_type="application/json",
                        status_code= status.HTTP_400_BAD_REQUEST
                    )


                new_quota = InternQuota(
                    duration = req["duration"],
                    quota = req["quota"],
                    division_id = req["division_id"]
                )

                session.add(new_quota)
                session.commit()
                session.refresh(new_quota)

                res = dict(
                        message = "Success set intern quota",
                        code = status.HTTP_200_OK
                    )
                
                return Response(
                    content=json.dumps(res),
                    media_type="application/json",
                    status_code= status.HTTP_200_OK
                )

        except Exception as e :
            res = dict(
                    message = "Failed to create intern division due to server",
                    code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    messaga = str(e)
                )

            return Response(
                content=json.dumps(res),
                media_type="application/json",
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    async def add_division(req: dict):
        try:
            with session_scope() as session:

                division = session.query(InternDivision).filter_by(
                    division_name = req["division_name"]
                ).first()

                if division :
                    res = dict(
                        message = f"Division with name {req["division_name"]} is already registered",
                        code = status.HTTP_400_BAD_REQUEST
                    )
                
                    return Response(
                        content=json.dumps(res),
                        media_type="application/json",
                        status_code= status.HTTP_400_BAD_REQUEST
                    )
                

                new_division = InternDivision(
                    division_name = req["division_name"]
                )

                session.add(new_division)
                session.commit()
                session.refresh(new_division)

                serialize_division = InternDivisionSchema().dump(new_division)
                res = dict(
                        message = "Success create division",
                        code = status.HTTP_200_OK,
                        data = serialize_division
                    )
                
                return Response(
                    content=json.dumps(res),
                    media_type="application/json",
                    status_code= status.HTTP_200_OK
                )

        except Exception as e :
            res = dict(
                    message = "Failed to create intern division due to server",
                    code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    messaga = str(e)
                )

            return Response(
                content=json.dumps(res),
                media_type="application/json",
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    async def get_quota():
        try: 
            with session_scope() as session:
                quotas = session.query(InternQuota).join(InternDivision).all()

                division_quota_mapping = {}
                for quota in quotas:
                    division_name = quota.division.division_name
                    if division_name not in division_quota_mapping:
                        division_quota_mapping[division_name] = {}
                    division_quota_mapping[division_name][quota.duration] = quota.quota


                res = dict(
                        message = "Success get intern quota",
                        code = status.HTTP_200_OK,
                        data = division_quota_mapping
                    )
                
                return Response(
                    content=json.dumps(res),
                    media_type="application/json",
                    status_code= status.HTTP_200_OK
                )

        except Exception as e :
            res = dict(
                    message = "Failed to get list division due to server",
                    code = status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                content=json.dumps(res),
                media_type="application/json",
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    async def get_divsion():
        try:
            with session_scope() as session:
                division = session.query(InternDivision).all()

                serialize_division = InternDivisionSchema(many = True).dump(division)
                res = dict(
                        message = "Success get division",
                        code = status.HTTP_200_OK,
                        data = serialize_division
                    )
                
                return Response(
                    content=json.dumps(res),
                    media_type="application/json",
                    status_code= status.HTTP_200_OK
                )

        except Exception as e :
            res = dict(
                    message = "Failed to get list division due to server",
                    code = status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                content=json.dumps(res),
                media_type="application/json",
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )