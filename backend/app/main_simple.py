from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
async def root():
    return {"message": "Go Buhat API"}

@app.post("/api/v1/users/{telegram_id}/upload-photo")
async def upload_photo(telegram_id: int, file: UploadFile = File(...)):
    # Save file
    upload_dir = "uploads/photos"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{telegram_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update user photo_url
    photo_url = f"/uploads/photos/{telegram_id}_{file.filename}"
    
    return {"photo_url": photo_url}