from flask import current_app, flash

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
            Account.account_name,
            CustomCategory.custom_category_name,
        )
        .join(Account)
        .outerjoin(CustomCategory)
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
    category_names = [category.custom_category_name for category in categories]
    return category_names


def create_custom_category_forms(transactions):
    forms = list()
    category_names = _get_custom_category_names()
    for transaction in transactions:
        form = AssignCustomCategory(
            prefix=f"{transaction.transaction_id}",
            category=transaction.custom_category_name,
        )
        form.category.choices = category_names
        forms.append(form)
    return forms


def record_custom_category(forms, db):
    for form in forms:  # Only one form can be submited at a time though from the page.
        if form.validate_on_submit():
            transaction = Transaction.query.filter(
                Transaction.transaction_id == form.transaction_id.data
            ).first()
            transaction.set_custom_category(custom_category_name=form.category.data)
            current_app.logger.info(
                f"transaction_id: {transaction.transaction_id} - updating custom_category: {form.category.data}"
            )
            db.session.commit()
            flash(
                f"TransactionID: {form.transaction_id.data} >>> Category changed to '{form.category.data}'"
            )
