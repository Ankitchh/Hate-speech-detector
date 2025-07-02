from flask import Flask, render_template, request, url_for, redirect, Blueprint
import os
from io import BytesIO
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()


models = Blueprint("models", __name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'avi'}


# elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# audio_path = "website/static/uploads/audio.mp3"

# # Open the file directly instead of using requests.get()
# with open(audio_path, 'rb') as audio_file:
#     audio_data = BytesIO(audio_file.read())

# transcription = elevenlabs.speech_to_text.convert(
#     file=audio_data,
#     model_id="scribe_v1",  # Model to use, for now only "scribe_v1" is supported
#     tag_audio_events=True,  # Tag audio events like laughter, applause, etc.
#     language_code="eng",  # Language of the audio file. If set to None, the model will detect the language automatically.
#     diarize=True,  # Whether to annotate who is speaking
# )



# # Join all words and spacings in correct order
# clean_text = ''.join([word.text for word in transcription.words])
# print(clean_text)

