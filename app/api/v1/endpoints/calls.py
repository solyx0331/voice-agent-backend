"""
Call endpoints
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from app.schemas.call import Call, CallCreate, CallUpdate, CallFilter
from app.schemas.common import PaginatedResponse
from app.core.database import calls_db, init_sample_data

router = APIRouter()


@router.get("", response_model=List[Call])
async def get_calls(
    search: Optional[str] = Query(None),
    agent: Optional[str] = Query(None),
    agent_id: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    date_range_start: Optional[str] = Query(None),
    date_range_end: Optional[str] = Query(None),
):
    """Get calls with optional filtering"""
    # TODO: Replace with database query
    init_sample_data()
    
    filtered_calls = calls_db.copy()
    
    if search:
        search_lower = search.lower()
        filtered_calls = [
            c for c in filtered_calls
            if search_lower in c.contact.lower()
            or search_lower in c.phone
            or search_lower in c.agent.lower()
        ]
    
    if agent:
        filtered_calls = [c for c in filtered_calls if c.agent == agent]
    
    if agent_id:
        filtered_calls = [c for c in filtered_calls if c.agent_id == agent_id]
    
    if type:
        filtered_calls = [c for c in filtered_calls if c.type == type]
    
    if status:
        filtered_calls = [c for c in filtered_calls if c.status == status]
    
    # TODO: Implement date range filtering
    
    return filtered_calls


@router.get("/{call_id}", response_model=Call)
async def get_call(call_id: str):
    """Get a specific call by ID"""
    call = next((c for c in calls_db if c.id == call_id), None)
    if not call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Call with id {call_id} not found"
        )
    return call


@router.post("", response_model=Call, status_code=status.HTTP_201_CREATED)
async def create_call(call: CallCreate):
    """Create a new call record"""
    new_call = Call(
        id=str(len(calls_db) + 1),
        **call.model_dump()
    )
    calls_db.append(new_call)
    return new_call


@router.put("/{call_id}", response_model=Call)
async def update_call(call_id: str, call_update: CallUpdate):
    """Update a call record"""
    call = next((c for c in calls_db if c.id == call_id), None)
    if not call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Call with id {call_id} not found"
        )
    
    update_data = call_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(call, field, value)
    
    return call


@router.delete("/{call_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_call(call_id: str):
    """Delete a call record"""
    from app.core.database import calls_db
    call = next((c for c in calls_db if c.id == call_id), None)
    if not call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Call with id {call_id} not found"
        )
    
    calls_db.remove(call)
    return None


@router.get("/{call_id}/recording", response_model=dict)
async def get_call_recording(call_id: str):
    """Get call recording URL"""
    call = next((c for c in calls_db if c.id == call_id), None)
    if not call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Call with id {call_id} not found"
        )
    
    if not call.recording:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No recording available for this call"
        )
    
    return {
        "url": f"/recordings/{call_id}.mp3",
        "call_id": call_id
    }


@router.post("/export")
async def export_calls(format: str = Query("csv", regex="^(csv|json)$")):
    """Export calls in CSV or JSON format"""
    # TODO: Implement actual export logic
    if format == "csv":
        # Generate CSV
        return {"message": "CSV export not yet implemented"}
    else:
        # Return JSON
        return calls_db

