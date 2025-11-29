"""
Analysis API Endpoints
Handles generating comprehensive recommendations
"""

from fastapi import APIRouter, HTTPException, Body
from models.schemas import RecommendationsResponse
from services import gemini_service
from typing import Dict, Any

router = APIRouter()


@router.post("/recommendations", response_model=RecommendationsResponse)
async def generate_recommendations(
    job_role: str = Body(...),
    company_name: str = Body(...),
    analysis: Dict[str, Any] = Body(...),
    ats_score: Dict[str, Any] = Body(...),
    company_research: Dict[str, Any] = Body(...)
):
    """
    Generate personalized recommendations based on all analyses
    
    Args:
        job_role: Target job role
        company_name: Company name
        analysis: Resume analysis data
        ats_score: ATS score data
        company_research: Company research data
        
    Returns:
        Comprehensive personalized recommendations
    """
    try:
        recommendations = await gemini_service.generate_recommendations(
            job_role=job_role,
            company_name=company_name,
            analysis=analysis,
            ats_score=ats_score,
            company_research=company_research
        )
        
        return RecommendationsResponse(**recommendations)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")
