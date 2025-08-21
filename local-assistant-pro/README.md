# Local Assistant Pro

Офлайн ассистент (FastAPI + llama.cpp + Chroma + офлайн STT/TTS + захват экрана + плагины).

## Быстрый старт
1) Создайте окружение Python 3.10+ и установите проект (офлайн — через локальные wheel, online — pip):
   ```bash
   pip install -e .
   ```

2. Заполните `.env` (см. пример `.env.example`).
3. Запуск API + UI:
   ```bash
   assistant run --host 127.0.0.1 --port 8000
   # затем откройте http://127.0.0.1:8000
   ```
4. Диагностика:
   ```bash
   assistant doctor
   ```
5. Ингест файлов в память:
   ```bash
   assistant ingest path/to/file.txt
   ```

## Каталоги с моделями (пример)

```
CACH_ROOT/
  models/
    gguf/model.gguf
    emb/paraphrase-multilingual-MiniLM-L12-v2/
    whisper/medium/
    tts/ru_v3.pt
    piper/ru_kirill-medium.onnx
  vendor/wheels/*.whl
  files/
  kb/raw/  kb/chroma/
```

## Лицензии моделей

Следите за лицензиями используемых моделей (GGUF/Whisper/Silero/Piper) — они распространяются отдельно.
