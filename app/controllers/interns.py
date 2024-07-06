from app.utils.databases import session_scope
from fastapi import status, Response
from app.models.intern_division import InternDivision
from app.models.intern_quota import InternQuota
import json
from app.schema.intern_division import InternDivisionSchema


class InternController:
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