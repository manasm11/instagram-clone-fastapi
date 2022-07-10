from datetime import datetime

from sqlalchemy.orm import Session

from db import DbComment
from routers.post.schema import CommentRequest


def create_comment(
    db: Session, request: CommentRequest, post_id: int, current_user_id: int
) -> None:
    comment = DbComment(
        **request.dict(), timestamp=datetime.now(), creator_id=current_user_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
