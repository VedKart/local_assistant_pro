import importlib.util, sys
from pathlib import Path
from typing import List
from .base import Skill
from ..core.config import settings
from ..core.logger import logger

class SkillManager:
    def __init__(self, skills_dir: Path | None = None):
        self.skills_dir = skills_dir or (settings.CACH_ROOT/"skills")
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.skills: List[Skill] = []

    def load_all(self):
        self.skills.clear()
        for py in self.skills_dir.glob("*.py"):
            try:
                spec = importlib.util.spec_from_file_location(py.stem, py)
                mod = importlib.util.module_from_spec(spec)
                sys.modules[py.stem] = mod
                spec.loader.exec_module(mod)  # type: ignore
                for attr in dir(mod):
                    obj = getattr(mod, attr)
                    if isinstance(obj, type) and issubclass(obj, Skill) and obj is not Skill:
                        self.skills.append(obj())
                        logger.info(f"Loaded skill: {obj.__name__} from {py.name}")
            except Exception as e:
                logger.error(f"Skill load error for {py}: {e}")

    def run(self, text: str, ctx: dict) -> str | None:
        for sk in self.skills:
            try:
                out = sk.on_request(text, ctx)
            except Exception as e:
                logger.error(f"Skill error {sk}: {e}")
                out = None
            if out:
                return out
        return None
