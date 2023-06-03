from sqlalchemy import Index, text
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.sql import func

from minty.extensions import db
from minty.models import CustomCategory


class Transaction(db.Model):
    __tablename__ = "transactions"

    transaction_id = db.Column(BIGINT, primary_key=True)  # ex. 13515895_679755723_0
    transaction_type_id = db.Column(
        INTEGER, db.ForeignKey("transaction_types.transaction_type_id")
    )  # Grab from transaction_types
    account_id = db.Column(
        BIGINT, db.ForeignKey("accounts.account_id")
    )  # Grab from Accounts
    transaction_date = db.Column(DATE, index=True)  # ex. 2015-07-16
    transaction_description = db.Column(VARCHAR(250))
    transaction_amount = db.Column(NUMERIC(19, 4))
    is_debit = db.Column(BOOLEAN)  # Created
    is_expense = db.Column(BOOLEAN)
    merchant_id = db.Column(BIGINT, db.ForeignKey("merchants.merchant_id"))
    category_id = db.Column(INTEGER, db.ForeignKey("categories.category_id"))
    custom_category_id = db.Column(
        INTEGER,
        db.ForeignKey("custom_categories.custom_category_id"),
        nullable=False,
        default=-1,
    )

    ix_transaction_description_gin = Index(
        "ix_transactions_transaction_description_tsv",
        func.to_tsvector(text("'english'"), transaction_description),
        postgresql_using="GIN",
    )

    __table_args__ = (ix_transaction_description_gin,)

    def set_custom_category(self, custom_category_name):
        custom_category = CustomCategory.query.filter_by(
            custom_category_name=custom_category_name
        ).first()
        self.custom_category_id = custom_category.custom_category_id
        db.session.commit()
