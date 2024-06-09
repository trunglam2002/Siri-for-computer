import os


def control_computer(action):
    # if action.lower() == 'turn off':
    #     os.system("shutdown /s /t 1")  # Shutdown command
    #     return "Turning off computer..."
    # elif action.lower() == 'restart':
    #     os.system("shutdown /r /t 1")  # Restart command
    return "Restarting computer..."
    # else:
    #     return "Sorry, I can't perform that action for the computer."


def manage_applications(action, app_name):
    # if action.lower() == 'open':
    #     os.system(f"start {app_name}")  # Command to open application
    #     return f"Opening application: {app_name}"
    # elif action.lower() == 'close':
    #     os.system(f"taskkill /IM {app_name}.exe /F")  # Command to close application
    return f"Closing application: {app_name}"
    # else:
    #     return "Sorry, I can't perform that action for applications."


def search_information(query):
    # Placeholder for searching and answering information from the internet
    return f"Searching information for: {query}"
