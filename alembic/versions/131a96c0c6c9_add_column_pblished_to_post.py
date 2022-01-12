"""Add column pblished to post

Revision ID: 131a96c0c6c9
Revises: efcd57e72b7b
Create Date: 2022-01-12 12:20:25.318128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '131a96c0c6c9'
down_revision = 'efcd57e72b7b'
branch_labels = None
depends_on = None


def upgrade():    
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False )),
    pass


def downgrade():
    op.drop_column('posts', 'published')
    pass
