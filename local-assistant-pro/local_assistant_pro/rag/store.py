from pathlib import Path
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from ..core.config import settings

_embed = HuggingFaceEmbeddings(model_name=settings.EMB_MODEL)
_vs = Chroma(collection_name="kb", embedding_function=_embed, persist_directory=str(settings.CACH_ROOT/"kb"/"chroma"))

def ingest_file(path: str) -> bool:
    p = Path(path)
    if not p.exists():
        return False
    text = p.read_text(encoding="utf-8", errors="ignore")
    if not text.strip():
        return False
    chunks, buf = [], []
    for ln in text.splitlines():
        if ln.strip(): buf.append(ln.strip())
        else:
            if buf: chunks.append(" ".join(buf)); buf=[]
    if buf: chunks.append(" ".join(buf))
    if not chunks: return False
    _vs.add_texts(texts=chunks, metadatas=[{"source": str(p)}]*len(chunks))
    _vs.persist();
    return True

def search(q: str, k: int = 3) -> List[str]:
    try:
        docs = _vs.similarity_search(q, k=k)
        return [d.page_content for d in docs if getattr(d, 'page_content', '')]
    except Exception:
        return []
