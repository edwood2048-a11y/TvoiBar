from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    trusted_contact: Optional[str] = None
    photo_url: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    date_time: Optional[datetime] = None
    max_participants: int = 10

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    creator_id: int
    current_participants: int = 0
    created_at: datetime

    class Config:
        from_attributes = True

class ParticipantBase(BaseModel):
    user_id: int
    event_id: int
    status: str = "pending"  # pending, accepted, rejected
    meeting_status: str = "not_started"  # not_started, in_progress, completed, emergency
    message: Optional[str] = None

class ParticipantCreate(ParticipantBase):
    pass

class Participant(ParticipantBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ComplaintBase(BaseModel):
    complainant_id: int
    accused_id: int
    reason: str
    description: Optional[str] = None

class ComplaintCreate(ComplaintBase):
    pass

class Complaint(ComplaintBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True