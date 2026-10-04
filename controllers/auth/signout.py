from schemas.request_schemas import SignOutRequest
from utils.jwt_handler import revoke_refresh_token
from utils.server_response import server_response
from constants.server_codes import SUCCESS

def signout(token_data: SignOutRequest):
    revoke_refresh_token(token_data.refresh_token)

    return server_response(
        status_code=SUCCESS,
        message="Signed out successfully",
    )