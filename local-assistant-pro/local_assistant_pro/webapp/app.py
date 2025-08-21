from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uuid

from ..core.config import settings
from ..core.logger import logger
from ..core.events import persona, build_system_prompt
from ..llm.llamacpp import LlamaCppLLM
from ..rag.store import search, ingest_file
from ..vision.screenwatch import ScreenWatch

# STT/TTS backends (ленивая инициализация)
_stt = None
_tts = None

app = FastAPI(title="Local Assistant Pro")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)
app.mount("/files", StaticFiles(directory=str(settings.CACH_ROOT/"files")), name="files")

WATCH = ScreenWatch(settings.WATCH_INTERVAL)
LLM = LlamaCppLLM()

UI = (Path(__file__).parent/"ui"/"index.html").read_text(encoding="utf-8")

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(UI)

@app.post("/ask")
async def ask(payload: dict):
    msg = (payload or {}).get("message", "").strip()
    if not msg: return JSONResponse({"answer": "Пустой запрос."})
    ctx_docs = search(msg, k=3)
    kb_ctx = "\n".join([f"- {d}" for d in ctx_docs])
    sys_prompt = build_system_prompt(kb_ctx, msg)
    messages = [{"role":"system","content":sys_prompt},{"role":"user","content":msg}]
    answer = LLM.chat(messages)

    audio_url = None
    try:
        tts = _get_tts()
        wav = tts.synth(answer) if tts else b""
        if wav:
            name = f"tts_{uuid.uuid4().hex[:6]}.wav"
            out = settings.CACH_ROOT/"files"/name
            out.write_bytes(wav)
            audio_url = f"/files/{name}"
    except Exception as e:
        logger.error(f"TTS error: {e}")

    return JSONResponse({"answer": answer, "audio": audio_url})

@app.post("/stt")
async def stt(audio: UploadFile = File(...)):
    raw = await audio.read()
    stt = _get_stt()
    text = stt.transcribe_webm(raw) if stt else ""
    return JSONResponse({"text": text})

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    target = settings.CACH_ROOT/"kb"/"raw"/file.filename
    target.write_bytes(await file.read())
    ok = ingest_file(str(target))
    return JSONResponse({"ok": ok, "path": str(target)})

@app.post("/start_watch")
async def start_watch():
    WATCH.start(); return {"ok": True}

@app.post("/stop_watch")
async def stop_watch():
    WATCH.stop_watch(); return {"ok": True}

@app.get("/watch_status")
async def watch_status():
    last = WATCH.last_image
    return {"last": f"/files/{last.name}" if last else None}

@app.post("/persona")
async def set_persona(payload: dict = Body(...)):
    name = (payload or {}).get("name"); base = (payload or {}).get("base_prompt"); voice=(payload or {}).get("tts_voice")
    if name: persona.name = name
    if base: persona.base_prompt = base
    if voice: persona.tts_voice = voice
    return {"ok": True, "persona": persona.__dict__}

@app.post("/doctor")
async def doctor():
    from ..core.doctor import run_doctor
    return run_doctor()

# Helpers

def _get_stt():
    global _stt
    if _stt is not None: return _stt
    if settings.STT_BACKEND == "whisper":
        from ..speech.stt.whisper_fw import WhisperFW
        _stt = WhisperFW(); return _stt
    return None

def _get_tts():
    global _tts
    if _tts is not None: return _tts
    if settings.TTS_BACKEND == "silero":
        from ..speech.tts.silero import SileroTTS
        _tts = SileroTTS(persona.tts_voice); return _tts
    if settings.TTS_BACKEND == "piper":
        from ..speech.tts.piper import PiperTTS
        _tts = PiperTTS(); return _tts
    return None

# Entrypoint for CLI

def run_server(host: str, port: int):
    import uvicorn
    uvicorn.run(app, host=host, port=port)
