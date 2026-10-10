"""add user organization references

Revision ID: 867773dc2171
Revises: multi_university_001
Create Date: 2026-10-05
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "867773dc2171"
down_revision: Union[str, None] = "multi_university_001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------------------------------------------------------
    # USER -> UNIVERSITY
    # ---------------------------------------------------------
    op.add_column(
        "user",
        sa.Column(
            "university_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_user_university_id",
        "user",
        ["university_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_user_university_id",
        "user",
        "university",
        ["university_id"],
        ["id"],
    )

    # ---------------------------------------------------------
    # USER -> CAMPUS
    # ---------------------------------------------------------
    op.add_column(
        "user",
        sa.Column(
            "campus_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_user_campus_id",
        "user",
        ["campus_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_user_campus_id",
        "user",
        "campus",
        ["campus_id"],
        ["id"],
    )

    # ---------------------------------------------------------
    # USER -> DEPARTMENT
    # ---------------------------------------------------------
    op.add_column(
        "user",
        sa.Column(
            "department_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_user_department_id",
        "user",
        ["department_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_user_department_id",
        "user",
        "department",
        ["department_id"],
        ["id"],
    )


def downgrade() -> None:
    # ---------------------------------------------------------
    # Remove USER -> DEPARTMENT
    # ---------------------------------------------------------
    op.drop_constraint(
        "fk_user_department_id",
        "user",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_user_department_id",
        table_name="user",
    )

    op.drop_column(
        "user",
        "department_id",
    )

    # ---------------------------------------------------------
    # Remove USER -> CAMPUS
    # ---------------------------------------------------------
    op.drop_constraint(
        "fk_user_campus_id",
        "user",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_user_campus_id",
        table_name="user",
    )

    op.drop_column(
        "user",
        "campus_id",
    )

    # ---------------------------------------------------------
    # Remove USER -> UNIVERSITY
    # ---------------------------------------------------------
    op.drop_constraint(
        "fk_user_university_id",
        "user",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_user_university_id",
        table_name="user",
    )

    op.drop_column(
        "user",
        "university_id",
    )