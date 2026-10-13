from sqlalchemy.orm import Session
from types import SimpleNamespace

from schemas.postgredb_schema import User, Engine
from schemas.request_schemas import VerifyOtpRequest
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR, UNAUTHORIZED
from utils.server_response import server_response
from utils.redis import redis_client

STATIC_TEXT = SimpleNamespace(
    verified_success="Email verified successfully. You can now log in.",
    user_not_found="User not found",
    already_verified="User is already verified",
    invalid_or_expired_otp="Invalid or expired verification OTP",
    server_error="An error occurred during verification",
)

async def verify_signup(user_data: VerifyOtpRequest):
    data = user_data.model_dump()
    email = data.get("email", "").strip()
    submitted_otp = data.get("otp", "").strip()

    redis_key = f"otp:{email}"
    stored_otp = redis_client.get(redis_key)

    if not stored_otp or stored_otp != submitted_otp:
        return server_response(
            status_code=UNAUTHORIZED,
            message=STATIC_TEXT.invalid_or_expired_otp,
        )

    with Session(Engine) as s:
        try:
            user = s.query(User).filter_by(email=email).first()
            if not user:
                return server_response(
                    status_code=UNAUTHORIZED,
                    message=STATIC_TEXT.user_not_found,
                )

            if user.is_verified:
                redis_client.delete(redis_key)
                return server_response(
                    status_code=SUCCESS,
                    message=STATIC_TEXT.already_verified,
                )

            user.is_verified = True
            s.commit()
            redis_client.delete(redis_key)

            return server_response(
                status_code=SUCCESS,
                message=STATIC_TEXT.verified_success,
            )

        except Exception as e:
            s.rollback()
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.server_error,
            )