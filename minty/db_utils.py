from sqlalchemy import text

from minty.config.settings import CustomCategoryEnum
from minty.extensions import db
from minty.models import CustomCategory


def populate_custom_category_table():
    enum_tuples = [(member.value, member.name) for member in CustomCategoryEnum]
    for value, name in enum_tuples:
        if not CustomCategory.query.filter(
            CustomCategory.custom_category_name == name
        ).first():
            custom_category = CustomCategory(
                custom_category_id=value, custom_category_name=name
            )
            db.session.add(custom_category)
    db.session.commit()


def populate_calendar_table():
    cmd = text("CALL create_calendar();")
    db.session.execute(cmd)
    db.session.commit()


def get_latest_pay_period():
    stmt = text(
        """
        SELECT 
        date_actual, 
        rolling_transactions_amounts,
        0 AS break_even
        FROM select_rolling_sum_time_periods() 
        ORDER BY date_actual ASC
        """
    )
    resultset = db.session.execute(stmt)
    rows = resultset.fetchall()
    return rows
