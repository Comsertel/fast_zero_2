"""empty message

Revision ID: 7e6e31591b35
Revises: 27bccb43e07e
Create Date: 2024-11-29 10:38:43.047401

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e6e31591b35'
down_revision: Union[str, None] = '27bccb43e07e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
