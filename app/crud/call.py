"""
CRUD operations for Calls
"""
from typing import Optional, List
from datetime import date, time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, func
from sqlalchemy.orm import selectinload
from app.crud.base import CRUDBase
from app.models.call import Call
from app.schemas.call import CallCreate, CallUpdate


class CRUDCall(CRUDBase[Call]):
    """CRUD operations for Call"""
    
    async def get_by_agent(
        self,
        db: AsyncSession,
        *,
        agent_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Call]:
        """Get calls by agent ID"""
        result = await db.execute(
            select(Call)
            .where(Call.agent_id == agent_id)
            .offset(skip)
            .limit(limit)
            .order_by(Call.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def get_by_contact(
        self,
        db: AsyncSession,
        *,
        contact_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Call]:
        """Get calls by contact ID"""
        result = await db.execute(
            select(Call)
            .where(Call.contact_id == contact_id)
            .offset(skip)
            .limit(limit)
            .order_by(Call.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def search(
        self,
        db: AsyncSession,
        *,
        search: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Call]:
        """Search calls by contact name, phone, or agent name"""
        search_pattern = f"%{search}%"
        result = await db.execute(
            select(Call)
            .where(
                or_(
                    Call.contact_name.ilike(search_pattern),
                    Call.phone.ilike(search_pattern),
                    Call.agent_name.ilike(search_pattern)
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(Call.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def filter_calls(
        self,
        db: AsyncSession,
        *,
        agent_id: Optional[str] = None,
        agent_name: Optional[str] = None,
        call_type: Optional[str] = None,
        status: Optional[str] = None,
        date_start: Optional[date] = None,
        date_end: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Call]:
        """Filter calls with multiple criteria"""
        query = select(Call)
        conditions = []
        
        if agent_id:
            conditions.append(Call.agent_id == agent_id)
        if agent_name:
            conditions.append(Call.agent_name.ilike(f"%{agent_name}%"))
        if call_type:
            conditions.append(Call.type == call_type)
        if status:
            conditions.append(Call.status == status)
        if date_start:
            conditions.append(Call.date >= date_start)
        if date_end:
            conditions.append(Call.date <= date_end)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        result = await db.execute(
            query.offset(skip).limit(limit).order_by(Call.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def get_today_count(self, db: AsyncSession) -> int:
        """Get count of calls today"""
        today = date.today()
        result = await db.execute(
            select(func.count(Call.id)).where(Call.date == today)
        )
        return result.scalar() or 0
    
    async def create(self, db: AsyncSession, *, obj_in: CallCreate) -> Call:
        """Create a new call"""
        obj_data = obj_in.model_dump()
        # Parse date and time strings
        if "date" in obj_data and isinstance(obj_data["date"], str):
            obj_data["date"] = date.fromisoformat(obj_data["date"])
        if "time" in obj_data and isinstance(obj_data["time"], str):
            time_parts = obj_data["time"].split(":")
            obj_data["time"] = time(int(time_parts[0]), int(time_parts[1]))
        
        # Handle JSON fields
        if "transcript" in obj_data and obj_data["transcript"]:
            obj_data["transcript"] = [t.model_dump() if hasattr(t, "model_dump") else t for t in obj_data["transcript"]]
        if "latency" in obj_data and obj_data["latency"]:
            latency = obj_data["latency"]
            obj_data["latency_avg"] = latency.get("avg") if isinstance(latency, dict) else latency.avg if hasattr(latency, "avg") else None
            obj_data["latency_peak"] = latency.get("peak") if isinstance(latency, dict) else latency.peak if hasattr(latency, "peak") else None
            del obj_data["latency"]
        
        db_obj = Call(**obj_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: Call,
        obj_in: CallUpdate
    ) -> Call:
        """Update a call"""
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # Handle date/time parsing
        if "date" in update_data and isinstance(update_data["date"], str):
            update_data["date"] = date.fromisoformat(update_data["date"])
        if "time" in update_data and isinstance(update_data["time"], str):
            time_parts = update_data["time"].split(":")
            update_data["time"] = time(int(time_parts[0]), int(time_parts[1]))
        
        # Handle JSON fields
        if "transcript" in update_data and update_data["transcript"]:
            update_data["transcript"] = [t.model_dump() if hasattr(t, "model_dump") else t for t in update_data["transcript"]]
        if "latency" in update_data and update_data["latency"]:
            latency = update_data["latency"]
            update_data["latency_avg"] = latency.get("avg") if isinstance(latency, dict) else latency.avg if hasattr(latency, "avg") else None
            update_data["latency_peak"] = latency.get("peak") if isinstance(latency, dict) else latency.peak if hasattr(latency, "peak") else None
            del update_data["latency"]
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


call = CRUDCall(Call)

