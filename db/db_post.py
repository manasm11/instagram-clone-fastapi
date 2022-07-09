from datetime import datetime

from sqlalchemy.orm import Session

from routers.post.schema import PostRequest

from .models import DbPost


def create_post(db: Session, request: PostRequest) -> DbPost:
    image_url_type = "absolute" if request.image_url.startswith("http") else "relative"
    post = DbPost(
        **request.dict(), timestamp=datetime.now(), image_url_type=image_url_type
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_all_post(db: Session) -> list:
    return db.query(DbPost).order_by(DbPost.timestamp.desc()).all()
