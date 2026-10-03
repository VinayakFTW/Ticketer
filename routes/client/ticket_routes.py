from fastapi import APIRouter

from constants.server_codes import SERVER_BASE_URL
from controllers.client.tickets.create_ticket import create_ticket
from controllers.client.tickets.get_all_tickets_by_user import get_all_tickets_by_user

CLIENT_TICKET_ROUTER = APIRouter(
    prefix=f"{SERVER_BASE_URL}/client/tickets", tags=["Tickets API"]
)

CLIENT_TICKET_ROUTER.add_api_route("/all", get_all_tickets_by_user, methods=["GET"])
CLIENT_TICKET_ROUTER.add_api_route("/create", create_ticket, methods=["POST"])
