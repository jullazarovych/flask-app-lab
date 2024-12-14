"""Set default value for image_file to profile_default.jpg

Revision ID: 0c636cc64c7c
Revises: 6faa1afd6a60
Create Date: 2024-12-14 16:16:34.459857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c636cc64c7c'
down_revision = '6faa1afd6a60'
branch_labels = None
depends_on = None


# Оновіть поле image_file для всіх існуючих записів
def upgrade():
    op.execute("UPDATE users SET image_file = 'profile_default.jpg' WHERE image_file IS NULL OR image_file = ''")

def downgrade():
    op.execute("UPDATE users SET image_file = NULL WHERE image_file = 'profile_default.jpg'")