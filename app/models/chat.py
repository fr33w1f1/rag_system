from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    context: str = None

class ChatResponse(BaseModel):
    reply: str