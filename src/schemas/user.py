from pydantic import BaseModel, Field, ConfigDict, EmailStr

from src.entity.models import UserRole


class UserBase(BaseModel):
    username: str = Field(min_length=2, max_length=50, description="Username")
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=12, description="Password")


class UserResponse(UserBase):
    id: int
    avatar: str | None
    role: UserRole
    model_config = ConfigDict(from_attributes=True)


class UserUpdateAvatar(BaseModel):
    avatar: str = Field(..., description="Avatar URL")


class RequestPasswordReset(BaseModel):
    email: EmailStr = Field(..., description="Email address for password reset")


class ResetPassword(BaseModel):
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(
        ...,
        min_length=6,
        max_length=12,
        description="New password"
    )