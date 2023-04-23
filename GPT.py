import itertools
import json
import random

import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_API_KEY=os.environ.get('SECRET_KEY')
INIT_IDEA_SIZE = 4
MIX_IDEA_SIZE = 4
STORAGE = []

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


def get_combinations(ideas):

    all_combinations = list(itertools.combinations(ideas, 2))

    if MIX_IDEA_SIZE > len(all_combinations):
        print("Number of desired combinations exceeds the total possible combinations.")
        return all_combinations

    return all_combinations[:MIX_IDEA_SIZE]

def send_data(data):
    ...

def sort_by_score(ideas):
    ...

def parse_json():
    ...

def step3(mixed_ideas):
    """
    Evaluate, rank & evaluate best results
    :return:
    """
    evaluated_mixed_ideas = []
    for _ in mixed_ideas:
        prompt = """
        Given the following JSON add a score (0 to 10) in the following format and evaluate the idea in terms of how easy it is to implement, how useful it is to humanity, and how innovative it is

        "score": {
          "implementation" ...
          "usefulness": ...
          "innovation": ...
        }
        """ + json.dumps(mixed_ideas)
        compelition_raw = chat_complete(prompt)
        compelition = parse_json(compelition_raw)
        evaluated_mixed_ideas.append(compelition)
    best_ideas = sort_by_score(evaluated_mixed_ideas)[:len(mixed_ideas)//2]
    return best_ideas

def step2(ideas, priv_best_ideas=[]):
    """
    Combine ideas
    :return:
    """
    combinations = get_combinations(ideas+priv_best_ideas)
    mixed_ideas = []
    for _ in combinations:
        prompt = """
        Given the following JSON, create a single item which takes both ideas and combines a single, coherent and useful idea. Output JSON in the same format. Output JSON only.
        
        [
          {
            "title": "Smart Traffic Lights",
            "description": "Develop a system of traffic lights that use sensors and AI to optimize traffic flow, reduce congestion, and improve safety on the road."
          },
          {
            "title": "Virtual Wardrobe",
            "description": "Create an app that allows users to upload pictures of their clothing and create virtual outfits, making it easier to plan outfits and reduce the environmental impact of fast fashion."
          }
        ]
        """
        compelition_raw = chat_complete(prompt)
        compelition = parse_json(compelition_raw)
        mixed_ideas.append(compelition)
    return mixed_ideas




def step1():
    """
    Generate N new ideas
    :return:
    """
    prompt = f"""
    Generate {INIT_IDEA_SIZE} ideas that are new and useful
        Reply in JSON with this format:
        [
          {
            "title": ...
            "description": ...
          }
        ]
    """
    compelition = chat_complete(prompt)
    return parse_json_list(compelition)




def execute_cycle(priv_best_ideas=[]):
    step1_compelition = step1()
    step2_compelition = step2(step1_compelition, priv_best_ideas)
    best_ideas = step3(step2_compelition)
    send_data(best_ideas)
    return best_ideas

def main():
    best_ideas = []
    while True:
       best_ideas = execute_cycle(best_ideas)


if __name__ == "__main__":
    prompt = "Insert prompt"
    response = chat_complete(input())
    
    print("Response:", response)
