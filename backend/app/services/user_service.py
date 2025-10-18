from app.repositories.abstract.user import AbstractUserRepository
from app.schemas import UserCreate, User

class UserService:
    def __init__(self, repo: AbstractUserRepository):
        self.repo = repo

    async def get_or_create_user(self, user_data: UserCreate) -> User:
        user = await self.repo.get_or_create(user_data)
        return User.from_orm(user)

    async def update_user(self, user_id: int, user_data: UserCreate) -> User:
        user = await self.repo.update(user_id, user_data)
        if user:
            return User.from_orm(user)
        raise ValueError("User not found")