"""add date_created to post table

Revision ID: 6c53cca917c3
Revises: 89df9fe0ec33
Create Date: 2022-01-11 15:13:16.161543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c53cca917c3'
down_revision = '89df9fe0ec33'
branch_labels = None
depends_on = None


def upgrade():    
    op.add_column('post', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False )),
    pass


def downgrade():
    op.drop_column('post', 'created_at')
    pass
