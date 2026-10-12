from fastapi import APIRouter

from constants.server_codes import SERVER_BASE_URL
from controllers.client.user.get_user_details import get_user_details
from controllers.client.user.update_user_details import update_user_details
from controllers.client.user.get_subscription import get_user_subscription

CLIENT_USER_ROUTER = APIRouter(
    prefix=f"{SERVER_BASE_URL}/client/users", tags=["Users API"]
)

CLIENT_USER_ROUTER.add_api_route("/details", get_user_details, methods=["GET"])
CLIENT_USER_ROUTER.add_api_route("/update", update_user_details, methods=["PUT"])
CLIENT_USER_ROUTER.add_api_route("/subscription", get_user_subscription, methods=["GET"])