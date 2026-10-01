from sqlalchemy.orm import Session
from types import SimpleNamespace
from datetime import datetime

from schemas.postgredb_schema import User
from schemas.postgredb_schema import Engine
from schemas.request_schemas import CreateUserRequest
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR
from utils.server_response import server_response


STATIC_TEXT = SimpleNamespace(
    user_created="User created successfully",
    user_creation_error="Error creating user",
)


async def create_user(user_data: CreateUserRequest):
    with Session(Engine) as s:
        try:
            user_data = user_data.model_dump()
            print(f"Creating user with data: {user_data}")
            new_user = User(
                name=user_data.get("name"),
                email=user_data.get("email"),
                institute=user_data.get("institute"),
                created_at=datetime.now(),
            )
            s.add(new_user)
            s.commit()
            s.refresh(new_user)
            return server_response(
                status_code=SUCCESS,
                data={"user": new_user.id},
                message=STATIC_TEXT.user_created,
            )
        except Exception as e:
            s.rollback()
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.user_creation_error,
                data={"error": str(e)},
            )
