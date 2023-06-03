from sqlalchemy.dialects.postgresql import *

from minty.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    category_id = db.Column(INTEGER, primary_key=True)  # ex. 13515895_21
    category_name = db.Column(VARCHAR(100))
    category_parent_id = db.Column(INTEGER)  # ex. 13515895_0
    category_parent_name = db.Column(VARCHAR(100))
