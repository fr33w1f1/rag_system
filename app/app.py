from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware 
from slowapi import Limiter
from slowapi.util import get_remote_address

from config import settings
from app.api.v1 import chat, documents

app = FastAPI(title="RAG System API")
limiter = Limiter(key_func=get_remote_address)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SlowAPIMiddleware)

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(documents.router, prefix="/api/v1", tags=["documents"])

app.include_router(chat.router, prefix="/api/latest", tags=["chat"])
app.include_router(documents.router, prefix="/api/latest", tags=["documents"])