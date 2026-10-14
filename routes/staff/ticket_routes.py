from fastapi import APIRouter

from constants.server_codes import SERVER_BASE_URL
from controllers.staff.tickets.update_ticket import update_ticket
from controllers.staff.tickets.get_all_tickets import get_all_tickets

STAFF_TICKET_ROUTER = APIRouter(
    prefix=f"{SERVER_BASE_URL}/staff/tickets", tags=["Tickets API"]
)

STAFF_TICKET_ROUTER.add_api_route("/all", get_all_tickets, methods=["GET"])
STAFF_TICKET_ROUTER.add_api_route("/update/{ticket_id}", update_ticket, methods=["PUT"])
