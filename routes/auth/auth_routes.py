from fastapi import APIRouter

from constants.server_codes import SERVER_BASE_URL
from controllers.auth.signin import signin
from controllers.auth.signup import sign_up
from controllers.auth.signout import signout
from controllers.auth.refresh import refresh_access_token
from controllers.auth.verify_email import verify_signup

AUTH_ROUTER = APIRouter(prefix=f"{SERVER_BASE_URL}/auth", tags=["Authentication API"])

AUTH_ROUTER.add_api_route("/signin", signin, methods=["POST"])
AUTH_ROUTER.add_api_route("/signup", sign_up, methods=["POST"])
AUTH_ROUTER.add_api_route("/signout", signout, methods=["POST"])
AUTH_ROUTER.add_api_route("/refresh", refresh_access_token, methods=["POST"])
AUTH_ROUTER.add_api_route("/verify", verify_signup, methods=["POST"])