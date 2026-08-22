@echo off
title Keresztény AI Termékgenerátor & Munkaállomás
chcp 65001 >nul
cd /d "%~dp0"
echo [INFO] Keresztény AI Termékgenerátor & Munkaállomás indítása...
echo [INFO] Helyi elérés: http://localhost:8501
start "" "http://localhost:8501"
python -X utf8 -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
