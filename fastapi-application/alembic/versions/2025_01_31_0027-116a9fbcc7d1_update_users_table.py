"""update users table

Revision ID: 116a9fbcc7d1
Revises: 
Create Date: 2025-01-31 00:27:33.386792

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '116a9fbcc7d1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_email_username_key', 'users', type_='unique')
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.create_unique_constraint(op.f('uq_users_email'), 'users', ['email'])
    op.create_unique_constraint(op.f('uq_users_username'), 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_users_username'), 'users', type_='unique')
    op.drop_constraint(op.f('uq_users_email'), 'users', type_='unique')
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.create_unique_constraint('users_email_username_key', 'users', ['email', 'username'])
    # ### end Alembic commands ###
