from flask import Flask, render_template, request, url_for, redirect, Blueprint
import os
import requests

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'avi'}

models = Blueprint("models", __name__)

# Define your Whisper API endpoint
WHISPER_API_ENDPOINT = "https://your-whisper-api-endpoint.com/transcribe"

@models.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        if 'audio' in request.files:
            file = request.files['audio']
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                # Send the audio file to Whisper for transcription
                transcription = transcribe_audio(os.path.join(UPLOAD_FOLDER, filename))
                return redirect(url_for('models.result', transcription=transcription))
            else:
                return "Invalid file format for audio"
        elif 'video' in request.files:
            file = request.files['video']
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                # Send the video file to Whisper for transcription
                transcription = transcribe_video(os.path.join(UPLOAD_FOLDER, filename))
                return redirect(url_for('models.result', transcription=transcription))
            else:
                return "Invalid file format for video"
    return render_template("base.html")

@models.route('/result')
def result():
    transcription = request.args.get('transcription', '')
    return render_template("result.html", transcription=transcription)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import requests

def transcribe_audio(audio_file_path):
    # Make a POST request to WHISPER_API_ENDPOINT with the audio file
    files = {'audio_file': open(audio_file_path, 'rb')}
    response = requests.post(WHISPER_API_ENDPOINT, files=files)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return the transcribed text from the response
        return response.text
    else:
        # If the request was not successful, print an error message and return None
        print("Error:", response.status_code, response.text)
        return None

def transcribe_video(video_file_path):
    # Make a POST request to WHISPER_API_ENDPOINT with the video file
    files = {'video_file': open(video_file_path, 'rb')}
    response = requests.post(WHISPER_API_ENDPOINT, files=files)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return the transcribed text from the response
        return response.text
    else:
        # If the request was not successful, print an error message and return None
        print("Error:", response.status_code, response.text)
        return None

