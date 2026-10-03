from sqlalchemy.orm import Session
from types import SimpleNamespace
from typing import Annotated
from fastapi import Depends

from schemas.postgredb_schema import Ticket, Engine
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR, NOT_FOUND
from utils.server_response import server_response
from middleware.dependencies import get_current_user_context

STATIC_TEXT = SimpleNamespace(
    tickets_retrieved="Tickets retrieved successfully",
    no_tickets_found="No tickets found",
    ticket_retrieval_error="Error retrieving tickets",
)


async def get_all_tickets_by_user(
    user: Annotated[dict, Depends(get_current_user_context)],
):
    with Session(Engine) as s:
        try:
            tickets = (
                s.query(Ticket).filter(Ticket.user_id == user.get("user_id")).all()
            )
            if tickets:
                ticket_list = [
                    {
                        "ticket_id": ticket.id,
                        "summary": ticket.summary,
                        "text": ticket.text,
                        "department": ticket.department,
                        "status": ticket.status,
                        "priority": ticket.priority,
                        "bump_count": ticket.bump_count,
                        "created_at": ticket.created_at.isoformat(),
                        "last_bump_time": ticket.last_bump_time.isoformat(),
                    }
                    for ticket in tickets
                ]
                return server_response(
                    status_code=SUCCESS,
                    data={"tickets": ticket_list},
                )
            else:
                return server_response(
                    status_code=NOT_FOUND, message=STATIC_TEXT.no_tickets_found
                )
        except Exception as e:
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.ticket_retrieval_error,
            )
