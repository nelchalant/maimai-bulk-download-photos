# maimai Photo Tools

Automatically download and organize your maimai DX NET photos.

This project includes:

- A bookmarklet for bulk downloading photos
- A Python watcher that automatically moves photos into your MaiMai folder

Windows only.

---

# Features

## Bookmarklet
- Downloads new photos automatically
- Skips already downloaded photos
- Clean automatic filenames

Example:

```txt
maimai_2026-05-23_19-00_MASTER_SongName.jpg
```

## Python Watcher
- Watches your Downloads folder
- Detects maimai photos automatically
- Moves them into your chosen folder
- Windows notifications
- Tray icon support

---

# Requirements

- Windows
- Python 3.10+
- Chrome / Edge / Firefox

---

# Setup

## 1. Install dependencies

Open Command Prompt and run:

```bash
pip install watchdog win10toast pystray pillow
```

---

## 2. Save the script

Place:

```txt
maimai_watcher.py
```

somewhere permanent.

Example:

```txt
C:\Users\YourName\maimai_watcher.py
```

---

## 3. Set your save folder

Inside the script:

```python
MAIMAI_FOLDER = Path(r"C:\Users\YourName\Pictures\MaiMai")
```

Change it to wherever you want your photos stored.

---

## 4. Run the watcher

```bash
python maimai_watcher.py
```

Leave it running in the background.

---

# Auto Start on Boot (Optional)

To make the watcher start automatically when Windows boots:

## 1. Open Startup Folder

Press:

```txt
Win + R
```

Type:

```txt
shell:startup
```

Then press Enter.

---

## 2. Create a VBS file

Create a file called:

```txt
maimai_watcher.vbs
```

Paste this inside:

```vb
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw C:\Users\YourName\maimai_watcher.py", 0, False
```

Replace the path with your actual script location.

Save the file.

Done.

Now the watcher will start silently every time Windows boots.

---

# Bookmarklet Setup

## 1. Create a bookmark

- Right click bookmarks bar
- Press "Add page"

Name:

```txt
maimai Downloader
```

URL:
Paste the contents of:

```txt
bookmarklet.min.js
```

Make sure it starts with:

```txt
javascript:
```

---

## 2. Open the album page

https://maimaidx-eng.com/maimai-mobile/playerData/photo/

---

## 3. Press the bookmark

The bookmarklet will download all new photos automatically.

---

# Reset Download History

Open browser console and run:

```js
localStorage.removeItem('maimai_seen_v1')
```

---

# Workflow

1. Start the watcher
2. Open maimai DX NET album
3. Press the bookmarklet
4. Photos download automatically
5. Watcher moves them into your MaiMai folder

---

# Notes

- Runs locally in your browser
- No data is uploaded anywhere
- Uses browser localStorage only
- Only affects files starting with:

```txt
maimai_
```

---

# License

MIT
