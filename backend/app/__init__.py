from flask import Flask, request, jsonify
from flask_cors import CORS
import wave
import struct
import io

app = Flask(__name__)
CORS(app)

def detect_silence(audio_data):
    # Open audio file from bytes
    with wave.open(io.BytesIO(audio_data), 'rb') as wav_file:
        framerate = wav_file.getframerate()
        sampwidth = wav_file.getsampwidth()
        nframes = wav_file.getnframes()
        audio_data = wav_file.readframes(nframes)

        # Convert byte data to integer samples
        fmt = f"<{nframes * sampwidth}h"
        samples = struct.unpack(fmt, audio_data)

        # Define silence threshold and duration
        silence_threshold = 500  # Example value; adjust as needed
        silence_duration = 1000  # 1000 ms
        
        silent_intervals = []
        in_silence = False
        start_time = 0
        
        # Calculate silence intervals
        for i, sample in enumerate(samples):
            if abs(sample) < silence_threshold:
                if not in_silence:
                    start_time = i / framerate * 1000
                    in_silence = True
            else:
                if in_silence:
                    end_time = i / framerate * 1000
                    if end_time - start_time > silence_duration:
                        silent_intervals.append((start_time, end_time))
                    in_silence = False

    return silent_intervals

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        audio_data = file.read()
        silent_intervals = detect_silence(audio_data)
        return jsonify({"silent_intervals": silent_intervals}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
