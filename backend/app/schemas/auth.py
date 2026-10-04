from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.domain import UserRole


class UserCreate(BaseModel):
    """
    Public registration payload.

    New users are always registered as STUDENT.
    Admin/faculty/security accounts must be created through
    controlled administrative processes.
    """

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=72,
    )

    full_name: str = Field(
        min_length=2,
        max_length=150,
    )

    uid: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    university_code: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    department: Optional[str] = Field(
        default=None,
        max_length=150,
    )


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool

    uid: Optional[str] = None
    university_code: Optional[str] = None
    department: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


class LoginRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=1,
        max_length=72,
    )


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenResponse(Token):
    pass