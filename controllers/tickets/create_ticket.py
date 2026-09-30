from types import SimpleNamespace
from sqlalchemy.orm import Session
from datetime import datetime
from utils.get_laya_decision import get_laya_decision

from schemas.postgredb_schema import Ticket, User
from schemas.postgredb_schema import Engine
from utils.server_response import server_response
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR

STATIC_TEXT = SimpleNamespace(
    ticket_created="Ticket created successfully",
    user_not_found="User not found",
    ticket_creation_error="Error creating ticket",
)

async def create_ticket(user_id, title, description):
    with Session(Engine) as s:
        s.begin()
        try:
            user = s.query(User).filter(User.user_id == user_id).first()
            if not user:
                return server_response(
                    status_code=INTERNAL_SERVER_ERROR,
                    message=STATIC_TEXT.user_not_found,
                )

            new_ticket = Ticket(
                user_id=user_id,
                title=title,
                text=description,
                status="open",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            s.add(new_ticket)
            s.commit()
            laya_decision = await get_laya_decision(title, description)

            return server_response(
                status_code=SUCCESS,
                data={
                    "ticket_id": new_ticket.ticket_id,
                    "laya_decision": laya_decision,
                },
                message=STATIC_TEXT.ticket_created,
            )
        except Exception as e:
            s.rollback()
            s.close()
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.ticket_creation_error,
            )
