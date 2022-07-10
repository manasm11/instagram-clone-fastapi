import os
import shutil
from typing import List

from fastapi import APIRouter, Depends, File, Request, UploadFile
from sqlalchemy.orm import Session

from auth import get_current_user
from db import DbUser, db_comment, db_post, get_db

from .common import check_image_filename, get_unique_filename
from .schema import CommentRequest, PostListResponse, PostRequest, PostResponse

router = APIRouter(prefix="/post", tags=["Post"])


@router.post("/", status_code=201, response_model=PostResponse)
async def create_post(
    postRequest: PostRequest,
    db: Session = Depends(get_db),
    current_user: DbUser = Depends(get_current_user),
):
    post = db_post.create_post(db, postRequest, current_user.id)
    return post


@router.get("/all", response_model=PostListResponse)
async def get_all_post(db: Session = Depends(get_db)):
    all_posts = db_post.get_all_post(db)
    return {"posts": all_posts}


@router.post("/image-upload")
async def image_upload(
    request: Request,
    image: UploadFile = File(...),
    current_user: DbUser = Depends(get_current_user),
):
    check_image_filename(image.filename)
    new_filename = get_unique_filename(image.filename)
    os.makedirs(f"images/{current_user.username}", exist_ok=True)
    path = f"images/{current_user.username}/{new_filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(image.file, f)
    return {"image_url": f"{request.base_url}{path}"}


@router.get("/delete/{post_id}")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: DbUser = Depends(get_current_user),
):
    db_post.delete_post(db, post_id, current_user.id)
    return {"message": "Post deleted"}


@router.post("/comment")
async def create_comment(
    commentRequest: CommentRequest,
    db: Session = Depends(get_db),
    current_user: DbUser = Depends(get_current_user),
):
    comment = db_comment.create_comment(db, commentRequest, current_user.id)
    return comment
