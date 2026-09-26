from typing import TypedDict, Literal
from pydantic import BaseModel


class TicketState(TypedDict):
    ticket_id: str
    user_id: str
    text: str
    language_checkpoint: str
    department: str
    urgency_level: str
    is_safety_grievance: bool
    status: Literal["open", "routed", "bumped", "escalated", "resolved"]
    assigned_email: str
    bump_count: int
    last_bump_time: str


class CreateTicketRequest(BaseModel):
    ticket_id: str
    user_id: str
    text: str
    created_at: str
