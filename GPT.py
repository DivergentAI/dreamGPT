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

def chat_complete(prompt, model="gpt-4", max_tokens=100):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = response.choices[0].text.strip()
    return message

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
