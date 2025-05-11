from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-large"

    sparse_model: str = 'Qdrant/bm25'
    
    qdrant_url: str =  "localhost:6333"
    # qdrant_api_key: str
    qdrant_collection_name: str = "documents"
    
    langfuse_secret_key: str
    langfuse_public_key: str
    langfuse_host: str = "localhost:3000"
    
    class Config:
        env_file = ".env"

settings = Settings()
