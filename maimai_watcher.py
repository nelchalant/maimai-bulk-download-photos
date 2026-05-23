"""
maimai Photo Watcher
--------------------
Watches your Downloads folder and automatically moves
any maimai photos to C:\\Users\\YourName\\Pictures\\MaiMai

Requirements (install once):
    pip install watchdog win10toast pystray pillow

To run at startup, see the instructions at the bottom of this file.
"""

import os
import shutil
import time
import threading
import sys
from pathlib import Path

# ─── Config ────────────────────────────────────────────────────────────────────
DOWNLOADS_FOLDER = Path.home() / "Downloads"
MAIMAI_FOLDER    = Path(r"C:\Users\YourName\Pictures\MaiMai")
WATCH_PREFIX     = "maimai_"          # only move files starting with this
WATCH_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
# ───────────────────────────────────────────────────────────────────────────────


def move_file(src: Path):
    """Move a maimai photo to the MaiMai folder and notify."""
    MAIMAI_FOLDER.mkdir(parents=True, exist_ok=True)
    dest = MAIMAI_FOLDER / src.name

    # If a file with the same name already exists, skip it
    if dest.exists():
        print(f"[skip] already exists: {src.name}")
        return

    try:
        shutil.move(str(src), str(dest))
        print(f"[moved] {src.name} → {MAIMAI_FOLDER}")
        send_notification(src.name)
    except Exception as e:
        print(f"[error] could not move {src.name}: {e}")


def send_notification(filename: str):
    """Show a Windows toast notification."""
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(
            "maimai 📸",
            f"Saved: {filename}",
            duration=4,
            threaded=True,
        )
    except Exception as e:
        print(f"[notify] failed: {e}")


def is_maimai_file(path: Path) -> bool:
    return (
        path.is_file()
        and path.name.startswith(WATCH_PREFIX)
        and path.suffix.lower() in WATCH_EXTENSIONS
    )


def scan_existing():
    """On startup, move any maimai files already sitting in Downloads."""
    for f in DOWNLOADS_FOLDER.iterdir():
        if is_maimai_file(f):
            print(f"[startup] found existing file: {f.name}")
            time.sleep(0.5)  # let any in-progress write finish
            move_file(f)


def start_watcher():
    """Watch Downloads folder using watchdog."""
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class Handler(FileSystemEventHandler):
        def on_created(self, event):
            if event.is_directory:
                return
            path = Path(event.src_path)
            if is_maimai_file(path):
                # Wait briefly for the browser to finish writing the file
                time.sleep(1.5)
                move_file(path)

        def on_moved(self, event):
            # Chrome writes to a .crdownload then renames — catch the rename
            if event.is_directory:
                return
            path = Path(event.dest_path)
            if is_maimai_file(path):
                time.sleep(0.5)
                move_file(path)

    observer = Observer()
    observer.schedule(Handler(), str(DOWNLOADS_FOLDER), recursive=False)
    observer.start()
    print(f"[watching] {DOWNLOADS_FOLDER}")
    return observer


def make_tray_icon():
    """Create a simple system tray icon."""
    import pystray
    from PIL import Image, ImageDraw

    # Draw a simple yellow circle as the icon
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 60, 60], fill="#f5c842", outline="#c49a00", width=3)
    draw.text((22, 18), "mai", fill="#333333")

    def on_quit(icon, item):
        icon.stop()
        os._exit(0)

    menu = pystray.Menu(
        pystray.MenuItem("maimai Photo Watcher", None, enabled=False),
        pystray.MenuItem(f"Saving to: MaiMai\\", None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit", on_quit),
    )

    icon = pystray.Icon("maimai_watcher", img, "maimai Watcher", menu)
    return icon


def main():
    print("maimai Photo Watcher starting...")
    print(f"  Downloads : {DOWNLOADS_FOLDER}")
    print(f"  MaiMai    : {MAIMAI_FOLDER}")

    # Move any files already in Downloads on startup
    scan_existing()

    # Start the folder watcher in a background thread
    observer = start_watcher()

    # Try to show a tray icon; fall back to just running headlessly
    try:
        icon = make_tray_icon()
        # Run watcher in thread, tray icon on main thread
        threading.Thread(target=lambda: None, daemon=True).start()
        icon.run()  # blocks until quit
    except Exception as e:
        print(f"[tray] not available ({e}), running headlessly. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    observer.stop()
    observer.join()
    print("Stopped.")


if __name__ == "__main__":
    main()


# ─── HOW TO ADD TO WINDOWS STARTUP ────────────────────────────────────────────
#
# Option 1 — Startup folder (easiest):
#   1. Press Win+R, type: shell:startup, press Enter
#   2. Create a new file called "maimai_watcher.vbs" with this content:
#
#      Set WshShell = CreateObject("WScript.Shell")
#      WshShell.Run "pythonw C:\Users\YourName\maimai_watcher.py", 0, False
#
#   3. Save it. Now it runs silently every time Windows starts.
#      (Use pythonw instead of python so no console window appears)
#
# Option 2 — Run manually anytime:
#   Just double-click maimai_watcher.py (if .py files open with Python)
#   or run:  pythonw C:\path\to\maimai_watcher.py
#
# ─── HOW TO INSTALL REQUIREMENTS ──────────────────────────────────────────────
#
#   Open Command Prompt and run:
#   pip install watchdog win10toast pystray pillow
#
# ──────────────────────────────────────────────────────────────────────────────
