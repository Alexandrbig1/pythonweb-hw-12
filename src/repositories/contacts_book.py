import logging
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact_Book, User
from src.schemas.contact_book import ContactBookSchema, ContactBookUpdateSchema, ContactBookResponse

logger = logging.getLogger("uvicorn.error")


class ContactBookRepository:
    """Repository class for managing contact book operations in the database.

    This class handles all database operations related to contacts including creating,
    reading, updating, and deleting contact entries. It uses SQLAlchemy for database
    operations and implements user-specific contact management.

    Attributes:
        db (AsyncSession): The database session for performing async database operations.
    """

    def __init__(self, session: AsyncSession):
        """Initialize the repository with a database session.

        Args:
            session (AsyncSession): An async SQLAlchemy session for database operations.
        """
        self.db = session

    async def get_contact(self, limit: int, offset: int, user: User) -> Sequence[Contact_Book]:
        """Retrieve a paginated list of contacts for a specific user.

        Args:
            limit (int): Maximum number of contacts to return.
            offset (int): Number of contacts to skip for pagination.
            user (User): The user whose contacts to retrieve.

        Returns:
            Sequence[Contact_Book]: A list of contact book entries.
        """
        stmt = select(Contact_Book).filter_by(user_id = user.id).offset(offset).limit(limit)
        contact = await self.db.execute(stmt)
        return contact.scalars().all()

    async def get_contact_by_id(self, contact_id: int, user: User) -> Contact_Book | None:
        """Retrieve a specific contact by its ID for a given user.

        Args:
            contact_id (int): The ID of the contact to retrieve.
            user (User): The user who owns the contact.

        Returns:
            Contact_Book | None: The contact if found, None otherwise.
        """
        stmt = select(Contact_Book).filter_by(id=contact_id, user_id = user.id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactBookSchema, user: User) -> Contact_Book:
        """Create a new contact for a user.

        Args:
            body (ContactBookSchema): The contact data to create.
            user (User): The user who will own the contact.

        Returns:
            Contact_Book: The newly created contact.
        """
        contact = Contact_Book(**body.model_dump(), user=user)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int ,user: User) -> Contact_Book | None:
        """Remove a contact by its ID for a specific user.

        Args:
            contact_id (int): The ID of the contact to remove.
            user (User): The user who owns the contact.

        Returns:
            Contact_Book | None: The removed contact if found and deleted, None otherwise.
        """
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def update_contact(
            self, contact_id: int, body: ContactBookUpdateSchema,user: User
    ) -> Contact_Book:
        """Update an existing contact for a user.

        Args:
            contact_id (int): The ID of the contact to update.
            body (ContactBookUpdateSchema): The updated contact data.
            user (User): The user who owns the contact.

        Returns:
            Contact_Book: The updated contact if found, None otherwise.
        """
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            update_data = body.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(contact, key, value)

            await self.db.commit()
            await self.db.refresh(contact)

        return contact