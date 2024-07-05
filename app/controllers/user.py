from app.utils.databases import session_scope
from fastapi import Response, status
from app.models.user_account import UserAccount
from app.models.user_profile import UserProfile
import json
from app.utils.jwt import create_access_token

class UserController:
    @staticmethod
    async def register_user(req: dict) -> Response:
        try :
            with session_scope() as session :
                data = session.query(UserAccount).filter_by(
                    username = req["username"]
                ).first()

                if data : 
                    res = dict(
                        message = "The username has been registered",
                        code = status.HTTP_400_BAD_REQUEST
                    )
                    return Response(
                        content=json.dumps(res),
                        media_type="application/json",
                        status_code= status.HTTP_400_BAD_REQUEST
                    )
                
                new_user = UserAccount(
                    username = req["username"],
                    password = req["password"]
                )

                session.add(new_user)
                session.commit()

                res = dict(
                    message = "Success register an account",
                    code = status.HTTP_200_OK
                )

                return Response(
                    content=json.dumps(res),
                    media_type="application/json",
                    status_code= status.HTTP_200_OK
                )
            
        except Exception as e :
            res = dict(
                    message = "Failed to register due to server",
                    code = status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                content=json.dumps(res),
                media_type="application/json",
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @staticmethod
    async def login_user(req: dict) -> Response: 
        try :
            with session_scope() as session :
                user: UserAccount = session.query(UserAccount).filter_by(
                    username = req["username"]
                ).first()
                
                if not user : 
                    res = dict(
                        message = "The username is not found",
                        code = status.HTTP_400_BAD_REQUEST
                    )
                    return Response(
                        content=json.dumps(res),
                        media_type="application/json",
                        status_code= status.HTTP_400_BAD_REQUEST
                    )
                
                if not user.check_password(req["password"]):
                    res = dict(
                        message = "The username/password didn't match",
                        code = status.HTTP_400_BAD_REQUEST
                    )
                    return Response(
                        content=json.dumps(res),
                        media_type="application/json",
                        status_code= status.HTTP_400_BAD_REQUEST
                    )
                
                # Create jwt token here, return
                access_token = create_access_token(
                    dict(
                        sub = user.id,
                        username = user.username,
                        is_complete = user.is_complete,
                        role = user.role
                    )
                )

                res = dict(
                        message = "Login success",
                        code = status.HTTP_200_OK,
                        data = {
                            "username" :user.username,
                            "role" : user.role,
                            "is_complete" : user.is_complete,
                            "access_token" : access_token,
                        }
                    )
                
                return Response(
                    content=json.dumps(res),
                    media_type="application/json",
                    status_code= status.HTTP_200_OK
                )

            
        except Exception as e :
            res = dict(
                message = "Failed to login due to server",
                code = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
            return Response(
                content=json.dumps(res),
                media_type="application/json",
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @staticmethod
    async def update_profile(req: dict, validation_data: dict) -> Response :
        try :
            with session_scope() as session :
                user_profile: UserProfile = session.query(UserProfile).filter_by(
                    user_account_id = validation_data["sub"]
                ).first()

                if user_profile:
                    for key, value in req.items():
                        setattr(user_profile, key, value)
                else:
                    req["user_account_id"] = validation_data["sub"]
                    user_profile = UserProfile(**req)

                    user_account: UserAccount = session.query(UserAccount).filter_by(
                        id = validation_data["sub"]
                    ).first()

                    user_account.is_complete = True

                    session.add(user_account)
                    
                session.add(user_profile)
                session.commit()


                
                res = dict(
                        message = "Success update profile",
                        code = status.HTTP_200_OK,
                        data = req
                    )
                
                return Response(
                    content=json.dumps(res),
                    media_type="application/json",
                    status_code= status.HTTP_200_OK
                )


        except Exception as e :
            res = dict(
                message = "Failed to update profile due to server",
                code = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
            return Response(
                content=json.dumps(res),
                media_type="application/json",
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR
            )