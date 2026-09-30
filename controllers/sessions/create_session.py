from sqlalchemy.orm import Session
from datetime import datetime
import json
import uuid
from types import SimpleNamespace

from brain.config import SYSTEM_PROMPT
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR
from schemas.postgredb_schema import Sessions
from schemas.postgredb_schema import Engine
from utils.server_response import server_response


STATIC_TEXT = SimpleNamespace(
    session_created="Session created successfully",
    session_creation_error="Error creating session",
)


async def create_session():
    session = Sessions(
        session_id=uuid.uuid4(),
        created_at=datetime.now(),
        last_accessed_at=datetime.now(),
        messages=json.dumps(
            {"messages": [{"role": "system", "content": SYSTEM_PROMPT}]}
        ),
    )
    with Session(Engine) as s:
        s.begin()
        try:
            s.add(session)
        except Exception as e:
            s.rollback()
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.session_creation_error,
            )
        else:
            s.commit()
            s.close()
            return server_response(
                status_code=SUCCESS,
                data={"session_id": session.session_id},
                message=STATIC_TEXT.session_created,
            )
