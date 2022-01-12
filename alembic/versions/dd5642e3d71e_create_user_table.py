"""create user table

Revision ID: dd5642e3d71e
Revises: 6c53cca917c3
Create Date: 2022-01-11 15:25:06.492737

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import UniqueConstraint


# revision identifiers, used by Alembic.
revision = 'dd5642e3d71e'
down_revision = '6c53cca917c3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    'user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    pass
