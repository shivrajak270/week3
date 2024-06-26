import tkinter as tk
from tkinter import messagebox
from googletrans import Translator, LANGUAGES
import speech_recognition as sr
from gtts import gTTS
import tempfile
import playsound
import threading

# Function to translate text
def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Function to recognize speech and translate
def recognize_and_translate():
    global keep_running
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Adjust recognition parameters if needed
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language="auto")
        source_text_var.set(recognized_text)

        target_language = target_language_var.get()

        # Translate recognized text
        translated_text = translate_text(recognized_text, target_language)
        translated_text_var.set(translated_text)

        # Convert translated text to speech
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts = gTTS(text=translated_text, lang=target_language)
            tts.save(fp.name + ".mp3")
            playsound.playsound(fp.name + ".mp3", True)

    except sr.UnknownValueError:
        messagebox.showerror("Error", "Sorry, I could not understand the audio.")
    except sr.RequestError:
        messagebox.showerror("Error", "Could not request results; check your network connection.")
    finally:
        keep_running = False

# Function to start recognition and translation
def start_recognition():
    global keep_running
    keep_running = True
    recognition_thread = threading.Thread(target=recognize_and_translate)
    recognition_thread.start()

# Function to stop recognition and translation
def stop_recognition():
    global keep_running
    keep_running = False

# Function to populate language options
def populate_languages():
    for lang_code, lang_name in LANGUAGES.items():
        target_language_menu['menu'].add_command(label=lang_name, command=tk._setit(target_language_var, lang_code))

# Create the main window
root = tk.Tk()
root.title("Voice Language Translator")

# Variables
source_text_var = tk.StringVar()
translated_text_var = tk.StringVar()
target_language_var = tk.StringVar(value='en')  # Default to English
keep_running = False

# Create GUI elements
source_text_label = tk.Label(root, text="Source Text:")
source_text_entry = tk.Entry(root, textvariable=source_text_var, width=50, state='disabled')
translated_text_label = tk.Label(root, text="Translated Text:")
translated_text_entry = tk.Entry(root, textvariable=translated_text_var, width=50, state='disabled')
target_language_label = tk.Label(root, text="Target Language:")
target_language_menu = tk.OptionMenu(root, target_language_var, "")
populate_languages_button = tk.Button(root, text="Populate Languages", command=populate_languages)
start_button = tk.Button(root, text="Start", command=start_recognition)
stop_button = tk.Button(root, text="Stop", command=stop_recognition)

# Layout
source_text_label.grid(row=0, column=0, padx=10, pady=10)
source_text_entry.grid(row=0, column=1, padx=10, pady=10)
translated_text_label.grid(row=1, column=0, padx=10, pady=10)
translated_text_entry.grid(row=1, column=1, padx=10, pady=10)
target_language_label.grid(row=2, column=0, padx=10, pady=10)
target_language_menu.grid(row=2, column=1, padx=10, pady=10)
populate_languages_button.grid(row=3, column=0, padx=10, pady=10)
start_button.grid(row=3, column=1, padx=10, pady=10)
stop_button.grid(row=3, column=2, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
