from minty.extensions import db
from sqlalchemy import text

def truncate_tables():
    stmt = text(
    """
    TRUNCATE TABLE public.transactions CASCADE
    """
    )
    db.session.execute(stmt)
    db.session.commit()