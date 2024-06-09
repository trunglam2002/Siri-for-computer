import os
import webbrowser

# Đăng ký Google Chrome
# Đảm bảo đường dẫn này đúng với hệ thống của bạn
chrome_path = "C://Program Files//Google//Chrome//Application//chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


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


# Ví dụ sử dụng
# print(manage_applications('open', 'notepad'))  # Mở notepad
# Tìm kiếm 'OpenAI' trên Google
print(manage_applications('open', '', 'Obama'))
