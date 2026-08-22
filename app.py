"""
Main Entry Point for Streamlit Cloud & Local Deployment
======================================================
Redirects execution to the modular v4.0 application package (app/app.py).
Ensures 100% parity between Streamlit Cloud and local desktop execution.
"""
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, "app")

if app_dir not in sys.path:
    sys.path.insert(0, app_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import main from app.app
from app.app import main

if __name__ == "__main__":
    main()
