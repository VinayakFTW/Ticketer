import logging
from sqlalchemy.orm import Session
from types import SimpleNamespace
from typing import Annotated
from fastapi import Depends

from schemas.postgredb_schema import Ticket, Engine, User
from constants.enums import UserRole
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR
from utils.server_response import server_response
from middleware.dependencies import require_roles, get_current_user_context

logger = logging.getLogger(__name__)

STATIC_TEXT = SimpleNamespace(
    tickets_retrieved="Tickets retrieved successfully",
    no_tickets_found="No tickets found",
    ticket_retrieval_error="Error retrieving tickets",
)


async def get_all_tickets(
    role: Annotated[dict, Depends(require_roles([UserRole.STAFF.value]))],
    user: Annotated[dict, Depends(get_current_user_context)],
):
    with Session(Engine) as s:
        try:
            user_record = s.query(User).filter(User.id == user["user_id"]).first()
            staff_email = user_record.email if user_record else None
            tickets = s.query(Ticket).order_by(Ticket.created_at.desc()).all()
            if tickets:
                ticket_list = [
                    {
                        "ticket_id": ticket.id,
                        "user_id": ticket.user_id,
                        "user_email": ticket.user.email if ticket.user else None,
                        "summary": ticket.summary,
                        "text": ticket.text,
                        "department": ticket.department,
                        "status": ticket.status,
                        "priority": ticket.priority,
                        "assigned_email": ticket.assigned_email,
                        "is_safety_grievance": ticket.is_safety_grievance,
                        "bump_count": ticket.bump_count,
                        "created_at": ticket.created_at.isoformat(),
                        "last_bump_time": ticket.last_bump_time.isoformat() if ticket.last_bump_time else None,
                    }
                    for ticket in tickets
                    if ticket.assigned_email == staff_email or ticket.assigned_email is None
                ]
                return server_response(
                    status_code=SUCCESS,
                    data={"tickets": ticket_list},
                )
            else:
                return server_response(
                    status_code=SUCCESS,
                    data={"tickets": []},
                    message=STATIC_TEXT.no_tickets_found,
                )
        except Exception as e:
            logger.error(f"Error retrieving staff tickets: {e}", exc_info=True)
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.ticket_retrieval_error,
                data=str(e),
            )

