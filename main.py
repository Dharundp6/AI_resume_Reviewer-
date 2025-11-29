"""
Job Application Optimizer API - Main Application Entry Point
FastAPI Backend with Google Gemini API Integration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api import resume, company, documents, analysis

# Initialize FastAPI app
app = FastAPI(
    title="Job Application Optimizer API",
    description="AI-powered job application optimization with ATS checking and document generation",
    version="1.0.0"
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
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Include routers
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
        "docs": "/docs",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "job-optimizer-api"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
