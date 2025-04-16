from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import User
from src.repositories.contacts_book import ContactBookRepository
from src.schemas.contact_book import ContactBookSchema, ContactBookUpdateSchema , ContactBookResponse


class ContactBookService:
    """
    Service class for managing contact book operations.

    This class provides methods for creating, retrieving, updating, and deleting
    contacts associated with a specific user.

    Attributes:
        todo_repository (ContactBookRepository): Repository for managing contact book operations.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the ContactBookService with a database session.

        Args:
            db (AsyncSession): An async SQLAlchemy session for database operations.
        """
        self.todo_repository = ContactBookRepository(db)

    async def create_contact(self, body: ContactBookSchema, user: User):
        """
        Create a new contact for the user.

        Args:
            body (ContactBookSchema): The data for the new contact.
            user (User): The user creating the contact.

        Returns:
            Contact_Book: The newly created contact.
        """
        return await self.todo_repository.create_contact(body, user)

    async def get_contacts(self, limit: int, offset: int, user: User):
        """
        Retrieve a list of contacts for the user.

        Args:
            limit (int): The maximum number of contacts to retrieve.
            offset (int): The number of contacts to skip.
            user (User): The user whose contacts are being retrieved.

        Returns:
            List[Contact_Book]: A list of contacts.
        """
        return await self.todo_repository.get_contact(limit, offset, user)

    async def get_contact(self, contact_id: int, user: User):
        """
        Retrieve a specific contact by its ID.

        Args:
            contact_id (int): The ID of the contact to retrieve.
            user (User): The user retrieving the contact.

        Returns:
            Contact_Book | None: The contact if found, None otherwise.
        """
        return await self.todo_repository.get_contact_by_id(contact_id, user)

    async def update_contact(self, contact_id: int, body: ContactBookUpdateSchema, user: User):
        """
        Update a specific contact's details.

        Args:
            contact_id (int): The ID of the contact to update.
            body (ContactBookUpdateSchema): The updated contact data.
            user (User): The user updating the contact.

        Returns:
            Contact_Book: The updated contact.
        """
        return await self.todo_repository.update_contact(contact_id, body, user)

    async def remove_contact(self, contact_id: int, user: User):
        """
        Remove a specific contact.

        Args:
            contact_id (int): The ID of the contact to remove.
            user (User): The user removing the contact.

        Returns:
            Contact_Book | None: The removed contact if found, None otherwise.
        """
        return await self.todo_repository.remove_contact(contact_id, user)