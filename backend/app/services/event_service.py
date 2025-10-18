from fastapi import HTTPException
from app.repositories.abstract.event import AbstractEventRepository
from app.schemas import EventCreate, Event
from typing import List

class EventService:
    def __init__(self, repo: AbstractEventRepository):
        self.repo = repo

    async def get_all_events(self) -> List[Event]:
        events = await self.repo.get_all()
        return [Event.from_orm(event) for event in events]

    async def get_event(self, event_id: int) -> Event:
        event = await self.repo.get_by_id(event_id)
        if event:
            return Event.from_orm(event)
        raise HTTPException(status_code=404, detail="Event not found")

    async def create_event(self, event_data: EventCreate, creator_id: int) -> Event:
        # Check if user already has an event
        existing = await self.repo.get_by_creator(creator_id)
        if existing:
            raise HTTPException(status_code=400, detail="User can only have one active event. Delete the existing one first.")
        event = await self.repo.create(event_data, creator_id)
        return Event.from_orm(event)

    async def update_event(self, event_id: int, event_data: EventCreate) -> Event:
        event = await self.repo.update(event_id, event_data)
        if event:
            return Event.from_orm(event)
        raise ValueError("Event not found")

    async def delete_event(self, event_id: int) -> bool:
        return await self.repo.delete(event_id)