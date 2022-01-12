"""create posts table

Revision ID: 71f12eff7ee9
Revises: 5c460f21cf07
Create Date: 2022-01-11 16:21:50.989702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71f12eff7ee9'
down_revision = '5c460f21cf07'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    'posts',
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.Column('content', sa.String()),    
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False ),
    # sa.PrimaryKeyConstraint('id')
    )
    pass

def downgrade():
    op.drop_table('posts')
    pass
