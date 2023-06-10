from flask import url_for

from minty.blueprints.main.forms import SearchForm
from minty.models import Account, Transaction


class TestIndexPage(object):
    def test_index_page(self, client):
        response = client.get(url_for("main.index"))
        assert response.status_code == 200


class TestRefreshData(object):
    def test_refresh_data(self, client):
        response = client.get(url_for("main.refresh_data"))
        assert response.status_code == 200


class TestAnalyzeData(object):
    def test_analyze_data(self, client):
        response = client.get(url_for("main.analyze_data"))
        assert response.status_code == 200


class TestAllTransactions(object):
    def test_all_transactions(self, client):
        response = client.get(url_for("main.all_transactions"))
        assert response.status_code == 200


class TestAccountTransactions(object):
    def test_account_transactions(self, client):
        account = Account.query.first()
        response = client.get(
            url_for("main.account_transactions", account_id=account.account_id)
        )
        assert response.status_code == 200


class TestSearchTransactions(object):
    def test_search_transactions(self, client):
        transaction = Transaction.query.first()
        search_term = transaction.transaction_description
        with client.application.test_request_context():
            search_form = SearchForm(q=search_term)
            response = client.post(
                url_for("main.all_transactions_search"),
                data=search_form.data,
                follow_redirects=True,
            )
            assert response.status_code == 200
            assert search_term.encode() in response.data
