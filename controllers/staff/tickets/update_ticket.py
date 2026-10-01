from sqlalchemy.orm import Session
from datetime import datetime
from types import SimpleNamespace
from typing import Annotated
from fastapi import Depends

from schemas.postgredb_schema import Ticket, Engine
from schemas.request_schemas import UpdateTicketRequest
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR, NOT_FOUND
from utils.server_response import server_response
from middleware.dependencies import require_roles

STATIC_TEXT = SimpleNamespace(
    ticket_updated="Ticket updated successfully",
    ticket_not_found="Ticket not found",
    ticket_update_error="Error updating ticket",
)

async def update_ticket(user: Annotated[dict, Depends(require_roles(["STAFF"]))], update_request: UpdateTicketRequest):
    with Session(Engine) as s:
        try:
            ticket_record = s.query(Ticket).filter(Ticket.id == update_request.ticket_id).first()
            if not ticket_record:
                return server_response(
                    status_code=NOT_FOUND, message=STATIC_TEXT.ticket_not_found
                )
            if update_request.assigned_email is not None:
                ticket_record.assigned_email = update_request.assigned_email
            if update_request.status is not None:
                ticket_record.status = update_request.status
            ticket_record.last_bump_time = datetime.now()
            ticket_record.bump_count += 1
            s.commit()
            return server_response(
                status_code=SUCCESS,
                data={
                    "ticket": {
                        "ticket_id": ticket_record.id,
                        "status": ticket_record.status,
                        "created_at": ticket_record.created_at.isoformat(),
                        "last_bump_time": ticket_record.last_bump_time.isoformat(),
                        "bump_count": ticket_record.bump_count,
                    }
                },
                message=STATIC_TEXT.ticket_updated,
            )
        except Exception as e:
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.ticket_update_error
            )