import re

app = ['Youtube', 'Chrome', 'Facebook', 'Instagram']


def extract_parameters(intent, user_input):
    if intent == 'control_computer':
        if 'off' in user_input.lower():
            return 'turn off'
        elif 'restart' in user_input.lower():
            return 'restart'
    elif intent == 'manage_applications':
        for application in app:
            if application.lower() in user_input.lower():
                if 'open' in user_input.lower():
                    # Check if there's a search query
                    search_match = re.search(
                        r"(?:search|find) ([\w\s]+)", user_input.lower())
                    if search_match:
                        search_query = search_match.group(1)
                        return ('open', 'chrome', search_query)
                    else:
                        return ('open', application, '')
                elif 'close' in user_input.lower():
                    return ('close', application, '')
        return ('nothing', 'None', '')
    elif intent == 'search_information':
        return user_input  # The entire user input is considered as the query for now
    return user_input  # Default to whole input if specific extraction isn't implemented
