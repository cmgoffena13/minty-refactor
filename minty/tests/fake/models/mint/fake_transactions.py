from faker import Faker

from minty.extensions import db
from minty.models import Transaction

fake = Faker()


class FakeTransaction(Transaction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_category_id = -1

    def generate_fake_description(self):
        if self.custom_category_id == 1:
            description = "Direct Deposit"
        else:
            description = fake.sentence(nb_words=4, variable_nb_words=True)
        return description

    @staticmethod
    def generate_fake_id():
        return fake.unique.random_number(digits=6)

    def generate_fake_data(self):
        self.transaction_description = self.generate_fake_description()
        self.is_debit = True if self.transaction_amount < 0 else False
        self.is_expense = True if self.is_debit else False
        self.transaction_id = self.generate_fake_id()

        db.session.add(self)
        db.session.commit()
