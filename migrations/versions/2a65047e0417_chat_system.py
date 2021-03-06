"""Chat System

Revision ID: 2a65047e0417
Revises: 5d15b26e8b10
Create Date: 2020-05-04 07:35:52.233121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a65047e0417'
down_revision = '5d15b26e8b10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user1', sa.Integer(), nullable=True),
    sa.Column('user2', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_chats'))
    )
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_chats_user1'), ['user1'], unique=False)
        batch_op.create_index(batch_op.f('ix_chats_user2'), ['user2'], unique=False)

    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('reciever_id', sa.Integer(), nullable=True),
    sa.Column('reciever_read', sa.Boolean(), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], name=op.f('fk_messages_chat_id_chats')),
    sa.ForeignKeyConstraint(['reciever_id'], ['user.id'], name=op.f('fk_messages_reciever_id_user')),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], name=op.f('fk_messages_sender_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_messages'))
    )
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_messages_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_index('ix_message_timestamp')

    op.drop_table('message')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('last_message_read_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_message_read_time', sa.DATETIME(), nullable=True))

    op.create_table('message',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('sender_id', sa.INTEGER(), nullable=True),
    sa.Column('recipient_id', sa.INTEGER(), nullable=True),
    sa.Column('body', sa.VARCHAR(length=140), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], name='fk_message_recipient_id_user'),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], name='fk_message_sender_id_user'),
    sa.PrimaryKeyConstraint('id', name='pk_message')
    )
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.create_index('ix_message_timestamp', ['timestamp'], unique=False)

    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_messages_timestamp'))

    op.drop_table('messages')
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_chats_user2'))
        batch_op.drop_index(batch_op.f('ix_chats_user1'))

    op.drop_table('chats')
    # ### end Alembic commands ###
