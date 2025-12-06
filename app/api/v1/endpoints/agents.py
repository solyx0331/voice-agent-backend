"""
Voice Agent endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.schemas.agent import (
    VoiceAgent, VoiceAgentCreate, VoiceAgentUpdate, VoiceAgentDetails
)
from app.schemas.call import Call
from app.core.database import agents_db, calls_db, init_sample_data

router = APIRouter()


@router.get("", response_model=List[VoiceAgent])
async def get_voice_agents():
    """Get all voice agents"""
    # TODO: Replace with database query
    init_sample_data()
    return agents_db


@router.get("/{agent_id}", response_model=VoiceAgentDetails)
async def get_agent_details(agent_id: str):
    """Get agent details with additional metrics"""
    # TODO: Replace with database query
    agent = next((a for a in agents_db if a.id == agent_id), None)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found"
        )
    
    return VoiceAgentDetails(
        **agent.model_dump(),
        created_at="2024-01-15",
        last_active="2 hours ago",
        total_calls=agent.calls,
        success_rate=94.5
    )


@router.post("", response_model=VoiceAgent, status_code=status.HTTP_201_CREATED)
async def create_agent(agent: VoiceAgentCreate):
    """Create a new voice agent"""
    # TODO: Replace with database insert
    new_agent = VoiceAgent(
        id=str(len(agents_db) + 1),
        **agent.model_dump()
    )
    agents_db.append(new_agent)
    return new_agent


@router.put("/{agent_id}", response_model=VoiceAgent)
async def update_agent(agent_id: str, agent_update: VoiceAgentUpdate):
    """Update a voice agent"""
    # TODO: Replace with database update
    agent = next((a for a in agents_db if a.id == agent_id), None)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found"
        )
    
    update_data = agent_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)
    
    return agent


@router.patch("/{agent_id}/status", response_model=VoiceAgent)
async def update_agent_status(agent_id: str, status_value: str):
    """Update agent status"""
    agent = next((a for a in agents_db if a.id == agent_id), None)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found"
        )
    
    if status_value not in ["active", "inactive", "busy"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be 'active', 'inactive', or 'busy'"
        )
    
    agent.status = status_value
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(agent_id: str):
    """Delete a voice agent"""
    # TODO: Replace with database delete
    from app.core.database import agents_db
    agent = next((a for a in agents_db if a.id == agent_id), None)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found"
        )
    
    agents_db.remove(agent)
    return None


@router.get("/{agent_id}/calls", response_model=List[Call])
async def get_agent_calls(agent_id: str, limit: Optional[int] = None):
    """Get calls for a specific agent"""
    # TODO: Replace with database query
    agent = next((a for a in agents_db if a.id == agent_id), None)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found"
        )
    
    # Filter calls by agent
    calls = [c for c in calls_db if c.agent_id == agent_id or c.agent == agent.name]
    if limit:
        calls = calls[:limit]
    
    return calls

