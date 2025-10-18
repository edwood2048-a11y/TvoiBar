from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.services.user_service import UserService
from app.api.dependencies import get_user_repository
from app.repositories.abstract.user import AbstractUserRepository
from app.schemas import UserCreate, User
import os
import shutil

router = APIRouter()

def get_user_service(repo: AbstractUserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)

@router.post("/users/", response_model=User)
async def create_or_get_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.get_or_create_user(user)

@router.get("/users/{telegram_id}", response_model=User)
async def get_user(telegram_id: int, service: UserService = Depends(get_user_service)):
    user = await service.repo.get_by_telegram_id(telegram_id)
    if user:
        return User.from_orm(user)
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{telegram_id}", response_model=User)
async def update_user(telegram_id: int, updates: dict, service: UserService = Depends(get_user_service)):
    user = await service.repo.get_by_telegram_id(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updates.items():
        if hasattr(user, key):
            setattr(user, key, value)
    await service.repo.update_user(User.from_orm(user))
    return User.from_orm(user)

@router.post("/users/{telegram_id}/upload-photo")
async def upload_photo(telegram_id: int, file: UploadFile = File(...), service: UserService = Depends(get_user_service)):
    user = await service.repo.get_by_telegram_id(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Save file
    upload_dir = "uploads/photos"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{telegram_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update user photo_url
    photo_url = f"/uploads/photos/{telegram_id}_{file.filename}"
    user.photo_url = photo_url
    await service.repo.update_user(User.from_orm(user))
    
    return {"photo_url": photo_url}