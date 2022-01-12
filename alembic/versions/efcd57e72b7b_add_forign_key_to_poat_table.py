"""add forign key to poat table

Revision ID: efcd57e72b7b
Revises: f888446399a4
Create Date: 2022-01-12 12:07:26.844250

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import Column


# revision identifiers, used by Alembic.
revision = 'efcd57e72b7b'
down_revision = 'f888446399a4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table="posts", referent_table="users", 
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_user_fk', table_name="posts" )
    op.drop_column('posts', 'owner_id')
    pass
