import sys, shutil, subprocess
from pathlib import Path
from .config import settings
from .logger import logger

CHECKS = {
    "gguf": lambda: Path(settings.GGUF_PATH).exists(),
    "emb_model": lambda: Path(settings.EMB_MODEL).exists(),
    "whisper_model_dir": lambda: settings.WHISPER_MODEL_DIR.exists(),
    "ffmpeg": lambda: shutil.which(settings.FFMPEG_EXE) is not None,
    "silero_model": lambda: Path(settings.SILERO_MODEL).exists(),
    "piper_exe": lambda: shutil.which(settings.PIPER_EXE) is not None,
    "piper_voice": lambda: Path(settings.PIPER_VOICE).exists(),
}

def run_doctor():
    report = {k: bool(fn()) for k, fn in CHECKS.items()}
    fixes = []
    vendor = settings.CACH_ROOT / "vendor" / "wheels"
    if vendor.exists():
        try:
            args = [sys.executable, "-m", "pip", "install", "--no-index", "--find-links", str(vendor), "-U", "-r", "<(echo)" ]
        except Exception:
            pass
    # Пробуем поставить всё из каталога, если есть .whl
    wheels = list(vendor.glob("*.whl")) if vendor.exists() else []
    if wheels:
        cmd = [sys.executable, "-m", "pip", "install", "--no-index", "--find-links", str(vendor)] + [str(w) for w in wheels]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            fixes.append({"pip_code": p.returncode, "out": p.stdout[-400:], "err": p.stderr[-400:]})
        except Exception as e:
            fixes.append({"error": str(e)})
    report["fixes"] = fixes
    return report
