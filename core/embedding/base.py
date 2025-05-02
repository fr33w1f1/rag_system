from abc import ABC, abstractmethod
from typing import List

class BaseEmbeddingModel(ABC):
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        pass

