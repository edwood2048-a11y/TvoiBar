import json
import aiofiles
import asyncio
from typing import Optional
from datetime import datetime
from app.repositories.abstract.user import AbstractUserRepository
from app.schemas import UserCreate
from app.models import User

class JSONUserRepository(AbstractUserRepository):
    def __init__(self, file_path: str = r"c:\Users\Artem\Desktop\go-buhat\backend\local_database.json"):
        self.file_path = file_path

    async def _read_data(self) -> dict:
        async with aiofiles.open(self.file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            return json.loads(content)

    async def _write_data(self, data: dict):
        async with aiofiles.open(self.file_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(data, indent=4, default=str))

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        await asyncio.sleep(0)  # Имитация I/O
        data = await self._read_data()
        for user_data in data.get("users", []):
            if user_data["telegram_id"] == telegram_id:
                user_data["created_at"] = datetime.fromisoformat(user_data["created_at"])
                return User(**user_data)
        return None

    async def create(self, user: UserCreate) -> User:
        await asyncio.sleep(0)
        data = await self._read_data()
        new_id = max([u["id"] for u in data["users"]] + [0]) + 1
        user_data = user.model_dump()
        user_data["id"] = new_id
        user_data["created_at"] = datetime.utcnow()
        data["users"].append(user_data)
        await self._write_data(data)
        return User(**user_data)

    async def update(self, user_id: int, user: UserCreate) -> Optional[User]:
        await asyncio.sleep(0)
        data = await self._read_data()
        for i, user_data in enumerate(data["users"]):
            if user_data["id"] == user_id:
                updated_data = user.model_dump()
                updated_data["id"] = user_id
                updated_data["created_at"] = datetime.fromisoformat(user_data["created_at"])
                data["users"][i] = updated_data
                await self._write_data(data)
                return User(**updated_data)
        return None

    async def update_user(self, user: User) -> None:
        await asyncio.sleep(0)
        data = await self._read_data()
        for i, user_data in enumerate(data.get("users", [])):
            if user_data["id"] == user.id:
                updated_data = user.model_dump()
                updated_data["created_at"] = user_data["created_at"]  # keep original created_at
                data["users"][i] = updated_data
                await self._write_data(data)
                return
        raise ValueError("User not found")

    async def get_or_create(self, user: UserCreate) -> User:
        existing = await self.get_by_telegram_id(user.telegram_id)
        if existing:
            return existing
        return await self.create(user)