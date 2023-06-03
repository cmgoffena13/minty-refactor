from sqlalchemy.dialects.postgresql import *

from minty.extensions import db


class TransactionType(db.Model):
    __tablename__ = "transaction_types"

    transaction_type_id = db.Column(INTEGER, primary_key=True)  # Auto-Generated
    transaction_type_name = db.Column(
        VARCHAR(100), nullable=False, index=True, unique=True
    )  # ex. CashAndCreditTransaction
