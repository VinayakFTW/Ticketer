from types import SimpleNamespace
from sqlalchemy.orm import Session
import json

from schemas.postgredb_schema import Sessions
from schemas.postgredb_schema import Engine
from utils.server_response import server_response
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR, NOT_FOUND

STATIC_TEXT = SimpleNamespace(
    session_saved="Session saved successfully",
    session_not_found="Session not found",
    session_save_error="Error saving session",
)


async def save_session(session_id, session_data):
    with Session(Engine) as s:
        try:
            session = (
                s.query(Sessions).filter(Sessions.session_id == session_id).first()
            )
            if session:
                session.messages = json.dumps(session_data)
                s.commit()
                return server_response(
                    status_code=SUCCESS,
                    message=STATIC_TEXT.session_saved,
                    data={"session_id": session_id, "session_data": session_data},
                )
            else:
                return server_response(
                    status_code=NOT_FOUND, message=STATIC_TEXT.session_not_found
                )
        except Exception as e:
            s.rollback()
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.session_save_error,
            )
