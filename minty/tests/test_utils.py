from sqlalchemy import text

from minty.extensions import db


def truncate_tables():
    stmt = text(
        """
    TRUNCATE TABLE public.transactions CASCADE;
    TRUNCATE TABLE public.accounts CASCADE;
    """
    )
    db.session.execute(stmt)
    db.session.commit()
