from fastapi import APIRouter, UploadFile, File
from typing import List
import os
from core.processing.document_processor import PDFProcessor
from core.retrieval.qdrant import QdrantRetriever
from core.embedding.openai import OpenAIEmbedding
from config import settings

router = APIRouter()

@router.post("/ingest-pdf")
def ingest_pdf(
    files: List[UploadFile] = File(...),
    collection_name: str = settings.qdrant_collection_name,
):
    embedding_model = OpenAIEmbedding()
    retriever = QdrantRetriever()