"""Create users table

Revision ID: 20b72c84164d
Revises: 9c7182748d5c
Create Date: 2025-01-08 01:05:35.255391

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid


# revision identifiers, used by Alembic.
revision: str = '20b72c84164d'
down_revision: Union[str, None] = '9c7182748d5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the 'users' table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('email', sa.String(), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
    )


def downgrade():
    # Drop the 'users' table
    op.drop_table('users')
