from faker import Faker

from minty.tests.fake.fake_utils import create_fake_transactions

FAKER_SEED = 1234
Faker.seed(FAKER_SEED)


def seed_test_db():
    create_fake_transactions(months=5, transactions_per_month=20)
