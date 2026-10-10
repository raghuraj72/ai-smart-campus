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


class University(SQLModel, table=True):
    """
    Top-level organization in the Smart Campus platform.

    One Smart Campus platform can support multiple universities.
    """

    __tablename__ = "university"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )

    name: str = Field(
        nullable=False,
        max_length=200,
    )

    code: str = Field(
        unique=True,
        index=True,
        nullable=False,
        max_length=100,
    )

    country: Optional[str] = Field(
        default="India",
        max_length=100,
    )

    state: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    city: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    is_active: bool = Field(
        default=True,
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
    )


class Campus(SQLModel, table=True):
    """
    A physical or logical campus belonging to a university.
    """

    __tablename__ = "campus"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )

    university_id: int = Field(
        foreign_key="university.id",
        nullable=False,
        index=True,
    )

    name: str = Field(
        nullable=False,
        max_length=200,
    )

    code: str = Field(
        nullable=False,
        max_length=100,
    )

    city: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    is_active: bool = Field(
        default=True,
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
    )


class Department(SQLModel, table=True):
    """
    Academic or administrative department inside a campus.
    """

    __tablename__ = "department"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )

    campus_id: int = Field(
        foreign_key="campus.id",
        nullable=False,
        index=True,
    )

    name: str = Field(
        nullable=False,
        max_length=200,
    )

    code: str = Field(
        nullable=False,
        max_length=100,
    )

    is_active: bool = Field(
        default=True,
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
    )


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

    # Existing field retained for backward compatibility.
    # This will later be replaced gradually by university_id.
    university_code: Optional[str] = Field(
        default=None,
        index=True,
        max_length=100,
    )

    # Existing field retained for backward compatibility.
    # This will later be replaced gradually by department_id.
    department: Optional[str] = Field(
        default=None,
        index=True,
        max_length=150,
    )

    # ---------------------------------------------------------
    # MULTI-UNIVERSITY RELATIONAL REFERENCES
    # ---------------------------------------------------------

    # University to which this user belongs.
    university_id: Optional[int] = Field(
        default=None,
        foreign_key="university.id",
        index=True,
    )

    # Specific campus to which this user belongs.
    campus_id: Optional[int] = Field(
        default=None,
        foreign_key="campus.id",
        index=True,
    )

    # Academic/administrative department of this user.
    department_id: Optional[int] = Field(
        default=None,
        foreign_key="department.id",
        index=True,
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

    Existing fields are intentionally preserved during the
    multi-university migration.
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

    # ---------------------------------------------------------
    # STUDENT REFERENCE
    # ---------------------------------------------------------

    student_id: int = Field(
        foreign_key="user.id",
        nullable=False,
    )

    # ---------------------------------------------------------
    # MULTI-UNIVERSITY RELATIONAL REFERENCES
    # ---------------------------------------------------------

    # University that owns this complaint.
    university_id: Optional[int] = Field(
        default=None,
        foreign_key="university.id",
        index=True,
    )

    # Campus where this complaint belongs.
    campus_id: Optional[int] = Field(
        default=None,
        foreign_key="campus.id",
        index=True,
    )

    # Department responsible for this complaint.
    department_id: Optional[int] = Field(
        default=None,
        foreign_key="department.id",
        index=True,
    )

    created_at: datetime = Field(
        default_factory=utc_now,
        nullable=False,
    )