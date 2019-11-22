"""empty message

Revision ID: 2e933c1015b2
Revises: 1b17967378b0
Create Date: 2019-11-22 03:48:38.892525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e933c1015b2'
down_revision = '1b17967378b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('process_group_withDSPGPGC', sa.Column('description', sa.String(length=140), nullable=True))
    op.create_unique_constraint(None, 'process_group_withDSPGPGC', ['description'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'process_group_withDSPGPGC', type_='unique')
    op.drop_column('process_group_withDSPGPGC', 'description')
    # ### end Alembic commands ###
