import os
from enum import Enum

from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
load_dotenv(os.path.join(base_dir, ".env"))
load_dotenv(os.path.join(base_dir, ".flaskenv"))


class MintProcessConfig(object):
    MINT_USERNAME = os.environ["MINT_USERNAME"]
    MINT_PASSWORD = os.environ["MINT_PASSWORD"]
    MFA_TOKEN = os.environ["MFA_TOKEN"]


class FlaskConfig(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
    FLASK_ENVIRONMENT = os.environ.get("FLASK_ENVIRONMENT")
    FLASK_APP = os.environ.get("FLASK_APP")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_PROFILER_DATABASE_URI = os.environ.get("PROFILER_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_SLOW_DB_QUERY_TIME = 0.5
    TRANSACTIONS_PER_PAGE = int(os.environ.get("TRANSACTIONS_PER_PAGE", 20))
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")
    LOG_TO_FILE = os.environ.get("LOG_TO_FILE")
    MIGRATE_IGNORE_TABLES = ["calendar"]
    FLASK_PROFILER = {
        "enabled": FLASK_DEBUG,
        "storage": {"engine": "sqlalchemy", "db_url": SQLALCHEMY_PROFILER_DATABASE_URI},
        "endpointRoot": "flask-profiler",
        "ignore": ["^/static/.*", "/_debug_toolbar/[^/]+."],
    }
    THREADING_ENABLED = True


class TestConfig(FlaskConfig):
    FLASK_DEBUG = 0
    TESTING = (True,)
    LOG_TO_FILE = 0
    LOG_TO_STDOUT = 0
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")
    SERVER_NAME = "localhost"
    APPLICATION_ROOT = "/"
    PREFERRED_URL_SCHEME = "http"


class CustomCategoryEnum(Enum):
    PAYCHECK = 1  # This is required. Used for Pay Period Calculations.
    ADDITIONAL_INCOME = 2
    APT_RENT = 3
    APT_PARKING = 4
    APT_ELECTRIC = 5
    CAR_GAS = 6
    HOUSE_UTILITIES = 7
    HOUSE_MORTGAGE = 8
    OPEN_HARVEST = 9
    GRUBHUB = 10
    MISC_FOOD = 11
    WORKING_OUT = 12
    AMAZON_BOOKS = 13
    ENTERTAINMENT = 14
    NAUGHTY_NAUGHTY = 15
    UNPLANNED = 16
    UNKNOWN = -1  # This is required. Default value for select field.
    EDUCATION = 17
    TRANSFER = -2  # This is required. Monthly expenses
    CRETID_CARD_PAYMENT = -3  # This is required. Monthly expenses
    HOUSE_REPAIR = 18
