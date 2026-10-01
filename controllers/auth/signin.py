from types import SimpleNamespace
from sqlalchemy.orm import Session

from schemas.postgredb_schema import User, Engine
from schemas.request_schemas import LoginRequest
from utils.jwt_handler import create_access_token
from utils.server_response import server_response
from utils.pass_hash import verify_password
from constants.server_codes import NOT_FOUND, SUCCESS, INTERNAL_SERVER_ERROR

STATIC_TEXT = SimpleNamespace(
    login_success="Login successful",
    incorrect_info="Invalid username or password",
    login_failed="Login failed.",
)

def user_login(user_data: LoginRequest):
    with Session(Engine) as s:
        try:
            user = s.query(User).filter(User.email == user_data.email).first()
            if not user or not verify_password(plain_password=user_data.password, hashed_password=str(user.password)):
                return server_response(
                    status_code=NOT_FOUND,
                    message=STATIC_TEXT.incorrect_info,
                )
            print(f"User {user.email} logged in successfully with role {user.role.value}")

            access_token = create_access_token(user_id=user.id, role= user.role.value)
            return server_response(
                status_code=SUCCESS,
                message=STATIC_TEXT.login_success,
                data={
                    "access_token": access_token,
                    "token_type": "bearer",
                })
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.login_failed,
                data={"error": str(e)},
            )