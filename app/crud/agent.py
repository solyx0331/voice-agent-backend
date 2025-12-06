"""
CRUD operations for Voice Agents
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.crud.base import CRUDBase
from app.models.agent import VoiceAgent
from app.schemas.agent import VoiceAgentCreate, VoiceAgentUpdate


class CRUDAgent(CRUDBase[VoiceAgent]):
    """CRUD operations for VoiceAgent"""
    
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[VoiceAgent]:
        """Get agent by name"""
        result = await db.execute(
            select(VoiceAgent).where(VoiceAgent.name == name)
        )
        return result.scalar_one_or_none()
    
    async def get_with_calls(self, db: AsyncSession, *, id: str) -> Optional[VoiceAgent]:
        """Get agent with related calls"""
        result = await db.execute(
            select(VoiceAgent)
            .options(selectinload(VoiceAgent.calls))
            .where(VoiceAgent.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_status(
        self,
        db: AsyncSession,
        *,
        status: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[VoiceAgent]:
        """Get agents by status"""
        result = await db.execute(
            select(VoiceAgent)
            .where(VoiceAgent.status == status)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_active_count(self, db: AsyncSession) -> int:
        """Get count of active agents"""
        result = await db.execute(
            select(func.count(VoiceAgent.id)).where(VoiceAgent.status == "active")
        )
        return result.scalar() or 0
    
    async def create(self, db: AsyncSession, *, obj_in: VoiceAgentCreate) -> VoiceAgent:
        """Create a new agent"""
        obj_data = obj_in.model_dump()
        db_obj = VoiceAgent(**obj_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: VoiceAgent,
        obj_in: VoiceAgentUpdate
    ) -> VoiceAgent:
        """Update an agent"""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


agent = CRUDAgent(VoiceAgent)

