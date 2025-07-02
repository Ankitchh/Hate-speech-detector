# website/models.py
from io import BytesIO

from flask import render_template, request, url_for, redirect, Blueprint, current_app
import os
import requests
from werkzeug.utils import secure_filename
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import json

load_dotenv()
elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

models = Blueprint("models", __name__)
ALLOWED_EXTENSIONS = {'mp3'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@models.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'audio' in request.files:
            file = request.files['audio']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)

                # ✅ Check if file size is non-zero
                if os.path.getsize(file_path) == 0:
                    return "❌ Uploaded file is empty or corrupted."

                try:
                    # ✅ Try ElevenLabs transcription
                    with open(file_path, 'rb') as f:
                        audio_data = BytesIO(f.read())

                    transcription = elevenlabs.speech_to_text.convert(
                        file=audio_data,
                        model_id="scribe_v1",
                        tag_audio_events=True,
                        language_code="eng",
                        diarize=True,
                    )
                    clean_text = ''.join([word.text for word in transcription.words])
                    rating = rate_output(clean_text)
                    return render_template("result.html", transcription=rating)
                except Exception as e:
                    return f"❌ Error in ElevenLabs API: {str(e)}"
            else:
                return "❌ Invalid file format. Please upload an mp3 or wav file."
        else:
            return "❌ No file uploaded."
    return render_template("base.html")



# Send transcription to Ollama
def rate_output(text):
    system_prompt = (
        "You are a text rating system. Rate the text based on the following criteria: "
        "Hate speech: Does the text contain hate speech? "
        "Bad words: Does the text contain bad words?"
        "Focus on hate speech and show if the text contains bad words or not. Detect bad words only if they are used in a hateful context."
        "Provide a rating between 1 to 10, where 1 is no hate speech or bad words and 10 is extremely hateful or full of bad words. "
        "Start with based on given speech"
    )
    user_prompt = f"Rate the following text between 1 to 10 from the intensity of hate speech or bad words: {text}"

    ollama_response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "gemma3:1b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        }
    )

    full_content = ""

    try:
        for line in ollama_response.text.strip().splitlines():
            if not line.strip():
                continue
            try:
                chunk = json.loads(line)
                if "message" in chunk and "content" in chunk["message"]:
                    full_content += chunk["message"]["content"]
            except json.JSONDecodeError as e:
                print(f"Skipping invalid line: {line[:100]}... ({e})")
                continue
        return full_content.strip()
    except Exception as e:
        return f"❌ Failed to parse JSON response from Ollama: {e}"

    
#   render_template("result.html", transcription= rate_output("This is a test text to rate the hate speech and bad words. (Hey Mohammed, go back to Marrakesh, we don't want Muslims in our country.)"))

# @models.route('/result')
# def result():
#     transcription = request.args.get('transcription', '')
#     return render_template("result.html", text=transcription)












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




# Result Page
# Okay, here's a rating of the text based on the criteria you provided, with a breakdown of the intensity: **Overall Rating: 6/10** **1. Hate Speech:** No. **2. Bad Words:** Yes. **Detailed Breakdown:** * **Intensity of Hate Speech:** Moderate. The text uses profanity (f\*ck, shit, etc.) and boasts about violence and criminal behavior. It’s a direct expression of anger and aggression, bordering on offensive. It's not overtly hateful in a targeted way, but it contributes to a hostile atmosphere. * **Bad Words:** Yes. The profanity and boastful language are the primary indicators of the text's problematic nature. **Justification for Rating:** The text leans heavily into aggressive and potentially threatening rhetoric. While it’s expressed in a somewhat stylized way, the core message – a desire for dominance and violence – is undeniably harmful. The language used is certainly not appropriate for a constructive or respectful discussion. Let me know if you'd like me to rate it on any other criteria (e.g., negativity, humor, etc.).