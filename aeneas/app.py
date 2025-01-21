from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_subtitles():
    data = request.json
    video_file_path = data.get('video_file_path')
    subtitle_file_path = data.get('subtitle_file_path')

    if not video_file_path or not subtitle_file_path:
        return {"error": "Missing parameters"}, 400

    # Call your existing script here
    subprocess.run(["python", "/aeneas/process_subtitles.py", video_file_path, subtitle_file_path])

    return {"status": "success"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Use port of your choice