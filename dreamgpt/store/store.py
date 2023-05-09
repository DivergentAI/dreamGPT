import os
import pinecone
import openai
from dotenv import load_dotenv

from dreamgpt.constants import EMBEDDING_VECTOR_SIZE, PINECONE_INDEX_NAME
from dreamgpt.llm.llm import getEmbedding
from dreamgpt.store.entity import Entity

load_dotenv()

openai.api_key = os.environ['OPENAI_API_KEY']

class Store:
    def __init__(self):
        self.inMemoryDB = []
        self._initDatabase()

    def _isPineconeConfigured(self):
        if (os.environ.get('PINECONE_API_KEY') is None) or (os.environ.get('PINECONE_ENVIRONMENT') is None):
            return False

        return True

    def _initDatabase(self):
        if (self._isPineconeConfigured()):
          index_name = PINECONE_INDEX_NAME
          pinecone.init(
            api_key=os.environ['PINECONE_API_KEY'], 
            environment=os.environ['PINECONE_ENVIRONMENT']
          )
          if index_name not in pinecone.list_indexes():
              print(f"Creating Pinecone index: {index_name}")
              pinecone.create_index(
                  name=index_name,
                  dimension=EMBEDDING_VECTOR_SIZE,
                  metric='cosine'
              )
              print(f"Index created")

          self.index = pinecone.Index(index_name)
        else:
          self.index = None
          print("Pinecone not configured. Please set PINECONE_API_KEY and PINECONE_ENVIRONMENT in your .env file.")
    
    def addEntity(self, entity: Entity):
        if (self._isPineconeConfigured()):
          self.index.upsert([
              (entity.id, entity.embedding, 
                {
                  "title": entity.title, 
                  "description": entity.description, 
                  "createdAt": entity.createdAt,
                  "noveltyScore": entity.noveltyScore,
                  "marketScore": entity.marketScore,
                  "usefulnessScore": entity.usefulnessScore,
                  "easeOfImplementationScore": entity.usefulnessScore,
                  "impactScore": entity.impactScore,
                  "totalScore": entity.totalScore,
                  "parents": entity.parents
                })
          ])

        self.inMemoryDB.append(entity)

    def addEntities(self, entities: list):
        if (self._isPineconeConfigured()):
            itemsToUpsert = list(map(lambda entity: (entity.id, entity.embedding, 
                {
                  "title": entity.title, 
                  "description": entity.description, 
                  "createdAt": entity.createdAt,
                  "noveltyScore": entity.noveltyScore,
                  "marketScore": entity.marketScore,
                  "usefulnessScore": entity.usefulnessScore,
                  "easeOfImplementationScore": entity.usefulnessScore,
                  "impactScore": entity.impactScore,
                  "totalScore": entity.totalScore,
                  "parents": entity.parents
                }), entities))
            self.index.upsert(itemsToUpsert)

        self.inMemoryDB += entities

    def updateEntity(self, updatedEntity: Entity):
        if (self._isPineconeConfigured()):
          self.index.upsert([
              (updatedEntity.id, updatedEntity.embedding, 
                {
                  "title": updatedEntity.title, 
                  "description": updatedEntity.description, 
                  "createdAt": updatedEntity.createdAt,
                  "noveltyScore": updatedEntity.noveltyScore,
                  "marketScore": updatedEntity.marketScore,
                  "usefulnessScore": updatedEntity.usefulnessScore,
                  "easeOfImplementationScore": updatedEntity.usefulnessScore,
                  "impactScore": updatedEntity.impactScore,
                  "totalScore": updatedEntity.totalScore,
                  "parents": updatedEntity.parents
                })
          ])

        self.inMemoryDB = [updatedEntity if entity.id == updatedEntity.id else entity for entity in self.inMemoryDB]

    def getSimilar(self, queryString, count=10):
        if (self._isPineconeConfigured()):
          embedding = getEmbedding(queryString)
          return self.index.query(vector=[embedding], top_k=count, include_metadata=True)
        else:
          print("Pinecone not configured. Please set PINECONE_API_KEY and PINECONE_ENVIRONMENT in your .env file.")
          return None
