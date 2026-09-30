from types import SimpleNamespace
from sqlalchemy.orm import Session

from brain.llm_interface import LLMRouter
from utils.server_response import server_response
from constants.server_codes import SUCCESS, NOT_FOUND
from schemas.postgredb_schema import Ticket
from schemas.postgredb_schema import Engine

STATIC_TEXT = SimpleNamespace(
    ticket_not_found="Ticket not found for the given session_id.",
)


async def get_llm_response(session_id, user_message):
    with Session(Engine) as s:
        ticket = s.query(Ticket).filter(Ticket.ticket_id == session_id).first()

        if not ticket:
            return server_response(
                status_code=NOT_FOUND,
                message=STATIC_TEXT.ticket_not_found,
            )

        session_data = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ]
        }

        llm_router = LLMRouter(session_id=session_id)
        llm_response = await llm_router.generate_response(session_data, user_message)

        return server_response(
            status_code=SUCCESS,
            data={
                "assistant_message": llm_response.get("data").get("assistant_message"),
                "session_id": session_id,
            },
        )
