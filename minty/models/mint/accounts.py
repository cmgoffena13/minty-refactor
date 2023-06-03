from sqlalchemy.dialects.postgresql import *

from minty.extensions import db


class Account(db.Model):
    __tablename__ = "accounts"

    account_id = db.Column(BIGINT, primary_key=True)  # ex. 13515895_8394663
    account_name = db.Column(VARCHAR(100))
    status = db.Column(VARCHAR(100))
    closed = db.Column(BOOLEAN)
    current_balance = db.Column(NUMERIC(19, 4))
    currency_type = db.Column(VARCHAR(20))
    financial_institution_name = db.Column(VARCHAR(100))
    mint_last_updated_on = db.Column(TIMESTAMP(timezone=True))
    mint_created_on = db.Column(TIMESTAMP(timezone=True))
    account_type_id = db.Column(
        INTEGER, db.ForeignKey("account_types.account_type_id")
    )  # ex. 2
    is_operation_account = db.Column(BOOLEAN)

    transactions = db.relationship(
        "Transaction",
        backref="account",
        lazy="dynamic",
    )
