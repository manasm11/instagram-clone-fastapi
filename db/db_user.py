from sqlalchemy.orm import Session

import exceptions
from db.hashing import Hash
from db.models import DbUser
from routers.user.schemas import UserRequest


def create_user(db: Session, user: UserRequest):
    user_with_username = (
        db.query(DbUser).filter(DbUser.username == user.username).first()
    )
    if user_with_username:
        raise exceptions.UserExists(user.username)
    user = DbUser(username=user.username, password=Hash.bcrypt(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
