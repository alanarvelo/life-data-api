"""empty message

Revision ID: 929a579ed1fc
Revises: 
Create Date: 2020-04-15 19:02:00.256526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '929a579ed1fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('isbn', sa.String(length=50), autoincrement=False, nullable=False),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.Column('author', sa.String(length=200), nullable=False),
    sa.Column('year_published', sa.DATE(), nullable=False),
    sa.Column('month_read', sa.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('isbn')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    # ### end Alembic commands ###