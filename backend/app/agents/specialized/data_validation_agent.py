"""Data Validation Agent for provider contact validation."""
from typing import List, Dict, Any
from smolagents import CodeAgent, Tool
from ...domain.enriched_entities import EnrichedProvider, DataElementConfidence, DataSource, ValidationStatus
from ...infrastructure.models.grok_model import GrokModel
from ...infrastructure.services.confidence_scoring import ConfidenceScoringService
from ..tools.nppes_tool import NppesTool
from ..tools.web_scraping_tool import WebScrapingTool
from ..tools.web_search_tool import WebSearchTool
from ..tools.google_maps_tool import GoogleMapsTool
from ...infrastructure.logging import get_logger


logger = get_logger(__name__)


class DataValidationAgent:
    """Agent for validating provider contact information."""
    
    def __init__(self, model: GrokModel):
        tools: List[Tool] = [
            NppesTool(),
            WebScrapingTool(),
            WebSearchTool(),
            GoogleMapsTool(),
        ]
        self.agent = CodeAgent(tools=tools, model=model, name="data_validation_agent")
        self.confidence_scoring = ConfidenceScoringService()
    
    async def validate_provider_contact(self, provider: EnrichedProvider) -> EnrichedProvider:
        """Validate provider contact information."""
        logger.info("validating_provider_contact", npi=provider.npi)
        
        # Build validation prompt
        prompt = f"""Validate the contact information for provider {provider.first_name} {provider.last_name} (NPI: {provider.npi}).

Current information:
- Phone: {provider.phone or 'Not provided'}
- Email: {provider.email or 'Not provided'}
- Address: {provider.address_line1}, {provider.city}, {provider.state} {provider.postal_code}
- Website: {provider.website or 'Not provided'}

Tasks:
1. Use nppes_search to verify provider information from NPPES registry
2. If website is available, use web_scrape_provider to verify contact information
3. Use google_maps_lookup to cross-validate location and phone
4. Use web_search to find additional provider information if needed
5. Identify any discrepancies between sources
6. Generate confidence scores for each data element

Return a summary with validated information and confidence scores.
"""
        
        try:
            result = await self.agent.run(prompt)
            
            # Process results and update provider
            provider = self._process_validation_results(provider, result)
            
            return provider
        except Exception as e:
            logger.error("validation_failed", npi=provider.npi, error=str(e))
            provider.validation_status = ValidationStatus.REQUIRES_REVIEW
            provider.validation_notes.append(f"Validation failed: {str(e)}")
            return provider
    
    def _process_validation_results(self, provider: EnrichedProvider, agent_result: Any) -> EnrichedProvider:
        """Process agent results and update provider with confidence scores."""
        # Extract information from agent result
        # This is a simplified version - in production, you'd parse structured output
        
        element_confidences: List[DataElementConfidence] = []
        
        # Phone validation
        if provider.phone:
            phone_conf = DataElementConfidence(
                element_name="phone",
                value=provider.phone,
                confidence_score=self.confidence_scoring.calculate_element_confidence(
                    provider.phone, DataSource.NPPES
                ),
                source=DataSource.NPPES,
                verified_at=None,
            )
            element_confidences.append(phone_conf)
            provider.phone_confidence = phone_conf.confidence_score
        
        # Email validation
        if provider.email:
            email_conf = DataElementConfidence(
                element_name="email",
                value=provider.email,
                confidence_score=self.confidence_scoring.calculate_element_confidence(
                    provider.email, DataSource.WEB_SCRAPING
                ),
                source=DataSource.WEB_SCRAPING,
            )
            element_confidences.append(email_conf)
            provider.email_confidence = email_conf.confidence_score
        
        # Address validation
        if provider.address_line1:
            address_conf = DataElementConfidence(
                element_name="address",
                value=f"{provider.address_line1}, {provider.city}, {provider.state}",
                confidence_score=self.confidence_scoring.calculate_element_confidence(
                    provider.address_line1, DataSource.NPPES
                ),
                source=DataSource.NPPES,
            )
            element_confidences.append(address_conf)
            provider.address_confidence = address_conf.confidence_score
        
        # Cross-validate and update
        validated_elements = self.confidence_scoring.cross_validate_elements(element_confidences)
        provider.data_element_confidences = validated_elements
        provider.overall_confidence = self.confidence_scoring.calculate_overall_confidence(validated_elements)
        
        # Update validation status
        if provider.overall_confidence >= 0.8:
            provider.validation_status = ValidationStatus.VALIDATED
        elif any(e.discrepancy_found for e in validated_elements):
            provider.validation_status = ValidationStatus.DISCREPANCY
            provider.requires_manual_review = True
            provider.review_priority = 5
        else:
            provider.validation_status = ValidationStatus.REQUIRES_REVIEW
        
        return provider

