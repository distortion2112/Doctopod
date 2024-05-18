import os

class Config:
    UPLOAD_FOLDER = 'uploads'
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    LOGGING_LOCATION = 'app.log'
    LOGGING_LEVEL = logging.INFO