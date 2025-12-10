"""
Vercel Serverless Function Entry Point
Exports the FastAPI app for Vercel's Python runtime (ASGI support)
"""
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the FastAPI app
from app import app as application

# Vercel's Python runtime supports ASGI apps directly
# Export the app instance - Vercel will detect it automatically
app = application
