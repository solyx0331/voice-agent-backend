"""
Contact endpoints
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from app.schemas.contact import Contact, ContactCreate, ContactUpdate, ContactFilter
from app.schemas.call import Call
from app.core.database import contacts_db, calls_db, init_sample_data

router = APIRouter()


@router.get("", response_model=List[Contact])
async def get_contacts(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    """Get contacts with optional filtering"""
    # TODO: Replace with database query
    init_sample_data()
    
    filtered_contacts = contacts_db.copy()
    
    if search:
        search_lower = search.lower()
        filtered_contacts = [
            c for c in filtered_contacts
            if search_lower in c.name.lower()
            or search_lower in c.email.lower()
            or search_lower in c.company.lower()
            or search_lower in c.phone
        ]
    
    if status:
        filtered_contacts = [c for c in filtered_contacts if c.status == status]
    
    return filtered_contacts


@router.get("/{contact_id}", response_model=Contact)
async def get_contact(contact_id: str):
    """Get a specific contact by ID"""
    contact = next((c for c in contacts_db if c.id == contact_id), None)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found"
        )
    return contact


@router.post("", response_model=Contact, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate):
    """Create a new contact"""
    # TODO: Replace with database insert
    new_contact = Contact(
        id=str(len(contacts_db) + 1),
        total_calls=0,
        last_contact="",
        **contact.model_dump()
    )
    contacts_db.append(new_contact)
    return new_contact


@router.put("/{contact_id}", response_model=Contact)
async def update_contact(contact_id: str, contact_update: ContactUpdate):
    """Update a contact"""
    contact = next((c for c in contacts_db if c.id == contact_id), None)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found"
        )
    
    update_data = contact_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contact, field, value)
    
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: str):
    """Delete a contact"""
    from app.core.database import contacts_db
    contact = next((c for c in contacts_db if c.id == contact_id), None)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found"
        )
    
    contacts_db.remove(contact)
    return None


@router.get("/{contact_id}/calls", response_model=List[Call])
async def get_contact_calls(contact_id: str):
    """Get calls for a specific contact"""
    contact = next((c for c in contacts_db if c.id == contact_id), None)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found"
        )
    
    # Filter calls by contact name or phone
    calls = [
        c for c in calls_db
        if c.contact == contact.name or c.phone == contact.phone
    ]
    
    return calls

