import json
import aiofiles
import asyncio
from datetime import datetime
from typing import Optional, List
from app.repositories.abstract.participant import AbstractParticipantRepository
from app.schemas import ParticipantCreate
from app.models import Participant

class JSONParticipantRepository(AbstractParticipantRepository):
    def __init__(self, file_path: str = r"c:\Users\Artem\Desktop\go-buhat\backend\local_database.json"):
        self.file_path = file_path

    async def _read_data(self) -> dict:
        async with aiofiles.open(self.file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            return json.loads(content)

    async def _write_data(self, data: dict):
        async with aiofiles.open(self.file_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(data, indent=4, default=str))

    async def get_all(self) -> List[Participant]:
        await asyncio.sleep(0)
        data = await self._read_data()
        participants = []
        for p_data in data.get("participants", []):
            p_data["created_at"] = datetime.fromisoformat(p_data["created_at"])
            participants.append(Participant(**p_data))
        return participants

    async def get_by_id(self, participant_id: int) -> Optional[Participant]:
        await asyncio.sleep(0)
        data = await self._read_data()
        for p_data in data.get("participants", []):
            if p_data["id"] == participant_id:
                p_data["created_at"] = datetime.fromisoformat(p_data["created_at"])
                return Participant(**p_data)
        return None

    async def create(self, participant: ParticipantCreate) -> Participant:
        await asyncio.sleep(0)
        data = await self._read_data()
        new_id = max([p["id"] for p in data["participants"]] + [0]) + 1
        p_data = participant.model_dump()
        p_data["id"] = new_id
        p_data["created_at"] = datetime.utcnow()
        data["participants"].append(p_data)
        await self._write_data(data)
        return Participant(**p_data)

    async def delete(self, participant_id: int) -> bool:
        await asyncio.sleep(0)
        data = await self._read_data()
        for i, p_data in enumerate(data["participants"]):
            if p_data["id"] == participant_id:
                del data["participants"][i]
                await self._write_data(data)
                return True
        return False

    async def get_by_user_and_event(self, user_id: int, event_id: int) -> Optional[Participant]:
        await asyncio.sleep(0)
        data = await self._read_data()
        for p_data in data.get("participants", []):
            if p_data["user_id"] == user_id and p_data["event_id"] == event_id:
                p_data["created_at"] = datetime.fromisoformat(p_data["created_at"])
                return Participant(**p_data)
        return None

    async def get_by_event(self, event_id: int) -> List[Participant]:
        await asyncio.sleep(0)
        data = await self._read_data()
        participants = []
        for p_data in data.get("participants", []):
            if p_data["event_id"] == event_id:
                p_data["created_at"] = datetime.fromisoformat(p_data["created_at"])
                participants.append(Participant(**p_data))
        return participants

    async def update_status(self, participant_id: int, status: str) -> Optional[Participant]:
        await asyncio.sleep(0)
        data = await self._read_data()
        for p_data in data.get("participants", []):
            if p_data["id"] == participant_id:
                p_data["status"] = status
                await self._write_data(data)
                p_data["created_at"] = datetime.fromisoformat(p_data["created_at"])
                return Participant(**p_data)
        return None

    async def update_meeting_status(self, participant_id: int, meeting_status: str) -> Optional[Participant]:
        await asyncio.sleep(0)
        data = await self._read_data()
        for p_data in data.get("participants", []):
            if p_data["id"] == participant_id:
                p_data["meeting_status"] = meeting_status
                await self._write_data(data)
                p_data["created_at"] = datetime.fromisoformat(p_data["created_at"])
                return Participant(**p_data)
        return None

    async def get_by_user(self, user_id: int) -> List[Participant]:
        await asyncio.sleep(0)
        data = await self._read_data()
        participants = []
        for p_data in data.get("participants", []):
            if p_data["user_id"] == user_id:
                p_data["created_at"] = datetime.fromisoformat(p_data["created_at"])
                participants.append(Participant(**p_data))
        return participants