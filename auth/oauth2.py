from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from db import db_user, get_db

oauth2_scheme = OAuth2PasswordBearer("login")

SECRET_KEY = "89ac45065956f753ae69785d3effe5cffbc093e72b3e9aa925bc7c6d8201be60"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_access_token(data: dict):
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_jwt = jwt.encode({**data, "exp": exp}, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("jc0-w9u4")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db_user.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user
