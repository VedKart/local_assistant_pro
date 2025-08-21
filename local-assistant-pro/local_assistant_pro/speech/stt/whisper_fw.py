import tempfile, subprocess
from pathlib import Path
from ...core.config import settings

class WhisperFW:
    def __init__(self):
        from faster_whisper import WhisperModel
        self.model = WhisperModel(str(settings.WHISPER_MODEL_DIR), device="auto", compute_type="int8")

    def _webm_to_wav(self, webm: bytes) -> bytes:
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=True) as f_in,              tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as f_out:
            f_in.write(webm); f_in.flush()
            p = subprocess.run([settings.FFMPEG_EXE, "-y", "-i", f_in.name, "-ar", "16000", "-ac", "1", f_out.name], capture_output=True)
            if p.returncode != 0:
                raise RuntimeError("ffmpeg failed")
            return Path(f_out.name).read_bytes()

    def transcribe_webm(self, webm: bytes) -> str:
        wav = self._webm_to_wav(webm)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as f:
            f.write(wav); f.flush()
            segs, _ = self.model.transcribe(f.name, language="ru")
            return " ".join([s.text.strip() for s in segs]).strip()
