import os
import webbrowser

chrome_path = "C://Program Files//Google//Chrome//Application//chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


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
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.get("chrome").open(url)
            return f"Opening Google Chrome and searching for: {search_query}"
        else:
            # Mở ứng dụng cụ thể
            os.system(f"start {app_name}")  # Command to open application
            return f"Opening application: {app_name}"
    elif action.lower() == 'close':
        # Đóng ứng dụng cụ thể
        # Command to close application
        os.system(f"taskkill /IM {app_name}.exe /F")
        return f"Closing application: {app_name}"
    else:
        return "Sorry, I can't perform that action for applications."


def search_information(query):
    # Placeholder for searching and answering information from the internet
    return f"Searching information for: {query}"
