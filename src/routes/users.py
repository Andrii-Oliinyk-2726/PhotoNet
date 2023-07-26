from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserResponse, UserModel
from src.database.models import User
from src.conf.type_error import ERROR_1503, ERROR_1504


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/users", response_model=List[UserResponse], tags=["users"])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def get_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_1504)
    return user


@router.post("/users", response_model=UserResponse, tags=["users"])
async def create_user(body: UserModel, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=body.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ERROR_1503)
    user = User(**body.dict())
    db.add(user)
    db.commit()
    return user


@router.put("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def update_user(body: UserModel, user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_1504)
    user.username = body.username
    user.age = body.age
    user.phone = body.phone
    user.email = body.email
    user.city = body.city
    user.description = body.description
    db.commit()
    return user


@router.delete("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def get_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_1504)
    db.delete(user)
    db.commit()
    return user
