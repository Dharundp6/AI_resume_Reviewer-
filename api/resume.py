"""
Resume API Endpoints
Handles resume upload and analysis
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from models.schemas import ResumeAnalysisResponse, ATSScoreResponse
from services import gemini_service, pdf_service
import os
import aiofiles

router = APIRouter()


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and extract text from resume PDF
    
    Args:
        file: PDF file upload
        
    Returns:
        Extracted resume text
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read file content
        content = await file.read()
        
        # Extract text from PDF
        resume_text = pdf_service.extract_text_from_bytes(content)
        
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")
        
        return {
            "success": True,
            "filename": file.filename,
            "resume_text": resume_text,
            "text_length": len(resume_text)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")


@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    resume_text: str = Form(...),
    job_role: str = Form(...),
    job_description: str = Form(None)
):
    """
    Analyze resume for a specific job role
    
    Args:
        resume_text: Full text of the resume
        job_role: Target job role/title
        job_description: Optional job description
        
    Returns:
        Resume analysis with scores and recommendations
    """
    try:
        analysis = await gemini_service.analyze_resume(
            resume_text=resume_text,
            job_role=job_role,
            job_description=job_description
        )
        
        return ResumeAnalysisResponse(**analysis)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@router.post("/ats-check", response_model=ATSScoreResponse)
async def check_ats_compatibility(
    resume_text: str = Form(...),
    job_description: str = Form(None)
):
    """
    Check ATS (Applicant Tracking System) compatibility
    
    Args:
        resume_text: Full text of the resume
        job_description: Optional job description
        
    Returns:
        ATS compatibility score and recommendations
    """
    try:
        ats_analysis = await gemini_service.analyze_ats_compatibility(
            resume_text=resume_text,
            job_description=job_description
        )
        
        return ATSScoreResponse(**ats_analysis)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking ATS compatibility: {str(e)}")
