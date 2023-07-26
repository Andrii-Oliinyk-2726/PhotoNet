import pathlib
import time
from ipaddress import ip_address
from typing import Callable

# import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
# from starlette.middleware.cors import CORSMiddleware
# from fastapi_limiter import FastAPILimiter

from src.database.db import get_db
# from src.routes import clients, auth, users
# from src.conf.config import settings

app = FastAPI()

templates = Jinja2Templates(directory='templates')
BASE_DIR = pathlib.Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR/"static"), name="static")


@app.get("/", response_class=HTMLResponse, description="Main Page")
async def root(request: Request):
    return templates.TemplateResponse('index.html', {"request": request, "title": "Contacts App"})


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


# перевірка підключення
# from src.database.db import get_db
# if __name__ == "__main__":
#     next(get_db())
