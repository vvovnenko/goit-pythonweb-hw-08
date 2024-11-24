from typing import List, Optional

from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas.contacts import ContactModel, ContactResponseModel
from src.service.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post(
    "/",
    response_model=ContactResponseModel,
    status_code=status.HTTP_201_CREATED,
    summary="Create new contact",
)
async def create_contact(body: ContactModel, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    return await contact_service.create_contact(body)


@router.get("/", response_model=List[ContactResponseModel], summary="Read contacts")
async def read_contacts(
    firstname: Optional[str] = Query(default=None, max_length=50, min_length=2),
    lastname: str | None = Query(default=None, max_length=50, min_length=2),
    email: str | None = Query(default=None, max_length=150, min_length=5),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=5, le=100, ge=5),
    db: AsyncSession = Depends(get_db),
):
    contact_service = ContactService(db)
    contacts = await contact_service.read_contacts(
        firstname, lastname, email, skip, limit
    )
    return contacts


@router.get(
    "/{contact_id}", response_model=ContactResponseModel, summary="Read contact"
)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contact = await contact_service.read_contact(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found."
        )
    return contact
