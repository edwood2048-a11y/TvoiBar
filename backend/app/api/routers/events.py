from fastapi import APIRouter, Depends
from app.services.event_service import EventService
from app.api.dependencies import get_event_repository
from app.repositories.abstract.event import AbstractEventRepository
from app.schemas import EventCreate, Event
from typing import List

router = APIRouter()

def get_event_service(repo: AbstractEventRepository = Depends(get_event_repository)) -> EventService:
    return EventService(repo)

@router.get("/events/", response_model=List[Event])
async def get_events(service: EventService = Depends(get_event_service)):
    return await service.get_all_events()

@router.get("/events/{event_id}", response_model=Event)
async def get_event(event_id: int, service: EventService = Depends(get_event_service)):
    return await service.get_event(event_id)

@router.post("/events/", response_model=Event)
async def create_event(event: EventCreate, creator_id: int, service: EventService = Depends(get_event_service)):
    return await service.create_event(event, creator_id)

@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: EventCreate, service: EventService = Depends(get_event_service)):
    return await service.update_event(event_id, event)

@router.delete("/events/{event_id}")
async def delete_event(event_id: int, service: EventService = Depends(get_event_service)):
    success = await service.delete_event(event_id)
    return {"success": success}