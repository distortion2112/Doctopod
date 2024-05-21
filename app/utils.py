import openai
from flask import current_app
from . import celery
import logging

logger = logging.getLogger(__name__)

@celery.task(bind=True)
def async_create_outline(self, file_path):
    try:
        return create_outline(file_path)
    except Exception as e:
        logger.error(f"Error in async_create_outline: {e}")
        self.retry(exc=e, countdown=60, max_retries=3)

@celery.task(bind=True)
def async_generate_podcast_content(self, section_text):
    try:
        return generate_podcast_content(section_text)
    except Exception as e:
        logger.error(f"Error in async_generate_podcast_content: {e}")
        self.retry(exc=e, countdown=60, max_retries=3)

def create_outline(file_path):
    try:
        with open(file_path, 'r') as file:
            document_text = file.read()
        response = openai.Completion.create(
            engine="davinci",
            prompt="Create an outline for the following document:\n\n" + document_text,
            max_tokens=500
        )
        outline = response['choices'][0]['text']
        return {'outline': outline}
    except Exception as e:
        logger.error(f"Error in create_outline: {e}")
        raise

def generate_podcast_content(section_text):
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt="Create a detailed podcast segment for the following section:\n\n" + section_text,
            max_tokens=1000
        )
        detailed_content = response['choices'][0]['text']
        return {'content': detailed_content}
    except Exception as e:
        logger.error(f"Error in generate_podcast_content: {e}")
        raise