from faker import Faker
from minty.extensions import db
from minty.models import Transaction

fake = Faker(seed=1234)

max_transactions=100

for transaction in range(0, max_transactions):
    Transaction.transaction_description = fake.sentence(nb_words=4, variable_nb_words=True)