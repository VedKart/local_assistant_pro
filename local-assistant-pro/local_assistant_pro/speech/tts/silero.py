import io
from wave import open as wave_open
import numpy as np

from ...core.config import settings

class SileroTTS:
    def __init__(self, speaker: str = "xenia"):
        import torch
        self.torch = torch
        self.model = torch.jit.load(str(settings.SILERO_MODEL), map_location="cpu")
        self.model.eval()
        self.speaker = speaker

    def synth(self, text: str) -> bytes:
        audio = self.model.apply_tts(text=text, speaker=self.speaker, sample_rate=48000)
        buf = io.BytesIO()
        with wave_open(buf, "wb") as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(48000)
            arr = (audio.numpy() * 32767.0).astype(np.int16)
            wf.writeframes(arr.tobytes())
        return buf.getvalue()
