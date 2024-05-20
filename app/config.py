import os
import logging

class Config:
    LOGGING_LEVEL = logging.INFO
    REDIS_URL = os.getenv('REDIS_URL')

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