from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from app.api.v1 import chat, documents

app = FastAPI(title="RAG System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])

app.include_router(chat.router, prefix="/api/latest/chat", tags=["chat"])
app.include_router(documents.router, prefix="/api/latest/documents", tags=["documents"])