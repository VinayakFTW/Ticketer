from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    email: str
    password: str


class CreateTicketRequest(BaseModel):
    text: str


class UpdateTicketRequest(BaseModel):
    ticket_id: int
    status: Optional[str] = None
    assigned_email: Optional[str] = None
    last_bump_time: Optional[str] = None


class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    institute: str


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    institute: Optional[str] = None