from datetime import datetime

from sqlalchemy.orm import Session

import exceptions
from routers.post.schema import PostRequest

from .models import DbPost, DbUser


def create_post(db: Session, request: PostRequest, current_user_id: int) -> DbPost:
    post = DbPost(
        **request.dict(), timestamp=datetime.now(), creator_id=current_user_id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_all_post(db: Session) -> list:
    return db.query(DbPost).order_by(DbPost.timestamp.desc()).all()


def delete_post(db: Session, post_id: int, user_id: int) -> None:
    post: DbPost = db.query(DbPost).get(post_id)
    if post is None:
        raise exceptions.PostNotExists(post_id)
    if post.creator_id != user_id:
        raise exceptions.NotAuthorized("to delete this post")
    db.delete(post)
    db.commit()
