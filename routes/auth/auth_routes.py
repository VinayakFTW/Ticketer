from fastapi import APIRouter

from constants.server_codes import SERVER_BASE_URL
from controllers.auth.signin import signin
from controllers.auth.signup import sign_up

AUTH_ROUTER = APIRouter(prefix=f"{SERVER_BASE_URL}/auth", tags=["Authentication API"])

AUTH_ROUTER.add_api_route("/signin", signin, methods=["POST"])
AUTH_ROUTER.add_api_route("/signup", sign_up, methods=["POST"])
