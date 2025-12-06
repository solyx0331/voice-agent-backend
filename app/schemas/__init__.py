"""Pydantic schemas"""
from app.schemas.common import ResponseModel, PaginationParams, PaginatedResponse, ErrorResponse
from app.schemas.call import Call, CallCreate, CallUpdate, CallFilter, TranscriptEntry, CallLatency
from app.schemas.agent import (
    VoiceAgent, VoiceAgentCreate, VoiceAgentUpdate, VoiceAgentDetails,
    VoiceConfig, FAQ, Intent, CallRules, LeadCapture, Notifications, BaseLogic
)
from app.schemas.contact import Contact, ContactCreate, ContactUpdate, ContactFilter
from app.schemas.dashboard import DashboardStats, LiveCall, AnalyticsData, LiveCallTranscript
from app.schemas.settings import (
    ProfileUpdate, VoiceSettingsUpdate, NotificationSettingsUpdate,
    PasswordChange, TwoFactorSetup, TwoFactorVerify, Session,
    BillingInfo, PaymentMethodUpdate, Invoice, ApiKey, ApiKeyCreate,
    Webhook, WebhookCreate, WebhookUpdate
)

__all__ = [
    # Common
    "ResponseModel", "PaginationParams", "PaginatedResponse", "ErrorResponse",
    # Call
    "Call", "CallCreate", "CallUpdate", "CallFilter", "TranscriptEntry", "CallLatency",
    # Agent
    "VoiceAgent", "VoiceAgentCreate", "VoiceAgentUpdate", "VoiceAgentDetails",
    "VoiceConfig", "FAQ", "Intent", "CallRules", "LeadCapture", "Notifications", "BaseLogic",
    # Contact
    "Contact", "ContactCreate", "ContactUpdate", "ContactFilter",
    # Dashboard
    "DashboardStats", "LiveCall", "AnalyticsData", "LiveCallTranscript",
    # Settings
    "ProfileUpdate", "VoiceSettingsUpdate", "NotificationSettingsUpdate",
    "PasswordChange", "TwoFactorSetup", "TwoFactorVerify", "Session",
    "BillingInfo", "PaymentMethodUpdate", "Invoice", "ApiKey", "ApiKeyCreate",
    "Webhook", "WebhookCreate", "WebhookUpdate",
]
