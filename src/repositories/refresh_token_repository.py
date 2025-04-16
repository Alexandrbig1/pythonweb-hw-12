import logging
from datetime import datetime


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import RefreshToken
from src.repositories.base import BaseRepository


logger = logging.getLogger("uvicorn.error")


class RefreshTokenRepository(BaseRepository):
    """
    Repository class for managing refresh tokens in the database.

    This class handles all database operations related to refresh tokens,
    including creating, retrieving, and revoking tokens.

    Attributes:
        db (AsyncSession): The database session for performing async database operations.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            session (AsyncSession): An async SQLAlchemy session for database operations.
        """
        super().__init__(session, RefreshToken)

    async def get_by_token_hash(self, token_hash: str) -> RefreshToken | None:
        """
        Retrieve a refresh token by its hash.

        Args:
            token_hash (str): The hash of the refresh token.

        Returns:
            RefreshToken | None: The refresh token if found, None otherwise.
        """
        stmt = select(self.model).where(RefreshToken.token_hash == token_hash)
        token = await self.db.execute(stmt)
        return token.scalars().first()

    async def get_active_token(
        self, token_hash: str, current_time: datetime
    ) -> RefreshToken | None:
        """
        Retrieve an active refresh token by its hash.

        Args:
            token_hash (str): The hash of the refresh token.
            current_time (datetime): The current time to check token validity.

        Returns:
            RefreshToken | None: The active refresh token if found, None otherwise.
        """
        stmt = select(self.model).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.expired_at > current_time,
            RefreshToken.revoked_at.is_(None),
        )
        token = await self.db.execute(stmt)
        return token.scalars().first()

    async def save_token(
        self,
        user_id: int,
        token_hash: str,
        expired_at: datetime,
        ip_address: str,
        user_agent: str,
    ) -> RefreshToken:
        """
        Save a new refresh token to the database.

        Args:
            user_id (int): The ID of the user associated with the token.
            token_hash (str): The hash of the refresh token.
            expired_at (datetime): The expiration time of the token.
            ip_address (str): The IP address of the user.
            user_agent (str): The user agent of the user's device.

        Returns:
            RefreshToken: The newly created refresh token.
        """
        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expired_at=expired_at,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return await self.create(refresh_token)

    async def revoke_token(self, refresh_token: RefreshToken) -> None:
        """
        Revoke a refresh token by setting its revoked timestamp.

        Args:
            refresh_token (RefreshToken): The refresh token to revoke.
        """
        refresh_token.revoked_at = datetime.now()
        await self.db.commit()