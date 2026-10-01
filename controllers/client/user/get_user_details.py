from sqlalchemy.orm import Session
from types import SimpleNamespace
from typing import Annotated
from fastapi import Depends

from schemas.postgredb_schema import User, Engine
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR, NOT_FOUND
from utils.server_response import server_response
from middleware.dependencies import get_current_user_context

STATIC_TEXT = SimpleNamespace(
    user_details_retrieved="User details retrieved successfully",
    user_not_found="User not found",
    user_retrieval_error="Error retrieving user details",
)

async def get_user_details(user: Annotated[dict, Depends(get_current_user_context)]):
    with Session(Engine) as s:
        try:
            user_id = user.get("user_id")
            user_record = s.query(User).filter(User.id == user_id).first()
            if not user_record:
                return server_response(
                    status_code=NOT_FOUND, message=STATIC_TEXT.user_not_found
                )

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
                data={"error": str(e)},
            )