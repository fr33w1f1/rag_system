from abc import ABC, abstractmethod
from typing import List, Optional, Dict

class BaseRetriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        pass
    
