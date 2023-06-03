import numpy as np
from flask import current_app
from mintapi import Mint
from sqlalchemy import text

from minty.config.settings import MintProcessConfig

# from minty.app import create_app
from minty.extensions import db
from minty.models import (
    Account,
    AccountType,
    Category,
    Merchant,
    NetWorth,
    Transaction,
    TransactionType,
)

mint_config = MintProcessConfig()


def _record_account_data(mint):
    account_ids_list = []
    db_account_ids_list = []
    accounts = mint.get_account_data()
    for account in accounts:
        # Account Type Data Row
        account_type_id = account["accountTypeInt"]
        account_type_name = account["type"]

        exists = (
            db.session.query(AccountType.account_type_id)
            .filter_by(account_type_id=account_type_id)
            .first()
            is not None
        )
        if not exists:
            account_type = AccountType(
                account_type_id=account_type_id, account_type_name=account_type_name
            )
            db.session.add(account_type)
            db.session.commit()

        # Account Data Row
        account_id = int(account["id"].split("_")[1])
        account_name = account["name"]
        status = account["accountStatus"]
        closed = bool(account["isClosed"])
        current_balance = account["value"]
        if closed:
            current_balance = 0
        currency_type = account["currency"]
        financial_institution_name = account["fiName"]
        if "lastUpdatedDate" in account["metaData"]:
            mint_last_updated_on = account["metaData"]["lastUpdatedDate"]
        else:
            mint_last_updated_on = None
        if "createdDate" in account["metaData"]:
            mint_created_on = account["metaData"]["createdDate"]
        else:
            mint_created_on = None
        account_type_id = account["accountTypeInt"]

        # if the record doesn't exist, insert
        exists = (
            db.session.query(Account.account_id)
            .filter_by(account_id=account_id)
            .first()
            is not None
        )
        if not exists:
            acct = Account(
                account_id=account_id,
                account_name=account_name,
                status=status,
                closed=closed,
                current_balance=current_balance,
                currency_type=currency_type,
                financial_institution_name=financial_institution_name,
                mint_last_updated_on=mint_last_updated_on,
                mint_created_on=mint_created_on,
                account_type_id=account_type_id,
            )
            db.session.add(acct)
            db.session.commit()
        else:
            acct = Account.query.filter_by(account_id=account_id).one()
            setattr(acct, "current_balance", current_balance)
            setattr(acct, "mint_last_updated_on", mint_last_updated_on)
            db.session.commit()

        account_ids_list.append(account["id"])
        db_account_ids_list.append(account_id)
    return account_ids_list, db_account_ids_list


def _record_transaction_data(mint, account_ids_list, db_account_ids_list, date_filter):
    for account_id, db_account_id in zip(account_ids_list, db_account_ids_list):
        transactions = mint.get_transaction_data(
            account_ids=[account_id], date_filter=date_filter
        )
        for transaction in transactions:
            # Transaction Type Data Row
            transaction_type_name = transaction["type"]
            exists = (
                db.session.query(TransactionType.transaction_type_name)
                .filter_by(transaction_type_name=transaction_type_name)
                .first()
                is not None
            )
            if not exists:
                transaction_type = TransactionType(
                    transaction_type_name=transaction_type_name
                )
                db.session.add(transaction_type)
                db.session.commit()

            # Categories Data Row
            category_id = int(transaction["category"]["id"].split("_")[1])
            category_name = transaction["category"]["name"]
            if "parentId" in transaction["category"]:
                category_parent_id = transaction["category"]["parentId"].split("_")[1]
            else:
                category_parent_id = None
            if "parentName" in transaction["category"]:
                category_parent_name = transaction["category"]["parentName"]
            else:
                category_parent_name = None

            exists = (
                db.session.query(Category.category_id)
                .filter_by(category_id=category_id)
                .first()
                is not None
            )
            if not exists:
                category = Category(
                    category_id=category_id,
                    category_name=category_name,
                    category_parent_id=category_parent_id,
                    category_parent_name=category_parent_name,
                )
                db.session.add(category)
                db.session.commit()

            if not transaction["isPending"]:
                # Transaction Data Row
                transaction_id = int(transaction["id"].split("_")[1])
                transaction_type_id = (
                    db.session.query(TransactionType.transaction_type_id)
                    .filter_by(transaction_type_name=transaction_type_name)
                    .scalar()
                )
                transaction_date = transaction["date"]
                transaction_description = transaction["description"]
                transaction_amount = transaction["amount"]
                debit_or_credit = transaction["transactionType"]
                if debit_or_credit.lower() == "debit":
                    is_debit = True
                else:
                    is_debit = False
                is_expense = transaction["isExpense"]
                if "merchantId" in transaction:
                    merchant_id = transaction["merchantId"]
                else:
                    merchant_id = None

                # Merchant Data Row (not sure how useful it will be)
                if merchant_id:
                    exists = (
                        db.session.query(Merchant.merchant_id)
                        .filter_by(merchant_id=merchant_id)
                        .first()
                        is not None
                    )
                    if not exists:
                        merchant = Merchant(merchant_id=merchant_id)
                        db.session.add(merchant)
                        db.session.commit()

                exists = (
                    db.session.query(Transaction.transaction_id)
                    .filter_by(transaction_id=transaction_id)
                    .first()
                    is not None
                )
                if not exists:
                    transaction = Transaction(
                        transaction_id=transaction_id,
                        transaction_type_id=transaction_type_id,
                        account_id=db_account_id,
                        transaction_date=transaction_date,
                        transaction_description=transaction_description,
                        transaction_amount=transaction_amount,
                        is_debit=is_debit,
                        is_expense=is_expense,
                        merchant_id=merchant_id,
                        category_id=category_id,
                    )
                    db.session.add(transaction)
                    db.session.commit()


def _record_net_worth_data(mint):
    # Record the net worth data
    net_worth_data = mint.get_net_worth_data()

    # The most recent keeps getting updated, so easier to just delete and insert everytime
    most_recent_record = NetWorth.query.order_by(NetWorth.net_worth_date.desc()).first()
    if most_recent_record is not None:
        db.session.delete(most_recent_record)
        db.session.commit()

    for record in net_worth_data:
        net_worth_date = record["date"]
        assets_amount = record["assets"]
        debts_amount = record["debts"]
        if np.isnan(debts_amount):
            debts_amount = 0
        net_amount = record["net"]
        if np.isnan(net_amount):
            net_amount = assets_amount + debts_amount

        exists = (
            db.session.query(NetWorth.net_worth_date)
            .filter_by(net_worth_date=net_worth_date)
            .first()
            is not None
        )
        if not exists:
            net_worth = NetWorth(
                net_worth_date=net_worth_date,
                assets_amount=assets_amount,
                debts_amount=debts_amount,
                net_amount=net_amount,
            )
            db.session.add(net_worth)
            db.session.commit()


def mint_pull(date_filter, outside_web_app=True, full_load=False):
    current_app.logger.info(
        f"Starting mint pull with inputs - date_filer: {date_filter}, full_load: {full_load}"
    )
    mint = Mint(
        email=mint_config.MINT_USERNAME,
        password=mint_config.MINT_PASSWORD,
        headless=True,
        mfa_method="soft-token",
        mfa_token=mint_config.MFA_TOKEN,
        # session_path=mint_config.CHROME_SESSION_PATH,
        wait_for_sync=True,
        wait_for_sync_timeout=300,
    )

    current_app.logger.info(f"Refreshing account data")
    # mint.initiate_account_refresh()

    # if outside_web_app:
    #    mint_pull_app = create_app(config_class=FlaskConfig)
    #    mint_pull_app_context = mint_pull_app.app_context()
    #    mint_pull_app_context.push()

    if full_load:
        current_app.logger.info("Executing Truncate statements")
        stmt = text(
            """
        TRUNCATE TABLE public.accounts, 
					   public.transactions,
					   public.account_types,
					   public.categories,
					   public.merchants,
					   public.custom_categories,
					   public.transaction_types CASCADE;
		TRUNCATE TABLE public.net_worth_by_day;
        """
        )
        db.session.execute(stmt)
        db.session.commit()

    current_app.logger.info("Recording account information")
    account_ids_list, db_account_ids_list = _record_account_data(mint=mint)

    current_app.logger.info("Recording transaction information")
    _record_transaction_data(
        mint=mint,
        account_ids_list=account_ids_list,
        db_account_ids_list=db_account_ids_list,
        date_filter=date_filter,
    )

    current_app.logger.info("Recording Net Worth information")
    _record_net_worth_data(mint=mint)

    # credit_data = mint.get_credit_report_data()
    # print(credit_data)
    mint.close()


# date_filter = "LAST_7_DAYS"
# date_filter = "ALL_TIME"
# mint_pull(date_filter=date_filter, outside_web_app=True, full_load=False)
