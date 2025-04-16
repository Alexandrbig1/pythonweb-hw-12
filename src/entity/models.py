from datetime import datetime
from enum import Enum
from sqlalchemy import (
    String,
    DateTime,
    func,
    ForeignKey,
    Text,
    Boolean,
    Enum as SqlEnum,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped, mapped_column

from src.conf import constants


class UserRole(str, Enum):

    USER = "USER"
    ADMIN = "ADMIN"


class Base(DeclarativeBase):
    pass


class Contact_Book(Base):
    __tablename__ = "Contact_Book"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(constants.USER_NAME_MAX_LENGTH), nullable=False
    )
    surname: Mapped[str] = mapped_column(
        String(constants.USER_SURNAME_MAX_LENGTH), nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(constants.USER_EMAIL_MAX_LENGTH), nullable=False
    )
    phone: Mapped[str] = mapped_column(
        String(constants.PHONE_NUMBER_MAX_LENGTH), nullable=False
    )
    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", backref="contacts", lazy="joined")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hash_password: Mapped[str] = mapped_column(nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user"
    )
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole), default=UserRole.USER, nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "hash_password": self.hash_password,
            "avatar": self.avatar,
            "confirmed": self.confirmed,
            "role": self.role.value,

        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls()
        user.id = data["id"]
        user.username = data["username"]
        user.email = data["email"]
        user.hash_password = data["hash_password"]
        user.avatar = data["avatar"]
        user.confirmed = data["confirmed"]
        user.role = UserRole(data["role"])
        return user


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    token_hash: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )
    expired_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[str] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")