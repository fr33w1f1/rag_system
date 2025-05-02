from qdrant_client import QdrantClient
from qdrant_client.models import Filter, PointStruct
from typing import List, Dict, Optional
from config import settings
from core.retrieval.base import BaseRetriever
from core.embedding.openai import OpenAIEmbedding

class QdrantRetriever(BaseRetriever):
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.collection = settings.qdrant_collection_name
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        query_embedding = self._get_embedding(query)
        
        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_embedding,
            limit=top_k
        )
        
        return [
            {
                "id": result.id,
                "score": result.score,
                "payload": result.payload,
                "vector": result.vector
            }
            for result in results
        ]
    
    def _get_embedding(self, text: str) -> List[float]:
        embedding_model = OpenAIEmbedding()
        return embedding_model.embed([text])[0]
