from flask import Flask, render_template, request, jsonify
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from playsound import playsound
import os

app = Flask(__name__)
translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    target_language = request.form.get('target_language')

    # Simulating recognized text (replace this with actual speech recognition logic)
    recognized_text = "Hello, how are you?"

    if recognized_text and target_language:
        translated_text = translate_text(recognized_text, target_language)
        if translated_text:
            play_translated_audio(translated_text, target_language)
            return jsonify({'translated_text': translated_text})
        else:
            return jsonify({'error': 'Failed to translate text'})
    else:
        return jsonify({'error': 'Recognized text or target language is missing'})

def translate_text(text, target_language):
    try:
        result = translator.translate(text, dest=target_language)
        return result.text if result else None
    except Exception as e:
        print(f"Translation Error: {e}")
        return None

def play_translated_audio(translated_text, target_language):
    try:
        tts = gTTS(translated_text, lang=target_language)
        audio_file = 'translated_audio.mp3'
        tts.save(audio_file)
        playsound(audio_file)
        os.remove(audio_file)
    except Exception as e:
        print(f"Audio Playback Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
