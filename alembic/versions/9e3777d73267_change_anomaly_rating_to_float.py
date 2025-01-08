"""Change anomaly_rating to Float

Revision ID: 9e3777d73267
Revises: 20b72c84164d
Create Date: 2025-01-08 12:58:59.932414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9e3777d73267'
down_revision: Union[str, None] = '20b72c84164d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Change anomaly_rating column to Float
    op.alter_column(
        'Checked_transactions',
        'anomaly_rating',
        existing_type=sa.Integer(),
        type_=sa.Float(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # Revert anomaly_rating column to Integer
    op.alter_column(
        'Checked_transactions',
        'anomaly_rating',
        existing_type=sa.Float(),
        type_=sa.Integer(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
