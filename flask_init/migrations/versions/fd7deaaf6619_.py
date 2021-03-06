"""empty message

Revision ID: fd7deaaf6619
Revises: 96a82d7243fa
Create Date: 2017-02-15 05:58:59.980114

"""

# revision identifiers, used by Alembic.
revision = 'fd7deaaf6619'
down_revision = '96a82d7243fa'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('author', 'is_author',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('author', 'password',
               existing_type=mysql.VARCHAR(length=80),
               type_=sa.String(length=60),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('author', 'password',
               existing_type=sa.String(length=60),
               type_=mysql.VARCHAR(length=80),
               existing_nullable=True)
    op.alter_column('author', 'is_author',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    # ### end Alembic commands ###
