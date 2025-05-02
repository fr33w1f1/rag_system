from langfuse import Langfuse
from langfuse.model import CreateTrace, CreateGeneration, CreateSpan
from typing import Optional, Dict, Any
from config import settings

class Tracer:
    def __init__(self):
        self.langfuse = Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_host
        )
        self.current_trace = None
        self.current_span = None
    
    def start_trace(self, name: str, input: Optional[Dict] = None, metadata: Optional[Dict] = None):
        self.current_trace = self.langfuse.trace(CreateTrace(
            name=name,
            input=input,
            metadata=metadata
        ))
        return self.current_trace
    
    def start_span(self, name: str, input: Optional[Dict] = None, metadata: Optional[Dict] = None):
        if self.current_trace is None:
            self.start_trace("auto-trace")
        self.current_span = self.current_trace.span(CreateSpan(
            name=name,
            input=input,
            metadata=metadata
        ))
        return self.current_span
    
    def log_generation(self, name: str, input: str, output: str, metadata: Optional[Dict] = None):
        if self.current_trace is None:
            self.start_trace("auto-trace")
        generation = self.current_trace.generation(CreateGeneration(
            name=name,
            input=input,
            output=output,
            metadata=metadata
        ))
        return generation
    
    def flush(self):
        self.langfuse.flush()
