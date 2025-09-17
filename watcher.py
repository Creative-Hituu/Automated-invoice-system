import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

invoices_folder = "invoices"

class InvoiceHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".pdf"):
            print(f"📄 New invoice detected: {event.src_path}")
            print("⚡ Processing...")
            subprocess.run(["python", "batch_process.py"])

if __name__ == "__main__":
    event_handler = InvoiceHandler()
    observer = Observer()
    observer.schedule(event_handler, invoices_folder, recursive=False)
    observer.start()

    print(f"👀 Watching folder: {invoices_folder}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
