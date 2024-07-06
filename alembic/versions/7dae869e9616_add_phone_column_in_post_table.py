"""add phone column in post table

Revision ID: 7dae869e9616
Revises: 20a3f24c8e48
Create Date: 2024-07-05 18:25:21.293192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dae869e9616'
down_revision: Union[str, None] = '20a3f24c8e48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('phone', sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "phone")
    
