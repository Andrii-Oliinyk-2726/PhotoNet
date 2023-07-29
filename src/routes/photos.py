from typing import List

from fastapi import Depends, Path, Query, APIRouter, File, UploadFile
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import PhotoModel, PhotoResponse
from src.conf.config import settings, cloudinary_config
from src.repository import photos as repository_photos


router = APIRouter(prefix="/photos", tags=["photos"])


@router.get("/", response_model=List[PhotoResponse], tags=["photos"])
async def get_photos(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    photos = await repository_photos.get_photos(limit, offset, db)
    return photos


@router.get("/{photo_id}", response_model=PhotoResponse, tags=["photos"])
async def get_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = await repository_photos.get_photo(photo_id, db)
    return photo


@router.post("/", response_model=PhotoResponse, tags=["photos"])
async def create_photo(body: PhotoModel = Depends(), image: UploadFile = File(), db: Session = Depends(get_db)):
    photo = await repository_photos.create_photo(body, image, db)
    return photo


@router.put("/{photo_id}", response_model=PhotoResponse, tags=["photos"])
async def update_photo(body: PhotoModel = Depends(), photo_id: int = Path(ge=1), db: Session = Depends(get_db)):
    photo = await repository_photos.update_photo(body, photo_id, db)
    return photo
