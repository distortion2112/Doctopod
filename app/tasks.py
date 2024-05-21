import openai
import logging
from celery import Celery
from celery.utils.log import get_task_logger
from .config import Config

# Initialize Celery
celery = Celery(__name__)

# Set up logging
logger = get_task_logger(__name__)

@celery.task
def async_create_outline(file_path):
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
        logger.error(f"Error creating outline: {e}")
        raise e

@celery.task
def async_generate_podcast_content(section_text):
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt="Create a detailed podcast segment for the following section:\n\n" + section_text,
            max_tokens=1000
        )
        detailed_content = response['choices'][0]['text']
        return {'content': detailed_content}
    except Exception as e:
        logger.error(f"Error generating podcast content: {e}")
        raise e

@celery.task
def async_process_outline(outline):
    try:
        # Example implementation: split the outline into sections and process each section
        sections = outline.split('\n')
        section_tasks = [async_generate_podcast_content.apply_async(args=[section]) for section in sections if section.strip()]
        return [task.id for task in section_tasks]
    except Exception as e:
        logger.error(f"Error processing outline: {e}")
        raise e

@celery.task
def async_assemble_script(section_task_ids):
    try:
        # Example implementation: collect the results from each section task and assemble them into a script
        script = ""
        for task_id in section_task_ids:
            section_task = async_generate_podcast_content.AsyncResult(task_id)
            if section_task.state == 'SUCCESS':
                script += section_task.info['content'] + '\n\n'
        return {'script': script}
    except Exception as e:
        logger.error(f"Error assembling script: {e}")
        raise e