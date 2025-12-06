"""
Dashboard endpoints
"""
from fastapi import APIRouter
from app.schemas.dashboard import DashboardStats, LiveCall, AnalyticsData
from datetime import datetime, timedelta
from typing import List, Optional, Union

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """Get dashboard statistics"""
    # TODO: Replace with actual database queries
    return DashboardStats(
        total_calls_today=42,
        active_agents=3,
        avg_call_duration="4:32",
        success_rate=94.5,
        calls_change=12.5,
        duration_change=-2.3,
        success_rate_change=1.2
    )


@router.get("/live-call", response_model=Optional[LiveCall])
async def get_live_call():
    """Get current live call (if any)"""
    # TODO: Replace with actual database/WebSocket query
    # Randomly return a live call or None
    import random
    if random.random() > 0.3:
        return LiveCall(
            id="live-1",
            contact="John Doe",
            phone="+1 (555) 123-4567",
            agent="Support Bot",
            agent_id="1",
            duration=120,
            start_time=(datetime.utcnow() - timedelta(seconds=120)).isoformat(),
            type="inbound",
            status="active",
            transcript=[
                {"speaker": "ai", "text": "Hello! How can I assist you today?", "timestamp": "00:00"},
                {"speaker": "user", "text": "I need help with my account", "timestamp": "00:03"},
            ],
            sentiment="neutral",
            is_muted=False,
            is_on_hold=False
        )
    return None


@router.get("/live-calls", response_model=List[LiveCall])
async def get_live_calls():
    """Get all active live calls"""
    # TODO: Replace with actual database/WebSocket query
    return [
        LiveCall(
            id="live-1",
            contact="John Doe",
            phone="+1 (555) 123-4567",
            agent="Support Bot",
            agent_id="1",
            duration=120,
            start_time=(datetime.utcnow() - timedelta(seconds=120)).isoformat(),
            type="inbound",
            status="active",
            transcript=[
                {"speaker": "ai", "text": "Hello! How can I assist you today?", "timestamp": "00:00"},
            ],
            sentiment="neutral",
            is_muted=False,
            is_on_hold=False
        )
    ]


@router.get("/analytics", response_model=AnalyticsData)
async def get_analytics_data():
    """Get analytics data"""
    # TODO: Replace with actual database queries
    return AnalyticsData(
        call_volume=[
            {"name": "Monday", "calls": 45},
            {"name": "Tuesday", "calls": 52},
            {"name": "Wednesday", "calls": 48},
            {"name": "Thursday", "calls": 61},
            {"name": "Friday", "calls": 55},
        ],
        hourly_data=[
            {"hour": "9:00", "calls": 5},
            {"hour": "10:00", "calls": 8},
            {"hour": "11:00", "calls": 12},
            {"hour": "12:00", "calls": 15},
            {"hour": "13:00", "calls": 10},
        ],
        agent_performance=[
            {"name": "Support Bot", "calls": 120, "success": 115},
            {"name": "Sales Bot", "calls": 95, "success": 88},
            {"name": "HR Bot", "calls": 75, "success": 72},
        ],
        call_type_data=[
            {"name": "Inbound", "value": 65, "color": "#3b82f6"},
            {"name": "Outbound", "value": 30, "color": "#10b981"},
            {"name": "Missed", "value": 5, "color": "#ef4444"},
        ]
    )

