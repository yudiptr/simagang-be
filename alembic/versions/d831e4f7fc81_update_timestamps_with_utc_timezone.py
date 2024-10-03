"""Update timestamps with UTC timezone

Revision ID: d831e4f7fc81
Revises: 28ac33cd2740
Create Date: 2024-10-03 12:47:29.110552

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = 'd831e4f7fc81'
down_revision: Union[str, None] = '28ac33cd2740'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Modify 'created_at' and 'updated_at' in each relevant table
    op.alter_column('intern_division', 'created_at', server_default=func.timezone('UTC', func.now()))
    op.alter_column('intern_division', 'updated_at', server_default=func.timezone('UTC', func.now()), onupdate=func.timezone('UTC', func.now()))
    
    op.alter_column('user_account', 'created_at', server_default=func.timezone('UTC', func.now()))
    op.alter_column('user_account', 'updated_at', server_default=func.timezone('UTC', func.now()), onupdate=func.timezone('UTC', func.now()))
    
    op.alter_column('intern_finished', 'created_at', server_default=func.timezone('UTC', func.now()))
    
    op.alter_column('intern_quota', 'created_at', server_default=func.timezone('UTC', func.now()))
    op.alter_column('intern_quota', 'updated_at', server_default=func.timezone('UTC', func.now()), onupdate=func.timezone('UTC', func.now()))
    
    op.alter_column('intern_registration', 'created_at', server_default=func.timezone('UTC', func.now()))
    op.alter_column('intern_registration', 'updated_at', server_default=func.timezone('UTC', func.now()), onupdate=func.timezone('UTC', func.now()))
    
    op.alter_column('user_profile', 'created_at', server_default=func.timezone('UTC', func.now()))
    op.alter_column('user_profile', 'updated_at', server_default=func.timezone('UTC', func.now()), onupdate=func.timezone('UTC', func.now()))


def downgrade() -> None:
    # Revert the columns to their original state if needed
    op.alter_column('intern_division', 'created_at', server_default=None)
    op.alter_column('intern_division', 'updated_at', server_default=None, onupdate=None)
    
    op.alter_column('user_account', 'created_at', server_default=None)
    op.alter_column('user_account', 'updated_at', server_default=None, onupdate=None)
    
    op.alter_column('intern_finished', 'created_at', server_default=None)
    
    op.alter_column('intern_quota', 'created_at', server_default=None)
    op.alter_column('intern_quota', 'updated_at', server_default=None, onupdate=None)
    
    op.alter_column('intern_registration', 'created_at', server_default=None)
    op.alter_column('intern_registration', 'updated_at', server_default=None, onupdate=None)
    
    op.alter_column('user_profile', 'created_at', server_default=None)
    op.alter_column('user_profile', 'updated_at', server_default=None, onupdate=None)