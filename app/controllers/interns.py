from app.utils.databases import session_scope
from fastapi import status, Response
from app.models.intern_division import InternDivision
from app.models.intern_quota import InternQuota
import json
from app.schema.intern_division import InternDivisionSchema


class InternController:

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