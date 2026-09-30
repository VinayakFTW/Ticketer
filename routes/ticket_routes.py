from fastapi import APIRouter

from constants.server_codes import SERVER_BASE_URL
from controllers.tickets.get_all_tickets import get_all_tickets
from controllers.tickets.create_ticket import create_ticket

TICKET_ROUTER = APIRouter(prefix=f"{SERVER_BASE_URL}/tickets", tags=["Tickets API"])

TICKET_ROUTER.add_api_route("/all", get_all_tickets, methods=["GET"])
TICKET_ROUTER.add_api_route("/create", create_ticket, methods=["POST"])