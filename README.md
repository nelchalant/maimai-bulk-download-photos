# maimai Photo Tools

Automatically download and organize your maimai DX NET photos.

This setup includes:

- A bookmarklet that downloads new photos
- A Python watcher that automatically moves them into a separate MaiMai folder

Windows only.

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

Open Command Prompt and run:

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

---

# Step 3 — Set Your MaiMai Folder

Inside the script, edit:

```python
MAIMAI_FOLDER = Path(r"C:\Users\YourName\Pictures\MaiMai")
```

Change it if you want another folder.

---

# Step 4 — Run the Watcher

Run:

```bash
pythonw C:\Users\YourName\maimai_watcher.py
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

Create:

```txt
maimai_watcher.vbs
```

Paste:

```vb
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw C:\Users\YourName\maimai_watcher.py", 0, False
```

Save it.

Now the watcher starts automatically every time Windows boots.

---

# Bookmarklet Setup

1. Create a new bookmark and name it whatever you want
2. Paste this in the URL:

```txt
javascript:(function(){const KEY='maimai_seen_v1';const seen=new Set(JSON.parse(localStorage.getItem(KEY)||'[]'));const links=[...document.querySelectorAll('a[href*="/img/photo/user/"]')];const fresh=links.filter(l=>!seen.has(l.href));if(!fresh.length){alert('maimai \u{1F4F8} All photos already saved! Nothing new.');return;}fresh.forEach((l,i)=>{setTimeout(()=>{const card=l.closest('[class*="score_back"]');const date=(card?.querySelector('.block_info')?.textContent||'').trim().replace(/\//g,'-').replace(/\s+/g,'_');const song=(card?.querySelector('.black_block')?.textContent||'photo').trim().replace(/[\\/:*?"<>|]/g,'').replace(/\s+/g,'_').substring(0,35);const diff=(card?.querySelector('[src*="diff_"]')?.src||'').match(/diff_(\w+)\./)?.[1]||'';const a=document.createElement('a');a.href=l.href;a.download='maimai_'+String(i+1).padStart(2,'0')+'_'+date+'_'+diff.toUpperCase()+'_'+song+'.jpg';document.body.appendChild(a);a.click();document.body.removeChild(a);seen.add(l.href);if(i===fresh.length-1){localStorage.setItem(KEY,JSON.stringify([...seen]));alert('maimai \u{1F4F8} Downloaded '+fresh.length+' new photo'+(fresh.length>1?'s':'')+'!');}},i*800);});})();
```

into the bookmark URL
3. Make sure it starts with:

```txt
javascript:
```

---

# Album Page

Open:

https://maimaidx-eng.com/maimai-mobile/playerData/photo/

Then press the bookmarklet.

It will:
- download only new photos
- skip already-downloaded ones
- automatically name files like:

```txt
maimai_2026-05-23_19-00_MASTER_SongName.jpg
```

---

# Reset Download History

If needed, run this in browser console:

```js
localStorage.removeItem('maimai_seen_v1')
```

---

# Notes

- Runs locally only
- No data is uploaded anywhere
- Uses browser localStorage only
- Only moves files starting with:

```txt
maimai_
```

---

# License

MIT
