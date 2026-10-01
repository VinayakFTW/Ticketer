from fastapi import APIRouter

from constants.server_codes import SERVER_BASE_URL
from controllers.admin.user.get_all_users import get_all_users


ADMIN_USER_ROUTER = APIRouter(prefix=f"{SERVER_BASE_URL}/users", tags=["Users API"])

ADMIN_USER_ROUTER.add_api_route("/all", get_all_users, methods=["GET"])
