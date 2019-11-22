"""empty message

Revision ID: 425a4dc5266b
Revises: 9754932edbb8
Create Date: 2019-11-21 21:47:52.787964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '425a4dc5266b'
down_revision = '9754932edbb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('participants_actors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('process_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('lastname', sa.String(length=140), nullable=True),
    sa.Column('role', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['process_id'], ['process_group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('participants_actors')
    # ### end Alembic commands ###
