"""add movie embeddings

Revision ID: ef3f09a4ac39
Revises: 8ab9d739a769
Create Date: 2026-10-02 23:26:56.722212

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = "ef3f09a4ac39"
down_revision: Union[str, Sequence[str], None] = "8ab9d739a769"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "movies",
        sa.Column(
            "embedding",
            Vector(384),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "movies",
        "embedding",
    )