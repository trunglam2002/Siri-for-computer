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

chrome_path = "C://Program Files//Google//Chrome//Application//chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

notepad_path = 'C:/Users/NgLaam/Desktop/notepad.exe'


def reverse_lookup(dictionary, value):
    """
    Truy vấn ngược từ giá trị đến khóa trong từ điển.
    """
    for key, val in dictionary.items():
        if val == value:
            return key
    return None


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


def search_information(query):
    # Placeholder for searching and answering information from the internet
    return f"Searching information for: {query}"


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
