from flask import Flask
from .routes import main
from .config import Config
from celery import Celery
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Create Celery object
    celery = make_celery(app)

    # Register blueprints
    app.register_blueprint(main)

    # Configure logging
    configure_logging(app)

    return app

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

def configure_logging(app):
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(app.config['LOGGING_LOCATION'], maxBytes=10000, backupCount=1)
        file_handler.setLevel(app.config['LOGGING_LEVEL'])
        file_handler.setFormatter(logging.Formatter(app.config['LOGGING_FORMAT']))
        app.logger.addHandler(file_handler)