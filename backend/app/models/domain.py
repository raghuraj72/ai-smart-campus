from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """
    Return the current UTC time as a timezone-aware datetime.
    """
    return datetime.now(timezone.utc)


class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    FACULTY = "FACULTY"
    STUDENT = "STUDENT"
    SECURITY = "SECURITY"


class PriorityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class User(SQLModel, table=True):
    """
    Single canonical user model for the entire application.

    All authentication, academic, complaint and future campus
    features should reference this model.
    """

    __tablename__ = "user"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )

    email: str = Field(
        unique=True,
        index=True,
        nullable=False,
        max_length=255,
    )

    hashed_password: str = Field(
        nullable=False,
        max_length=255,
    )

    full_name: str = Field(
        nullable=False,
        max_length=150,
    )

    role: UserRole = Field(
        default=UserRole.STUDENT,
        nullable=False,
    )

    is_active: bool = Field(
        default=True,
        nullable=False,
    )

    # University/student/faculty identifier
    uid: Optional[str] = Field(
        default=None,
        unique=True,
        index=True,
        max_length=100,
    )

    # Example: CU-UP / CSE / AIML
    university_code: Optional[str] = Field(
        default=None,
        index=True,
        max_length=100,
    )

    department: Optional[str] = Field(
        default=None,
        index=True,
        max_length=150,
    )

    created_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
    )


class Complaint(SQLModel, table=True):
    """
    Campus complaint submitted by a student.
    """

    __tablename__ = "complaint"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )

    title: str = Field(
        nullable=False,
        max_length=200,
    )

    description: str = Field(
        nullable=False,
    )

    location: str = Field(
        nullable=False,
        max_length=200,
    )

    category: Optional[str] = Field(
        default="Unclassified",
        max_length=100,
    )

    priority: PriorityLevel = Field(
        default=PriorityLevel.MEDIUM,
        nullable=False,
    )

    department: Optional[str] = Field(
        default="General Maintenance",
        max_length=150,
    )

    status: str = Field(
        default="Assigned",
        max_length=50,
    )

    student_id: int = Field(
        foreign_key="user.id",
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
    )