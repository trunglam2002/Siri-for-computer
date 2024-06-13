from command_task.excecutive_command import *
from command_task.extract_parameter import *
import pickle

# Tải mô hình đã lưu từ tệp
with open('save_model_SVC/classify_duty.h5', 'rb') as file:
    model = pickle.load(file)

with open('save_model_SVC/count_vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

# Define intents and their corresponding functions
intents = {
    'control_computer': 'control_computer',
    'manage_applications': 'manage_applications',
    'search_information': 'search_information'
}

task_mapping = {
    'control_computer': control_computer,
    'manage_applications': manage_applications,
    'search_information': search_information
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


def assistant(user_input):
    intent = recognize_intent(user_input)
    parameters = extract_parameters(intent, user_input)
    print('Parameter:', parameters)
    return execute_task(intent, parameters)
