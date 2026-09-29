from pydantic import BaseModel


class CreateTicketRequest(BaseModel):
    ticket_id: str
    user_id: str
    text: str
    created_at: str
