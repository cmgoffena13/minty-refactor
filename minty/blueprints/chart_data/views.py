from datetime import datetime, timedelta

from flask import Blueprint, jsonify

from minty.db_utils import (
    get_latest_category_spending,
    get_latest_pay_period,
    get_monthly_expenses,
)
from minty.models import NetWorth

chart_data_bp = Blueprint(
    name="chart_data", import_name=__name__, template_folder="templates"
)


@chart_data_bp.route("/chart-data/net_worth")
def net_worth():
    net_worth_data = NetWorth.query.filter(
        NetWorth.net_worth_date >= (datetime.now() - timedelta(days=395))
    ).all()
    net_worth_list = [
        {
            "net_worth_date": net_worth.net_worth_date.strftime("%Y-%m-%d"),
            "assets_amount": int(net_worth.assets_amount),
            "debts_amount": int(net_worth.debts_amount),
            "net_amount": int(net_worth.net_amount),
        }
        for net_worth in net_worth_data
    ]
    return jsonify(net_worth_list)


@chart_data_bp.route("/chart-data/pay_period")
def pay_period():
    pay_period_data = get_latest_pay_period()
    pay_period_data = [
        {
            "date_actual": pay_period.date_actual.strftime("%Y-%m-%d"),
            "rolling_transactions_amounts_p1": int(
                pay_period.rolling_transactions_amounts_p1
            ),
            "rolling_transactions_amounts_p2": int(
                pay_period.rolling_transactions_amounts_p2
            ),
            "break_even": int(pay_period.break_even),
        }
        for pay_period in pay_period_data
    ]
    return jsonify(pay_period_data)


@chart_data_bp.route("/chart-data/category_spending")
def category_spending():
    # CATEGORIES_SKIP = set(["APT_RENT", "HOUSE_MORTGAGE"])
    category_spending_data = get_latest_category_spending()
    category_spending_data = [
        {
            "category_name": str(category_spending.custom_category_name).replace(
                "_", " "
            ),
            "current_total_transaction_amount": int(
                category_spending.total_transaction_amount_p1
            ),
            "previous_total_transaction_amount": int(
                category_spending.total_transaction_amount_p2
            ),
        }
        for category_spending in category_spending_data
        if category_spending.custom_category_name  # not in CATEGORIES_SKIP
    ]
    return jsonify(category_spending_data)


@chart_data_bp.route("/chart-data/monthly_expenses")
def monthly_expenses():
    monthly_expenses_data = get_monthly_expenses(
        date_filter=datetime.date((datetime.now() - timedelta(days=395)))
    )
    monthly_expenses_data = [
        {
            "last_date_of_month": monthly_expenses.last_date_of_month.strftime(
                "%Y-%m-%d"
            ),
            "monthly_expenses": -int(monthly_expenses.monthly_expenses),
        }
        for monthly_expenses in monthly_expenses_data
    ]
    return jsonify(monthly_expenses_data)
