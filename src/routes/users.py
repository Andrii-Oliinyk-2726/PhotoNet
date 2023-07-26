from typing import List

from fastapi import Depends, Path, APIRouter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserResponse, UserModel
from src.repository import users as repository_users


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/users", response_model=List[UserResponse], tags=["users"])
async def get_users(db: Session = Depends(get_db)):
    users = await repository_users.get_users(db)
    return users


@router.get("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def get_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = await repository_users.get_user(user_id, db)
    return user


@router.post("/users", response_model=UserResponse, tags=["users"])
async def create_user(body: UserModel, db: Session = Depends(get_db)):
    user = await repository_users.create_user(body, db)
    return user


@router.put("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def update_user(body: UserModel, user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = await repository_users.update_user(body, user_id, db)
    return user


@router.delete("/users/{user_id}", response_model=UserResponse, tags=["users"])
async def delete_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):

    user = await repository_users.delete_user(user_id, db)
    return user
