"""Add Checked_transactions table

Revision ID: 9c7182748d5c
Revises: b9c39b7c5a2b
Create Date: 2025-01-08 00:18:20.220281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9c7182748d5c'
down_revision: Union[str, None] = 'b9c39b7c5a2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Checked_transactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('transaction_hash', sa.String(length=80), nullable=False),
    sa.Column('anomaly_rating', sa.Integer(), nullable=False),
    sa.Column('anomaly', sa.Integer(), nullable=False),
    sa.Column('checked_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('transaction_hash')
    )
    
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Checked_transactions')
    # ### end Alembic commands ###
