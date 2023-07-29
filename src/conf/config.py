from pydantic_settings import BaseSettings
import cloudinary


class Settings(BaseSettings):
    sqlalchemy_database_url: str = "postgresql+psycopg2://postgres:password@localhost:5432/dbname"
    jwt_secret_key: str = "secret"
    jwt_algorithm: str = "HS256"
    mail_username: str = "example@meta.ua"
    mail_password: str = "password"
    mail_from: str = "example@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.test.com"
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str = "dwnpoaklw"
    cloudinary_api_key: str = "234929413527732"
    cloudinary_api_secret: str = "TtyktkFdOQEbhUetueVCaTcOnE0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

cloudinary_config = cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )