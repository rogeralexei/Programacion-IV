"""Initial Migration

Revision ID: 9c9fd22434bf
Revises: 
Create Date: 2020-06-14 21:18:53.441890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c9fd22434bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('slangs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('palabra', sa.String(), nullable=True),
    sa.Column('definicion', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('slangs')
    # ### end Alembic commands ###
