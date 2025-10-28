"""User schemas for API."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema."""

    username: str
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema."""

    password: str


class UserUpdate(BaseModel):
    """User update schema."""

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    """User response schema."""

    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token schema."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema."""

    username: Optional[str] = None
