from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from .utils import async_create_outline, async_generate_podcast_content

main = Blueprint('main', __name__)

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        task = async_create_outline.apply_async(args=[file_path])
        return jsonify({'task_id': task.id}), 202

@main.route('/process_section', methods=['POST'])
def process_section():
    data = request.get_json()
    section_text = data.get('section_text')
    if not section_text:
        return jsonify({'error': 'No section text provided'}), 400
    task = async_generate_podcast_content.apply_async(args=[section_text])
    return jsonify({'task_id': task.id}), 202

@main.route('/combine_segments', methods=['POST'])
def combine_segments():
    data = request.get_json()
    segments = data.get('segments')
    if not segments:
        return jsonify({'error': 'No segments provided'}), 400
    combined_script = "\n\n".join(segments)
    return jsonify({'podcast_script': combined_script})