"""recreate created at for post table

Revision ID: 5c460f21cf07
Revises: dd5642e3d71e
Create Date: 2022-01-11 15:50:52.080327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c460f21cf07'
down_revision = 'dd5642e3d71e'
branch_labels = None
depends_on = None


def upgrade():    
    op.add_column('post', sa.Column('date_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False )),
    pass


def downgrade():
    op.drop_column('post', 'created_at')
    pass

