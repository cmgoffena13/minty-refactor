from sqlalchemy import text

from minty.extensions import db
from minty.models import Transaction


def truncate_tables():
    stmt = text(
        """
    TRUNCATE TABLE public.transactions CASCADE;
    TRUNCATE TABLE public.accounts CASCADE;
    """
    )
    db.session.execute(stmt)
    db.session.commit()


def test_transactions_available(test_app):
    tran_count = len(Transaction.query.all())
    assert tran_count > 0
