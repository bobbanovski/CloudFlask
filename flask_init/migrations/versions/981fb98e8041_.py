"""empty message

Revision ID: 981fb98e8041
Revises: 122526dc42f0
Create Date: 2017-02-17 01:21:48.081976

"""

# revision identifiers, used by Alembic.
revision = '981fb98e8041'
down_revision = '122526dc42f0'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('author', 'is_author',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.add_column('post', sa.Column('image', sa.String(length=255), nullable=True))
    op.alter_column('post', 'live',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'live',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.drop_column('post', 'image')
    op.alter_column('author', 'is_author',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    # ### end Alembic commands ###
