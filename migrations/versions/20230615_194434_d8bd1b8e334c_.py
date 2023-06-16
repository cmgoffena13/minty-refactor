"""empty message

Revision ID: d8bd1b8e334c
Revises: 1df2307fda8e
Create Date: 2023-06-15 19:44:34.153523

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "d8bd1b8e334c"
down_revision = "1df2307fda8e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("classifiers", schema=None) as batch_op:
        batch_op.add_column(sa.Column("date_filter", sa.DATE(), nullable=True))
        batch_op.drop_column("vectorizer")
        batch_op.drop_column("classifier")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("classifiers", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "classifier", postgresql.BYTEA(), autoincrement=False, nullable=True
            )
        )
        batch_op.add_column(
            sa.Column(
                "vectorizer", postgresql.BYTEA(), autoincrement=False, nullable=True
            )
        )
        batch_op.drop_column("date_filter")

    # ### end Alembic commands ###
