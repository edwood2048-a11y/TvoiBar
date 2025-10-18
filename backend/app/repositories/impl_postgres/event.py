from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.repositories.abstract.event import AbstractEventRepository
from app.schemas import EventCreate
from app.models import Event

class PostgresEventRepository(AbstractEventRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Event]:
        result = await self.session.execute(select(Event))
        return result.scalars().all()

    async def get_by_id(self, event_id: int) -> Optional[Event]:
        result = await self.session.execute(select(Event).where(Event.id == event_id))
        return result.scalars().first()

    async def get_by_creator(self, creator_id: int) -> Optional[Event]:
        result = await self.session.execute(select(Event).where(Event.creator_id == creator_id))
        return result.scalars().first()

    async def create(self, event: EventCreate, creator_id: int) -> Event:
        db_event = Event(**event.model_dump(), creator_id=creator_id)
        self.session.add(db_event)
        await self.session.commit()
        await self.session.refresh(db_event)
        return db_event

    async def update(self, event_id: int, event: EventCreate) -> Optional[Event]:
        result = await self.session.execute(select(Event).where(Event.id == event_id))
        db_event = result.scalars().first()
        if db_event:
            for key, value in event.model_dump().items():
                setattr(db_event, key, value)
            await self.session.commit()
            await self.session.refresh(db_event)
        return db_event

    async def delete(self, event_id: int) -> bool:
        result = await self.session.execute(select(Event).where(Event.id == event_id))
        db_event = result.scalars().first()
        if db_event:
            await self.session.delete(db_event)
            await self.session.commit()
            return True
        return False