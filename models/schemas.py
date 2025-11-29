"""
Pydantic models for request and response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ResumeAnalysisRequest(BaseModel):
    """Request model for resume analysis"""
    job_role: str = Field(..., description="Target job role/title")
    company_name: str = Field(..., description="Company name")
    job_description: Optional[str] = Field(None, description="Job description (optional)")


class ResumeAnalysisResponse(BaseModel):
    """Response model for resume analysis"""
    overall_score: float = Field(..., ge=1, le=10, description="Overall resume score (1-10)")
    strengths: List[str] = Field(..., description="Resume strengths")
    skills_to_emphasize: List[str] = Field(..., description="Skills to emphasize")
    keywords_to_add: List[str] = Field(..., description="Keywords to add")
    experience_to_highlight: List[str] = Field(..., description="Experience to highlight")
    gaps_to_address: List[str] = Field(..., description="Gaps to address")
    improvement_areas: List[str] = Field(..., description="Areas for improvement")


class ATSScoreResponse(BaseModel):
    """Response model for ATS compatibility analysis"""
    ats_score: int = Field(..., ge=0, le=100, description="ATS compatibility score (0-100)")
    keyword_match: int = Field(..., ge=0, le=100, description="Keyword match percentage")
    formatting_issues: List[str] = Field(..., description="Formatting issues found")
    missing_keywords: List[str] = Field(..., description="Missing keywords")
    strengths: List[str] = Field(..., description="ATS strengths")
    recommendations: List[str] = Field(..., description="ATS recommendations")


class CompanyResearchResponse(BaseModel):
    """Response model for company research"""
    company_overview: str = Field(..., description="Company overview")
    mission_and_values: List[str] = Field(..., description="Mission and values")
    recent_news: List[str] = Field(..., description="Recent news")
    industry_position: str = Field(..., description="Industry position")
    culture: str = Field(..., description="Company culture")
    key_leadership: List[str] = Field(..., description="Key leadership")
    challenges: List[str] = Field(..., description="Current challenges")
    opportunities: List[str] = Field(..., description="Opportunities")


class RecommendationsResponse(BaseModel):
    """Response model for personalized recommendations"""
    resume_alignment: List[str] = Field(..., description="Resume alignment actions")
    cover_letter_talking_points: List[str] = Field(..., description="Cover letter talking points")
    cultural_fit: List[str] = Field(..., description="Cultural fit demonstrations")
    interview_questions: List[str] = Field(..., description="Potential interview questions")
    preparation_tips: List[str] = Field(..., description="Preparation tips")
    next_steps: List[str] = Field(..., description="Next steps")


class DocumentGenerationRequest(BaseModel):
    """Request model for document generation"""
    resume_text: str = Field(..., description="Original resume text")
    job_role: str = Field(..., description="Target job role")
    company_name: str = Field(..., description="Company name")
    analysis: dict = Field(..., description="Resume analysis data")
    ats_score: dict = Field(..., description="ATS score data")
    company_research: dict = Field(..., description="Company research data")


class DocumentGenerationResponse(BaseModel):
    """Response model for document generation"""
    optimized_resume: str = Field(..., description="Optimized resume content")
    cover_letter: str = Field(..., description="Cover letter content")
    resume_file_path: Optional[str] = Field(None, description="Path to resume file")
    cover_letter_file_path: Optional[str] = Field(None, description="Path to cover letter file")
