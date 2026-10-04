from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
import secrets
import hashlib

from utils.redis import redis_client
from brain.config import ENVIRONMENT_VARIABLES

SECRET_KEY = ENVIRONMENT_VARIABLES.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_SECONDS = 30 * 24 * 60 * 60

def create_access_token(
    user_id: int, role: str, expires_delta: Optional[timedelta] = None
) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "role": str(role),
        "exp": expire,
        "jti": secrets.token_urlsafe(32),
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def hash_refresh_token(refresh_token: str) -> str:
    return hashlib.sha256(refresh_token.encode()).hexdigest()


def store_refresh_token(user_id: int):
    refresh_token = secrets.token_urlsafe(64)
    token_hash = hash_refresh_token(refresh_token)

    redis_client.setex(
        f"refresh_token:{token_hash}",
        REFRESH_TOKEN_EXPIRE_SECONDS,
        str(user_id),
    )
    return refresh_token


def get_refresh_token_user(refresh_token: str):
    token_hash = hash_refresh_token(refresh_token)
    user_id = redis_client.get(
        f"refresh_token:{token_hash}"
    )

    if user_id is None:
        return None

    return int(user_id)


def revoke_refresh_token(refresh_token: str):
    token_hash = hash_refresh_token(refresh_token)
    redis_client.delete(
        f"refresh_token:{token_hash}"
    )


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            return None
        if "sub" in payload and payload["sub"] is not None:
            payload["user_id"] = int(payload["sub"])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
