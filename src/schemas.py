import datetime
from pydantic import BaseModel, EmailStr, Field


# Вхідні дані ->//
class UserModel(BaseModel):
    username: str
    age: int
    phone: str
    email: EmailStr
    city: str
    description: str


# Вихідні дані //->
class UserResponse(BaseModel):
    id: int
    username: str
    age: int
    phone: str
    email: EmailStr
    city: str
    description: str

    class Config:
        orm_mode = True


# Вхідні дані ->//
class PhotoModel(BaseModel):
    title: str = Field()
    description: str = Field(min_length=10, max_length=50)
    user_id: int = Field(gt=0)


# Вихідні дані //->
class PhotoResponse(BaseModel):
    id: int
    title: str
    description: str
    url: str
    path: str
    updated_at: datetime
    created_at: datetime
    user: UserResponse

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
