"""empty message

Revision ID: f27a4a9c50af
Revises: 
Create Date: 2020-04-16 18:43:20.549443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f27a4a9c50af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('isbn', sa.String(length=50), nullable=True),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.Column('author', sa.String(length=200), nullable=False),
    sa.Column('year_published', sa.String(length=4), nullable=True),
    sa.Column('date_read', sa.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('degrees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('institution', sa.String(length=200), nullable=False),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('year_completed', sa.String(length=4), nullable=False),
    sa.Column('location', sa.String(length=200), nullable=True),
    sa.Column('url', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('degrees')
    op.drop_table('books')
    # ### end Alembic commands ###
