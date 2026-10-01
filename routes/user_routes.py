from fastapi import APIRouter

from constants.server_codes import SERVER_BASE_URL
from controllers.user.get_all_users import get_all_users
from controllers.auth.signin import user_login
from controllers.auth.signup import sign_up

USER_ROUTER = APIRouter(prefix=f"{SERVER_BASE_URL}/users", tags=["Users API"])

USER_ROUTER.add_api_route("/all", get_all_users, methods=["GET"])
USER_ROUTER.add_api_route("/signin", user_login, methods=["POST"])
USER_ROUTER.add_api_route("/signup", sign_up, methods=["POST"])
