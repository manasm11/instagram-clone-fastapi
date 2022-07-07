from sqlalchemy.orm import Session

import exceptions
from db.models import DbUser
from routers.schemas import UserRequest


def create_user(db: Session, user: UserRequest):
    user_with_username = (
        db.query(DbUser).filter(DbUser.username == user.username).first()
    )
    if user_with_username:
        raise exceptions.UserExists(user.username)
    user = DbUser(username=user.username, password=user.password)  # Hash the password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
