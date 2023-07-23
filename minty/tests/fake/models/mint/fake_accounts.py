from faker import Faker

from minty.extensions import db
from minty.models import Account

fake = Faker()


class FakeAccount(Account):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate_fake_id(self):
        self.account_id = fake.unique.random_number(digits=6)
        self.is_operation_account = True

    def generate_fake_data(self):
        db.session.add(self)
        db.session.commit()
