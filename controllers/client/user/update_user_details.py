from sqlalchemy.orm import Session
from types import SimpleNamespace
from typing import Annotated
from fastapi import Depends

from schemas.postgredb_schema import User, Engine
from schemas.request_schemas import UpdateUserRequest
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR, NOT_FOUND
from constants.enums import UserRole
from utils.server_response import server_response
from utils.pass_hash import hash_password
from middleware.dependencies import get_current_user_context

STATIC_TEXT = SimpleNamespace(
    user_details_retrieved="User details retrieved successfully",
    user_not_found="User not found",
    user_retrieval_error="Error retrieving user details",
    user_update_error="Error updating user details",
)


async def update_user_details(
    user: Annotated[dict, Depends(get_current_user_context)],
    user_data: UpdateUserRequest,
):
    with Session(Engine) as s:
        try:
            user_id = user.get("user_id")
            user_record = s.query(User).filter(User.id == user_id).first()
            if not user_record:
                return server_response(
                    status_code=NOT_FOUND, message=STATIC_TEXT.user_not_found
                )
            if user_data.name:
                user_record.name = user_data.name
            if user_data.email:
                user_record.email = user_data.email
            if user_data.password:
                user_record.password = hash_password(user_data.password)
            if user_data.institute:
                user_record.institute = user_data.institute
            if (user_record.role == UserRole.ADMIN or UserRole.STAFF) and user_data.role:
                user_record.role = user_data.role
                
            s.commit()
            return server_response(
                status_code=SUCCESS,
                data={
                    "user": {
                        "user_id": user_record.id,
                        "username": user_record.name,
                        "email": user_record.email,
                        "institute": user_record.institute,
                    }
                },
                message=STATIC_TEXT.user_details_retrieved,
            )
        except Exception as e:
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.user_retrieval_error,
            )
