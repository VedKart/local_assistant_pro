import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
import yaml

load_dotenv(override=True)

class Settings(BaseModel):
    CACH_ROOT: Path = Path(os.getenv("CACH_ROOT", r"E:\\CACH")).resolve()
    GGUF_PATH: Path = Path(os.getenv("GGUF_PATH", "models/gguf/model.gguf"))
    EMB_MODEL: str = os.getenv("EMB_MODEL", "models/emb/paraphrase-multilingual-MiniLM-L12-v2")

    STT_BACKEND: str = os.getenv("STT_BACKEND", "whisper").lower()
    WHISPER_MODEL_DIR: Path = Path(os.getenv("WHISPER_MODEL_DIR", "models/whisper/medium"))
    FFMPEG_EXE: str = os.getenv("FFMPEG_EXE", "ffmpeg")

    TTS_BACKEND: str = os.getenv("TTS_BACKEND", "silero").lower()
    SILERO_MODEL: Path = Path(os.getenv("SILERO_MODEL", "models/tts/ru_v3.pt"))
    PIPER_EXE: str = os.getenv("PIPER_EXE", "piper")
    PIPER_VOICE: Path = Path(os.getenv("PIPER_VOICE", "models/piper/ru_kirill-medium.onnx"))

    N_CTX: int = int(os.getenv("N_CTX", 4096))
    N_THREADS: int = int(os.getenv("N_THREADS", 8))
    N_GPU_LAYERS: int = int(os.getenv("N_GPU_LAYERS", 35))
    N_BATCH: int = int(os.getenv("N_BATCH", 64))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", 512))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", 0.6))
    TOP_P: float = float(os.getenv("TOP_P", 0.9))

    WATCH_INTERVAL: float = float(os.getenv("WATCH_INTERVAL", 2.0))
    WATCH_MAX_FRAMES: int = int(os.getenv("WATCH_MAX_FRAMES", 300))

    def ensure_dirs(self):
        root = self.CACH_ROOT
        for rel in ("kb/chroma", "kb/raw", "logs", "files", "tmp", "vendor/wheels", "models"):
            (root / rel).mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.ensure_dirs()
