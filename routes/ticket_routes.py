from fastapi import APIRouter

from controllers.tickets.get_all_tickets import get_all_tickets
from controllers.tickets.create_ticket import create_ticket

TICKET_ROUTER = APIRouter(route_prefix="/api/v1/tickets", tags=["Tickets API"])

TICKET_ROUTER.add_api_route("/all", get_all_tickets, methods=["GET"])
TICKET_ROUTER.add_api_route("/create", create_ticket, methods=["POST"])