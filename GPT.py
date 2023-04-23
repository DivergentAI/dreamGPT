import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def chat_complete(messages ,model="gpt-4"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
)
    return response

def chat_test():
    messages = [
        {"role": "system", "content": "You are a friendly neighbour GPT"},
        {"role": "user", "content": "Hi, neighbour"},
    ]
    print(chat_complete(messages))
""" Input Message structure
    [
        {"role": "system", "content": ""},
        {"role": "user", "content": ""},
        {"role": "assistant", "content": ""},
        {"role": "user", "content": ""}
    ]"""

""" Output Message structure
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "Hello! How are you today, neighbour? It's nice to see you. If you need any help or just want to chat, feel free to reach out!",
        "role": "assistant"
      }
    }
  ],
  "created": 1682279983,
  "id": "chatcmpl-78aA3nPI5sCkbD3PjyNDXcUbN79i9",
  "model": "gpt-4-0314",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 33,
    "prompt_tokens": 21,
    "total_tokens": 54
  }
}
"""

"""[
    {"title": String,
    "description": String,
    "score": float,
    }
]"""



if __name__ == "__main__":
    chat_test()
