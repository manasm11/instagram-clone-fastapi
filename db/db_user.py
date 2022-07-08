from sqlalchemy.orm import Session

import exceptions
from db.hashing import Hash
from db.models import DbUser
from routers.user.schemas import UserRequest


def create_user(db: Session, user: UserRequest):
    _user = db.query(DbUser).filter(DbUser.username == user.username).first()
    if _user:
        raise exceptions.UserExists(user.username)
    user = DbUser(username=user.username, password=Hash.bcrypt(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
