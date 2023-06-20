from sqlalchemy.dialects.postgresql import *
from sqlalchemy.sql import func

from minty.extensions import db


class AccuracyHistory(db.Model):
    __tablename__ = "classifier_history"

    classifier_history_id = db.Column(INTEGER, primary_key=True)
    classifier_id = db.Column(
        INTEGER,
        db.ForeignKey("classifiers.classifier_id"),
        index=True,
    )
    transaction_id = db.Column(BIGINT, db.ForeignKey("transactions.transaction_id"))
    category_id = db.Column(INTEGER)
    predicted_category_id = db.Column(INTEGER)
    accurate = db.Column(SMALLINT)
    created_on = db.Column(TIMESTAMP(timezone=True), server_default=func.now())

    custom_index = db.Index(
        "ix_classifier_history", classifier_id, postgresql_include=["accurate"]
    )
