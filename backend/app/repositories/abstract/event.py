from abc import ABC, abstractmethod
from typing import Optional, List
from app.schemas import Event, EventCreate
from app.models import Event as EventModel

class AbstractEventRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[EventModel]:
        pass

    @abstractmethod
    async def get_by_id(self, event_id: int) -> Optional[EventModel]:
        pass

    @abstractmethod
    async def get_by_creator(self, creator_id: int) -> Optional[EventModel]:
        pass

    @abstractmethod
    async def create(self, event: EventCreate, creator_id: int) -> EventModel:
        pass

    @abstractmethod
    async def update(self, event_id: int, event: EventCreate) -> Optional[EventModel]:
        pass

    @abstractmethod
    async def delete(self, event_id: int) -> bool:
        pass