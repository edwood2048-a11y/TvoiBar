from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    gender = Column(String, nullable=True)  # 'male', 'female', 'other'
    trusted_contact = Column(String, nullable=True)  # phone or telegram id
    photo_url = Column(String, nullable=True)  # profile photo URL
    created_at = Column(DateTime, default=datetime.utcnow)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    date_time = Column(DateTime, nullable=True)
    max_participants = Column(Integer, default=10)
    current_participants = Column(Integer, default=0)
    creator_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("User")

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    status = Column(String, default="pending")  # pending, accepted, rejected
    meeting_status = Column(String, default="not_started")  # not_started, in_progress, completed, emergency
    message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    event = relationship("Event")

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    complainant_id = Column(Integer, ForeignKey("users.id"))  # who complains
    accused_id = Column(Integer, ForeignKey("users.id"))  # who is accused
    reason = Column(String)  # e.g., "fake_photo", "no_show", "inappropriate"
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    complainant = relationship("User", foreign_keys=[complainant_id])
    accused = relationship("User", foreign_keys=[accused_id])