import tkinter as tk
from tkinter import scrolledtext
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


def log_update_and_speak(log, title, text, title_tag, text_tag, engine):
    log.insert(tk.END, title, title_tag)
    log.insert(tk.END, text + "\n", text_tag)
    log.yview(tk.END)  # Auto-scroll to the end
    root.update()  # Update the GUI
    # Speak only if the text is from the assistant
    if title == "Assistant: ":
        speak(text, engine)


def handle_text_input(engine, log):
    text = input_entry.get()
    log_update_and_speak(log, "You said: ", text,
                         'user_label', 'user_text', engine)
    if text.lower() == 'quit':
        log_update_and_speak(log, "Assistant: ", "Thank you",
                             'assistant_label', 'assistant_text', engine)
        return 'quit'
    elif text.lower() == 'switch to voice':
        show_voice_interface()
        return 'voice'
    else:
        response = assistant(text)
        log_update_and_speak(log, "Assistant: ", response,
                             'assistant_label', 'assistant_text', engine)
        input_entry.delete(0, tk.END)
    return 'text'


def handle_voice_input(engine, recognizer, log):
    with sr.Microphone() as source:
        log_update_and_speak(log, "Listening...\n", "",
                             'assistant_label', 'assistant_text', engine)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            log_update_and_speak(log, "You said: ", text,
                                 'user_label', 'user_text', engine)
            if 'quit' in text.lower():
                log_update_and_speak(
                    log, "Assistant: ", "Thank you", 'assistant_label', 'assistant_text', engine)
                return 'quit'
            if 'switch to text' in text.lower():
                show_text_interface()
                return 'text'

            response = assistant(text)
            log_update_and_speak(log, "Assistant: ", response,
                                 'assistant_label', 'assistant_text', engine)
        except sr.UnknownValueError:
            log_update_and_speak(log, "Assistant: ", "Sorry, I could not understand what you said.",
                                 'assistant_label', 'assistant_text', engine)
        except sr.RequestError as e:
            log_update_and_speak(
                log, "Assistant: ", f"Could not request results; {e}", 'assistant_label', 'assistant_text', engine)


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

# Log area with different colors and styles for user and assistant
log_text = scrolledtext.ScrolledText(
    frame, width=40, height=20, wrap=tk.WORD, bg="#ffffff", fg="#000000", font=("Calibri", 12))
log_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Create tags for different message types
log_text.tag_configure('user_label', foreground='#0000FF', font=(
    "Calibri", 12, "bold"))  # Blue and bold for user label
log_text.tag_configure('assistant_label', foreground='#FF0000', font=(
    "Calibri", 12, "bold"))  # Red and bold for assistant label
log_text.tag_configure('user_text', foreground='#0000FF', font=(
    "Calibri", 12))  # Blue for user text without bold
log_text.tag_configure('assistant_text', foreground='#FF0000', font=(
    "Calibri", 12))  # Red for assistant text without bold

# Text interface setup
text_frame = tk.Frame(root, bg="#f0f0f0")
input_entry = tk.Entry(text_frame, width=25, font=("Calibri", 12))
input_entry.pack(side=tk.LEFT, pady=5, padx=10, fill=tk.X, expand=True)

size = 35
# Load and resize the circular icon
original_image = Image.open("send_icon.png")
# Adjust to the desired button size
resized_image = original_image.resize((size, size))
send_icon = ImageTk.PhotoImage(resized_image)

# Create button with round image
send_button = tk.Button(text_frame, image=send_icon, command=lambda: handle_text_input(
    engine, log_text), bg="#f0f0f0", borderwidth=0, relief="flat", width=size, height=size)
send_button.pack(side=tk.RIGHT, padx=10)

# Voice interface setup
voice_frame = tk.Frame(root, bg="#f0f0f0")
listen_button = tk.Button(voice_frame, text="Click to Speak",
                          command=start_listening, bg="#FF5722", fg="#ffffff", font=("Calibri", 12))
listen_button.pack(pady=10)

# Switch button
switch_button = tk.Button(frame, text="Switch to Voice", command=show_voice_interface,
                          bg="#FFC107", fg="#000000", font=("Calibri", 12))
switch_button.pack(side=tk.BOTTOM, pady=10)

engine = voice_ai_init()
recognizer = sr.Recognizer()
mode = 'text'

show_text_interface()

root.mainloop()
