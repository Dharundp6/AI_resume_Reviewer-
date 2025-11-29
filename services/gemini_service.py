"""
Google Gemini AI Service
Handles all AI model interactions
"""

import google.generativeai as genai
import json
import re
from typing import Dict, Any
from core.config import settings


class GeminiService:
    """Service class for Google Gemini AI interactions"""
    
    def __init__(self):
        """Initialize Gemini service with API key"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        
    async def generate_content(self, prompt: str, temperature: float = None) -> str:
        """
        Generate content using Gemini API
        
        Args:
            prompt: The prompt to send to Gemini
            temperature: Temperature for generation (0.0-1.0)
            
        Returns:
            Generated text response
        """
        try:
            generation_config = genai.GenerationConfig(
                temperature=temperature or settings.GEMINI_TEMPERATURE,
                max_output_tokens=settings.GEMINI_MAX_TOKENS,
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    async def generate_json_response(self, prompt: str) -> Dict[str, Any]:
        """
        Generate JSON response from Gemini
        
        Args:
            prompt: The prompt requesting JSON output
            
        Returns:
            Parsed JSON response as dictionary
        """
        response_text = await self.generate_content(prompt, temperature=0.3)
        
        # Clean up response - remove markdown code blocks if present
        cleaned_text = response_text.strip()
        cleaned_text = re.sub(r'```json\s*', '', cleaned_text)
        cleaned_text = re.sub(r'```\s*$', '', cleaned_text)
        cleaned_text = cleaned_text.strip()
        
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            # If JSON parsing fails, try to extract JSON from text
            json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            raise Exception(f"Failed to parse JSON response: {str(e)}")
    
    async def analyze_resume(
        self,
        resume_text: str,
        job_role: str,
        job_description: str = None
    ) -> Dict[str, Any]:
        """
        Analyze resume for a specific job role
        
        Args:
            resume_text: Full text of the resume
            job_role: Target job role/title
            job_description: Optional job description
            
        Returns:
            Dictionary with resume analysis
        """
        prompt = f"""You are an expert resume analyst and career coach. Analyze this resume for a {job_role} position.

RESUME CONTENT:
{resume_text}

JOB DESCRIPTION:
{job_description or 'No specific job description provided'}

Provide a comprehensive analysis in the following JSON format. YOUR ENTIRE RESPONSE MUST BE VALID JSON ONLY. DO NOT INCLUDE ANY TEXT OUTSIDE THE JSON STRUCTURE.

{{
  "overall_score": 7.5,
  "strengths": ["strength 1", "strength 2", "strength 3", "strength 4"],
  "skills_to_emphasize": ["skill 1 with reason", "skill 2 with reason", "skill 3 with reason", "skill 4 with reason"],
  "keywords_to_add": ["keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5"],
  "experience_to_highlight": ["experience point 1", "experience point 2", "experience point 3"],
  "gaps_to_address": ["gap 1 with suggestion", "gap 2 with suggestion"],
  "improvement_areas": ["area 1 with specific suggestion", "area 2 with specific suggestion", "area 3 with specific suggestion"]
}}"""

        return await self.generate_json_response(prompt)
    
    async def analyze_ats_compatibility(
        self,
        resume_text: str,
        job_description: str = None
    ) -> Dict[str, Any]:
        """
        Analyze ATS (Applicant Tracking System) compatibility
        
        Args:
            resume_text: Full text of the resume
            job_description: Optional job description
            
        Returns:
            Dictionary with ATS analysis
        """
        prompt = f"""You are an ATS (Applicant Tracking System) expert. Analyze this resume for ATS compatibility.

RESUME CONTENT:
{resume_text}

JOB DESCRIPTION:
{job_description or 'General analysis'}

Provide ATS analysis in the following JSON format. YOUR ENTIRE RESPONSE MUST BE VALID JSON ONLY.

{{
  "ats_score": 75,
  "keyword_match": 65,
  "formatting_issues": ["issue 1", "issue 2", "issue 3"],
  "missing_keywords": ["keyword 1", "keyword 2", "keyword 3", "keyword 4"],
  "strengths": ["ATS strength 1", "ATS strength 2", "ATS strength 3"],
  "recommendations": ["recommendation 1", "recommendation 2", "recommendation 3", "recommendation 4"]
}}"""

        return await self.generate_json_response(prompt)
    
    async def research_company(self, company_name: str) -> Dict[str, Any]:
        """
        Research company information
        
        Args:
            company_name: Name of the company to research
            
        Returns:
            Dictionary with company research
        """
        prompt = f"""Research the company "{company_name}" and provide comprehensive, up-to-date information. Focus on factual, verifiable information.

Provide your research in the following JSON format. YOUR ENTIRE RESPONSE MUST BE VALID JSON ONLY.

{{
  "company_overview": "brief overview in 2-3 sentences",
  "mission_and_values": ["value 1", "value 2", "value 3", "value 4"],
  "recent_news": ["news item 1", "news item 2", "news item 3"],
  "industry_position": "description of market position and competitiveness",
  "culture": "description of company culture and work environment",
  "key_leadership": ["leader 1 with role", "leader 2 with role", "leader 3 with role"],
  "challenges": ["challenge 1", "challenge 2"],
  "opportunities": ["opportunity 1", "opportunity 2", "opportunity 3"]
}}"""

        return await self.generate_json_response(prompt)
    
    async def generate_recommendations(
        self,
        job_role: str,
        company_name: str,
        analysis: Dict[str, Any],
        ats_score: Dict[str, Any],
        company_research: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate personalized recommendations
        
        Args:
            job_role: Target job role
            company_name: Company name
            analysis: Resume analysis data
            ats_score: ATS score data
            company_research: Company research data
            
        Returns:
            Dictionary with recommendations
        """
        prompt = f"""You are a career strategist. Based on the resume analysis and company research, provide personalized recommendations for applying to {company_name} for a {job_role} position.

RESUME ANALYSIS:
{json.dumps(analysis, indent=2)}

ATS ANALYSIS:
{json.dumps(ats_score, indent=2)}

COMPANY RESEARCH:
{json.dumps(company_research, indent=2)}

Provide actionable recommendations in the following JSON format. YOUR ENTIRE RESPONSE MUST BE VALID JSON ONLY.

{{
  "resume_alignment": ["specific change 1", "specific change 2", "specific change 3", "specific change 4"],
  "cover_letter_talking_points": ["point 1", "point 2", "point 3", "point 4", "point 5"],
  "cultural_fit": ["how to demonstrate fit 1", "how to demonstrate fit 2", "how to demonstrate fit 3"],
  "interview_questions": ["potential question 1", "potential question 2", "potential question 3", "potential question 4"],
  "preparation_tips": ["tip 1", "tip 2", "tip 3", "tip 4"],
  "next_steps": ["action 1", "action 2", "action 3"]
}}"""

        return await self.generate_json_response(prompt)
    
    async def generate_optimized_resume(
        self,
        resume_text: str,
        job_role: str,
        company_name: str,
        analysis: Dict[str, Any],
        ats_score: Dict[str, Any]
    ) -> str:
        """
        Generate an optimized version of the resume
        
        Args:
            resume_text: Original resume text
            job_role: Target job role
            company_name: Company name
            analysis: Resume analysis data
            ats_score: ATS score data
            
        Returns:
            Optimized resume text
        """
        prompt = f"""Based on all the analysis, create an optimized version of this resume for the {job_role} position at {company_name}.

ORIGINAL RESUME:
{resume_text}

ANALYSIS INSIGHTS:
- Skills to emphasize: {', '.join(analysis.get('skills_to_emphasize', []))}
- Keywords to add: {', '.join(analysis.get('keywords_to_add', []))}
- ATS recommendations: {', '.join(ats_score.get('recommendations', []))}

Create a professional, ATS-friendly resume. Format it in a clean, structured way with clear sections. 
Use proper formatting with section headers, bullet points, and clear structure.
Return ONLY the resume text, no additional commentary or markdown formatting."""

        return await self.generate_content(prompt, temperature=0.5)
    
    async def generate_cover_letter(
        self,
        job_role: str,
        company_name: str,
        company_research: Dict[str, Any],
        recommendations: Dict[str, Any]
    ) -> str:
        """
        Generate a personalized cover letter
        
        Args:
            job_role: Target job role
            company_name: Company name
            company_research: Company research data
            recommendations: Recommendations data
            
        Returns:
            Cover letter text
        """
        prompt = f"""Create a compelling cover letter for {job_role} position at {company_name}.

KEY INFORMATION:
- Company values: {', '.join(company_research.get('mission_and_values', []))}
- Talking points: {', '.join(recommendations.get('cover_letter_talking_points', []))}
- Cultural fit: {', '.join(recommendations.get('cultural_fit', []))}

Write a professional, engaging cover letter that demonstrates enthusiasm and fit. 
Use a professional business letter format with proper greeting, body paragraphs, and closing.
Return ONLY the cover letter text, no additional commentary."""

        return await self.generate_content(prompt, temperature=0.7)


# Create a singleton instance
gemini_service = GeminiService()
