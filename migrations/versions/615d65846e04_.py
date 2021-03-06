"""empty message

Revision ID: 615d65846e04
Revises: 
Create Date: 2019-12-01 18:42:30.535969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '615d65846e04'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('DPGPAS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('DSPGPGC',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('process_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participants_actors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('process_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('lastname', sa.String(length=140), nullable=True),
    sa.Column('role', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['process_id'], ['process_group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('process_group_with_dpgpa_s2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.Column('process_id', sa.Integer(), nullable=True),
    sa.Column('dpgpas_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dpgpas_id'], ['DPGPAS.id'], ),
    sa.ForeignKeyConstraint(['process_id'], ['process_group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('process_group_with_dspgpg_c2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.Column('process_id', sa.Integer(), nullable=True),
    sa.Column('dspgpgc_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dspgpgc_id'], ['DSPGPGC.id'], ),
    sa.ForeignKeyConstraint(['process_id'], ['process_group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tec',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('process_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.ForeignKeyConstraint(['process_id'], ['process_group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tool',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('process_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.ForeignKeyConstraint(['process_id'], ['process_group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('rank', sa.String(length=64), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_table('user')
    op.drop_table('tool')
    op.drop_table('tec')
    op.drop_table('process_group_with_dspgpg_c2')
    op.drop_table('process_group_with_dpgpa_s2')
    op.drop_table('participants_actors')
    op.drop_table('project')
    op.drop_table('process_group')
    op.drop_table('DSPGPGC')
    op.drop_table('DPGPAS')
    # ### end Alembic commands ###
