"""Process Group Table Added

Revision ID: 724da492dbe8
Revises: 969ef26d604e
Create Date: 2019-11-21 06:30:59.928918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '724da492dbe8'
down_revision = '969ef26d604e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('process_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('description')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('process_group')
    # ### end Alembic commands ###