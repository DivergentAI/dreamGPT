import time
import uuid
from dotenv import load_dotenv
from dreamgpt.constants import IMPACT_WEIGHT, IMPLEMENTATION_WEIGHT, MARKET_WEIGHT, NOVELTY_WEIGHT, USEFULNESS_WEIGHT

from dreamgpt.llm.llm import getEmbedding

def getEntityFromJSON(entityJSON, parentIDs=None):
    try:
        return Entity( 
                        entityJSON["title"],
                        entityJSON["description"],
                        entityJSON["noveltyScore"],
                        entityJSON["marketScore"],
                        entityJSON["usefulnessScore"],
                        entityJSON["easeOfImplementationScore"],
                        entityJSON["impactScore"],
                        parents = parentIDs if parentIDs is not None else entityJSON.get("parents", []),
                    )
    except Exception as e:
        print(e)
        return None

class Entity:
    def __init__(self, title, description, noveltyScore = 0, marketScore = 0, usefulnessScore = 0, easeOfImplementationScore=0, impactScore = 0, parents=[], id=None, embedding=None, createdAt=None):
        self.title = title
        self.description = description
        self.noveltyScore = noveltyScore
        self.marketScore = marketScore
        self.usefulnessScore = usefulnessScore
        self.easeOfImplementationScore = easeOfImplementationScore
        self.impactScore = impactScore
        self.parents = parents
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
    
    @property
    def totalScore(self):
        return NOVELTY_WEIGHT * self.noveltyScore + \
               MARKET_WEIGHT * self.marketScore + \
               USEFULNESS_WEIGHT * self.usefulnessScore + \
               IMPLEMENTATION_WEIGHT * self.easeOfImplementationScore + \
               IMPACT_WEIGHT * self.impactScore
    
    def _getEmbedding(self):
        fullText = f"{self.title}: {self.description}"
        return getEmbedding(fullText)
    