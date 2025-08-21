import subprocess
from ...core.config import settings

class PiperTTS:
    def synth(self, text: str) -> bytes:
        if not text.strip():
            return b""
        cmd = [settings.PIPER_EXE, "-m", str(settings.PIPER_VOICE), "--sample_rate", "22050"]
        p = subprocess.run(cmd, input=text.encode("utf-8"), capture_output=True)
        return p.stdout if p.returncode == 0 else b""
