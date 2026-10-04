from sqlalchemy.orm import Session
from types import SimpleNamespace

from schemas.postgredb_schema import User, Engine
from schemas.request_schemas import RefreshTokenRequest
from utils.jwt_handler import create_access_token, get_refresh_token_user
from utils.server_response import server_response
from constants.server_codes import SUCCESS,NOT_FOUND,INTERNAL_SERVER_ERROR

STATIC_TEXT = SimpleNamespace(
    refresh_success="Access token refreshed",
    invalid_refresh_token="Invalid or expired refresh token",
    user_not_found="User not found",
    refresh_failed="Failed to refresh access token",
)

def refresh_access_token(
    token_data: RefreshTokenRequest,
):

    try:

        user_id = get_refresh_token_user(
            token_data.refresh_token
        )

        if user_id is None:
            return server_response(
                status_code=NOT_FOUND,
                message=STATIC_TEXT.invalid_refresh_token,
            )

        with Session(Engine) as s:

            user = (
                s.query(User)
                .filter(User.id == user_id)
                .first()
            )

            if not user:
                return server_response(
                    status_code=NOT_FOUND,
                    message=STATIC_TEXT.user_not_found,
                )
            
            access_token = create_access_token(
                user_id=user.id,
                role=user.role.value,
            )

            return server_response(
                status_code=SUCCESS,
                message=STATIC_TEXT.refresh_success,
                data={
                    "access_token": access_token,
                    "token_type": "bearer",
                },
            )

    except Exception as e:

        return server_response(
            status_code=INTERNAL_SERVER_ERROR,
            message=STATIC_TEXT.refresh_failed,
            data={
                "error": str(e),
            },
        )