# Jazira Download Manager (JDM)

Free download manager for Windows — no serial, no activation.

## Features
- Multi-connection downloads (1–32 connections per file) with dynamic splitting
- Pause / resume, even after closing the app or losing the connection
- Speed limiter and a download queue (max simultaneous downloads)
- Scheduler: start and stop downloads at set times on chosen days
- Browser capture for Chrome / Edge (extension in `extension/`)
- Tray icon, completion notifications, optional start with Windows

## Build the installer (GitHub Actions)
1. Upload this folder to a new GitHub repository.
2. Open **Actions → Build Windows Installer → Run workflow**.
3. Download `JDM-Setup` from the finished run.
   Pushing a tag like `v1.0.0` also publishes it under **Releases**.

## Build locally (Windows)
```
pip install -r requirements.txt pyinstaller
pyinstaller --noconfirm --windowed --name JDM --icon assets/jdm.ico --add-data "assets;assets" --paths app app/main.py
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\jdm.iss
```

## Install the browser extension
1. Open `chrome://extensions` (or `edge://extensions`).
2. Turn on **Developer mode**.
3. Click **Load unpacked** and choose `C:\Program Files\JDM\extension`.

When JDM is closed, the browser downloads files normally.

## Project layout
```
app/main.py      UI (PySide6), scheduler, tray
app/engine.py    download engine
app/bridge.py    local bridge for the extension (127.0.0.1:9614)
extension/       Chrome / Edge extension (Manifest V3)
installer/       Inno Setup script
tests/           engine tests
```
