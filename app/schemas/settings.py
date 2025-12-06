"""
Settings schemas
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field


class ProfileUpdate(BaseModel):
    """Profile update request"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    company: Optional[str] = None
    timezone: Optional[str] = None


class VoiceSettingsUpdate(BaseModel):
    """Voice settings update request"""
    voice_model: Optional[str] = None
    speech_speed: Optional[float] = Field(None, ge=0.5, le=2.0)
    api_key: Optional[str] = None


class NotificationSettingsUpdate(BaseModel):
    """Notification settings update request"""
    settings: Dict[str, bool] = Field(default_factory=dict)


class PasswordChange(BaseModel):
    """Password change request"""
    current_password: str
    new_password: str = Field(min_length=8)


class TwoFactorSetup(BaseModel):
    """2FA setup response"""
    secret: str
    qr_code: str


class TwoFactorVerify(BaseModel):
    """2FA verification request"""
    code: str = Field(min_length=6, max_length=6)


class Session(BaseModel):
    """Active session"""
    id: str
    device: str
    location: str
    last_active: str
    current: bool


class BillingInfo(BaseModel):
    """Billing information"""
    plan: str
    status: str
    next_billing_date: str
    amount: str
    payment_method: Dict[str, Any]


class PaymentMethodUpdate(BaseModel):
    """Payment method update request"""
    card_number: str
    expiry: str
    cvv: str
    name: str


class Invoice(BaseModel):
    """Invoice"""
    id: str
    date: str
    amount: str
    status: str
    download_url: str


class ApiKey(BaseModel):
    """API Key"""
    id: str
    name: str
    key: str
    created_at: str
    last_used: Optional[str] = None


class ApiKeyCreate(BaseModel):
    """Create API key request"""
    name: str


class Webhook(BaseModel):
    """Webhook configuration"""
    id: str
    url: str
    events: List[str]
    status: str
    created_at: Optional[str] = None


class WebhookCreate(BaseModel):
    """Create webhook request"""
    url: str
    events: List[str]


class WebhookUpdate(BaseModel):
    """Update webhook request"""
    url: Optional[str] = None
    events: Optional[List[str]] = None
    status: Optional[str] = None

