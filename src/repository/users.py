from typing import List, Type

from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserModel
from src.database.models import User
from src.conf.type_error import ERROR_1503, ERROR_1504


async def get_users(db: Session) -> List[Type[User]] | None:
    return db.query(User).all()


async def get_user(user_id: int, db: Session) -> Type[User] | None:
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_1504)
    return user


async def create_user(body: UserModel, db: Session) -> User:
    user = db.query(User).filter_by(email=body.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ERROR_1503)
    user = User(username=body.username,
                age=body.age,
                phone=body.phone,
                email=body.email,
                city=body.city,
                description=body.description)
    db.add(user)
    db.commit()
    return user


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


async def delete_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_1504)
    db.delete(user)
    db.commit()
    return user
