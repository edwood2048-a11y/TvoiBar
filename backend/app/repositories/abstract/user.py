from abc import ABC, abstractmethod
from typing import Optional, List
from app.schemas import User, UserCreate
from app.models import User as UserModel

class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[UserModel]:
        pass

    @abstractmethod
    async def create(self, user: UserCreate) -> UserModel:
        pass

    @abstractmethod
    async def update(self, user_id: int, user: UserCreate) -> Optional[UserModel]:
        pass

    @abstractmethod
    async def update_user(self, user: UserModel) -> None:
        pass

    @abstractmethod
    async def get_or_create(self, user: UserCreate) -> UserModel:
        pass