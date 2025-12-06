"""
Voice Agent endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.agent import (
    VoiceAgent, VoiceAgentCreate, VoiceAgentUpdate, VoiceAgentDetails
)
from app.schemas.call import Call
from app.core.database import get_db
from app.crud import agent as crud_agent
from app.crud import call as crud_call
from datetime import datetime

router = APIRouter()


@router.get("", response_model=List[VoiceAgent])
async def get_voice_agents(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get all voice agents"""
    agents = await crud_agent.get_multi(db, skip=skip, limit=limit)
    return [VoiceAgent.model_validate(a) for a in agents]


@router.get("/{agent_id}", response_model=VoiceAgentDetails)
async def get_agent_details(
    agent_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get agent details with additional metrics"""
    db_agent = await crud_agent.get(db, id=agent_id)
    if not db_agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found"
        )
    
    # Get call statistics
    agent_calls = await crud_call.get_by_agent(db, agent_id=agent_id)
    total_calls = len(agent_calls)
    successful_calls = len([c for c in agent_calls if c.outcome == "success"])
    success_rate = (successful_calls / total_calls * 100) if total_calls > 0 else 0.0
    
    # Get last active time (from most recent call)
    last_active = "Never"
    if agent_calls:
        latest_call = max(agent_calls, key=lambda c: c.created_at)
        time_diff = datetime.utcnow() - latest_call.created_at
        if time_diff.days > 0:
            last_active = f"{time_diff.days} days ago"
        elif time_diff.seconds > 3600:
            last_active = f"{time_diff.seconds // 3600} hours ago"
        else:
            last_active = f"{time_diff.seconds // 60} minutes ago"
    
    agent_dict = {
        "id": str(db_agent.id),
        "name": db_agent.name,
        "description": db_agent.description,
        "status": db_agent.status.value,
        "calls": db_agent.calls_count,
        "avg_duration": db_agent.avg_duration,
        "voice": db_agent.voice_config,
        "greeting_script": db_agent.greeting_script,
        "faqs": db_agent.faqs,
        "intents": db_agent.intents,
        "call_rules": db_agent.call_rules,
        "lead_capture": db_agent.lead_capture,
        "notifications": db_agent.notifications,
        "base_logic": db_agent.base_logic,
        "created_at": db_agent.created_at.isoformat() if db_agent.created_at else "",
        "last_active": last_active,
        "total_calls": total_calls,
        "success_rate": success_rate
    }
    
    return VoiceAgentDetails(**agent_dict)


@router.post("", response_model=VoiceAgent, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent: VoiceAgentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new voice agent"""
    db_agent = await crud_agent.create(db, obj_in=agent)
    return VoiceAgent.model_validate(db_agent)


@router.put("/{agent_id}", response_model=VoiceAgent)
async def update_agent(
    agent_id: str,
    agent_update: VoiceAgentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a voice agent"""
    db_agent = await crud_agent.get(db, id=agent_id)
    if not db_agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found"
        )
    
    db_agent = await crud_agent.update(db, db_obj=db_agent, obj_in=agent_update)
    return VoiceAgent.model_validate(db_agent)


@router.patch("/{agent_id}/status", response_model=VoiceAgent)
async def update_agent_status(
    agent_id: str,
    status_value: str,
    db: AsyncSession = Depends(get_db)
):
    """Update agent status"""
    db_agent = await crud_agent.get(db, id=agent_id)
    if not db_agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found"
        )
    
    if status_value not in ["active", "inactive", "busy"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be 'active', 'inactive', or 'busy'"
        )
    
    from app.models.agent import AgentStatus
    db_agent.status = AgentStatus(status_value)
    db.add(db_agent)
    await db.commit()
    await db.refresh(db_agent)
    
    return VoiceAgent.model_validate(db_agent)


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a voice agent"""
    db_agent = await crud_agent.delete(db, id=agent_id)
    if not db_agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found"
        )
    return None


@router.get("/{agent_id}/calls", response_model=List[Call])
async def get_agent_calls(
    agent_id: str,
    limit: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get calls for a specific agent"""
    db_agent = await crud_agent.get(db, id=agent_id)
    if not db_agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found"
        )
    
    calls = await crud_call.get_by_agent(db, agent_id=agent_id, limit=limit or 100)
    
    # Convert to schema format
    result = []
    for c in calls:
        call_dict = {
            "id": str(c.id),
            "contact": c.contact_name,
            "phone": c.phone,
            "agent": c.agent_name,
            "agent_id": str(c.agent_id) if c.agent_id else None,
            "type": c.type.value,
            "duration": c.duration,
            "date": c.date.isoformat() if c.date else "",
            "time": c.time.strftime("%H:%M") if c.time else "",
            "status": c.status.value,
            "recording": c.recording,
            "outcome": c.outcome.value if c.outcome else None,
            "latency": {
                "avg": c.latency_avg,
                "peak": c.latency_peak
            } if c.latency_avg and c.latency_peak else None,
            "transcript": c.transcript
        }
        result.append(Call(**call_dict))
    
    return result
