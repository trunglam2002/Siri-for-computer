import pyttsx3
import speech_recognition as sr

# Khởi tạo text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Thiết lập giọng nói (ví dụ: chọn giọng nữ thứ 2 trong danh sách)
engine.setProperty('voice', voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()

# Hàm nhận diện giọng nói và phản hồi


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        speak("Sorry, I could not understand what you said.")
        return None
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))
        speak("Could not request results from Google Speech Recognition service.")
        return None


# Ví dụ sử dụng
if __name__ == "__main__":
    text = recognize_speech()
    if text:
        response = f"You said: {text}"
        print(response)
        speak(response)
