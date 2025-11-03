"""PDF extraction service using VLM and text extraction."""
import pdfplumber
import pypdf
from typing import List, Dict, Any, Optional
from pathlib import Path
import aiofiles
import asyncio
from ...infrastructure.logging import get_logger
from ..models.grok_model import GrokModel


logger = get_logger(__name__)


class PDFExtractorService:
    """Service for extracting data from PDFs."""
    
    def __init__(self, grok_model: Optional[GrokModel] = None):
        self.grok_model = grok_model
    
    async def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF."""
        try:
            text_content = []
            
            # Try pdfplumber first (better for structured data)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
            
            if not text_content:
                # Fallback to pypdf
                with open(pdf_path, 'rb') as file:
                    reader = pypdf.PdfReader(file)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            text_content.append(text)
            
            return "\n\n".join(text_content)
        except Exception as e:
            logger.error("pdf_extraction_failed", path=pdf_path, error=str(e))
            raise
    
    async def extract_provider_data(self, pdf_path: str) -> Dict[str, Any]:
        """Extract provider data from PDF using VLM and text extraction."""
        # Extract text first
        text = await self.extract_text(pdf_path)
        
        if not self.grok_model:
            # Fallback to rule-based extraction
            return self._rule_based_extraction(text)
        
        # Use Grok/VLM for intelligent extraction
        try:
            prompt = f"""Extract provider information from this document text. 
Return structured JSON with fields: first_name, last_name, organization_name, 
phone, email, address, city, state, postal_code, license_number, state, 
license_type, specialties, taxonomy.

Document text:
{text[:2000]}  # Limit to avoid token limits
"""
            
            from smolagents.models import ChatMessage
            messages = [ChatMessage(role="user", content=prompt)]
            response = await self.grok_model.generate(messages)
            
            # Try to parse JSON from response
            import json
            content = response.content if hasattr(response, 'content') else str(response)
            
            # Extract JSON from response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            
            # Fallback to rule-based
            return self._rule_based_extraction(text)
        except Exception as e:
            logger.warning("vlm_extraction_failed", error=str(e))
            return self._rule_based_extraction(text)
    
    def _rule_based_extraction(self, text: str) -> Dict[str, Any]:
        """Rule-based extraction as fallback."""
        import re
        data = {}
        
        # Extract phone
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            data['phone'] = phones[0]
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            data['email'] = emails[0]
        
        # Extract ZIP code
        zip_pattern = r'\b\d{5}(?:-\d{4})?\b'
        zips = re.findall(zip_pattern, text)
        if zips:
            data['postal_code'] = zips[0]
        
        # Extract name patterns
        name_pattern = r'([A-Z][a-z]+\s+[A-Z][a-z]+)'  # Simple name pattern
        names = re.findall(name_pattern, text)
        if names:
            parts = names[0].split()
            if len(parts) >= 2:
                data['first_name'] = parts[0]
                data['last_name'] = ' '.join(parts[1:])
        
        return data

