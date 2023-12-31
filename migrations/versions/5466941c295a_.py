"""empty message

Revision ID: 5466941c295a
Revises: f07803ec105b
Create Date: 2023-09-28 14:37:37.852415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5466941c295a'
down_revision = 'f07803ec105b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('alert', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_created', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('alert', schema=None) as batch_op:
        batch_op.drop_column('date_created')

    # ### end Alembic commands ###
