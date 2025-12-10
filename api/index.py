"""
Vercel Serverless Function Entry Point
This file exports the FastAPI app for Vercel's Python runtime using Mangum adapter
"""
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app
from mangum import Mangum

# Mangum is an adapter for running ASGI applications (like FastAPI) in AWS Lambda and Vercel
# It wraps the FastAPI app to work with serverless function event/context model
handler = Mangum(app, lifespan="off")
