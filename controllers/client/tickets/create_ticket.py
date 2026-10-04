from types import SimpleNamespace
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Depends
from typing import Annotated

from schemas.request_schemas import CreateTicketRequest
from schemas.postgredb_schema import Ticket, User, Engine
from constants.enums import TicketStatus
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR
from utils.server_response import server_response
from utils.get_laya_decision import get_laya_decision
from utils.get_llm_response import get_ticket_summary
from middleware.dependencies import get_current_user_context

STATIC_TEXT = SimpleNamespace(
    ticket_created="Ticket created successfully",
    user_not_found="User not found",
    ticket_creation_error="Error creating ticket",
)


async def create_ticket(
    user: Annotated[dict, Depends(get_current_user_context)],
    ticket_data: CreateTicketRequest,
):
    laya_decision = await get_laya_decision(ticket_data.text)
    llm_summary = await get_ticket_summary(
        user_message=ticket_data.text, laya_decision=laya_decision
    )
    if not llm_summary.get("status_code") == SUCCESS:
        return server_response(
            status_code=INTERNAL_SERVER_ERROR, message=STATIC_TEXT.ticket_creation_error
        )
    with Session(Engine) as s:
        try:
            user = s.query(User).filter(User.id == user.get("user_id")).first()
            if not user:
                return server_response(
                    status_code=INTERNAL_SERVER_ERROR,
                    message=STATIC_TEXT.user_not_found,
                )

            new_ticket = Ticket(
                user_id=user.id,
                text=ticket_data.text,
                status=TicketStatus.OPEN,
                department=laya_decision.get("decision").get("department"),
                priority=laya_decision.get("decision").get("priority").upper(),
                summary=llm_summary.get("data").get("assistant_message"),
                is_safety_grievance=laya_decision.get("decision").get(
                    "is_safety_grievance"
                ),
                created_at=datetime.now(),
                last_bump_time=datetime.now(),
            )
            s.add(new_ticket)
            s.commit()
            s.refresh(new_ticket)

            return server_response(
                status_code=SUCCESS,
                data={
                    "ticket_id": new_ticket.id,
                    "summary": new_ticket.summary,
                    "laya_decision": laya_decision,
                },
                message=STATIC_TEXT.ticket_created,
            )
        except Exception as e:
            s.rollback()
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.ticket_creation_error
            )
