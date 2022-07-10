from sqlalchemy.orm import Session

import exceptions
from db.hashing import Hash
from db.models import DbUser
from routers.user.schema import UserRequest


def create_user(db: Session, user: UserRequest):
    _user = db.query(DbUser).filter(DbUser.username == user.username).first()
    if _user:
        raise exceptions.UserExists(user.username)
    user = DbUser(username=user.username, password=Hash.bcrypt(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_username(db: Session, username: str):
    users_query = db.query(DbUser).filter(DbUser.username == username)
    users = users_query.all()
    if len(users) == 0:
        raise exceptions.UserNotExists(username)
    if len(users) > 1:
        raise exceptions.MultipleUsersWithSameUsername(username, len(users))
    return users_query.first()
