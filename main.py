import time

import cloudinary
import cloudinary.uploader

from typing import List

from fastapi import FastAPI, File, UploadFile, Query
from cloudinary import api

from src.conf.config import settings


app = FastAPI()

cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )


@app.post("/photo/")
async def photo(image: UploadFile = File()):
    # Fake user data
    user_id = 1
    unique_filename = f'PhotoNet/{user_id}/{int(time.time() * 1000)}'

    uploaded_result = cloudinary.uploader.upload(image.file, upload_preset="google_auto_tagging", public_id=unique_filename)
    image_url = uploaded_result["secure_url"]
    tags = uploaded_result["tags"][:5]    # Limit quantity of tags to 5
    cloudinary.api.update(unique_filename, tags=tags)    # Upload first 5 tags to image

    return {"url": image_url, "tags": tags}


@app.get("/photo/")
async def photo(tags: List[str] = Query(None)):
    if tags is None:
        return {'message': 'Please provide at least one tag.'}

    tag_expression = ' OR '.join(tags)
    search_result = cloudinary.Search().expression(f'tags={tag_expression}').execute()
    found_photos = [founded_photo for founded_photo in search_result['resources']]
    # photo_url = result['resources'][0]['public_id']    photo's public id
    # photo_url = result['resources'][0]['secure_url']    photo's  url
    return {'founded photo': found_photos}

# перевірка підключення 
# from src.database.db import get_db
# if __name__ == "__main__":
#     next(get_db())