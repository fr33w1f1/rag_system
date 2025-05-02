import openai
from typing import Optional, Dict, Any
from core.llm.base import BaseLLM
from config import settings

class OpenAIChat(BaseLLM):
    def __init__(self):
        self.client = openai.Client(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content
