from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt

from brain.config import ENVIRONMENT_VARIABLES

SECRET_KEY = ENVIRONMENT_VARIABLES.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(user_id: int, role: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "role": str(role),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "sub" in payload and payload["sub"] is not None:
            payload["user_id"] = int(payload["sub"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None