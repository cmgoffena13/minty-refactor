from sqlalchemy.dialects.postgresql import *

from minty.extensions import db


class Merchant(db.Model):
    __tablename__ = "merchants"

    merchant_id = db.Column(BIGINT, primary_key=True)
    merchant_name = db.Column(VARCHAR(100))
    merchant_pattern = db.Column(VARCHAR)
