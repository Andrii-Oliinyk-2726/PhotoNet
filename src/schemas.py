import datetime
from pydantic import BaseModel, EmailStr, Field, HttpUrl

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
    id: int = 1
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
    url: str = Field("Photo url")
    title: str = Field("Photo name", min_length=3, max_length=25)
    description: str = Field("Photo description", min_length=10, max_length=50)
    user_id: int = Field(1, gt=0)


# Вихідні дані //->
class PhotoResponse(BaseModel):
    id: int = 1
    url: str
    title: str
    description: str
    user: UserResponse
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True