import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3

from excutive_duty_05 import assistant
from application.app import timeout_duration


def voice_ai_init():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    return engine


def speak(text, engine):
    engine.say(text)
    engine.runAndWait()


def handle_text_input(engine, log):
    text = input_entry.get()
    log.insert(tk.END, "You said: " + text + "\n")
    if text.lower() == 'quit':
        log.insert(tk.END, "Thank you\n")
        speak("Thank you", engine)
        return 'quit'
    elif text.lower() == 'switch to voice':
        show_voice_interface()
        return 'voice'
    else:
        response = assistant(text)
        log.insert(tk.END, "Assistant: " + response + "\n")
        speak(response, engine)
        input_entry.delete(0, tk.END)
    return 'text'


def handle_voice_input(engine, recognizer, log):
    with sr.Microphone() as source:
        log.insert(tk.END, "Listening...\n")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            log.insert(tk.END, "You said: " + text + "\n")
            if 'quit' in text.lower():
                log.insert(tk.END, "Thank you\n")
                speak("Thank you", engine)
                return 'quit'
            if 'switch to text' in text.lower():
                show_text_interface()
                return 'text'

            response = assistant(text)
            log.insert(tk.END, "Assistant: " + response + "\n")
            speak(response, engine)
        except sr.UnknownValueError:
            log.insert(tk.END, "Sorry, I could not understand what you said.\n")
            speak("Sorry, I could not understand what you said.", engine)
        except sr.RequestError as e:
            log.insert(tk.END, f"Could not request results; {e}\n")
            speak("Could not request results.", engine)


def start_listening():
    handle_voice_input(engine, recognizer, log_text)


def show_text_interface():
    voice_frame.pack_forget()
    text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    switch_button.config(text="Switch to Voice", command=show_voice_interface)


def show_voice_interface():
    text_frame.pack_forget()
    voice_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    switch_button.config(text="Switch to Text", command=show_text_interface)


# GUI setup
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("360x640")  # Dimensions resembling a smartphone screen

# Frame for logs and input
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Log area
log_text = scrolledtext.ScrolledText(
    frame, width=40, height=20, wrap=tk.WORD, bg="#ffffff", fg="#000000", font=("Helvetica", 12))
log_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Text interface setup
text_frame = tk.Frame(root, bg="#f0f0f0")
input_entry = tk.Entry(text_frame, width=25, font=("Helvetica", 12))
input_entry.pack(side=tk.LEFT, pady=5, padx=10, fill=tk.X, expand=True)

size = 35
# Load and resize the circular icon
original_image = Image.open("send_icon.png")
# Adjust to the desired button size
resized_image = original_image.resize((size, size))
send_icon = ImageTk.PhotoImage(resized_image)

# Tạo nút với ảnh hình tròn
send_button = tk.Button(text_frame, image=send_icon, command=lambda: handle_text_input(
    engine, log_text), bg="#f0f0f0", borderwidth=0, relief="flat", width=size, height=size)
send_button.pack(side=tk.RIGHT, padx=10)

# Voice interface setup
voice_frame = tk.Frame(root, bg="#f0f0f0")
listen_button = tk.Button(voice_frame, text="Click to Speak",
                          command=start_listening, bg="#FF5722", fg="#ffffff", font=("Helvetica", 12))
listen_button.pack(pady=10)

# Switch button
switch_button = tk.Button(frame, text="Switch to Voice", command=show_voice_interface,
                          bg="#FFC107", fg="#000000", font=("Helvetica", 12))
switch_button.pack(side=tk.BOTTOM, pady=10)

engine = voice_ai_init()
recognizer = sr.Recognizer()
mode = 'text'

show_text_interface()

root.mainloop()
