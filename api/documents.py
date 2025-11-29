"""
Document Generation API Endpoints
Handles creating optimized resume and cover letter
"""

from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import FileResponse
from models.schemas import DocumentGenerationResponse
from services import gemini_service, document_service
from typing import Dict, Any
import os

router = APIRouter()


@router.post("/generate", response_model=DocumentGenerationResponse)
async def generate_documents(
    resume_text: str = Body(...),
    job_role: str = Body(...),
    company_name: str = Body(...),
    analysis: Dict[str, Any] = Body(...),
    ats_score: Dict[str, Any] = Body(...),
    company_research: Dict[str, Any] = Body(...),
    recommendations: Dict[str, Any] = Body(...)
):
    """
    Generate optimized resume and cover letter
    
    Args:
        resume_text: Original resume text
        job_role: Target job role
        company_name: Company name
        analysis: Resume analysis data
        ats_score: ATS score data
        company_research: Company research data
        recommendations: Recommendations data
        
    Returns:
        Generated documents with file paths
    """
    try:
        # Generate optimized resume
        optimized_resume = await gemini_service.generate_optimized_resume(
            resume_text=resume_text,
            job_role=job_role,
            company_name=company_name,
            analysis=analysis,
            ats_score=ats_score
        )
        
        # Generate cover letter
        cover_letter = await gemini_service.generate_cover_letter(
            job_role=job_role,
            company_name=company_name,
            company_research=company_research,
            recommendations=recommendations
        )
        
        # Create Word documents
        resume_file_path = document_service.create_resume_docx(
            content=optimized_resume,
            company_name=company_name
        )
        
        cover_letter_file_path = document_service.create_cover_letter_docx(
            content=cover_letter,
            company_name=company_name
        )
        
        return DocumentGenerationResponse(
            optimized_resume=optimized_resume,
            cover_letter=cover_letter,
            resume_file_path=resume_file_path,
            cover_letter_file_path=cover_letter_file_path
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating documents: {str(e)}")


@router.get("/download/{filename}")
async def download_document(filename: str):
    """
    Download a generated document
    
    Args:
        filename: Name of the file to download
        
    Returns:
        File download response
    """
    try:
        file_path = os.path.join("outputs", filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")
