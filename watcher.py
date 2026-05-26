"""Watch data/ for new CSV files and trigger briefing_generator.py automatically."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
GENERATOR = ROOT / "briefing_generator.py"


class CSVHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() != ".csv" or path.name.startswith("."):
            return
        print(f"[watcher] Detected new file: {path.name} — generating briefing...")
        subprocess.run([sys.executable, str(GENERATOR)], cwd=str(ROOT), check=False)
        print("[watcher] Done.")


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    observer = Observer()
    observer.schedule(CSVHandler(), str(DATA_DIR), recursive=False)
    observer.start()
    print("[watcher] Monitoring data/ folder — drop a CSV to generate a briefing")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
