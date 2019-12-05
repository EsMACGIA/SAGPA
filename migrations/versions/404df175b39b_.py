"""empty message

Revision ID: 404df175b39b
Revises: 615d65846e04
Create Date: 2019-12-02 23:31:44.787237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '404df175b39b'
down_revision = '615d65846e04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activityDPGPAS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('process_id', sa.Integer(), nullable=True),
    sa.Column('dpgpas_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.ForeignKeyConstraint(['dpgpas_id'], ['process_group_with_dpgpa_s2.id'], ),
    sa.ForeignKeyConstraint(['process_id'], ['process_group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('activityDPGPAS')
    # ### end Alembic commands ###