from typing import List

from fastapi import Depends, HTTPException, status, Path, Query, File, UploadFile
from sqlalchemy.orm import Session
import cloudinary.uploader
import cloudinary.api
from cloudinary.exceptions import NotFound

from src.database.db import get_db
from src.schemas import PhotoModel, PhotoResponse
from src.database.models import User, Photo
from src.conf.type_error import ERROR_1504, ERROR_1505
from src.conf.config import settings


async def get_photos(limit: int, offset: int, db: Session) -> List[Photo] | None:
    photos = db.query(Photo).limit(limit).offset(offset).all()
    return photos


async def get_photo(photo_id: int, db: Session) -> Photo | None:
    photo = db.query(Photo).filter_by(id=photo_id).first()
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_1504)
    return photo


async def create_photo(body: PhotoModel, image: UploadFile, db: Session) -> Photo:
    user = db.query(User).filter_by(id=body.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_1505)

    unique_filename = f'PhotoNet/{body.user_id}/{body.title}'

    try:
        existing_resource = cloudinary.api.resource(unique_filename)    # search photo by name
        if existing_resource:   # if photo exists with this name
            raise FileExistsError('Photo already exists with this name')
    except NotFound:
        upload_photo = cloudinary.uploader.upload(image.file,  public_id=unique_filename)    # upload_preset="google_auto_tagging",
        image_url = upload_photo["secure_url"]
        image_path = upload_photo['public_id']
        # tags = upload_photo["tags"][:5]    # Limit quantity of tags to 5
        # cloudinary.api.update(unique_filename, tags=tags)    # Upload first 5 tags to image

        uploaded_photo = Photo(title=body.title,
                               description=body.description,
                               user_id=body.user_id,
                               url=image_url,
                               path=image_path)
        db.add(uploaded_photo)
        db.commit()

        return uploaded_photo


async def update_photo(body: PhotoModel, photo_id: int, db: Session) -> Photo:
    photo = db.query(Photo).filter_by(id=photo_id).first()
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_1504)
    user = db.query(User).filter_by(id=body.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_1505)
    photo.title = body.title
    photo.description = body.description
    photo.user_id = body.user_id
    db.commit()
    return photo
