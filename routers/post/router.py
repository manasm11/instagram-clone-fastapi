from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_post
from db.database import get_db

from .schema import PostRequest, PostResponse

router = APIRouter(prefix="/post", tags=["Post"])


@router.post("/", status_code=201, response_model=PostResponse)
async def create_post(postRequest: PostRequest, db: Session = Depends(get_db)):
    post = db_post.create_post(db, postRequest)
    return post
