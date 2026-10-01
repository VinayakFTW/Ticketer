from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.user_routes import USER_ROUTER
from routes.session_routes import SESSION_ROUTER
from routes.ticket_routes import TICKET_ROUTER
from routes.ai_routes import AI_ROUTER
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

server.include_router(USER_ROUTER)
server.include_router(SESSION_ROUTER)
server.include_router(TICKET_ROUTER)
server.include_router(AI_ROUTER)
