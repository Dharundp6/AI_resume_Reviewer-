"""
Configuration settings for the Job Optimizer API
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    GEMINI_API_KEY: str = "YOUR_GEMINI_API_KEY_HERE"  # Replace with your actual API key
    
    # Alternative API Keys (if you want to support multiple providers)
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Application settings
    APP_NAME: str = "Job Application Optimizer"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # File upload settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    OUTPUT_DIR: str = "outputs"
    
    # Gemini model settings
    GEMINI_MODEL: str = "gemini-flash-latest"  # or "gemini-1.5-flash" for faster/cheaper
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 4096
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
