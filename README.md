# maimai Photo Tools

Automatically download and organize your maimai DX NET photos.

This setup includes:

- A bookmarklet that downloads new photos
- A Python watcher that automatically moves them into a separate MaiMai folder

Windows only.

---

# Quick Setup

1. Install Python
2. Install dependencies
3. Edit your MaiMai folder path inside:

```txt
maimai_watcher.py
```

4. Run the watcher
5. Create the bookmarklet
6. Open the album page
7. Press the bookmark

Done.

---

# Requirements

- Windows
- Python 3.10 or newer
- Chrome / Edge / Firefox

Download Python here:

https://www.python.org/downloads/

IMPORTANT:

During installation, enable:

```txt
Add Python to PATH
```

---

# What This Does

After setup:

1. Open your maimai album page
2. Press the bookmarklet
3. Photos download automatically
4. The watcher instantly moves them into:

```txt
C:\Users\YourName\Pictures\MaiMai
```

No manual sorting needed.

---

# Step 1 — Install Python Dependencies

Open Command Prompt:

- Press:

```txt
Win + R
```

- Type:

```txt
cmd
```

- Press Enter

Then run:

```bash
pip install watchdog win10toast pystray pillow
```

---

# Step 2 — Save the Python Script

Save:

```txt
maimai_watcher.py
```

somewhere permanent.

Example:

```txt
C:\Users\YourName\maimai_watcher.py
```

Do NOT place it in Downloads or temporary folders.

---

# Step 3 — Set Your MaiMai Folder

Open:

```txt
maimai_watcher.py
```

with any text editor (Notepad is fine).

Find this line:

```python
MAIMAI_FOLDER = Path(r"C:\Users\YourName\Pictures\MaiMai")
```

Change it to your own folder.

Example:

```python
MAIMAI_FOLDER = Path(r"D:\Games\MaiMaiPhotos")
```

Save the file after editing.

---

# Step 4 — Run the Watcher

Open Command Prompt inside the folder containing:

```txt
maimai_watcher.py
```

Then run:

```bash
python maimai_watcher.py
```

You should see:
- a tray icon
- notifications when photos are moved

The watcher now monitors your Downloads folder automatically.

---

# Optional — Start Automatically With Windows

Press:

```txt
Win + R
```

Type:

```txt
shell:startup
```

Press Enter.

Create a file called:

```txt
maimai_watcher.vbs
```

Paste this inside:

```vb
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw C:\Users\YourName\maimai_watcher.py", 0, False
```

Save it.

IMPORTANT:

If your script is not located at:

```txt
C:\Users\YourName\maimai_watcher.py
```

you must edit the path inside the VBS file.

Example:

```vb
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw D:\Scripts\maimai_watcher.py", 0, False
```

If Windows hides file extensions and your file becomes:

```txt
maimai_watcher.vbs.txt
```

it will NOT work.

To fix this:

- Open File Explorer
- Press:

```txt
View
```

- Enable:

```txt
File name extensions
```

Now the watcher starts automatically every time Windows boots.

---

# Bookmarklet Setup

If your bookmarks bar is hidden, press:

```txt
Ctrl + Shift + B
```

---

## 1. Create a Bookmark

- Right click your bookmarks bar
- Press:

```txt
Add page
```

Name it anything you want.

Example:

```txt
maimai 📸
```

---

## 2. Paste the Bookmarklet

Paste this into the bookmark URL:

```txt
javascript:(function(){const KEY='maimai_seen_v1';const seen=new Set(JSON.parse(localStorage.getItem(KEY)||'[]'));const links=[...document.querySelectorAll('a[href*="/img/photo/user/"]')];const fresh=links.filter(l=>!seen.has(l.href));if(!fresh.length){alert('maimai \u{1F4F8} All photos already saved! Nothing new.');return;}fresh.forEach((l,i)=>{setTimeout(()=>{const card=l.closest('[class*="score_back"]');const date=(card?.querySelector('.block_info')?.textContent||'').trim().replace(/\//g,'-').replace(/\s+/g,'_');const song=(card?.querySelector('.black_block')?.textContent||'photo').trim().replace(/[\\/:*?"<>|]/g,'').replace(/\s+/g,'_').substring(0,35);const diff=(card?.querySelector('[src*="diff_"]')?.src||'').match(/diff_(\w+)\./)?.[1]||'';const a=document.createElement('a');a.href=l.href;a.download='maimai_'+date+'_'+diff.toUpperCase()+'_'+song+'.jpg';document.body.appendChild(a);a.click();document.body.removeChild(a);seen.add(l.href);if(i===fresh.length-1){localStorage.setItem(KEY,JSON.stringify([...seen]));alert('maimai \u{1F4F8} Downloaded '+fresh.length+' new photo'+(fresh.length>1?'s':'')+'!');}},i*800);});})();
```

IMPORTANT:

Make sure it starts with:

```txt
javascript:
```

---

# Album Page

Open:

:contentReference[oaicite:0]{index=0}

Then press the bookmark.

It will:
- download only new photos
- skip already-downloaded ones
- automatically name files like:

```txt
maimai_2026-05-23_19-00_MASTER_SongName.jpg
```

---

# Browser Permission Popup

Your browser may ask for:

- multiple downloads permission
- automatic download access

Press:

```txt
Allow
```

Otherwise bulk download may fail.

Firefox users may need to manually allow automatic downloads in browser settings.

---

# Reset Download History

If needed, open browser console with:

```txt
F12
```

Go to:

```txt
Console
```

Then run:

```js
localStorage.removeItem('maimai_seen_v1')
```

This makes the bookmarklet treat all photos as new again.

---

# Safety

This project:

- runs locally on your PC only
- does not upload data anywhere
- does not connect to third-party servers
- only accesses the maimai DX NET album page while you are logged in

---

# Notes

- Uses browser localStorage only
- Only moves files starting with:

```txt
maimai_
```

---

# Troubleshooting

## Bookmarklet Does Nothing

Check:
- You are on the correct album page
- The bookmark starts with `javascript:`
- Automatic downloads are allowed in browser settings

---

## Watcher Is Not Moving Files

Check:
- Python is installed correctly
- Dependencies were installed
- The watcher is running
- File names start with:

```txt
maimai_
```

---

## Python Command Does Not Work

If you see:

```txt
'python' is not recognized as an internal or external command
```

Python was not added to PATH.

Reinstall Python and enable:

```txt
Add Python to PATH
```

---

# Disclaimer

This project is unofficial and is not affiliated with :contentReference[oaicite:1]{index=1} or maimai DX.

Use at your own discretion.

---

# License

MIT
