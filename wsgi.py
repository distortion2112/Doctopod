import os
from app import create_app
from app.celery_utils import make_celery
from redis import Redis
from flask import url_for

# Get the configuration name from the environment variable FLASK_CONFIG
# Default to 'production' if the variable is not set
config_name = os.getenv('FLASK_CONFIG', 'production')
app = create_app(config_name)  # Create the Flask application using the specified configuration
celery = make_celery(app)  # Initialize Celery after creating the Flask app

@app.route('/')
def home():
    redis_test_url = url_for('test_redis_connection')
    welcome_message = f"""Hey if you want to test your redis connection: 
    Detailed Test: <a href="{redis_test_url}">go to /test_redis_connection</a>"""
    return welcome_message

@app.route('/test_redis_connection')
def test_redis_connection():
    redis_url = os.getenv('REDIS_URL')
    redis = Redis.from_url(redis_url)

    # Test the connection
    try:
        redis.ping()
        return "Connected to Redis"
    except Exception as e:
        return f"Cannot connect to Redis: {str(e)}"

# If this script is executed directly, run the Flask development server
# Note: This block is not used when deploying with Gunicorn
if __name__ == "__main__":
    app.run()