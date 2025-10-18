"""add max_participants and current_participants to events

Revision ID: 4f757b17b635
Revises: 4e4ee8a19ce7
Create Date: 2025-10-18 17:53:43.970974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f757b17b635'
down_revision: Union[str, Sequence[str], None] = '4e4ee8a19ce7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('events', sa.Column('max_participants', sa.Integer(), nullable=False, default=10))
    op.add_column('events', sa.Column('current_participants', sa.Integer(), nullable=False, default=0))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('events', 'current_participants')
    op.drop_column('events', 'max_participants')
