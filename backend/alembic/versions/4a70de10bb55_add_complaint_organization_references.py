"""add complaint organization references

Revision ID: 4a70de10bb55
Revises: 867773dc2171
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4a70de10bb55"
down_revision: Union[str, Sequence[str], None] = "867773dc2171"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add multi-university organization references to complaints."""

    op.add_column(
        "complaint",
        sa.Column("university_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "complaint",
        sa.Column("campus_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "complaint",
        sa.Column("department_id", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        "fk_complaint_university_id",
        "complaint",
        "university",
        ["university_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_complaint_campus_id",
        "complaint",
        "campus",
        ["campus_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_complaint_department_id",
        "complaint",
        "department",
        ["department_id"],
        ["id"],
    )

    op.create_index(
        "ix_complaint_university_id",
        "complaint",
        ["university_id"],
    )

    op.create_index(
        "ix_complaint_campus_id",
        "complaint",
        ["campus_id"],
    )

    op.create_index(
        "ix_complaint_department_id",
        "complaint",
        ["department_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    # This migration was originally recorded as applied
    # without actually changing the database. The database
    # currently has none of these objects, so downgrade is
    # intentionally empty.
    pass
