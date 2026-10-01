from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    email: str
    password: str


class CreateTicketRequest(BaseModel):
    text: str


class UpdateTicketRequest(BaseModel):
    ticket_id: str
    text: Optional[str] = None
    status: str
    assigned_email: str
    bump_count: int
    last_bump_time: str


class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    institute: str


class CreateSessionRequest(BaseModel):
    session_id: str
    created_at: str
    last_accessed_at: str
    messages: str  # JSON string
