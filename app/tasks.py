import openai
from celery import Celery

celery = Celery(__name__)

@celery.task
def async_create_outline(file_path):
    with open(file_path, 'r') as file:
        document_text = file.read()
    response = openai.Completion.create(
        engine="davinci",
        prompt="Create an outline for the following document:\n\n" + document_text,
        max_tokens=500
    )
    outline = response['choices'][0]['text']
    return {'outline': outline}

@celery.task
def async_generate_podcast_content(section_text):
    response = openai.Completion.create(
        engine="davinci",
        prompt="Create a detailed podcast segment for the following section:\n\n" + section_text,
        max_tokens=1000
    )
    detailed_content = response['choices'][0]['text']
    return {'content': detailed_content}