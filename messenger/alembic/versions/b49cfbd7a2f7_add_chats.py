"""Add chats

Revision ID: b49cfbd7a2f7
Revises: 1b91225ee1f3
Create Date: 2022-05-04 19:08:50.000536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b49cfbd7a2f7'
down_revision = '1b91225ee1f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(40, collation='utf8_general_ci'), nullable=True),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('type', sa.String(60, collation='utf8_general_ci'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chats_id'), 'chats', ['id'], unique=False)
    op.create_table('users_chats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_chats_id'), 'users_chats', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_chats_id'), table_name='users_chats')
    op.drop_table('users_chats')
    op.drop_index(op.f('ix_chats_id'), table_name='chats')
    op.drop_table('chats')
    # ### end Alembic commands ###
