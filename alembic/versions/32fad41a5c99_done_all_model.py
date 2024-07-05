"""done all model

Revision ID: 32fad41a5c99
Revises: 
Create Date: 2024-07-05 15:01:29.044881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32fad41a5c99'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('intern_division',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('division_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_account',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('ADMIN', 'USER', name='roles'), nullable=True),
    sa.Column('is_complete', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('intern_finished',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('intern_certification', sa.String(), nullable=True),
    sa.Column('division_id', sa.Integer(), nullable=True),
    sa.Column('user_account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['division_id'], ['intern_division.id'], ),
    sa.ForeignKeyConstraint(['user_account_id'], ['user_account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('intern_quota',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('quota', sa.Integer(), nullable=True),
    sa.Column('division_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['division_id'], ['intern_division.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('intern_registration',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('ACCEPTED', 'ON_PROCESS', 'REJECTED', name='intern_registration_status'), nullable=False),
    sa.Column('cv', sa.String(), nullable=True),
    sa.Column('cover_letter', sa.String(), nullable=True),
    sa.Column('student_card', sa.String(), nullable=True),
    sa.Column('photo', sa.String(), nullable=True),
    sa.Column('proposal', sa.String(), nullable=True),
    sa.Column('updated_with', sa.String(), nullable=True),
    sa.Column('division_id', sa.Integer(), nullable=True),
    sa.Column('user_account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['division_id'], ['intern_division.id'], ),
    sa.ForeignKeyConstraint(['user_account_id'], ['user_account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_profile',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('fullname', sa.String(), nullable=True),
    sa.Column('student_number', sa.String(), nullable=True),
    sa.Column('ipk', sa.Numeric(precision=3, scale=2, asdecimal=False), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('university', sa.String(), nullable=True),
    sa.Column('semester', sa.Integer(), nullable=True),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='gender_choices'), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('user_account_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_account_id'], ['user_account.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_account_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_profile')
    op.drop_table('intern_registration')
    op.drop_table('intern_quota')
    op.drop_table('intern_finished')
    op.drop_table('user_account')
    op.drop_table('intern_division')
    # ### end Alembic commands ###
