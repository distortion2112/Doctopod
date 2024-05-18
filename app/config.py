import os
import logging

class Config:
    LOGGING_LEVEL = logging.INFO
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

def init_app(app):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}