from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from app.repositories.abstract.user import AbstractUserRepository
from app.schemas import UserCreate
from app.models import User

class PostgresUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalars().first()

    async def create(self, user: UserCreate) -> User:
        db_user = User(**user.model_dump())
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def update(self, user_id: int, user: UserCreate) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        db_user = result.scalars().first()
        if db_user:
            for key, value in user.model_dump().items():
                setattr(db_user, key, value)
            await self.session.commit()
            await self.session.refresh(db_user)
        return db_user

    async def update_user(self, user: User) -> None:
        # Since user is already attached to session, just commit
        await self.session.commit()

    async def get_or_create(self, user: UserCreate) -> User:
        existing = await self.get_by_telegram_id(user.telegram_id)
        if existing:
            return existing
        return await self.create(user)