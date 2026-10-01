from fastapi import Depends
from sqlalchemy.orm import Session
from types import SimpleNamespace
from typing import Annotated

from schemas.postgredb_schema import User, Engine
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR, NOT_FOUND
from utils.server_response import server_response
from middleware.dependencies import require_roles

STATIC_TEXT = SimpleNamespace(
    users_retrieved="Users retrieved successfully",
    users_not_found="No users found",
    user_retrieval_error="Error retrieving users",
)

async def get_all_users(user: Annotated[dict, Depends(require_roles(["ADMIN"]))]):
    with Session(Engine) as s:
        try:
            users = s.query(User).all()
            if not users:
                return server_response(
                    status_code=NOT_FOUND, message=STATIC_TEXT.users_not_found
                )

            return server_response(
                status_code=SUCCESS,
                data={
                    "users": [
                        {
                            "user_id": u.id,
                            "username": u.name,
                            "email": u.email,
                            "institute": u.institute,
                        }
                        for u in users
                    ]
                },
                message=STATIC_TEXT.users_retrieved,
            )
        except Exception as e:
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.user_retrieval_error,
                data={"error": str(e)},
            )
