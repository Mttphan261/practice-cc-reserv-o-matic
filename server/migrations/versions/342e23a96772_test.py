"""test

Revision ID: 342e23a96772
Revises: 
Create Date: 2023-06-18 17:17:20.092177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '342e23a96772'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_customers'))
    )
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('max_party_size', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_locations'))
    )
    op.create_table('reservations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('party_name', sa.String(), nullable=True),
    sa.Column('party_size', sa.Integer(), nullable=True),
    sa.Column('reservation_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_reservations'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservations')
    op.drop_table('locations')
    op.drop_table('customers')
    # ### end Alembic commands ###
