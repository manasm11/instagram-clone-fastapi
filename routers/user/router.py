from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import db_user, get_db

from .schema import UserRequest, UserResponse

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserRequest, db: Session = Depends(get_db)):
    new_user = db_user.create_user(db, user)
    return new_user
