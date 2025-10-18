from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.repositories.abstract.participant import AbstractParticipantRepository
from app.schemas import ParticipantCreate
from app.models import Participant

class PostgresParticipantRepository(AbstractParticipantRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Participant]:
        result = await self.session.execute(select(Participant))
        return result.scalars().all()

    async def get_by_id(self, participant_id: int) -> Optional[Participant]:
        result = await self.session.execute(select(Participant).where(Participant.id == participant_id))
        return result.scalars().first()

    async def create(self, participant: ParticipantCreate) -> Participant:
        db_participant = Participant(**participant.model_dump())
        self.session.add(db_participant)
        await self.session.commit()
        await self.session.refresh(db_participant)
        return db_participant

    async def delete(self, participant_id: int) -> bool:
        result = await self.session.execute(select(Participant).where(Participant.id == participant_id))
        db_participant = result.scalars().first()
        if db_participant:
            await self.session.delete(db_participant)
            await self.session.commit()
            return True
        return False

    async def get_by_user_and_event(self, user_id: int, event_id: int) -> Optional[Participant]:
        result = await self.session.execute(select(Participant).where(Participant.user_id == user_id, Participant.event_id == event_id))
        return result.scalars().first()

    async def get_by_event(self, event_id: int) -> List[Participant]:
        result = await self.session.execute(select(Participant).where(Participant.event_id == event_id))
        return result.scalars().all()

    async def update_status(self, participant_id: int, status: str) -> Optional[Participant]:
        result = await self.session.execute(select(Participant).where(Participant.id == participant_id))
        db_participant = result.scalars().first()
        if db_participant:
            db_participant.status = status
            await self.session.commit()
            await self.session.refresh(db_participant)
            return db_participant
        return None

    async def update_meeting_status(self, participant_id: int, meeting_status: str) -> Optional[Participant]:
        result = await self.session.execute(select(Participant).where(Participant.id == participant_id))
        db_participant = result.scalars().first()
        if db_participant:
            db_participant.meeting_status = meeting_status
            await self.session.commit()
            await self.session.refresh(db_participant)
            return db_participant
        return None

    async def get_by_user(self, user_id: int) -> List[Participant]:
        result = await self.session.execute(select(Participant).where(Participant.user_id == user_id))
        return result.scalars().all()