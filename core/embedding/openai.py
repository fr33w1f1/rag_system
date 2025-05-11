import openai
from typing import List
from core.embedding.base import BaseEmbeddingModel
from config import settings

class OpenAIEmbedding(BaseEmbeddingModel):
    def __init__(self):
        self.client = openai.Client(api_key=settings.openai_api_key)
        self.model = settings.openai_embedding_model
        self.model_dims = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
        }
    def embed(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        return [data.embedding for data in response.data]

    def get_dimension(self) -> int:
        return self.model_dims[self.model]
    

if __name__ == "__main__":
    emb = OpenAIEmbedding()
    print(emb.embed('this is a abc'))
