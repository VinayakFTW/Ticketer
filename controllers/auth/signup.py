from sqlalchemy.orm import Session
from types import SimpleNamespace
from datetime import datetime
import secrets
import string

from schemas.postgredb_schema import User
from schemas.postgredb_schema import Engine
from schemas.request_schemas import CreateUserRequest
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR, UNAUTHORIZED
from utils.server_response import server_response
from utils.pass_hash import hash_password
from utils.redis import redis_client
from services.email_service import send_verification_email

STATIC_TEXT = SimpleNamespace(
    user_created="User created successfully",
    user_creation_error="Error creating user",
)

OTP_EXPIRY_SECONDS = 5 * 60  # 5 minutes

async def sign_up(user_data: CreateUserRequest):
    user_data = user_data.model_dump()
    otp = "".join(secrets.choice(string.digits) for _ in range(6))
    email = user_data.get("email")
    with Session(Engine) as s:
        try:
            if user_data.get("email").split("@")[1] != "sitpune.edu.in":
                return server_response(
                    status_code=INTERNAL_SERVER_ERROR,
                    message="Email not from sitpune.edu.in domain",
                )
            existing_user = s.query(User).filter_by(email=email).first()
            if existing_user:
                if not existing_user.is_verified:
                    redis_client.setex(f"otp:{email}", OTP_EXPIRY_SECONDS, otp)
                    send_verification_email(email, otp)
                    return server_response(
                        status_code=SUCCESS,
                        message="A new verification OTP has been sent to your email.",
                    )
            verified_email_response = send_verification_email(user_data.get("email"), otp)
            if verified_email_response["status_code"] != SUCCESS:
                return server_response(
                    status_code=UNAUTHORIZED,
                    message=verified_email_response["message"],
                )
            redis_client.setex(f"otp:{email}", OTP_EXPIRY_SECONDS, otp)
            new_user = User(
                name=user_data.get("name"),
                email=user_data.get("email"),
                password=hash_password(user_data.get("password")),
                institute=user_data.get("institute"),
                created_at=datetime.now(),
                is_verified=False,
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
            redis_client.delete(f"otp:{email}")
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.user_creation_error
            )
