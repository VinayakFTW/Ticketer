from sqlalchemy.orm import Session

from schemas.postgredb_schema import User
from schemas.postgredb_schema import Engine


async def get_all_users(user_id):
    with Session(Engine) as s:
        try:
            user = s.query(User).filter(User.user_id == user_id).first()
            if not user:
                return []

            sessions = s.query(User).all()
            return sessions
        except Exception as e:
            raise e
