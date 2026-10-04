from fastapi import APIRouter

from constants.server_codes import SERVER_BASE_URL
from controllers.admin.tickets.get_all_tickets import get_all_tickets
from controllers.admin.tickets.create_ticket import create_ticket

ADMIN_TICKET_ROUTER = APIRouter(
    prefix=f"{SERVER_BASE_URL}/admin/tickets", tags=["Tickets API"]
)

ADMIN_TICKET_ROUTER.add_api_route("/all", get_all_tickets, methods=["GET"])
ADMIN_TICKET_ROUTER.add_api_route("/create", create_ticket, methods=["POST"])
