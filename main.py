import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Logolás beállítása fájlba és konzolra
LOG_FILE = Path(__file__).parent / "watchdog.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Figyelt mappa
WATCH_PATH = "c:/Users/gallz/Downloads/"


class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self._last_event = {}

    def _deduplicate(self, event):
        """1 másodpercen belüli duplikált események kiszűrése."""
        now = time.time()
        last = self._last_event.get(event.src_path, 0)
        if now - last < 1:
            return True
        self._last_event[event.src_path] = now
        return False

    def on_modified(self, event):
        if not self._deduplicate(event):
            logger.info("Változás történt: %s", event.src_path)

    def on_created(self, event):
        if not self._deduplicate(event):
            logger.info("Létrehozva: %s", event.src_path)

    def on_deleted(self, event):
        if not self._deduplicate(event):
            logger.info("Törölve: %s", event.src_path)


def main():
    logger.info("Watchdog elindult — figyelt mappa: %s", WATCH_PATH)
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_PATH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Leállítás...")
    finally:
        observer.stop()
        observer.join()
        logger.info("Watchdog leállt.")


if __name__ == "__main__":
    main()
