"""
Call endpoints
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from datetime import date as date_type
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.call import Call, CallCreate, CallUpdate
from app.core.database import get_db
from app.crud import call as crud_call

router = APIRouter()


def convert_db_call_to_schema(db_call) -> Call:
    """Convert database call model to schema"""
    return Call(
        id=str(db_call.id),
        contact=db_call.contact_name,
        phone=db_call.phone,
        agent=db_call.agent_name,
        agent_id=str(db_call.agent_id) if db_call.agent_id else None,
        type=db_call.type.value,
        duration=db_call.duration,
        date=db_call.date.isoformat() if db_call.date else "",
        time=db_call.time.strftime("%H:%M") if db_call.time else "",
        status=db_call.status.value,
        recording=db_call.recording,
        outcome=db_call.outcome.value if db_call.outcome else None,
        latency={
            "avg": db_call.latency_avg,
            "peak": db_call.latency_peak
        } if db_call.latency_avg and db_call.latency_peak else None,
        transcript=db_call.transcript
    )


@router.get("", response_model=List[Call])
async def get_calls(
    search: Optional[str] = Query(None),
    agent: Optional[str] = Query(None),
    agent_id: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    date_range_start: Optional[str] = Query(None),
    date_range_end: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get calls with optional filtering"""
    # Parse date range
    date_start = None
    date_end = None
    if date_range_start:
        date_start = date_type.fromisoformat(date_range_start)
    if date_range_end:
        date_end = date_type.fromisoformat(date_range_end)
    
    # Use search or filter
    if search:
        calls = await crud_call.search(db, search=search, skip=skip, limit=limit)
    else:
        calls = await crud_call.filter_calls(
            db,
            agent_id=agent_id,
            agent_name=agent,
            call_type=type,
            status=status,
            date_start=date_start,
            date_end=date_end,
            skip=skip,
            limit=limit
        )
    
    return [convert_db_call_to_schema(c) for c in calls]


@router.get("/{call_id}", response_model=Call)
async def get_call(
    call_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific call by ID"""
    db_call = await crud_call.get(db, id=call_id)
    if not db_call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Call with id {call_id} not found"
        )
    return convert_db_call_to_schema(db_call)


@router.post("", response_model=Call, status_code=status.HTTP_201_CREATED)
async def create_call(
    call: CallCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new call record"""
    db_call = await crud_call.create(db, obj_in=call)
    return convert_db_call_to_schema(db_call)


@router.put("/{call_id}", response_model=Call)
async def update_call(
    call_id: str,
    call_update: CallUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a call record"""
    db_call = await crud_call.get(db, id=call_id)
    if not db_call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Call with id {call_id} not found"
        )
    
    db_call = await crud_call.update(db, db_obj=db_call, obj_in=call_update)
    return convert_db_call_to_schema(db_call)


@router.delete("/{call_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_call(
    call_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a call record"""
    db_call = await crud_call.delete(db, id=call_id)
    if not db_call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Call with id {call_id} not found"
        )
    return None


@router.get("/{call_id}/recording", response_model=dict)
async def get_call_recording(
    call_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get call recording URL"""
    db_call = await crud_call.get(db, id=call_id)
    if not db_call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Call with id {call_id} not found"
        )
    
    if not db_call.recording:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No recording available for this call"
        )
    
    return {
        "url": db_call.recording_url or f"/recordings/{call_id}.mp3",
        "call_id": call_id
    }


@router.post("/export")
async def export_calls(
    format: str = Query("csv", regex="^(csv|json)$"),
    db: AsyncSession = Depends(get_db)
):
    """Export calls in CSV or JSON format"""
    calls = await crud_call.get_multi(db, skip=0, limit=10000)
    
    if format == "csv":
        # Generate CSV
        import csv
        from io import StringIO
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Contact", "Phone", "Agent", "Type", "Duration", "Date", "Time", "Status"])
        for call in calls:
            writer.writerow([
                call.contact_name,
                call.phone,
                call.agent_name,
                call.type.value,
                call.duration,
                call.date.isoformat() if call.date else "",
                call.time.strftime("%H:%M") if call.time else "",
                call.status.value
            ])
        from fastapi.responses import Response
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=calls.csv"}
        )
    else:
        # Return JSON
        return [convert_db_call_to_schema(c) for c in calls]
