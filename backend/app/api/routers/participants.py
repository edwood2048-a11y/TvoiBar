from fastapi import APIRouter, Depends
from app.services.participant_service import ParticipantService
from app.api.dependencies import get_participant_service
from app.schemas import ParticipantCreate, Participant
from typing import List
from app.services.scheduler_service import start_check_in_job

router = APIRouter()

@router.post("/events/{event_id}/join", response_model=Participant)
async def join_event(event_id: int, user_id: int, message: str = None, service: ParticipantService = Depends(get_participant_service)):
    return await service.join_event(user_id, event_id, message)

@router.delete("/events/{event_id}/leave")
async def leave_event(event_id: int, user_id: int, service: ParticipantService = Depends(get_participant_service)):
    success = await service.leave_event(user_id, event_id)
    return {"success": success}

@router.get("/events/{event_id}/participants", response_model=List[Participant])
async def get_participants(event_id: int, service: ParticipantService = Depends(get_participant_service)):
    return await service.get_participants_by_event(event_id)

@router.put("/participants/{participant_id}/accept", response_model=Participant)
async def accept_participant(participant_id: int, service: ParticipantService = Depends(get_participant_service)):
    return await service.accept_participant(participant_id)

@router.put("/participants/{participant_id}/reject", response_model=Participant)
async def reject_participant(participant_id: int, service: ParticipantService = Depends(get_participant_service)):
    return await service.reject_participant(participant_id)

@router.put("/participants/{participant_id}/meeting_status", response_model=Participant)
async def update_meeting_status(participant_id: int, meeting_status: str, service: ParticipantService = Depends(get_participant_service)):
    participant = await service.update_meeting_status(participant_id, meeting_status)
    if meeting_status == "in_progress":
        # Start check-in job
        start_check_in_job(participant_id, participant.user_id)
    return participant

@router.get("/users/{user_id}/participants", response_model=List[Participant])
async def get_user_participants(user_id: int, service: ParticipantService = Depends(get_participant_service)):
    return await service.get_participants_by_user(user_id)