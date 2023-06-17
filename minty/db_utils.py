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
        rolling_transactions_amounts_p1,
		rolling_transactions_amounts_p2,
        0 AS break_even
        FROM select_rolling_sum_time_periods() 
        ORDER BY date_actual ASC
        """
    )
    resultset = db.session.execute(stmt)
    rows = resultset.fetchall()
    return rows


def get_latest_category_spending():
    stmt = text(
        """
        SELECT
        custom_category_name,
        total_transaction_amount_p1,
        total_transaction_amount_p2
        FROM select_latest_category_spending()
        """
    )
    resultset = db.session.execute(stmt)
    rows = resultset.fetchall()
    return rows


def get_monthly_expenses(date_filter):
    stmt = text(
        f"""
        SELECT
        last_date_of_month,
        monthly_expenses
        FROM select_monthly_expenses('{date_filter}')
        """
    )
    resultset = db.session.execute(stmt)
    rows = resultset.fetchall()
    return rows
