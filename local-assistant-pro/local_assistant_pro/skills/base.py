from abc import ABC, abstractmethod
from typing import Dict, Any

class Skill(ABC):
    name: str = "skill"

    @abstractmethod
    def on_request(self, user_text: str, context: Dict[str, Any]) -> str | None: ...
