from typing import List, Dict
from llama_cpp import Llama
from ..core.config import settings

class LlamaCppLLM:
    def __init__(self):
        self.model = Llama(
            model_path=str(settings.GGUF_PATH),
            n_ctx=settings.N_CTX,
            n_threads=settings.N_THREADS,
            n_gpu_layers=settings.N_GPU_LAYERS,
            n_batch=settings.N_BATCH,
        )

    def chat(self, messages: List[Dict[str, str]], **gen) -> str:
        resp = self.model.create_chat_completion(
            messages=messages,
            temperature=gen.get("temperature", settings.TEMPERATURE),
            top_p=gen.get("top_p", settings.TOP_P),
            max_tokens=gen.get("max_tokens", settings.MAX_TOKENS),
            stream=False,
        )
        return (resp.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
