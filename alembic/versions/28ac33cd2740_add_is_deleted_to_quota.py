"""add is deleted to quota

Revision ID: 28ac33cd2740
Revises: 652cd6b7f18c
Create Date: 2024-08-02 23:37:33.559859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28ac33cd2740'
down_revision: Union[str, None] = '652cd6b7f18c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('intern_quota', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('intern_quota', 'is_deleted')
    # ### end Alembic commands ###
