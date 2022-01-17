"""create post tables

Revision ID: 89df9fe0ec33
Revises: 
Create Date: 2022-01-11 08:53:29.233273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89df9fe0ec33'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    'post',
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.Column('content', sa.String()),
    # sa.Column('date_created', sa.DateTime()),
    # sa.PrimaryKeyConstraint('id')
    )
    pass

def downgrade():
    op.drop_table('post')
    pass
