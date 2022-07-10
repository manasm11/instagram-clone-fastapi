from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import exceptions
from auth import create_access_token
from db import DbUser, Hash, get_db

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if not user:
        raise exceptions.UserNotExists(request.username)
    if not Hash.verify(request.password, user.password):
        raise exceptions.IncorrectPassword()

    access_token = create_access_token(data={"jc0-w9u4": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "user_id": user.id,
    }
