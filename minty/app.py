import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, request
from flask_migrate import upgrade
from flask_sqlalchemy.record_queries import get_recorded_queries
from sqlalchemy import text

from minty.blueprints.categories import categories_bp
from minty.blueprints.chart_data import chart_data_bp
from minty.blueprints.main import main_bp
from minty.blueprints.ml import ml_bp
from minty.blueprints.view_utils import NegativeIntConverter
from minty.config.settings import FlaskConfig
from minty.extensions import bootstrap, db, debug_toolbar, migrate, profiler
from minty.templates.filters import (
    format_boolean,
    format_currency,
    good_accuracy,
    limit_characters,
)


def create_app(config_class=FlaskConfig):
    app = Flask(import_name=__name__)
    app.config.from_object(config_class)

    app.jinja_env.filters["format_currency"] = format_currency
    app.jinja_env.filters["limit_characters"] = limit_characters
    app.jinja_env.filters["good_accuracy"] = good_accuracy
    app.jinja_env.filters["format_boolean"] = format_boolean

    app.url_map.converters["negative_int"] = NegativeIntConverter

    blueprints(app=app)
    extensions(app=app)

    @app.after_request
    def after_request(response):
        if not app.debug and not app.testing:
            for query in get_recorded_queries():
                if query.duration >= app.config["FLASKY_SLOW_DB_QUERY_TIME"]:
                    app.logger.warning(
                        f"Query: {query.statement} \
                                            \nParameters:{query.parameters} \
                                            \nDuration:{query.duration} \
                                            \nContext:{query.context}"
                    )
        return response

    if app.debug:
        app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

        @app.before_request
        def before_request():
            request.start_time = time.time()

        @app.after_request
        def after_request(response):
            request_name = request.endpoint
            elapsed_time = time.time() - request.start_time
            app.logger.info(f"Request {request_name} took: {elapsed_time:.2f} seconds")
            return response

    if app.testing:
        pass

    if app.config["LOG_TO_STDOUT"]:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    if app.config["LOG_TO_FILE"]:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = TimedRotatingFileHandler(
            "logs/minty.log", when="D", interval=1, backupCount=5, delay=True
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
                "%Y-%m-%dT%H:%M:%S%z",
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    # app.logger.info("Applying postgres setup scripts:")
    postgres_files_short_path = "setup/postgres"
    minty_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    postgres_files_full_path = os.path.join(minty_directory, postgres_files_short_path)

    for file in os.listdir(postgres_files_full_path):
        file_path = os.path.join(postgres_files_full_path, file)
        # app.logger.info(f"    Executing: {file}")
        query = text(open(file_path).read())
        with app.app_context():
            db.session.execute(query)
            db.session.commit()

    with app.app_context():
        from minty.db_utils import (
            populate_calendar_table,
            populate_custom_category_table,
            seed_db,
        )

        app.logger.info("Running postgres startup scripts")
        populate_custom_category_table()
        # seed_db()
        populate_calendar_table()
    return app


def extensions(app):
    debug_toolbar.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    bootstrap.init_app(app=app)
    profiler.init_app(app=app)
    return None


def blueprints(app):
    app.register_blueprint(blueprint=main_bp)
    app.register_blueprint(blueprint=chart_data_bp)
    app.register_blueprint(blueprint=ml_bp)
    app.register_blueprint(blueprint=categories_bp)
    return None
