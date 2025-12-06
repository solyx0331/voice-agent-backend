"""
Call database model
"""
from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, Enum as SQLEnum, Date, Time, JSON
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel


class CallType(str, enum.Enum):
    """Call type enum"""
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    MISSED = "missed"


class CallStatus(str, enum.Enum):
    """Call status enum"""
    COMPLETED = "completed"
    MISSED = "missed"
    VOICEMAIL = "voicemail"


class CallOutcome(str, enum.Enum):
    """Call outcome enum"""
    SUCCESS = "success"
    CALLER_HUNG_UP = "caller_hung_up"
    SPEECH_NOT_RECOGNIZED = "speech_not_recognized"
    OTHER = "other"


class Call(BaseModel):
    """Call model"""
    __tablename__ = "calls"
    
    # Foreign keys
    contact_id = Column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True, index=True)
    agent_id = Column(String(36), ForeignKey("voice_agents.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Contact info (denormalized for performance)
    contact_name = Column(String(255), nullable=False, index=True)
    phone = Column(String(50), nullable=False, index=True)
    agent_name = Column(String(255), nullable=False, index=True)
    
    # Call details
    type = Column(SQLEnum(CallType), nullable=False, index=True)
    duration = Column(String(50), nullable=False)  # Stored as "MM:SS" format
    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=False)
    status = Column(SQLEnum(CallStatus), nullable=False, index=True)
    recording = Column(Boolean, default=False, nullable=False)
    outcome = Column(SQLEnum(CallOutcome), nullable=True)
    
    # Metrics and data
    latency_avg = Column(Float, nullable=True)  # Average latency in milliseconds
    latency_peak = Column(Float, nullable=True)  # Peak latency in milliseconds
    transcript = Column(JSON, nullable=True)  # List[TranscriptEntry]
    recording_url = Column(String(500), nullable=True)
    
    # Relationships
    contact = relationship("Contact", back_populates="calls")
    agent = relationship("VoiceAgent", back_populates="calls")
    
    def __repr__(self):
        return f"<Call(id={self.id}, contact={self.contact_name}, type={self.type}, status={self.status})>"

