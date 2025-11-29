"""
PDF Processing Service
Handles PDF file operations
"""

from PyPDF2 import PdfReader
from typing import BinaryIO
import io


class PDFService:
    """Service for PDF processing operations"""
    
    @staticmethod
    def extract_text_from_pdf(file: BinaryIO) -> str:
        """
        Extract text content from PDF file
        
        Args:
            file: Binary file object (PDF)
            
        Returns:
            Extracted text content
        """
        try:
            # Read the PDF
            pdf_reader = PdfReader(file)
            
            # Extract text from all pages
            text_content = []
            for page in pdf_reader.pages:
                text_content.append(page.extract_text())
            
            # Join all pages with newlines
            full_text = "\n\n".join(text_content)
            
            return full_text.strip()
            
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_bytes(pdf_bytes: bytes) -> str:
        """
        Extract text from PDF bytes
        
        Args:
            pdf_bytes: PDF file as bytes
            
        Returns:
            Extracted text content
        """
        file_obj = io.BytesIO(pdf_bytes)
        return PDFService.extract_text_from_pdf(file_obj)


# Create singleton instance
pdf_service = PDFService()
