"""empty message

Revision ID: 4309ab6187f6
Revises: c0acf045478f
Create Date: 2023-05-20 19:47:59.128985

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4309ab6187f6"
down_revision = "c0acf045478f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("transactions", schema=None) as batch_op:
        batch_op.create_index(
            "ix_transactions_transaction_description_tsv",
            [sa.text("to_tsvector('english', transaction_description)")],
            unique=False,
            postgresql_using="GIN",
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("transactions", schema=None) as batch_op:
        batch_op.drop_index(
            "ix_transactions_transaction_description_tsv", postgresql_using="GIN"
        )

    # ### end Alembic commands ###
