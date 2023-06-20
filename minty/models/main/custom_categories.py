from sqlalchemy.dialects.postgresql import *

from minty.extensions import db


class CustomCategory(db.Model):
    __tablename__ = "custom_categories"

    custom_category_id = db.Column(INTEGER, primary_key=True)
    custom_category_name = db.Column(VARCHAR(100), unique=True, nullable=False)

    transactions = db.relationship(
        "Transaction",
        backref="custom_category",
        lazy="dynamic",
    )
