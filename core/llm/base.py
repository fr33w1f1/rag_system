from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
