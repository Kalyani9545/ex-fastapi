"""auto-vote

Revision ID: 95e708596a08
Revises: d5a84fbfca66
Create Date: 2023-04-20 18:21:03.118939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95e708596a08'
down_revision = 'd5a84fbfca66'
branch_labels = None
depends_on = None


def upgrade() -> None:
    
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table('voting')
    pass
    # ### end Alembic commands ###
