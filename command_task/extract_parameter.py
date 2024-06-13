import re
from application.app import *


def extract_parameters(intent, user_input):
    if intent == 'control_computer':
        if 'off' in user_input.lower():
            return 'turn off'
        elif 'restart' in user_input.lower():
            return 'restart'

    elif intent == 'manage_applications':
        if 'open' in user_input.lower():
            if 'chrome' in user_input.lower():
                # Check if there's a search query
                search_match = re.search(
                    r"(?:search|find) ([\w\s]+)", user_input.lower())
                if search_match:
                    search_query = search_match.group(1)
                    return ('open', 'chrome', search_query)
                else:
                    link = link_app_chrome.get('chrome', None)
                    return ('open', 'chrome', link)
            for app_chr in app_chrome:
                if app_chr.lower() in user_input.lower():
                    link = link_app_chrome.get(app_chr, None)
                    return ('open', 'chrome', link)

            for app_com in app_comp:
                if app_com.lower() in user_input.lower():
                    return ('open', app_com, None)
            # Nếu không khớp với bất kỳ ứng dụng nào
            return ('nothing', 'None', '')
        elif 'close' in user_input.lower():
            # edit later
            if 'chrome' in user_input.lower():
                return ('close', 'chrome', '')
            # Nếu không khớp với bất kỳ ứng dụng nào
            return ('nothing', 'None', '')

    elif intent == 'search_information':
        # Toàn bộ đầu vào của người dùng được xem xét là truy vấn cho đến khi cải thiện
        return user_input
    return ('nothing', 'None', '')
