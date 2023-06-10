from datetime import datetime

from faker import Faker

from minty.tests.fake.models.mint import FakeAccount, FakeTransaction

fake = Faker()


def create_fake_accounts():
    fake_accounts = []

    fake_account = FakeAccount(
        account_name="Checking",
        financial_institution_name="Banky Bank",
        current_balance=0,
        closed=False,
        is_operation_account=True,
    )
    fake_account.generate_fake_id()
    fake_accounts.append(fake_account.account_id)
    fake_account.generate_fake_data()

    fake_account = FakeAccount(
        account_name="Savings",
        financial_institution_name="Banky Bank",
        current_balance=0,
        closed=False,
        is_operation_account=False,
    )
    fake_account.generate_fake_id()
    fake_accounts.append(fake_account.account_id)
    fake_account.generate_fake_data()
    return fake_accounts


def create_fake_transactions(months, transactions_per_month):
    fake_accounts = create_fake_accounts()
    for month in range(0, months):
        month += 1
        for tran_index, _ in enumerate(range(transactions_per_month)):
            transaction = FakeTransaction()
            transaction.transaction_date = fake.date_between_dates(
                date_start=datetime(datetime.today().year, month, 1),
                date_end=datetime(datetime.today().year, month, 28),
            )

            if tran_index == 0:
                transaction.custom_category_id = 1  # paycheck per month

            if transaction.custom_category_id == 1:
                transaction.transaction_amount = fake.random_int(min=5000, max=8000)
            else:
                transaction.transaction_amount = fake.random_int(min=-4000, max=-1)

            if transaction.custom_category_id == 1:
                transaction.account_id = fake_accounts[0]  # first is checking
            else:
                transaction.account_id = fake.random_choices(elements=fake_accounts)[0]
            transaction.generate_fake_data()
