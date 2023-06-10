from flask import url_for


class TestNetWorth(object):
    def test_net_worth(self, client):
        response = client.get(url_for("chart_data.net_worth"))
        assert response.status_code == 200


class TestPayPeriod(object):
    def test_pay_period(self, client):
        response = client.get(url_for("chart_data.pay_period"))
        assert response.status_code == 200
        pay_period_data = response.get_json()
        assert isinstance(pay_period_data, list)
        for entry in pay_period_data:
            assert isinstance(entry, dict)
            assert "date_actual" in entry
            assert "rolling_transactions_amounts_p1" in entry
            assert "rolling_transactions_amounts_p2" in entry
            assert "break_even" in entry


class TestCategorySpending(object):
    def test_category_spending(self, client):
        response = client.get(url_for("chart_data.category_spending"))
        assert response.status_code == 200
        category_spending_data = response.get_json()
        assert isinstance(category_spending_data, list)
        for entry in category_spending_data:
            assert isinstance(entry, dict)
            assert "category_name" in entry
            assert "current_total_transaction_amount" in entry
            assert "previous_total_transaction_amount" in entry
