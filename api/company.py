"""
Company Research API Endpoints
Handles company information research
"""

from fastapi import APIRouter, HTTPException, Form
from models.schemas import CompanyResearchResponse
from services import gemini_service

router = APIRouter()


@router.post("/research", response_model=CompanyResearchResponse)
async def research_company(company_name: str = Form(...)):
    """
    Research company information
    
    Args:
        company_name: Name of the company to research
        
    Returns:
        Comprehensive company research data
    """
    try:
        research_data = await gemini_service.research_company(company_name)
        
        return CompanyResearchResponse(**research_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error researching company: {str(e)}")
