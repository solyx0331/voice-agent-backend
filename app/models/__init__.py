"""Data models"""
from app.models.base import BaseModel
from app.models.agent import VoiceAgent, AgentStatus
from app.models.contact import Contact, ContactStatus
from app.models.call import Call, CallType, CallStatus, CallOutcome

# Import all models for Alembic
from app.core.database import Base

__all__ = [
    "BaseModel",
    "VoiceAgent",
    "AgentStatus",
    "Contact",
    "ContactStatus",
    "Call",
    "CallType",
    "CallStatus",
    "CallOutcome",
    "Base",
]
