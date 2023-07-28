from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database.models import User
from src.schemas.user_schemas import UserModel, UserUpdate, UserBlackList


async def get_user_by_email(email: str, db: Session) -> User | None:
    """

    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """

    admin_exists = db.query(User).filter(User.role == 'admin').first()

    if admin_exists:
        new_user = User(**body.dict(), role='user')
    else:
        new_user = User(**body.dict(),  role='admin')

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """

    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """

    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def get_user_info(username: str, db: Session):

    user = db.query(User).filter(User.username == username).first()
    return user


async def update_user_info(body: UserUpdate, username: str, db: Session):
    """

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.username = body.username
    user.email = body.email
    db.commit()
    return user


async def block(email: str, body: UserBlackList, db: Session):

    user = await get_user_by_email(email, db)
    if user:
        user.banned = body.banned
        db.commit()
    return user
