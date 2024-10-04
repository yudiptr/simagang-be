"""add status intern deleted

Revision ID: 186c51c94a9e
Revises: d831e4f7fc81
Create Date: 2024-10-04 23:00:01.177924

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '186c51c94a9e'
down_revision: Union[str, None] = 'd831e4f7fc81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add the new value directly to the ENUM
    op.execute("ALTER TYPE intern_registration_status ADD VALUE 'DELETED'")

def downgrade():
    # Note: PostgreSQL doesn't support removing an individual enum value easily,
    # so if you need to revert, you would have to recreate the ENUM without the value.
    # This is a limitation in PostgreSQL.
    pass