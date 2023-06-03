import pytest

from minty.app import create_app
from minty.config.settings import TestConfig
from minty.extensions import db


@pytest.fixture(scope="session")
def test_app():
    print("Setting up test db")
    _app = create_app(config_class=TestConfig)
    _app_context = _app.app_context()
    _app_context.push()
    db.create_all()
    yield
    print("Tearing down test db")
    db.session.remove()
    db.drop_all()
    _app_context.pop()


@pytest.fixture(scope="function")
def client(test_app):
    yield test_app.test_clint()
