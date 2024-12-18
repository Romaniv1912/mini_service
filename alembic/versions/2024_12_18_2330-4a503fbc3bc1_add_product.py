"""add product

Revision ID: 4a503fbc3bc1
Revises:
Create Date: 2024-12-18 23:30:08.059133

"""

from typing import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4a503fbc3bc1'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'product',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='Primary key id'),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('external_id', sa.Integer(), nullable=True),
        sa.Column('created_time', sa.DateTime(timezone=True), nullable=False, comment='creation time'),
        sa.Column('updated_time', sa.DateTime(timezone=True), nullable=True, comment='update time'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_product')),
    )
    op.create_index(op.f('ix_product_id'), 'product', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_product_id'), table_name='product')
    op.drop_table('product')
    # ### end Alembic commands ###
