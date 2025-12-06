"""
Contact database model
"""
from sqlalchemy import Column, String, Integer, Enum as SQLEnum, Date
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel


class ContactStatus(str, enum.Enum):
    """Contact status enum"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    LEAD = "lead"


class Contact(BaseModel):
    """Contact model"""
    __tablename__ = "contacts"
    
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(50), nullable=False, index=True)
    company = Column(String(255), nullable=True, index=True)
    status = Column(SQLEnum(ContactStatus), default=ContactStatus.LEAD, nullable=False, index=True)
    total_calls = Column(Integer, default=0, nullable=False)
    last_contact = Column(Date, nullable=True)
    
    # Relationships
    calls = relationship("Call", back_populates="contact", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Contact(id={self.id}, name={self.name}, email={self.email})>"

