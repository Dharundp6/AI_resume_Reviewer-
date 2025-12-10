"""
Vercel Serverless Function Entry Point
This file exports the FastAPI app for Vercel's Python runtime
"""
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app

# Vercel expects a variable named 'app' or 'handler'
# Export the FastAPI app instance
handler = app
