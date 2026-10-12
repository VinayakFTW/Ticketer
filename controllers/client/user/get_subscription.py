from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from types import SimpleNamespace
from typing import Annotated

from schemas.postgredb_schema import Subscription, User, Engine
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR, NOT_FOUND
from utils.server_response import server_response
from middleware.dependencies import get_current_user_context

STATIC_TEXT = SimpleNamespace(
    USER_NOT_FOUND="User not found"
)

def get_user_subscription(user: Annotated[dict, Depends(get_current_user_context)]):
    user_id = user.get("user_id")

    with Session(Engine) as db:
        try:
            user_record = db.query(User).filter(User.id == user_id).first()
            if not user_record:
                return server_response(status_code=NOT_FOUND, message=STATIC_TEXT.USER_NOT_FOUND)
        except Exception as e:
            raise HTTPException(status_code=INTERNAL_SERVER_ERROR)

        try:
            subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
            if not subscription:
                return server_response(
                        status_code=NOT_FOUND,
                        data={
                            "active": False
                        }
                    )
        except Exception as e:
            raise HTTPException(status_code=INTERNAL_SERVER_ERROR)

        return server_response(
            status_code=SUCCESS,
            data={
                "active": subscription.active
            }
        )