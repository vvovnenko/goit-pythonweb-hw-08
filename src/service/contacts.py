from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.repository.contacts import ContactsRepository
from src.schemas.contacts import ContactModel


class ContactService:
    def __init__(self, db_session: AsyncSession):
        self.contact_repo = ContactsRepository(db_session)

    async def create_contact(self, contact_data: ContactModel) -> Contact:
        return await self.contact_repo.create_contact(contact_data)

    async def read_contacts(
        self,
        firstname: Optional[str] = None,
        lastname: Optional[str] = None,
        email: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[Contact]:
        return await self.contact_repo.read_contacts(
            firstname, lastname, email, skip, limit
        )

    async def read_contact(self, contact_id: int) -> Optional[Contact]:
        return await self.contact_repo.read_contact(contact_id)
