import requests

user = "User:"
bot = "Bot:"
ENDPOINT = "https://farming-freebsd-created-vacations.trycloudflare.com/api"
conversation_history = []


def get_prompt(user_msg):
    return {
        "prompt": f"You are a helpful AI assistant named Miku. You always respond in English and your personality is playful, cheerful, friendly. {user_msg}",
        "use_story": False,
        "use_memory": True,
        "use_authors_note": False,
        "use_world_info": False,
        "max_context_length": 2048,
        "max_length": 150,
        "rep_pen": 1.05,
        "rep_pen_range": 2048,
        "rep_pen_slope": 0.7,
        "temperature": 0.7,
        "tfs": 0.95,
        "top_a": 0.85,
        "top_k": 40,
        "top_p": 0.9,
        "typical": 0.2,
        "sampler_order": [0, 1, 3, 4, 5, 2, 6],
        "singleline": False,
        "sampler_seed": 42,
        "sampler_full_determinism": False,
        "frmttriminc": True,
        "frmtrmblln": True,
        "stop_sequence": ["\n\n\n\n\n", f"{user}"]
    }


while True:
    try:
        user_message = input(f"{user} ")
        print(user_message)
        if len(user_message.strip()) < 1:
            print(f"{bot} Please provide a valid input.")
            continue

        # Add all of conversation history if it exists and add User and Bot names
        fullmsg = f"{''.join(conversation_history)}{user} {user_message}\n{bot} "
        prompt = get_prompt(fullmsg)
        response = requests.post(f"{ENDPOINT}/v1/generate", json=prompt)

        if response.status_code == 200:
            results = response.json()['results']
            text = results[0]['text']
            response_text = text.split('\n')[0].replace("  ", " ")
            if response_text not in conversation_history:
                conversation_history.append(
                    f"{user} {user_message}\n{bot} {response_text}\n")
            print(f"{bot} {response_text}")
        else:
            print(f"An error occurred: {response.status_code} {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")
