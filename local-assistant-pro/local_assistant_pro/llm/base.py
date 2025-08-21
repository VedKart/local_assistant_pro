from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLM(ABC):
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **gen) -> str: ...
