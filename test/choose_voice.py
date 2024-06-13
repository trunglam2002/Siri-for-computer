import pyttsx3

# Khởi tạo text-to-speech engine
engine = pyttsx3.init()

# Lấy danh sách các giọng nói có sẵn
voices = engine.getProperty('voices')

# Hiển thị danh sách giọng nói
for i, voice in enumerate(voices):
    print(f"Voice {i}: {voice.name}, {voice.gender}, {voice.id}")

# Thiết lập giọng nói (ví dụ: chọn giọng nữ thứ 2 trong danh sách)
engine.setProperty('voice', voices[0].id)

# Thay đổi tốc độ nói (tốc độ mặc định là 200)
engine.setProperty('rate', 150)  # Giảm tốc độ nói

# Thay đổi âm lượng (âm lượng mặc định là 1.0)
engine.setProperty('volume', 0.9)  # Giảm âm lượng một chút


def speak(text):
    engine.say(text)
    engine.runAndWait()


# Ví dụ sử dụng
if __name__ == "__main__":
    speak("Hello, how are you?")
    speak("I am an AI assistant with a female voice.")
