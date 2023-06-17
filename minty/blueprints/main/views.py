from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from minty.blueprints.main.forms import RefreshData, SearchForm
from minty.blueprints.main.tasks import mint_pull
from minty.blueprints.main.view_utils import (
    convert_records_to_json,
    create_custom_category_forms,
    get_accounts,
    get_transactions,
    make_batch_prediction,
    record_custom_category,
)
from minty.extensions import db
from minty.models import Account

main_bp = Blueprint(name="main", import_name=__name__, template_folder="templates")


@main_bp.before_app_request
def before_request():
    g.search_form = SearchForm()


@main_bp.route("/", methods=["GET"])
@main_bp.route("/index", methods=["GET"])
def index():
    accounts = get_accounts()
    return render_template(
        template_name_or_list="main/index.html",
        title="Home",
        accounts=accounts,
    )


@main_bp.route("/refresh-data", methods=["GET", "POST"])
def refresh_data():
    form = RefreshData()

    if form.validate_on_submit():
        mint_pull(date_filter=form.date_filter.data)
        flash(f"Refreshed data using filter: {form.date_filter.data}")
        return redirect(url_for("main.refresh_data", title="Refresh Data", form=form))

    return render_template(
        template_name_or_list="main/refresh_data.html", title="Refresh Data", form=form
    )


@main_bp.route("/analyze-data", methods=["GET", "POST"])
def analyze_data():
    return render_template(
        template_name_or_list="main/analyze_data.html", title="Analyze Data"
    )


@main_bp.route("/transactions", methods=["GET", "POST"])
def all_transactions():
    page = request.args.get("page", 1, type=int)
    transactions = get_transactions(page=page)

    next_url = (
        url_for("main.all_transactions", page=transactions.next_num)
        if transactions.has_next
        else None
    )
    prev_url = (
        url_for("main.all_transactions", page=transactions.prev_num)
        if transactions.has_prev
        else None
    )

    forms = create_custom_category_forms(transactions=transactions)

    transaction_json = convert_records_to_json(transactions.items)
    predictions = make_batch_prediction(json_data=transaction_json)
    print(predictions)

    transaction_data = zip(transactions, forms)

    if request.method == "POST":
        record_custom_category(forms=forms, db=db)

        return redirect(
            url_for(
                "main.all_transactions",
                page=page,
                next_url=next_url,
                prev_url=prev_url,
                transaction_data=transaction_data,
                transactions=transactions,
                predictions=predictions,
                route="main.all_transactions",
            )
        )

    return render_template(
        template_name_or_list="main/transactions.html",
        title="Transactions",
        next_url=next_url,
        prev_url=prev_url,
        transaction_data=transaction_data,
        transactions=transactions,
        predictions=predictions,
        route="main.all_transactions",
    )


@main_bp.route("/<int:account_id>/transactions", methods=["GET", "POST"])
def account_transactions(account_id):
    page = request.args.get("page", 1, type=int)

    transactions = get_transactions(page=page, account_id=account_id)

    next_url = (
        url_for(
            "main.account_transactions",
            account_id=account_id,
            page=transactions.next_num,
        )
        if transactions.has_next
        else None
    )
    prev_url = (
        url_for(
            "main.account_transactions",
            account_id=account_id,
            page=transactions.prev_num,
        )
        if transactions.has_prev
        else None
    )

    account_name_data = (
        db.session.query(Account.account_name)
        .filter(Account.account_id == account_id)
        .one()
    )
    account_name_header = account_name_data[0]

    forms = create_custom_category_forms(transactions=transactions)

    transaction_json = convert_records_to_json(transactions.items)
    predictions = make_batch_prediction(json_data=transaction_json)

    transaction_data = zip(transactions, forms)

    if request.method == "POST":
        record_custom_category(forms=forms, db=db)

        return redirect(
            url_for(
                "main.account_transactions",
                account_name_header=account_name_header,
                account_id=account_id,
                page=page,
                next_url=next_url,
                prev_url=prev_url,
                transaction_data=transaction_data,
                transactions=transactions,
                predictions=predictions,
                route="main.account_transactions",
            )
        )

    return render_template(
        template_name_or_list="main/transactions.html",
        title="Transactions",
        account_name_header=account_name_header,
        account_id=account_id,
        next_url=next_url,
        prev_url=prev_url,
        transaction_data=transaction_data,
        transactions=transactions,
        predictions=predictions,
        route="main.account_transactions",
    )


@main_bp.route("/transactions/search", methods=["GET", "POST"])
def all_transactions_search():
    if not g.search_form.validate():
        return redirect(url_for("main.all_transactions"))

    page = request.args.get("page", 1, type=int)
    transactions = get_transactions(page=page, search_data=g.search_form.q.data)

    next_url = (
        url_for(
            "main.all_transactions_search",
            q=g.search_form.q.data,
            page=transactions.next_num,
        )
        if transactions.has_next
        else None
    )
    prev_url = (
        url_for(
            "main.all_transactions_search",
            q=g.search_form.q.data,
            page=transactions.prev_num,
        )
        if transactions.has_prev
        else None
    )

    forms = create_custom_category_forms(transactions=transactions)

    transaction_json = convert_records_to_json(transactions.items)
    predictions = make_batch_prediction(json_data=transaction_json)

    transaction_data = zip(transactions, forms)

    if request.method == "POST":
        record_custom_category(forms=forms, db=db)

        return redirect(
            url_for(
                "main.all_transactions_search",
                page=page,
                q=g.search_form.q.data,
                next_url=next_url,
                prev_url=prev_url,
                transaction_data=transaction_data,
                transactions=transactions,
                predictions=predictions,
                route="main.all_transactions_search",
            )
        )

    return render_template(
        template_name_or_list="main/transactions.html",
        title="Search",
        q=g.search_form.q.data,
        next_url=next_url,
        prev_url=prev_url,
        transaction_data=transaction_data,
        transactions=transactions,
        predictions=predictions,
        route="main.all_transactions_search",
    )
