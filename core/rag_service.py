from typing import Dict, List, Optional
from core.llm.base import BaseLLM
from core.retrieval.base import BaseRetriever
from core.tracing.tracer import Tracer

class RAGService:
    def __init__(self, llm: BaseLLM, retriever: BaseRetriever, tracer: Tracer):
        self.llm = llm
        self.retriever = retriever
        self.tracer = tracer
    
    def generate_response(self, query: str, context: Optional[str] = None) -> Dict:
        # Start trace
        trace = self.tracer.start_trace("rag-query", input={"query": query})
        
        # Retrieve relevant documents
        retrieval_span = trace.start_span("retrieval")
        documents = self.retriever.retrieve(query)
        retrieval_span.end(output={"documents": documents})
        
        # Generate response
        generation_span = trace.start_span("generation")
        
        if not context:
            context = "\n\n".join([doc["payload"]["text"] for doc in documents])
        
        prompt = self._build_prompt(query, context)
        
        generation = trace.log_generation(
            name="llm-generation",
            input=prompt,
            output="",  # Will be updated
            metadata={"model": self.llm.model}
        )
        
        response = self.llm.generate(prompt)
        
        generation.update(output=response)
        generation_span.end(output={"response": response})
        
        # Flush traces
        self.tracer.flush()
        
        return {
            "response": response,
            "documents": documents,
            "trace_id": trace.id
        }
    
    def _build_prompt(self, query: str, context: str) -> str:
        return f"""
        You are a helpful assistant. Use the following context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
        Context:
        {context}
        
        Question: {query}
        
        Answer:
        """
