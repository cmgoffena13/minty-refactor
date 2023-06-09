from flask import url_for


class TestIndexPage(object):
    def test_index_page(self, client):
        response = client.get(url_for("main.index"))
        assert response.status_code == 200
