from types import SimpleNamespace
from sqlalchemy.orm import Session
import json

from brain.llm_interface import LLMRouter
from utils.server_response import server_response
from constants.server_codes import INTERNAL_SERVER_ERROR, SUCCESS, NOT_FOUND
from schemas.postgredb_schema import Ticket
from schemas.postgredb_schema import Engine

STATIC_TEXT = SimpleNamespace(
    ticket_not_found="Ticket not found.",
)


async def generate_assistant_response(ticket_id, user_message):
    llm = LLMRouter()
    with Session(Engine) as s:
        ticket = s.query(Ticket).filter(Ticket.id == ticket_id).first()

        if not ticket:
            return server_response(
                status_code=NOT_FOUND,
                message=STATIC_TEXT.ticket_not_found,
            )

    llm_response = await llm.generate_response(user_message)
    return {
        "status_code": SUCCESS,
        "data": {
            "assistant_message": llm_response.get("assistant_message"),
            "ticket_id": ticket_id,
        },
    }


async def get_ticket_summary(user_message, laya_decision):
    llm = LLMRouter()
    llm_response = await llm.generate_summary(user_message, laya_decision)
    if not llm_response.get("status_code") == SUCCESS:
        return {
            "status_code": INTERNAL_SERVER_ERROR,
        }
    return {
        "status_code": SUCCESS,
        "data": {
            "assistant_message": llm_response.get("assistant_message"),
        },
    }
