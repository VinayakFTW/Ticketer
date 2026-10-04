from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth.auth_routes import AUTH_ROUTER
from routes.admin.user_routes import ADMIN_USER_ROUTER
from routes.admin.ticket_routes import ADMIN_TICKET_ROUTER
from routes.staff.ticket_routes import STAFF_TICKET_ROUTER
from routes.client.user_routes import CLIENT_USER_ROUTER
from routes.client.ticket_routes import CLIENT_TICKET_ROUTER
from routes.client.ai_routes import AI_ROUTER
from middleware.authenticate_user import AuthContextMiddleware

server = FastAPI(title="Ticketer Server", version="0.1.0")

server.add_middleware(AuthContextMiddleware)

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

server.include_router(AUTH_ROUTER)
server.include_router(ADMIN_USER_ROUTER)
server.include_router(ADMIN_TICKET_ROUTER)
server.include_router(STAFF_TICKET_ROUTER)
server.include_router(CLIENT_USER_ROUTER)
server.include_router(CLIENT_TICKET_ROUTER)
server.include_router(AI_ROUTER)
