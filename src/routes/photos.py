from typing import List

from fastapi import Depends, HTTPException, status, Path, Query, APIRouter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import PhotoModel, PhotoResponse
from src.database.models import User, Photo
from src.conf.type_error import ERROR_1504, ERROR_1505

router = APIRouter(prefix="/photos", tags=["photos"])


@router.get("/photos", response_model=List[PhotoResponse], tags=["photos"])
async def get_photos(limit: int = Query(10, le=300), offset: int = 0, db: Session = Depends(get_db)):
    photos = db.query(Photo).limit(limit).offset(offset).all()
    return photos


@router.get("/photos/{photo_id}", response_model=PhotoResponse, tags=["photos"])
async def get_photo(photo_id: int = Path(ge=1), db: Session = Depends(get_db)):
    photo = db.query(Photo).filter_by(id=photo_id).first()
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_1504)
    return photo


@router.post("/photos", response_model=PhotoResponse, tags=["photos"])
async def create_photo(body: PhotoModel, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=body.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_1505)
    photo = Photo(**body.dict())
    db.add(photo)
    db.commit()
    return photo


@router.put("/photos/{photo_id}", response_model=PhotoResponse, tags=["photos"])
async def update_photo(body: PhotoModel, photo_id: int = Path(ge=1), db: Session = Depends(get_db)):
    photo = db.query(Photo).filter_by(id=photo_id).first()
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_1504)
    # user = db.query(User).filter_by(id=body.user_id).first()
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_1505)
    photo.url = body.url
    photo.title = body.title
    photo.description = body.description
    photo.user_id = body.user_id
    db.commit()
    return photo
