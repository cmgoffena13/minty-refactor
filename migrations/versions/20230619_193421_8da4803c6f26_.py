"""empty message

Revision ID: 8da4803c6f26
Revises: 3744d688bcd7
Create Date: 2023-06-19 19:34:21.594851

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8da4803c6f26"
down_revision = "3744d688bcd7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("custom_categories", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            batch_op.f("uq_custom_categories_custom_category_name"),
            ["custom_category_name"],
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("custom_categories", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("uq_custom_categories_custom_category_name"), type_="unique"
        )

    # ### end Alembic commands ###
