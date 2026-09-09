"""add_mode_to_research_jobs

Revision ID: 9a1b2c3d4e5f
Revises: 8725af5114d5
Create Date: 2026-09-10 01:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a1b2c3d4e5f'
down_revision: Union[str, None] = '8725af5114d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('research_jobs', sa.Column('mode', sa.String(), nullable=True, server_default='research'))


def downgrade() -> None:
    op.drop_column('research_jobs', 'mode')
