import pytest

from minty.app import create_app
from minty.config.settings import TestConfig
from minty.extensions import db
from minty.tests.fake.seed_test_db import seed_test_db
from minty.tests.test_utils import truncate_tables


@pytest.fixture(scope="session")
def test_app():
    print("Setting up test db")
    _app = create_app(config_class=TestConfig)
    _app_context = _app.app_context()
    _app_context.push()
    seed_test_db()
    yield _app
    print("Tearing down test db")
    db.session.remove()
    truncate_tables()
    _app_context.pop()


@pytest.fixture(scope="function")
def client(test_app):
    yield test_app.test_client()
