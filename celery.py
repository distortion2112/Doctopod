from app import create_app
from app.celery_utils import make_celery

flask_app = create_app()
celery = make_celery(flask_app)