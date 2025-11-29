"""
Job Application Optimizer API - Alternative Entry Point
FastAPI Backend with Google Gemini API Integration
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import os
from pathlib import Path

# Import routers
from api import resume, company, documents, analysis

# Ensure required directories exist
Path("uploads").mkdir(exist_ok=True)
Path("outputs").mkdir(exist_ok=True)

# Initialize FastAPI app
app = FastAPI(
    title="Job Application Optimizer API",
    description="AI-powered job application optimization with ATS checking and document generation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static file directories
try:
    app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
except Exception as e:
    print(f"Warning: Could not mount static directories: {e}")

# Include API routers
app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(company.router, prefix="/api/company", tags=["Company"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Job Application Optimizer API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "resume_upload": "/api/resume/upload",
            "resume_analyze": "/api/resume/analyze",
            "ats_check": "/api/resume/ats-check",
            "company_research": "/api/company/research",
            "generate_documents": "/api/documents/generate",
            "recommendations": "/api/analysis/recommendations"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "job-optimizer-api",
        "version": "1.0.0"
    }


@app.get("/info")
async def app_info():
    """Application information and configuration"""
    return {
        "app_name": "Job Application Optimizer",
        "version": "1.0.0",
        "description": "AI-powered job application optimization",
        "features": [
            "Resume Analysis",
            "ATS Compatibility Check",
            "Company Research",
            "Document Generation",
            "Personalized Recommendations"
        ],
        "ai_model": "Google Gemini",
        "supported_formats": ["PDF"],
        "output_formats": ["DOCX", "JSON"]
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    # Run the application
    print("Starting Job Application Optimizer API...")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative Docs: http://localhost:8000/redoc")
    print("Health Check: http://localhost:8000/health")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )
