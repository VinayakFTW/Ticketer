from  fastapi import Depends
from sqlalchemy.orm import Session
from types import SimpleNamespace
from typing import Annotated
from datetime import datetime

from schemas.postgredb_schema import Subscription, User, Engine
from schemas.request_schemas import UpdateSubscriptionRequest
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR, NOT_FOUND
from constants.enums import UserRole
from utils.server_response import server_response
from middleware.dependencies import require_roles

STATIC_TEXT = SimpleNamespace(
    USER_NOT_FOUND="User not found",
    ERROR_UPDATING_SUBSCRIPTION="Error updating subscription"
)

async def update_user_subscription(user_id: int, SubscriptionRequest: UpdateSubscriptionRequest, role: Annotated[dict, Depends(require_roles([UserRole.ADMIN.value]))]):
    active = SubscriptionRequest.active
    with Session(Engine) as db:
        try:
            user_record = db.query(User).filter(User.id == user_id).first()
            if not user_record:
                return server_response(
                    status_code=NOT_FOUND,
                    message= STATIC_TEXT.USER_NOT_FOUND
                )
            subscription = db.query(Subscription).filter(Subscription.user_id == user_id).first()
            if not subscription:
                subscription = Subscription(user_id=user_id, active=active,renewed_at=datetime.now())
                db.add(subscription)
            else:
                subscription.active = active
                subscription.renewed_at = datetime.now()
            db.commit()
            return server_response(
                        status_code=SUCCESS,
                        data={
                            "user_id": user_id,
                            "active": active
                        }
                    )
        except Exception as e:
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
                message=STATIC_TEXT.ERROR_UPDATING_SUBSCRIPTION
            )