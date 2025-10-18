import json
import aiofiles
import asyncio
from typing import Optional, List
from datetime import datetime
from app.repositories.abstract.event import AbstractEventRepository
from app.schemas import EventCreate
from app.models import Event

class JSONEventRepository(AbstractEventRepository):
    def __init__(self, file_path: str = r"c:\Users\Artem\Desktop\go-buhat\backend\local_database.json"):
        self.file_path = file_path

    async def _read_data(self) -> dict:
        async with aiofiles.open(self.file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            return json.loads(content)

    async def _write_data(self, data: dict):
        async with aiofiles.open(self.file_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(data, indent=4, default=str))

    async def get_all(self) -> List[Event]:
        await asyncio.sleep(0)
        data = await self._read_data()
        events = []
        for event_data in data.get("events", []):
            event_data["created_at"] = datetime.fromisoformat(event_data["created_at"])
            if event_data.get("date_time"):
                event_data["date_time"] = datetime.fromisoformat(event_data["date_time"])
            # Add defaults if missing
            if "max_participants" not in event_data:
                event_data["max_participants"] = 10
            if "current_participants" not in event_data:
                event_data["current_participants"] = 0
            events.append(Event(**event_data))
        return events

    async def get_by_id(self, event_id: int) -> Optional[Event]:
        await asyncio.sleep(0)
        data = await self._read_data()
        for event_data in data.get("events", []):
            if event_data["id"] == event_id:
                event_data["created_at"] = datetime.fromisoformat(event_data["created_at"])
                if event_data.get("date_time"):
                    event_data["date_time"] = datetime.fromisoformat(event_data["date_time"])
                # Add defaults if missing
                if "max_participants" not in event_data:
                    event_data["max_participants"] = 10
                if "current_participants" not in event_data:
                    event_data["current_participants"] = 0
                return Event(**event_data)
        return None

    async def get_by_creator(self, creator_id: int) -> Optional[Event]:
        await asyncio.sleep(0)
        data = await self._read_data()
        for event_data in data.get("events", []):
            if event_data["creator_id"] == creator_id:
                event_data["created_at"] = datetime.fromisoformat(event_data["created_at"])
                if event_data.get("date_time"):
                    event_data["date_time"] = datetime.fromisoformat(event_data["date_time"])
                # Add defaults if missing
                if "max_participants" not in event_data:
                    event_data["max_participants"] = 10
                if "current_participants" not in event_data:
                    event_data["current_participants"] = 0
                return Event(**event_data)
        return None

    async def create(self, event: EventCreate, creator_id: int) -> Event:
        await asyncio.sleep(0)
        data = await self._read_data()
        new_id = max([e["id"] for e in data["events"]] + [0]) + 1
        event_data = event.model_dump()
        event_data["id"] = new_id
        event_data["creator_id"] = creator_id
        event_data["current_participants"] = 0
        event_data["created_at"] = datetime.utcnow()
        data["events"].append(event_data)
        await self._write_data(data)
        return Event(**event_data)

    async def update(self, event_id: int, event: EventCreate) -> Optional[Event]:
        await asyncio.sleep(0)
        data = await self._read_data()
        for i, event_data in enumerate(data["events"]):
            if event_data["id"] == event_id:
                updated_data = event.model_dump()
                updated_data["id"] = event_id
                updated_data["creator_id"] = event_data["creator_id"]
                updated_data["created_at"] = datetime.fromisoformat(event_data["created_at"])
                data["events"][i] = updated_data
                await self._write_data(data)
                return Event(**updated_data)
        return None

    async def delete(self, event_id: int) -> bool:
        await asyncio.sleep(0)
        data = await self._read_data()
        for i, event_data in enumerate(data["events"]):
            if event_data["id"] == event_id:
                del data["events"][i]
                await self._write_data(data)
                return True
        return False