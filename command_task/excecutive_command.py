from application.app import *
import os
import webbrowser
import psutil
import subprocess
import re

chrome_path = "C://Program Files//Google//Chrome//Application//chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


def reverse_lookup(dictionary, value):
    """
    Truy vấn ngược từ giá trị đến khóa trong từ điển.
    """
    for key, val in dictionary.items():
        if val == value:
            return key
    return None


def control_computer(action):
    if action.lower() == 'turn off':
        os.system("shutdown /s /t 1")  # Shutdown command
        return "Turning off computer..."
    elif action.lower() == 'restart':
        os.system("shutdown /r /t 1")  # Restart command
        return "Restarting computer..."
    else:
        return "Sorry, I can't perform that action for the computer."


def manage_applications(action, app_name, search_query=None):
    if action.lower() == 'open':
        # Mở Google Chrome và tìm kiếm trên Google nếu có search_query
        if search_query:
            if 'https://' in search_query.lower():
                # Mở liên kết trực tiếp
                webbrowser.get("chrome").open(search_query)
                return f"Opening {reverse_lookup(link_app_chrome, search_query)}"
            else:
                url = f"https://www.google.com/search?q={search_query}"
                webbrowser.get("chrome").open(url)
                return f"Opening Google Chrome"
        else:
            # Mở ứng dụng cụ thể
            os.system(f"start {app_name}")  # Command to open application
            return f"Opening application: {app_name}"

    # đóng tab (check xem tiến trình có chạy không trước khi đóng)
    elif action.lower() == 'close':
        if search_query:
            if app_name.lower() == 'chrome':
                if search_query is None:
                    close_chrome()
                    return f"Closing Google Chrome successful"
                for app_chr in app_chrome:
                    if app_chr.lower() == search_query.lower():
                        check_tab = close_chrome_tab(app_chr)
                        if check_tab == True:
                            return f"Closing {app_chr} successful"
                        else:
                            return f"{app_chr} not found or already closed."
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
    else:
        return "Sorry, I can't perform that action for applications."


def search_information(query):
    # Placeholder for searching and answering information from the internet
    return f"Searching information for: {query}"


def find_process_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == name:
            return proc
    return None


def close_chrome_tab(tab_name):
    tab_found = False
    tabs = get_chrome_tabs()
    for tab in tabs:
        if tab_name.lower() in tab.lower():
            for process in psutil.process_iter(['pid', 'name', 'cmdline']):
                if process.info['name'] == 'chrome.exe' and process.info['cmdline']:
                    cmdline = ' '.join(process.info['cmdline'])
                    if tab in cmdline:
                        pid = process.info['pid']
                        os.system(f'taskkill /F /PID {pid}')
                        tab_found = True

        # Lấy và in ra danh sách các tab của Chrome hiện tại
    chrome_tabs = get_chrome_tabs()
    print("Current Chrome tabs:")
    for tab in chrome_tabs:
        print(tab)

    return tab_found


def get_chrome_tabs():
    chrome_tabs = []
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['name'] == 'chrome.exe' and process.info['cmdline']:
            cmdline = ' '.join(process.info['cmdline'])
            match = re.search(r'--profile-directory=([\w-]+)', cmdline)
            if match:
                profile_directory = match.group(1)
                chrome_tabs.append(profile_directory)
    return chrome_tabs


def close_chrome():
    os.system("taskkill /IM chrome.exe /F")
