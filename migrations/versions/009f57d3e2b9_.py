"""empty message

Revision ID: 009f57d3e2b9
Revises: 404df175b39b
Create Date: 2019-12-02 23:53:43.382346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '009f57d3e2b9'
down_revision = '404df175b39b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activityDSPGPGC',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('process_id', sa.Integer(), nullable=True),
    sa.Column('dspgpgc_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.ForeignKeyConstraint(['dspgpgc_id'], ['process_group_with_dspgpg_c2.id'], ),
    sa.ForeignKeyConstraint(['process_id'], ['process_group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('activityDSPGPGC')
    # ### end Alembic commands ###
