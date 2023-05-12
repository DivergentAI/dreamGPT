import os
import openai
from dotenv import load_dotenv

from dreamgpt.constants import OPENAI_EMBEDDING_MODEL

load_dotenv()

openai.api_key = os.environ['OPENAI_API_KEY']

def getEmbedding(fullText):
    openAIEmbedding = openai.Embedding.create(input = [fullText], model=OPENAI_EMBEDDING_MODEL)['data'][0]['embedding']
    return openAIEmbedding