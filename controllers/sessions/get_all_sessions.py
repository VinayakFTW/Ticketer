from types import SimpleNamespace
from sqlalchemy.orm import Session

from schemas.postgredb_schema import Sessions
from schemas.postgredb_schema import Engine
from utils.server_response import server_response
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR

STATIC_TEXT = SimpleNamespace(
    sessions_retrieved="Sessions retrieved successfully",
    session_retrieval_error="Error retrieving sessions",
)


async def get_all_sessions():
    with Session(Engine) as s:
        try:
            sessions = s.query(Sessions).all()
            session_list = [
                {
                    "session_id": session.session_id,
                    "messages": session.messages,
                }
                for session in sessions
            ]
            return server_response(
                status_code=SUCCESS,
                data={"sessions": session_list},
                message=STATIC_TEXT.sessions_retrieved,
            )
        except Exception as e:
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.session_retrieval_error,
            )
