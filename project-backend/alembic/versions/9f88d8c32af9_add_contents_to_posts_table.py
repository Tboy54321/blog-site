"""add contents to posts table

Revision ID: 9f88d8c32af9
Revises: 0efd2d702a21
Create Date: 2024-08-17 20:35:21.218228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f88d8c32af9'
down_revision: Union[str, None] = '0efd2d702a21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('contents', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "contents")
    pass
