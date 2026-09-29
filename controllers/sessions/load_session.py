import json
from sqlalchemy.orm import Session

from schemas.postgredb_schema import Sessions
from schemas.postgredb_schema import Engine
from utils.server_response import server_response
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR, NOT_FOUND


STATIC_TEXT = {
    "session_loaded": "Session loaded successfully",
    "session_not_found": "Session not found",
    "session_load_error": "Error loading session",
}


async def load_session(session_id):
    with Session(Engine) as s:
        try:
            session = (
                s.query(Sessions).filter(Sessions.session_id == session_id).first()
            )
            if session:
                return server_response(
                    status_code=SUCCESS,
                    data=json.loads(session.messages),
                    message=STATIC_TEXT.session_loaded,
                )
            else:
                return server_response(
                    status_code=NOT_FOUND, message=STATIC_TEXT.session_not_found
                )
        except Exception as e:
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.session_load_error,
            )
