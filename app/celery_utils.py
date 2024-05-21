from celery import Celery

def make_celery(app):
    """
    Create a new Celery object and tie the Celery config to the app's config.
    Wrap all tasks in the context of the Flask application.
    
    :param app: The Flask application instance
    :return: A configured Celery object
    """
    celery = Celery(
        app.import_name,
        backend=app.config['REDIS_URL'],
        broker=app.config['REDIS_URL']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery