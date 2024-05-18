from flask import Blueprint, request, jsonify, current_app
from .tasks import async_create_outline, async_generate_podcast_content, async_process_outline, async_assemble_script
import os

main = Blueprint('main', __name__)

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file:
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)
        outline_task = async_create_outline.apply_async(args=[file_path])
        return jsonify({"task_id": outline_task.id})

@main.route('/outline_status/<task_id>', methods=['GET'])
def outline_status(task_id):
    task = async_create_outline.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', ''),
            'result': task.info.get('result', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # exception raised
        }
    return jsonify(response)

@main.route('/process_outline/<task_id>', methods=['POST'])
def process_outline(task_id):
    task = async_create_outline.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        outline = task.info['result']
        process_task = async_process_outline.apply_async(args=[outline])
        return jsonify({"task_id": process_task.id})
    else:
        return jsonify({"error": "Outline task not completed or failed"})

@main.route('/assemble_script/<task_id>', methods=['POST'])
def assemble_script(task_id):
    task = async_process_outline.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        section_task_ids = task.info
        assemble_task = async_assemble_script.apply_async(args=[section_task_ids])
        return jsonify({"task_id": assemble_task.id})
    else:
        return jsonify({"error": "Processing task not completed or failed"})