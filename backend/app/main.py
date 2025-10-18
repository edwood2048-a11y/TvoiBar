from fastapi import FastAPI, Depends, HTTPException
from app.api.routers.users import router as user_router
from app.api.routers.events import router as event_router
from app.api.routers.participants import router as participant_router
from app.api.routers.complaints import router as complaint_router
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import requests
from app.api.dependencies import get_user_repository
from app.services.user_service import UserService
from app.repositories.abstract.user import AbstractUserRepository
from pydantic import BaseModel
from app.services.scheduler_service import init_scheduler, shutdown_scheduler
from fastapi.staticfiles import StaticFiles
from app.services.telegram_service import send_telegram_message

async def get_user_service(repo: AbstractUserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

class TestAlertRequest(BaseModel):
    telegram_id: int
    lat: float = None
    lng: float = None

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(user_router, prefix="/api/v1")
app.include_router(event_router, prefix="/api/v1")
app.include_router(participant_router, prefix="/api/v1")
app.include_router(complaint_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # init_scheduler()
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # shutdown_scheduler()
    pass

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/test-safety-alert")
async def test_safety_alert(request: TestAlertRequest, service: UserService = Depends(get_user_service)):
    print(f"Received test-safety-alert request for telegram_id: {request.telegram_id}")
    telegram_id = request.telegram_id
    user = await service.repo.get_by_telegram_id(telegram_id)
    print(f"User found: {user}")
    if not user:
        print("User not found")
        raise HTTPException(status_code=400, detail="User not found")
    
    # Send to trusted contact if available, otherwise to self
    recipient_id = user.trusted_contact if user.trusted_contact else str(telegram_id)
    
    # If starts with @, treat as username, else try as ID
    if recipient_id.startswith('@'):
        recipient_id = recipient_id  # keep as is
    else:
        try:
            recipient_id_int = int(recipient_id)
            recipient_id = str(recipient_id_int)
        except ValueError:
            print(f"Invalid trusted contact: {recipient_id}")
            raise HTTPException(status_code=400, detail="Invalid trusted contact")
    
    lat = request.lat or 55.7558
    lng = request.lng or 37.6173
    location = f"{lat}, {lng}" if request.lat else "55.7558, 37.6173 (Москва, тест)"
    message = f"Тестовое уведомление безопасности: Пользователь {user.first_name} {user.last_name} не ответил на 3 вызова. Геолокация: {location}"
    print(f"Sending message to {recipient_id}: {message}")
    send_telegram_message(recipient_id, message)
    print("Message sent (or attempted)")
    print("Test alert sent successfully")
    return {"message": "Test alert sent"}

@app.post("/api/v1/check-in-response")
async def check_in_response(participant_id: int, response: str):
    from app.services.scheduler_service import participant_jobs, scheduler
    print(f"Check-in response from participant {participant_id}: {response}")
    # Remove job if exists
    if participant_id in participant_jobs:
        scheduler.remove_job(participant_jobs[participant_id])
        del participant_jobs[participant_id]
    return {"message": "Response received"}

@app.get("/")
async def root():
    return {"message": "Go Buhat API"}