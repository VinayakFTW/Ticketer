from fastapi import APIRouter

from constants.server_codes import SERVER_BASE_URL
from controllers.admin.user.get_all_users import get_all_users
from controllers.admin.user.get_subscription import get_user_subscription

ADMIN_USER_ROUTER = APIRouter(prefix=f"{SERVER_BASE_URL}/admin/users", tags=["Users API"])

ADMIN_USER_ROUTER.add_api_route("/all", get_all_users, methods=["GET"])
ADMIN_USER_ROUTER.add_api_route("/subscription/{user_id}", get_user_subscription, methods=["GET"])
