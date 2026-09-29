from sqlalchemy.orm import Session
from datetime import datetime
from utils.get_laya_decision import get_laya_decision

from schemas.postgredb_schema import Ticket, User
from schemas.postgredb_schema import Engine
from utils.server_response import server_response
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR


async def create_ticket(user_id, title, description):
    with Session(Engine) as s:
        s.begin()
        try:
            user = s.query(User).filter(User.user_id == user_id).first()
            if not user:
                return server_response(
                    status_code=INTERNAL_SERVER_ERROR,
                    message="User not found",
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
                message="Ticket created successfully",
            )
        except Exception as e:
            s.rollback()
            s.close()
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message="Error creating ticket",
            )
