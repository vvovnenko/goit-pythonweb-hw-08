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
