from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DatabaseError

from src.conf.config import settings

# SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, max_overflow=5)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except DatabaseError:
        db.rollback()
    finally:
        db.close()
