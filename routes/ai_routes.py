from fastapi import APIRouter

from constants.server_codes import SERVER_BASE_URL


AI_ROUTER = APIRouter(prefix=f"{SERVER_BASE_URL}/ai", tags=["AI API"])
