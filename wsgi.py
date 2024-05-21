import os
from app import create_app
from app.celery_utils import make_celery

# Get the configuration name from the environment variable FLASK_CONFIG
# Default to 'production' if the variable is not set
config_name = os.getenv('FLASK_CONFIG', 'production')
app = create_app(config_name)  # Create the Flask application using the specified configuration
celery = make_celery(app)  # Initialize Celery after creating the Flask app

@app.route('/')
def home():
    welcome_message = "Hey if you want to test your redis connection, go to /test_redis"
    return welcome_message

@app.route('/test_redis')
def test_redis():
    result = celery.send_task('test_redis_connection')
    return str(result.get())

# If this script is executed directly, run the Flask development server
# Note: This block is not used when deploying with Gunicorn
if __name__ == "__main__":
    app.run()