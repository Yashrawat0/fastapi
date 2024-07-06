"""create posts table

Revision ID: d7e5c490d441
Revises: 
Create Date: 2024-07-05 13:04:09.855378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7e5c490d441'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("post", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False))
    pass

def downgrade() -> None:
    op.drop_table("post")
    pass
