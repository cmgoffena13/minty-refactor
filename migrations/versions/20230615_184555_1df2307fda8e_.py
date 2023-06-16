"""empty message

Revision ID: 1df2307fda8e
Revises: 2702574a5262
Create Date: 2023-06-15 18:45:55.547184

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1df2307fda8e"
down_revision = "2702574a5262"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "classifiers",
        sa.Column("classifier_id", sa.INTEGER(), nullable=False),
        sa.Column("classifier_name", sa.VARCHAR(length=100), nullable=True),
        sa.Column("classifier_model", sa.PickleType(), nullable=True),
        sa.Column("vectorizer", sa.PickleType(), nullable=True),
        sa.Column("classifier", sa.PickleType(), nullable=True),
        sa.Column("is_trained", sa.BOOLEAN(), nullable=True),
        sa.Column("accuracy", sa.NUMERIC(precision=20, scale=4), nullable=True),
        sa.PrimaryKeyConstraint("classifier_id", name=op.f("pk_classifiers")),
        sa.UniqueConstraint(
            "classifier_name", name=op.f("uq_classifiers_classifier_name")
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("classifiers")
    # ### end Alembic commands ###