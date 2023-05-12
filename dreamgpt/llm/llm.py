import json
import os
import time
import traceback
import openai
from dotenv import load_dotenv

from dreamgpt.constants import EMBEDDING_MODEL

load_dotenv()

openai.api_key = os.environ['OPENAI_API_KEY']

def getEmbedding(text):
    openAIEmbedding = openai.Embedding.create(input = [text], model=EMBEDDING_MODEL)['data'][0]['embedding']
    return openAIEmbedding

def chatComplete(messages, model="gpt-3.5-turbo", max_retries=3, initial_wait_time=1):
    retries = 0
    wait_time = initial_wait_time
    while retries <= max_retries:
        try:
            # Make the API request
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages
            )
            rawJSONResponse = response.choices[0].message.content
            print(rawJSONResponse)
            return json.loads(rawJSONResponse)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            # traceback.print_exc()
            if retries == max_retries:
                raise Exception("Maximum retries reached. Unable to complete the request.") from e
            print("Retrying...")
            retries += 1
        except openai.error.RateLimitError as e:
            # If RateLimitError is encountered, apply exponential backoff and retry
            print("RateLimitError: retrying...")
            if retries == max_retries:
                raise Exception("Maximum retries reached. Unable to complete the request.") from e
            time.sleep(wait_time)
            wait_time *= 2
            retries += 1