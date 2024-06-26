import os
import logging

class Config:
    LOGGING_LEVEL = logging.INFO
    LOGGING_FORMAT = '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'  # Added LOGGING_FORMAT
    REDIS_URL = os.getenv('REDIS_URL')
    LOGGING_LOCATION = os.getenv('LOGGING_LOCATION', '/tmp/app.log')  # Default to '/tmp/app.log'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

    @staticmethod
    def init_app(app):
        Config.init_app(app)

class TestingConfig(Config):
    TESTING = True

    @staticmethod
    def init_app(app):
        Config.init_app(app)

class ProductionConfig(Config):
    DEBUG = False

    @staticmethod
    def init_app(app):
        Config.init_app(app)
        # Add any production-specific initialization here

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}