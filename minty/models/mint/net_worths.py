from sqlalchemy.dialects.postgresql import *

from minty.extensions import db


class NetWorth(db.Model):
    __tablename__ = "net_worth_by_day"

    net_worth_date = db.Column(DATE, primary_key=True)
    assets_amount = db.Column(NUMERIC(19, 4))
    debts_amount = db.Column(NUMERIC(19, 4))
    net_amount = db.Column(NUMERIC(19, 4))
