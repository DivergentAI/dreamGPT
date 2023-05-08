import time
import uuid
from dotenv import load_dotenv

from dreamgpt.store.embeddings import getEmbedding

class Entity:
    def __init__(self, title, description, scores=None, id=None, embedding=None, createdAt=None):
        self.title = title
        self.description = description
        if scores is None:
            self.scores = []
        else:
            self.scores = [float(score) for score in scores.split(",")]
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        if createdAt is None:
            self.createdAt = int(time.time() * 1000)
        else:
            self.createdAt = createdAt
        if embedding is None:
            self.embedding = self._getEmbedding()
        else:
            self.embedding = embedding

    def getEntityScoreString(self):
        if self.scores is None:
            return ""
        else:
            return ",".join([str(score) for score in self.scores])
    
    def _getEmbedding(self):
        fullText = f"{self.title}: {self.description}"
        return getEmbedding(fullText)
    