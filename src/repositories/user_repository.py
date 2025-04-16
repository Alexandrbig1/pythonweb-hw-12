import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import User
from src.repositories.base import BaseRepository
from src.schemas.user import UserCreate

logger = logging.getLogger("uvicorn.error")


class UserRepository(BaseRepository):
    """
    Repository class for managing user-related database operations.

    This class handles all database operations related to users, including
    creating, retrieving, and updating user records.

    Attributes:
        db (AsyncSession): The database session for performing async database operations.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            session (AsyncSession): An async SQLAlchemy session for database operations.
        """
        super().__init__(session, User)

    async def get_by_username(self, username: str) -> User | None:
        """
        Retrieve a user by their username.

        Args:
            username (str): The username of the user.

        Returns:
            User | None: The user if found, None otherwise.
        """
        stmt = select(self.model).where(self.model.username == username)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            User | None: The user if found, None otherwise.
        """
        stmt = select(self.model).where(self.model.email == email)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def create_user(
        self, user_data: UserCreate, hashed_password: str, avatar: str
    ) -> User:
        """
        Create a new user in the database.

        Args:
            user_data (UserCreate): The data for the new user.
            hashed_password (str): The hashed password for the user.
            avatar (str): The avatar URL for the user.

        Returns:
            User: The newly created user.
        """
        user = User(
            **user_data.model_dump(exclude_unset=True, exclude={"password"}),
            hash_password=hashed_password,
            avatar=avatar
        )
        return await self.create(user)

    async def confirmed_email(self, email: str) -> None:
        """
        Mark a user's email as confirmed.

        Args:
            email (str): The email address of the user.
        """
        user = await self.get_user_by_email(email)
        user.confirmed = True
        await self.db.commit()

    async def update_avatar_url(self, email: str, url: str) -> User:
        """
        Update a user's avatar URL.

        Args:
            email (str): The email address of the user.
            url (str): The new avatar URL.

        Returns:
            User: The updated user.
        """
        user = await self.get_user_by_email(email)
        user.avatar = url
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_password(self, user: User, new_password_hash: str) -> User:
        """
        Update a user's password with a new hashed password.

        Args:
            user (User): The user whose password is being updated.
            new_password_hash (str): The new hashed password.

        Returns:
            User: The updated user.
        """
        user.hash_password = new_password_hash
        await self.db.commit()
        await self.db.refresh(user)
        return user