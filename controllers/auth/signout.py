from utils.jwt_handler import revoke_refresh_token
from utils.server_response import server_response
from constants.server_codes import SUCCESS

def signout(refresh_token: str):
    revoke_refresh_token(refresh_token)

    return server_response(
        status_code=SUCCESS,
        message="Signed out successfully",
    )