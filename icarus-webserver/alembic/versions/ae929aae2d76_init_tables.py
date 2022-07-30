"""create init tables

Revision ID: ae929aae2d76
Revises: 
Create Date: 2022-07-26 09:46:17.937505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae929aae2d76'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'images',
        sa.Column('uuid', sa.String(100), primary_key=True),
        sa.Column('file_name', sa.String(100), nullable=True),
        sa.Column('file_path', sa.String(100), nullable=True),
        sa.Column('file_extension', sa.String(20), nullable=True),
        sa.Column('stored', sa.Boolean, nullable=True),
        sa.Column('time_stamp', sa.String(50)),
    )

    op.create_table(
        'image_meta_data',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('image_uuid', sa.String(100), nullable=False),
        sa.Column('label', sa.String(50), nullable=True),
        sa.Column('bx', sa.Integer, nullable=True),
        sa.Column('by', sa.Integer, nullable=True),
        sa.Column('w', sa.Integer, nullable=True),
        sa.Column('h', sa.Integer, nullable=True),
        sa.ForeignKeyConstraint(('image_uuid',), ['images.uuid'], ),
    )

def downgrade():
    pass
