"""
CRUD operations for Contacts
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from sqlalchemy.orm import selectinload
from app.crud.base import CRUDBase
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


class CRUDContact(CRUDBase[Contact]):
    """CRUD operations for Contact"""
    
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[Contact]:
        """Get contact by email"""
        result = await db.execute(
            select(Contact).where(Contact.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_phone(self, db: AsyncSession, *, phone: str) -> Optional[Contact]:
        """Get contact by phone"""
        result = await db.execute(
            select(Contact).where(Contact.phone == phone)
        )
        return result.scalar_one_or_none()
    
    async def search(
        self,
        db: AsyncSession,
        *,
        search: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Contact]:
        """Search contacts by name, email, phone, or company"""
        search_pattern = f"%{search}%"
        result = await db.execute(
            select(Contact)
            .where(
                or_(
                    Contact.name.ilike(search_pattern),
                    Contact.email.ilike(search_pattern),
                    Contact.phone.ilike(search_pattern),
                    Contact.company.ilike(search_pattern)
                )
            )
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_status(
        self,
        db: AsyncSession,
        *,
        status: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Contact]:
        """Get contacts by status"""
        result = await db.execute(
            select(Contact)
            .where(Contact.status == status)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_with_calls(self, db: AsyncSession, *, id: str) -> Optional[Contact]:
        """Get contact with related calls"""
        result = await db.execute(
            select(Contact)
            .options(selectinload(Contact.calls))
            .where(Contact.id == id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, db: AsyncSession, *, obj_in: ContactCreate) -> Contact:
        """Create a new contact"""
        obj_data = obj_in.model_dump()
        db_obj = Contact(**obj_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: Contact,
        obj_in: ContactUpdate
    ) -> Contact:
        """Update a contact"""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


contact = CRUDContact(Contact)

