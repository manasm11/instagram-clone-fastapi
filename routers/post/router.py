import os
import shutil
from typing import List

from fastapi import APIRouter, Depends, File, Request, UploadFile
from sqlalchemy.orm import Session

from db import db_post
from db.database import get_db

from .common import check_image_filename, get_unique_filename
from .schema import PostListResponse, PostRequest, PostResponse

router = APIRouter(prefix="/post", tags=["Post"])


@router.post("/", status_code=201, response_model=PostResponse)
async def create_post(postRequest: PostRequest, db: Session = Depends(get_db)):
    post = db_post.create_post(db, postRequest)
    return post


@router.get("/all", response_model=PostListResponse)
async def get_all_post(db: Session = Depends(get_db)):
    all_posts = db_post.get_all_post(db)
    return {"posts": all_posts}


@router.post("/image-upload")
async def image_upload(request: Request, image: UploadFile = File(...)):
    check_image_filename(image.filename)
    new_filename = get_unique_filename(image.filename)
    os.makedirs("images", exist_ok=True)
    path = f"images/{new_filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(image.file, f)
    return {"image_url": f"{request.base_url}{path}"}
