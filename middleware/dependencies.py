from typing import Annotated, List
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.jwt_handler import decode_access_token

security = HTTPBearer()

def get_current_user_context(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    request: Request,
) -> dict:
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing, invalid, or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = int(payload["sub"])
    role = str(payload.get("role", "")).strip().upper()

    request.state.user_id = user_id
    request.state.role = role

    return {"user_id": user_id, "role": role}

def require_roles(allowed_roles: List[str]):
    def role_checker(
        user: Annotated[dict, Depends(get_current_user_context)],
    ) -> str:
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles}",
            )
        return user["role"]

    return role_checker