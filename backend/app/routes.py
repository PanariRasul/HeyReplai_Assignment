import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from .vad import process_audio

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Process the audio file for VAD
        vad_results = process_audio(file_path)
        
        # Remove the file after processing
        os.remove(file_path)
        
        return jsonify({"vad_results": vad_results})
    else:
        return jsonify({"error": "File type not allowed"}), 400
