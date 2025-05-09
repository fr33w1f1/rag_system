from fastapi import APIRouter, Depends
from core.rag_service import RAGService
from core.llm.openai import OpenAIChat
from core.retrieval.qdrant import QdrantRetriever
from core.tracing.tracer import Tracer
from app.models.chat import ChatRequest, ChatResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

def get_rag_service() -> RAGService:
    llm = OpenAIChat()
    retriever = QdrantRetriever()
    tracer = Tracer()
    return RAGService(llm, retriever, tracer)

@router.post("/chat", response_model=ChatResponse)
@limiter.limit("5/minute")
async def chat_query(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    response = rag_service.generate_response(request.query, request.context)
    return {
        "response": response["response"],
        "documents": response["documents"],
        "trace_id": response["trace_id"]
    }
