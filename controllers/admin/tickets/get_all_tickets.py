from sqlalchemy.orm import Session
from types import SimpleNamespace
from typing import Annotated
from fastapi import Depends

from schemas.postgredb_schema import Ticket, Engine
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR, NOT_FOUND
from utils.server_response import server_response
from middleware.dependencies import require_roles

STATIC_TEXT = SimpleNamespace(
    tickets_retrieved="Tickets retrieved successfully",
    no_tickets_found="No tickets found",
    ticket_retrieval_error="Error retrieving tickets",
)


async def get_all_tickets(user: Annotated[dict, Depends(require_roles(["ADMIN"]))]):
    with Session(Engine) as s:
        try:
            tickets = s.query(Ticket).all()
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
                        "last_bump_time": ticket.last_bump_time.isoformat() if ticket.last_bump_time else None,
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
