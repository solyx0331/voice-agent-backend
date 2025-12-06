"""
Voice Agent schemas
"""
from typing import Optional, List, Literal, Dict, Any
from pydantic import BaseModel, Field


class VoiceConfig(BaseModel):
    """Voice configuration"""
    type: Literal["generic", "custom"] = "generic"
    generic_voice: Optional[str] = Field(None, description="Generic voice name, e.g., 'ElevenLabs - Aria'")
    custom_voice_id: Optional[str] = Field(None, description="Retell voice ID")
    custom_voice_url: Optional[str] = Field(None, description="Uploaded voice file URL")


class FAQ(BaseModel):
    """FAQ entry"""
    question: str
    answer: str


class Intent(BaseModel):
    """Intent configuration"""
    name: str
    prompt: str
    response: Optional[str] = None


class BusinessHoursSchedule(BaseModel):
    """Business hours schedule entry"""
    day: str = Field(description="Day of week: monday, tuesday, etc.")
    start: str = Field(description="Start time in HH:MM format")
    end: str = Field(description="End time in HH:MM format")


class CallRules(BaseModel):
    """Call rules configuration"""
    business_hours: Dict[str, Any] = Field(
        default_factory=lambda: {
            "enabled": False,
            "timezone": "UTC",
            "schedule": []
        }
    )
    fallback_to_voicemail: bool = False
    voicemail_message: Optional[str] = None


class LeadCaptureField(BaseModel):
    """Lead capture field"""
    name: str
    question: str
    required: bool = False
    type: Literal["text", "email", "phone", "number"] = "text"


class LeadCapture(BaseModel):
    """Lead capture configuration"""
    fields: List[LeadCaptureField] = Field(default_factory=list)


class CRMConfig(BaseModel):
    """CRM integration configuration"""
    type: Literal["webhook", "salesforce", "hubspot", "zapier"]
    endpoint: Optional[str] = None
    api_key: Optional[str] = None


class Notifications(BaseModel):
    """Notifications configuration"""
    email: Optional[str] = None
    crm: Optional[CRMConfig] = None


class BaseLogic(BaseModel):
    """Base receptionist logic"""
    greeting_message: str
    primary_intent_prompts: List[str] = Field(default_factory=list)
    lead_capture_questions: List[Dict[str, str]] = Field(default_factory=list)
    response_logic: Optional[List[Dict[str, str]]] = None


class VoiceAgentBase(BaseModel):
    """Base voice agent model"""
    name: str
    description: str
    status: Literal["active", "inactive", "busy"] = "inactive"
    calls: int = 0
    avg_duration: str = "0:00"
    voice: Optional[VoiceConfig] = None
    greeting_script: Optional[str] = None
    faqs: Optional[List[FAQ]] = None
    intents: Optional[List[Intent]] = None
    call_rules: Optional[CallRules] = None
    lead_capture: Optional[LeadCapture] = None
    notifications: Optional[Notifications] = None
    base_logic: Optional[BaseLogic] = None


class VoiceAgent(VoiceAgentBase):
    """Voice agent model with ID"""
    id: str

    class Config:
        from_attributes = True


class VoiceAgentCreate(VoiceAgentBase):
    """Create voice agent request"""
    pass


class VoiceAgentUpdate(BaseModel):
    """Update voice agent request"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["active", "inactive", "busy"]] = None
    voice: Optional[VoiceConfig] = None
    greeting_script: Optional[str] = None
    faqs: Optional[List[FAQ]] = None
    intents: Optional[List[Intent]] = None
    call_rules: Optional[CallRules] = None
    lead_capture: Optional[LeadCapture] = None
    notifications: Optional[Notifications] = None
    base_logic: Optional[BaseLogic] = None


class VoiceAgentDetails(VoiceAgent):
    """Voice agent with additional details"""
    created_at: str
    last_active: str
    total_calls: int
    success_rate: float

