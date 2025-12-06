"""
Voice Agent database model
"""
from sqlalchemy import Column, String, Integer, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel


class AgentStatus(str, enum.Enum):
    """Agent status enum"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BUSY = "busy"


class VoiceAgent(BaseModel):
    """Voice Agent model"""
    __tablename__ = "voice_agents"
    
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(AgentStatus), default=AgentStatus.INACTIVE, nullable=False, index=True)
    calls_count = Column(Integer, default=0, nullable=False)
    avg_duration = Column(String(50), default="0:00", nullable=False)
    
    # JSON fields for complex configurations
    voice_config = Column(JSON, nullable=True)  # VoiceConfig
    greeting_script = Column(Text, nullable=True)
    faqs = Column(JSON, nullable=True)  # List[FAQ]
    intents = Column(JSON, nullable=True)  # List[Intent]
    call_rules = Column(JSON, nullable=True)  # CallRules
    lead_capture = Column(JSON, nullable=True)  # LeadCapture
    notifications = Column(JSON, nullable=True)  # Notifications
    base_logic = Column(JSON, nullable=True)  # BaseLogic
    
    # Relationships
    calls = relationship("Call", back_populates="agent", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<VoiceAgent(id={self.id}, name={self.name}, status={self.status})>"

