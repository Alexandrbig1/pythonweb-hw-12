from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.contacts_book import ContactBookRepository
from src.schemas.contact_book import ContactBookSchema, ContactBookUpdateSchema , ContactBookResponse


class ContactBookService:
    def __init__(self, db: AsyncSession):
        self.todo_repository = ContactBookRepository(db)

    async def create_contact(self, body: ContactBookSchema):
        return await self.todo_repository.create_contact(body)

    async def get_contacts(self, limit: int, offset: int):
        return await self.todo_repository.get_contact(limit, offset)

    async def get_contact(self, contact_id: int):
        return await self.todo_repository.get_contact_by_id(contact_id)

    async def update_contact(self, contact_id: int, body: ContactBookUpdateSchema):
        return await self.todo_repository.update_contact(contact_id, body)


    async def remove_contact(self, contact_id: int):
        return await self.todo_repository.remove_contact(contact_id)