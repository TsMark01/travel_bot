from token import *
import requests
from config import TOKENIZE_URL, GPT_MODEL, GPT_URL
from super_secret import *

def count_gpt_tokens(messages):
    """Count the number of tokens in the given messages using Yandex GPT API."""
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{folder_id}/yandexgpt-lite",
        "messages": messages
    }
    try:
        response = requests.post(url=TOKENIZE_URL, json=data, headers=headers).json()['tokens']
        return len(response)
    except Exception as e:
        print(e)
        return 0

def ask_gpt(SYSTEM_PROMPT):
    """Generate a response using Yandex GPT API with the provided prompt."""
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{folder_id}/{GPT_MODEL}",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": 300
        },
        "messages": SYSTEM_PROMPT
    }
    try:
        response = requests.post(GPT_URL, headers=headers, json=data)
        if response.status_code != 200:
            return False, f"GPT error. Status code: {response.status_code}", None
        answer = response.json()['result']['alternatives'][0]['message']['text']
        tokens_in_answer = count_gpt_tokens([{'role': 'assistant', 'text': answer}])
        return True, answer, tokens_in_answer
    except Exception as e:
        print(e)
        return False, "Error communicating with GPT", None



