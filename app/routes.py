from flask import Blueprint, request, jsonify, current_app
from .tasks import async_create_outline, async_generate_podcast_content, async_process_outline, async_assemble_script
import os
import logging

main = Blueprint('main', __name__)

@main.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request has the file part
    if 'file' not in request.files:
        current_app.logger.error("No file part in the request")
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    # Check if a file is selected
    if file.filename == '':
        current_app.logger.error("No selected file")
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)
        outline_task = async_create_outline.apply_async(args=[file_path])
        current_app.logger.info(f"File uploaded and task {outline_task.id} created for outline")
        return jsonify({"task_id": outline_task.id}), 202

@main.route('/outline_status/<task_id>', methods=['GET'])
def outline_status(task_id):
    task = async_create_outline.AsyncResult(task_id)
    response = {
        'state': task.state,
        'current': 0,
        'total': 1,
        'status': 'Pending...'
    }
    
    if task.state == 'PENDING':
        current_app.logger.info(f"Task {task_id} is pending")
    elif task.state != 'FAILURE':
        response.update({
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', ''),
            'result': task.info.get('result', '')
        })
        current_app.logger.info(f"Task {task_id} status updated")
    else:
        response.update({
            'current': 1,
            'total': 1,
            'status': str(task.info)  # exception raised
        })
        current_app.logger.error(f"Task {task_id} failed with error: {task.info}")
    
    return jsonify(response)

@main.route('/process_outline/<task_id>', methods=['POST'])
def process_outline(task_id):
    task = async_create_outline.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        outline = task.info['result']
        process_task = async_process_outline.apply_async(args=[outline])
        current_app.logger.info(f"Outline processed and task {process_task.id} created")
        return jsonify({"task_id": process_task.id}), 202
    else:
        current_app.logger.error(f"Outline task {task_id} not completed or failed")
        return jsonify({"error": "Outline task not completed or failed"}), 400

@main.route('/assemble_script/<task_id>', methods=['POST'])
def assemble_script(task_id):
    task = async_process_outline.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        section_task_ids = task.info
        assemble_task = async_assemble_script.apply_async(args=[section_task_ids])
        current_app.logger.info(f"Script assembled and task {assemble_task.id} created")
        return jsonify({"task_id": assemble_task.id}), 202
    else:
        current_app.logger.error(f"Processing task {task_id} not completed or failed")
        return jsonify({"error": "Processing task not completed or failed"}), 400