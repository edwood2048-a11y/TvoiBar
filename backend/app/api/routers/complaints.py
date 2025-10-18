from fastapi import APIRouter, Depends, HTTPException
from app.services.user_service import UserService
from app.api.dependencies import get_user_repository
from app.repositories.abstract.user import AbstractUserRepository
from app.schemas import ComplaintCreate, Complaint

router = APIRouter()

def get_user_service(repo: AbstractUserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)

@router.post("/complaints/", response_model=Complaint)
async def create_complaint(complaint: ComplaintCreate, service: UserService = Depends(get_user_service)):
    # For now, just return the complaint (in real app, save to DB)
    return complaint