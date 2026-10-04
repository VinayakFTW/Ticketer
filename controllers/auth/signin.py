from types import SimpleNamespace
from sqlalchemy.orm import Session

from schemas.postgredb_schema import User, Engine
from schemas.request_schemas import LoginRequest
from utils.jwt_handler import create_access_token, store_refresh_token
from utils.server_response import server_response
from utils.pass_hash import verify_password
from constants.server_codes import NOT_FOUND, SUCCESS, INTERNAL_SERVER_ERROR

STATIC_TEXT = SimpleNamespace(
    login_success="Login successful",
    incorrect_info="Invalid username or password",
    login_failed="Login failed.",
)


def signin(user_data: LoginRequest):
    with Session(Engine) as s:
        try:
            user = s.query(User).filter(User.email == user_data.email).first()
            if not user or not verify_password(
                plain_password=user_data.password, hashed_password=str(user.password)
            ):
                return server_response(
                    status_code=NOT_FOUND,
                    message=STATIC_TEXT.incorrect_info,
                )

            access_token = create_access_token(user_id=user.id, role=user.role.value)
            refresh_token = store_refresh_token(user_id=user.id)
            return server_response(
                status_code=SUCCESS,
                message=STATIC_TEXT.login_success,
                data={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer",
                },
            )

        except Exception as e:
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.login_failed
            )
