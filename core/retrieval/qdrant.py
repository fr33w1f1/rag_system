from qdrant_client import QdrantClient, models
from langchain.schema import Document
from typing import List, Dict, Optional
from config import settings
from core.retrieval.base import BaseRetriever
from core.embedding.openai import OpenAIEmbedding
from fastembed import SparseTextEmbedding

class QdrantRetriever(BaseRetriever):
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.collection = settings.qdrant_collection_name
        self.dense_embedding_model = OpenAIEmbedding()
        self.sparse_embedding_model = SparseTextEmbedding(model_name="Qdrant/bm25")

    def create_collection(self):
        if not client.collection_exists(collection_name=self.collection):
            client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    'text-dense': models.VectorParams(
                        size=dense_embedding_model.get_dimension(),
                        distance=models.Distance.COSINE,
                    )
                },
                sparse_vectors_config={
                    "text-sparse": models.SparseVectorParams(
                        index=models.SparseIndexParams()
                    )
                }
            )
        else:
            print(f"Collection '{collection_name}' already exists.")

    def upsert_documents(self, documents: List[Document]):
        texts = [doc.page_content for doc in documents]
        dense_embeddings = self.embedding_model.embed(texts)
        sparse_embeddings = list(self.sparse_embedding_model.embed(texts))

        points = []
        for idx, (doc, dense_vec, idx_sparse_vec) in enumerate(zip(documents, dense_embeddings, sparse_embeddings)):
            points.append(
                PointStruct(
                    id=idx,
                    vector={
                        "text-dense": dense_vec,  # Dense vector
                        "text-sparse": models.SparseVector(indices=idx_sparse_vec.indices.tolist() , values=idx_sparse_vec.values.tolist()), 
                    },
                    payload={
                        "text": doc.page_content,
                        "source": doc.metadata['source']
                        }
                )
            )

        # Upsert points
        client.upsert(
            collection_name=collection_name,
            points=points,
            # wait=True
        )

    
    def query(self, text: str, top_k: int = 10):
        """Perform hybrid search using both dense and sparse vectors."""
        dense_vector = self.embedding_model.embed(text)[0]
        sparse_vector = list(self.sparse_model.embed(text))[0]

        prefetch = [
            Prefetch(query=dense_vector, using="text-dense", limit=top_k),
            Prefetch(
                query=SparseVector(
                    indices=sparse_vector.indices.tolist(),
                    values=sparse_vector.values.tolist()
                ),
                using="text-sparse",
                limit=top_k,
            ),
        ]

        results = self.client.query_points(
            collection_name=self.collection,
            prefetch=prefetch,
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            with_payload=True,
            limit=top_k
        )

        return results