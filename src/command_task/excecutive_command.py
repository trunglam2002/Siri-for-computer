from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import requests
from application.app import *
from application.command import *
import os
import webbrowser
import psutil
import re
from pywinauto import Desktop
import time
import re
import subprocess
from pytube import YouTube
from youtube_search import YoutubeSearch
from datetime import timedelta


webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


def reverse_lookup(dictionary, value):
    """
    Truy vấn ngược từ giá trị đến khóa trong từ điển.
    """
    for key, val in dictionary.items():
        if val == value:
            return key
    return None


def nothing():
    return "Sorry, I can't perform that action."


def control_computer(action):
    # if action.lower() == 'turn off':
    #     os.system("shutdown /s /t 1")  # Shutdown command
    #     return "Turning off computer..."
    # elif action.lower() == 'restart':
    #     os.system("shutdown /r /t 1")  # Restart command
    #     return "Restarting computer..."
    # else:
    return "Sorry, I can't perform that action for the computer."


def manage_applications(action, app_name, query=None):
    if manage_application['open'] == 1:
        if action.lower() == 'open':
            # Mở Google Chrome và tìm kiếm trên Google nếu có query
            if query:
                if 'https://' in query.lower():
                    # Mở liên kết trực tiếp
                    webbrowser.get("chrome").open(query)
                    return f"Opening {reverse_lookup(link_app_chrome, query)}"
                else:
                    url = f"https://www.google.com/search?q={query}"
                    webbrowser.get("chrome").open(url)
                    return f"Opening Google Chrome"
            else:
                # Mở ứng dụng cụ thể
                os.system(f"start {app_name}")  # Command to open application
                return f"Opening application: {app_name}"

    if manage_application['close'] == 1:
        # đóng tab (check xem tiến trình có chạy không trước khi đóng)
        if action.lower() == 'close':
            if app_name == 'chrome':
                if query:
                    for app_chr in app_chrome:
                        if app_chr.lower() in query.lower():
                            is_run = close_chrome_tab(app_chr.lower())
                            if is_run:
                                return f'Close {app_chr} successful'
                            else:
                                return f'{app_chr} is not running'
                else:
                    is_run = close_chrome()
                    if is_run:
                        return 'Close Chrome successful'
                    else:
                        return 'Chrome is not running'
            else:
                # Kiểm tra xem tiến trình có đang chạy hay không
                check_process = os.popen(
                    f'tasklist /FI "IMAGENAME eq {app_name}.exe" 2>NUL | find /I /N "{app_name}.exe"').read()
                if f"{app_name}.exe" in check_process:
                    # Đóng ứng dụng cụ thể
                    os.system(f"taskkill /IM {app_name}.exe /F")
                    return f"Closing application: {app_name}"
                else:
                    return f"Application {app_name} is not running."

    if manage_application['write'] == 1:
        if action.lower() == 'write':
            write_to_notepad(query, notepad_path)
            return "Open notepad and write successful"

    return "Sorry, I can't perform that action for applications."


user = "User:"
bot = "Bot:"
conversation_history = []


def get_prompt(user_msg):
    return {
        "prompt": f"You are a helpful AI assistant named Miku. You always respond in English and your personality is playful, cheerful, friendly. {user_msg}",
        "use_story": False,
        "use_memory": True,
        "use_authors_note": False,
        "use_world_info": False,
        "max_context_length": 2048,
        "max_length": 150,
        "rep_pen": 1.05,
        "rep_pen_range": 2048,
        "rep_pen_slope": 0.7,
        "temperature": 0.7,
        "tfs": 0.95,
        "top_a": 0.85,
        "top_k": 40,
        "top_p": 0.9,
        "typical": 0.2,
        "sampler_order": [0, 1, 3, 4, 5, 2, 6],
        "singleline": False,
        "sampler_seed": 42,
        "sampler_full_determinism": False,
        "frmttriminc": True,
        "frmtrmblln": True,
        "stop_sequence": ["\n\n\n\n\n", f"{user}"]
    }


def search_information(query):
    if search_information['chatbot'] == 1:
        try:
            user_message = query

            # Add all of conversation history if it exists and add User and Bot names
            fullmsg = f"{''.join(conversation_history)}{user} {user_message}\n{bot} "
            prompt = get_prompt(fullmsg)
            response = requests.post(f"{ENDPOINT}/v1/generate", json=prompt)

            if response.status_code == 200:
                results = response.json()['results']
                text = results[0]['text']
                if text == '':
                    return "Sorry i can answer the question"
                response_text = text.split('\n')[0].replace("  ", " ")
                if response_text not in conversation_history:
                    conversation_history.append(
                        f"{user} {user_message}\n{bot} {response_text}\n")
                return response_text
            else:
                return f"An error occurred: {response.status_code} {response.text}"

        except Exception as e:
            return f"An error occurred: {e}"
    return "Sorry, I can't perform that action"


def terminate_previous_vlc():
    # Iterate through all running processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Check if the process name contains 'vlc' (case insensitive)
            if 'vlc' in proc.name().lower():
                # Terminate the VLC process and its children
                parent = psutil.Process(proc.pid)
                for child in parent.children(recursive=True):
                    child.terminate()
                parent.terminate()
                print(f"Terminated VLC process with PID {proc.pid}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        except Exception as e:
            print(f"Error terminating process: {e}")
            return ("Error terminating process")


def play_music(parameters):

    if manage_application['play_music'] == 1:
        if parameters == 'continue music':
            return 'To continue the music, press Ctrl F11 or anykey depend on your setting in Tool Preference Hotkey in VLC'
        try:
            # Tìm kiếm video trên YouTube và sắp xếp theo số lượt xem cao nhất
            results = YoutubeSearch(parameters, max_results=5).to_dict()

            # Chọn video có số lượt xem cao nhất từ kết quả tìm kiếm
            if results:
                def get_views(view_count):
                    # Hàm chuyển đổi số lượt xem từ dạng string sang int
                    return int(re.sub(r'\D', '', view_count))

                # Sắp xếp kết quả theo số lượt xem (lớn đến nhỏ)
                sorted_results = sorted(
                    results, key=lambda x: get_views(x['views']), reverse=True)

                # Lấy URL của video có số lượt xem cao nhất
                top_video = sorted_results[0]
                video_url = f"https://www.youtube.com{top_video['url_suffix']}"

                # Sử dụng pytube để lấy thông tin chi tiết về video
                yt_video = YouTube(video_url)
                print("Video information:")
                print("Title:", yt_video.title)
                print("Duration:", str(timedelta(seconds=yt_video.length)))

                # Lấy URL của luồng phát video và âm thanh chất lượng cao nhất
                stream = yt_video.streams.filter(
                    progressive=True, file_extension='mp4').first()
                video_url = stream.url

                # Kết thúc tiến trình VLC trước nếu có
                terminate_previous_vlc()

                # Sử dụng subprocess để chạy VLC trong nền
                current_vlc_process = subprocess.Popen([vlc_path, video_url])
                return "Started playing video in the background."

            else:
                return "No suitable results found."

        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred while processing. Please try again later."

    else:
        return "Sorry, I can't perform that action."


def stop_music():
    return 'To stop music, press Ctrl F12 or anykey depend on your setting in Tool Preference Hotkey in VLC'


def change_volume(parameters):
    if manage_application['change_volume'] == 1:
        parameters = int(parameters)/100
        try:
            # Kiểm tra nếu tham số parameters không nằm trong khoảng từ 0 đến 1
            if not 0 <= parameters <= 100:
                return "Input volume should be in range 0 and 100"

            # Lấy danh sách tất cả các sessions âm thanh đang chạy
            sessions = AudioUtilities.GetAllSessions()

            # Duyệt qua từng session và điều chỉnh âm lượng
            for session in sessions:
                volume_object = session._ctl.QueryInterface(ISimpleAudioVolume)
                volume_object.SetMasterVolume(parameters, None)

            return f"System volume set to {int(parameters * 100)}%"

        except TypeError as e:
            print(f"Error while setting volume: {str(e)}")
            return f"Error while setting volume"


def close_chrome_tab(app_chr):
    pattern = r"^.*?-(.*?)-(.*?)-"

    # Kết nối đến cửa sổ Chrome
    desktop = Desktop(backend="uia")
    chrome_window = desktop.window(
        title_re=".* Google Chrome$", control_type="Pane")

    # Tìm tất cả các tab trong cửa sổ Chrome
    tabs = chrome_window.descendants(control_type="TabItem")

    # Xác định tab YouTube và đóng nó
    for tab in tabs:
        # in các tiến trình đang chạy trên chrome
        # print(tab.window_text)
        try:
            match = re.match(pattern, str(tab.window_text))
            if match:
                if app_chr in match.group(2).lower() or (app_chr in match.group(1).lower() and "usage" in match.group(2).lower()):
                    chrome_window.set_focus()
                    tab.click_input(double=True)  # Đảm bảo tab được chọn
                    time.sleep(1)  # Đợi để đảm bảo tab đã được chọn
                    tab.type_keys("^w")  # Đóng tab
                    return True

        except Exception as e:
            # Tiếp tục vòng lặp
            print(f"Lỗi: {e}")
            continue

    return False


def is_chrome_running():
    # Kiểm tra tất cả các tiến trình đang chạy
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'chrome.exe':
            return True
    return False


def close_chrome():
    if is_chrome_running():
        os.system("taskkill /IM chrome.exe /F")
        return True
    return False


def write_to_notepad(text, directory):
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Base filename and extension
    base_filename = "output"
    extension = ".txt"
    counter = 1

    # Determine the filename
    while True:
        filename = os.path.join(
            directory, f"{base_filename}{counter}{extension}")
        if not os.path.exists(filename):
            break
        counter += 1

    # Open the file in write mode and write the text
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)

    # Open the file with Notepad in a non-blocking way
    subprocess.Popen(["notepad.exe", filename])
