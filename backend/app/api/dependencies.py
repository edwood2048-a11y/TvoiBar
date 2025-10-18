import os
from fastapi import Depends
from typing import Optional
from app.repositories.abstract.user import AbstractUserRepository
from app.repositories.abstract.event import AbstractEventRepository
from app.repositories.abstract.participant import AbstractParticipantRepository
from app.repositories.impl_postgres.user import PostgresUserRepository
from app.repositories.impl_postgres.event import PostgresEventRepository
from app.repositories.impl_postgres.participant import PostgresParticipantRepository
from app.repositories.impl_json.user import JSONUserRepository
from app.repositories.impl_json.event import JSONEventRepository
from app.repositories.impl_json.participant import JSONParticipantRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.core.config import DATABASE_MODE

async def get_user_repository(session: Optional[AsyncSession] = Depends(get_db_session)) -> AbstractUserRepository:
    if DATABASE_MODE == "postgres":
        if session is None:
            raise ValueError("Session required for postgres")
        return PostgresUserRepository(session)
    else:
        return JSONUserRepository()

async def get_event_repository(session: Optional[AsyncSession] = Depends(get_db_session)) -> AbstractEventRepository:
    if DATABASE_MODE == "postgres":
        if session is None:
            raise ValueError("Session required for postgres")
        return PostgresEventRepository(session)
    else:
        return JSONEventRepository()

async def get_participant_repository(session: Optional[AsyncSession] = Depends(get_db_session)) -> AbstractParticipantRepository:
    if DATABASE_MODE == "postgres":
        if session is None:
            raise ValueError("Session required for postgres")
        return PostgresParticipantRepository(session)
    else:
        return JSONParticipantRepository()

from app.services.participant_service import ParticipantService

async def get_participant_service(
    repo: AbstractParticipantRepository = Depends(get_participant_repository),
    event_repo: AbstractEventRepository = Depends(get_event_repository),
    user_repo: AbstractUserRepository = Depends(get_user_repository)
) -> ParticipantService:
    return ParticipantService(repo, event_repo, user_repo)