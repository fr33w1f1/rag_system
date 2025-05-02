import openai
from typing import List
from core.embedding.base import BaseEmbeddingModel
from config import settings

class OpenAIEmbedding(BaseEmbeddingModel):
    def __init__(self):
        self.client = openai.Client(api_key=settings.openai_api_key)
        self.model = settings.openai_embedding_model
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        return [data.embedding for data in response.data]

if __name__ == "__main__":
    emb = OpenAIEmbedding()
    print(emb.embed('this is a abc'))
