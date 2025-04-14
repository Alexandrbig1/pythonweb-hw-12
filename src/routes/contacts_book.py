import logging

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.services.contacts_book import ContactBookService
from src.schemas.contact_book import (
    ContactBookResponse,
ContactBookUpdateSchema,
ContactBookSchema
)


router = APIRouter(prefix="/contacts", tags=["contacts"])
logger = logging.getLogger("uvicorn.error")


@router.get("/", response_model=list[ContactBookResponse])
async def get_contacts(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    contact_service = ContactBookService(db)
    return await contact_service.get_contacts(limit, offset)


@router.get(
    "/{contact_id}",
    response_model=ContactBookResponse,
)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactBookService(db)
    contact = await contact_service.get_contact(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post(
    "/",
    response_model=ContactBookResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(body: ContactBookSchema, db: AsyncSession = Depends(get_db)):
    contact_service= ContactBookService(db)
    return await contact_service.create_contact(body)


@router.put("/{contact_id}", response_model=ContactBookResponse)
async def update_contact(
    contact_id: int, body: ContactBookUpdateSchema, db: AsyncSession = Depends(get_db)
):
    contact_service = ContactBookService(db)
    todo = await contact_service.update_contact(contact_id, body)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return todo




@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactBookService(db)
    await contact_service.remove_contact(contact_id)
    return None