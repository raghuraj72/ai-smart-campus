"""add multi university foundation

Revision ID: multi_university_001
Revises: d4acc91592fe
Create Date: 2026-10-05
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "multi_university_001"
down_revision: Union[str, None] = "d4acc91592fe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------------------------------------------------------
    # UNIVERSITY
    # ---------------------------------------------------------
    op.create_table(
        "university",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )

    op.create_index(
        "ix_university_code",
        "university",
        ["code"],
        unique=False,
    )

    # ---------------------------------------------------------
    # CAMPUS
    # ---------------------------------------------------------
    op.create_table(
        "campus",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("university_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["university_id"],
            ["university.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_campus_university_id",
        "campus",
        ["university_id"],
        unique=False,
    )

    # ---------------------------------------------------------
    # DEPARTMENT
    # ---------------------------------------------------------
    op.create_table(
        "department",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("campus_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["campus_id"],
            ["campus.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_department_campus_id",
        "department",
        ["campus_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_department_campus_id",
        table_name="department",
    )

    op.drop_table("department")

    op.drop_index(
        "ix_campus_university_id",
        table_name="campus",
    )

    op.drop_table("campus")

    op.drop_index(
        "ix_university_code",
        table_name="university",
    )

    op.drop_table("university")