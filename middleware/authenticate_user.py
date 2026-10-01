from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from utils.jwt_handler import decode_access_token


class AuthContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user_id = None
        request.state.role = None

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()
            payload = decode_access_token(token)

            if payload:
                request.state.user_id = payload.get("sub")
                request.state.role = payload.get("role")

        response = await call_next(request)
        return response
