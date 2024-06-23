import pickle
from command_task.extract_parameter import *
from command_task.excecutive_command import *

# Tải mô hình đã lưu từ tệp
with open('save_model_SVC/classify_duty.h5', 'rb') as file:
    model = pickle.load(file)

with open('save_model_SVC/count_vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

# Define intents and their corresponding functions
intents = {
    'control_computer': 'control_computer',
    'manage_applications': 'manage_applications',
    'search_information': 'search_information',
    'play_music': 'play_music',
    'stop_music': 'stop_music',
    'change_volume': 'change_volume',
}

task_mapping = {
    'control_computer': control_computer,
    'manage_applications': manage_applications,
    'search_information': search_information,
    'play_music': play_music,
    'stop_music': stop_music,
    'change_volume': change_volume,
}


def recognize_intent(user_input):
    # candidate_labels = list(intents.keys())
    user_input_transform = vectorizer.transform([user_input])
    result = model.predict(user_input_transform)
    return result  # Most likely intent


def execute_task(intent, parameters):
    if intent == 'control_computer':
        return control_computer(parameters)
    elif intent == 'manage_applications':
        action, app_name, query = parameters
        return manage_applications(action, app_name, query)
    elif intent == 'search_information':
        return search_information(parameters)
    elif intent == 'play_music':
        return play_music(parameters)
    elif intent == 'stop_music':
        return stop_music()
    elif intent == 'change_volume':
        return change_volume(parameters)
    return nothing()


def assistant(user_input):
    intent = recognize_intent(user_input)
    parameters = extract_parameters(intent, user_input)
    print('Parameter:', parameters)
    return execute_task(intent, parameters)
