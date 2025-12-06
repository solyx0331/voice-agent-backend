"""
Contact endpoints
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.contact import Contact, ContactCreate, ContactUpdate
from app.schemas.call import Call
from app.core.database import get_db
from app.crud import contact as crud_contact
from app.crud import call as crud_call

router = APIRouter()


def convert_db_contact_to_schema(db_contact) -> Contact:
    """Convert database contact model to schema"""
    return Contact(
        id=str(db_contact.id),
        name=db_contact.name,
        email=db_contact.email,
        phone=db_contact.phone,
        company=db_contact.company,
        status=db_contact.status.value,
        total_calls=db_contact.total_calls,
        last_contact=db_contact.last_contact.isoformat() if db_contact.last_contact else ""
    )


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


@router.get("", response_model=List[Contact])
async def get_contacts(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get contacts with optional filtering"""
    if search:
        contacts = await crud_contact.search(db, search=search, skip=skip, limit=limit)
    elif status:
        contacts = await crud_contact.get_by_status(db, status=status, skip=skip, limit=limit)
    else:
        contacts = await crud_contact.get_multi(db, skip=skip, limit=limit)
    
    return [convert_db_contact_to_schema(c) for c in contacts]


@router.get("/{contact_id}", response_model=Contact)
async def get_contact(
    contact_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific contact by ID"""
    db_contact = await crud_contact.get(db, id=contact_id)
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found"
        )
    return convert_db_contact_to_schema(db_contact)


@router.post("", response_model=Contact, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact: ContactCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new contact"""
    db_contact = await crud_contact.create(db, obj_in=contact)
    return convert_db_contact_to_schema(db_contact)


@router.put("/{contact_id}", response_model=Contact)
async def update_contact(
    contact_id: str,
    contact_update: ContactUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a contact"""
    db_contact = await crud_contact.get(db, id=contact_id)
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found"
        )
    
    db_contact = await crud_contact.update(db, db_obj=db_contact, obj_in=contact_update)
    return convert_db_contact_to_schema(db_contact)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a contact"""
    db_contact = await crud_contact.delete(db, id=contact_id)
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found"
        )
    return None


@router.get("/{contact_id}/calls", response_model=List[Call])
async def get_contact_calls(
    contact_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get calls for a specific contact"""
    db_contact = await crud_contact.get(db, id=contact_id)
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found"
        )
    
    calls = await crud_call.get_by_contact(db, contact_id=contact_id)
    return [convert_db_call_to_schema(c) for c in calls]
