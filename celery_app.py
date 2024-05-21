from app import create_app
from app.celery_utils import make_celery

# Create an instance of the Flask application
flask_app = create_app()

# Create an instance of Celery using the Flask app context
celery = make_celery(flask_app)

# If you have any custom configurations for Celery, you can set them here
# e.g., celery.conf.update({})

# Ensure that Flask app context is pushed to allow Celery tasks to access the Flask app context
@celery.task(bind=True)
def debug_task(self):
    with flask_app.app_context():
        print('Request: {0!r}'.format(self.request))

# Optional: You can define other configurations or tasks here if needed