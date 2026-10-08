"""Scratch Table

Revision ID: 308d0313fe59
Revises:
Create Date: 2026-10-08 00:57:28.320713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '308d0313fe59'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("scratch", sa.Column("id", sa.Integer, primary_key=True))
    pass


def downgrade() -> None:
    op.drop_table("scratch")
    pass
