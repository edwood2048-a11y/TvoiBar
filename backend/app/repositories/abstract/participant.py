from abc import ABC, abstractmethod
from typing import Optional, List
from app.schemas import Participant, ParticipantCreate
from app.models import Participant as ParticipantModel

class AbstractParticipantRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[ParticipantModel]:
        pass

    @abstractmethod
    async def get_by_id(self, participant_id: int) -> Optional[ParticipantModel]:
        pass

    @abstractmethod
    async def create(self, participant: ParticipantCreate) -> ParticipantModel:
        pass

    @abstractmethod
    async def delete(self, participant_id: int) -> bool:
        pass

    @abstractmethod
    async def get_by_user_and_event(self, user_id: int, event_id: int) -> Optional[ParticipantModel]:
        pass

    @abstractmethod
    async def get_by_event(self, event_id: int) -> List[ParticipantModel]:
        pass

    @abstractmethod
    async def update_status(self, participant_id: int, status: str) -> Optional[ParticipantModel]:
        pass

    @abstractmethod
    async def update_meeting_status(self, participant_id: int, meeting_status: str) -> Optional[ParticipantModel]:
        pass

    @abstractmethod
    async def get_by_user(self, user_id: int) -> List[ParticipantModel]:
        pass