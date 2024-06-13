from application.app import *
import os
import webbrowser

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
    # if action.lower() == 'turn off':
    #     os.system("shutdown /s /t 1")  # Shutdown command
    #     return "Turning off computer..."
    # elif action.lower() == 'restart':
    #     os.system("shutdown /r /t 1")  # Restart command
    return "Restarting computer..."
    # else:
    #     return "Sorry, I can't perform that action for the computer."


def manage_applications(action, app_name, search_query=None):
    if action.lower() == 'open':
        # Mở Google Chrome và tìm kiếm trên Google nếu có search_query
        if search_query:
            if 'https://' in search_query.lower():
                # Mở liên kết trực tiếp
                webbrowser.get("chrome").open(search_query)
                return f"Opening link: {reverse_lookup(link_app_chrome, search_query)}"
            else:
                url = f"https://www.google.com/search?q={search_query}"
                webbrowser.get("chrome").open(url)
                return f"Opening Google Chrome"
        else:
            # Mở ứng dụng cụ thể
            os.system(f"start {app_name}")  # Command to open application
            return f"Opening application: {app_name}"
    elif action.lower() == 'close':
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
