from sqlalchemy.orm import Session

from db.models import DbUser
from routers.schemas import UserRequest


def create_user(db: Session, user: UserRequest):
    user = DbUser(username=user.username, password=user.password)  # Hash the password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
