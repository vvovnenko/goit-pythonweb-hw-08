from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.repository.contacts import ContactsRepository
from src.schemas.contacts import ContactModel


class ContactService:
    def __init__(self, db_session: AsyncSession):
        self.contact_repo = ContactsRepository(db_session)

    async def create_contact(self, contact_data: ContactModel) -> Contact:
        return await self.contact_repo.create_contact(contact_data)
