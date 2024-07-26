import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import time
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
    text_frame.pack()


def show_voice_interface():
    text_frame.pack_forget()
    voice_frame.pack()


# GUI setup
root = tk.Tk()
root.title("Voice Assistant")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

log_text = scrolledtext.ScrolledText(frame, width=50, height=20, wrap=tk.WORD)
log_text.pack()

text_frame = tk.Frame(root)
input_entry = tk.Entry(text_frame, width=50)
input_entry.pack(side=tk.LEFT, pady=5)
send_button = tk.Button(text_frame, text="Send",
                        command=lambda: handle_text_input(engine, log_text))
send_button.pack(side=tk.RIGHT, padx=5)

voice_frame = tk.Frame(root)
listen_button = tk.Button(
    voice_frame, text="Click to Speak", command=start_listening)
listen_button.pack(pady=5)

switch_to_voice_button = tk.Button(
    frame, text="Switch to Voice", command=show_voice_interface)
switch_to_voice_button.pack(side=tk.LEFT, padx=5)

switch_to_text_button = tk.Button(
    frame, text="Switch to Text", command=show_text_interface)
switch_to_text_button.pack(side=tk.RIGHT, padx=5)

engine = voice_ai_init()
recognizer = sr.Recognizer()
mode = 'text'

show_text_interface()

root.mainloop()
