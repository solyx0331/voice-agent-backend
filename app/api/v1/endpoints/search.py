"""
Global search endpoint
"""
from fastapi import APIRouter, Query
from typing import List
from app.schemas.agent import VoiceAgent
from app.schemas.call import Call
from app.schemas.contact import Contact
from pydantic import BaseModel

router = APIRouter()


class SearchResults(BaseModel):
    """Search results"""
    agents: List[VoiceAgent]
    calls: List[Call]
    contacts: List[Contact]


@router.get("", response_model=SearchResults)
async def search_global(query: str = Query(..., min_length=1)):
    """Global search across agents, calls, and contacts"""
    # TODO: Implement actual search logic with database
    query_lower = query.lower()
    
    # Mock data - replace with actual database queries
    agents = []
    calls = []
    contacts = []
    
    # In a real implementation, you would search across all tables
    # For now, return empty results
    return SearchResults(
        agents=agents,
        calls=calls,
        contacts=contacts
    )

