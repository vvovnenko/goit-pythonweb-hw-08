from typing import List, Optional
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas.contacts import ContactModel


class ContactsRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def create_contact(self, body: ContactModel) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def read_contacts(
        self,
        firstname: Optional[str] = None,
        lastname: Optional[str] = None,
        email: Optional[str] = None,
        upcoming_birthday_days: Optional[int] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[Contact]:
        stmt = select(Contact).offset(skip).limit(limit)

        if firstname:
            stmt = stmt.where(Contact.firstname.match(firstname))
        if lastname:
            stmt = stmt.where(Contact.lastname.match(lastname))
        if email:
            stmt = stmt.where(Contact.email.match(email))

        if upcoming_birthday_days:
            stmt = stmt.where(
                Contact.birthday.between(
                    date.today(), date.today() + timedelta(days=upcoming_birthday_days)
                )
            )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def read_contact(self, contact_id: int) -> Optional[Contact]:
        stmt = select(Contact).filter_by(id=contact_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_contact(
        self, contact_id: int, body: ContactModel
    ) -> Optional[Contact]:
        contact = await self.read_contact(contact_id)
        if contact:
            for key, value in body.model_dump(exclude_unset=True).items():
                setattr(contact, key, value)
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def delete_contact(self, contact_id: int) -> Optional[Contact]:
        contact = await self.read_contact(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact
