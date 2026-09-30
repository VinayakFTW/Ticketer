from sqlalchemy.orm import Session
from types import SimpleNamespace

from schemas.postgredb_schema import User
from schemas.postgredb_schema import Engine
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR, NOT_FOUND
from utils.server_response import server_response

STATIC_TEXT = SimpleNamespace(
    users_retrieved="Users retrieved successfully",
    users_not_found="No users found",
    user_retrieval_error="Error retrieving users",
)

async def get_all_users():
    with Session(Engine) as s:
        try:
            users = s.query(User).all()
            if not users:
                return server_response(
                    status_code=NOT_FOUND, message=STATIC_TEXT.users_not_found
                )

            return server_response(
                status_code=SUCCESS,
                data={"users": [{"user_id": u.user_id, "username": u.username} for u in users]},
                message=STATIC_TEXT.users_retrieved,
            )
        except Exception as e:
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.user_retrieval_error,
            )
