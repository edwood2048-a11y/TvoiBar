from app.repositories.abstract.participant import AbstractParticipantRepository
from app.repositories.abstract.event import AbstractEventRepository
from app.repositories.abstract.user import AbstractUserRepository
from app.schemas import ParticipantCreate, Participant, EventCreate
from typing import List
import requests
# from app.main import scheduler, participant_jobs

class ParticipantService:
    def __init__(self, repo: AbstractParticipantRepository, event_repo: AbstractEventRepository, user_repo: AbstractUserRepository):
        self.repo = repo
        self.event_repo = event_repo
        self.user_repo = user_repo

    async def get_all_participants(self) -> List[Participant]:
        participants = await self.repo.get_all()
        return [Participant.from_orm(p) for p in participants]

    async def join_event(self, user_id: int, event_id: int, message: str = None) -> Participant:
        # Check if already joined
        existing = await self.repo.get_by_user_and_event(user_id, event_id)
        if existing:
            return Participant.from_orm(existing)
        
        # Check if event has available spots
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise ValueError("Event not found")
        if event.current_participants >= event.max_participants:
            raise ValueError("Event is full")
        
        participant = ParticipantCreate(user_id=user_id, event_id=event_id, message=message)
        p = await self.repo.create(participant)
        
        # Increment current_participants
        event.current_participants += 1
        await self.event_repo.update(event_id, EventCreate(**event.__dict__))
        
        # Send notification to event creator
        event = await self.event_repo.get_by_id(event_id)
        if event:
            creator = await self.user_repo.get_by_id(event.creator_id)
            if creator and creator.telegram_id:
                user = await self.user_repo.get_by_id(user_id)
                username = user.username or f"Пользователь {user_id}" if user else f"Пользователь {user_id}"
                msg = f"Новый участник в событии '{event.title}': {username}"
                if message:
                    msg += f"\nСообщение: {message}"
                try:
                    requests.post("http://localhost:8001/notify", json={"telegram_id": creator.telegram_id, "message": msg})
                except:
                    pass  # Ignore notification errors
        
        return Participant.from_orm(p)

    async def leave_event(self, user_id: int, event_id: int) -> bool:
        existing = await self.repo.get_by_user_and_event(user_id, event_id)
        if existing:
            result = await self.repo.delete(existing.id)
            if result:
                # Decrement current_participants
                event = await self.event_repo.get_by_id(event_id)
                if event and event.current_participants > 0:
                    event.current_participants -= 1
                    await self.event_repo.update(event_id, EventCreate(**event.__dict__))
            return result
        return False

    async def get_participants_by_event(self, event_id: int) -> List[Participant]:
        participants = await self.repo.get_by_event(event_id)
        return [Participant.from_orm(p) for p in participants]

    async def accept_participant(self, participant_id: int) -> Participant:
        p = await self.repo.update_status(participant_id, "accepted")
        if p:
            # Send notification to participant
            user = await self.user_repo.get_by_id(p.user_id)
            event = await self.event_repo.get_by_id(p.event_id)
            if user and user.telegram_id and event:
                msg = f"Ваша заявка на событие '{event.title}' принята!"
                try:
                    requests.post("http://localhost:8001/notify", json={"telegram_id": user.telegram_id, "message": msg})
                except:
                    pass
            return Participant.from_orm(p)
        return None

    async def reject_participant(self, participant_id: int) -> Participant:
        p = await self.repo.update_status(participant_id, "rejected")
        if p:
            # Send notification to participant
            user = await self.user_repo.get_by_id(p.user_id)
            event = await self.event_repo.get_by_id(p.event_id)
            if user and user.telegram_id and event:
                msg = f"Ваша заявка на событие '{event.title}' отклонена."
                try:
                    requests.post("http://localhost:8001/notify", json={"telegram_id": user.telegram_id, "message": msg})
                except:
                    pass
            return Participant.from_orm(p)
        return None

    async def update_meeting_status(self, participant_id: int, meeting_status: str) -> Participant:
        p = await self.repo.update_meeting_status(participant_id, meeting_status)
        if p:
            if meeting_status == 'in_progress':
                # Schedule check-in every 30 minutes
                # job = scheduler.add_job(safety_check_in, 'interval', minutes=30, args=[participant_id])
                # participant_jobs[participant_id] = job.id
                pass
            elif meeting_status in ['completed', 'emergency']:
                # Cancel job if exists
                # job_id = participant_jobs.get(participant_id)
                # if job_id:
                #     scheduler.remove_job(job_id)
                #     del participant_jobs[participant_id]
                pass
            return Participant.from_orm(p)
        return None

    async def get_participants_by_user(self, user_id: int) -> List[Participant]:
        participants = await self.repo.get_by_user(user_id)
        return [Participant.from_orm(p) for p in participants]

async def safety_check_in(participant_id: int):
    # Get participant
    # Since this is a job, need access to repo
    # For simplicity, assume we have the service instance, but since it's global, hard.
    # Perhaps make it a method of the service, but scheduler needs a function.
    # Use a global service or something.
    # For now, hardcode the logic here.
    # This is not ideal, but for demo.
    print(f"Safety check-in for participant {participant_id}")
    # Send message to user
    # Assume telegram_id is known, but need to fetch.
    # This is complex, perhaps skip for now or simplify.
    pass