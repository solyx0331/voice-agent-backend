"""
Dashboard endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta, date
from typing import List, Optional
from app.schemas.dashboard import DashboardStats, LiveCall, AnalyticsData
from app.core.database import get_db
from app.models.call import Call, CallStatus, CallType
from app.models.agent import VoiceAgent, AgentStatus

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """Get dashboard statistics"""
    today = date.today()
    
    # Get today's call count
    today_calls_result = await db.execute(
        select(func.count(Call.id)).where(Call.date == today)
    )
    total_calls_today = today_calls_result.scalar() or 0
    
    # Get active agents count
    active_agents_result = await db.execute(
        select(func.count(VoiceAgent.id)).where(VoiceAgent.status == AgentStatus.ACTIVE)
    )
    active_agents = active_agents_result.scalar() or 0
    
    avg_duration = "4:32"
    
    completed_calls_result = await db.execute(
        select(func.count(Call.id)).where(Call.status == CallStatus.COMPLETED)
    )
    completed_calls = completed_calls_result.scalar() or 0
    
    total_calls_result = await db.execute(select(func.count(Call.id)))
    total_calls = total_calls_result.scalar() or 0
    
    success_rate = (completed_calls / total_calls * 100) if total_calls > 0 else 0.0
    
    calls_change = 12.5
    duration_change = -2.3
    success_rate_change = 1.2
    
    return DashboardStats(
        total_calls_today=total_calls_today,
        active_agents=active_agents,
        avg_call_duration=avg_duration,
        success_rate=round(success_rate, 2),
        calls_change=calls_change,
        duration_change=duration_change,
        success_rate_change=success_rate_change
    )


@router.get("/live-call", response_model=Optional[LiveCall])
async def get_live_call(db: AsyncSession = Depends(get_db)):
    """Get current live call (if any)"""
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
async def get_live_calls(db: AsyncSession = Depends(get_db)):
    """Get all active live calls"""
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
async def get_analytics_data(db: AsyncSession = Depends(get_db)):
    """Get analytics data"""
    call_volume = []
    for i in range(7):
        day_date = date.today() - timedelta(days=6-i)
        day_name = day_date.strftime("%A")
        result = await db.execute(
            select(func.count(Call.id)).where(Call.date == day_date)
        )
        call_count = result.scalar() or 0
        call_volume.append({"name": day_name, "calls": call_count})
    
    hourly_data = []
    for hour in range(9, 14):
        result = await db.execute(
            select(func.count(Call.id)).where(
                func.extract('hour', Call.created_at) == hour
            )
        )
        call_count = result.scalar() or 0
        hourly_data.append({"hour": f"{hour}:00", "calls": call_count})
    
    agent_performance = []
    agents_result = await db.execute(select(VoiceAgent))
    agents = agents_result.scalars().all()
    for agent in agents:
        calls_result = await db.execute(
            select(func.count(Call.id)).where(Call.agent_id == str(agent.id))
        )
        total_calls = calls_result.scalar() or 0
        
        success_result = await db.execute(
            select(func.count(Call.id)).where(
                Call.agent_id == str(agent.id),
                Call.outcome == "success"
            )
        )
        success_calls = success_result.scalar() or 0
        
        agent_performance.append({
            "name": agent.name,
            "calls": total_calls,
            "success": success_calls
        })
    
    inbound_result = await db.execute(
        select(func.count(Call.id)).where(Call.type == CallType.INBOUND)
    )
    inbound_count = inbound_result.scalar() or 0
    
    outbound_result = await db.execute(
        select(func.count(Call.id)).where(Call.type == CallType.OUTBOUND)
    )
    outbound_count = outbound_result.scalar() or 0
    
    missed_result = await db.execute(
        select(func.count(Call.id)).where(Call.type == CallType.MISSED)
    )
    missed_count = missed_result.scalar() or 0
    
    total = inbound_count + outbound_count + missed_count
    inbound_pct = (inbound_count / total * 100) if total > 0 else 0
    outbound_pct = (outbound_count / total * 100) if total > 0 else 0
    missed_pct = (missed_count / total * 100) if total > 0 else 0
    
    call_type_data = [
        {"name": "Inbound", "value": round(inbound_pct), "color": "#3b82f6"},
        {"name": "Outbound", "value": round(outbound_pct), "color": "#10b981"},
        {"name": "Missed", "value": round(missed_pct), "color": "#ef4444"},
    ]
    
    return AnalyticsData(
        call_volume=call_volume,
        hourly_data=hourly_data,
        agent_performance=agent_performance,
        call_type_data=call_type_data
    )
