from datetime import datetime

from sqlalchemy.orm import Session

from routers.post.schema import PostRequest

from .models import DbPost


def create_post(db: Session, request: PostRequest):
    post = DbPost(**request.dict(), timestamp=datetime.now())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
