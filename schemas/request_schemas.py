from pydantic import BaseModel


class CreateTicketRequest(BaseModel):
    ticket_id: str
    user_id: str
    text: str
    created_at: str


class UpdateTicketRequest(BaseModel):
    ticket_id: str
    status: str
    assigned_email: str
    bump_count: int
    last_bump_time: str


class CreateUserRequest(BaseModel):
    name: str
    email: str
    institute: str


class CreateSessionRequest(BaseModel):
    session_id: str
    created_at: str
    last_accessed_at: str
    messages: str  # JSON string
