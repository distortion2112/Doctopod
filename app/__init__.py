from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .routes import main
    app.register_blueprint(main)

    from .celery_utils import make_celery
    celery = make_celery(app)
    app.celery = celery

    configure_logging(app)

    return app

def configure_logging(app):
    import logging
    from logging.handlers import RotatingFileHandler

    if not app.debug:
        file_handler = RotatingFileHandler(app.config['LOGGING_LOCATION'], maxBytes=10000, backupCount=1)
        file_handler.setLevel(app.config['LOGGING_LEVEL'])
        file_handler.setFormatter(logging.Formatter(app.config['LOGGING_FORMAT']))
        app.logger.addHandler(file_handler)