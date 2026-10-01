from fastapi import APIRouter

from constants.server_codes import SERVER_BASE_URL
from controllers.user.get_all_users import get_all_users
from controllers.user.create_user import create_user

USER_ROUTER = APIRouter(prefix=f"{SERVER_BASE_URL}/users", tags=["Users API"])

USER_ROUTER.add_api_route("/all", get_all_users, methods=["GET"])
USER_ROUTER.add_api_route("/create", create_user, methods=["POST"])
