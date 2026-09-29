from sqlalchemy.orm import Session
import json

from schemas.postgredb_schema import Ticket
from schemas.postgredb_schema import Engine
from utils.server_response import server_response
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR, NOT_FOUND

STATIC_TEXT = {
    "tickets_retrieved": "Tickets retrieved successfully",
    "no_tickets_found": "No tickets found",
    "ticket_retrieval_error": "Error retrieving tickets",
}


async def get_all_tickets():
    with Session(Engine) as s:
        try:
            tickets = s.query(Ticket).all()
            if tickets:
                ticket_list = [
                    {
                        "ticket_id": ticket.ticket_id,
                        "title": ticket.title,
                        "description": ticket.text,
                        "status": ticket.status,
                        "created_at": ticket.created_at.isoformat(),
                        "updated_at": ticket.updated_at.isoformat(),
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
