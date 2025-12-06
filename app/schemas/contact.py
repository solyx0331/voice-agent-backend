"""
Contact schemas
"""
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field


class ContactBase(BaseModel):
    """Base contact model"""
    name: str
    email: EmailStr
    phone: str
    company: str
    status: Literal["active", "inactive", "lead"] = "lead"


class Contact(ContactBase):
    """Contact model with ID and metadata"""
    id: str
    total_calls: int = 0
    last_contact: str

    class Config:
        from_attributes = True


class ContactCreate(ContactBase):
    """Create contact request"""
    pass


class ContactUpdate(BaseModel):
    """Update contact request"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: Optional[Literal["active", "inactive", "lead"]] = None


class ContactFilter(BaseModel):
    """Contact filter parameters"""
    search: Optional[str] = None
    status: Optional[Literal["active", "inactive", "lead"]] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)

