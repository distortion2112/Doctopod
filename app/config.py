import os

class Config:
    # Your existing configurations
    LOGGING_LEVEL = logging.INFO
    # Add Redis configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

def init_app(app):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    # Production specific configurations
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}