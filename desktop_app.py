"""
Standalone Desktop Launcher for Keresztény AI Munkaállomás
===========================================================
Launches Streamlit in background and opens an Edge/Chrome Application Mode window
(No URL bar, no browser tabs, native desktop feel).
"""

import os
import sys
import time
import subprocess
import webbrowser
import shutil


def find_browser_executable():
    """Finds Google Chrome or Microsoft Edge executable on Windows."""
    paths = [
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe")
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    app_py = os.path.join(root_dir, "app", "app.py")
    url = "http://localhost:8501"

    print("================================================================")
    print("✝️  KERESZTÉNY AI MUNKAÁLLOMÁS · ASZTALI MÓD (APP WINDOW)")
    print("================================================================")
    print("Indítás folyamatban...")

    # Start streamlit server in background
    cmd = [sys.executable, "-X", "utf8", "-m", "streamlit", "run", app_py, "--server.address", "0.0.0.0", "--server.port", "8501", "--server.headless", "true"]
    server_process = subprocess.Popen(cmd, cwd=root_dir)

    time.sleep(2.5)

    browser = find_browser_executable()
    if browser:
        print(f"Böngésző alkalmazás ablak megnyitása: {browser}")
        subprocess.Popen([browser, f"--app={url}", "--window-size=1400,920"])
    else:
        print("Megnyitás az alapértelmezett böngészőben...")
        webbrowser.open(url)

    try:
        server_process.wait()
    except KeyboardInterrupt:
        server_process.terminate()


if __name__ == "__main__":
    main()
