from flask import Flask
from .config import config, init_app
from .celery_utils import make_celery
import logging

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize Celery
    celery = make_celery(app)

    # Import and register blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    configure_logging(app)

    return app, celery


def configure_logging(app):
    import logging
    from logging.handlers import RotatingFileHandler

    if not app.debug:
        file_handler = RotatingFileHandler(app.config['LOGGING_LOCATION'], maxBytes=10000, backupCount=1)
        file_handler.setLevel(app.config['LOGGING_LEVEL'])
        file_handler.setFormatter(logging.Formatter(app.config['LOGGING_FORMAT']))
        app.logger.addHandler(file_handler)