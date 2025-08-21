import time, threading, queue
from datetime import datetime
from pathlib import Path
from PIL import Image
import mss
from ..core.config import settings

class ScreenWatch:
    def __init__(self, interval: float):
        self.interval = float(interval)
        self.stop = threading.Event()
        self.thread = None
        self.last_image: Path | None = None
        self.frames = queue.Queue(maxsize=settings.WATCH_MAX_FRAMES)

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self.stop.clear()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop_watch(self):
        self.stop.set()
        if self.thread:
            self.thread.join(timeout=2)

    def _run(self):
        sct = mss.mss()
        i = 0
        while not self.stop.is_set():
            i += 1
            ts = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            path = settings.CACH_ROOT/"files"/f"shot_{ts}_{i:05d}.png"
            img = sct.grab(sct.monitors[1])
            im = Image.frombytes("RGB", img.size, img.rgb)
            im.save(path)
            self.last_image = path
            try:
                self.frames.put_nowait(path)
            except queue.Full:
                _ = self.frames.get_nowait()
                self.frames.put_nowait(path)
            time.sleep(self.interval)
