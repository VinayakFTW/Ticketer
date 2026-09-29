from fastapi import APIRouter

from controllers.sessions.load_session import load_session
from controllers.sessions.save_session import save_session
from controllers.sessions.get_all_sessions import get_all_sessions
from controllers.sessions.create_session import create_session

SESSION_ROUTER = APIRouter(route_prefix="/api/v1/sessions", tags=["Sessions API"])

SESSION_ROUTER.add_api_route("/all", get_all_sessions, methods=["GET"])
SESSION_ROUTER.add_api_route("/create", create_session, methods=["POST"])
SESSION_ROUTER.add_api_route("/load/{session_id}", load_session, methods=["GET"])
SESSION_ROUTER.add_api_route("/save/{session_id}", save_session, methods=["PUT"])