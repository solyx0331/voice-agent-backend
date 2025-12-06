"""
Call-related schemas
"""
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class TranscriptEntry(BaseModel):
    """Transcript entry"""
    speaker: Literal["user", "ai"]
    text: str
    timestamp: str


class CallLatency(BaseModel):
    """Call latency metrics"""
    avg: float = Field(description="Average latency in milliseconds")
    peak: float = Field(description="Peak latency in milliseconds")


class CallBase(BaseModel):
    """Base call model"""
    contact: str
    phone: str
    agent: str
    agent_id: Optional[str] = None
    type: Literal["inbound", "outbound", "missed"]
    duration: str
    date: str
    time: str
    status: Literal["completed", "missed", "voicemail"]
    recording: bool = False
    outcome: Optional[Literal["success", "caller_hung_up", "speech_not_recognized", "other"]] = None
    latency: Optional[CallLatency] = None
    transcript: Optional[List[TranscriptEntry]] = None


class Call(CallBase):
    """Call model with ID"""
    id: str

    class Config:
        from_attributes = True


class CallCreate(CallBase):
    """Create call request"""
    pass


class CallUpdate(BaseModel):
    """Update call request"""
    contact: Optional[str] = None
    phone: Optional[str] = None
    agent: Optional[str] = None
    agent_id: Optional[str] = None
    type: Optional[Literal["inbound", "outbound", "missed"]] = None
    duration: Optional[str] = None
    status: Optional[Literal["completed", "missed", "voicemail"]] = None
    recording: Optional[bool] = None
    outcome: Optional[Literal["success", "caller_hung_up", "speech_not_recognized", "other"]] = None
    transcript: Optional[List[TranscriptEntry]] = None


class CallFilter(BaseModel):
    """Call filter parameters"""
    search: Optional[str] = None
    agent: Optional[str] = None
    agent_id: Optional[str] = None
    type: Optional[Literal["inbound", "outbound", "missed"]] = None
    status: Optional[Literal["completed", "missed", "voicemail"]] = None
    date_range_start: Optional[str] = None
    date_range_end: Optional[str] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)

