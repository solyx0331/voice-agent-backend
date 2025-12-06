"""
Global search endpoint
"""
from fastapi import APIRouter, Query, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.agent import VoiceAgent
from app.schemas.call import Call
from app.schemas.contact import Contact
from app.core.database import get_db
from pydantic import BaseModel

router = APIRouter()


class SearchResults(BaseModel):
    """Search results"""
    agents: List[VoiceAgent]
    calls: List[Call]
    contacts: List[Contact]


@router.get("", response_model=SearchResults)
async def search_global(
    query: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db)
):
    """Global search across agents, calls, and contacts"""
    from app.crud import agent as crud_agent, call as crud_call, contact as crud_contact
    
    query_lower = query.lower()
    
    agents_list = await crud_agent.search(db, search=query_lower) if hasattr(crud_agent, 'search') else []
    calls_list = await crud_call.search(db, search=query_lower)
    contacts_list = await crud_contact.search(db, search=query_lower)
    
    return SearchResults(
        agents=[VoiceAgent.model_validate(a) for a in agents_list],
        calls=[Call.model_validate(c) for c in calls_list],
        contacts=[Contact.model_validate(c) for c in contacts_list]
    )

