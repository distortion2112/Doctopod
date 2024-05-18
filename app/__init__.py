from flask import Flask
from .config import Config
from .routes import main
from .celery_utils import make_celery

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(main)

    # Configure logging
    configure_logging(app)

    # Initialize Celery
    celery = make_celery(app)
    app.celery = celery

    return app

def configure_logging(app):
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(app.config['LOGGING_LOCATION'], maxBytes=10000, backupCount=1)
        file_handler.setLevel(app.config['LOGGING_LEVEL'])
        file_handler.setFormatter(logging.Formatter(app.config['LOGGING_FORMAT']))
        app.logger.addHandler(file_handler)