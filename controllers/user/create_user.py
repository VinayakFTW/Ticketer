from sqlalchemy.orm import Session
from types import SimpleNamespace
from schemas.postgredb_schema import User
from schemas.postgredb_schema import Engine
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR
from utils.server_response import server_response



STATIC_TEXT = SimpleNamespace(
    user_created="User created successfully",
    user_creation_error="Error creating user",
)

async def create_user(user_data):
    with Session(Engine) as s:
        s.begin()
        try:
            new_user = User(
                id=user_data.get("id"),
                name=user_data.get("name"),
                email=user_data.get("email"),
            )
            s.add(new_user)
            s.commit()
            s.close()
            return server_response(
                status_code=SUCCESS,
                data={"user_id": new_user.id},
                message=STATIC_TEXT.user_created,
            )
        except Exception as e:
            s.rollback()
            s.close()
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.user_creation_error,
            )
