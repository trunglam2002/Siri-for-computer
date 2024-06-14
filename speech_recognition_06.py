import speech_recognition as sr
from excutive_duty_05 import assistant
import pyttsx3


def voice_ai_init():
    # Khởi tạo text-to-speech engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Thiết lập giọng nói (ví dụ: chọn giọng nữ thứ 2 trong danh sách)
    engine.setProperty('voice', voices[1].id)
    return engine


def speak(text, engine):
    engine.say(text)
    engine.runAndWait()


def voice_assistant():
    engine = voice_ai_init()
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        if text:
            print("You said:", text)
            response = assistant(text)
            # Pass the initialized engine object here
            speak("Assistant: " + response, engine)
            return response
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        speak("Sorry, I could not understand what you said.", engine)
        return None
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))
        speak("Could not request results from Google Speech Recognition service.", engine)
        return None


print(assistant('close Instagram'))
