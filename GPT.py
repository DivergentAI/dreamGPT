import itertools
import json
import random

import openai
import os
from dataclasses import dataclass
# from dotenv
from typing import Optional, List
from colorama import Fore, Style
# from pydantic import BaseModel
# load_dotenv()

# TODO: put your api key here
openai.api_key = ""
INIT_IDEA_SIZE = 4
MIX_IDEA_SIZE = 4
STORAGE = []

CONTEXT_PROMPT = """
    An Innovator is someone who is creative and has the ability to think outside the box. 
    They also have strong problem-solving skills, along with knowledge of research and development, 
    business development, and market analysis. Additionally, they have the determination and resilience 
    to overcome obstacles, and the communication skills to effectively collaborate with others.
    
    You are an Innovator agent. You will research the market, identify potential customers and competitors, 
    and explore new technologies and trends.
    """
GENERATE_PROMPT = f"""
You will brainstorm and develop creative concepts and ideas that could potentially be used to 
develop a new product, service, or business model. Generate {INIT_IDEA_SIZE} ideas that are new and useful.
Reply in JSON with this format:
[
  {{
    "title": ...
    "description": ...
  }}
]
"""
EXAMPLE_GENERATION = """
[
    {
      "title": "Smart Home Garden",
      "description": "A device that can be used to grow plants indoors using hydroponics and AI. The device will be able to detect the needs of the plants and adjust the environment accordingly. It will also be able to connect to a smartphone app, where users can monitor and control the device."
    },
    {
      "title": "Virtual Personal Stylist",
      "description": "A virtual assistant that uses AI to recommend clothing and accessories based on a person's preferences, body type, and occasion. The assistant will take into account the user's budget and suggest items from different brands and retailers."
    },
    {
      "title": "Smart Recycling Bin",
      "description": "A recycling bin that can detect and sort different types of waste using computer vision and machine learning. The bin will also be able to compress the waste and notify the user when it needs to be emptied. The data collected can be used to optimize waste management and recycling programs."
    },
    {
      "title": "Virtual Language Tutor",
      "description": "An AI-powered language tutor that can interact with users in real-time, providing personalized feedback and coaching. The tutor will use natural language processing to understand the user's speech and provide real-time corrections and suggestions. It will also be able to adapt to the user's learning style and pace."
    }
]
"""
GENERATE_MESSAGE = [
    {"role": "system", "content": CONTEXT_PROMPT},
    {"role": "user", "content": GENERATE_PROMPT},
    {"role": "assistant", "content": EXAMPLE_GENERATION},
    {"role": "user", "content": GENERATE_PROMPT}
]

COMBINE_PROMPT = """
Given the following JSON, create a single item which takes both ideas and combines a single, 
coherent and useful idea. Output JSON in the same format. Output JSON only.
[
    {
      "title": "Smart Home Garden",
      "description": "A device that can be used to grow plants indoors using hydroponics and AI. The device will be able to detect the needs of the plants and adjust the environment accordingly. It will also be able to connect to a smartphone app, where users can monitor and control the device."
    },
    {
        "title": "Virtual Personal Stylist",
        "description": "A virtual assistant that uses AI to recommend clothing and accessories based on a person's preferences, body type, and occasion. The assistant will take into account the user's budget and suggest items from different brands and retailers."
      },
]
"""

COMBINE_RESPONSE = """
[
    {
      "title": "Smart Wardrobe",
      "description": "A device that combines a smart home garden and a virtual personal stylist. The device will be able to recommend clothing and accessories based on a person's preferences, body type, and occasion. It will also be able to grow plants indoors using hydroponics and AI, which can be used to make natural dyes or fabrics. The device will connect to a smartphone app where users can monitor and control the device."
    }
]
"""


def combine_complete(title_1, description_1, title_2, description_2):
    combine_prompt_use = f"""
    Given the following JSON, create a single item which takes both ideas and combines a single, 
    coherent and useful idea. Output JSON in the same format. Output JSON only.
    [
      {{
        "title": "{title_1}",
        "description": "{description_1}"
        }},
        {{
          "title": "{title_2}",
          "description": "{description_2}"
        }},
    ]
"""
    combine_message = [
        {"role": "system", "content": CONTEXT_PROMPT},
        {"role": "user", "content": COMBINE_PROMPT},
        {"role": "assistant", "content": COMBINE_RESPONSE},
        {"role": "user", "content": combine_prompt_use}
    ]
    return combine_message


RANK_PROMPT = """
Respond with JSON data only!!!
Given the following JSON add a score (0 to 10) in the following format and evaluate the idea in
 terms of how easy it is to implement, how useful it is to humanity, and how innovative it is

"score": {
  "implementation" ...
  "usefulness": ...
  "innovation": ...
}

    {
      "title": "Smart Home Recycling System",
      "description": "A device that combines a smart home garden and a smart recycling bin. The device will be able to detect and sort different types of waste using computer vision and machine learning. It will also be able to grow plants indoors using hydroponics and AI, which can be used to compost organic waste. The device will connect to a smartphone app where users can monitor and control the device and optimize their recycling and gardening efforts."
    }
"""

RANK_RESPONSE = """
    {
      "title": "Smart Wardrobe",
      "description": "A device that combines a smart home garden and a virtual personal stylist. The device will be able to recommend clothing and accessories based on a person's preferences, body type, and occasion. It will also be able to grow plants indoors using hydroponics and AI, which can be used to make natural dyes or fabrics. The device will connect to a smartphone app where users can monitor and control the device.",
      "score": {
        "implementation": 8,
        "usefulness": 9,
        "innovation": 7
      }
    }
"""


def rank_complete(entity):
    rank_prompt_use = f"""
    Respond with JSON data only!!!
    Given the following JSON add a score (0 to 10) in the following format and evaluate the idea in
    terms of how easy it is to implement, how useful it is to humanity, and how innovative it is
    
    "score": {{
      "implementation" ...
      "usefulness": ...
      "innovation": ...
    }}

    {{
      "title": {entity.title},
      "description": {entity.description}
      }}
    """
    rank_message = [
        {"role": "system", "content": CONTEXT_PROMPT},
        {"role": "user", "content": RANK_PROMPT},
        {"role": "assistant", "content": RANK_RESPONSE},
        {"role": "user", "content": rank_prompt_use}
    ]

    return rank_message


def chat_complete(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message


@dataclass
class Entity():
    title: str
    description: str
    implementation_score: Optional[int] = None
    usefulness_score: Optional[int] = None
    innovation_score: Optional[int] = None


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
    def score_sum(item):
        return sum(item['score'].values())
    return sorted(ideas, key=score_sum, reverse=True)


def parse_step3_json(data: str) -> List[Entity]:
    json_data = json.loads(data)

    result = []

    # for item in json_data:
    #     result.append(
    #         Entity(
    #             item["title"],
    #             item["description"],
    #             item["score"]["implementation"],
    #             item["score"]["usefulness"],
    #             item["score"]["innovation"]
    #         )
    #     )
    result.append(
        Entity(
            json_data["title"],
            json_data["description"],
            json_data["score"]["implementation"],
            json_data["score"]["usefulness"],
            json_data["score"]["innovation"]
        )
    )

    return result


def parse_step2_json(data: str) -> Entity:
    json_data = json.loads(data)

    return Entity(json_data[0]["title"], json_data[0]["description"])


def parse_step1_json(data: str) -> List[Entity]:
    json_data = json.loads(data)

    result = []

    for item in json_data:
        result.append(Entity(item["title"], item["description"]))

    return result


def parse_json_list(ideas):
    ideas = {"ideas": ideas}
    ...


def step3(mixed_ideas):
    """
    Evaluate, rank & sort best results
    :return:
    """
    print(Fore.YELLOW + "\n\nStep 3: Best results\n" + Style.RESET_ALL)
    evaluated_mixed_ideas = []
    for idea in mixed_ideas:
        # prompt = """
        # Given the following JSON add a score (0 to 10) in the following format and evaluate the idea in terms of how easy it is to implement, how useful it is to humanity, and how innovative it is

        # "score": {
        #   "implementation" ...
        #   "usefulness": ...
        #   "innovation": ...
        # }
        # """ + idea.json()
        compelition_raw = chat_complete(rank_complete(idea))
        compelition: List[Entity] = parse_step3_json(compelition_raw.content)
        # TODO: this needs to be a loop
        compelition: Entity = compelition[0]
        print(Fore.WHITE + 'Title: ' + compelition.title)
        print(Fore.WHITE + 'Implementation score: ' +
              str(compelition.implementation_score))
        print(Fore.WHITE + 'Usefullness score: ' +
              str(compelition.usefulness_score))
        print(Fore.WHITE + 'Innovation score: ' +
              str(compelition.innovation_score))

        print('Description: ' + compelition.description + '\n')
        evaluated_mixed_ideas.append(compelition)
    # best_ideas = sort_by_score(evaluated_mixed_ideas)[:len(mixed_ideas)//2]
    return evaluated_mixed_ideas[:len(mixed_ideas)//2]


def step2(ideas, priv_best_ideas=[]):
    """
    Combine ideas
    :return:
    """
    print(Fore.YELLOW + "\n\nStep 2: Combine ideas\n" + Style.RESET_ALL)
    combinations = get_combinations(ideas+priv_best_ideas)
    mixed_ideas = []
    for combo in combinations:
        i1, i2 = combo[0], combo[1]
        compelition_raw = chat_complete(combine_complete(
            i1.title, i1.description, i2.title, i2.description))
        compelition: Entity = parse_step2_json(compelition_raw.content)
        print(Fore.WHITE + 'Title: ' + compelition.title)
        print('Description: ' + compelition.description + '\n')
        mixed_ideas.append(compelition)
    return mixed_ideas


def step1():
    """
    Generate N new ideas
    :return:
    """
    print(Fore.YELLOW + "\n\nStep 1: Generate new ideas\n" + Style.RESET_ALL)
    compelition = chat_complete(GENERATE_MESSAGE)
    raw_ideas: List[Entity] = parse_step1_json(compelition.content)
    for idea in raw_ideas:
        print(Fore.WHITE + 'Title: ' + idea.title)
        print('Description: ' + idea.description + '\n')
    return raw_ideas


def execute_cycle(priv_best_ideas=[]):
    print(Fore.GREEN + "\n\n#################################################")
    print("\n\n#################################################" + Style.RESET_ALL)
    step1_compelition = step1()
    step2_compelition = step2(step1_compelition, priv_best_ideas)
    best_ideas = step3(step2_compelition)
    # send_data(best_ideas)
    return best_ideas


def main():
    best_ideas = []
    while True:
        best_ideas = execute_cycle(best_ideas)


if __name__ == "__main__":
    main()
