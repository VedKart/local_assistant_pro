from abc import ABC, abstractmethod

class STT(ABC):
    @abstractmethod
    def transcribe_webm(self, webm: bytes) -> str: ...
