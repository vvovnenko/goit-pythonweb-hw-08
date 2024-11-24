from fastapi import APIRouter, Depends, status, Query
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
