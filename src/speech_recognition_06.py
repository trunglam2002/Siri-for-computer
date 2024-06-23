import speech_recognition as sr
from excutive_duty_05 import assistant  # Ensure this module is accessible
import pyttsx3
import time
from application.app import timeout_duration


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
    last_activity_time = time.time()

    while True:
        current_time = time.time()
        if current_time - last_activity_time > timeout_duration:
            print("No activity detected. Exiting...")
            speak("No activity detected. Exiting...", engine)
            break

        with sr.Microphone() as source:
            print("Say something...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

        try:
            text = recognizer.recognize_google(audio)
            last_activity_time = time.time()  # Update last activity time
            if 'quit' in text:
                print("You said:", text)
                print("Thank you")
                speak("Thank you", engine)
                break

            if text:
                print("You said:", text)
                response = assistant(text)
                print("Assistant: " + response)
                speak(response, engine)
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            speak("Sorry, I could not understand what you said.", engine)
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))
            speak(
                "Could not request results from Google Speech Recognition service.", engine)
            break
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            break
        print()


if __name__ == "__main__":
    print(assistant('play chân ái'))
