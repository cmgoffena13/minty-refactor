from sqlalchemy.dialects.postgresql import *

from minty.extensions import db


class AccountType(db.Model):
    __tablename__ = "account_types"

    account_type_id = db.Column(INTEGER, primary_key=True)  # ex. 2
    account_type_name = db.Column(VARCHAR(100), nullable=False)  # ex. BankAccount
