"""
Dashboard schemas
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class DashboardStats(BaseModel):
    """Dashboard statistics"""
    total_calls_today: int
    active_agents: int
    avg_call_duration: str
    success_rate: float
    calls_change: float = Field(description="Percentage change in calls")
    duration_change: float = Field(description="Percentage change in duration")
    success_rate_change: float = Field(description="Percentage change in success rate")


class LiveCallTranscript(BaseModel):
    """Live call transcript entry"""
    speaker: str = Field(description="'user' or 'ai'")
    text: str
    timestamp: str


class LiveCall(BaseModel):
    """Live call model"""
    id: str
    contact: str
    phone: str
    agent: str
    agent_id: Optional[str] = None
    duration: int = Field(description="Duration in seconds")
    start_time: str = Field(description="ISO format datetime")
    type: Optional[str] = Field(None, description="'inbound' or 'outbound'")
    status: Optional[str] = Field(None, description="'active', 'on_hold', or 'transferring'")
    transcript: Optional[List[LiveCallTranscript]] = None
    sentiment: Optional[str] = Field(None, description="'positive', 'neutral', or 'negative'")
    is_muted: bool = False
    is_on_hold: bool = False


class AnalyticsData(BaseModel):
    """Analytics data"""
    call_volume: List[Dict[str, Any]] = Field(description="Call volume by name")
    hourly_data: List[Dict[str, Any]] = Field(description="Hourly call data")
    agent_performance: List[Dict[str, Any]] = Field(description="Agent performance metrics")
    call_type_data: List[Dict[str, Any]] = Field(description="Call type distribution")

