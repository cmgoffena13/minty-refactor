import time

import requests
from flask import current_app, flash, url_for

from minty.blueprints.main.forms import AssignCustomCategory
from minty.models import Account, CustomCategory, Transaction


def get_transactions(page, account_id=None, search_data=None):
    query = (
        Transaction.query.with_entities(
            Transaction.transaction_id,
            Transaction.transaction_date,
            Transaction.transaction_description,
            Transaction.transaction_amount,
            Transaction.is_debit,
            Transaction.account_id,
            Account.account_name,
            CustomCategory.custom_category_id,
            CustomCategory.custom_category_name,
        )
        .join(Account)
        .join(CustomCategory)
    )

    if search_data:
        query = query.filter(Transaction.transaction_description.match(search_data))
    if account_id:
        query = query.filter(Transaction.account_id == account_id)

    query = query.order_by(
        Transaction.transaction_date.desc(), Transaction.transaction_id.desc()
    ).paginate(
        page=page,
        per_page=current_app.config["TRANSACTIONS_PER_PAGE"],
        error_out=False,
    )
    return query


def get_accounts():
    query = (
        Account.query.filter(Account.closed == False)
        .with_entities(
            Account.account_id,
            Account.account_name,
            Account.financial_institution_name,
            Account.current_balance,
            Account.mint_last_updated_on,
        )
        .order_by(Account.account_id.asc())
        .all()
    )
    return query


def _get_custom_category_names():
    categories = CustomCategory.query.all()
    category_choices = [
        (category.custom_category_id, category.custom_category_name)
        for category in categories
    ]
    return category_choices


def create_custom_category_forms(transactions):
    forms = list()
    category_choices = _get_custom_category_names()
    for transaction in transactions:
        form = AssignCustomCategory(
            prefix=f"{transaction.transaction_id}",
            category=transaction.custom_category_id,
        )
        form.category.choices = category_choices
        forms.append(form)
    return forms


def record_custom_category(forms, db):
    start_time = time.time()
    for form in forms:  # Only one form can be submited at a time though from the page.
        if form.validate_on_submit():
            transaction = Transaction.query.filter(
                Transaction.transaction_id == form.transaction_id.data
            ).first()
            transaction.set_custom_category(
                custom_category_name_id=int(form.category.data)
            )
            current_app.logger.info(
                f"transaction_id: {transaction.transaction_id} - updating custom_category_id: {form.category.data}"
            )
            db.session.commit()
            end_time = time.time()
            current_app.logger.info(f"Saving took {end_time - start_time:.2f} seconds")
            flash(f"Changes saved for TransactionID: {form.transaction_id.data}")


def convert_records_to_json(records):
    # json_data = [dict(row._asdict()) for row in records]
    data_list = list()
    data = {"transactions": data_list}
    for record in records:
        new_record = dict()
        key = {int(record.transaction_id): new_record}
        new_record["transaction_description"] = str(record.transaction_description)
        new_record["transaction_amount"] = float(record.transaction_amount)
        new_record["account_id"] = int(record.account_id)
        data_list.append(key)
    return data


def make_batch_prediction(json_data):
    url = url_for("ml.predict_batch", _external=True)
    response = requests.post(url, json=json_data)
    if response.status_code == 200:
        predictions = response.json()
        predictions = predictions["predictions"]
        categories = CustomCategory.query.all()
        predictions = {
            int(k): categories[v].custom_category_name for k, v in predictions.items()
        }
    else:
        predictions = None
    return predictions
