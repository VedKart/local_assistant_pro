from typing import Optional
import typer
from .webapp.app import run_server
from .core.doctor import run_doctor
from .rag.store import ingest_file

app = typer.Typer(add_completion=False)

@app.command()
def run(host: str = "127.0.0.1", port: int = 8000):
    """Запуск FastAPI + UI"""
    run_server(host, port)

@app.command()
def doctor():
    """Диагностика окружения и моделей"""
    info = run_doctor()
    import json
    typer.echo(json.dumps(info, ensure_ascii=False, indent=2))

@app.command()
def ingest(path: str):
    """Добавить файл в память (Chroma)"""
    ok = ingest_file(path)
    typer.echo("OK" if ok else "FAIL")
