"""empty message

Revision ID: b9d1b111201e
Revises: 136b6de44d2d
Create Date: 2019-11-21 14:57:38.608636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9d1b111201e'
down_revision = '136b6de44d2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tec', sa.Column('process_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tec', 'process_group', ['process_id'], ['id'])
    op.add_column('tool', sa.Column('process_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tool', 'process_group', ['process_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tool', type_='foreignkey')
    op.drop_column('tool', 'process_id')
    op.drop_constraint(None, 'tec', type_='foreignkey')
    op.drop_column('tec', 'process_id')
    # ### end Alembic commands ###
