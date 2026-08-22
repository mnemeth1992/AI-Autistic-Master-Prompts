@echo off
title Keresztény AI Munkaállomás - Asztali Mód
chcp 65001 >nul
cd /d "%~dp0"
echo [INFO] Keresztény AI Asztali Munkaállomás indítása keret nélküli ablakban...
python -X utf8 desktop_app.py
pause
