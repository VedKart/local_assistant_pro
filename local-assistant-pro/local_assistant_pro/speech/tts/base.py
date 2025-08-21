from abc import ABC, abstractmethod

class TTS(ABC):
    @abstractmethod
    def synth(self, text: str) -> bytes: ...
