import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_API_KEY=os.environ.get('SECRET_KEY')
IDEAS_NUM_PER_CYCLE = 10

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

def step1():
    """
    Generate N new ideas
    :return:
    """
    prompt = f"Generate {IDEAS_NUM_PER_CYCLE} new ideas. Some context {get_context()}"
    result = chat_complete(prompt)



def execute_cycle():
    step1()
    step2()
    step3()
    step4()

def main():
    while True:
       execute_cycle()


if __name__ == "__main__":
    prompt = "Insert prompt"
    response = chat_complete(input())
    
    print("Response:", response)
