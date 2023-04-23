import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_API_KEY=os.environ.get('SECRET_KEY')


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

if __name__ == "__main__":
    prompt = "Insert prompt"
    response = chat_complete(input())
    
    print("Response:", response)
